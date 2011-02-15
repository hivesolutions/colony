#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 9712 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-08-10 13:42:37 +0100 (ter, 10 Ago 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import glob
import setuptools

BASE_DATA_FILES = [
    ("config", ["src/config/README"]),
    ("deploy", ["src/deploy/README"]),
    ("log", ["src/log/README"]),
    ("meta", ["src/meta/README"]),
    ("plugins", ["src/plugins/README"]),
    ("scripts", ["src/scripts/README"]),
    ("tmp", ["src/tmp/README"]),
    ("var", ["src/var/README"])
]
""" The base data files to be used """

def find_data_files(source_path, target_path, patterns):
    # in case the source path or the target path contain
    # a glob pattern
    if glob.has_magic(source_path) or glob.has_magic(target_path):
        # raises an exception
        raise ValueError("Magic not allowed in source and target")

    # creates the data files map
    data_files_map = {}

    # iterates over all the patterns
    for pattern in patterns:
        # joins the source path and the pattern
        # to create the "complete" pattern
        pattern = os.path.join(source_path, pattern)

        # iterates over all the filenames in the
        # glob pattern
        for file_name in glob.glob(pattern):
            # in case there is no file
            if not os.path.isfile(file_name):
                # continues the loop
                continue

            # retrieves the relative file path between
            # the source path and the file name
            relative_file_path = os.path.relpath(file_name, source_path)

            # creates the target file path using the
            # target path and the relative path
            target_file_path = os.path.join(target_path, relative_file_path)

            # retrieves the directory name from the target path
            path = os.path.dirname(target_file_path)

            # adds the filename to the data files map
            data_files_map.setdefault(path, []).append(file_name)

    # retrieves the data files items
    data_files_items = data_files_map.items()

    # sorts the data files items
    data_files_items = sorted(data_files_items)

    # returns the data files items
    return data_files_items

# finds the scripts data files
scripts_data_files = find_data_files("src/scripts", "scripts", ["all/*", "lib/*", "unix/*", "win32/*"])

# finds the config data files
config_data_files = find_data_files("src/config", "config", ["*.py"])

# creates the "complete" data files
data_files = BASE_DATA_FILES + scripts_data_files + config_data_files

setuptools.setup (
    name = "colony",
    version = "1.0.0",
    author = "Hive Solutions Lda.",
    author_email = "development@hive.pt",
    description = ("Hive Colony Framework",),
    license = "GNU General Public License (GPL), Version 3",
    keywords = "colony plugin framework web",
    url = "http://getcolony.com",
    py_modules = ["main", "script"],
    packages = [
        "colony",
        "colony.base",
        "colony.libs",
        "colony.test",
        "colony.test.base",
        "colony.test.libs"
    ],
    test_suite = "colony.test.colony_test",
    package_dir = {
        "" : "src"
    },
    package_data = {
    },
    data_files = data_files,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ]
)
