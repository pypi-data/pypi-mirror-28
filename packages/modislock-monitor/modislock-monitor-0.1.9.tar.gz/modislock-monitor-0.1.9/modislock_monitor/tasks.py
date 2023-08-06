import re

# Async worker
from celery import Celery
from celery.utils.log import get_logger

# Database
from .database import Database, Settings, SettingsValues, Locations, Sensors

# Email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
from .config import load_config

# System calls
from subprocess import PIPE, Popen, run

# File operations
from shutil import copy2

from subprocess import check_output, CalledProcessError

config = load_config()
app = Celery('modis-mon', broker=config.CELERY_BROKER_URL)
logger = get_logger(__name__)
logger.setLevel('DEBUG' if config.DEBUG else 'INFO')


@app.task
def reboot():
    try:
        run(args=['systemctl', 'reboot'], timeout=60)
    except (CalledProcessError, TimeoutError):
        logger.debug('Failed to reboot')
        return {'message': 'Failed to reboot'}
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

        try:
            run(args=['supervisorctl', 'restart', 'admin:*'], stdout=PIPE, stderr=PIPE, timeout=60)
        except (CalledProcessError, TimeoutError):
            logger.debug('Failed to restart admin processes')


@app.task
def factory_reset():
    """Resets to factory defaults

    :return:
    """
    # 1. Reset database
    args = ['mysql', '-u', 'root', '-D', 'modislock']
    try:
        p = Popen(args, stdin=PIPE, stdout=PIPE)
        out, err = p.communicate('SOURCE /etc/modis/modislock_init.sql;\nexit\n'.encode(), timeout=30)
        print(out, err)
    except (CalledProcessError, TimeoutError):
        logger.debug('Failed to restore database to factory defaults')

    # 2. Rename host
    with open('/etc/hostname', 'w') as f:
        f.write('modislock')

    # 3. Reset networking
    copy2('/etc/modis/interfaces.bu', '/etc/network/interfaces')

    # 4. Purge logs

    # 5. Reset passwords

    # 6. Restart system
    try:
        run(args=['systemctl', 'reboot'])
    except (CalledProcessError, TimeoutError):
        logger.debug('Failed to reboot after factory default')


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


@app.task
def update_cpu_temps():
    """Periodic task that records the case and cpu temps to database

        :return:
        """
    case_temp = None
    cpu_temp = None

    try:
        case_temp = check_output(args=['sensors', 'ds3231-i2c-1-68'])
    except CalledProcessError:
        logger.debug('Error in processing case temp')
    except TimeoutError:
        logger.debug('Timeout error in processing case temp')
    except FileNotFoundError:
        logger.debug('Not on a RPi platform')
    else:
        if case_temp:
            case = case_temp.decode().split('\n')
            for lines in case:
                if 'temp' in lines:
                    m = re.search(r' [+-]?(\d{1,3}.\d?)', lines)
                    if m is not None:
                        try:
                            case_temp = int(float(m.group(1)))
                        except ValueError:
                            logger.debug('Value error')

    try:
        cpu_temp = check_output(args=['/DietPi/dietpi/dietpi-cpuinfo', '1'])
    except CalledProcessError:
        logger.error('Error in processing cpu temp')
    except TimeoutError:
        logger.error('Timeout error in processing cpu temp')
    except FileNotFoundError:
        logger.debug('Not on a RPi platform')
    else:
        if cpu_temp:
            cpu_temp = int(cpu_temp)

    with Database() as db:
        sensor_nums = db.session.query(Locations) \
            .join(Sensors, Sensors.locations_id_locations == Locations.id_locations) \
            .filter(Locations.name.like('HOST')).with_entities(Sensors.id_sensors, Sensors.name, Locations.name) \
            .all()
        if sensor_nums is not None:
            for result in sensor_nums:
                sensor_id = result[0]
                if 'CASE' in result[1] and case_temp:
                    db.session.execute('CALL add_reading(' + str(case_temp) + ',' + str(sensor_id) + ')')
                elif 'CPU' in result[1] and cpu_temp:
                    db.session.execute('CALL add_reading(' + str(cpu_temp) + ',' + str(sensor_id) + ')')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Get CPU and Case temps
    sender.add_periodic_task(30.0, update_cpu_temps.s(), name='Retrieve CPU and Case temps')


__all__ = ['app', 'send_async_msg', 'reboot', 'system_reset', 'factory_reset']
