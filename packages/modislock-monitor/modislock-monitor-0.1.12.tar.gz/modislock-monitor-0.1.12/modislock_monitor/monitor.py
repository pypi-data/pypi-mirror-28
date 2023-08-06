# coding: utf-8

import time
from threading import Thread, Event

# Queue
from .event_queue import EventQueue

# Serial Objects
from serial import SerialException, serial_for_url
from .transport import WatchedReader, ReaderMessage

# Extensions
from .extensions import log

# Readers
from .slave_reader import SlaveReader, SlaveRequest, SlaveResponse, ControllerMessage

# Sensors
from .door_sensor import DoorSensor
from .reader import Reader

# Tasks
from celery.exceptions import OperationalError
from .tasks import update_door_status, update_reader_status, update_status_request


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

    STATUS_INTERVAL = 45.0

    # Monitor elements
    # monitor = SimpleNamespace(transport=None, sessions=dict(), events=EventQueue())

    def __init__(self, port, readers, door_sensors):
        super(Monitor, self).__init__(daemon=True, name='Monitor')

        self.__doors = list()
        self.__readers = list()
        self.__sessions = dict()
        self.__event = Event()
        self.__event_queue = EventQueue(self.__event)
        self.__transport = None
        self.__status_timer = Thread(target=self._request_status, name='Monitor Status')
        self.__running = False

        #: Initialize the readers, doors
        for name, pin in door_sensors.items():
            self.__doors.append(DoorSensor(pin, name, self._door_callback))

        for i, name in enumerate(readers):
            self.__readers.append(Reader(i + 1, readers[name], name, self._reader_callback))

        try:
            serial_port = serial_for_url(port, baudrate=115200, timeout=1)
        except SerialException as e:
            log.error('Error initializing serial port: {}'.format(e))
            raise IOError
        else:
            # Serial port setup
            log.debug('Opened port on: {}'.format(port))

        self.__transport = WatchedReader(serial_port, ReaderMessage)
        self.__transport.start()

        while not self.__transport.is_alive():
            time.sleep(0.5)

        self.__transport.set_handlers(self._handle_incoming, self._handle_noise)

    def _door_callback(self, door_id, value):
        """Door callback for handling events

        :param door_id:
        :param value:
        :return:
        """
        try:
            update_door_status.delay(door_id, value)
        except OperationalError:
            pass

    def _reader_callback(self, reader_id, value):
        """Reader callback for handling reader status events

        :param reader_id:
        :param value:
        :return:
        """
        try:
            update_reader_status.delay(reader_id, value)
        except OperationalError:
            pass

    def _request_status(self):
        """Periodic task that requests active readers status

        :return:
        """

        while self.__running:
            # Send to host controller first
            self.__event_queue.enqueue(self._handle_outgoing,
                                       SlaveRequest(0, SlaveRequest.REQUEST_STATUS, ControllerMessage.CONTROLLER_STATUS),
                                       priority=150)
            # Send to attached readers
            for reader in self.__readers:
                time.sleep(1)
                # Only active readers are requested
                if reader.current_status == 1:
                    self.__event_queue.enqueue(self._handle_outgoing,
                                               SlaveRequest(reader.reader_id, SlaveRequest.REQUEST_STATUS, ControllerMessage.CONTROLLER_STATUS),
                                               priority=150)
            time.sleep(self.STATUS_INTERVAL)

    def _handle_noise(self, packet):
        log.debug('Garbage received from uart outside of frame: {}'.format(packet))

    def _handle_incoming(self, packet):
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
                if req_size > 3 and slave_id not in self.__sessions:
                    reader = SlaveReader(slave_id, request_cb=self._handle_outgoing)
                    self.__sessions[slave_id] = reader
            elif frame_type == SlaveResponse.RESPONSE_SECOND_KEY:
                try:
                    reader = self.__sessions[slave_id]
                except IndexError:
                    log.debug('Not found in sessions')
            elif frame_type == SlaveResponse.RESPONSE_STATUS:
                response = SlaveResponse(packet)

                if response.frame_type == SlaveResponse.RESPONSE_STATUS:
                    status = response.status
                    update_status_request.delay(response.address, status)

            if reader is not None:
                reader.process_message(packet)

    def _handle_outgoing(self, packet, **kwargs):
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
                    del self.__sessions[packet.address]
                except KeyError:
                    log.error('Key not found in sessions')
            self.__transport.send_packet(packet.message)

    def run(self):
        """Runs the monitor thread

        Waits for interrupts and processes the event queue. During startup will send a command to the controller
        to restart.

        """
        # Reset on-board controller
        self.__event_queue.enqueue(self._handle_outgoing,
                                   SlaveRequest(0, SlaveRequest.REQUEST_STATUS, ControllerMessage.CONTROLLER_REBOOT),
                                   priority=160)

        self.__running = True
        self.__status_timer.start()

        while not self.__status_timer.is_alive():
            time.sleep(1)

        while self.__running:
            # Sleep until event happens
            self.__event.wait(timeout=100)
            # Process all the events
            while self.__event_queue.has_more():
                # Dequeue functions to run
                func, args, kwargs = self.__event_queue.dequeue()

                if func is not None:
                    func(*args, **kwargs)
            # All events processed go back to sleep
            self.__event.clear()

        for door in self.__doors:
            door.deinitialize()
        for reader in self.__readers:
            reader.deinitialize()
        self.__transport.stop()
        log.debug('readers/doors/ports de-initialized')

    def stop(self):
        """Stops the current running monitor

        :return:
        """
        log.info('Monitor shutdown requested')
        self.__running = False


