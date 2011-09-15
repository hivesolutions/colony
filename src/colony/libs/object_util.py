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

__revision__ = "$LastChangedRevision: 3219 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-05-26 11:52:00 +0100 (ter, 26 Mai 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import copy
import types

TOPPER_VALUE = "_topper"
""" The value of the attribute to hold the top values """

LIST_TYPES = (types.ListType, types.TupleType)
""" A tuple with the various list types """

def object_flatten(object, flattening_map):
    """
    Flattens the given object using the given flattening
    map as reference for the flattening process.

    @type object: Object
    @param object: The object to be flatten.
    @type flattening_map: Dictionary
    @param flattening_map: Map describing the structure
    for flattening.
    """

    # retrieves the type of the object
    object_type = type(object)

    # in case the type of object is (just)
    # an instance
    if object_type == types.InstanceType:
        # converts the instance to a list
        # (in order to be able to work with it)
        object = [object]
    # in case the object is neither an instance
    # nor a list
    elif object_type in LIST_TYPES:
        # raises a runtime error
        raise RuntimeError("invalid object type")

    # flattens the structure of the object (list)
    # using the flattening map (the returned structure
    # is a list of "flatten" objects)
    flatten_list = _object_flatten(object, flattening_map)

    # returns the flatten list
    return flatten_list

def object_print_list(objects_list):
    """
    Prints some information on the obects
    in the given list, for debugging purposes.

    @type objects_list: List
    @param objects_list: The list of objects
    to be printed for debugging.
    """

    # iterates over all the objects
    # in the objects list to print them
    for object in objects_list:
        # prints the debug information on
        # the object
        object_print(object)

        # prints a blank line
        print ""

def object_print(object):
    """
    Prints some debug information on the
    object, for debugging purposes.

    @type object: Object
    @param object: The object to be printed
    for debugging.
    """

    # retrieves the list of all the attribute names
    # for the object
    attribute_names = dir(object)

    # iterates over all the attribute names of the object
    # (filters the invalid ones)
    for attribute_name in attribute_names:
        # retrieves the attribute and the name
        # of the attribute from the object
        attribute = getattr(object, attribute_name)
        attribute_type = type(attribute)

        if attribute_name in ("__doc__", "__module__"):
            continue

        if attribute_type in (types.InstanceType, types.MethodType, types.ListType):
            continue

        # prints the attribute name and the attribute value
        print "%s: %s" % (attribute_name, attribute)

def _object_flatten(objects_list, flattening_map):
    # iterates over all the "base" objects
    for object in objects_list:
        # flattens the object in the to one relations
        # and the attributes (according to the flattening map)
        __object_flatten_to_one(object, object, flattening_map)

    # flattens the to many relation in the objects
    # in the given list
    objects_list = __object_flatten_to_many(objects_list, flattening_map)

    # flushes the "topper" map in the objects list
    __object_flush_topper(objects_list)

    # returns the list of flatten objects
    return objects_list

def __object_flatten_to_one(base_object, object, flattening_map):
    # iterates over all the keys and values
    # in the flattening map structure
    for key, value in flattening_map.items():
        # retrieves the value type
        value_type = type(value)

        # retrieves the object value and type
        object_value = getattr(object, key)
        object_value_type = type(object_value)

        # in case the value if of type string
        # (a leaf of the flattening structure)
        if value_type == types.StringType:
            # sets the leaf value in the base object
            setattr(base_object, value, object_value)
        # in case the value is of type dictionary
        # and the object value type is an instance
        # (defined to one relation)
        elif value_type == types.DictionaryType and object_value_type == types.InstanceType:
            # "flattens" the to one object relation (recursion)
            __object_flatten_to_one(base_object, object_value, value)

