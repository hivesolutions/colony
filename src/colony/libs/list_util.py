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

def list_intersect(first_list, second_list):
    """
    Intersects the given lists, returning a list with
    the elements contained in both lists.

    @type first_list: List
    @param first_list: The first list to be used in intersection.
    @type second_list: List
    @param second_list: The second list to be used in intersection.
    @rtype: List
    @return: The list containing the elements contained
    in both lists (intersection).
    """

    # returns the intersection resulting list
    return [value for value in first_list if value in second_list]

def list_extend(base_list, extension_list):
    """
    Extends the list with the the extension list,
    retrieving a list resulting of the merge of both list.
    Duplicates are avoided to remove additional elements.

    @type base_list: List
    @param base_list: The list to be used as base for
    the merge.
    @type extension_list: List
    @param extension_list: The list to be used to extend the base
    one.
    @rtype: List
    @return: The list that result of the merge of both lists.
    """

    # creates the list of values that are "new" to the base
    # list (in order to avoid duplicates)
    filtered_list = [value for value in extension_list if not value in base_list]

    # extends the base list with the filtered list (new elements)
    base_list.extend(filtered_list)

    # returns the "new" base list
    return base_list
