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

def list_intersect(first_list, second_list):
    """
    Intersects the given lists, returning a list with
    the elements contained in both lists.

    :type first_list: List
    :param first_list: The first list to be used in intersection.
    :type second_list: List
    :param second_list: The second list to be used in intersection.
    :rtype: List
    :return: The list containing the elements contained
    in both lists (intersection).
    """

    # returns the intersection resulting list
    return [value for value in first_list if value in second_list]

def list_extend(base_list, extension_list, copy_base_list = True):
    """
    Extends the list with the the extension list,
    returning a list resulting of the merge of both list.

    Duplicates are avoided to remove additional elements.
    The base list may be changed or left untouched based on
    the copy base list flag.

    :type base_list: List
    :param base_list: The list to be used as base for
    the merge.
    :type extension_list: List
    :param extension_list: The list to be used to extend the base
    one.
    :type copy_base_list: bool
    :param copy_base_list: If the base list should be copied before
    being extended in order to avoid loss of data.
    :rtype: List
    :return: The list that result of the merge of both lists.
    """

    # copies the base list to create the initial result list (optional)
    result_list = copy_base_list and copy.copy(base_list) or base_list

    # creates the list of values that are "new" to the base
    # list (in order to avoid duplicates)
    filtered_list = [value for value in extension_list if not value in base_list]

    # extends the result list with the filtered list (new elements)
    result_list.extend(filtered_list)

    # returns the result list
    return result_list

def list_exclude(base_list, exclusion_list, copy_base_list = True):
    """
    Excludes a series of items from the given base list,
    the resulting list (without the items) is returned.
    The base list may be changed or left untouched based on
    the copy base list flag.

    :type base_list: List
    :param base_list: The list to be used as base for
    the exclusion.
    :type exclusion_list: List
    :param exclusion_list: The list to be used as model for
    the exclusion of items
    :type copy_base_list: bool
    :param copy_base_list: If the base list should be copied before
    the exclusion process in order to avoid loss of data.
    :rtype: List
    :return: The list that result of the exclusion of the given
    list from the provided base list.
    """

    # copies the base list to create the initial result list (optional)
    result_list = copy_base_list and copy.copy(base_list) or base_list

    # iterates over all the items in the exclusion list
    # to remove them from the "result" list
    for exclusion_item in exclusion_list:
        # removes the exclusion item from  the result list
        result_list.remove(exclusion_item)

    # returns the result list
    return result_list

def list_no_duplicates(list):
    """
    Removes the duplicated values from the given list.
    This method is expensive and should be used carefully.

    :type list: List
    :param list: The list to heave it's duplicates removed.
    :rtype: List
    :return: The list with the duplicates removed.
    """

    # creates the initial result list to hold the results
    result_list = []

    # iterates over all the values in the list
    for value in list:
        # in case the value already exists
        # in the result list (duplicate)
        if value in result_list:
            # continues the loop
            continue

        # adds the value to the result list
        result_list.append(value)

    # returns the result list
    return result_list
