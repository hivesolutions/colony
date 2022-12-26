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

def version_cmp(version, version_compare):
    """
    Compares the given version string against a compare string
    that may contain wildcard values.

    This way it's possible to compare it against version ranges
    defined in the form of wildcard values.

    :type version: String
    :param version: The base version string to be verified
    by the comparison.
    :type version_compare: String
    :param version_compare: The compare version string to be used
    as reference in the comparison (may contain wildcard values).
    :rtype: bool
    :return: The result of the version string comparison (includes
    wildcard comparison).
    """

    # splits both the (base) version string and the compare string
    # into the three version parts (major, medium and minor) to get
    # them into the normal tuple comparison
    major, medium, minor = version.split(".")
    major_compare, medium_compare, minor_compare = version_compare.split(".")

    # compares all the three parts of the version string so that
    # if there is a mismatch in the version number or in case there
    # is no wildcard present in the compare string the comparison fails
    if not major_compare == "x" and not major == major_compare: return False
    if not medium_compare == "x" and not medium == medium_compare: return False
    if not minor_compare == "x" and not minor == minor_compare: return False

    # returns valid version, all the version tests have passed successfully
    # the version is considered to be valid (equivalent)
    return True

def version_is_concrete(version):
    """
    Verifies if the provided version number is of type concrete
    (all the partial number are specified), or if the version
    string contains wildcard values that match an open range
    of version values.

    :param version: String
    :param version: The string containing the version to be verified
    to be of type concrete.
    :rtype: bool
    :return: The result of the version concrete testing.
    """

    # checks if the wildcard character is present in the version
    # string, if it is the version is considered to be wildcard
    # then returns the negation of that as the is concrete value
    is_wildcard = "x" in version
    return not is_wildcard
