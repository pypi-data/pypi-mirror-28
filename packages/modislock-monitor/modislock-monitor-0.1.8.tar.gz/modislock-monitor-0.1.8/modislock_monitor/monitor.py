# coding: utf-8

import time
from threading import Thread, Timer

# Queue
from .event_queue import EventQueue

# Serial Objects
from serial import SerialException, serial_for_url
from .transport import WatchedReader, PacketHandler

# Database
from .database import Database, Readings, ReaderStatus, ReaderSettings, Locations, Sensors
from sqlalchemy.exc import IntegrityError, OperationalError

# Extensions
from .extensions import log

# Readers
from .slave_reader import SlaveReader, SlaveRequest, SlaveResponse, ControllerMessage

# Pins
from .platform_detection import isRaspberryPi
from .door_sensor import DoorSensor
from .reader import Reader

# GPIO access
if isRaspberryPi:
    import RPi.GPIO as GPIO
else:
    import GPIOEmu as GPIO


class Monitor(Thread):
    """Monitor(Database)

    The monitor uses UART communication from the incoming reader requests to determine validation and onboard relay
    settings. GPIO pins associated with each reader are pulled high when a slave ID of 1 to 4 are responding to the
    heartbeat request sent out periodically.

    The Monitor object acts as the central validation source worker for the Modis Lock. The object is responsible for
    communication with the controller on the lock that in turn communicates to the remote readers. Interface with the
    Monitor and controller is done through UART.

    GPIO pins are used for both status information as well as sensor readings. These GPIO states are tracked with the
    use of a database connection. Without this connection the Monitor will fail to initialize.

    Usually a Monitor object can be created with defaults with the .. file::`__init__.py` file of the package like this:

    >>> from modislock_monitor import Monitor
    >>> monitor = Monitor()

    """

    STATUS_INTERVAL = 30

    def __init__(self, port, readers, door_sensors):
        super(Monitor, self).__init__(daemon=True, name='Monitor')
        self.__doors = list()
        self.__readers = list()
        self.__sessions = dict()
        self.__event_queue = EventQueue()
        self.__transport = None

        #: Initialize the readers, doors, and reset buttons
        for i, name in enumerate(door_sensors):
            self.__doors.append(DoorSensor(i, door_sensors[name], name, self._door_callback))

        for i, name in enumerate(readers):
            self.__readers.append(Reader(i, readers[name], name, self._reader_callback))

        # Serial port setup
        log.debug('Opening port on: {}'.format(port))

        try:
            serial_port = serial_for_url(port, baudrate=115200, timeout=1)
        except SerialException as e:
            log.error('Error initializing serial port: {}'.format(e))
            raise IOError

        # Transportation mechanism
        class ReaderMessage(PacketHandler):
            """Packet Handler for communications between host and readers.

            The handler is quite simplified from the previous version and simply enqueues a task onto the event queue.

            """

            def __init__(self):
                super(ReaderMessage, self).__init__()

            def handle_packet(self, packet):
                """Places the packet with the handler function onto the event queue

                :param bytes packet:

                """
                Monitor.handle_incoming(packet)

            def handle_out_of_packet_data(self, data):
                """Handles any bytes received from outside a frame

                :param bytes data:
                """
                log.debug('Garbage received from uart outside of frame: {}'.format(data))

        self.__transport = WatchedReader(serial_port, ReaderMessage)
        self.__running = False
        self.__status_timer = Timer(self.STATUS_INTERVAL, self._request_status)

    def _door_callback(self, door_id, value):
        """Door callback for handling events

        :param door_id:
        :param value:
        :return:
        """
        self.__event_queue.enqueue(Monitor.handle_doors, args=[door_id, value], priority=100)

    def _reader_callback(self, reader_id, value):
        """Reader callback for handling reader status events

        :param reader_id:
        :param value:
        :return:
        """
        self.__event_queue.enqueue(Monitor.handle_reader, args=[reader_id, value], priority=100)

    @classmethod
    def handle_incoming(cls, packet):
        """Handles incoming packets from controller over UART

        :param bytes packet: Incoming packet request from transport

        """
        reader = None

        try:
            slave_id = int.from_bytes(packet[:1], byteorder='big')
            frame_type = int.from_bytes(packet[1:2], byteorder='big')
            req_size = int.from_bytes(packet[2:3], byteorder='big')
        except ValueError:
            log.debug('Malformed frame. Unable to convert bytes to integer representations.')
        except IndexError:
            log.debug('Number of bytes too low')
        else:
            # if SlaveResponse.RESPONSE_NO_EVENT <= frame_type <= SlaveResponse.RESPONSE_STATUS:
            if frame_type == SlaveResponse.RESPONSE_NO_EVENT:
                log.debug('Heartbeat received')
            elif frame_type == SlaveResponse.RESPONSE_EVENT_W_PROTOCOL:
                if req_size > 3 and slave_id not in cls.sessions:
                    reader = SlaveReader(slave_id, request_cb=Monitor.handle_outgoing)
                    cls.sessions[slave_id] = reader
            elif frame_type == SlaveResponse.RESPONSE_SECOND_KEY:
                try:
                    reader = cls.sessions[slave_id]
                except IndexError:
                    log.debug('Not found in sessions')
            elif frame_type == SlaveResponse.RESPONSE_STATUS:
                cls.queue.enqueue(Monitor.handle_status, args=[packet], priority=150)

            if reader is not None:
                reader.process_message(packet)

    @classmethod
    def handle_outgoing(cls, packet):
        """Handles all processed packages returning from the slave reader objects

        :param SlaveRequest packet: Frame outgoing through controller to reader

        """
        if isinstance(packet, SlaveRequest):
            log.debug('Outgoing message to:\nSlave->{}\nFrame type->{}\nMessage: {}'
                      .format(packet.address,
                              packet.frame_type,
                              ''.join('%02x' % b for b in packet.message)))

            if packet.frame_type == SlaveRequest.REQUEST_DENIED or packet.frame_type == SlaveRequest.REQUEST_APPROVED:
                try:
                    del cls.sessions[packet.address]
                except KeyError:
                    log.error('Key not found in sessions')

            cls.transport.send_packet(packet.message)

    @classmethod
    def handle_doors(cls, sensor_id, value):
        """Handles door sensors changes from GPIO interrupts

        :param int sensor_id: GPIO Number of door sensor
        :param int value: LOW(0) | HIGH(1)

        """
        with Database() as db:
            query = db.session.query(Readings) \
                .filter(Readings.sensors_id_sensors == sensor_id) \
                .first()

            if query is not None:
                query.value = 'ACTIVE' if value == GPIO.HIGH else 'INACTIVE'

                try:
                    db.session.commit()
                except (IntegrityError, OperationalError):
                    db.session.rollback()
                    log.error('Error updating door status in database')

    @classmethod
    def handle_reader(cls, reader_id, value):
        """Handles the reader changes from GPIO interrupts

        :param int reader_id: Reader GPIO pin number
        :param int value: LOW(0) | HIGH(1)

        """
        with Database() as db:
            query = db.session.query(ReaderStatus) \
                .filter(ReaderStatus.reader_id_reader == reader_id) \
                .one_or_none()

            if query is not None:
                query.status = 'CONNECTED' if value == GPIO.HIGH else 'DISCONNECTED'

                try:
                    db.session.commit()
                except (IntegrityError, OperationalError):
                    db.session.rollback()
                    log.error('Error updating reader status is database')

    @classmethod
    def handle_status(cls, packet):
        """Handles status response from requested slave

        :param bytes packet: raw byte stream from communication
        :return:
        """
        response = SlaveResponse(packet)

        if response.frame_type == SlaveResponse.RESPONSE_STATUS:
            status = response.status
        else:
            return

        with Database() as db:
            sensor = db.session.query(ReaderSettings) \
                .join(Locations, ReaderSettings.id_reader == Locations.reader_settings_id_reader) \
                .join(Sensors, Locations.id_locations == Sensors.locations_id_locations) \
                .filter(ReaderSettings.id_reader == response.address) \
                .with_entities(Sensors.id_sensors, Sensors.name, ReaderSettings.location_name).all()

            for result in sensor:
                sensor_id = result[0]
                if 'TEMP' in result[1]:
                    db.session.execute('CALL add_reading(' + str(status["temp"]) + ',' + str(sensor_id) + ')')
                elif 'VALIDATION' in result[1]:
                    db.session.execute('CALL add_reading(' + str(status['validations']) + ',' + str(sensor_id) + ')')
                elif 'DENIED' in result[1]:
                    db.session.execute('CALL add_reading(' + str(status['denials']) + ',' + str(sensor_id) + ')')

    def _request_status(self):
        """Periodic task that requests active readers status

        :return:
        """

        self.__event_queue.enqueue(Monitor.handle_outgoing,
                                   args=[ControllerMessage(ControllerMessage.CONTROLLER_STATUS, 0).message],
                                   priority=100)
        for reader in self.__readers:
            time.sleep(1)
            # Only active readers are requested
            if reader.current_status == 1:
                self.__event_queue.enqueue(Monitor.handle_outgoing,
                                           args=[ControllerMessage(ControllerMessage.CONTROLLER_STATUS,
                                                                   reader.reader_id).message],
                                           priority=100)

    @property
    def sessions(self):
        """Gets active session list

        :return list:
        """
        return self.__sessions

    @property
    def transport(self):
        """Gets active transport layer

        :return WatchReader:
        """
        return self.__transport

    @property
    def queue(self):
        """Gets event queue

        :return EventQueue:
        """
        return self.__event_queue

    def run(self):
        """Runs the monitor thread

        Waits for interrupts and processes the event queue. During startup will send a command to the controller
        to restart.

        """
        self.transport.start()

        while not self.transport.is_alive():
            time.sleep(0.5)

        self.__running = True
        self.__status_timer.start()
        # Reset on-board controller
        self.transport.send_packet(ControllerMessage(ControllerMessage.CONTROLLER_REBOOT, 0).message)

        while self.__running:
            while self.__event_queue.has_more():
                # Dequeue functions to run
                func, args, kwargs = self.__event_queue.dequeue()

                if func is not None:
                    func(*args, **kwargs)

        for door in self.__doors:
            door.deinitialize()
        for reader in self.__readers:
            reader.deinitialize()
        self.transport.stop()
        self.__status_timer.cancel()
        log.debug('readers/doors/ports de-initialized')

    def stop(self):
        """Stops the current running monitor

        :return:
        """
        log.info('Monitor shutdown requested')
        self.__running = False


