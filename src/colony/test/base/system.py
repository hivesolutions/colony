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

try:
    import unittest.mock as mock
except ImportError:
    mock = None


class PluginManagerTest(colony.ColonyTestCase):
    """
    Test case for the verification of the core plugin
    manager instance responsible for the base orchestration
    of the Colony Plugin system.
    """

    def test_resolve_string_value(self):
        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        plugin_manager = colony.PluginManager()

        self.assertEqual(plugin_manager.resolve_string_value("%manager_path%"), [""])
        self.assertRaises(
            colony.ColonyException,
            lambda: plugin_manager.resolve_string_value("%plugin_path:pt.hive.main%"),
        )
        self.assertRaises(
            AttributeError, lambda: plugin_manager.resolve_string_value("%unset%")
        )

        plugin_manager.get_plugin_path_by_id = mock.MagicMock(return_value="hello_path")
        self.assertEqual(
            plugin_manager.resolve_string_value("%plugin_path:pt.hive.main%"),
            ["hello_path"],
        )
