#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony


class SizeTest(colony.ColonyTestCase):
    """
    Class that tests the utility functions that
    are associated with size and strings.
    """

    def test_size_round_unit(self):
        result = colony.size_round_unit(256)
        self.assertEqual(result, "256B")

        result = colony.size_round_unit(1024)
        self.assertEqual(result, "1KB")

        result = colony.size_round_unit(1024 * 1024)
        self.assertEqual(result, "1MB")

        result = colony.size_round_unit(2048)
        self.assertEqual(result, "2KB")

        result = colony.size_round_unit(2049)
        self.assertEqual(result, "2KB")

        result = colony.size_round_unit(2049, space=True)
        self.assertEqual(result, "2 KB")

        result = colony.size_round_unit(2500)
        self.assertEqual(result, "2.44KB")

        result = colony.size_round_unit(2500, space=True)
        self.assertEqual(result, "2.44 KB")

        result = colony.size_round_unit(2048, reduce=False)
        self.assertEqual(result, "2.00KB")

        result = colony.size_round_unit(2500, reduce=False)
        self.assertEqual(result, "2.44KB")

        result = colony.size_round_unit(209715200)
        self.assertEqual(result, "200MB")

        result = colony.size_round_unit(107073781760)
        self.assertEqual(result, "99.7GB")

        result = colony.size_round_unit(940592644096)
        self.assertEqual(result, "876GB")

        result = colony.size_round_unit(1883405279232)
        self.assertEqual(result, "1.71TB")

        result = colony.size_round_unit(1883405279232, places=1)
        self.assertEqual(result, "2TB")

        result = colony.size_round_unit(2500, simplified=True)
        self.assertEqual(result, "2.44K")

        result = colony.size_round_unit(2048, justify=True)
        self.assertEqual(result, "   2KB")

        result = colony.size_round_unit(0)
        self.assertEqual(result, "0B")

        result = colony.size_round_unit(1)
        self.assertEqual(result, "1B")

        result = colony.size_round_unit(1023)
        self.assertEqual(result, "1023B")

        result = colony.size_round_unit(1023.6)
        self.assertEqual(result, "1KB")

        result = colony.size_round_unit(1048063)
        self.assertEqual(result, "1023KB")

        result = colony.size_round_unit(1048575)
        self.assertEqual(result, "1MB")

        result = colony.size_round_unit(1073741823)
        self.assertEqual(result, "1GB")

        result = colony.size_round_unit(1024**8)
        self.assertEqual(result, "1YB")

        result = colony.size_round_unit(1024**9)
        self.assertEqual(result, "1024YB")
