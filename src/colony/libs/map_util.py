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

import sys
import copy
import calendar
import datetime

from colony.base import legacy

def map_clean(map):
    """
    Cleans the map from all of its entries.
    The clean process is "slow" as it iterates over
    all the map keys to remove its values.

    :type map: Dictionary
    :param map: The map to be cleaned.
    """

    # retrieves the map keys
    map_keys = legacy.keys(map)

    # iterates over all the map keys deleting
    # the complete set of item present in it
    for map_key in map_keys: del map[map_key]

def map_get(map, keys = []):
    """
    Recursively retrieves values from the provided map using
    the sequence of keys provided.

    This method may suffer from stack overflow (recursion) so
    a reasonable list of keys should be provided to avoid that.

    :type map: Dictionary
    :param map: The map (containing maps) from which the value
    is going to be retrieved using a recursive strategy.
    :type keys: List
    :param keys: The list of keys to be used in the recursive
    retrieval of values from the map.
    :rtype: Object
    :return: The final value retrieved through recursion
    """

    if not keys: return map
    return map_get(map[keys[0]], keys[1:])

def map_copy(source_map, destiny_map):
    """
    Copies the contents of the source map to the destiny map.

    Note that in case the value already exists in the destiny
    map the copy step will be ignored.

    :type source_map: Dictionary
    :param source_map: The source map of the copy.
    :type destiny_map: Dictionary
    :param destiny_map: The destiny map of the copy.
    """

    # iterates over all the source map keys in order to copy
    # the complete set of values from the source to destiny map
    for source_map_key in source_map:
        # retrieves the source map value, that may be set
        # in the destiny map in case no duplicate key exists
        source_map_value = source_map[source_map_key]

        # in case the key is not present in the destiny map
        # must add it into the destiny map (ensures existence)
        if not source_map_key in destiny_map or\
            destiny_map[source_map_key] == None or\
            destiny_map[source_map_key] == "none":
            destiny_map[source_map_key] = source_map_value

def map_copy_deep(source_map, destiny_map):
    """
    Copies the contents of the source map to the destiny map.
    This mode provides a deep copy, using a recursive approach.

    :type source_map: Dictionary
    :param source_map: The source map of the copy.
    :type destiny_map: Dictionary
    :param destiny_map: The destiny map of the copy.
    """

    # copies the current source map to the destiny map
    map_copy(source_map, destiny_map)

    # iterates over all the source map items
    for source_key, source_value in legacy.iteritems(source_map):
        # retrieves the source value type
        source_value_type = type(source_value)

        # in case the source value type is not a dictionary
        # continues the loop, nothing to be done in the
        # current iteration
        if not source_value_type == dict: continue

        # creates the destiny value map and sets the
        # destiny value in the destiny map
        destiny_value = {}
        destiny_map[source_key] = destiny_value

        # copies the source value (map) to the destiny value
        map_copy_deep(source_value, destiny_value)

def map_duplicate(item):
    """
    Duplicates the provided item (map) creating a new
    structure with duplicated references both for sequences
    (list and tuples) and for maps.

    This function is useful in order to avoid reference
    overlapping in data structures.

    :type item: Object
    :param item: The item to be used as reference for duplication
    this should be a map at the initial call of the function.
    :rtype: item: Object
    :return: The duplicated data structure with all the references
    replicated in the sequences and maps.
    """

    # retrieves the type for the current
    # item in order to percolate it appropriately
    _type = type(item)

    # in case the current item is a sequence
    # must "copy" all of its elements
    if _type in (list, tuple):
        return [map_duplicate(value) for value in item]

    # in case the current item is a map
    # must create a new map with the result
    # of the copy of all the elements
    elif _type == dict:
        # creates the item map to be populated
        # with the copied values
        _item = {}

        # iterates over all the items to copy
        # them and sets them in the new items map
        for key, value in legacy.iteritems(item):
            _item[key] = map_duplicate(value)
        return _item

    # otherwise must be a "single" item and the
    # (reduce) operation must be performed on it
    else:
        return item

def map_remove(removal_map, destiny_map):
    """
    Removes all the values with keys present in the
    removal map from the destiny map.

    :type removal_map: Dictionary
    :param removal_map: The map to be used in reference
    with the key values.
    :type destiny_map: Dictionary
    :param destiny_map: The "destiny" map to have the values removed.
    """

    # iterates over all the keys in
    # the removal map
    for key in removal_map:
        # in case the key does not exists in
        # destiny map, continues the loop
        if not key in destiny_map: continue

        # removes the key item from the destiny map
        del destiny_map[key]

