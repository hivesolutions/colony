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

import colony

class SchedulerTest(colony.ColonyTestCase):
    """
    Class that tests the scheduler up to the expected
    values, making sure that race and other weird conditions
    are properly handled.
    """

    def setUp(self):
        self.scheduler = colony.Scheduler()
        self.scheduler.start_scheduler()

    def tearDown(self):
        self.scheduler.stop_scheduler()
        self.scheduler.join(10)

    def test_basic(self):
        """
        Runs a series of basic sanity tests for the scheduler.
        """

        self.assertEqual(self.scheduler.is_running(), True)

        values = dict()

        def update_values():
            values["a"] = 1

        self.assertEqual(values, dict())

        identifier = self.scheduler.add_callable(update_values)
        self.scheduler.wait_callable(identifier)
        self.assertEqual(identifier, 1)
        self.assertEqual(values, dict(a = 1))
        self.assertEqual(self.scheduler.is_running(), True)
        self.assertEqual(self.scheduler.is_busy(), False)

        self.scheduler.reset_scheduler()
        self.assertEqual(self.scheduler.is_running(), False)
        self.assertEqual(self.scheduler.is_busy(), False)

    def test_delayed(self):
        """
        Tests that a delayed work can be scheduled and executed
        in the proper time.
        """

        self.assertEqual(self.scheduler.is_running(), True)

        values = dict()

        def update_values():
            values["a"] = 1

        self.assertEqual(values, dict())

        initial = time.time()
        identifier = self.scheduler.add_callable(update_values, timestamp = time.time() + 0.3)
        self.assertEqual(identifier, 1)
        time.sleep(0.1)
        self.assertEqual(values, dict())

        self.scheduler.wait_callable(identifier)
        self.assertEqual(time.time() - initial >= 0.3, True)
        self.assertEqual(values, dict(a = 1))

    def test_multiple(self):
        """
        Tests that multiple parallel callable tasks can be
        scheduled and executed.
        """

        self.assertEqual(self.scheduler.is_running(), True)

        values = dict()

        def update_values_1():
            values["a"] = 1

        def update_values_2():
            values["b"] = 2

        self.assertEqual(values, dict())

        identifier_1 = self.scheduler.add_callable(update_values_1)
        identifier_2 = self.scheduler.add_callable(update_values_2)
        self.scheduler.wait_callable(identifier_1)
        self.scheduler.wait_callable(identifier_2)
        self.assertEqual(identifier_1, 1)
        self.assertEqual(identifier_2, 2)
        self.assertEqual(values, dict(a = 1, b = 2))
        self.assertEqual(self.scheduler.is_running(), True)
        self.assertEqual(self.scheduler.is_busy(), False)

        values = dict()

        def update_values_3():
            values["a"] = 1

        def update_values_4():
            values["b"] = values["a"] + 1

        self.assertEqual(values, dict())

        identifier_1 = self.scheduler.add_callable(update_values_3, timestamp = time.time() + 0.1)
        identifier_2 = self.scheduler.add_callable(update_values_4, timestamp = time.time() + 0.2)
        self.scheduler.wait_callable(identifier_1)
        self.scheduler.wait_callable(identifier_2)
        self.assertEqual(identifier_1, 3)
        self.assertEqual(identifier_2, 4)
        self.assertEqual(values, dict(a = 1, b = 2))
        self.assertEqual(self.scheduler.is_running(), True)
        self.assertEqual(self.scheduler.is_busy(), False)

        values = dict()

        def update_values_5():
            values["a"] = values["b"] + 1

        def update_values_6():
            values["b"] = 2

        self.assertEqual(values, dict())

        identifier_1 = self.scheduler.add_callable(update_values_5, timestamp = time.time() + 0.2)
        identifier_2 = self.scheduler.add_callable(update_values_6, timestamp = time.time() + 0.1)
        self.scheduler.wait_callable(identifier_1)
        self.scheduler.wait_callable(identifier_2)
        self.assertEqual(identifier_1, 5)
        self.assertEqual(identifier_2, 6)
        self.assertEqual(values, dict(a = 3, b = 2))
        self.assertEqual(self.scheduler.is_running(), True)
        self.assertEqual(self.scheduler.is_busy(), False)

    def test_overflow(self):
        """
        Tests that it is possible to add a task that overflows
        the max timeout value for the scheduler.
        """

        self.assertEqual(self.scheduler.is_running(), True)

        values = dict()

        def update_values():
            values["a"] = 1

        self.assertEqual(values, dict())

        identifier = self.scheduler.add_callable(
            update_values,
            timestamp = time.time() + colony.SCHEDULING_MAX + 1
        )
        self.assertEqual(identifier, 1)
        self.assertEqual(values, dict())
        self.assertEqual(self.scheduler.is_running(), True)

        update_values()
        self.assertEqual(values, dict(a = 1))

    def test_stopped(self):
        """
        Tests that if the scheduler is currently stopped then
        a series of consequences must happen.
        """

        self.assertEqual(self.scheduler.is_running(), True)

        self.scheduler.stop_scheduler()
        self.assertEqual(self.scheduler.join(10), None)
        self.assertEqual(self.scheduler.is_running(), False)
        self.assert_raises(colony.AssertionError, lambda: self.scheduler.add_callable(lambda: 1))

        values = dict()

        def update_values():
            values["a"] = 1

        self.assertEqual(values, dict())

        identifier = self.scheduler.add_callable(update_values, verify = False)
        self.scheduler.wait_callable(identifier)
        self.assertEqual(values, dict())

        self.assert_raises(RuntimeError, self.scheduler.start_scheduler)

        update_values()
        self.assertEqual(values, dict(a = 1))

    def test_exception_handler(self):
        """
        Tests that the exception handler is properly handling
        exceptions raised in the callable execution.
        """

        self.assertEqual(self.scheduler.is_running(), True)
        self.assertEqual(self.scheduler.exception_handler, None)

        values = dict()

        def update_values_raise():
            values["a"] = 1
            raise Exception()

        identifier = self.scheduler.add_callable(update_values_raise)
        self.scheduler.wait_callable(identifier)
        self.assertEqual(values, dict(a = 1))
        self.assertEqual(self.scheduler.is_running(pedantic = True), True)

        def exception_handler(callable, exception):
            values["callable"] = callable
            values["exception"] = exception.__class__

        self.scheduler.set_exception_handler(exception_handler)

        identifier = self.scheduler.add_callable(update_values_raise)
        self.scheduler.wait_callable(identifier)
        self.assertEqual(
            values,
            dict(
                a = 1,
                callable = update_values_raise,
                exception = Exception
            )
        )
        self.assertEqual(self.scheduler.is_running(pedantic = True), True)

    def test_waiting(self):
        """
        Tests the waiting operation, specially for edge cases.
        """

        self.assertEqual(self.scheduler.is_running(), True)

        values = dict()

        def update_values_1():
            values["a"] = 1

        self.assertEqual(values, dict())

        identifier = self.scheduler.add_callable(update_values_1)
        self.scheduler.wait_callable(identifier)
        self.assertEqual(identifier, 1)
        self.assertEqual(values, dict(a = 1))

        values = dict()

        def update_values_2():
            values["a"] = 2

        self.assertEqual(values, dict())

        identifier = self.scheduler.add_callable(update_values_2)
        time.sleep(0.1)
        self.scheduler.wait_callable(identifier)
        self.assertEqual(identifier, 2)
        self.assertEqual(values, dict(a = 2))
