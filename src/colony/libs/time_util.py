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

import datetime

from . import list_util

DAY_VALUE = "day"
""" The day value """

HOUR_VALUE = "hour"
""" The hour value """

MINUTE_VALUE = "minute"
""" The minute value """

SECOND_VALUE = "second"
""" The second value """

SIMPLE_VALUE = "simple"
""" The simple value """

BASIC_VALUE = "basic"
""" The basic value """

EXTENDED_VALUE = "extended"
""" The extended value """

EXTENDED_SIMPLE_VALUE = "extended_simple"
""" The extended simple value """

MINIMIZE_MULTIPLE = "minimize_multiple"
""" The minimization with multiple value support """

MINIMIZE_UNIQUE = "minimize_unique"
""" The minimization with unique value support """

DEFAULT_INCLUDES = (
    DAY_VALUE,
    HOUR_VALUE,
    MINUTE_VALUE,
    SECOND_VALUE
)
""" The default includes list (tuple) """

DEFAULT_FORMAT = "%(D)d days, %(H)d hours, %(M)d minutes"
""" The default format """

FORMATS = {
    SIMPLE_VALUE : {
        DAY_VALUE : "%(D)d",
        HOUR_VALUE : "%(H)d",
        MINUTE_VALUE : "%(M)d",
        SECOND_VALUE : "%(S)d"
    },
    BASIC_VALUE : {
        DAY_VALUE : "%(D)dd",
        HOUR_VALUE : "%(H)dh",
        MINUTE_VALUE : "%(M)dm",
        SECOND_VALUE : "%(S)ds"
    },
    EXTENDED_VALUE : {
        DAY_VALUE : "%(D)d days",
        HOUR_VALUE : "%(H)d hours",
        MINUTE_VALUE : "%(M)d minutes",
        SECOND_VALUE : "%(S)d seconds"
    },
    EXTENDED_SIMPLE_VALUE : {
        DAY_VALUE : "%(D)d days",
        HOUR_VALUE : "%(H)d hours",
        MINUTE_VALUE : "%(M)d minutes",
        SECOND_VALUE : "%(S)d seconds"
    }
}
""" The formats map """

SEPARATORS = {
    SIMPLE_VALUE : ":",
    BASIC_VALUE : ", ",
    EXTENDED_VALUE : ", ",
    EXTENDED_SIMPLE_VALUE : " "
}
""" The separators map """

def format_seconds_smart(
    seconds,
    mode = SIMPLE_VALUE,
    includes = DEFAULT_INCLUDES,
    minimize = MINIMIZE_MULTIPLE
):
    """
    Formats the given seconds according to the given
    mode, includes and minimization support.
    The smart mode supports the creation of format strings
    dynamically from the pre-built modes.

    :type seconds: int
    :param seconds: The number of seconds to be formatted.
    :type mode: String
    :param mode: The formatting mode to be used.
    :type includes: List
    :param includes: The list of types to be included in the
    formatted string.
    :type minimize: String
    :param minimize: If the includes list should be minimized
    according to the number of seconds "available". The minimize
    string controls the way of minimization.
    :rtype: String
    :return: The string containing the formated seconds.
    """

    # in case the minimize flag is active
    if minimize:
        # re-processes the includes to according to the
        # amount of seconds available to be processed, the
        # minimize mode controls the way the include are going
        # to be minimized
        processed_includes = _process_includes(seconds, includes, minimize)
    # otherwise
    else:
        # sets the processed includes as the original includes
        processed_includes = includes

    # in case the processed includes
    # is invalid
    if not processed_includes:
        # sets the processed includes with the last
        # element of the original includes, in order to
        # avoid empty strings
        processed_includes = (
            includes[-1],
        )

    # creates the is first flag
    is_first = True

    # creates the format string lisr
    format_string_list = []

    # retrieves the formats for the mode
    formats = FORMATS[mode]

    # retrieves the separator for the mode
    separator = SEPARATORS[mode]

    for include in processed_includes:
        # in case it's the first
        # iteration
        if is_first:
            # unsets the is first flag
            is_first = False
        else:
            # adds the separator to the format
            # string list
            format_string_list.append(separator)

        # retrieves the format for the include
        format_include = formats[include]

        # adds the format include to the
        # format string list
        format_string_list.append(format_include)

    # creates the format string, joining the
    # format string list
    format_string = "".join(format_string_list)

    # formats the seconds according to the created
    # format string
    formatted_seconds = format_seconds(seconds, format_string)

    # returns the formatted seconds
    return formatted_seconds

