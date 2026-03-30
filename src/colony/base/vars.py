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

    :type name: str
    :param name: The name of the global variable.
    :type: value: object
    :param value: The value to assign to the global variable.
    """

    GLOBALS[name] = value


def get_global(name, default=None):
    """
    Returns the value of a global variable,
    if found, otherwise the default value.

    :type name: str
    :param name: The name of the global variable.
    :type name: object
    :param default: The default value to return if
    the global variable is not found.
    :rtype: object
    :return: The value of the global variable if found,
    otherwise the default value.
    """

    return GLOBALS.get(name, default)


def has_global(name):
    """
    Checks if a global variable with the given name exists.

    :type name: str
    :param name: The name of the global variable to check.
    :rtype: bool
    :return: True if the global variable exists, False otherwise.
    """

    return name in GLOBALS


def delete_global(name):
    """
    Deletes a global variable with the given name.

    :type name: str
    :param name: The name of the global variable to delete.
    """

    if name not in GLOBALS:
        return
    del GLOBALS[name]
