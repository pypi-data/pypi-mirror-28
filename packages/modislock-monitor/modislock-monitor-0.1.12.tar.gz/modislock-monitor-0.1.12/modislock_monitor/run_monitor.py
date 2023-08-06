import sys
import os
import signal
import time

# Database
from modislock_monitor.database import Database
from sqlalchemy import text

from modislock_monitor import Monitor
from modislock_monitor.extensions import log, mon_config
from modislock_monitor.reset import Reset

# Pins
from modislock_monitor.platform_detection import isRaspberryPi

# GPIO access
if isRaspberryPi:
    import RPi.GPIO as GPIO
else:
    import GPIOEmu as GPIO

# Inserts module path into system search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def testdb(db):
    """Tests if database connection is valid

    :param Database db: database session
    :return bool: connection succeeded or failed
    """
    try:
        db.session.query("1").from_statement(text("SELECT 1")).all()
        return True
    except:
        return False


def signal_handler(signal, frame):
    """Used to handle termination signals from the OS

    :param signal:
    :param frame:
    :return:
    """
    signals = {2: 'SIGINT', 15: 'SIGTERM'}
    log.info('Monitor stopped with signal: {}'.format(signals[signal]))
    raise ServiceExit


class ServiceExit(Exception):
    """Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def main():
    #: Check version of python
    if sys.version_info[:3] < mon_config.REQUIRED_PYTHON_VER:
        log.error("Monitor requires at least Python {}.{}.{}".format(*mon_config.REQUIRED_PYTHON_VER))
        sys.exit(1)

    with Database() as db:
        iterations = 0

        while testdb(db) is not True:
            log.debug('Database not available, waiting..')
            time.sleep(2)
            iterations += 1

            if iterations > 20:
                log.error('Database was not available')
                sys.exit(1)

    #: Initialize the GPIO module and PINs
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(mon_config.DEBUG)
    #: Status LED
    GPIO.setup(mon_config.STATUS_PIN, GPIO.OUT, initial=GPIO.LOW)
    reset_btn = Reset(mon_config.RESET_PIN)

    try:
        monitor = Monitor(port=mon_config.SERIAL_PORT['RPI_PORT'] if isRaspberryPi else mon_config.SERIAL_PORT['PC_PORT'],
                          readers=mon_config.READER_PIN,
                          door_sensors=mon_config.DOOR_PIN)
    except IOError:
        log.debug('Invalid or unavailable serial port')
        sys.exit(1)

    log.info('****Monitor Starting****')
    # Registers signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        monitor.start()

        while True:
            time.sleep(0.5)
            GPIO.output(mon_config.STATUS_PIN, not GPIO.input(mon_config.STATUS_PIN))
    except (KeyboardInterrupt, ServiceExit):
        reset_btn.deinitialize()
        GPIO.cleanup(mon_config.STATUS_PIN)

        # Start threads
        monitor.stop()

        log.info('****Monitor Closing in 5 seconds***')
        time.sleep(5)


if __name__ == '__main__':
    main()
