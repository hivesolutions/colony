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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.string_buffer_util

QUOTE_SAFE_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-"
""" The string containing all the safe characters to be quoted """

QUOTE_SAFE_MAPS = {}
""" The map of cached (buffered) safe lists to be quoted """

HEX_TO_CHAR_MAP = dict(("%02x" % i, chr(i)) for i in range(256))
""" The map associating the hexadecimal byte (256) values with the integers """

# updates the map with the upper case values
HEX_TO_CHAR_MAP.update(("%02X" % i, chr(i)) for i in range(256))

def quote(string_value, safe = "/"):
    """
    Quotes the given string value according to
    the url encoding specification.
    The implementation is based on the python base library.

    @type string_value: String
    @param string_value: The string value to be quoted.
    @rtype: String
    @return: The quoted string value.
    """

    # creates the cache key tuple
    cache_key = (safe, QUOTE_SAFE_CHAR)

    try:
        # in case the cache key is not defined
        # in the quote sage maps creates a new entry
        safe_map = QUOTE_SAFE_MAPS[cache_key]
    except KeyError:
        # adds the "base" quote safe characters to the
        # "safe list"
        safe += QUOTE_SAFE_CHAR

        # starts the safe map
        safe_map = {}

        # iterates over all the ascii values
        for index in range(256):
            # retrieves the character for the
            # given index
            character = chr(index)

            # adds the "valid" character ot the safe mao entry
            safe_map[character] = (character in safe) and character or ("%%%02X" % index)

        # sets the safe map in the cache quote safe maps
        QUOTE_SAFE_MAPS[cache_key] = safe_map

    # maps the getitem method of the map to all the string
    # value to retrieve the valid items
    resolution_list = map(safe_map.__getitem__, string_value)

    # joins the resolution list to retrieve the quoted value
    return "".join(resolution_list)

def quote_plus(string_value, safe = ""):
    """
    Quotes the given string value according to
    the url encoding specification. This kind of quote
    takes into account the plus and the space relation.
    The implementation is based on the python base library.

    @type string_value: String
    @param string_value: The string value to be quoted.
    @type safe: String
    @param safe: The string containing the characters considered
    safe for quoting.
    @rtype: String
    @return: The quoted string value.
    """

    # in case there is at least one white
    # space in the string value
    if " " in string_value:
        # quotes the string value adding the white space
        # to the "safe list"
        string_value = quote(string_value, safe + " ")

        # replaces the white spaces with plus signs and
        # returns the result
        return string_value.replace(" ", "+")

    # returns the quoted string value
    return quote(string_value, safe)

def unquote(string_value):
    """
    Unquotes the given string value according to
    the url encoding specification.
    The implementation is based on the python base library.

    @type string_value: String
    @param string_value: The string value to be unquoted.
    @rtype: String
    @return: The unquoted string value.
    """

    # splits the string value around
    # percentage value
    string_value_splitted = string_value.split("%")

    # iterates over all the "percentage values" range
    for index in xrange(1, len(string_value_splitted)):
        # retrieves the current iteration item
        item = string_value_splitted[index]

        try:
            string_value_splitted[index] = HEX_TO_CHAR_MAP[item[:2]] + item[2:]
        except KeyError:
            string_value_splitted[index] = "%" + item
        except UnicodeDecodeError:
            string_value_splitted[index] = unichr(int(item[:2], 16)) + item[2:]

    # returns the joined "partial" string value
    return "".join(string_value_splitted)

def unquote_plus(string_value):
    """
    Unquotes the given string value according to
    the url encoding specification. This kind of unquote
    takes into account the plus and the space relation.
    The implementation is based on the python base library.

    @type string_value: String
    @param string_value: The string value to be unquoted.
    @rtype: String
    @return: The unquoted string value.
    """

    # replaces the plus sign with a space
    string_value = string_value.replace("+", " ")

    # returns the unquoted string value
    return unquote(string_value)

def url_encode(attributes_map, plus_encoding = False):
    """
    Encodes the given attributes into url encoding.

    @type attributes_map: Dictionary.
    @param attributes_map: The map of attributes to be encoded
    using url encoding.
    @type plus_encoding: bool
    @param plus_encoding: If the plus encoding should be used.
    @rtype: String
    @return: The encoded attributes string.
    """

    # retrieves the quote method to be used
    quote_method = plus_encoding and quote_plus or quote

    # creates a string buffer to hold the encoded attribute values
    string_buffer = colony.libs.string_buffer_util.StringBuffer()

    # sets the is first flag
    is_first = True

    # iterates over all the attribute keys and values
    for attribute_key, attribute_value in attributes_map.items():
        # quotes both the attribute key and value
        attribute_key_quoted = quote_method(attribute_key)
        attribute_value_quoted = quote_method(attribute_value)

        # in case it's is the first iteration
        if is_first:
            # unsets the is first flag
            is_first = False
        else:
            # writes the and continuation in the string buffer
            string_buffer.write("&")

        # adds the quoted key and value strings to the
        # string buffer
        string_buffer.write(attribute_key_quoted)
        string_buffer.write("=")
        string_buffer.write(attribute_value_quoted)

    # retrieves the encoded attributes from the string buffer
    encoded_attributes = string_buffer.get_value()

    # returns the encoded attributes
    return encoded_attributes
