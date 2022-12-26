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

        result = colony.roundi(1171.735, 2)
        self.assertNotEqual(result, 1171.74)

        result = colony.roundi(99999999.995, 2)
        self.assertEqual(result, 100000000.0)

        result = colony.roundi(999999999999999999999999999.9944444444444444444444, 2)
        if is_new: self.assertEqual(result, 999999999999999999999999999.99)

        result = colony.roundi(999999999999999999999999999.995, 2)
        if is_new: self.assertEqual(result, 1000000000000000000000000000.0)

        result = colony.roundi(770.155, 2)
        if is_new: self.assertEqual(result, 770.15)
        else: self.assertEqual(result, 770.16)

    def test_rounds(self):
        is_new = colony.round_is_new()

        result = colony.rounds(2.675, 2)
        self.assertEqual(result, 2.68)

        result = colony.rounds(2.685, 2)
        self.assertEqual(result, 2.69)

        result = colony.rounds(2.68, 2)
        self.assertEqual(result, 2.68)

        result = colony.rounds(2.683, 2)
        self.assertEqual(result, 2.68)

        result = colony.rounds(2.689, 2)
        self.assertEqual(result, 2.69)

        result = colony.rounds(2.695, 2)
        self.assertEqual(result, 2.70)

        result = colony.rounds(2.999, 2)
        self.assertEqual(result, 3.0)

        result = colony.rounds(2.945, 2)
        self.assertEqual(result, 2.95)

        result = colony.rounds(2.9444, 2)
        self.assertEqual(result, 2.94)

        result = colony.rounds(2.9444444444444444444444, 2)
        self.assertEqual(result, 2.94)

        result = colony.rounds(2.9944444444444444444444, 2)
        self.assertEqual(result, 2.99)

        result = colony.rounds(2.995, 2)
        self.assertEqual(result, 3.0)

        result = colony.rounds(1171.735, 2)
        self.assertEqual(result, 1171.74)

        result = colony.rounds(99999999.995, 2)
        self.assertEqual(result, 100000000.0)

        result = colony.rounds(999999999999999999999999999.9944444444444444444444, 2)
        if is_new: self.assertEqual(result, 999999999999999999999999999.99)

        result = colony.rounds(999999999999999999999999999.995, 2)
        if is_new: self.assertEqual(result, 1000000000000000000000000000.0)

        result = colony.rounds(770.155, 2)
        self.assertEqual(result, 770.16)

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
