#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-01-15 17:29:58 +0000 (sÃ¡b, 15 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys
import decimal

QUANTIFIERS = {}
""" The map of quantifier strings indexed by
the number of decimal places for their round """

def roundi(value, places):
    """
    Rounds the provided float value to the provided
    number of decimal places returning a floating
    point number representing the result.

    The provided value is rounded using the round half up
    strategy where (to nearest with ties going away from zero).

    The rounding procedure is done using the "old" rounding
    method, that contains a floating point based error.
    This is the rounding method expected by the current
    colony infra-structure and as such it should be applied
    at the beginning of a new plugin system instance.

    This rounding method incurs in major performance issues
    and should only be used for interpreters that use the
    "new" rounding method.

    @type value: float
    @param value: The floating point value to be rounded
    @type places: int
    @param places: The number of decimal places to be used
    in the rounding operation.
    @see: http://docs.python.org/2/tutorial/floatingpoint.html
    """

    # converts the value into an integer value (to obtain
    # the integer part from it) and then retrieves the size
    # of it (in number) by converting it into a string
    value_i = int(value)
    integer_size = len(str(value_i))

    # deduces the size of the decimal part of it by decrementing
    # the float value size to the integer size and creates the
    # appropriate formatter to retrieve it the float value with
    # the appropriate decimal places
    decimal_size = 17 - integer_size
    value_format = "%%.%df" % decimal_size
    value_s = value_format % value

    # retrieves the last digit of the float part and verifies if
    # it's greater that fix for such case a rounding propagation
    # round must be applies recursively
    last = int(value_s[-1])
    if last >= 5:
        # retrieves the references for both the
        # integer and the floating part of the number
        # and then converts the the float part into
        # a list to be manipulated
        integer_part = value_s[:integer_size]
        float_part = value_s[integer_size + 1:]
        float_part = list(float_part)

        # sets the last digit of the float part as zero
        # a round will be used and propagated and then
        # starts the index value to the last character
        # minus one and start the loop
        float_part[-1] = "0"
        index = decimal_size - 2
        while True:
            # in case the minus one index has been reached
            # breaks the loop as no more rounding should be
            # applied to the number
            if index == -1: break

            # converts the current digit into an integer and
            # in case the number is nine continues the round
            # operation otherwise increments the value and
            # stops the rounding propagation
            current = int(float_part[index])
            if current == 9:
                float_part[index] = "0"
                index -= 1
                continue
            else:
                float_part[index] = str(current + 1)
                break

        # joins the float part list to create the final
        # float part of the number and joins the integer
        # a float parts again to create the string value
        float_part = "".join(float_part)
        value_s = "%s.%s" % (integer_part, float_part)

    # sets the created string values as the base
    # value for the "newly" created decimal (avoids
    # external rounds)
    value_d = decimal.Decimal(value_s)

    # tries to retrieve the quantifier value from
    # the quantifier map (fast construction) in case
    # the value is not found creates a new decimal
    # with such number of places and sets it in the
    # quantifiers map (additional accesses will match)
    quantifier = QUANTIFIERS.get(places, None)
    if quantifier == None:
        quantifier_s = "." + ("0" * places) if places else "0"
        quantifier = decimal.Decimal(quantifier_s)
        QUANTIFIERS[places] = quantifier

    # rounds the decimal value using the provided quantifier
    # and then converts the resulted rounded value into the
    # associated float value, returning the value to the
    # caller method (old python version compatible)
    value_d = value_d.quantize(quantifier, rounding = decimal.ROUND_HALF_UP)
    value_f = float(value_d)
    return value_f

def apply():
    """
    Applies the "old" rounding strategy to the current
    interpreted in a global fashion (override).

    This method only applies the rounding method for
    interpreters that uses the new rounding method
    avoiding the apply of the calculus for old rounding
    method interpreters (provides performance).
    """

    # unpacks the system's version information tuple
    # into its major and minor values to be used for
    # the checking of the new round method
    major = sys.version_info[0]
    minor = sys.version_info[1]

    # verifies that the current executing version of
    # the interpreter is using the new rounding methods
    # in case it's not no apply occurs (not required)
    new_round = major > 3 or (major == 3 and minor >= 1) or\
        (major == 2 and minor >= 7)
    if not new_round: return

    # updates the built-in round function with the new
    # round function so that the rounds are coherent
    __builtins__["round"] = roundi
