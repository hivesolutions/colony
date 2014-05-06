#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class JournaledListTest(colony.ColonyTestCase):
    """
    Class that tests the journaled list structure.
    """

    def test_append(self):
        """
        Tests the append method of the journaled list.
        """

        # creates a jounaled list with elements from an existent
        # list and then adds some extra elements (that are going to
        # be journalized) to test the appending of them
        jounaled_list = colony.JournaledList([1, 2, 3])
        jounaled_list.append(4)
        jounaled_list.append(5)
        jounaled_list.append(6)

        # retrieves the list of appends and tests it
        # against the appended values
        appends = jounaled_list.get_appends()
        self.assertEqual(appends, [4, 5, 6])

        # appends one extra value to the list
        # and re-tests the appends list
        jounaled_list.append(4)
        self.assertEqual(appends, [4, 5, 6, 4])

        # verifies that the contents of the jounaled list
        # are the expected ones
        self.assertEqual(jounaled_list, [1, 2, 3, 4, 5, 6, 4])

        # retrieves the removes list, that must be empty and
        # tests it against an empty list
        removes = jounaled_list.get_removes()
        self.assertEqual(removes, [])

    def test_remove(self):
        """
        Tests the remove method of the journaled list.
        """

        # creates a jounaled list with elements from an existent
        # list and then adds some extra elements (that are going to
        # be journalized) to test the removal of them
        jounaled_list = colony.JournaledList([1, 2, 3])
        jounaled_list.remove(1)
        jounaled_list.remove(2)
        jounaled_list.remove(3)

        # retrieves the list of removes and tests it
        # against the appended values
        removes = jounaled_list.get_removes()
        self.assertEqual(removes, [1, 2, 3])

        # tries to remove the first element one more time
        # (this should raise a value error, and the removes
        # list should remain the same)
        self.assert_raises(ValueError, jounaled_list.remove, 1)
        self.assertEqual(removes, [1, 2, 3])

        # verifies that the contents of the jounaled list
        # are now empty
        self.assertEqual(jounaled_list, [])

        # retrieves the appends list, that must be empty and
        # tests it against an empty list
        appends = jounaled_list.get_appends()
        self.assertEqual(appends, [])

    def test_overriding(self):
        """
        Tests the overriding of remove over append operation and
        the reverse.
        """

        # creates a jounaled list with elements from an existent
        # list and then adds (and removes) some extra elements (that are going to
        # be journalized) to test the overriding of them
        jounaled_list = colony.JournaledList([1, 2, 3])
        jounaled_list.append(1)
        jounaled_list.append(1)
        jounaled_list.remove(1)

        # retrieves the list of appends and tests it
        # against the expected values
        appends = jounaled_list.get_appends()
        self.assertEqual(appends, [1])

        # retrieves the list of removes and tests it
        # against the expected values
        removes = jounaled_list.get_removes()
        self.assertEqual(removes, [])

        # removes one value and tests the appends
        # and removes list (again)
        jounaled_list.remove(1)
        self.assertEqual(appends, [])
        self.assertEqual(removes, [])

        # removes one value and tests the appends
        # and removes list (again)
        jounaled_list.remove(1)
        self.assertEqual(appends, [])
        self.assertEqual(removes, [1])

        # appends two values and tests the appends
        # and removes list (again)
        jounaled_list.append(1)
        jounaled_list.append(1)
        self.assertEqual(appends, [1])
        self.assertEqual(removes, [])

    def test_clear_jounal(self):
        """
        Tests the clear journal method of the journaled list.
        """

        # creates a jounaled list with elements from an existent
        # list and then adds and removes some extra elements (that are going to
        # be journalized) to test the appending and removal of them
        jounaled_list = colony.JournaledList([1, 2, 3])
        jounaled_list.append(1)
        jounaled_list.remove(2)
        jounaled_list.remove(3)

        # retrieves the list of appends and tests it
        # against the expected values
        appends = jounaled_list.get_appends()
        self.assertEqual(appends, [1])

        # retrieves the list of removes and tests it
        # against the expected values
        removes = jounaled_list.get_removes()
        self.assertEqual(removes, [2, 3])

        # verifies that the journaled list contains
        # the expected values
        self.assertEqual(jounaled_list, [1, 1])

        # clears the journal and verifies that both
        # the appends and removes lists are now empty
        jounaled_list.clear_jounal()
        self.assertEqual(appends, [])
        self.assertEqual(removes, [])

        # verifies that the journaled list remains unmodified
        self.assertEqual(jounaled_list, [1, 1])

    def test__append(self):
        """
        Tests the _append method of the journaled list.
        """

        # creates a jounaled list with elements from an existent
        # list and then adds some extra elements (that are not going to
        # be journalized) to test the (not jounalized) appending of them
        jounaled_list = colony.JournaledList([1, 2, 3])
        jounaled_list._append(4)
        jounaled_list._append(5)
        jounaled_list._append(6)

        # retrieves the list of appends and tests it
        # against the empty list (not jounalized)
        appends = jounaled_list.get_appends()
        self.assertEqual(appends, [])

        # appends one extra value to the list
        # and re-tests the appends list
        jounaled_list._append(4)
        self.assertEqual(appends, [])

        # verifies that the contents of the jounaled list
        # are the expected ones
        self.assertEqual(jounaled_list, [1, 2, 3, 4, 5, 6, 4])

        # retrieves the removes list, that must be empty and
        # tests it against an empty list
        removes = jounaled_list.get_removes()
        self.assertEqual(removes, [])

    def test__remove(self):
        """
        Tests the _remove method of the journaled list.
        """

        # creates a jounaled list with elements from an existent
        # list and then adds some extra elements (that are not going to
        # be journalized) to test the (not jounalized) removal of them
        jounaled_list = colony.JournaledList([1, 2, 3])
        jounaled_list._remove(1)
        jounaled_list._remove(2)
        jounaled_list._remove(3)

        # retrieves the list of removes and tests it
        # against the empty list (not jounalized)
        removes = jounaled_list.get_removes()
        self.assertEqual(removes, [])

        # tries to remove the first element one more time
        # (this should raise a value error, and the removes
        # list should remain the same)
        self.assert_raises(ValueError, jounaled_list._remove, 1)
        self.assertEqual(removes, [])

        # verifies that the contents of the jounaled list
        # are empty
        self.assertEqual(jounaled_list, [])

        # retrieves the appends list, that must be empty and
        # tests it against an empty list
        appends = jounaled_list.get_appends()
        self.assertEqual(appends, [])

class OrderedMap(colony.ColonyTestCase):
    """
    Class that tests the ordered map structure.
    """

    def test_order(self):
        """
        Tests that the order of item assignment is respected
        in the ordered map structure.
        """

        # creates an ordered map structures with a previously
        # defined sequence of setting of values, to be used
        # to after verify that they are set in the correct
        # order of appearance (test structure)
        ordered_map = colony.OrderedMap()
        ordered_map["1"] = 1
        ordered_map["2"] = 2
        ordered_map["3"] = 3

        # starts the index counter to be used during
        # the iteration part of the test
        index = 0

        # iterates over all the keys in the ordered
        # map to make sure order remains
        for key in ordered_map:
            # verifies that the correct values are found
            # for each of the iteration cycles according
            # to the previously defined map order
            if index == 0: self.assertEqual(key, "1")
            elif index == 1: self.assertEqual(key, "2")
            elif index == 1: self.assertEqual(key, "3")

            # increments the index counter
            # (new iteration)
            index += 1
