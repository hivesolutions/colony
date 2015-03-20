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

class RoundTest(colony.ColonyTestCase):
    """
    Test case bundle aimed at verifying the integrity of the
    round associated functions.
    """

    def test_legacy(self):
        is_new = colony.round_is_new()

        result = round(2.675, 2)
        self.assertEqual(result, 2.67 if is_new else 2.68)

        result = round(2.685, 2)
        self.assertEqual(result, 2.69)

    def test_roundi(self):
        is_new = colony.round_is_new()

        result = colony.roundi(2.675, 2)
        self.assertEqual(result, 2.68)

        result = colony.roundi(2.685, 2)
        self.assertEqual(result, 2.69)

        result = colony.roundi(2.68, 2)
        self.assertEqual(result, 2.68)

        result = colony.roundi(2.683, 2)
        self.assertEqual(result, 2.68)

        result = colony.roundi(2.689, 2)
        self.assertEqual(result, 2.69)

        result = colony.roundi(2.695, 2)
        self.assertEqual(result, 2.70)

        result = colony.roundi(2.999, 2)
        self.assertEqual(result, 3.0)

        result = colony.roundi(2.945, 2)
        self.assertEqual(result, 2.95)

        result = colony.roundi(2.9444, 2)
        self.assertEqual(result, 2.94)

        result = colony.roundi(2.9444444444444444444444, 2)
        self.assertEqual(result, 2.94)

        result = colony.roundi(2.9944444444444444444444, 2)
        self.assertEqual(result, 2.99)

        result = colony.roundi(2.995, 2)
        self.assertEqual(result, 3.0)

        result = colony.roundi(99999999.995, 2)
        self.assertEqual(result, 100000000.0)

        result = colony.roundi(999999999999999999999999999.9944444444444444444444, 2)
        is_new and self.assertEqual(result, 999999999999999999999999999.99)

        result = colony.roundi(999999999999999999999999999.995, 2)
        is_new and self.assertEqual(result, 1000000000000000000000000000.0)

    def test_roundt(self):
        result = colony.roundt(2.675, 2)
        self.assertEqual(type(result), float)

        result = colony.roundt(colony.Decimal(2.675), 2)
        self.assertEqual(type(result), colony.Decimal)

        result = colony.roundt(2, 2)
        self.assertEqual(type(result), int)

    def test_apply(self):
        colony.round_apply(force = True)
        try:
            self.assertEqual(round, colony.roundi)
            result = round(2.675, 2)
            self.assertEqual(result, 2.68)
        finally:
            colony.round_unapply()

    def test_unapply(self):
        _round = round
        colony.round_apply(force = True)
        try: self.assertEqual(round, colony.roundi)
        finally: colony.round_unapply()
        self.assertEqual(round, _round)
