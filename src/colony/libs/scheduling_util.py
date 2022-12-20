#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import time
import threading

from . import verify_util

DEFAULT_SLEEP_STEP = 0.1
""" The default sleep step to be used in the scheduler
this value should not be too big that prevent immediate
scheduling operation nor to low that spends to many resources """

class Scheduler(threading.Thread):
    """
    Class that implements a scheduler to be used
    to "call" callable objects for a provided timestamp.
    """

    sleep_step = None
    """ The amount of time to be used during a sleep iteration
    this is required as not `Condition` objects are used to
    control the producer/consumer dynamics """

    running_flag = False
    """ Flag that controls if the scheduler event loop is currently
    running """

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

    timestamp_lock = None
    """ The lock that controls the access to the timestamp structures """

    action_lock = None
    """ The lock that controls the access to the start and stop actions """

    exception_handler = None
    """ If set defined an handler (callable) that is going to be called
    whenever an exception is raised in the execution of the callable units """

    def __init__(self, sleep_step = DEFAULT_SLEEP_STEP):
        """
        Constructor of the class.

        :type plugin: Plugin
        :param plugin: The plugin to be used.
        :type sleep_step: float
        :param sleep_step: The amount of time to be used
        during a sleep iteration.
        """

        threading.Thread.__init__(self)

        self.sleep_step = sleep_step

        self.daemon = True
        self.timestamp_queue = []
        self.timestamp_map = {}
        self.timestamp_lock = threading.RLock()
        self.action_lock = threading.RLock()

    def run(self):
        self.running_flag = True

        try:
            # iterates while the continue flag is set, this means
            # that this is a continuous loop operation
            while self.continue_flag:
                # acquires the timestamp lock
                self.timestamp_lock.acquire()

                try:
                    # retrieves the current timestamp
                    current_timestamp = time.time()

                    # iterates over the timestamp queue
                    while True:
                        # in case the timestamp queue is invalid
                        # (possibly empty)
                        if not self.timestamp_queue:
                            # breaks the loop (no more work
                            # to be processed for now)
                            break

                        # retrieves the timestamp from the
                        # timestamp queue
                        timestamp = self.timestamp_queue[0]

                        # in case the final timestamp has been
                        # reached, meaning that the timestamp
                        # of the task is greater than the current
                        # timestamp
                        if timestamp > current_timestamp:
                            # breaks the loop (no more work
                            # to be processed for now)
                            break

                        # retrieves the callable (elements) list
                        # for the timestamp
                        callable_list = self.timestamp_map[timestamp]

                        # removes the callable list for the timestamp
                        # (done before the calling to avoid race condition)
                        del self.timestamp_map[timestamp]

                        # pops (removes first element) the timestamp
                        # from the timestamp queue (done before the
                        # calling to avoid race condition)
                        self.timestamp_queue.pop(0)

                        # sets the busy flag and releases the timestamp
                        # lock (avoids waiting for callables)
                        self.busy_flag = True
                        self.timestamp_lock.release()

                        try:
                            # iterates over all the callables to call
                            # them (calls the proper function)
                            for callable in callable_list:
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
                            # acquires the timestamp lock (back)
                            # and unsets the busy flag
                            self.timestamp_lock.acquire()
                            self.busy_flag = False
                finally:
                    # releases the timestamp lock
                    self.timestamp_lock.release()

                # sleeps for the amount of time defined
                # in the sleep step
                time.sleep(self.sleep_step)
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

    def reset_scheduler(self):
        """
        Resets the scheduler to the original state.
        This method may be used to avoid the allocation
        of new scheduler objects.
        This operation is dangerous an is not thread safe.
        A typical usage of this method involves first the
        stopping of the scheduler.
        """

        self.continue_flag = False
        self.timestamp_queue = []
        self.timestamp_map = {}
        self.timestamp_lock = threading.RLock()

    def add_callable(self, callable, timestamp = None, verify = True):
        """
        Adds a callable object to the scheduler
        for calling upon the given timestamp value.
        The sent callable is called without any arguments
        and the real time for calling may not be assured.

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
        """

        # in case the verify flag is set then we need to make
        # sure that the scheduler is running
        if verify: verify_util.verify(self.is_running())

        # in case no explicit timestamp is provided then uses
        # the current time - immediate task scheduling
        if timestamp == None: timestamp = time.time()

        # acquires the timestamp lock
        self.timestamp_lock.acquire()

        try:
            # starts the index value
            index = 0

            # iterates over all the timestamps in the
            # timestamp queue (to find position for insertion)
            for _timestamp in self.timestamp_queue:
                # in case the the current iteration
                # timestamp contains a value smaller than
                # the timestamp to be inserted
                if timestamp < _timestamp:
                    # breaks the loop (position for
                    # insertion reached)
                    break

                # increments the index
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
            callable_list.append(callable)
            self.timestamp_map[timestamp] = callable_list
        finally:
            # releases the timestamp lock
            self.timestamp_lock.release()

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
