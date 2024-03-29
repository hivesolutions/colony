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
