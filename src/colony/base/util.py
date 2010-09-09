#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2294 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:00:18 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import time

CPYTHON_ENVIRONMENT = "cpython"
""" CPython environment value """

JYTHON_ENVIRONMENT = "jython"
""" Jython environment value """

IRON_PYTHON_ENVIRONMENT = "iron_python"
""" IronPython environment value """

WINDOWS_OS = "windows"
""" The windows os value """

MAC_OS = "mac"
""" The mac os value """

UNIX_OS = "unix"
""" The unix os value """

OTHER_OS = "other"
""" The other os value """

UID_PRECISION = 8
""" Unique id precision """

class Event:
    """
    The class that describes an event to be used in a generic event queue.
    """

    event_name = None
    """ The name of the event """

    event_args = []
    """ The arguments of the event """

    def __init__(self, event_name, event_args = []):
        """
        Constructor of the class.

        @type event_name: String
        @param event_name: The name of the event.
        @type event_args: List
        @param event_args: The arguments of the event.
        """

        self.event_name = event_name
        self.event_args = event_args

def module_import(module_name):
    """
    Imports the module with the given name.

    @type module_name: String
    @param module_name: The name of the module to be imported.
    @rtype: module
    @return: The imported module.
    """

    module = __import__(module_name)
    components = module_name.split(".")
    for component in components[1:]:
        module = getattr(module, component)
    return module

def get_environment():
    """
    Retrieves the current python environment.

    @rtype: String
    @return: The type of the current python environment.
    """

    platform = sys.platform

    if platform.find("java") != -1:
        return JYTHON_ENVIRONMENT
    elif platform.find("cli") != -1:
        return IRON_PYTHON_ENVIRONMENT
    else:
        return CPYTHON_ENVIRONMENT

def get_operative_system():
    """
    Retrieves the current operative system.

    @rtype: String
    @return: The type of the current operative system.
    """

    # retrieves the current os name
    os_name = os.name

    if os_name == "nt" or os_name == "dos":
        return WINDOWS_OS
    elif os_name == "mac":
        return MAC_OS
    elif os_name == "posix":
        return UNIX_OS

    return OTHER_OS

def get_timestamp_uid():
    """
    Retrieves a unique id based in the current timestamp.

    @rtype: String
    @return: A unique id based in the current timestamp.
    """

    # retrieves the current timestamp
    timestamp = time.time()

    # increments precision decimal places
    float_value = timestamp * (10 ** UID_PRECISION)

    # retrieves the integer value
    integer_value = long(float_value)

    # converts the integer value to string value
    string_value = str(integer_value)

    # returns the string value
    return string_value
