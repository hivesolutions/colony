#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

class ColonyException(Exception):
    """
    The top level colony exception, this is the main exception
    for the complete colony infra-structure and all the other
    exceptions should inherit from this one.
    """

    def __unicode__(self):
        """
        Returns the unicode representation of the class.

        @rtype: String
        @return: The unicode representation of the class.
        """

        return self.__str__()

class PluginSystemException(ColonyException):
    """
    The plugin system exception class.
    """

    message = None
    """ The exception's message """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        ColonyException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Plugin system exception - %s" % self.message

class PluginClassNotAvailable(PluginSystemException):
    """
    The plugin class not available class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        PluginSystemException.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Plugin class not available - %s" % self.message

class InvalidCommand(PluginSystemException):
    """
    The invalid command class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        PluginSystemException.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Invalid command - %s" % self.message

class InvalidArgument(PluginSystemException):
    """
    The invalid argument class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        PluginSystemException.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Invalid argument - %s" % self.message

class OperationNotComplete(PluginSystemException):
    """
    The operation not complete class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        PluginSystemException.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Operation not complete - %s" % self.message
