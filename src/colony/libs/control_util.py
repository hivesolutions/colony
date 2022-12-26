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

from . import number_util

COEFFICIENT_VALUES = (
    2, 3, 4, 5, 6, 7, 8, 9
)
""" The tuple containing the coefficient values """

def calculate_tax_number_control_value(tax_number):
    """
    Calculates the control value for the tax number.

    :type tax_number: int
    :param tax_number: The tax number to calculate the
    control value.
    :rtype: int
    :return: The calculated control value.
    """

    # calculates the number of digits in the number
    number_digits = number_util.get_number_length(tax_number)

    # in case the number of digits is invalid  must raise an
    # exception indicating the error, note that this requirement
    # in terms of size ensures that no tax number may start with
    # a number like zero (reducing the length of the valid digits)
    if not number_digits == 8:
        raise RuntimeError("Invalid tax number length '%d'" % number_digits)

    # calculates the control value for the number and then
    # returns it to the caller method
    control_value = _calculate_control_value(tax_number)
    return control_value

def calculate_id_number_control_value(id_number):
    """
    Calculates the control value for the id number.

    :type id_number: int
    :param id_number: The id number to calculate the
    control value.
    :rtype: int
    :return: The calculated control value.
    """

    # calculates the number of digits in the number
    number_digits = number_util.get_number_length(id_number)

    # in case the number of digits is invalid
    # must raise an exception indicating the error
    if number_digits < 6 or number_digits > 8:
        raise RuntimeError("Invalid id number length '%d'" % number_digits)

    # adds zeros to the right of the number (if necessary)
    id_number *= 10 ** (8 - number_digits)

    # calculates the control value for the number and then
    # returns it to the caller method
    control_value = _calculate_control_value(id_number)
    return control_value

def _calculate_control_value(number):
    """
    Calculates the control value for the given number, this
    control value is related with the calculus of a tax
    number number or id number.

    :type number: int
    :param number: The number to calculate the control value,
    the length of this number is not verifies and may assume
    any size, as that's not part of the control value calculus.
    :rtype: int
    :return: The control value for the given number.
    """

    # calculates the number of digits in the number
    number_digits = number_util.get_number_length(number)

    # starts the accumulator
    accumulator = 0

    # iterates over the range of the number of digits
    for index in range(number_digits):
        # retrieves the current digit and then the associated
        # coefficient value, incrementing then the accumulator
        # with the current digit multiplied with the current
        # coefficient (as expected by algorithm)
        current_digit = number_util.get_digit(number, index)
        current_coefficient = COEFFICIENT_VALUES[index]
        accumulator += current_digit * current_coefficient

    # calculates the partial value from
    # the accumulator value
    partial_value = accumulator % 11

    # in case the partial value is zero
    # or one sets the control value as zero
    if partial_value in (0, 1): control_value = 0

    # otherwise calculates the control value based
    # on the partial value
    else: control_value = 11 - partial_value

    # returns the control value
    return control_value
