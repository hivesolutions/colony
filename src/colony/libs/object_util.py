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

import copy

from colony.base import legacy

NOT_SET_VALUE = None
""" The value to be set when the value is not set (defined) """

TOPPER_VALUE = "_topper"
""" The value of the attribute to hold the top values """

LIST_TYPES = (list, tuple)
""" A tuple with the various list types """

INVALID_ATTRIBUTE_NAMES = ("__doc__", "__module__")
""" The set of invalid attribute names (for printing) """

VALID_ATTRIBUTE_TYPES = (
    int,
    legacy.LONG,
    float,
    bool,
    str,
    legacy.UNICODE,
    type(None)
)
""" The set of valid attribute types (for printing) """

def object_attribute_names(instance):
    """
    Function that retrieves the valid attribute
    names for printing.
    A valid attribute is considered to be an attribute
    that may have it's value ready for printing.

    :type instance: Object
    :param instance: The instance to retrieve the (valid)
    attribute names.
    :rtype: List
    :return: The valid attribute names according to the
    the state for printing the value.
    """

    # filters the attribute names based on the type and value
    # of them (non printable attributes are filtered out)
    valid_attribute_names = [key for key, value in __object_items(instance) if type(value) in VALID_ATTRIBUTE_TYPES]

    # returns the valid attribute names (ready for print)
    return valid_attribute_names

def object_attribute_values(instance, valid_attribute_names = None, strict = True):
    """
    Function that retrieves the valid attribute
    values for printing.

    A valid attribute is considered to be an attribute
    that may have it's value ready for printing.

    A non strict mode is possible to be used where in
    case an attribute is not found the value is set
    as not valid (invalid value).

    :type instance: Object
    :param instance: The instance to retrieve the (valid)
    attribute values.
    :type valid_attribute_names: List
    :param valid_attribute_names: List of valid attribute
    names that may be used to retrieve valid attribute values.
    :type strict: bool
    :param strict: If a strict based strategy should be used
    for the retrieval of the object attributes, meaning that
    an exception is raised in case the attribute does not exist.
    :rtype: List
    :return: The valid attribute value according to the
    the state for printing the value.
    """

    # retrieves the valid attribute names in order
    # to use them to retrieve the valid attribute values
    valid_attribute_names = valid_attribute_names or object_attribute_names(instance)
    valid_attribute_values = [__object_get_attr(instance, value, strict = strict) for value in valid_attribute_names]

    # returns the valid attribute values (ready for print)
    return valid_attribute_values

def object_flatten(instance, flattening_map):
    """
    Flattens the given instance using the given flattening
    map as reference for the flattening process.

    :type instance: Object
    :param instance: The instance to be flatten.
    :type flattening_map: Dictionary
    :param flattening_map: Map describing the structure
    for flattening.
    """

    # retrieves the type of the instance
    instance_type = type(instance)

    # in case the type of instance is (just) map (dictionary)
    # the instance should be encloses in a sequence object
    if instance_type == dict:
        # converts the instance to a list
        # (in order to be able to work with it)
        instance = [instance]
    # in case the instance is neither an instance
    # nor a list
    elif not instance_type in LIST_TYPES:
        # raises a runtime error (no valid instance type)
        raise RuntimeError("Invalid instance type")

    # flattens the structure of the instance (list)
    # using the flattening map (the returned structure
    # is a list of "flatten" instances)
    flatten_list = _object_flatten(instance, flattening_map)

    # returns the flatten list
    return flatten_list

def object_print_list(instances_list):
    """
    Prints some information on the objects
    in the given list, for debugging purposes.

    :type instances_list: List
    :param instances_list: The list of instances
    to be printed for debugging.
    """

    # iterates over all the instances
    # in the instances list to print them
    for instance in instances_list:
        # prints the debug information on
        # the instance
        object_print(instance)

        # prints a blank line
        print("")

def object_print(instance):
    """
    Prints some debug information on the
    instance, for debugging purposes.

    :type instance: Object
    :param instance: The instance to be printed
    for debugging.
    """

    # retrieves the list of all the attribute names
    # for the instance
    attribute_names = __object_keys(instance)

    # iterates over all the attribute names of the instance
    # (filters the invalid ones)
    for attribute_name in attribute_names:
        # retrieves the attribute and the name
        # of the attribute from the instance
        attribute = __object_get_attr(instance, attribute_name)
        attribute_type = type(attribute)

        # in case the attribute name or the type is invalid
        # must skip the current loop (not required)
        if attribute_name in INVALID_ATTRIBUTE_NAMES: continue
        if not attribute_type in VALID_ATTRIBUTE_TYPES: continue

        # prints the attribute name and the attribute value
        print("%s: %s" % (attribute_name, attribute))

