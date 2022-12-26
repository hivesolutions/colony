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

MAP_STRUCTURE = dict(
    name = "name",
    age = 41,
    sons = [
        dict(
            name = "name_son_1",
            age = 12
        ),
        dict(
            name = "name_son_2",
            age = 16
        )
    ],
    father = dict(
        name = "name_father",
        age = 81
    )
)
""" The structure that is going to be the basis for some
of the tests in the map utilities, should be simple enough
to be able to be verified with simplicity """

class MapTest(colony.ColonyTestCase):
    """
    Class that tests the utility functions that
    are associated with map manipulation.
    """

    def test_map_flatten(self):
        """
        Tests the flattening support for map linearization.
        """

        map_flat = colony.map_flatten(MAP_STRUCTURE)
        self.assertNotEqual(map_flat, None)
        self.assertNotEqual(len(map_flat), 6)
        self.assertEqual(map_flat["name"], "name")
        self.assertEqual(map_flat["father.name"], "name_father")
        self.assertEqual(map_flat["sons"], MAP_STRUCTURE["sons"])