def __object_flatten_to_one_map(base_map, object, flattening_map):
    # iterates over all the keys and values
    # in the flattening map structure
    for key, value in flattening_map.items():
        # retrieves the value type
        value_type = type(value)

        # retrieves the object value and type
        object_value = getattr(object, key)
        object_value_type = type(object_value)

        # in case the value if of type string
        # (a leaf of the flattening structure)
        if value_type == types.StringType:
            # sets the leaf value in the base map
            base_map[value] = object_value
        # in case the value is of type dictionary
        # and the object value type is an instance
        # (defined to one relation)
        elif value_type == types.DictionaryType and object_value_type == types.InstanceType:
            # "flattens" the to one object relation (recursion)
            __object_flatten_to_one_map(base_map, object_value, value)

def __object_flatten_to_many(objects_list, flattening_map):
    # creates the new objects list
    new_objects_list = []

    # iterates over all the object in the objects
    # list to process the to many relations
    for object in objects_list:
        # creates a new (initial bucket)
        # with only the initial object
        bucket = [object]

        # retrieves all the attribute names for the object
        attribute_names = dir(object)

        # retrieves all the to many attribute names of the object based
        # on the type being a list type (tuple or list)
        to_many_attribute_names = [attribute_name for attribute_name in attribute_names if type(getattr(object, attribute_name)) in LIST_TYPES]

        # iterates over all the "to many" attributes
        # to process the relations
        for to_many_attribute_name in to_many_attribute_names:
            # retrieves the to many attribute
            to_many_attribute = getattr(object, to_many_attribute_name)

            # retrieves the (new) flattening map for the to many
            # attribute
            _flattening_map = flattening_map.get(to_many_attribute_name, {})

            # flattens the to many attribute (list) and retrieves the list
            # of to many objects list
            to_many_objects_list = __object_flatten_to_many(to_many_attribute, _flattening_map)

            # calculates the new bucket (list) based on the product
            # of the bucket against the to many objects list, this product
            # is made with the "help" of the new flattening map
            bucket = __object_flatten_product(bucket, to_many_objects_list, _flattening_map)

        # extends the new objects list with the bucket for
        # the current object
        new_objects_list.extend(bucket)

    # returns the new objects list
    return new_objects_list

def __object_flush_topper(objects_list):
    """
    Flushes (clears) the temporary "topper"
    map in all the objects in the given list.

    @type objects_list: List
    @param objects_list: The list of objects to have
    the "topper" map cleared.
    """

    # iterates over all the objects in the
    # objects list (to clear the "topper" map)
    for object in objects_list:
        # in case the object does not
        # contain the topper map
        if not hasattr(object, TOPPER_VALUE):
            # continues th loop
            continue

        # retrieves the "topper" map for
        # the current object
        _topper = object._topper

        # iterates over all the "topper" map
        # items (to set them in the object)
        for key, value in _topper.items():
            # sets the item in the object
            setattr(object, key, value)

        # deletes the (temporary) "topper"
        # map value
        delattr(object, TOPPER_VALUE)

def __object_flatten_product(first_list, second_list, _flattening_map):
    # creates the initial product list
    product_list = []

    # iterates over all the items in
    # the first list
    for first_item in first_list:
        # iterates over all the items
        # in the second list
        for second_item in second_list:
            # creates a clone of an item
            # from the first (base) list
            new_item = copy.copy(first_item)

            # in case the second item contains
            # the "topper" attribute
            if hasattr(second_item, TOPPER_VALUE):
                # retrieves the "topper" attribute
                # from the second item
                _topper = second_item._topper
            # otherwise it's a leaf node and a "topper"
            # map must be created
            else:
                # creates a new "topper" map
                _topper = {}

            # flattens the to one relations in the second item
            # and puts them in the topper map
            __object_flatten_to_one_map(_topper, second_item, _flattening_map)

            # sets the "topper" map in the new item
            new_item._topper = _topper

            # adds the new item to the product
            # list
            product_list.append(new_item)

    # returns the (object) product
    # list (result of multiplication)
    return product_list
