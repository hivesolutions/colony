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

__author__ = "Luís Martinho <lmartinho@hive.pt> & João Magalhães <joamag@hive.pt>"
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

DIGIT_ENCODING_MAP = {
    "0" : "NNWWN",
    "1" : "WNNNW",
    "2" : "NWNNW",
    "3" : "WWNNN",
    "4" : "NNWNW",
    "5" : "WNWNN",
    "6" : "NWWNN",
    "7" : "NNNWW",
    "8" : "WNNWN",
    "9" : "NWNWN"
}
""" The digit encoding map converting the digit into
N(arrow) and W(ide) combinations, useful for 2 of 5 encoding  """

START_CODE_2_OF_5 = "NnNn"
""" The start code for 2 of 5 """

END_CODE_2_OF_5 = "WnN"
""" The end code for 2 of 5 """

START_CODES_CODE_128 = {
    "A" : 103,
    "B" : 104,
    "C" : 105
}
""" The code 128 start codes for each code set """

END_CODE_CODE_128 = 106
""" The end code for code 128 """

def encode_2_of_5(string_value):
    """
    Encodes the provided string value into the 2 of 5
    barcode encoding to be used with the most prominent
    true type fonts for display.

    :type string_value: String
    :param string_value: The string value to be encoded into
    the 2 of 5 barcode string representation.
    :rtype: String
    :return: The generated 2 of 5 barcode string representation.
    :see: http://en.wikipedia.org/wiki/Interleaved_2_of_5
    """

    # starts the encoded buffer with the default
    # start code for the 2 of 5
    encoded_buffer = string_buffer_util.StringBuffer()
    encoded_buffer.write(START_CODE_2_OF_5)

    # retrieves the length of the string value and the
    # uses it to check if the string value length is
    # of type odd or even
    string_value_length = len(string_value)
    is_even_length = string_value_length % 2 == 0

    # in case the string value does not contains an even
    # number of digits a zero character is prepended to
    # the string value (so that it's possible to codify it)
    if not is_even_length: string_value = "0" + string_value

    # resets the index counter
    index = 0

    # iterates over the range of indexes of the
    # string value range
    while index < string_value_length:
        # retrieves the first and second digits
        # for the current string value index
        first_digit = string_value[index]
        second_digit = string_value[index + 1]

        # encodes the first and second digits
        # using the the digit encoding map
        first_digit_encoded = DIGIT_ENCODING_MAP.get(first_digit, None)
        second_digit_encoded = DIGIT_ENCODING_MAP.get(second_digit, None)

        # in case at least one of the digits is not valid
        # (not possible to encoded) it, this is an error
        # situation and a runtime error must be raised
        if first_digit_encoded == None or second_digit_encoded == None: raise RuntimeError("Value is not serializable in 2 of 5 encoding")

        # interleaves both the first and second encoded
        # digits and then writes the result to the encoded buffer
        interleaved_digits_string = _interleave_digits(first_digit_encoded, second_digit_encoded)
        encoded_buffer.write(interleaved_digits_string)

        # increments the index counter in two values
        # so that so that the s
        index += 2

    # writes the end of the 2 of 5 encoding
    # value to the encoded buffer and then
    # retrieves the (final) encoded value
    encoded_buffer.write(END_CODE_2_OF_5)
    encoded_value = encoded_buffer.get_value()

    # returns the 2 of 5 encoded value
    return encoded_value

def encode_code_128(value, code_set = "A"):
    """
    Encodes the provided string value into the code 128
    barcode encoding to be used with the most prominent
    true type fonts for display.

    :type string_value: String
    :param string_value: The string value to be encoded into
    the code 128 barcode string representation.
    :rtype: String
    :return: The generated code 128 barcode string representation.
    :see: http://en.wikipedia.org/wiki/Code_128
    """

    # encodes the value into the proper representation
    # using the requested code set, in case no valid code
    # set is provided raises a runtime error
    if code_set == "A": character_values = _encode_code_set_a(value)
    elif code_set == "B": character_values = _encode_code_set_b(value)
    elif code_set == "C": character_values = _encode_code_set_c(value)
    else: raise RuntimeError("Specified code set not supported %s" % code_set)

    # computes and appends the check digit
    # using the current character values list
    check_digit = _calculate_check_digit(character_values)
    character_values.append(check_digit)

    # appends the final end code, to finish
    # the set of character values
    character_values.append(END_CODE_CODE_128)

    # retrieves the character string for the
    # code 128 values and returns it as the
    # final encoded unicode string
    character_string = _get_character_string(character_values)
    return character_string

def encode_code_39(value):
    """
    Encodes the provided string value into the code 39
    barcode encoding to be used with the most prominent
    true type fonts for display.

    :type string_value: String
    :param string_value: The string value to be encoded into
    the code 39 barcode string representation.
    :rtype: String
    :return: The generated code 39 barcode string representation.
    :see: http://en.wikipedia.org/wiki/Code_39
    """

    return "*" + value + "*"

def _interleave_digits(first_digit, second_digit):
    """
    Interleaves both 2 of 5 encoded digits by creating
    a composite string that represents the interleaved
    version of them.

    This process is specific for the general version of
    the 2 of 5 true type font encoding.

    :type first_digit: String
    :param first_digit: The first digit encoded in the
    2 of 5 normal encoding.
    :type second_digit: String
    :param second_digit: The second digit encoded in the
    2 of 5 normal encoding.
    :rtype: String
    :return: The interleaved representation of the concatenation
    of both digits in the normal 2 of 5 barcode format.
    """

    # creates the list that will hold the
    # various interleaved letters
    interleaved_leetters = []

    # iterates over the default range
    # of a digit encoding in 2 of 5
    for index in range(5):
        # retrieves the first and the second
        # letters from the first and second digits
        first_letter = first_digit[index]
        second_letter = second_digit[index]

        # converts the second letter to lowercase ands
        # then creates the interleaved letters sequence
        # by appending the first letter to the lowercase
        # version of the second letter and then appends
        # it to the interleaved letter list
        second_letter_lower = second_letter.lower()
        interleaved_letters = first_letter + second_letter_lower
        interleaved_leetters.append(interleaved_letters)

    # joins the set of interleaved letters to obtain the
    # "final" interleaved digits string, then returns it
    interleaved_digits_string = "".join(interleaved_leetters)
    return interleaved_digits_string