def format_seconds(seconds, format_string = DEFAULT_FORMAT):
    """
    Formats the given seconds according to the given
    format string.

    :type seconds: int
    :param seconds: The number of seconds to be formatted.
    :type format_string: String
    :param format_string: The format string to be used.
    :rtype: String
    :return: The string containing the formated seconds.
    """

    # calculates the number of days from the seconds
    days = int(seconds / 86400.0)

    # calculates the days modulus from the seconds
    days_modulus = (seconds % 86400.0)

    # calculates the number of hours from the days modulus
    hours = int(days_modulus / 3600.0)

    # calculates the hours modules from the days modulus
    hours_modulus = days_modulus % 3600.0

    # calculates the number of minutes from the hours modulus
    minutes = int(hours_modulus / 60.0)

    # calculates the minutes modules from the hours modulus
    minutes_modulus = hours_modulus % 60.0

    # calculates the number of seconds from the minutes modulus
    seconds = int(minutes_modulus)

    # creates the attributes map with the various values
    attributes = {"D" : days, "H" : hours, "M" : minutes, "S" : seconds}

    # formats the string with the attributes map
    formatted_string = format_string % attributes

    # returns the formatted string
    return formatted_string

def timestamp_datetime(timestamp_string):
    """
    Converts the provided timestamp string to a datetime object.

    :type timestamp_string String.
    :param timestamp_string The timestamp value as string.
    """

    # retrieves the type of the timestamp string
    timestamp_string_type = type(timestamp_string)

    # in case the timestamp string is already
    # a date time object
    if timestamp_string_type == datetime.datetime:
        # returns the timestamp string itself
        # (no conversion required)
        return timestamp_string

    # converts the timestamp string to float
    timestamp_float = float(timestamp_string)

    # converts to a datetime object
    datetime_value = datetime.datetime.utcfromtimestamp(timestamp_float)

    # returns the converted datetime
    return datetime_value

def _process_includes(seconds, includes, minimize_mode):
    """
    Processes the includes list, retrieving the minimized
    includes list with only the minimum required includes.

    :type seconds: int
    :param seconds: The number of seconds to be processed.
    :type includes: List
    :param includes: The list of includes to be processed.
    :rtype: List
    :return: The processed includes
    :type minimize_mode: String
    :param minimize_mode: The minimize mode to be used.
    """

    # in case there are only seconds to be
    # represented
    if seconds < 60:
        # sets the valid includes as the seconds
        valid_includes = minimize_mode == MINIMIZE_MULTIPLE and (
            SECOND_VALUE,
        ) or (
            SECOND_VALUE,
        )
    # in case there are only second and minutes
    # to be represented
    elif seconds < 3600:
        # sets the valid includes as the minutes
        # and the seconds
        valid_includes = minimize_mode == MINIMIZE_MULTIPLE and (
            MINUTE_VALUE,
            SECOND_VALUE
        ) or (
            MINUTE_VALUE,
        )
    # in case there are seconds, minutes and
    # hours to be represented
    elif seconds < 86400:
        # sets the valid includes as the hours, the minutes
        # and the seconds
        valid_includes = minimize_mode == MINIMIZE_MULTIPLE and (
            HOUR_VALUE,
            MINUTE_VALUE,
            SECOND_VALUE
        ) or (
            HOUR_VALUE,
        )
    # in case everything should be represented
    else:
        # sets the valid includes as the days, the hours, the minutes
        # and the seconds
        valid_includes = minimize_mode == MINIMIZE_MULTIPLE and (
            DAY_VALUE,
            HOUR_VALUE,
            MINUTE_VALUE,
            SECOND_VALUE
        ) or (
            DAY_VALUE,
        )

    # intersects the (original) list of includes and the valid includes
    # to retrieve the processed includes
    processed_includes = list_util.list_intersect(includes, valid_includes)

    # returns the processed includes
    return processed_includes
