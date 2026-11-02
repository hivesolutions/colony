#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import math

SIZE_UNITS_LIST = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
""" The size units list """

SIZE_UNITS_LIST_S = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")
""" The simplified size units list """

SIZE_UNIT_COEFFICIENT = 1024
""" The size unit coefficient """

DEFAULT_MINIMUM = 1024
""" The default minimum value """

DEFAULT_PLACES = 3
""" The default number of places (digits) """


def size_round_unit(
    size_value,
    minimum=DEFAULT_MINIMUM,
    space=False,
    depth=0,
    places=DEFAULT_PLACES,
    reduce=True,
    justify=False,
    simplified=False,
):
    """
    Rounds the size unit, returning a string representation
    of the value with a good rounding precision.
    This method should be used to round data sizing units.

    Note that using the places parameter it's possible to control
    the number of digits (including decimal places) of the
    number that is going to be "generated".

    :type size_value: int/float
    :param size_value: The current size value (in bytes).
    :type minimum: int
    :param minimum: The minimum value to be used.
    :type space: bool
    :param space: If a space character must be used dividing
    the value from the unit symbol.
    :type depth: int
    :param depth: The current iteration depth value.
    :type places: int
    :param places: The target number of digits to be used for
    describing the value to be used for output, this is going
    to be used to calculate the proper number of decimal places.
    :type reduce: bool
    :param reduce: If the final string value should be reduced
    meaning that right decimal zeros should be removed as they
    represent an extra unused value.
    :type justify: bool
    :param justify: If the size string value should be (right)
    justified important for properly aligned values in a table.
    :type simplified: bool
    :param simplified: If the simplified version of the units
    should be used instead of the longer one.
    :rtype: String
    :return: The string representation of the data size
    value in a simplified manner (unit).
    """

    # in case the current size value is acceptable (less than
    # the minimum) or there's no larger unit to represent it, this
    # is the final iteration and the final string representation
    # is going to be created
    last = depth + 1 == len(SIZE_UNITS_LIST)
    if size_value < minimum or last:
        # calculates the maximum size of the string that is going
        # to represent the base size value as the number of places
        # plus one (representing the decimal separator character)
        size_s = places + 1

        # calculates the target number of decimal places taking
        # into account the size (in digits) of the current size
        # value, this may never be a negative number
        log_value = size_value and math.log10(size_value)
        digits = int(log_value) + 1
        decimal_places = places - digits
        decimal_places = decimal_places if decimal_places > 0 else 0

        # rounds the size value and in case the rounding raises it
        # to the minimum (eg: 1023.9KB to 1024KB) represents it in
        # the next unit instead (eg: 1MB), as a larger value would
        rounded_value = round(size_value, decimal_places)
        if rounded_value >= minimum and not last:
            return size_round_unit(
                float(size_value) / SIZE_UNIT_COEFFICIENT,
                minimum=minimum,
                space=space,
                depth=depth + 1,
                places=places,
                reduce=reduce,
                justify=justify,
                simplified=simplified,
            )

        # creates the proper format string that is going to
        # be used in the creation of the proper float value
        # according to the calculated number of places, then
        # converts the rounded size value into a string
        format = "%%.%df" % decimal_places
        size_value_s = format % rounded_value

        # forces the reduce flag when the depth is zero, meaning
        # that an integer value will never be decimal, this is
        # required to avoid strange results for depth zero
        reduce = reduce or depth == 0

        # in case the dot value is not present in the size value
        # string adds it to the end otherwise an issue may occur
        # while removing extra padding characters for reduce
        if reduce and not "." in size_value_s:
            size_value_s += "."

        # strips the value from zero appended to the right and
        # then strips the value also from a possible decimal
        # point value that may be included in it, this is only
        # performed in case the reduce flag is enabled
        if reduce:
            size_value_s = size_value_s.rstrip("0")
        if reduce:
            size_value_s = size_value_s.rstrip(".")

        # in case the justify flag is set runs the justification
        # process on the size value taking into account the maximum
        # size of the associated size string
        if justify:
            size_value_s = size_value_s.rjust(size_s)

        # retrieves the size unit (string mode) for the current
        # depth according to the provided map
        if simplified:
            size_unit = SIZE_UNITS_LIST_S[depth]
        else:
            size_unit = SIZE_UNITS_LIST[depth]

        # retrieves the appropriate separator based
        # on the value of the space flag
        separator = space and " " or ""

        # creates the size value string appending the rounded
        # size value string and the size unit and returns it
        # to the caller method as the size value string
        size_value_string = size_value_s + separator + size_unit
        return size_value_string

    # otherwise the value is not acceptable and a new iteration
    # must be ran with one less depth of size value
    else:
        # re-calculates the new size value, increments the depth
        # and runs the size round unit again with the new values
        new_size_value = float(size_value) / SIZE_UNIT_COEFFICIENT
        new_depth = depth + 1
        return size_round_unit(
            new_size_value,
            minimum=minimum,
            space=space,
            depth=new_depth,
            places=places,
            reduce=reduce,
            justify=justify,
            simplified=simplified,
        )
