#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import logging

import colony

from colony.base import loggers

try:
    import unittest.mock as mock
except ImportError:
    mock = None


class LoggersTest(colony.ColonyTestCase):
    """
    Test case for the verification of logging related
    methods and functions of colony.
    """

    def test_silent_value(self):
        self.assertEqual(colony.SILENT, logging.CRITICAL + 1)
        self.assertEqual(type(colony.SILENT), int)

    def test_silent_above_critical(self):
        self.assertTrue(colony.SILENT > logging.CRITICAL)

    def test_trace_value(self):
        self.assertEqual(colony.TRACE, 5)
        self.assertEqual(colony.TRACE, logging.DEBUG - 5)
        self.assertEqual(type(colony.TRACE), int)

    def test_trace_below_debug(self):
        self.assertTrue(colony.TRACE < logging.DEBUG)

    def test_level_ordering(self):
        self.assertTrue(colony.TRACE < logging.DEBUG)
        self.assertTrue(logging.DEBUG < logging.INFO)
        self.assertTrue(logging.INFO < logging.WARNING)
        self.assertTrue(logging.WARNING < logging.ERROR)
        self.assertTrue(logging.ERROR < logging.CRITICAL)
        self.assertTrue(logging.CRITICAL < colony.SILENT)

    def test_patch_logging(self):
        colony.patch_logging()

        result = logging.getLevelName(colony.TRACE)

        self.assertEqual(result, "TRACE")

    def test_patch_logging_reverse(self):
        colony.patch_logging()

        result = logging.getLevelName("TRACE")

        self.assertEqual(result, colony.TRACE)

    def test_patch_logging_idempotent(self):
        colony.patch_logging()
        colony.patch_logging()

        result = logging.getLevelName(colony.TRACE)

        self.assertEqual(result, "TRACE")

    def test_patch_logging_logger_trace(self):
        colony.patch_logging()

        logger = logging.getLogger("colony.test.trace")

        self.assertTrue(hasattr(logger, "trace"))
        self.assertTrue(callable(logger.trace))

    def test_patch_logging_logger_trace_call(self):
        colony.patch_logging()

        logger = logging.getLogger("colony.test.trace.call")
        logger.setLevel(colony.TRACE)
        records = []
        handler = logging.Handler()
        handler.setLevel(colony.TRACE)
        handler.emit = lambda record: records.append(record)
        logger.addHandler(handler)

        try:
            logger.trace("trace test message")

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].getMessage(), "trace test message")
            self.assertEqual(records[0].levelno, colony.TRACE)
            self.assertEqual(records[0].levelname, "TRACE")
        finally:
            logger.removeHandler(handler)

    def test_patch_logging_logger_trace_filtered(self):
        colony.patch_logging()

        logger = logging.getLogger("colony.test.trace.filtered")
        logger.setLevel(logging.DEBUG)
        records = []
        handler = logging.Handler()
        handler.setLevel(colony.TRACE)
        handler.emit = lambda record: records.append(record)
        logger.addHandler(handler)

        try:
            # the trace message should be filtered since the logger
            # level is set to DEBUG which is above TRACE
            logger.trace("this should be filtered")

            self.assertEqual(len(records), 0)
        finally:
            logger.removeHandler(handler)

    def test_get_level_int_trace(self):
        result = colony.getLevelInt("TRACE")

        self.assertEqual(result, colony.TRACE)
        self.assertEqual(result, 5)

    def test_get_level_int_silent(self):
        result = colony.getLevelInt("SILENT")

        self.assertEqual(result, colony.SILENT)
        self.assertEqual(result, 51)

    def test_get_level_name_trace(self):
        result = colony.getLevelName("TRACE")

        self.assertEqual(result, loggers.TRACE)

    def test_get_level_name_silent(self):
        result = colony.getLevelName("SILENT")

        self.assertEqual(result, loggers.SILENT)

    def test_dummy_logger_trace(self):
        logger = colony.DummyLogger("test")

        self.assertTrue(hasattr(logger, "trace"))
        self.assertTrue(callable(logger.trace))

        # should not raise, just a no-op
        logger.trace("test message")

    def test_memory_handler(self):
        memory_handler = colony.MemoryHandler()
        formatter = logging.Formatter("%(message)s")
        memory_handler.setFormatter(formatter)

        latest = memory_handler.get_latest()
        self.assertEqual(len(latest), 0)
        self.assertEqual(latest, [])

        record = logging.makeLogRecord(
            dict(msg="hello world", levelname=logging.getLevelName(logging.INFO))
        )
        memory_handler.emit(record)
        latest = memory_handler.get_latest()

        self.assertEqual(len(latest), 1)
        self.assertEqual(latest, ["hello world"])

        record = logging.makeLogRecord(
            dict(msg="hello world 2", levelname=logging.getLevelName(logging.ERROR))
        )
        memory_handler.emit(record)
        latest = memory_handler.get_latest()

        self.assertEqual(len(latest), 2)
        self.assertEqual(latest, ["hello world 2", "hello world"])

        latest = memory_handler.get_latest(level=logging.ERROR)

        self.assertEqual(len(latest), 1)
        self.assertEqual(latest, ["hello world 2"])

        latest = memory_handler.get_latest(level=logging.CRITICAL)

        self.assertEqual(len(latest), 0)
        self.assertEqual(latest, [])

        latest = memory_handler.get_latest(level=logging.INFO)

        self.assertEqual(len(latest), 2)
        self.assertEqual(latest, ["hello world 2", "hello world"])

        latest = memory_handler.get_latest(count=1, level=logging.INFO)

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
            dict(msg="hello world", levelname=logging.getLevelName(logging.INFO))
        )
        memory_handler.emit(record)
        record = logging.makeLogRecord(
            dict(msg="hello world 2", levelname=logging.getLevelName(logging.INFO))
        )
        memory_handler.emit(record)

        file = colony.legacy.BytesIO()

        memory_handler.flush_to_file(file, clear=False)

        file.seek(0)
        contents = file.read()

        self.assertEqual(contents, b"hello world\nhello world 2\n")

        file = colony.legacy.BytesIO()

        memory_handler.flush_to_file(file, reverse=False)

        file.seek(0)
        contents = file.read()

        self.assertEqual(contents, b"hello world 2\nhello world\n")

        latest = memory_handler.get_latest(count=1)
        self.assertEqual(len(latest), 0)

    def test_logstash_handler(self):
        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        mock_api_client = mock.Mock()
        mock_api_client_messages = []
        mock_api_client.log_bulk = (
            lambda messages, tag, raise_e="default": mock_api_client_messages.extend(
                messages
            )
        )

        logstash_handler = colony.LogstashHandler(api=mock_api_client)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        logstash_handler.setFormatter(formatter)

        self.assertEqual(len(logstash_handler.messages), 0)

        record = logging.makeLogRecord(
            dict(msg="hello world", levelname=logging.getLevelName(logging.INFO))
        )
        logstash_handler.emit(record)
        self.assertEqual(len(logstash_handler.messages), 1)
        self.assertEqual(
            logstash_handler.messages[0]["message_fmt"], "INFO - hello world"
        )
        self.assertEqual(logstash_handler.messages[0]["message"], "hello world")
        self.assertEqual(logstash_handler.messages[0]["level"], "INFO")
        self.assertEqual(logstash_handler.messages[0]["logger"], None)
        self.assertEqual(logstash_handler.messages[0]["path"], "")

        logstash_handler.flush()
        self.assertEqual(len(logstash_handler.messages), 0)
        self.assertEqual(len(mock_api_client_messages), 1)
        self.assertEqual(
            mock_api_client_messages[0]["message_fmt"], "INFO - hello world"
        )
        self.assertEqual(mock_api_client_messages[0]["message"], "hello world")
        self.assertEqual(mock_api_client_messages[0]["level"], "INFO")
        self.assertEqual(mock_api_client_messages[0]["logger"], None)
        self.assertEqual(mock_api_client_messages[0]["path"], "")

        record = logging.makeLogRecord(
            dict(msg="hello world 2", levelname=logging.getLevelName(logging.INFO))
        )
        logstash_handler.emit(record)
        self.assertEqual(len(logstash_handler.messages), 1)
        self.assertEqual(
            logstash_handler.messages[0]["message_fmt"], "INFO - hello world 2"
        )
        self.assertEqual(logstash_handler.messages[0]["message"], "hello world 2")
        self.assertEqual(logstash_handler.messages[0]["level"], "INFO")
        self.assertEqual(logstash_handler.messages[0]["logger"], None)
        self.assertEqual(logstash_handler.messages[0]["path"], "")
