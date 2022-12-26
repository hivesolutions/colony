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

import logging

import colony

class LoggersTest(colony.ColonyTestCase):
    """
    Test case for the verification of logging related
    methods and functions of colony.
    """

    def test_memory_handler(self):
        memory_handler = colony.MemoryHandler()
        formatter = logging.Formatter("%(message)s")
        memory_handler.setFormatter(formatter)

        latest = memory_handler.get_latest()
        self.assertEqual(len(latest), 0)
        self.assertEqual(latest, [])

        record = logging.makeLogRecord(
            dict(
                msg = "hello world",
                levelname = logging.getLevelName(logging.INFO)
            )
        )
        memory_handler.emit(record)
        latest = memory_handler.get_latest()

        self.assertEqual(len(latest), 1)
        self.assertEqual(latest, ["hello world"])

        record = logging.makeLogRecord(
            dict(
                msg = "hello world 2",
                levelname = logging.getLevelName(logging.ERROR)
            )
        )
        memory_handler.emit(record)
        latest = memory_handler.get_latest()

        self.assertEqual(len(latest), 2)
        self.assertEqual(latest, ["hello world 2", "hello world"])

        latest = memory_handler.get_latest(level = logging.ERROR)

        self.assertEqual(len(latest), 1)
        self.assertEqual(latest, ["hello world 2"])

        latest = memory_handler.get_latest(level = logging.CRITICAL)

        self.assertEqual(len(latest), 0)
        self.assertEqual(latest, [])

        latest = memory_handler.get_latest(level = logging.INFO)

        self.assertEqual(len(latest), 2)
        self.assertEqual(latest, ["hello world 2", "hello world"])

        latest = memory_handler.get_latest(count = 1, level = logging.INFO)

        self.assertEqual(len(latest), 1)
        self.assertEqual(latest, ["hello world 2"])

    def test_memory_handler_file(self):
        memory_handler = colony.MemoryHandler()
        formatter = logging.Formatter("%(message)s")
        memory_handler.setFormatter(formatter)

        latest = memory_handler.get_latest()
        self.assertEqual(len(latest), 0)
        self.assertEqual(latest, [])

        record = logging.makeLogRecord(
            dict(
                msg = "hello world",
                levelname = logging.getLevelName(logging.INFO)
            )
        )
        memory_handler.emit(record)
        record = logging.makeLogRecord(
            dict(
                msg = "hello world 2",
                levelname = logging.getLevelName(logging.INFO)
            )
        )
        memory_handler.emit(record)

        file = colony.legacy.BytesIO()

        memory_handler.flush_to_file(file, clear = False)

        file.seek(0)
        contents = file.read()

        self.assertEqual(contents, b"hello world\nhello world 2\n")

        file = colony.legacy.BytesIO()

        memory_handler.flush_to_file(file, reverse = False)

        file.seek(0)
        contents = file.read()

        self.assertEqual(contents, b"hello world 2\nhello world\n")

        latest = memory_handler.get_latest(count = 1)
        self.assertEqual(len(latest), 0)
