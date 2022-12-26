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

import binascii

from colony.base import legacy

def encode_two_complement_string(long_value):
    """
    Encode a long to a two's complement little-endian binary string.
    Note that "0L" is a special case, returning an empty string, to save a
    byte.

    :type long_value: int
    :param long_value: The long value to be encoded.
    :rtype: String
    :return: The encoded two's complement little-endian binary string.
    """

    # in case the long value is zero
    if long_value == 0:
        # returns empty string
        return ""
    # in case the long value is larger
    # than zero
    elif long_value > 0:
        # converts the long value to the hexadecimal string value
        long_value_hexadecial = hex(long_value)

        # counts the number of nibbles in the given value
        number_nibbles = _count_nibbles(long_value_hexadecial)

        # in case the number of nibbles is odd
        if number_nibbles & 1:
            # need an even # of nibbles for unhexlify
            long_value_hexadecial = "0x0" + long_value_hexadecial[2:]
        # in case the number i
        elif int(long_value_hexadecial[2], 16) >= 8:
            # looks negative so need a byte of sign bits
            long_value_hexadecial = "0x00" + long_value_hexadecial[2:]
    else:
        # converts the (negative) long value to the hexadecimal string value
        long_value_hexadecial = hex(-long_value)

        # counts the number of nibbles in the given value
        number_nibbles = _count_nibbles(long_value_hexadecial)

        # in case the number of nibbles is odd
        if number_nibbles & 1:
            # extends to a full byte.
            number_nibbles += 1

        # calculates the number of bits from the nibbles
        number_bits = number_nibbles * 4

        # puts the negative indication as the last digit
        long_value += 1 << number_bits

        # converts the long value to the hexadecimal string value
        long_value_hexadecial = hex(long_value)

        # counts the number of nibbles in the given value
        new_number_nibbles = _count_nibbles(long_value_hexadecial)

        # in case the new number of nibbles is smaller than
        # the previous one
        if new_number_nibbles < number_nibbles:
            # puts the sign bits
            long_value_hexadecial = "0x" + "0" * (number_nibbles - new_number_nibbles) + long_value_hexadecial[2:]
        # in case it's a positive number
        if int(long_value_hexadecial[2], 16) < 8:
            # no need a byte of sign bits
            long_value_hexadecial = "0xff" + long_value_hexadecial[2:]

    # in case the long value hexadecimal ends with the long
    # indication value
    if long_value_hexadecial.endswith("L"):
        # removes the last character to avoid the extra long indication
        long_value_hexadecial = long_value_hexadecial[2:-1]
    # otherwise
    else:
        # sets the normal value without the "0x" initialization
        long_value_hexadecial = long_value_hexadecial[2:]

    # unhexflies the value retrieving the binary value
    binary = binascii.unhexlify(long_value_hexadecial)

    # reverses the binary value
    reversed_binary = binary[::-1]

    # returns the reversed binary value
    return reversed_binary

def decode_two_complement_string(data):
    """
    Decode a long from a two's complement little-endian binary string.

    :type data: String
    :param data: The data to be used in the decoding.
    :rtype: int
    :return: The decoded data.
    """

    # retrieves the data length
    data_length = len(data)

    # in case the data length is zero
    if data_length == 0:
        # return zero
        return legacy.LONG(0)

    # converts the (inverted) data to hexadecimal string
    long_value_hexadecial = binascii.hexlify(data[::-1])

    # converts the long value hexadecimal to integer
    # using base 16
    long_value = legacy.LONG(long_value_hexadecial, 16)

    # in case the last digit is 0x80 (negative)
    if data[-1] >= "\x80":
        # puts the negative indication as the last digit
        long_value -= legacy.LONG(1) << (data_length * 8)

    # returns the long value
    return long_value

def _count_nibbles(long_value_hexadecial):
    """
    Calculates the number of nibbles (4 bit group) from the given
    long value encoded in hexadecimal string.

    :type long_value_hexadecial: String
    :param long_value_hexadecial: The long value encoded in
    hexadecimal string to count the nibbles.
    :rtype: int
    :return: The number of nibbles in the given value.
    """

    # calculates the number of "junk" characters
    number_junk_characters = 2 + long_value_hexadecial.endswith("L")

    # calculates the number of nibbles from the length of the
    # long value string without the junk characters
    number_nibbles = len(long_value_hexadecial) - number_junk_characters

    # returns the number of nibbles
    return number_nibbles
