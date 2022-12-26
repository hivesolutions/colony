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

import colony

class DecimalTest(colony.ColonyTestCase):
    """
    Class that tests the decimal (fixed point) data structure
    so that it ensured to be conformant with required operations.
    """

    def test_basic(self):
        """
        Runs a series of basic sanity tests for the decimal
        data structure.
        """

        result = +colony.Decimal(12.2)
        self.assertEqual(result, +12.2)
        self.assertEqual(type(result), colony.Decimal)

        result = -colony.Decimal(12.2)
        self.assertEqual(result, -12.2)
        self.assertEqual(type(result), colony.Decimal)

        result = abs(colony.Decimal(-12.2))
        self.assertEqual(result, 12.2)
        self.assertEqual(type(result), colony.Decimal)

        result = round(colony.Decimal(88.151), 2)
        self.assertEqual(result, 88.15)
        self.assertEqual(type(result), colony.Decimal)

    def test_arithmetic(self):
        """
        Tests a series of arithmetic operations around the
        decimal data structure (critical operations).
        """

        result = colony.Decimal(12.2) * 34.23
        self.assertEqual(result, 417.606)

        result = colony.Decimal(12687.23) * 34.132
        self.assertEqual(result, 433040.53436)

        result = colony.Decimal(532687.23) * 4534.23
        self.assertEqual(result, 2415326418.8829)

        result = 12.2 * 34.23
        self.assertNotEqual(result, 417.606)

        result = colony.Decimal(88.151) - 88.15
        self.assertEqual(result, 0.001)

        result = 88.151 - 88.15
        self.assertNotEqual(result, 0.001)

        result = colony.Decimal(888888888.151) - 88.55
        self.assertEqual(result, 888888799.601)

        result = 888888888.151 - 88.55
        self.assertNotEqual(result, 888888799.601)

        result = colony.Decimal(88.151) - 823.35
        self.assertEqual(result, -735.199)

        result = 88.151 - 823.35
        self.assertNotEqual(result, -735.199)

        result = colony.Decimal(88.151) - 823.35
        self.assertEqual(type(result), colony.Decimal)

        result = 88.151 - 823.35
        self.assertEqual(type(result), float)

        result = colony.Decimal(1.55)
        self.assertEqual(result, 1.55)

        result = colony.Decimal(9999999999.155555555555555555)
        self.assertEqual(result, 9999999999.15555555555555555)

        result = colony.Decimal(88.151) / 1
        self.assertEqual(result, 88.151)
        self.assertEqual(type(result), colony.Decimal)

        result = sum([colony.Decimal(88.151)])
        self.assertEqual(result, 88.151)
        self.assertEqual(type(result), colony.Decimal)

        result = 88 - colony.Decimal(88.15)
        self.assertEqual(result, -0.15)
        self.assertEqual(type(result), colony.Decimal)

        result = 88.151 - colony.Decimal(88.15)
        self.assertEqual(result, 0.001)
        self.assertEqual(type(result), colony.Decimal)

        result = colony.Decimal(3348.5) * colony.Decimal(0.23)
        self.assertEqual(result, 770.155)
        self.assertEqual(type(result), colony.Decimal)

        result = colony.rounds(result, 2)
        self.assertEqual(result, 770.16)
        self.assertEqual(type(result), colony.Decimal)

    def test_boolean(self):
        """
        Runs a series of tests on the boolean based operators
        defined for the decimal data structure.
        """

        result = colony.Decimal(12.2) and 12.2
        self.assertEqual(result, 12.2)
        self.assertEqual(type(result), float)

        result = 12.2 and colony.Decimal(12.2)
        self.assertEqual(result, colony.Decimal(12.2))
        self.assertEqual(type(result), colony.Decimal)

        result = colony.Decimal(12.2) or 12
        self.assertEqual(result, colony.Decimal(12.2))
        self.assertEqual(type(result), colony.Decimal)

    def test_operations(self):
        """
        Runs a series of general operations testing for the
        decimal data structure.
        """

        key = colony.Decimal(88.151) - 88.15
        self.assertEqual(type(key), colony.Decimal)

        map = dict()
        map[key] = "value"
        result = map[key]
        self.assertEqual(result, "value")

    def test_coercing(self):
        """
        Runs a series of coercing tests for the decimal data
        type conversion to other types and vice-versa
        """

        result = int(colony.Decimal(12.2))
        self.assertEqual(result, 12)
        self.assertEqual(type(result), int)

        result = int(colony.Decimal(12.99))
        self.assertEqual(result, 12)
        self.assertEqual(type(result), int)

        result = float(colony.Decimal(12.99))
        self.assertEqual(result, 12.99)
        self.assertEqual(type(result), float)

        result = str(colony.Decimal(12.99))
        self.assertEqual(result, "12.99")
        self.assertEqual(type(result), str)

        result = colony.Decimal(int(12))
        self.assertEqual(result, 12.0)
        self.assertEqual(type(result), colony.Decimal)

        result = colony.Decimal(float(12.99))
        self.assertEqual(result, 12.99)
        self.assertEqual(type(result), colony.Decimal)

        result = colony.Decimal("12.99")
        self.assertEqual(result, 12.99)
        self.assertEqual(type(result), colony.Decimal)