def _object_flatten(instances_list, flattening_map):
    """
    Flattens the given instance using the given flattening
    map as reference for the flattening process.
    This function implements the concrete behavior for the
    flattening of an instance.

    :type instance: Object
    :param instance: The instance to be flatten.
    :type flattening_map: Dictionary
    :param flattening_map: Map describing the structure
    for flattening.
    :rtype: List
    :return: The list of instances in the flatten state.
    """

    # iterates over all the "base" instances
    for instance in instances_list:
        # flattens the instance in the to one relations
        # and the attributes (according to the flattening map)
        __object_flatten_to_one(instance, instance, flattening_map)

    # flattens the to many relation in the instances
    # in the given list
    instances_list = __object_flatten_to_many(instances_list, flattening_map)

    # flushes the "topper" map in the instances list
    __object_flush_topper(instances_list)

    # flushes the null elements in the instances list
    __object_flush_null(instances_list)

    # returns the list of flatten instances
    return instances_list

def __object_flatten_to_one(base_instance, instance, flattening_map):
    """
    Auxiliary function that provides the mechanism
    to "map" the "to-one" relations in the instance
    according to the flattening map.

    :type base_instance: Object
    :param base_instance: The base (top level) instance to
    be used to set the top level attributes.
    :type instance: Object
    :param instance: The current concrete instance in the
    recursion set.
    :type flattening_map: Dictionary
    :param flattening_map: Map describing the structure
    for flattening.
    """

    # iterates over all the keys and values
    # in the flattening map structure
    for key, value in legacy.iteritems(flattening_map):
        # retrieves the value type
        value_type = type(value)

        # tries to retrieves the instance value
        # sets the value to invalid in case there
        # is no such instance value (attribute)
        instance_value = __object_has_attr(instance, key) and __object_get_attr(instance, key) or None

        # in case the instance value is not set, must
        # continue the loop (skips the current iteration)
        if instance_value == None: continue

        # in case the value if of type string
        # (a leaf of the flattening structure)
        if value_type == str:
            # sets the leaf value in the base instance
            __object_set_attr(base_instance, value, instance_value)
        # in case the value is of type dictionary
        # (defined to one relation)
        elif value_type == dict:
            # "flattens" the to one instance relation (recursion)
            __object_flatten_to_one(base_instance, instance_value, value)

def __object_flatten_to_one_map(base_map, instance, flattening_map):
    """
    Auxiliary function that provides the mechanism
    to "map" the "to-one" relations in the instance
    according to the flattening map.

    :type base_map: Dictionary
    :param base_map: The base (top level) map to
    be used to set the top level attributes.
    :type instance: Object
    :param instance: The current concrete instance in the
    recursion set.
    :type flattening_map: Dictionary
    :param flattening_map: Map describing the structure
    for flattening.
    """

    # iterates over all the keys and values
    # in the flattening map structure
    for key, value in legacy.iteritems(flattening_map):
        # retrieves the value type
        value_type = type(value)

        # tries to retrieves the instance value
        # sets the value to invalid in case there
        # is no such instance value (attribute)
        instance_value = __object_has_attr(instance, key) and __object_get_attr(instance, key) or None

        # in case the instance value is not set
        if instance_value == None:
            # continues the loop
            continue

        # in case the value if of type string
        # (a leaf of the flattening structure)
        if value_type == str:
            # sets the leaf value in the base map
            base_map[value] = instance_value
        # in case the value is of type dictionary
        # (defined to one relation)
        elif value_type == dict:
            # "flattens" the to one instance relation (recursion)
            __object_flatten_to_one_map(base_map, instance_value, value)

