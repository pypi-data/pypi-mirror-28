
# Extensions
from .extensions import log

# Database
from .database import Database, Readings, Sensors
from sqlalchemy.exc import IntegrityError, OperationalError

# Pins
from .platform_detection import isRaspberryPi

# GPIO access
if isRaspberryPi:
    import RPi.GPIO as GPIO
else:
    import GPIOEmu as GPIO


class DoorSensor:
    """Door Sensor

    """
    def __init__(self, sensor_id, door_pin, sensor_name=None, callback=None):
        assert type(sensor_id) is int, 'Sensor ID shoudl be of int type: %r' % sensor_id
        assert type(door_pin) is int, 'Door pin should be of int type: %r' % door_pin

        self.__sensor_id = sensor_id
        self.__door_pin = door_pin
        self.__sensor_name = sensor_name if sensor_name is not None else 'unknown'
        self.__callback = self._callback if callback is None else callback

        # Setup Pin
        GPIO.setup(self.door_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Get Value
        self.__current_state = GPIO.input(self.door_pin)

        # Add event
        GPIO.add_event_detect(self.door_pin,
                              GPIO.BOTH,
                              callback=self._update_door_status)

        with Database() as db:
            query = db.session.query(Sensors) \
                .filter(Readings.sensors_id_sensors == self.sensor_id) \
                .first()

            if query is not None:
                query.value = "ACTIVE" if self.current_state == GPIO.HIGH else 'INACTIVE'

                try:
                    db.session.commit()
                except (IntegrityError, OperationalError):
                    db.session.rollback()
                    log.error('Status Monitor Database Error')
            else:
                door = Readings(value='ACTIVE' if self.current_state == GPIO.HIGH else 'INACTIVE',
                                sensors_id_sensors=self.door_pin)
                db.session.add(door)

                try:
                    db.session.commit()
                except (IntegrityError, OperationalError):
                    db.session.rollback()
                    log.error('Status Monitor Database Error')

    def _callback(self, id, value):
        pass

    def _update_door_status(self, gpio):
        """Thread worker that watches the door inputs

        Updates the database accordingly.

        :param int gpio_id: GPIO of door that has triggered the event

        """
        if gpio != self.door_pin:
            return

        val = GPIO.input(self.door_pin)

        if val != self.current_state:
            self.current_state = val
            log.debug('Door Update:\nPin {}\nStatus {}\n'
                      .format(self.door_pin, 'HIGH' if self.current_state == GPIO.HIGH else 'LOW'))
            self.__callback(self.sensor_id, self.current_state)

    @property
    def sensor_id(self):
        return self.__sensor_id

    @sensor_id.setter
    def sensor_id(self, id):
        self.__sensor_id = id

    @property
    def door_pin(self):
        return self.__door_pin

    @property
    def sensor_name(self):
        return self.__sensor_name

    @property
    def current_state(self):
        return self.__current_state

    @current_state.setter
    def current_state(self, state):
        self.__current_state = state

    def deinitialize(self):
        GPIO.remove_event_detect(self.door_pin)
        GPIO.cleanup(self.door_pin)