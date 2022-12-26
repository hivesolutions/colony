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

CRITICAL = 50
""" Critical logging level """

ERROR = 40
""" Error logging level """

WARNING = 30
""" Warning logging level """

INFO = 20
""" Info logging level """

DEBUG = 10
""" Debug logging level """

NOTSET = 0
""" Not set logging level """

WARN = WARNING
""" Alias to WARNING log level """

_levelNames = {
    CRITICAL : "CRITICAL",
    ERROR : "ERROR",
    WARNING : "WARNING",
    INFO : "INFO",
    DEBUG : "DEBUG",
    NOTSET : "NOTSET",
    "CRITICAL" : CRITICAL,
    "ERROR" : ERROR,
    "WARN" : WARNING,
    "WARNING" : WARNING,
    "INFO" : INFO,
    "DEBUG" : DEBUG,
    "NOTSET" : NOTSET,
}
""" The map relating the log levels with the textual representation and vice-versa """

def getLogger(name):
    """
    Returns the dummy logger for the given name.

    :type name: String
    :param name: The name of the logger to retrieve.
    :rtype: DummyLogger
    :return: The dummy logger for the gtiven name.
    """

    return DummyLogger("dummy")

def getLevelName(level):
    """
    Returns the textual representation of logging level.

    :type level: int
    :param level: The logging level to retrieve the textual representation.
    :rtype: String
    :return: The textual representation of logging level.
    """

    return _levelNames.get(level, ("Level %s" % level))

class DummyLogger(object):
    """
    The dummy logger class.
    """

    def __init__(self, name, level = NOTSET):
        """
        Constructor of the class.

        :type name: String
        :param name: The name of the logger.
        :type level: int
        :param level: The logging level for the new logger.
        """

        pass

    def setLevel(self, level):
        """
        Sets the level of the logger.

        :type level: int
        :param level: The level of the logger.
        """

        pass

    def debug(self, msg, *args, **kwargs):
        """
        Prints a debug message to the logger.

        :type msg: String
        :param msg: The message to print.
        """

        pass

    def info(self, msg, *args, **kwargs):
        """
        Prints an info message to the logger.

        :type msg: String
        :param msg: The message to print.
        """

        pass

    def warning(self, msg, *args, **kwargs):
        """
        Prints a warning message to the logger.

        :type msg: String
        :param msg: The message to print.
        """

        pass

    def error(self, msg, *args, **kwargs):
        """
        Prints an error message to the logger.

        :type msg: String
        :param msg: The message to print.
        """

        pass

    def exception(self, msg, *args):
        """
        Prints an exception message to the logger.

        :type msg: String
        :param msg: The message to print.
        """

        pass

    def critical(self, msg, *args, **kwargs):
        """
        Prints a critical message to the logger.

        :type msg: String
        :param msg: The message to print.
        """

        pass

    def addHandler(self, hdlr):
        """
        Adds an handler to the logger.

        :type hdlr: Handler
        :param hdlr: The handler to add to the logger.
        """

        pass

    def removeHandler(self, hdlr):
        """
        Removes an handler from the logger.

        :type hdlr: Handler
        :param hdlr: The handler to remove from the logger.
        """

        pass

class StreamHandler(object):
    """
    The stream handler class.
    """

    def setFormatter(self, fmt):
        """
        Sets the formatter for this handler.
        """

        self.formatter = fmt

class Formatter(object):
    """
    The formatter class.
    """

    def __init__(self, format):
        """
        Constructor of the class.

        :type format: String
        :param format: The formatter format.
        """

        pass
