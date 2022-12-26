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

import math

from colony.base import legacy

FLOAT_PRECISION = 14
""" The amount of precision (in decimal places) that
is going to be used for the decimal internal usage """

class Decimal(float):
    """
    Fixed point rational number representation/manipulation
    structure aimed at replacing the internal python data
    structure with the same name.

    Provides a simple unified way of re-using the float data
    type to performed fixed point operations, using techniques
    around the special rounding method.

    The implementation of the data structure is not aimed at
    performance and because of that it should not be used for
    task that are considered performance intensive.
    """

    def __new__(self, value = 0.0):
        value = float(value)
        integer = abs(int(value // 1))
        count = 1 if integer == 0 else int(math.log10(integer)) + 1
        places = FLOAT_PRECISION - count
        self.places = places
        value = round(value, places)
        return super(Decimal, self).__new__(self, value)

    def __hash__(self):
        return float.__hash__(self)

    def __cmp__(self, other):
        other = self._normalize(other)
        if float.__gt__(self, other): return 1
        if float.__lt__(self, other): return -1
        return 0

    def __lt__(self, other):
        other = self._normalize(other)
        return float.__lt__(self, other)

    def __le__(self, other):
        other = self._normalize(other)
        return float.__le__(self, other)

    def __eq__(self, other):
        other = self._normalize(other)
        return float.__eq__(self, other)

    def __ne__(self, other):
        other = self._normalize(other)
        return float.__ne__(self, other)

    def __gt__(self, other):
        other = self._normalize(other)
        return float.__gt__(self, other)

    def __ge__(self, other):
        other = self._normalize(other)
        return float.__ge__(self, other)

    def __add__(self, other):
        result = float.__add__(self, other)
        return Decimal(result)

    def __radd__(self, other):
        result = float.__radd__(self, other)
        return Decimal(result)

    def __sub__(self, other):
        result = float.__sub__(self, other)
        return Decimal(result)

    def __rsub__(self, other):
        result = float.__rsub__(self, other)
        return Decimal(result)

    def __mul__(self, other):
        result = float.__mul__(self, other)
        return Decimal(result)

    def __rmul__(self, other):
        result = float.__rmul__(self, other)
        return Decimal(result)

    def __floordiv__(self, other):
        result = float.__floordiv__(self, other)
        return Decimal(result)

    def __rfloordiv__(self, other):
        result = float.__rfloordiv__(self, other)
        return Decimal(result)

    def __div__(self, other):
        result = float.__div__(self, other)
        return Decimal(result)

    def __rdiv__(self, other):
        result = float.__rdiv__(self, other)
        return Decimal(result)

    def __truediv__(self, other):
        result = float.__truediv__(self, other)
        return Decimal(result)

    def __rtruediv__(self, other):
        result = float.__rtruediv__(self, other)
        return Decimal(result)

    def __mod__(self, other):
        result = float.__mod__(self, other)
        return Decimal(result)

    def __rmod__(self, other):
        result = float.__rmod__(self, other)
        return Decimal(result)

    def __and__(self, other):
        other = self._normalize(other)
        return float.__and__(self, other)

    def __rand__(self, other):
        other = self._normalize(other)
        return float.__rand__(self, other)

    def __or__(self, other):
        other = self._normalize(other)
        return float.__or__(self, other)

    def __ror__(self, other):
        other = self._normalize(other)
        return float.__ror__(self, other)

    def __xor__(self, other):
        other = self._normalize(other)
        return float.__xor__(self, other)

    def __rxor__(self, other):
        other = self._normalize(other)
        return float.__rxor__(self, other)

    def __pos__(self):
        result = float.__pos__(self)
        return Decimal(result)

    def __neg__(self):
        result = float.__neg__(self)
        return Decimal(result)

    def __abs__(self):
        result = float.__abs__(self)
        return Decimal(result)

    def __invert__(self):
        result = float.__invert__(self)
        return Decimal(result)

    def __round__(self, n = 0):
        result = float.__round__(self, n)
        return Decimal(result)

    def __floor__(self):
        result = math.floor(float(self))
        return Decimal(result)

    def __ceil__(self):
        result = math.ceil(float(self))
        return Decimal(result)

    def __trunc__(self):
        result = float.__trunc__(self)
        return Decimal(result)

    def _normalize(self, value):
        if not type(value) == float: return value
        return round(value, self.places)

class JournaledList(list):
    """
    List structure that keeps track of the append and
    remove operation in a jounalized format.
    This structures is relevant for use cases where
    "diffs" around a base list must be kept.
    """

    _appends = []
    """ The list containing the various appends to the list (journal) """

    _removes = []
    """ The list containing the various removes from the list (journal) """

    def __init__(self, *args, **kwargs):
        """
        Constructor of the class, this constructor
        may be used together with a previously "simple" list
        to start the jounalized list with initial (non logged)
        values.
        """

        list.__init__(self, *args, **kwargs)

        self._appends = []
        self._removes = []

    def append(self, object):
        """
        Appends an object to the list, keeping the registry
        of the operation in the appends list.

        :type object: Object
        :param object: The object to be appended to the list.
        """

        # appends the object to the list
        list.append(self, object)

        # in case the object is present in the removes
        # list it must be removed (previous reverse operations
        # should reverted)
        if object in self._removes:
            # removes the object from the removes list
            # (reversion of operation)
            self._removes.remove(object)
        # otherwise the object must be added to the
        # appends list (normal behavior)
        else:
            # appends the object to the appends list
            # (for logging)
            self._appends.append(object)

    def remove(self, object):
        """
        Removes an object from the list, keeping the registry
        of the operation in the removes list.

        :type object: Object
        :param object: The object to be removed from the list.
        """

        # removes the object from the list, an exception
        # should be raises in case it fails
        list.remove(self, object)

        # in case the object is present in the appends
        # list it must be removed (previous reverse operations
        # should reverted)
        if object in self._appends:
            # removes the object from the appends list
            # (reversion of operation)
            self._appends.remove(object)
        # otherwise the object must be added to the
        # removes list (normal behavior)
        else:
            # appends the object to the removes list
            # (for logging)
            self._removes.append(object)

    def clear_jounal(self):
        """
        Clears the journal, reseting it to the original
        state (internal structures state).
        This method should be called whenever a new jounalized
        unit is required for a new phase
        """

        del self._appends[:]
        del self._removes[:]

    def get_appends(self):
        """
        Retrieves the list of the current (valid) append operations
        from the journaled list.

        :rtype: List
        :return: The list of the current (valid) append operations
        from the journaled list.
        """

        return self._appends

    def get_removes(self):
        """
        Retrieves the list of the current (valid) remove operations
        from the journaled list.

        :rtype: List
        :return: The list of the current (valid) remove operations
        from the journaled list.
        """

        return self._removes

    def _append(self, object):
        """
        Appends an object to the list, avoiding the keeping
        of a log on that operation (simple operation).

        :type object: Object
        :param object: The object to be appended to the list.
        """

        list.append(self, object)

    def _remove(self, object):
        """
        Removes an object from the list, avoiding the keeping
        of a log on that operation (simple operation).

        :type object: Object
        :param object: The object to be removed from the list.
        """

        list.remove(self, object)

class OrderedMap(object):
    """
    Structure that allow the usage of a map
    like syntax to create ordered elements.

    The ordered map uses a composing strategy to
    achieve the extra behavior for order in map.
    """

    tuples_list = None
    """ The list of tuples """

    _map = None
    """ The map to be used internally for virtual access """

    _keys = None
    """ The internal keys list for ordered keys retrieval """

    def __init__(self, ordered_keys = False, map = None):
        """
        Constructor of the class.

        In case a map is provided the map is first sorted according
        to the default sorting operation in the map keys and then
        all of their values are entered.

        :type ordered_keys: bool
        :param ordered_keys: If the keys should also be provided
        in an ordered fashion (expensive remove operation).
        :type map: Dictionary
        :param map: The map to be used to populate the ordered map
        initially using the default key order.
        """

        self.tuples_list = []
        self._map = {}

        if ordered_keys: self._keys = []
        if map: self._load_map(map)

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
        for key, value in legacy.iteritems(map):
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

    def itervalues(self):
        return self._map.itervalues()

    def iteritems(self):
        return self.items()

    def iterkeys(self):
        return self.keys()

    def _load_map(self, map):
        """
        Loads the provided map into the current ordered
        map so that the keys are sorted in the default
        manner and then the associated items are inserted
        using the order of the keys.

        :type map: Dictionary
        :param map: The map that is going to be used to
        populate the current ordered map using the default
        order of the keys.
        """

        keys = map.keys()
        keys.sort()
        for key in keys:
            value = map[key]
            self.__add_item(key, value)

    def __add_item(self, key, value):
        """
        Adds an item with the given key to the
        internal structures.

        :type key: String
        :param key: The key of the element to be added
        to the internal structures.
        :type value: Object
        :param value: The value of the element to be added
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
        # the keys list is available and set and the key
        # is not present in the keys list)
        if not self._keys == None and not key in self._keys: self._keys.append(key)

    def __remove_item(self, key):
        """
        Removes the item with the given key from the
        internal structures.

        :type key: String
        :param key: The key of the element to be removed
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

class OrderedMapIterator(object):
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

        :type ordered_map: OrderedMap
        :param ordered_map: The ordered map to be used by the iterator.
        """

        self.ordered_map = ordered_map

        self.current_index = 0

    def __next__(self):
        """
        Retrieves the next ordered map key.

        This is the magic method responsible for the retrieval of
        the next value (should forward the request).

        :rtype: String
        :return: The next key in the ordered map.
        """

        return self.next()

    def next(self):
        """
        Retrieves the next ordered map key.

        :rtype: String
        :return: The next key in the ordered map.
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

class MultipleValueMap(object):
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

    def itervalues(self):
        return self._map.itervalues()

    def iteritems(self):
        return self.items()

    def iterkeys(self):
        return self._map.keys()

    def unset(self, key, value):
        """
        Unsets the value from the specified key.

        :type key: Object
        :param key: The key where to unset the value.
        :type value: Object
        :param value: The value to unset.
        """

        # retrieves the values
        values = self._map[key]

        # removes the value
        values.remove(value)

class FormatTuple(object):
    """
    Tuple based structure that may be used to represent
    a string to be formated with a series of values.
    This structure provides a portable way of passing
    the base format string and a series of arguments.
    """

    format_string = None
    """ The (base) format string to be used in the
    process of formatting the final string """

    arguments = ()
    """ The tuple containing the various arguments to
    be used during the formatting of the string """

    def __init__(self, format_string, *args):
        """
        Constructor of the class.

        :type format_string: String
        :param format_string: The format string to be
        used during the process of formatting.
        """

        self.format_string = format_string
        self.arguments = args

    @staticmethod
    def build(format_string, *args):
        """
        Builds (constructs) a new format tuple from the provided
        format string and (optional) series of arguments for the
        formatting.

        :type format_string: String
        :param format_string: The string to be used for formatting of
        the string result.
        :rtype: FormatTuple
        :return: The resulting format tuple object from the
        building "generated" from the provided arguments.
        """

        return FormatTuple(format_string, *args)

    def __hash__(self):
        return hash(self.format_string)

    def __str__(self):
        return self.format()

    def __eq__(self, other):
        if other == self.format_string: return True
        return False

    def __ne__(self, value):
        return not self.__eq__(value)

    def __add__(self, other):
        return self.format() + other

    def __radd__(self, other):
        return other + self.format()

    def __replace__(self, value):
        self.set_format_string(value)

    def json_v(self, format = False):
        if format: return self.format()
        else: return (self.format_string, self.arguments)

    def format(self, format_string = None):
        """
        Formats the current format tuple using the currently loaded
        attributes and the provided format string.

        In case no format string is provided the default format
        string is used instead.

        :type format_string: String
        :param format_string: The string to be used for formatting of
        the final string result.
        :rtype: String
        :return: The "final" resulting string after the format of it.
        """

        # retrieves the "final" format string, using the
        # provided format string or the "original" and
        # default format string
        format_string = format_string or self.format_string

        # uses the format string to format the string using
        # the currently available arguments, then returns
        # the resulting string value
        return format_string % self.arguments

    def get_format_string(self):
        """
        Retrieves the currently associated string for formatting
        in the current format tuple.

        :rtype: String
        :return: The currently available format string.
        """

        return self.format_string

    def set_format_string(self, format_string):
        """
        Sets the currently associated string for formatting
        in the current format tuple.

        :type: String
        :param: The string to be set as the currently
        available format string.
        """

        self.format_string = format_string

class FileReference(object):
    """
    Simple structure for the description of a file in the
    current file system.

    The structure contains a series of utility methods that
    allow fast and simple operation on the described file.
    """

    path = None
    """ The file to the file that is being described by the
    the current file reference object """

    encoding = None
    """ The encoding used for the file in case the referred
    file is text based, useful for simple reading operations """

    def __init__(self, path, encoding = None):
        """
        Constructor of the class.

        :type path: String
        :param path: The path to the file that is being described
        by the current file reference object to be created.
        :type encoding: String
        :param encoding: String describing the encoding used by the
        referenced file (only for text based).
        """

        self.path = path
        self.encoding = encoding

    def read_all(self, mode = "rb"):
        """
        Reads the complete set of the contents from the file that
        is currently being described.

        :type mode: String
        :param mode: The file open mode to be used for the reading
        (may control binary/text modes).
        """

        file = open(self.path, mode)
        try: data = file.read()
        finally: file.close()
        if self.encoding: data = data.decode(self.encoding)
        return data

def is_dictionary(object):
    """
    Validates if the given object is a valid
    dictionary object.

    :type object: Object
    :param object: The object to be validated.
    :rtype: bool
    :return: If the given object is a valid
    dictionary object.
    """

    # retrieves the object type
    object_type = type(object)

    # in case the object type is dictionary
    if object_type == dict: return True

    # in case the object type id ordered map
    # (this is the custom dictionary class)
    if object_type == OrderedMap: return True

    # returns false
    return False