def __object_flatten_to_many(instances_list, flattening_map):
    """
    Auxiliary function that provides the mechanism
    to "map" the "to-many" relations in the instance
    according to the flattening map.

    :type instances_list: List
    :param instances_list: The list of instances to have
    the "to-many" relations mapped.
    :type flattening_map: Dictionary
    :param flattening_map: Map describing the structure
    for flattening.
    :rtype: List
    :return: The resulting list after the "to-many" operations
    that include cartesian product.
    """

    # creates the new instances list
    new_instances_list = []

    # iterates over all the instance in the instances
    # list to process the to many relations
    for instance in instances_list:
        # creates a new (initial bucket)
        # with only the initial instance
        bucket = [instance]

        # retrieves all the attribute names (keys) for the instance
        attribute_names = __object_keys(instance)

        # retrieves all the to many attribute names of the instance based
        # on the type being a list type (tuple or list)
        to_many_attribute_names = [attribute_name for attribute_name in attribute_names if type(__object_get_attr(instance, attribute_name)) in LIST_TYPES]

        # iterates over all the "to many" attributes
        # to process the relations
        for to_many_attribute_name in to_many_attribute_names:
            # retrieves the to many attribute
            to_many_attribute = __object_get_attr(instance, to_many_attribute_name)

            # retrieves the (new) flattening map for the to many
            # attribute
            _flattening_map = flattening_map.get(to_many_attribute_name, {})

            # flattens the to many attribute (list) and retrieves the list
            # of to many instances list
            to_many_intances_list = __object_flatten_to_many(to_many_attribute, _flattening_map)

            # calculates the new bucket (list) based on the product
            # of the bucket against the to many instances list, this product
            # is made with the "help" of the new flattening map
            bucket = __object_flatten_product(bucket, to_many_intances_list, _flattening_map)

        # extends the new instances list with the bucket for
        # the current instance
        new_instances_list.extend(bucket)

    # returns the new instances list
    return new_instances_list

def __object_flush_topper(instances_list):
    """
    Flushes (clears) the temporary "topper"
    map in all the instances in the given list.

    :type instances_list: List
    :param instances_list: The list of instances to have
    the "topper" map cleared.
    """

    # iterates over all the instances in the
    # instances list (to clear the "topper" map)
    for instance in instances_list:
        # in case the instance does not
        # contain the topper map
        if not __object_has_attr(instance, TOPPER_VALUE):
            # continues th loop
            continue

        # retrieves the "topper" map for
        # the current instance
        _topper = __object_get_attr(instance, TOPPER_VALUE)

        # iterates over all the "topper" map
        # items (to set them in the instance)
        for key, value in legacy.iteritems(_topper):
            # sets the item in the instance
            __object_set_attr(instance, key, value)

        # deletes the (temporary) "topper"
        # map value
        __object_del_attr(instance, TOPPER_VALUE)

def __object_flush_null(instances_list):
    """
    Flushes (clears) the elements in the objects
    which don't have any value defined.
    This method allows every object to become uniform
    with the others.

    :type instances_list: List
    :param instances_list: The list of instances to have
    the null values flushed.
    """

    # creates the set of instance keys
    instances_keys = set()

    # iterates over all the instances in the
    # instances list (to clear retrieve the object keys)
    for instance in instances_list:
        # retrieves the keys (names) for the instance
        instance_keys = __object_keys(instance)

        # retrieves the instances keys from the
        # union of the instance keys element
        instances_keys = instances_keys.union(instance_keys)

    # iterates over all the instances in
    # the instance list
    for instance in instances_list:
        # iterates over all the instances keys
        # in the instances keys list
        for instances_key in instances_keys:
            # in case the instance already contains
            # the instances key
            if __object_has_attr(instance, instances_key):
                # continues the loop
                continue

            # sets the object key in the instance
            # as null (none)
            __object_set_attr(instance, instances_key, None)

def __object_flatten_product(first_list, second_list, flattening_map):
    """
    Provides a special case of the cartesian product of
    two sets (in this case lists).
    Both lists are "multiplied" and then using the flattening
    map the second list item is filtered accordingly.

    :type first_list: List
    :param first_list: The first (base) list for the cartesian
    product.
    :type second_list: List
    :param second_list: The second list for the cartesian product.
    :type flattening_map: Dictionary
    :param flattening_map: Map describing the structure
    for flattening.
    :see: http://en.wikipedia.org/wiki/Cartesian_product
    """

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
            if __object_has_attr(second_item, TOPPER_VALUE):
                # retrieves the "topper" attribute
                # from the second item
                _topper = __object_get_attr(second_item, TOPPER_VALUE)
            # otherwise it's a leaf node and a "topper"
            # map must be created
            else:
                # creates a new "topper" map
                _topper = {}

            # flattens the to one relations in the second item
            # and puts them in the topper map
            __object_flatten_to_one_map(_topper, second_item, flattening_map)

            # sets the "topper" map in the new item
            __object_set_attr(new_item, TOPPER_VALUE, _topper)

            # adds the new item to the product
            # list
            product_list.append(new_item)

    # returns the (instance) product
    # list (result of multiplication)
    return product_list

def __object_has_attr(instance, attribute_name):
    """
    Checks if an attribute with the given name
    exists in the given instance.
    This method provides an additional layer of abstraction
    that allows it to be used in objects or in maps.

    :type instance: Object
    :param instance: The instance to be checked
    for attribute.
    :type attribute_name: String
    :param attribute_name: The name of the attribute
    to be checked in the instance.
    :rtype: bool
    :return: The result of the has attribute testing
    in the instance.
    """

    # retrieves the instance type
    instance_type = type(instance)

    # in case the instance type is dictionary
    if instance_type == dict:
        # checks if the attribute name exists in
        # instance (map)
        return attribute_name in instance
    # otherwise the instance is a "normal" instance
    else:
        # calls the normal has attr function
        # in the instance
        return hasattr(instance, attribute_name)

