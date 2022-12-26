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

class NumberTest(colony.ColonyTestCase):
    """
    Class that tests the number various functions method.
    """

    def test_to_fixed(self):
        """
        Tests the to fixed function.
        """

        # creates the the same value using an "infinite"
        # (repeating decimal) approach (through the 0.33)
        # and using the final and fixed value, this will create
        # problems in a normal float comparison
        infinite_float_value = 0.33 + 0.11 - 0.09 - 0.33
        correct_float_value = 0.02

        # verifies that the "infinite" (repeating decimal) based
        # float number is not the same as the non "infinite" based
        # number in a normal based float comparison
        self.assertNotEqual(infinite_float_value, correct_float_value)

        # converts both values into the fixed representation to test them
        # into a fixed based comparison, that must be valid
        infinite_fixed_value = colony.to_fixed(infinite_float_value, 2)
        correct_fixed_value = colony.to_fixed(correct_float_value, 2)

        # verifies that the comparison of the fixed based values should
        # be valid (this time the comparison takes no side effects)
        self.assertEqual(infinite_fixed_value, correct_fixed_value)
