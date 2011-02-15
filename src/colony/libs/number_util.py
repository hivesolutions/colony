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

__author__ = "João Magalhães <joamag@hive.pt>"
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

import math

def get_number_length(number):
    """
    Retrieves the length (in digits) of the
    given number.

    @type number: int
    @param number: The number to retrieve the length
    in number of digits.
    @rtype: int
    @return: The length of the given number in number
    of digits.
    """

    return int(math.ceil(math.log(number, 10)))

def get_digit(number, index):
    """
    Retrieves the digit in the given index.
    The index values start with the least
    significant value.

    @type number: int
    @param number: The base number to retrieve
    the digit.
    @type index: int
    @param index: The index to retrieve the digit.
    @rtype: int
    @return: The digit in the given index.
    """

    return number / (10 ** index) % 10
