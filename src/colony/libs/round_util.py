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

__date__ = "$LastChangedDate: 2011-01-15 17:29:58 +0000 (sÃ¡b, 15 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2022 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import sys
import math

FLOAT_PRECISION = 14
""" The amount of precision (in decimal places) that
is going to be used in the calculus of the delta """

DELTA = 1 / math.pow(10, FLOAT_PRECISION)
""" The delta value that is going to be applied to
the round operation representing the old strategy of
rounding, this is required so that a proper half way
up strategy is applied in the rounding """

QUANTIFIERS = {}
""" The map of quantifier strings indexed by
the number of decimal places for their round """

_round = round

def roundi(value, places = 0, precise = False):
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

    :type value: float
    :param value: The floating point value to be rounded
    :type places: int
    :param places: The number of decimal places to be used
    in the rounding operation.
    :type precise: bool
    :param precise: If the precise mode should be used where
    the delta value is calculated taking into account the
    number of places of the provided float, otherwise the
    "safe" delta is used, which should be good for most of
    the float number to be used.
    :rtype: float
    :return: The resulting rounded value according to the
    round half up strategy.
    :see: http://docs.python.org/2/tutorial/floatingpoint.html
    """

    delta = _delta(value) if precise else DELTA
    return _round_t(value + delta, places)

def rounds(value, places = 0):
    """
    Considered to be the "safest" way of rounding a number either
    a "native" float number or a decimal, this operation should
    always be used whenever the rounding result should be accurate.

    For the decimal data type usage this is considered to be the
    only way of ensuring proper and deterministic rounding.

    Note that this is an expensive operation and proper care should
    be taken to avoid extra processor usage.

    :type value: float
    :param value: The floating point value to be rounded
    :type places: int
    :param places: The number of decimal places to be used
    in the rounding operation.
    :rtype: float
    :return: The resulting rounded value according to the
    current (most precise) way of rounding.
    """

    return roundi(value, places, precise = True)

def roundt(value, places = 0):
    """
    Simple rounding utility function that performs the currently
    selected rounding operation on the provided value and then
    re-casts the resulting value back to the original data type.

    This function is relevant/useful for situation where the base
    value inherits indirectly from the float class.

    :type value: float
    :param value: The value that is meant to be rounded and then
    "casted" back to the original data type.
    :param places: The number of decimal places to be used
    in the rounding operation.
    :rtype: float
    :return: The resulting rounded value according to the
    default rounding strategy defined.
    """

    value_t = type(value)
    result = round(value, places)
    return result if type(result) == value_t else value_t(result)

def round_apply(force = False):
    """
    Applies the "old" rounding strategy to the current
    interpreted in a global fashion (override).

    This method only applies the rounding method for
    interpreters that uses the new rounding method
    avoiding the apply of the calculus for old rounding
    method interpreters (provides performance).

    :type force: bool
    :param force: If the apply operation should be performed
    for environments where it's not required (old rounding).
    """

    # verifies that the current executing version of
    # the interpreter is using the new rounding methods
    # in case it's not no apply occurs (not required)
    new_round = round_is_new()
    if not new_round and not force: return

    # updates the built-in round function with the new
    # round function so that the rounds are coherent, note
    # that the builtins reference may be either map based
    # or module based, logic must take care of both cases
    builtins = globals()["__builtins__"]
    if type(builtins) == dict: builtins["round"] = roundi
    else: builtins.round = roundi

def round_unapply(force = False):
    """
    Reverts the apply operation of the "old" rounding
    strategy back to the original built-in rounding.

    This method should be used carefully as it may produce
    some unexpected results.

    :type force: bool
    :param force: If the unapply operation should be performed
    for environments where it's not required (old rounding).
    """

    # verifies that the current executing version of
    # the interpreter is using the new rounding methods
    # in case it's not no unapply occurs (not required)
    new_round = round_is_new()
    if not new_round and not force: return

    # updates the built-in round function with the old
    # round function so that the rounds are reverted, note
    # that the builtins reference may be either map based
    # or module based, logic must take care of both cases
    builtins = globals()["__builtins__"]
    if type(builtins) == dict: builtins["round"] = _round_t
    else: builtins.round = _round_t

def round_is_new():
    """
    Verifies that the current execution version of the interpreter
    is running the new rounding strategy, meaning that the round
    operations will be performed using the half way undefined strategy.

    This method infers the strategy that is currently in use for
    rounding based on the version of the interpreted.

    :rtype: bool
    :return: If the current (python) interpreter is running the
    new rounding strategy (half way undefined).
    :see: http://docs.python.org/2/tutorial/floatingpoint.html
    """

    # unpacks the system's version information tuple
    # into its major and minor values to be used for
    # the checking of the new round method
    major = sys.version_info[0]
    minor = sys.version_info[1]

    # verifies that the current executing version of
    # the interpreter is using the new rounding methods
    # in case it's not no unapply occurs (not required)
    new_round = major > 3 or (major == 3 and minor >= 1) or\
        (major == 2 and minor >= 7)
    return new_round

def _round_t(value, places = 0):
    """
    Internal function similar to the the type one but uses
    the internal (built-in) version of the rounder to perform
    the rounding operation.

    This function should only be used for old python 2 based
    versions and not for the new python 3+ versions where the
    proper overriding of the __round__ method is preferred.

    :type value: float
    :param value: The value that is meant to be rounded and then
    "casted" back to the original data type.
    :param places: The number of decimal places to be used
    in the rounding operation.
    :rtype: float
    :return: The resulting rounded value according to the
    default rounding strategy defined.
    """

    value_t = type(value)
    result = _round(value, places)
    return result if type(result) == value_t else value_t(result)

def _delta(value):
    """
    Calculates the proper minimum delta value that may be
    applied to the provided value so that it's still able
    to represent the "next" value.

    This is an expensive operation operation and should be
    used carefully to avoid extra computation.

    :type value: float
    :param value: The value for which the proper (minimum)
    delta value is going to be calculated.
    :rtype: float
    :param float: The (minimum) delta value calculated for
    the provided float value, this value may be used for
    proper "old" rounding strategy.
    """

    integer = abs(int(value // 1))
    count = 1 if integer == 0 else int(math.log10(integer)) + 1
    places = FLOAT_PRECISION - count
    if places < 1: places = 1
    delta = 1 / math.pow(10, places)
    return delta

# verifies if the current interpreter version is python 3+ and
# if that's the case used the builtin round function instead to
# allow data type casting through the __round__ magic method
if sys.version_info[0] >= 3: _round_t = _round

# updates the round reference in the builtin dictionary so that
# the proper type based casting is used instead of the builtin
# functions (allows proper data type casting for python 2)
builtins = globals()["__builtins__"]
if type(builtins) == dict: builtins["round"] = _round_t
else: builtins.round = _round_t
