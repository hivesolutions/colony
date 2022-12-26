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

from colony.base import legacy

from . import string_buffer_util

QUOTE_SAFE_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-"
""" The string containing all the safe characters to be quoted """

QUOTE_SAFE_MAPS = {}
""" The map of cached (buffered) safe lists to be quoted """

HEX_TO_CHAR_MAP = dict((legacy.bytes("%02x" % i), legacy.bytes(chr(i))) for i in range(256))
""" The map associating the hexadecimal byte (256) values
with the integers, the association is done using byte values """

# updates the map with the upper case values
HEX_TO_CHAR_MAP.update((legacy.bytes("%02X" % i), legacy.bytes(chr(i))) for i in range(256))

def quote(string_value, safe = "/"):
    """
    Quotes the given string value according to
    the URL encoding specification.
    The implementation is based on the python base library.

    :type string_value: String
    :param string_value: The string value to be quoted.
    :rtype: String
    :return: The quoted string value.
    """

    # in case the provided string value is unicode based it
    # must be encoded first using the default encoder
    is_unicode = type(string_value) == legacy.UNICODE
    if is_unicode: string_value = string_value.encode("utf-8")

    # creates the cache key tuple, that is going to be used
    # to avoid the re-creation of the safe map in every operation
    cache_key = (safe, QUOTE_SAFE_CHAR)

    try:
        # in case the cache key is not defined
        # in the quote safe maps, creates a new entry
        safe_map = QUOTE_SAFE_MAPS[cache_key]
    except KeyError:
        # adds the "base" quote safe characters to the
        # "safe list"
        safe += QUOTE_SAFE_CHAR

        # starts the safe map
        safe_map = {}

        # iterates over all the ascii values
        for index in range(256):
            # retrieves the character for the given index,
            # note that this strategy takes into account the
            # current version of the python environment
            character = chr(index)
            reference = index if legacy.PYTHON_3 else character

            # adds the "valid" character or the safe map entry
            safe_map[reference] = character if (character in safe) else ("%%%02X" % index)

        # sets the safe map in the cache quote safe maps
        QUOTE_SAFE_MAPS[cache_key] = safe_map

    # maps the get item method of the map to all the string
    # values to retrieve the valid items
    resolution_list = map(safe_map.__getitem__, string_value)

    # joins the resolution list to retrieve the quoted value
    # this will trigger the lazy loaded map operation
    return "".join(resolution_list)

def quote_plus(string_value, safe = ""):
    """
    Quotes the given string value according to
    the URL encoding specification. This kind of quote
    takes into account the plus and the space relation.
    The implementation is based on the python base library.

    :type string_value: String
    :param string_value: The string value to be quoted.
    :type safe: String
    :param safe: The string containing the characters considered
    safe for quoting.
    :rtype: String
    :return: The quoted string value.
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

def unquote(string_value, strict = True):
    """
    Unquotes the given string value according to the URL
    encoding specification.
    The implementation is based on the python base library.

    :type string_value: String
    :param string_value: The string value to be unquoted, this
    string should be either encoded as an utf-8 based string
    or decoded with the proper unicode representation.
    :type strict: bool
    :param strict: If the unquoting operation should be performed
    using a strict approach meaning that all the characters are
    properly validated for ascii compliance, avoid duplicated
    unquoting operations.
    :rtype: String
    :return: The unquoted string value, this value is either
    returned as an utf-8 encoded string or an unicode string.
    """

    # forces the encoding of the string value as a string and
    # then splits the string value around percentage value
    # so that the various partial encoded values are decoded
    is_unicode = type(string_value) == legacy.UNICODE
    encoding = "ascii" if strict else "utf-8"
    if is_unicode: string_value = string_value.encode(encoding)
    if strict: string_value.decode("ascii")
    string_value_splitted = string_value.split(b"%")

    # iterates over all the "percentage values" range to decode
    # the complete set of percent encoded characters
    for index in range(1, len(string_value_splitted)):
        # retrieves the current iteration item, that is going to
        # be decoded using the hexadecimal to character map
        item = string_value_splitted[index]

        try:
            # tries to run the decoding operation using the hexadecimal
            # to character map and appends the remaining string value
            string_value_splitted[index] = HEX_TO_CHAR_MAP[item[:2]] + item[2:]
        except KeyError:
            # in case the decoding failed (no processing possible) the raw
            # value is set instead of the decoded value (fallback strategy)
            string_value_splitted[index] = b"%" + item

    # joins the various partial string values to be able to retrieve
    # the full unquoted utf-8 encoded string/bytes values, the value
    # is then decoded in case the current environment requires it
    unquoted = b"".join(string_value_splitted)
    return unquoted.decode("utf-8") if legacy.PYTHON_3 else unquoted

def unquote_plus(string_value, strict = True):
    """
    Unquotes the given string value according to
    the URL encoding specification. This kind of unquote
    takes into account the plus and the space relation.
    The implementation is based on the python base library.

    :type string_value: String
    :param string_value: The string value to be unquoted, this
    string should be either encoded as an utf-8 based string
    or decoded with the proper unicode representation.
    :type strict: bool
    :param strict: If the unquoting operation should be performed
    using a strict approach meaning that all the characters are
    properly validated for ascii compliance, avoid duplicated
    unquoting operations.
    :rtype: String
    :return: The unquoted string value.
    """

    # replaces the plus sign with a space, this is considered
    # the default plus symbol substitution, note that the proper
    # replacement operation is used according to base data type
    is_bytes = legacy.is_bytes(string_value)
    if is_bytes: string_value = string_value.replace(b"+", b" ")
    else: string_value = string_value.replace("+", " ")

    # returns the unquoted string value
    return unquote(string_value, strict = strict)

def url_encode(attributes_map = None, attributes_list = None, plus_encoding = False):
    """
    Encodes the given attributes into URL encoding. The
    attributes may be either provided as a map or alternatively
    as a sequence of key value tuples.

    :type attributes_map: Dictionary
    :param attributes_map: The map of attributes to be encoded
    using URL encoding, if this value is defined the attributes
    list is not going to be used.
    :type attributes_list: List
    :param attributes_list: The list of key and value tuples
    that are going to be processed as the attributes.
    :type plus_encoding: bool
    :param plus_encoding: If the plus encoding should be used.
    :rtype: String
    :return: The encoded attributes string.
    """

    # retrieves the quote method to be used
    quote_method = plus_encoding and quote_plus or quote

    # creates a string buffer to hold the encoded attribute values
    string_buffer = string_buffer_util.StringBuffer()

    # retrieves the reference to the proper items sequence to be used
    # notice that the attributes map has preference to the list version
    items = legacy.iteritems(attributes_map) if attributes_map else attributes_list

    # sets the is first flag, that is going to be used in the iteration
    # cycle to define the first iteration (exceptional iteration)
    is_first = True

    # iterates over all the attribute keys and values to be able to
    # quote their values and append the value to the buffer
    for attribute_key, attribute_value in items:
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
