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

__author__ = "Hugo Gomes <hugo@frontdoorhq.com>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import unittest

import colony


class VarsTest(unittest.TestCase):
    def test_set_global(self):
        colony.set_global("test_var", 42)
        result = colony.get_global("test_var")
        self.assertEqual(result, 42)

    def test_get_global_existing(self):
        colony.set_global("existing_var", "Hello, World!")
        result = colony.get_global("existing_var")
        self.assertEqual(result, "Hello, World!")

    def test_get_global_default(self):
        result = colony.get_global("non_existing_var", "Default Value")
        self.assertEqual(result, "Default Value")

    def test_get_global_no_default(self):
        result = colony.get_global("non_existing_var")
        self.assertIsNone(result)

    def test_get_global_existing_default(self):
        colony.set_global("existing_var", "Hello, World!")
        result = colony.get_global("existing_var", "Default Value")
        self.assertEqual(result, "Hello, World!")

    def test_has_global_existing(self):
        colony.set_global("existing_var", "Hello, World!")
        result = colony.has_global("existing_var")
        self.assertTrue(result)

    def test_has_global_non_existing(self):
        result = colony.has_global("non_existing_var")
        self.assertFalse(result)

    def test_has_global_with_none(self):
        colony.set_global("none_var", None)
        result = colony.has_global("none_var")
        self.assertTrue(result)
