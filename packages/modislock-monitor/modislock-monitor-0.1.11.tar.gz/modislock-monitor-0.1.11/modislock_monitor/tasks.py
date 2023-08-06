import re

# Async worker
from celery import Celery
from celery.utils.log import get_logger

# Database
from .database import (Database,
                       Settings,
                       SettingsValues,
                       Locations,
                       Sensors,
                       Readings,
                       StaticReadings,
                       ReaderStatus,
                       ReaderSettings)
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError

# Email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
from .config import load_config

# System calls
from subprocess import Popen, run, PIPE, CalledProcessError, TimeoutExpired

# File operations
from shutil import copy2

config = load_config()
app = Celery('modis-mon', broker=config.CELERY_BROKER_URL)
logger = get_logger(__name__)
logger.setLevel('DEBUG' if config.DEBUG else 'INFO')


@app.task
def reboot():
    try:
        run(args=['systemctl', 'reboot'], timeout=60)
    except (CalledProcessError, TimeoutExpired):
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
        except (CalledProcessError, TimeoutExpired):
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
    except (CalledProcessError, TimeoutExpired, FileNotFoundError):
        logger.debug('Failed to restore database to factory defaults')

    # 2. Rename host
    with open('/etc/hostname', 'w') as f:
        f.write('modislock')

    # 3. Reset networking
    try:
        copy2('/etc/modis/interfaces.bu', '/etc/network/interfaces')
    except FileNotFoundError:
        pass

    # 4. Purge logs

    # 5. Reset passwords

    # 6. Restart system
    try:
        run(args=['systemctl', 'reboot'], timeout=10)
    except (CalledProcessError, TimeoutExpired):
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
        case_temp = run(args=['sensors', 'ds3231-i2c-1-68'], stdout=PIPE)
    except CalledProcessError:
        logger.debug('Error in processing case temp')
    except TimeoutExpired:
        logger.debug('Timeout error in processing case temp')
    except FileNotFoundError:
        logger.debug('Not on a RPi platform')
    else:
        if case_temp.returncode == 0 and case_temp.stdout:
            case = case_temp.stdout.decode().split('\n')
            case_temp = None

            for lines in case:
                if 'temp' in lines:
                    m = re.search(r' [+-]?(\d{1,3}.\d?)', lines)
                    if m is not None:
                        try:
                            case_temp = int(float(m.group(1)))
                        except ValueError:
                            logger.debug('Value error')
        else:
            case_temp = None

    try:
        cpu_temp = run(args=['/DietPi/dietpi/dietpi-cpuinfo', '1'], stdout=PIPE)
    except CalledProcessError:
        logger.error('Error in processing cpu temp')
    except TimeoutExpired:
        logger.error('Timeout error in processing cpu temp')
    except FileNotFoundError:
        logger.debug('Not on a RPi platform')
    else:
        if cpu_temp.returncode == 0 and cpu_temp.stdout:
            if re.search(r'^(\d{1,3})', cpu_temp.stdout.decode()):
                cpu_temp = int(cpu_temp.stdout.decode())
        else:
            cpu_temp = None

    if case_temp or cpu_temp:
        with Database() as db:
            sensor_nums = db.session.query(Locations) \
                .join(Sensors, Sensors.locations_id_locations == Locations.id_locations) \
                .filter(Locations.name.like('HOST')).with_entities(Sensors.id_sensors, Sensors.name, Locations.name) \
                .all()
            if sensor_nums is not None:
                for result in sensor_nums:
                    sensor_id = result[0]
                    if 'CASE' in result[1] and case_temp:
                        try:
                            db.session.execute('CALL add_reading(' + str(case_temp) + ',' + str(sensor_id) + ')')
                        except ProgrammingError:
                            pass
                    elif 'CPU' in result[1] and cpu_temp:
                        try:
                            db.session.execute('CALL add_reading(' + str(cpu_temp) + ',' + str(sensor_id) + ')')
                        except ProgrammingError:
                            pass


@app.task
def update_door_status(door_id, status):
    """Update door status

    :param door_id:
    :param status:
    :return:
    """
    with Database() as db:
        query = db.session.query(StaticReadings) \
            .filter(StaticReadings.sensors_id_sensors == door_id) \
            .first()

        if query is not None:
            query.value = 'ACTIVE' if status == 1 else 'INACTIVE'

            try:
                db.session.commit()
            except (IntegrityError, OperationalError):
                db.session.rollback()
                logger.error('Error updating door status in database')


@app.task
def update_reader_status(reader_id, status):
    """Update reader status

    :param reader_id:
    :param status:
    :return:
    """
    with Database() as db:
        query = db.session.query(ReaderStatus) \
            .filter(ReaderStatus.reader_id_reader == reader_id) \
            .one_or_none()

        if query is not None:
            query.status = 'CONNECTED' if status == 1 else 'DISCONNECTED'

            try:
                db.session.commit()
            except (IntegrityError, OperationalError):
                db.session.rollback()
                logger.error('Error updating reader status is database')


@app.task
def update_status_request(sensor_id, value):
    """Update status of sensor

    :param sensor_id:
    :param value:
    :return:
    """

    with Database() as db:
        sensor = db.session.query(ReaderSettings) \
            .join(Locations, ReaderSettings.id_reader == Locations.reader_settings_id_reader) \
            .join(Sensors, Locations.id_locations == Sensors.locations_id_locations) \
            .filter(ReaderSettings.id_reader == sensor_id) \
            .with_entities(Sensors.id_sensors, Sensors.name, ReaderSettings.location_name).all()

        for result in sensor:
            sensor_id = result[0]
            if 'TEMP' in result[1]:
                try:
                    db.session.execute('CALL add_reading(' + str(value["temp"]) + ',' + str(sensor_id) + ')')
                except ProgrammingError:
                    pass
            elif 'VALIDATION' in result[1]:
                try:
                    db.session.execute('CALL add_reading(' + str(value['validations']) + ',' + str(sensor_id) + ')')
                except ProgrammingError:
                    pass
            elif 'DENIED' in result[1]:
                try:
                    db.session.execute('CALL add_reading(' + str(value['denials']) + ',' + str(sensor_id) + ')')
                except ProgrammingError:
                    pass


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Get CPU and Case temps
    sender.add_periodic_task(30.0, update_cpu_temps.s(), name='Retrieve CPU and Case temps')


__all__ = ['app', 'send_async_msg', 'reboot', 'system_reset', 'factory_reset', 'update_cpu_temps',
           'update_door_status', 'update_reader_status', 'update_status_request']
