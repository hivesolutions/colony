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

import colony

class SchedulerTest(colony.ColonyTestCase):
    """
    Class that tests the scheduler up to the expected
    values, making sure that race and other weird conditions
    are properly handled.
    """

    def test_basic(self):
        """
        Runs a series of basic sanity tests for the scheduler.
        """

        scheduler = colony.Scheduler()
        scheduler.start_scheduler()
        self.assertEqual(scheduler.is_running(), True)

        values = dict()

        def update_values():
            values["a"] = 1

        self.assertEqual(values, dict())

        identifier = scheduler.add_callable(update_values)
        scheduler.wait_callable(identifier)
        self.assertEqual(identifier, 1)
        self.assertEqual(values, dict(a = 1))

    def test_delayed(self):
        """
        Tests that a delayed work can be scheduled and executed
        in the proper time.
        """

        scheduler = colony.Scheduler()
        scheduler.start_scheduler()
        self.assertEqual(scheduler.is_running(), True)

        values = dict()

        def update_values():
            values["a"] = 1

        self.assertEqual(values, dict())

        initial = time.time()
        identifier = scheduler.add_callable(update_values, time.time() + 0.5)
        self.assertEqual(identifier, 1)
        time.sleep(0.25)
        self.assertEqual(values, dict())

        scheduler.wait_callable(identifier)
        self.assertEqual(time.time() - initial >= 0.5, True)
        self.assertEqual(values, dict(a = 1))

    def test_stopped(self):
        """
        Tests that if the scheduler is currently stopped then
        a series of consequences must happen.
        """

        scheduler = colony.Scheduler()
        scheduler.start_scheduler()
        self.assertEqual(scheduler.is_running(), True)

        scheduler.stop_scheduler()
        self.assertEqual(scheduler.join(1), None)
        self.assertEqual(scheduler.is_running(), False)
        self.assert_raises(colony.AssertionError, lambda: scheduler.add_callable(lambda: 1))

        values = dict()

        def update_values():
            values["a"] = 1

        self.assertEqual(values, dict())

        identifier = scheduler.add_callable(update_values, verify = False)
        scheduler.wait_callable(identifier)
        self.assertEqual(values, dict())

        self.assert_raises(RuntimeError, scheduler.start_scheduler)

    def test_exception_handler(self):
        """
        Tests that the exception handler is properly handling
        exceptions raised in the callable execution.
        """

        scheduler = colony.Scheduler()
        scheduler.start_scheduler()
        self.assertEqual(scheduler.is_running(), True)
        self.assertEqual(scheduler.exception_handler, None)

        values = dict()

        def update_values_raise():
            values["a"] = 1
            raise Exception()

        identifier = scheduler.add_callable(update_values_raise)
        scheduler.wait_callable(identifier)
        self.assertEqual(values, dict(a = 1))
        self.assertEqual(scheduler.is_running(pedantic = True), True)

        def exception_handler(callable, exception):
            values["callable"] = callable
            values["exception"] = exception.__class__

        scheduler.set_exception_handler(exception_handler)

        identifier = scheduler.add_callable(update_values_raise)
        scheduler.wait_callable(identifier)
        self.assertEqual(
            values,
            dict(
                a = 1,
                callable = update_values_raise,
                exception = Exception
            )
        )
        self.assertEqual(scheduler.is_running(pedantic = True), True)