class JournaledListTest(colony.ColonyTestCase):
    """
    Class that tests the journaled list structure.
    """

    def test_append(self):
        """
        Tests the append method of the journaled list.
        """

        # creates a journaled list with elements from an existent
        # list and then adds some extra elements (that are going to
        # be journalized) to test the appending of them
        journaled_list = colony.JournaledList([1, 2, 3])
        journaled_list.append(4)
        journaled_list.append(5)
        journaled_list.append(6)

        # retrieves the list of appends and tests it
        # against the appended values
        appends = journaled_list.get_appends()
        self.assertEqual(appends, [4, 5, 6])

        # appends one extra value to the list
        # and re-tests the appends list
        journaled_list.append(4)
        self.assertEqual(appends, [4, 5, 6, 4])

        # verifies that the contents of the journaled list
        # are the expected ones
        self.assertEqual(journaled_list, [1, 2, 3, 4, 5, 6, 4])

        # retrieves the removes list, that must be empty and
        # tests it against an empty list
        removes = journaled_list.get_removes()
        self.assertEqual(removes, [])

    def test_remove(self):
        """
        Tests the remove method of the journaled list.
        """

        # creates a journaled list with elements from an existent
        # list and then adds some extra elements (that are going to
        # be journalized) to test the removal of them
        journaled_list = colony.JournaledList([1, 2, 3])
        journaled_list.remove(1)
        journaled_list.remove(2)
        journaled_list.remove(3)

        # retrieves the list of removes and tests it
        # against the appended values
        removes = journaled_list.get_removes()
        self.assertEqual(removes, [1, 2, 3])

        # tries to remove the first element one more time
        # (this should raise a value error, and the removes
        # list should remain the same)
        self.assert_raises(ValueError, journaled_list.remove, 1)
        self.assertEqual(removes, [1, 2, 3])

        # verifies that the contents of the journaled list
        # are now empty
        self.assertEqual(journaled_list, [])

        # retrieves the appends list, that must be empty and
        # tests it against an empty list
        appends = journaled_list.get_appends()
        self.assertEqual(appends, [])

    def test_overriding(self):
        """
        Tests the overriding of remove over append operation and
        the reverse.
        """

        # creates a journaled list with elements from an existent
        # list and then adds (and removes) some extra elements (that are going to
        # be journalized) to test the overriding of them
        journaled_list = colony.JournaledList([1, 2, 3])
        journaled_list.append(1)
        journaled_list.append(1)
        journaled_list.remove(1)

        # retrieves the list of appends and tests it
        # against the expected values
        appends = journaled_list.get_appends()
        self.assertEqual(appends, [1])

        # retrieves the list of removes and tests it
        # against the expected values
        removes = journaled_list.get_removes()
        self.assertEqual(removes, [])

        # removes one value and tests the appends
        # and removes list (again)
        journaled_list.remove(1)
        self.assertEqual(appends, [])
        self.assertEqual(removes, [])

        # removes one value and tests the appends
        # and removes list (again)
        journaled_list.remove(1)
        self.assertEqual(appends, [])
        self.assertEqual(removes, [1])

        # appends two values and tests the appends
        # and removes list (again)
        journaled_list.append(1)
        journaled_list.append(1)
        self.assertEqual(appends, [1])
        self.assertEqual(removes, [])

    def test_clear_jounal(self):
        """
        Tests the clear journal method of the journaled list.
        """

        # creates a journaled list with elements from an existent
        # list and then adds and removes some extra elements (that are going to
        # be journalized) to test the appending and removal of them
        journaled_list = colony.JournaledList([1, 2, 3])
        journaled_list.append(1)
        journaled_list.remove(2)
        journaled_list.remove(3)

        # retrieves the list of appends and tests it
        # against the expected values
        appends = journaled_list.get_appends()
        self.assertEqual(appends, [1])

        # retrieves the list of removes and tests it
        # against the expected values
        removes = journaled_list.get_removes()
        self.assertEqual(removes, [2, 3])

        # verifies that the journaled list contains
        # the expected values
        self.assertEqual(journaled_list, [1, 1])

        # clears the journal and verifies that both
        # the appends and removes lists are now empty
        journaled_list.clear_jounal()
        self.assertEqual(appends, [])
        self.assertEqual(removes, [])

        # verifies that the journaled list remains unmodified
        self.assertEqual(journaled_list, [1, 1])

    def test__append(self):
        """
        Tests the _append method of the journaled list.
        """

        # creates a journaled list with elements from an existent
        # list and then adds some extra elements (that are not going to
        # be journalized) to test the (not jounalized) appending of them
        journaled_list = colony.JournaledList([1, 2, 3])
        journaled_list._append(4)
        journaled_list._append(5)
        journaled_list._append(6)

        # retrieves the list of appends and tests it
        # against the empty list (not jounalized)
        appends = journaled_list.get_appends()
        self.assertEqual(appends, [])

        # appends one extra value to the list
        # and re-tests the appends list
        journaled_list._append(4)
        self.assertEqual(appends, [])

        # verifies that the contents of the journaled list
        # are the expected ones
        self.assertEqual(journaled_list, [1, 2, 3, 4, 5, 6, 4])

        # retrieves the removes list, that must be empty and
        # tests it against an empty list
        removes = journaled_list.get_removes()
        self.assertEqual(removes, [])

    def test__remove(self):
        """
        Tests the _remove method of the journaled list.
        """

        # creates a journaled list with elements from an existent
        # list and then adds some extra elements (that are not going to
        # be journalized) to test the (not jounalized) removal of them
        journaled_list = colony.JournaledList([1, 2, 3])
        journaled_list._remove(1)
        journaled_list._remove(2)
        journaled_list._remove(3)

        # retrieves the list of removes and tests it
        # against the empty list (not jounalized)
        removes = journaled_list.get_removes()
        self.assertEqual(removes, [])

        # tries to remove the first element one more time
        # (this should raise a value error, and the removes
        # list should remain the same)
        self.assert_raises(ValueError, journaled_list._remove, 1)
        self.assertEqual(removes, [])

        # verifies that the contents of the journaled list
        # are empty
        self.assertEqual(journaled_list, [])

        # retrieves the appends list, that must be empty and
        # tests it against an empty list
        appends = journaled_list.get_appends()
        self.assertEqual(appends, [])

class OrderedMapTest(colony.ColonyTestCase):
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
