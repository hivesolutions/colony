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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

DEFAULT_NUMBER_RETRIES = 3
""" The default number of retries to register or unregister """

DEFAULT_RETRY_SLEEP = 1
""" The default sleep time between retries """

def execute_retries(callable, number_retries = DEFAULT_NUMBER_RETRIES, retry_sleep = DEFAULT_RETRY_SLEEP):
    """
    Executes the given callable retring the call in case an exception occurs.
    The number of retries and the time between retries is configurable.
    The method returns the return value from the call or raises the last
    known exception.

    @type callable: Callable
    @param callable: The callalbe to be called using retries.
    @type number_retries: int
    @param number_retries: The number of retries to be used.
    @type retry_sleep: int´
    @param retry_sleep: The sleep time between retries.
    @rtype: Object
    @return: The return value from the callable.
    """

    # iterates over the range of the number retries (plus one)
    # the last iteration is used for exception re-raising
    for index in range(number_retries + 1):
        try:
            # calls the callable object, retrieving
            # and saving the return value
            return_value = callable()

            # breaks the loop, because there is
            # no exception raised (successful call)
            break
        except:
            # in case it's the last index position
            # the exception should be re-raised
            if index == number_retries:
                # re-raises the exception
                raise

            # sleeps a while to avoid problems
            time.sleep(retry_sleep)

    # returns the callable return value
    return return_value
