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

__revision__ = "$LastChangedRevision: 3219 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-05-26 11:52:00 +0100 (ter, 26 Mai 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

def xor_string_value(first_string, second_string):
    """
    Runs the xor bitwise operation over all the items
    of both strings, retrieving the result.

    @type first_string: String
    @param first_string: The first string to the xor operation.
    @type second_string: String
    @param second_string: The second string to the xor operation.
    @rtype: String
    @return: The "string" result of the xor operation.
    """

    # retrieves the length of the first string
    first_string_length = len(first_string)

    # retrieves the length of the second string
    second_string_length = len(second_string)

    # in case the string have different length
    if not first_string_length == second_string_length:
        # raises the value erorr exception
        raise ValueError("Arguments to xor string must have the same length")

    # creates the list to hold the resulting characters
    result_character_list = []

    # iterates over all the characters in both strings
    for first_character, second_character in zip(first_string, second_string):
        # calculates the result character from the first and second characters
        result_character = chr(ord(first_character) ^ ord(second_character))

        # adds the result character to the result character list
        result_character_list.append(result_character)

    # joins the result character list to retrieve
    # the final xor result
    xor_result = "".join(result_character_list)

    # returns the xor result
    return xor_result
