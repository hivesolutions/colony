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

import time

from colony.base import legacy

DEFAULT_NUMBER_RETRIES = 3
""" The default number of retries to register or unregister """

DEFAULT_RETRY_SLEEP = 1
""" The default sleep time between retries """

def execute_retries(
    callable,
    number_retries = DEFAULT_NUMBER_RETRIES,
    retry_sleep = DEFAULT_RETRY_SLEEP
):
    """
    Executes the given callable retrying the call in case an exception occurs.
    The number of retries and the time between retries is configurable.
    The method returns the return value from the call or raises the last
    known exception.

    :type callable: Callable
    :param callable: The callable to be called using retries.
    :type number_retries: int
    :param number_retries: The number of retries to be used.
    :type retry_sleep: int´
    :param retry_sleep: The sleep time between retries.
    :rtype: Object
    :return: The return value from the callable.
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
        except Exception:
            # in case it's the last index position
            # the exception should be re-raised
            if index == number_retries: raise

            # sleeps a while to avoid problems
            time.sleep(retry_sleep)

    # returns the callable return value
    return return_value

def call_safe(callable, *args, **kwargs):
    """
    Method used to call a callable object using a "safe" approach,
    meaning that each of its keyword arguments will be validated
    for existence in the target callable definition.

    In case the validation of the keyword argument fails the same
    argument is removed from the map of keyword arguments.

    Note that in case the wildcard based kwargs value exists in
    the callable definition the callable is immediately considered
    to be valid and the call is ran.

    :type callable: Callable
    :param callable: The callable that is going to have the keyword
    based arguments validated and the get called.
    :rtype: object
    :return: The resulting value from the safe call of the provided
    callable, this may have any data type.
    """

    # retrieves the arguments specification to the provided callable
    # and retrieves the various argument names and the existence or
    # not of the wildcard kwargs value in the callable and in case it
    # exists runs the callable call immediately
    argspec = legacy.getargspec(callable)
    method_args = argspec[0]
    method_kwargs = argspec[2]
    if method_kwargs: return callable(*args, **kwargs)

    # iterates over the complete set of keyword based arguments to be
    # used in the call and validates them against the method specification
    # in case they do not exist in the specification deletes them from
    # the map of keyword based arguments (not going to be sent)
    for name in legacy.keys(kwargs):
        if name in method_args: continue
        del kwargs[name]

    # runs the callable with the "remaining" arguments and keyword arguments
    # returning the value to the caller method
    return callable(*args, **kwargs)
