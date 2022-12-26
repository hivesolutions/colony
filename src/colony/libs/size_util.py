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

SIZE_UNITS_LIST = (
    "B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"
)
""" The size units list """

SIZE_UNIT_COEFFICIENT = 1024
""" The size unit coefficient """

DEFAULT_MINIMUM = 1024
""" The default minimum value """

def size_round_unit(size_value, minimum = DEFAULT_MINIMUM, space = False, depth = 0):
    """
    Rounds the size unit, returning a string representation
    of the value with a good rounding precision.
    This method should be used to round data sizing units.

    :type size_value: int
    :param size_value: The current size value (in bytes).
    :type minimum: int
    :param minimum: The minimum value to be used.
    :type space: bool
    :param space: If a space character must be used dividing
    the value from the unit symbol.
    :type depth: int
    :param depth: The current iteration depth value.
    :rtype: String
    :return: The string representation of the data size
    value in a simplified manner (unit).
    """

    # in case the current size value is
    # acceptable (less than the minimum)
    if size_value < minimum:
        # rounds the size value
        rounded_size_value = int(size_value)

        # converts the rounded size value to string
        rounded_size_value_string = str(rounded_size_value)

        # retrieves the size unit (string mode)
        size_unit = SIZE_UNITS_LIST[depth]

        # retrieves the appropriate separator based
        # on the value of the space flag
        separator = space and " " or ""

        # creates the size value string appending the rounded
        # size value string and the size unit
        size_value_string = rounded_size_value_string + separator + size_unit

        # returns the size value string
        return size_value_string
    # otherwise the value is not acceptable
    # and a new iteration must be ran
    else:
        # re-calculates the new size value
        new_size_value = size_value / SIZE_UNIT_COEFFICIENT

        # increments the depth
        new_depth = depth + 1

        # runs the size round unit again with the new values
        return size_round_unit(new_size_value, minimum, space, new_depth)
