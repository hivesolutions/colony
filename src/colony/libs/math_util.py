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

import math

def ceil_integer(value):
    """
    Retrieves the ceil of a value and then converts it
    into an integer.
    The conversion to integer ensures that the ceil
    is compatible with certain operations.

    @type value: int
    @param value: The value to apply the ceil.
    @rtype: int
    @return: The ceil of the given value "casted" as an
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

    @type p_value: int
    @param p_value: The first prime number to obtain
    the greatest common divisor.
    @type q_value: int
    @param q_value: The second prime number to obtain
    the greatest common divisor.
    @rtype: int
    @return: The greatest common divisor between both values.
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

    @type base: int
    @param base: The base value for the exponentiation.
    @type exponent: int
    @param exponent: The exponent value for the exponentiation.
    @type modulus: int
    @param modulus: The modulus value for the exponentiation.
    @rtype: int
    @return: The result of the exponentiation.
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
