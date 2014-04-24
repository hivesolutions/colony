#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class LazyClass(object):
    """
    Class representing a lazy loaded symbol, objects
    from this class may be used to represent a lazy
    loaded symbol to the end developer.
    """

    def __repr__(self):
        return "<lazy>"

    def __eq__(self, other):
        if other == None: return True

        return hash(self) == hash(other)

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

    def next(self):
        raise StopIteration()

# creates the global unique reference
# to the object to be used for lazy
# loaded symbols
Lazy = LazyClass()

# creates the global unique reference
# to the lazy iterator (singleton object)
LazyIterator = LazyIteratorClass()
