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

import unittest

import colony

try:
    import unittest.mock as mock
except ImportError:
    mock = None


class ConfigTest(unittest.TestCase):
    def test_basic(self):
        colony.conf_s("NAME", "name")
        result = colony.conf("NAME")

        self.assertEqual(result, "name")

        result = colony.conf("NAME", cast=str)

        self.assertEqual(result, "name")
        self.assertEqual(type(result), str)

        result = colony.conf("NAME", cast="str")

        self.assertEqual(result, "name")
        self.assertEqual(type(result), str)

        colony.conf_s("AGE", "10")
        result = colony.conf("AGE", cast=int)

        self.assertEqual(result, 10)
        self.assertEqual(type(result), int)

        result = colony.conf("AGE", cast="int")

        self.assertEqual(result, 10)
        self.assertEqual(type(result), int)

        result = colony.conf("AGE", cast=str)

        self.assertEqual(result, "10")
        self.assertEqual(type(result), str)

        result = colony.conf("HEIGHT")

        self.assertEqual(result, None)

    def test_none(self):
        colony.conf_s("AGE", None)
        result = colony.conf("AGE", cast=int)

        self.assertEqual(result, None)

        result = colony.conf("HEIGHT", cast=int)

        self.assertEqual(result, None)

    def test_load_dot_env(self):
        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        mock_data = mock.mock_open(
            read_data=b"#This is a comment\nAGE=10\nNAME=colony\n"
        )

        with mock.patch("os.path.exists", return_value=True), mock.patch(
            "builtins.open", mock_data, create=True
        ) as mock_open:
            ctx = dict(configs={}, config_f=[])

            colony.base.config.load_dot_env(".env", "utf-8", ctx)

            result = colony.conf("AGE", cast=int)
            self.assertEqual(type(result), int)
            self.assertEqual(result, 10)

            result = colony.conf("AGE", cast=str)

            self.assertEqual(result, "10")
            self.assertEqual(type(result), str)

            result = colony.conf("HEIGHT", cast=int)
            self.assertEqual(result, None)

            self.assertEqual(len(ctx["configs"]), 2)

            self.assertEqual(mock_open.return_value.close.call_count, 1)
