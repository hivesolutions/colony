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

class LazyClass(object):
    """
    Class representing a lazy loaded symbol, objects
    from this class may be used to represent a lazy
    loaded symbol to the end developer.
    """

    def __repr__(self):
        return "<lazy>"

    def __hash__(self):
        return None.__hash__()

    def __eq__(self, other):
        if other == None: return True
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return other

    def __radd__(self, other):
        return other

    def __nonzero__(self):
        return False

    def __len__(self):
        return 0

    def __iter__(self):
        return LazyIterator

class LazyIteratorClass(object):
    """
    Class representing an "empty" iterator to be used
    to provider iterator capabilities to the lazy
    object.

    This way it's possible to "iterate" over the globally
    available lazy object.
    """

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration()

    def next(self):
        raise StopIteration()

def is_lazy(value):
    """
    Verifies if the provided value is a lazy loaded value
    by "looking" at its data type.

    This is a simple and quick util for file type verification
    and should be used as often as possible to provide a valid,
    simple and coherent interface for lazy verification/validation.

    :type value: Object
    :param value: The value that is going to be verified to
    be lazy loaded or not (lazy verification).
    :rtype: bool
    :return: If the provided value is a lazy loaded value or not
    according to the current specification.
    """

    return type(value) == LazyClass

# creates the global unique reference
# to the object to be used for lazy
# loaded symbols
Lazy = LazyClass()

# creates the global unique reference
# to the lazy iterator (singleton object)
LazyIterator = LazyIteratorClass()
