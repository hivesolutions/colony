#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class LazyClassTest(colony.ColonyTestCase):
    """
    Class that tests the lazy loading mechanisms.
    """

    def test_equals(self):
        """
        Tests the "equals" value function.
        """

        # verifies that the global lazy reference is
        # "equivalent" to a null reference
        self.assertEqual(colony.Lazy, None)

        # creates a new lazy class instance to check the
        # comparisons against it
        lazy = colony.LazyClass()

        # verifies that the new instance is equivalent to
        # a null object, itself and the global lazy reference
        self.assertEqual(lazy, None)
        self.assertEqual(lazy, lazy)
        self.assertEqual(lazy, colony.Lazy)
