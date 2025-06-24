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

import os
import tempfile
import colony


class PathTest(colony.ColonyTestCase):
    """
    Class that tests the utility functions that
    are associated with path manipulation.
    """

    def test_ensure_file_path(self):
        """
        Tests the ensure_file_path function to verify it correctly
        handles file creation and copying from default file.
        """

        if not hasattr(tempfile, "TemporaryDirectory"):
            self.skipTest("TemporaryDirectory is not available")

        with tempfile.TemporaryDirectory() as temp_dir:
            default_file_path = os.path.join(temp_dir, "default.txt")
            default_content = b"Default content for ensure_file_path"
            with open(default_file_path, "wb") as file:
                file.write(default_content)

            target_file_path = os.path.join(temp_dir, "new", "target.txt")
            colony.ensure_file_path(target_file_path, default_file_path)

            self.assertTrue(os.path.exists(target_file_path))
            with open(target_file_path, "rb") as file:
                content = file.read()
            self.assertEqual(content, default_content)

            existing_content = b"Existing content"
            with open(target_file_path, "wb") as file:
                file.write(existing_content)

            colony.ensure_file_path(target_file_path, default_file_path)

            with open(target_file_path, "rb") as file:
                content = file.read()
            self.assertEqual(content, existing_content)

            deep_target_path = os.path.join(
                temp_dir, "deep", "nested", "path", "file.txt"
            )
            colony.ensure_file_path(deep_target_path, default_file_path)

            self.assertTrue(os.path.exists(deep_target_path))
            with open(deep_target_path, "rb") as file:
                content = file.read()
            self.assertEqual(content, default_content)
