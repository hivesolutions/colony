#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2022 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2022 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import time
import threading

from . import verify_util

SCHEDULING_MAX = getattr(threading, "TIMEOUT_MAX", 3600)
""" The value for the maximum timeout value allowed
for the threading await operations (defaults to an hour
in case no base value is obtainable) """

class Scheduler(threading.Thread):
    """
    Class that implements a scheduler to be used
    to "call" callable objects for a provided timestamp.
    """

    running_flag = False
    """ Flag that controls if the scheduler event loop is currently
    running, set at the start of the loop and unset by the end of it """

    continue_flag = False
    """ Flag controlling the execution of the scheduler, if unset
    it will trigger the unloading of the loop """

    busy_flag = False
    """ Flag controlling the busy state of the scheduler, controls
    if there's working being "done" by the scheduler """

    timestamp_queue = []
    """ Ordered list (queue) of timestamps for callables """

    timestamp_map = {}
    """ The map associating the timestamp with a list of callables """

    tasks = set()
    """ The complete set of tasks that are currently under pending
    execution, this should be a set of unique identifiers """

    waits = set()
    """ The sequence that contains the complete set of callables that
    are waiting to be notified """

    condition = None
    """ The condition that will control the access to the data structures
    and trigger events on the production of new items """

    waits_condition = None
    """ Condition that is going to be used in the waits operation and control
    the access to the waits set """

    exception_handler = None
    """ If set defined an handler (callable) that is going to be called
    whenever an exception is raised in the execution of the callable units """

    _counter = 1
    """ The unique identifier counter that is going to be incremented
    per each callable to be added """

    def __init__(self):
        """
        Constructor of the class.

        :type plugin: Plugin
        :param plugin: The plugin to be used.
        """

        threading.Thread.__init__(self)

        self.daemon = True
        self.timestamp_queue = []
        self.timestamp_map = {}
        self.tasks = set()
        self.waits = set()
        self.condition = threading.Condition()
        self.waits_condition = threading.Condition()

    def run(self):
        # sets the initial value of the timeout, which is an unset
        # one, this value is only going to be set in case of deferred
        # first item in queue exists
        timeout = None

        # sets the running flag, effectively indicating that the scheduler
        # is running its main loop
        self.running_flag = True

        try:
            # iterates while the continue flag is set, this means
            # that this is a continuous loop operation
            while self.continue_flag:

                # acquires the condition so that we can safely wait for
                # new "events" and access the underlying data structures
                # for proper and safe consuming of them
                with self.condition:
                    # waits for the condition while the system is running and
                    # either the queue is empty or there's a timeout defined
                    # (meaning a pending final value has been reached)
                    while self.continue_flag and (not self.timestamp_queue or timeout):
                        # makes sure that the timeout value does not overflow
                        # maximum timeout value for scheduling, this would
                        # raise an overflow exception, making this verification
                        # will imply running more wait operations for large values
                        # which is OK as no significant resources will be used
                        if timeout: timeout = min(SCHEDULING_MAX, timeout)

                        # waits for the condition and timeouts according to the
                        # provided partial value (if any)
                        self.condition.wait(timeout = timeout)

                        # resets the timeout value as we've stepped outside the
                        # wait operation and this value is no longer relevant
                        timeout = None

                    # in case the continue flag has been unset
                    # (by triggering condition), then breaks loop
                    if not self.continue_flag: break

                    # retrieves the current timestamp, to be
                    # used in comparison operations
                    current_timestamp = time.time()

                    # retrieves the timestamp from the
                    # timestamp queue
                    timestamp = self.timestamp_queue[0]

                    # in case the final timestamp has been
                    # reached, meaning that the timestamp
                    # of the task is greater than the current
                    # timestamp
                    if timestamp > current_timestamp:
                        # sleeps for the amount of time defined
                        # in the sleep step
                        timeout = timestamp - current_timestamp

                        # breaks the loop (no more work
                        # to be processed for now)
                        continue

                    # pops (removes first element) the timestamp
                    # from the timestamp queue, proper timestamp
                    # consuming operation
                    self.timestamp_queue.pop(0)

                    # retrieves the callable (elements) list
                    # for the timestamp
                    callable_list = self.timestamp_map[timestamp]

                    # removes the callable list for the timestamp
                    # (done before the calling to avoid race condition)
                    del self.timestamp_map[timestamp]

                # runs the callable calling operation (consuming)
                # which should properly handle exceptions avoiding
                # internal execution problems
                self._handle_callables(callable_list)
        finally:
            self.running_flag = False
            self.continue_flag = False

    def start_scheduler(self):
        """
        Starts the scheduler process.
        This method is asynchronous and the starting of
        the scheduler is not immediate.
        This method creates a new thread for scheduling.
        """

        # if the scheduler is already running avoids
        # duplicate starting, returns immediately
        if self.continue_flag: return

        # sets the continue flag to the valid value (controls
        # the loop) and then start the main loop process
        self.continue_flag = True
        self.start()

    def stop_scheduler(self):
        """
        Stops the scheduler process.
        This method is asynchronous and the stopping of
        the scheduler is not immediate.
        """

        # if the scheduler is already stopped avoids
        # duplicate stopping, returns immediately
        if not self.continue_flag: return

        # unsets the continue flag, this will trigger
        # the unload of the scheduler as soon as possible
        self.continue_flag = False

        # triggers the condition so that the listener is
        # able to stop the waiting process
        with self.condition:
            self.condition.notify()

    def reset_scheduler(self, notify = True):
        """
        Resets the scheduler to the original state.
        This method may be used to avoid the allocation
        of new scheduler objects.
        This operation is dangerous an is not thread safe.
        A typical usage of this method involves first the
        stopping of the scheduler.

        :type notify: bool
        :param notify: If a notification in the condition should
        be sent so that the thread is unblocked if needed.
        """

        _condition = self.condition

        self.running_flag = False
        self.continue_flag = False
        self.busy_flag = False
        self.timestamp_queue = []
        self.timestamp_map = {}
        self.tasks = set()
        self.waits = set()
        self.condition = threading.Condition()
        self.wait_execution = threading.Condition()
        self.exception_handler = None
        self._counter = 1

        if notify:
            with _condition: _condition.notify()

    def add_callable(self, callable, timestamp = None, verify = True):
        """
        Adds a callable object to the scheduler
        for calling upon the given timestamp value.
        The sent callable is called without any arguments
        and the real time for calling may not be assured.

        An unique callable identifier is returned.

        :type callable: Callable
        :param callable: The callable object to be called
        upon in time described in the given timestamp.
        :type timestamp: float
        :param timestamp: The timestamp describing the
        time for calling the callable object, if not defined
        the current timestamp is used (immediate scheduling).
        :type ensure: bool
        :param ensure: If set makes sure that the scheduler
        is running, raising an exception otherwise.
        :rtype: int
        :return: The identifier of the callable task that has just
        been created, can be used for waiting for task completion.
        """

        # in case the verify flag is set then we need to make
        # sure that the scheduler is running
        if verify: verify_util.verify(self.is_running())

        # in case no explicit timestamp is provided then uses
        # the current time - immediate task scheduling
        if timestamp == None: timestamp = time.time()

        # acquires the condition to be able to safely
        # manipulate the structure and produce item
        with self.condition:
            # obtains the identifier for the current
            # callable operation schedule
            identifier = self._counter
            self._counter += 1

            # starts the index value
            index = 0

            # iterates over all the timestamps in the timestamp
            # queue (to find position for insertion)
            for _timestamp in self.timestamp_queue:
                # in case the the current iteration timestamp
                # contains a value smaller than the timestamp
                # to be inserted
                if timestamp < _timestamp:
                    # breaks the loop (position as
                    # insertion has been reached)
                    break

                # increments the index, offsetting the value
                index += 1

            # checks if the timestamp already exists in the
            # current structures
            timestamp_exists = timestamp in self.timestamp_map

            # inserts the timestamp in the timestamp queue
            # for the correct index (in order to maintain order)
            # in case it does not exist already
            if not timestamp_exists: self.timestamp_queue.insert(index, timestamp)

            # retrieves the list of callable for the given timestamp
            # and then updates it with the given callable object
            callable_list = self.timestamp_map.get(timestamp, [])
            callable_list.append((callable, identifier))
            self.timestamp_map[timestamp] = callable_list

            # adds the identifier to the sequence that controls the
            # tasks that are considered active
            self.tasks.add(identifier)

            # notifies the condition effectively indicating that a
            # new item or set of items is available for consumption
            self.condition.notify()

            # returns the final identifier for the callable task
            # that has just been scheduled
            return identifier

    def wait_callable(self, identifier):
        verify_util.verify(isinstance(identifier, int))

        with self.waits_condition:
            self.waits.add(identifier)

        if not identifier in self.tasks:
            with self.waits_condition:
                if identifier in self.waits:
                    self.waits.remove(identifier)
            return

        with self.waits_condition:
            while self.continue_flag and identifier in self.waits:
                self.waits_condition.wait()

    def set_exception_handler(self, exception_handler):
        """
        Sets the handler that will be called in case there's an
        user exception raised in the callable.

        :type exception_handler: Callable
        :param exception_handler: The handler to be called upon
        exception in callable execution.
        """

        self.exception_handler = exception_handler

    def is_busy(self):
        """
        Checks if the scheduler is currently in a busy status
        meaning that it's executing some sort of work.

        :rtype: bool
        :return: If the scheduler is executing any kind of work.
        """

        return self.busy_flag

    def is_running(self, pedantic = False):
        """
        Checks if the scheduler is currently running, the scheduler
        is considered to be running if the continue flag is set.

        In case the pedantic flag is set the scheduler is only
        considered to be running in case the running flag (which
        is set when thread is running) is also set.

        :rtype: bool
        :return: If the scheduler is currently running.
        """

        if pedantic: return self.running_flag and self.continue_flag
        return self.continue_flag

    def _handle_callables(self, callable_list):
        # sets the busy flag indicating that there's execution
        # of callable object happening
        self.busy_flag = True

        try:
            # iterates over all the callables to call
            # them (calls the proper function)
            for callable, _identifier in callable_list:
                try:
                    # calls the callable (element)
                    # this can be of long duration
                    callable()
                except Exception as exception:
                    if self.exception_handler:
                        self.exception_handler(callable, exception)
                    else:
                        print(exception)
        finally:
            self.busy_flag = False

        # runs a final waits condition operation that will
        # make sure that the pending waits values are notified
        # in case they are in a waiting state, it will also
        # remove the multiple callable tasks from the sequence
        # that controls the pending tasks
        with self.waits_condition:
            notify = False

            for callable, identifier in callable_list:
                if identifier in self.waits:
                    self.waits.remove(identifier)
                    notify = True
                self.tasks.remove(identifier)

            if notify:
                self.waits_condition.notify_all()
