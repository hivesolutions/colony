#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import types

class OrderedMap:
    """
    Structure that allow the usage of a map
    like syntax to create ordered elements.
    """

    tuples_list = None
    """ The list of tuples """

    _map = None
    """ The map to be used internally for virtual access """

    _keys = None
    """ The internal keys list for ordered keys retrieval """

    def __init__(self, ordered_keys = False):
        """
        Constructor of the class.

        @type ordered_keys: bool
        @param ordered_keys: If the keys should also be provided
        in an ordered fashion (expensive remove operation).
        """

        self.tuples_list = []
        self._map = {}

        if ordered_keys: self._keys = []

    def __len__(self):
        return self._map.__len__()

    def __getitem__(self, key):
        return self._map[key]

    def __setitem__(self, key, value):
        self.__add_item(key, value)

    def __delitem__(self, key):
        self.__remove_item(key)

    def __iter__(self):
        return OrderedMapIterator(self)

    def __contains__(self, item):
        return self._map.__contains__(item)

    def get(self, key, default_value):
        return self._map.get(key, default_value)

    def values(self):
        return self._map.values()

    def items(self):
        return self.tuples_list

    def extend(self, map):
        # iterates over all the map items
        for key, value in map.items():
            # sets the item in the structure
            self.__setitem__(key, value)

    def keys(self):
        # in case the keys (list) is not
        # defined (no ordered keys used)
        if self._keys == None:
            keys = self._map.keys()
        # otherwise the ordered keys list
        # is available and must be used
        else:
            keys = self._keys

        # returns the valid keys
        return keys

    def __add_item(self, key, value):
        """
        Adds an item with the given key to the
        internal structures.

        @type key: String
        @param key: The key of the element to be added
        to the internal structures.
        @type value: Object
        @param value: The value of the element to be added
        to the internal structures.
        """

        # in case the key (item) exists
        # in the map
        if key in self._map:
            # removes the item from the internal
            # structures (using the key)
            self.__remove_item(key)

        # adds the tuple to the tuples list
        self.tuples_list.append((key, value))

        # sets the value in the map
        self._map[key] = value

        # adds the key to the keys list (only in case
        # the keys list is available and set)
        if not self._keys == None: self._keys.append(key)

    def __remove_item(self, key):
        """
        Removes the item with the given key from the
        internal structures.

        @type key: String
        @param key: The key of the element to be removed
        from the internal structures.
        """

        # retrieves the value for the key
        value = self._map[key]

        # removes the tuple from the tuples list
        self.tuples_list.remove((key, value))

        # removes the value from the map
        del self._map[key]

        # removes the key from the keys list (only in case
        # the keys list is available and set)
        if not self._keys == None: self._keys.remove(key)

class OrderedMapIterator:
    """
    The iterator for the ordered map.
    """

    ordered_map = None
    """ The ordered map to be used """

    current_index = None
    """ The current index value """

    def __init__(self, ordered_map):
        """
        Constructor of the class.

        @type ordered_map: OrderedMap
        @param ordered_map: The ordered map to be used by the iterator.
        """

        self.ordered_map = ordered_map

        self.current_index = 0

    def next(self):
        """
        Retrieves the next ordered map key.

        @rtype: String
        @return: The next key in the ordered map.
        """

        # retrieves the ordered map length
        ordered_map_length = len(self.ordered_map)

        # in case there is an overflow (current index is over the length)
        if not ordered_map_length > self.current_index:
            # breaks the iteration
            raise StopIteration()

        # retrieves the key and value for the current index
        key, _value = self.ordered_map.tuples_list[self.current_index]

        # increments the current index
        self.current_index += 1

        # returns the current key value
        return key

class MultipleValueMap:
    """
    Map that holds multiple values for
    each key, and considers
    the first value to the key's value.
    """

    _map = None
    """ The map to be used internally for virtual access """

    def __init__(self):
        """
        Constructor of the class.
        """

        # initializes the map
        self._map = {}

    def __len__(self):
        return self._map.__len__()

    def __getitem__(self, key):
        # returns the value
        values = self._map.get(key)

        # returns in case no
        # value was found
        if not values:
            return

        # retrieves the first value
        value = values[0]

        # returns the value
        return value

    def __setitem__(self, key, value):
        # retrieves the values
        values = self._map.get(key, [])

        # adds the value to the list
        values.append(value)

        # sets the values in the map
        self._map[key] = values

    def __delitem__(self, key):
        del self._map[key]

    def __iter__(self):
        return self._map.__iter__()

    def __contains__(self, item):
        return self._map.__contains__(item)

    def get(self, key, default_value):
        return self._map.get(key, default_value)

    def values(self):
        return self._map.values()

    def items(self):
        return self.tuples_list

    def keys(self):
        return self._map.keys()

    def unset(self, key, value):
        """
        Unsets the value from the specified key.

        @type key: Object
        @param key: The key where to unset the value.
        @type value: Object
        @param value: The value to unset.
        """

        # retrieves the values
        values = self._map[key]

        # removes the value
        values.remove(value)

def is_dictionary(object):
    """
    Validates if the given object is a valid
    dictionary object.

    @type object: Object
    @param object: The object to be validated.
    @rtype: bool
    @return: If the given object is a valid
    dictionary object.
    """

    # retrieves the object type
    object_type = type(object)

    # in case the object type is dictionary
    if object_type == types.DictType:
        # returns true
        return True

    # in case the object type is instance and
    # the class is ordered map
    if object_type == types.InstanceType and object.__class__ == OrderedMap:
        # returns true
        return True

    # returns false
    return False
