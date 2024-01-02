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

import sys

VERSION = "%(version)s"
""" The version value, that identifies the current
running version, this value should have three components """

RELEASE = "%(release)s"
""" The release value identifying the continuous integration
based value, this value should be considered internal """

BUILD = "%(build)s"
""" The build value, considered to be internal """

RELEASE_DATE = "%(date)s"
""" The release date value conformant with the typical
data and string values """

RELEASE_DATE_TIME = "%(date_time)s"
""" The release date time value that should timestamp the
current system """

ENVIRONMENT_VERSION = (
    str(sys.version_info[0])
    + "."
    + str(sys.version_info[1])
    + "."
    + str(sys.version_info[2])
    + "-"
    + str(sys.version_info[3])
)
""" The environment version, constructed using information
from the currently running python interpreter """

ENVIRONMENT = "python-" + sys.platform + " " + ENVIRONMENT_VERSION
""" The environment string that should identify in a minimal
way the currently running system/environment """

__GENERATED__ = "%(generated)s"
""" Flag based global object that controls if the
values in the current module have been already
generated by a previous call or tool """

# % END_INFORMATION % #

DEFAULT_ENCODING = "utf-8"
""" The default encoding value to be used to convert
the information values into string, this value should
be set as compatible with the information file encoding
so that no encoding related exceptions are raised """

DATE_FORMAT = "%b %d %Y"
""" The format used to convert dates to strings """

DATE_TIME_FORMAT = "%b %d %Y %H:%M:%S"
""" The format used to convert date times to strings """

INFORMATION_PATH = "../res/colony.json"
""" The relative path to the file containing the
complete "release" information about the current
colony implementation running """


def generate(information=None, encoding=DEFAULT_ENCODING):
    # sets the various environment variables as the
    # global reference to their values to avoid
    # confusing local allocation
    global VERSION
    global RELEASE
    global BUILD
    global RELEASE_DATE
    global RELEASE_DATE_TIME
    global __GENERATED__

    # checks if the values in the current module have been
    # already generated in such case there's no need to generate
    # them again (expensive operation)
    if __GENERATED__ == "1":
        return

    # sets the generated flag to indicate that the values
    # in the module have been already processed
    __GENERATED__ = "1"

    # in case no information is provided the configuration
    # file must be uses to retrieve the proper information
    # for the global values, this approach has impact in
    # the performance of the generation and also requires
    # the usage of the JSON module (may not exist)
    if information == None:
        # tries to import the JSON module in case of failure
        # a silent return must occur to avoid problems
        try:
            import os, json, datetime
        except ImportError:
            return

        # retrieves the current directory path and uses it to
        # infer the location of the information file to the
        # current colony instance, then uses that path to load
        # the associated JSON information
        directory = os.path.dirname(__file__)
        file_path = os.path.join(directory, INFORMATION_PATH)
        file_path = os.path.normpath(file_path)
        file = open(file_path, "rb")
        try:
            data = file.read()
        finally:
            file.close()
        data = data.decode(encoding)
        information = json.loads(data)

        # retrieves the current datetime and formats it
        # according to the two pre-defined formats
        current_datetime = datetime.datetime.utcnow()
        current_date_string = current_datetime.strftime(DATE_FORMAT)
        current_date_time_string = current_datetime.strftime(DATE_TIME_FORMAT)

        # sets both the date string and the date time string
        # in the symbols map for template reference
        information["date"] = current_date_string
        information["date_time"] = current_date_time_string

    # processes the various items of the information
    # module using the provided information map, this
    # map must contain all the information required
    # for the generation of these string, otherwise
    # this function will fails in exception
    VERSION = VERSION % information
    RELEASE = RELEASE % information
    BUILD = BUILD % information
    RELEASE_DATE = RELEASE_DATE % information
    RELEASE_DATE_TIME = RELEASE_DATE_TIME % information


# runs the generate task at import time to provide
# the most update values to the importer agent
generate()
