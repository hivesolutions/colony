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

GLOBALS_REFERENCE_VALUE = "_globals"
""" The globals reference value """

LOCALS_REFERENCE_VALUE = "_locals"
""" The locals reference value """

def __importer__(module_name):
    """
    Importer function to be used in the process of importing
    a module referred in inverted way.
    This function should be used in cases where the inversion injection
    was made using the data helper.

    @type module_name: String
    @param module_name: The name of the module to be imported.
    @rtype: Module
    @return: The imported module.
    """

    # retrieves the caller of the importer method
    caller = sys._getframe(1)

    # in case the module name exists in the globals map
    # of the caller
    if module_name in caller.f_globals[GLOBALS_REFERENCE_VALUE]:
        # retrieves the module from the globals map of the caller
        module = caller.f_globals[GLOBALS_REFERENCE_VALUE][module_name]
    # in case the module name exists in the locals map
    # of the caller
    elif module_name in caller.f_globals[LOCALS_REFERENCE_VALUE]:
        # retrieves the module from the locals map of the caller
        module = caller.f_globals[LOCALS_REFERENCE_VALUE][module_name]

    # returns the module
    return module
