# Async worker
from celery import Celery
from celery.utils.log import get_logger

# Database
from .database import Database, Settings, SettingsValues

# Email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
from .config import load_config

# System calls
from subprocess import PIPE, Popen

# File operations
from shutil import copy2

config = load_config()
app = Celery('modis-mon', broker=config.CELERY_BROKER_URL)
logger = get_logger(__name__)
logger.setLevel('DEBUG' if config.DEBUG else 'INFO')


@app.task
def reboot():
    args = ['systemctl', 'reboot']
    ret = Popen(args, stdout=PIPE, stderr=PIPE, timeout=60)
    ret.communicate()
    return {'message': 'Rebooting now'}


@app.task
def system_reset():
    with Database() as db:
        reset = db.session.query(SettingsValues)\
            .join(Settings, SettingsValues.settings_id_settings == Settings.id_settings)\
            .filter(Settings.settings_name == 'REGISTRATION').first()

        if reset is not None:
            reset.value = 'ENABLED'
            db.session.commit()

        args = ['supervisorctl', 'restart', 'admin:*']
        ret = Popen(args, stdout=PIPE, stderr=PIPE, timeout=60)
        ret.communicate()
        return {'message': 'Successfully reset registration'}


@app.task
def factory_reset():
    # 1. Reset database
    args = ['mysql', '-u', 'root', '-D', 'modislock']
    p = Popen(args, stdin=PIPE, stdout=PIPE)
    out, err = p.communicate('SOURCE /etc/modis/modislock_init.sql;\nexit\n'.encode(), timeout=30)
    print(out, err)

    # 2. Rename host
    with open('/etc/hostname', 'w') as f:
        f.write('modislock')

    # 3. Reset networking
    copy2('/etc/modis/interfaces.bu', '/etc/network/interfaces')

    # 4. Purge logs

    # 5. Reset passwords

    # 6. Restart system

    args = ['systemctl', 'reboot']
    ret = Popen(args, timeout=60)
    ret.communicate()
    return {'message': 'System reset to factory defaults'}


@app.task
def send_async_msg(message, server):
    """
    Send a message using SMTP
    :param message:
    :param server:
    :return:
    """
    COMMASPACE = ', '

    # Create a Container
    msg = MIMEMultipart()
    msg['From'] = message.get('sender')
    msg['To'] = COMMASPACE.join(message.get('destination'))
    msg['Subject'] = message.get('subject')
    msg.preamble = message.get('header')

    # Add body
    body = MIMEText(message.get('body'), 'html')
    msg.attach(body)

    if server.get('use_ssl') is True:
        send = smtplib.SMTP_SSL(server.get('address'), server.get('port'))
    else:
        send = smtplib.SMTP(server.get('address'), server.get('port'))

    send.set_debuglevel(1 if config.DEBUG else 0)

    if server.get('use_tls') is True:
        # Add ttls
        send.ehlo()

        try:
            send.starttls()
        except (smtplib.SMTPHeloError, smtplib.SMTPNotSupportedError) as e:
            logger.debug('Exception starting tls')
        else:
            send.ehlo()
    else:
        # Login
        try:
            send.login(server.get('user'), server.get('password'))
        except (smtplib.SMTPServerDisconnected, smtplib.SMTPAuthenticationError, smtplib.SMTPNotSupportedError) as e:
            logger.debug('Exception on login: ' + e)

    try:
        send.send_message(msg)
    except (smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused) as e:
        logger.debug('Error in sending message')
    # Quit
    send.quit()


__all__ = ['app', 'send_async_msg', 'reboot', 'system_reset', 'factory_reset']
