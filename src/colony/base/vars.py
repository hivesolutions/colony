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

__author__ = "Hugo Gomes <hugo@frontdoorhq.com>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

GLOBALS = {}


def set_global(name, value):
    """
    Sets a global variable with the given name and value.

    :param name: The name of the global variable.
    :param value: The value to assign to the global variable.
    """
    GLOBALS[name] = value


def get_global(name, default=None):
    """
    Returns the value of a global variable,
    if found, otherwise the default value.

    :param name: The name of the global variable.
    :param default: The default value to return if
    the global variable is not found.
    :return: The value of the global variable if found,
    otherwise the default value.
    """
    return GLOBALS.get(name, default)


def has_global(name):
    """
    Checks if a global variable with the given name exists.

    :param name: The name of the global variable to check.
    :type name: str
    :return: True if the global variable exists, False otherwise.
    :rtype: bool
    """
    return name in GLOBALS