def __object_get_attr(instance, attribute_name, default = None, strict = True):
    """
    Retrieves an attribute with the given name from the
    given instance.

    This method provides an additional layer of abstraction
    that allows it to be used in objects or in maps.

    Note that the strict mode ensures that if the attribute
    is not present an exception is properly raised.

    :type instance: Object
    :param instance: The instance to retrieve the attribute, this
    may be either a dictionary or an object instance.
    :type attribute_name: String
    :param attribute_name: The name of the attribute to be retrieved
    from the instance.
    :type default: Object
    :param default: The default value to be returned in the value is
    not found, this is only used in case the strict mode is not set.
    :type strict: bool
    :param strict: If the strict mode should be used, meaning that
    the attributes must be set under the instance otherwise an exception
    will be raised.
    :rtype: Object
    :return: The retrieved attribute from the instance.
    """

    # retrieves the instance type
    instance_type = type(instance)

    # in case the instance type is dictionary the typical
    # dictionary access operation is used
    if instance_type == dict:
        if strict: return instance[attribute_name]
        else: return instance.get(attribute_name, default)

    # otherwise the instance is a "normal" instance, note
    # that the attribute is first verified for presence
    # in case the non strict mode is currently in use
    else:
        if strict: return getattr(instance, attribute_name)
        elif hasattr(instance, attribute_name):
            return getattr(instance, attribute_name)
        else: return default

def __object_set_attr(instance, attribute_name, attribute):
    """
    Sets an attribute with the given name in the
    given instance.
    This method provides an additional layer of abstraction
    that allows it to be used in objects or in maps.

    :type instance: Object
    :param instance: The instance to retrieve the
    attribute.
    :type attribute_name: String
    :param attribute_name: The name of the attribute
    to be set in the instance.
    :type attribute: Object
    :param attribute: The attribute (value) to be set in
    the instance.
    """

    # retrieves the instance type
    instance_type = type(instance)

    # in case the instance type is dictionary
    if instance_type == dict:
        # sets the attribute using the normal
        # map setter
        instance[attribute_name] = attribute
    # otherwise the instance is a "normal" instance
    else:
        # uses the typical setattr function to set
        # the attribute in the instance
        setattr(instance, attribute_name, attribute)

def __object_del_attr(instance, attribute_name):
    """
    Deletes the attribute with the given name from the
    given instance.
    This method provides an additional layer of abstraction
    that allows it to be used in objects or in maps.

    :type instance: Object
    :param instance: The instance to delete the
    attribute.
    :type attribute_name: String
    :param attribute_name: The name of the attribute
    to be deleted.
    :rtype: Object
    :return: The retrieved attribute from the instance.
    """

    # retrieves the instance type
    instance_type = type(instance)

    # in case the instance type is dictionary
    if instance_type == dict:
        # calls the del operator in the instance
        # map (dictionary)
        del instance[attribute_name]
    # otherwise the instance is a "normal" instance
    else:
        # deletes the attribute from the instance
        # using the delattr function
        delattr(instance, attribute_name)

def __object_keys(instance):
    """
    Retrieves a list with all the instance names (keys),
    from the given instance.
    This method provides an additional layer of abstraction
    that allows it to be used in objects or in maps.

    :type instance: Object
    :param instance: The instance to retrieve the keys
    list (names list).
    """

    # retrieves the instance type
    instance_type = type(instance)

    # in case the instance type is dictionary
    if instance_type == dict:
        # returns the instance (map) keys values
        # using the normal map method
        return legacy.keys(instance)
    # otherwise the instance is a "normal" instance
    else:
        # returns the instance dictionary keys
        # (the instance names)
        return legacy.keys(instance)

def __object_items(instance):
    """
    Retrieves a list with all the instance value and keys (items),
    from the given instance.
    This method provides an additional layer of abstraction
    that allows it to be used in objects or in maps.

    :type instance: Object
    :param instance: The instance to retrieve the values
    and keys list (items list).
    """

    # retrieves the instance type
    instance_type = type(instance)

    # in case the instance type is dictionary
    if instance_type == dict:
        # returns the instance (map) keys values
        # using the normal map method
        return legacy.items(instance)
    # otherwise the instance is a "normal" instance
    else:
        # returns the instance dictionary keys
        # (the instance names)
        return legacy.items(instance.__dict__)
