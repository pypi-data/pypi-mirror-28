# coding: utf-8

from queue import PriorityQueue, Full, Empty
from modislock_monitor.extensions import log
from threading import Event


class Task:
    """Task to be run

    Holds a task that needs to be run

    :param int priority: Priority from 1 to 1000, lower number = higher priority
    :param func task: function to be called
    """
    def __init__(self, priority, task):
        if type(task) is not tuple:
            raise TypeError
        self._priority = priority
        self._task = task

    def __lt__(self, other):
        return not other._priority < self._priority

    @property
    def task(self):
        """Task

        :returns: func - task to be run
        """
        return self._task


class EventQueue(PriorityQueue):
    """Event queue

    Queue to hold tasks that need to be run.

    :param int maxsize=0: A max size of 0 or negative is unlimited
    """
    def __init__(self, put_event, maxsize=0):
        super(EventQueue, self).__init__(maxsize)
        assert isinstance(put_event, Event) is True, 'Put event must be of type Event'
        self._event = put_event

    @staticmethod
    def _pack_call(func, args, kwargs):
        """Pack the function args and key words into tuple

        :param func func:
        :param *args args:
        :param **kwargs kwargs:
        :returns: tuple

        """
        return (func, args, kwargs)

    @staticmethod
    def _uppack_call(task):
        """Unpack task into respective elements

        :param func task:
        :returns: func, args, kwargs
        """
        return task[0], task[1], task[2]

    def enqueue(self, func, *args, **kwargs):
        """Enqueue a task

        :param func func:
        :param dict args:
        :param dict kwargs:
        :param int priority:
        :returns:

        """
        priority = 100

        if 'priority' in kwargs:
            priority = kwargs['priority']

        element = Task(priority, self._pack_call(func, args, kwargs))

        try:
            self.put(element, block=True, timeout=None)
        except Full:
            log.debug('Event Queue is FULL')
        else:
            self._event.set()

    def dequeue(self, block=True, timeout=None):
        """Dequeue a task from the queue

        :param bool block:
        :param int timeout:
        :returns: Task
        """
        if self.has_more():
            try:
                task = self.get(block, timeout)
            except Empty:
                log.debug('Queue is empty')
                return None, None, None
            else:
                return self._uppack_call(task.task)

    def has_more(self):
        """Has more elements

        :returns: bool - true if elements are still on the queue
        """
        return not self.empty()

