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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

import number_util

COEFFICIENT_VALUES = (2, 3, 4, 5, 6, 7, 8, 9)
""" The tuple containing the coefficient values """

def calculate_tax_number_control_value(tax_number):
    """
    Calculates the control value for the tax number.

    @type id_number: int
    @param id_number: The tax number to calculate the
    control value.
    @rtype: int
    @return: The calculated control value.
    """

    # calculates the number of digits in the number
    number_digits = number_util.get_number_length(tax_number)

    # in case the number of digits is invalid
    if not number_digits == 8:
        # raises an exception
        raise RuntimeError("Invalid tax number length '%d'" % number_digits)

    # calculates the control value for the number
    control_value = calculate_control_value(tax_number)

    # returns the control value
    return control_value

def calculate_id_number_control_value(id_number):
    """
    Calculates the control value for the id number.

    @type id_number: int
    @param id_number: The id number to calculate the
    control value.
    @rtype: int
    @return: The calculated control value.
    """

    # calculates the number of digits in the number
    number_digits = number_util.get_number_length(id_number)

    # in case the number of digits is invalid
    if number_digits < 6 or number_digits > 8:
        # raises an exception
        raise RuntimeError("Invalid id number length '%d'" % number_digits)

    # adds zeros to the right of the number (if necessary)
    id_number *= 10 ** (8 - number_digits)

    # calculates the control value for the number
    control_value = calculate_control_value(id_number)

    # returns the control value
    return control_value

def calculate_control_value(number):
    """
    Calculates the control value for the given
    number.

    @type number: int
    @param number: The number to calculate the control value.
    @rtype: int
    @return: The control value for the given
    number.
    """

    # calculates the number of digits in the number
    number_digits = number_util.get_number_length(number)

    # starts the accumulator
    accumulator = 0

    # iterates over the range of the number of digits
    for index in range(number_digits):
        # retrieves the current digit
        current_digit = number_util.get_digit(number, index)

        # retrieves the current coefficient
        current_coefficient = COEFFICIENT_VALUES[index]

        # increments the accumulator with the current digit
        # multiplied with the current coefficient
        accumulator += current_digit * current_coefficient

    # calculates the partial value from
    # the accumulator value
    partial_value = accumulator % 11

    # in case the partial value is zero
    # or one
    if partial_value in (0, 1):
        # sets the control value as zero
        control_value = 0
    # otherwise
    else:
        # calculates the control value based
        # on the partial value
        control_value = 11 - partial_value

    # returns the control value
    return control_value
