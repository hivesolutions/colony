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

import sys
import copy
import types

def map_clean(map):
    """
    Cleans the map from all of its entries.
    The clean process is "slow" as it iterates over
    all the map keys to remove its values.

    @type map: Dictionary
    @param map: The map to be cleaned.
    """

    # retrieves the map keys
    map_keys = map.keys()

    # iterates over all the map keys
    for map_key in map_keys:
        # removes the map entry
        del map[map_key]

def map_copy(source_map, destiny_map):
    """
    Copies the contents of the source map to the destiny map.

    @type source_map: Dictionary
    @param source_map: The source map of the copy.
    @type destiny_map: Dictionary
    @param destiny_map: The destiny map of the copy.
    """

    # iterates over all the source map keys
    for source_map_key in source_map:
        # retrieves the source map value
        source_map_value = source_map[source_map_key]

        # in case the key is not present in the destiny map
        if not source_map_key in destiny_map or destiny_map[source_map_key] == None or destiny_map[source_map_key] == "none":
            # adds the value to the destiny map
            destiny_map[source_map_key] = source_map_value

def map_copy_deep(source_map, destiny_map):
    """
    Copies the contents of the source map to the destiny map.
    This mode provides a deep copy, using a recursive approach.

    @type source_map: Dictionary
    @param source_map: The source map of the copy.
    @type destiny_map: Dictionary
    @param destiny_map: The destiny map of the copy.
    """

    # copies the current source map to the destiny map
    map_copy(source_map, destiny_map)

    # iterates over all the source map items
    for source_key, source_value in source_map.items():
        # retrieves the source value type
        source_value_type = type(source_value)

        # in case the source value type is dictionary
        if not source_value_type == types.DictType:
            # continues the loop
            continue

        # creates the destiny value map
        destiny_value = {}

        # sets the destiny value in the destiny map
        destiny_map[source_key] = destiny_value

        # copies the source value (map) to the destiny value
        map_copy_deep(source_value, destiny_value)

def map_remove(removal_map, destiny_map):
    """
    Removes all the values with keys present in the
    removal map from the destiny map.

    @type removal_map: Dictionary
    @param removal_map: The map to be used in reference
    with the key values.
    @type destiny_map: Dictionary
    @param destiny_map: The "destiny" map to have the values removed.
    """

    # iterates over all the keys in
    # the removal map
    for key in removal_map:
        # removes the key item from the destiny map
        del destiny_map[key]

def map_extend(base_map, extension_map, override = True):
    """
    Extends the given map with the extension map,
    retrieving a map resulting of the merge of both maps.
    In case the override flag is set the values are overridden
    in case they already exist in the base map.

    @type base_map: Dictionary
    @param base_map: The map to be used as base for
    the merge.
    @type extension_map: Dictionary
    @param extension_map: The map to be used to extend the base
    one.
    @type override: bool
    @param override: If a value should be overridden in
    case it already exists in the base map.
    @rtype: Dictionary
    @return: The map that result of the merge of both maps.
    """

    # copies the base map to create the initial result map
    result_map = copy.copy(base_map)

    # iterates over all the keys and values
    # in the extension map
    for key, value in extension_map.items():
        # in case the override flag is not set
        # and the key already exists in the result map
        if not override and key in result_map:
            # continues the loop
            continue

        # sets the extension value in the result map
        result_map[key] = value

    # returns the result map
    return result_map

def map_check_parameters(map, parameters_list, exception = Exception):
    """
    Checks if the parameters in the parameters list are defined
    in the given map.
    In case a check fails an exception is raised.

    @type map: Dictionary
    @param map: The dictionary to be checked.
    @type parameters_list: List
    @param parameters_list: The list of parameters to be checked.
    @type exception: Exception
    @param exception: The exception to be raised in case check fails.
    """

    # iterates over all the parameters in the parameters list
    for parameter in parameters_list:
        # in case the parameter is not in the map
        if not parameter in map:
            # raises the exception
            raise exception(parameter)

def map_get_value_cast(map, key, cast_type = str, default_value = None):
    """
    Retrieves the value of the map for the given key.
    The value is casted to the given type.
    In case something wrong (exception raised) occurs
    the default value is returned.

    @type map: Dictionary
    @param map: The dictionary to be used.
    @type key: String
    @param key: The key to the value to be retrieved.
    @type cast_type: Type
    @param cast_type: The type to be used to cast the retrieved
    value (this should be a valid type, with constructor).
    @type default_value: Object
    @param default_value: The default value to be used
    when something wrong (exception raised) occurs.
    @rtype: Object
    @return: The retrieved value casted to the defined type.
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
    except:
        # returns the default value
        return default_value

def map_get_values(map, key):
    """
    Retrieves the value of the map for the given key.
    The value is validated for type and in case it's not
    a list a list is created with the value.
    This way the method return value is always a list
    independently from the type of the original value.

    @type map: Dictionary
    @param map: The dictionary to be used.
    @type key: String
    @param key: The key to the value(s) to be retrieved.
    @rtype: List
    @return: The values(s) for the key.
    """

    # retrieves the values from the map
    values = map.get(key, [])

    # retrieves the values type
    values_type = type(values)

    # in case the values element is not a list
    if not values_type == types.ListType:
        # creates the list with the values element
        values = [values]

    # returns the values
    return values

def map_output(map, output_method = sys.stdout.write, indentation = ""):
    """
    Outputs (pretty print) the given map, using the
    defined output method.
    The map is printed with the given indentation as a start
    point from the line.

    @type map: Dictionary
    @param map: The map to be outputed (pretty print).
    @type output_method: Function
    @param output_method: The output function (method) to be
    used for outputting the value.
    @type indentation: String
    @param indentation: The indentation level to be used.
    """

    # iterates over all the keys in the map
    for key in map:
        # retrieves the map value
        map_value = map[key]

        # outputs the map value
        if type(map_value) == types.DictType:
            # defines the key string
            key_string = indentation + unicode(key) + ":"

            # outputs the key string
            output_method(key_string)

            # defines the output map indentation
            output_map_identation = indentation + "  "

            # outputs the map value
            map_output(map_value, output_method, output_map_identation)
        # otherwise it must be a "simple" value
        else:
            # creates a string representation of the map value
            map_value_string = indentation + unicode(key) + " = " + unicode(map_value)

            # outputs the map value string
            output_method(map_value_string)
