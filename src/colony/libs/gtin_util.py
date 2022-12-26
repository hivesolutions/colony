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

def calculate_control_value(number):
    """
    Calculates the control value for the given
    number.

    :type number: int
    :param number: The number to calculate the control value.
    :rtype: int
    :return: The control value for the given
    number.
    """

    # calculates the number of digits in the number
    number_digits = number_util.get_number_length(number)

    # starts the accumulator
    accumulator = 0

    # iterates over the range of the number of digits
    for index in range(number_digits):
        # in case it's even, sets the multiplier as one
        # otherwise it must be odd and the multiplier
        # should be set as three
        if index % 2: multiplier = 1
        else: multiplier = 3

        # retrieves the current digit
        current_digit = number_util.get_digit(number, index)

        # increments the accumulator with the current digit
        # multiplied with the current multiplier
        accumulator += current_digit * multiplier

    # calculates the partial value from
    # the accumulator value
    partial_value = accumulator % 10

    # calculates the control value based
    # on the partial value
    control_value = 10 - partial_value

    # returns the control value
    return control_value
