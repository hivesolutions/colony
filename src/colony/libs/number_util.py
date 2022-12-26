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

import math
import decimal

def get_number_length(number):
    """
    Retrieves the length (in digits) of the given number.
    This method does not allow any kind of padding zeros
    as they are not going to be handled.

    :type number: int
    :param number: The number to retrieve the length
    in number of digits.
    :rtype: int
    :return: The length of the given number in number
    of digits, according to logarithmic calculus.
    """

    return int(math.ceil(math.log(number, 10)))

def get_digit(number, index):
    """
    Retrieves the digit in the given index.
    The index values start with the least
    significant value.

    :type number: int
    :param number: The base number to retrieve
    the digit.
    :type index: int
    :param index: The index to retrieve the digit.
    :rtype: int
    :return: The digit in the given index.
    """

    return number // (10 ** index) % 10

def to_fixed(number, places = 2):
    """
    Converts a (possible) float number into a decimal
    representation of fixed point real.

    This function is useful for situation where operations
    on the float number rendered it impossible for a
    precise comparison.

    Use this method carefully as it may provide unrealistic
    comparisons.

    :type number: float
    :param number: The float number to be converted in to
    a fixed point decimal number.
    :type places: int
    :param places: The number of decimal places to be used
    in the conversion into fixed point.
    :rtype: Decimal
    :return: The decimal representation of the number (fixed
    point arithmetic) with the correct number of decimal places.
    """

    # creates the "initial" format string with the correct
    # (requested) number of decimal places
    format_string = "%%.%df" % places

    # uses the created format string to create a string
    # representing the number with the request decimal places
    # and the uses it as the argument to construct the correct
    # decimal representation of the number
    number_string = format_string % number
    number_fixed = decimal.Decimal(number_string)

    # returns the created decimal representation of the number
    # in a fixed point arithmetic approach
    return number_fixed
