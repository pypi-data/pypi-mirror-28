
# Extensions
from .extensions import log

# Database
from .database import Database, ReaderStatus
from sqlalchemy.exc import IntegrityError, OperationalError

# Pins
from .platform_detection import isRaspberryPi

# GPIO access
if isRaspberryPi:
    import RPi.GPIO as GPIO
else:
    import GPIOEmu as GPIO


class Reader:
    """Reader status update

    """
    def __init__(self, reader_id, status_pin, reader_name=None, callback=None):
        assert type(reader_id) is int, 'Reader ID should be of int type: %r' % reader_id
        assert type(status_pin) is int, 'Reader output status pin should be of int type: %r' % status_pin

        self.__reader_id = reader_id
        self.__status_pin = status_pin
        self.__reader_name = reader_name if reader_name is not None else 'unknown'
        self.__callback = self._callback if callback is None else callback
        self.__current_status = None

        # Setup PIN
        GPIO.setup(self.status_pin, GPIO.IN)

        # Get initial value
        self.current_status = GPIO.input(self.status_pin)
        # Add event to PIN
        GPIO.add_event_detect(self.status_pin,
                              GPIO.BOTH,
                              callback=self._update_reader_status)

        with Database() as db:
            query = db.session.query(ReaderStatus) \
                .filter(ReaderStatus.reader_id_reader == self.reader_id) \
                .first()

            if query is not None:
                query.status = 'DISCONNECTED' if self.current_status == GPIO.LOW else 'CONNECTED'

                try:
                    db.session.commit()
                except (IntegrityError, OperationalError) as e:
                    db.session.rollback()
                    log.error(e.args[0])
            else:
                reader = ReaderStatus(status='DISCONNECTED' if self.current_status == GPIO.LOW else 'CONNECTED',
                                      reader_id_reader=self.reader_id)
                db.session.add(reader)

                try:
                    db.session.commit()
                except (IntegrityError, OperationalError):
                    db.session.rollback()
                    log.error('Status Monitor Database Error')

    def _callback(self, id, status):
        pass

    def _update_reader_status(self, gpio):
        if gpio != self.status_pin:
            return

        val = GPIO.input(self.status_pin)

        if val != self.current_status:
            self.current_status = val
            log.debug('Reader Update:\nPin {}/{}\nStatus {}\n'
                      .format(self.status_pin, self.reader_id,
                              'HIGH' if val == GPIO.HIGH else 'LOW'))
            self.__callback(self.reader_id, self.current_status)

    @property
    def reader_id(self):
        return self.__reader_id

    @reader_id.setter
    def reader_id(self, reader_id):
        self.__reader_id = reader_id

    @property
    def status_pin(self):
        return self.__status_pin

    @property
    def reader_name(self):
        return self.__reader_name

    @property
    def current_status(self):
        return self.__current_status

    @current_status.setter
    def current_status(self, status):
        self.__current_status = status

    def deinitialize(self):
        GPIO.remove_event_detect(self.status_pin)
        GPIO.cleanup(self.status_pin)