def _calculate_check_digit(character_values):
    """
    Computes the check digit based on a modulus 103 checksum,
    the algorithm is quite simple, the idea is to weight the
    value of each position over its own index position.

    :type character_values: List
    :param character_values: The list of character values to
    calculate the check digit (checksum).
    :rtype: int
    :return: The resulting check digit for the provided set
    of character values.
    """

    # starts the checksum value with the first
    # value and then retrieves the string
    # containing the remaining values
    checksum = character_values[0]
    remaining_values = character_values[1:]
    remaining_values_length = len(remaining_values)

    # iterates over the range of the remaining
    # value length to calculate the checksum
    for index in range(remaining_values_length):
        # retrieves the current value and multiplies
        # it over it's own index value plus one, that
        # will be its weighted value (value to be added
        # to the checksum integer)
        value = remaining_values[index]
        weighted_value = value * (index + 1)
        checksum += weighted_value

    # runs the modulus operation on the checksum
    # and returns it as its check digit
    check_digit = checksum % 103
    return check_digit

def _encode_code_set_a(string_value):
    """
    Encodes the provided string value into a list of code 128
    values using the code set a.

    :type string_value: String
    :param string_value: The string value to be converted into the
    list of code 128 values.
    :rtype: List
    :return: The list containing a set of code 128 numeric
    values representing the requested string in code set a.
    """

    # retrieves the start code for the current
    # encoding and starts the character values
    # list with the start code
    start_code = START_CODES_CODE_128["A"]
    character_values = [start_code]

    # iterates over all the characters contained
    # in the string value to encode them
    for character in string_value:
        # retrieves the ordinal value of the character
        # and checks if it's a valid one
        character_ascii_value = ord(character)
        if character_ascii_value > 95: raise RuntimeError("Code set does not support character '%s' " % character)

        # "calculates" the appropriate code 128 code set a
        # for the value and appends it to the character values
        character_code_128_value = character_ascii_value > 32 and character_ascii_value - 32 or character_ascii_value + 64
        character_values.append(character_code_128_value)

    # returns the list containing the code set
    # a encoded values
    return character_values

def _encode_code_set_b(string_value):
    """
    Encodes the provided string value into a list of code 128
    values using the code set b.

    :type string_value: String
    :param string_value: The string value to be converted into the
    list of code 128 values.
    :rtype: List
    :return: The list containing a set of code 128 numeric
    values representing the requested string in code set b.
    """

    # retrieves the start code for the current
    # encoding and starts the character values
    # list with the start code
    start_code = START_CODES_CODE_128["B"]
    character_values = [start_code]

    # iterates over all the characters contained
    # in the string value to encode them
    for character in string_value:
        # retrieves the ordinal value of the character
        # and checks if it's a valid one
        character_ascii_value = ord(character)
        if character_ascii_value < 32: raise RuntimeError("Code set does not support character '%s' " % character)

        # "calculates" the appropriate code 128 code set b
        # for the value and appends it to the character values
        character_code_128_value = character_ascii_value - 32
        character_values.append(character_code_128_value)

    # returns the list containing the code set
    # b encoded values
    return character_values

def _encode_code_set_c(string_value):
    """
    Encodes the provided string value into a list of code 128
    values using the code set c.

    :type string_value: String
    :param string_value: The string value to be converted into the
    list of code 128 values.
    :rtype: List
    :return: The list containing a set of code 128 numeric
    values representing the requested string in code set c.
    """

    # retrieves the start code for the current
    # encoding and starts the character values
    # list with the start code
    start_code = START_CODES_CODE_128["C"]
    character_values = [start_code]

    # resets the index value
    index = 0

    # iterates over the range of string value
    # to access all of its characters
    while index < len(string_value) - 1:
        # retrieves the current character slice and
        # parses it as an integer to append it to
        # the character values list
        characters_slice = string_value[index:index + 2]
        character_value = int(characters_slice)
        character_values.append(character_value)
        index += 2

    # returns the list containing the code set
    # c encoded values
    return character_values

def _get_character_string(character_values):
    """
    Converts the provided list of code 128 characters
    in an integer format into the appropriate unicode
    representation of them in the code 128 true type
    font format.

    :type character_values: List
    :param character_values: The list of code 128 integer
    values to be converted into the unicode string.
    :rtype: String
    :return: The converted unicode string, ready to be
    used in the true type font.
    """

    # creates the buffer to hold the various partial
    # encoded value that will constitute the "final"
    # character string
    character_buffer = string_buffer_util.StringBuffer()

    # iterates over all the characters in the list of
    # code 128 character values
    for character_value in character_values:
        # converts the value offset according to the position
        # in the conversion table
        if character_value < 95: ordinal_value = character_value + 32
        else: ordinal_value = character_value + 100

        # converts the ordinal value into an
        # unicode encoded value and adds it
        # to the character buffer
        character = legacy.unichr(ordinal_value)
        character_buffer.write(character)

    # retrieves the character string as the value from the
    # character buffer and then returns the value
    character_string = character_buffer.get_value()
    return character_string