def map_extend(
    base_map,
    extension_map,
    override = True,
    recursive = False,
    copy_base_map = True
):
    """
    Extends the given map with the extension map,
    retrieving a map resulting of the merge of both maps.

    In case the override flag is set the values are overridden
    in case they already exist in the base map.

    An optional recursive flag allows the extension to be
    made recursive in case the value is a map.

    The base map may be changed or left untouched based on
    the copy base map flag.

    :type base_map: Dictionary
    :param base_map: The map to be used as base for the merge,
    should contain more values at the end of the merge.
    :type extension_map: Dictionary
    :param extension_map: The map to be used to extend the base
    one, this map may be recursively percolated if requested.
    :type override: bool
    :param override: If a value should be overridden in
    case it already exists in the base map.
    :type recursive: bool
    :param recursive: If a value should be extended in
    case it already exists in the base map (recursive
    extension).
    :type copy_base_map: bool
    :param copy_base_map: If the base map should be copied before
    being extended in order to avoid loss of data.
    :rtype: Dictionary
    :return: The map that result of the merge of both maps.
    """

    # copies the base map to create the initial result map (optional)
    result_map = copy.copy(base_map) if copy_base_map else base_map

    # iterates over all the keys and values
    # in the extension map
    for key, value in legacy.iteritems(extension_map):
        # in case the override flag is not set and
        # the key already exists in the result map
        # must skip the current iteration loop
        if not override and key in result_map:
            continue

        # retrieves the data type for the current value in
        # iteration so that it may be used to determine the
        # need for the recursive percolated copy/merge
        value_type = type(value)

        # in case the value is a map and the recursive flag
        # is set, must try to extend the current item with
        # the new one, as expected
        if recursive and value_type == dict:
            #  tries to retrieve the result map value, so
            # that it's possible to extend the current value
            # with the previously existing one, a default map
            # is created in case it does not exists so that
            # it's possible to used as the base for population
            result_map_value = result_map.get(key, {})

            # extends the map that is currently in the result
            # map with the new value (recursive step), note
            # that a new map may have been created to be used
            # as the placeholder of new map values, this avoids
            # collision between sub-maps (would cause problems)
            value = map_extend(
                result_map_value,
                value,
                override = override,
                recursive = recursive,
                copy_base_map = copy_base_map
            )

        # sets the (extension) value in the result map
        result_map[key] = value

    # returns the result map
    return result_map

def map_flatten(map):
    """
    Flattens the provided map, meaning that in case there's a
    value in the map associated with another map the name in
    that map will be linearized into the top level map.

    :type map: Dictionary
    :param map: The map that is going to be linearized/flatten
    and for each relations will be set in the top level.
    :rtype: Dictionary
    :return: The resulting flatten map, note that the original
    map is not changed.
    """

    # creates a new dictionary/map to hold the resulting map,
    # then retrieves the various linear key and value pairs
    # for the complete set of relations setting the values
    # in the resulting map and returns the map to caller method
    result = dict()
    pairs = _map_flatten_pairs(map)
    for key, value in pairs: result[key] = value
    return result

def map_check_parameters(map, parameters_list, exception = Exception):
    """
    Checks if the parameters in the parameters list are defined
    in the given map.
    In case a check fails an exception is raised.

    :type map: Dictionary
    :param map: The dictionary to be checked.
    :type parameters_list: List
    :param parameters_list: The list of parameters to be checked.
    :type exception: Exception
    :param exception: The exception to be raised in case check fails.
    """

    # iterates over all the parameters in the parameters list
    # to try to verify for their existence in the map
    for parameter in parameters_list:
        # in case the parameter is in the map must continue
        # the current loop, no exception raised this time
        if parameter in map: continue

        # raises the provided exception as the parameter does
        # not exist in the provided map
        raise exception(parameter)

def map_get_value_cast(map, key, cast_type = str, default_value = None):
    """
    Retrieves the value of the map for the given key.
    The value is casted to the given type.
    In case something wrong (exception raised) occurs
    the default value is returned.

    :type map: Dictionary
    :param map: The dictionary to be used.
    :type key: String
    :param key: The key to the value to be retrieved.
    :type cast_type: Type
    :param cast_type: The type to be used to cast the retrieved
    value (this should be a valid type, with constructor).
    :type default_value: Object
    :param default_value: The default value to be used
    when something wrong (exception raised) occurs.
    :rtype: Object
    :return: The retrieved value casted to the defined type.
    """

    try:
        # retrieves the value for the map
        value = map[key]

        # retrieves the value type
        value_type = type(value)

        # in case the type of the value
        # is the "target" cast type
        if value_type == cast_type:
            # sets the value casted as the
            # "original" value
            value_casted = value
        # otherwise
        else:
            # casts the value for the cast type
            value_casted = cast_type(value)

        # returns the value casted
        return value_casted
    except Exception:
        # returns the default value
        return default_value

