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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import re

UNDERSCORE_FIRST_VALUE = "(.)([A-Z][a-z]+)"
""" The underscore first value """

UNDERSCORE_FIRST_REGEX = re.compile(UNDERSCORE_FIRST_VALUE)
""" The underscore first regex """

UNDERSCORE_SECOND_VALUE = "([a-z0-9])([A-Z])"
""" The underscore second value """

UNDERSCORE_SECOND_REGEX = re.compile(UNDERSCORE_SECOND_VALUE)
""" The underscore second regex """

def xor_string_value(first_string, second_string):
    """
    Runs the xor bitwise operation over all the items
    of both strings, retrieving the result.

    :type first_string: String
    :param first_string: The first string to the xor operation.
    :type second_string: String
    :param second_string: The second string to the xor operation.
    :rtype: String
    :return: The "string" result of the xor operation.
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

def to_underscore(string_value):
    """
    Converts the given camel cased string value into
    the underscore notation.
    This method is useful to treat class string values in python.

    :type string_value: String
    :param string_value: The camel cased string value to be converted
    into underscore notation.
    :rtype: String
    :return: The converted underscore notation string value.
    """

    # converts the string value into the initial underscore notation
    string_value_underscore = UNDERSCORE_FIRST_REGEX.sub(r"\1_\2", string_value)

    # converts the string value underscore into the next underscore notation
    string_value_underscore = UNDERSCORE_SECOND_REGEX.sub(r"\1_\2", string_value_underscore)

    # converts the string value in underscore notation to lowercase
    string_value_underscore = string_value_underscore.lower()

    # returns the string value in underscore notation
    return string_value_underscore

def to_camelcase(string_value):
    """
    Converts the given underscore notation string value into
    the camel case notation.
    This method is useful to treat class string values in python.

    :type string_value: String
    :param string_value: The underscore notation string
    value to be converted into camel case notation.
    :rtype: String
    :return: The converted camel case notation string value.
    """

    # splits the string value retrieving
    # the string value tokens
    string_value_tokens = string_value.split("_")

    # creates a list with all the string value tokens capitalized
    string_value_tokens_capitalized = [value.capitalize() for value in string_value_tokens]

    # joins the various string value tokens
    # creating the string value camel case
    string_value_camelcase = "".join(string_value_tokens_capitalized)

    # returns the string value camel case
    return string_value_camelcase

def pluralize(string_value):
    """
    Pluralizes the given string value, using a
    typical heuristic for it.

    :type string_value: String
    :param string_value: The string to be pluralized.
    :rtype: String
    :return: The pluralized string.
    """

    return "%ss" % string_value

def capitalize_all(string_value):
    """
    Takes a space separated string value
    and capitalizes all of its words.

    :type string_value: String
    :param string_value: The space separated string
    to be capitalized.
    :rtype: String
    :return: The capitalized string.
    """

    # splits the string value retrieving
    # the string value tokens
    string_value_tokens = string_value.split()

    # creates a list with all the string value tokens capitalized
    string_value_tokens_capitalized = [value.capitalize() for value in string_value_tokens]

    # joins the various string value tokens
    # creating the string value capitalized
    string_value_capitalized = " ".join(string_value_tokens_capitalized)

    # returns the string value capitalized
    return string_value_capitalized

def join(first_value, second_value, join_value = "/"):
    """
    Joins two string making sure that the join value is
    not repeated in the "join point" (no double join).
    The "join point" is guaranteed to be unique.

    :type first_value: String
    :param first_value: The first string to be joined.
    :type second_value: String
    :param second_value: The second string to be joined.
    :type join_value: String
    :param join_value: The join value to be verifies and
    used in the "join point".
    :rtype: String
    :return: The joined string ensured to be with a single
    join point (not repeated).
    """

    # removes the join value from both the first and second value
    # to avoid duplicate values in the joining
    first_value = not first_value.endswith(join_value) and first_value or first_value[:-1]
    second_value = not second_value.startswith(join_value) and second_value or second_value[1:]

    # joins the first and second values using the join
    # value from the join point
    string_value = join_value.join((first_value, second_value))

    # returns the "resulting" stirng value
    return string_value
