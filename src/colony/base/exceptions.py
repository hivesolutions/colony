#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import uuid

class ColonyException(Exception):
    """
    The top level colony exception, this is the main exception
    for the complete colony infra-structure and all the other
    exceptions should inherit from this one.
    """

    message = None
    """ The exception's message, to be used latter for runtime
    based diagnostics """

    def __init__(self, message = None):
        Exception.__init__(self)
        self.message = message
        self._uid = None

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        if self.message == None: return Exception.__str__(self)
        return "Colony exception - %s" % self.message

    def __unicode__(self):
        """
        Returns the unicode representation of the class.

        :rtype: String
        :return: The unicode representation of the class.
        """

        return self.__str__()

    @property
    def uid(self):
        """
        The unique identifier of the current exception may
        be used safely from a global/universal point of view.

        :rtype: String
        :return: The global unique identifier of the current
        exception entity.
        """

        if self._uid: return self._uid
        self._uid = uuid.uuid4()
        return self._uid

class PluginSystemException(ColonyException):
    """
    The plugin system exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ColonyException.__init__(self, message = message)

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Plugin system exception - %s" % self.message

class PluginClassNotAvailable(PluginSystemException):
    """
    The plugin class not available class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        PluginSystemException.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Plugin class not available - %s" % self.message

class InvalidCommand(PluginSystemException):
    """
    The invalid command class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        PluginSystemException.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Invalid command - %s" % self.message

class InvalidArgument(PluginSystemException):
    """
    The invalid argument class, meaning that some passed
    parameter/argument is not valid under the context of
    the current execution.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        PluginSystemException.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Invalid argument - %s" % self.message

class SecurityError(PluginSystemException):
    """
    The security (kind) error, that represents an issue
    related with something that may be able to compromise
    the security of the system.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        PluginSystemException.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Security error - %s" % self.message

class OperationNotComplete(PluginSystemException):
    """
    The operation not complete class, meaning that the
    some operation has been blocked in the middle of execution.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        PluginSystemException.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Operation not complete - %s" % self.message

class OperationRestart(PluginSystemException):
    """
    The operation restart class, meaning that the current
    executing operation should be restart by its owner (up
    in the call stack).
    """

    def __init__(self, message, delay = 0):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        :type delay: float
        :param delay: The delay (in seconds) to be used in
        the waiting before the restart of the operation.
        """

        PluginSystemException.__init__(self, message)
        self.message = message
        self.delay = delay

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        delay_s = " (%0.1f seconds delay)" % self.delay if self.delay else ""
        return "Operation restart%s - %s" % (delay_s, self.message)