def map_get_values(map, key):
    """
    Retrieves the value of the map for the given key.
    The value is validated for type and in case it's not
    a list a list is created with the value.
    This way the method return value is always a list
    independently from the type of the original value.

    :type map: Dictionary
    :param map: The dictionary to be used.
    :type key: String
    :param key: The key to the value(s) to be retrieved.
    :rtype: List
    :return: The values(s) for the key.
    """

    # retrieves the values from the map
    values = map.get(key, [])

    # retrieves the values type
    values_type = type(values)

    # in case the values element is not a list
    # the values element is converted into a
    # a list with the original values in it,
    # ensuring that the returned value is always
    # a valid sequence value, ready to be iterated
    if not values_type == list: values = [values]

    # returns the values
    return values

def map_output(map, output_method = sys.stdout.write, indentation = ""):
    """
    Outputs (pretty print) the given map, using the
    defined output method.
    The map is printed with the given indentation as a start
    point from the line.

    :type map: Dictionary
    :param map: The map to be outputted (pretty print).
    :type output_method: Function
    :param output_method: The output function (method) to be
    used for outputting the value.
    :type indentation: String
    :param indentation: The indentation level to be used.
    """

    # iterates over all the keys in the map in order to render
    # their value to the provided output method/function
    for key in map:
        # retrieves the map value
        map_value = map[key]

        # outputs the map value, meaning that a key to value
        # association will be "printed" to the output method
        if type(map_value) == dict:
            # defines the key string with the proper indentation
            # value and the key value and outputs it properly
            key_string = indentation + legacy.UNICODE(key) + ":"
            output_method(key_string)

            # defines the "new" output map indentation and runs the
            # recursive operation so that the new map is printed
            output_map_identation = indentation + "  "
            map_output(map_value, output_method, output_map_identation)

        # otherwise it must be a "simple" value and so the a "simple"
        # key and value string is going to be printed to the method
        else:
            # creates a string representation of the map value and
            # then "runs" it to the output method
            map_value_string = indentation + legacy.UNICODE(key) +\
                " = " + legacy.UNICODE(map_value)
            output_method(map_value_string)

def map_normalize(item, operation = None):
    """
    Normalizes the provided map/item, applying the reduce
    operation to each of the items.

    In case no operation is provided, the default reduce
    map operation is used.

    This operation may be used to convert "complex" type
    based maps into simplified type based maps.

    :type item: Object
    :param item: The map/item to be normalized.
    :type operation: Method
    :param operation: The operation used for normalization
    (reduce operation).
    :rtype: Object
    :return: The normalized map, resulting from the normalization
    of each of its items.
    """

    # sets the (reduce) operation, defaulting
    # to reduce map in case none is defined
    operation = operation or _map_reduce

    # retrieves the type for the current
    # item in order to percolate it appropriately
    _type = type(item)

    # in case the current item is a sequence
    # must normalize all of its elements
    if _type in (list, tuple):
        return [map_normalize(value, operation) for value in item]

    # in case the current item is a map
    # must create a new map with the result
    # of the normalization of all the elements
    elif _type == dict:
        # creates the item map to be populated
        # with the normalized values
        _item = {}

        # iterates over all the items to normalize
        # them and sets them in the new items map
        for key, value in legacy.iteritems(item):
            _item[key] = map_normalize(value, operation)
        return _item

    # otherwise must be a "single" item and the
    # (reduce) operation must be performed on it
    else:
        return operation(item)

def _map_flatten_pairs(map):
    """
    Retrieves the complete set of linear key to value pairs
    of the attributes of the provided map.

    Any dictionary based value of the provided map will be
    linearized using an extra recursion step.

    :type map: Dictionary
    :param map: The map that is the basis of the recursion
    step for the retrieval of the key value pairs.
    :rtype: Generator
    :return: A generator that yields the various key to value
    linear relations, using a recursive approach.
    """

    # iterates over the complete set of key value pairs of the
    # provided map to verify if the pair is map based and if
    # that's the case run a new depth of recursion with a new
    # composite name, so that all relations are linearized
    for key, value in legacy.iteritems(map):
        is_class = hasattr(value, "__class__")
        is_map = is_class and issubclass(value.__class__, dict)
        if not is_map: yield key, value; continue
        pairs = _map_flatten_pairs(value)
        for _key, _value in pairs: yield key + "." + _key, _value

def _map_reduce(value):
    """
    Reduces the provided value, converting it into the appropriate
    value considered to be "raw".

    :type value: Object
    :param value: The value to be reduced.
    :rtype: Object
    :return: The reduced value affected by the transformed function.
    """

    # retrieves the type for the item
    _type = type(value)

    # in case the current value is of type datetime then
    # it must be converted to the corresponding timestamp
    if _type == datetime.datetime:
        timetuple = value.utctimetuple()
        return calendar.timegm(timetuple)

    # returns the original value (default fallback)
    return value
