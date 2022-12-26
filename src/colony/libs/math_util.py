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

from colony.base import legacy

def ceil_integer(value):
    """
    Retrieves the ceil of a value and then converts it
    into an integer.
    The conversion to integer ensures that the ceil
    is compatible with certain operations.

    :type value: int
    :param value: The value to apply the ceil.
    :rtype: int
    :return: The ceil of the given value "casted" as an
    integer.
    """

    # retrieves the ceil value
    ceil_value = math.ceil(value)

    # casts the ceil value into integer
    ceil_value_integer = int(ceil_value)

    # returns the ceil value integer
    return ceil_value_integer

def greatest_common_divisor(p_value, q_value):
    """
    Calculates the greatest common divisor of p value and q value.
    This method uses the classic euclidean algorithm.

    :type p_value: int
    :param p_value: The first prime number to obtain
    the greatest common divisor.
    :type q_value: int
    :param q_value: The second prime number to obtain
    the greatest common divisor.
    :rtype: int
    :return: The greatest common divisor between both values.
    """

    # in case the p value is smaller than
    # the q value
    if p_value < q_value:
        # inverts the greatest common divisor
        # calculation strategy
        return greatest_common_divisor(q_value, p_value)

    # in case the q value is zero
    if q_value == 0:
        # returns the p value
        # because there is no division by zero
        return p_value

    # calculates the next q value
    _q_value = abs(p_value % q_value)

    # return the recalculation of the greatest common
    # divisor
    return greatest_common_divisor(q_value, _q_value)

def fast_exponentiation(base, exponent, modulus):
    """
    Applies a fast exponentiation algorithm to the
    given value retrieving the exponentiation result.
    The calculus may be defined by: base ^ exponent % modulus.

    :type base: int
    :param base: The base value for the exponentiation.
    :type exponent: int
    :param exponent: The exponent value for the exponentiation.
    :type modulus: int
    :param modulus: The modulus value for the exponentiation.
    :rtype: int
    :return: The result of the exponentiation.
    """

    # calculates the (initial) result
    result = base % modulus

    # creates the remainders list
    remainders = []

    # iterates while the exponent is not one
    while not exponent == 1:
        # adds the exponent first bit to
        # the remainders
        remainders.append(exponent & 1)

        # shifts the exponent one bit to the right
        exponent >>= 1

    # iterates while there are
    # remainders left
    while remainders:
        # pops the remainder value
        remainder = remainders.pop()

        # calculates the result value
        result = ((base ** remainder) * result ** 2) % modulus

    # returns the result
    return result

def item_set_total(item_set):
    """
    Calculates the total value from the
    given item set (map).
    The total is calculated summing the value
    parts of the map.

    :type item_set: Dictionary
    :param item_set: The item set (map) to calculate
    the total from its values.
    :rtype: float
    :return: The total value from the item set.
    """

    # retrieves the item set values
    item_set_values = legacy.values(item_set)

    # calculates the total value
    total_value = sum(item_set_values)

    # returns the total value
    return total_value

def item_set_percentage(item_name, item_set):
    """
    Calculates the relative percentage value of
    the value of the item with the given name,
    in relation to the total value of the item set.

    :type item_name: String
    :param item_name: The name of the item to retrieve
    the relative percentage value.
    :type item_set: Dictionary
    :param item_set: The item set (map) to be used
    as base (total) for relative calculation.
    :rtype: float
    :return: The relative percentage value of the item
    in relation to the total value of the item set.
    """

    # retrieves the item value from the give
    # item name
    item_value = item_set.get(item_name, None)

    # in case the item value is not defined
    # or is zero, avoiding division by zero
    if not item_value: return 0

    # calculates the total value from the
    # item set
    total_value = item_set_total(item_set)

    # calculates the percentage value from the
    # total value (multiplication by on hundred)
    percentage_value = float(item_value) / total_value * 100

    # returns the percentage value
    return percentage_value
