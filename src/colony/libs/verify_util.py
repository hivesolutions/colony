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

from colony.base import exceptions

def verify(condition, message = None, code = None, exception = None, **kwargs):
    if condition: return
    exception = exception or exceptions.AssertionError
    kwargs = dict(kwargs)
    if not message == None: kwargs["message"] = message
    if not code == None: kwargs["code"] = code
    raise exception(**kwargs)

def verify_equal(first, second, message = None, code = None, exception = None, **kwargs):
    message = message or "Expected %s got %s" % (repr(second), repr(first))
    return verify(
        first == second,
        message = message,
        code = code,
        exception = exception,
        **kwargs
    )

def verify_not_equal(first, second, message = None, code = None, exception = None, **kwargs):
    message = message or "Expected %s not equal to %s" % (repr(first), repr(second))
    return verify(
        not first == second,
        message = message,
        code = code,
        exception = exception,
        **kwargs
    )

def verify_type(value, types, null = True, message = None, code = None, exception = None, **kwargs):
    message = message or "Expected %s to have type %s" % (repr(value), repr(types))
    return verify(
        (null and value == None) or isinstance(value, types),
        message = message,
        code = code,
        exception = exception,
        **kwargs
    )

def verify_many(sequence, message = None, code = None, exception = None, **kwargs):
    for condition in sequence:
        verify(
            condition,
            message = message,
            code = code,
            exception = exception,
            **kwargs
        )
