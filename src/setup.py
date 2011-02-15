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

import setuptools

setuptools.setup (
    name = "colony",
    version = "1.0.0",
    author = "Hive Solutions Lda.",
    author_email = "development@hive.pt",
    description = ("Hive Colony Framework",),
    license = "GNU General Public License (GPL), Version 3",
    keywords = "colony plugin framework web",
    url = "http://getcolony.com",
    packages = ["root", "colony", "colony.base", "colony.libs", "colony.test",
                "colony.test.base", "colony.test.libs", "config", "deploy",
                "log", "meta", "plugins", "scripts", "scripts.all", "scripts.lib",
                "scripts.unix", "scripts.win32", "tmp", "var"],
    test_suite = "colony.test.colony_test",
    package_dir = {
        "root" : ""
    },
    package_data = {
        "config" : ["README"],
        "deploy" : ["README"],
        "log" : ["README"],
        "meta" : ["README"],
        "plugins" : ["README"],
        "scripts" : ["README"],
        "scripts.unix" : ["*.sh"],
        "scripts.win32" : ["*.bat"],
        "tmp" : ["README"],
        "var" : ["README"]
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ]
)
