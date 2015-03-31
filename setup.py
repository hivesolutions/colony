#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import setuptools

setuptools.setup(
    name = "colony",
    version = "1.3.11",
    author = "Hive Solutions Lda.",
    author_email = "development@hive.pt",
    description = "Colony Framework",
    license = "GNU General Public License (GPL), Version 3",
    keywords = "colony plugin framework web",
    url = "http://getcolony.com",
    zip_safe = False,
    py_modules = [
        "colony_adm",
        "colony_start",
        "colony_wsgi"
    ],
    packages = [
        "colony",
        "colony.base",
        "colony.config",
        "colony.libs",
        "colony.test",
        "colony.test.base",
        "colony.test.libs"
    ],
    test_suite = "colony.test",
    package_dir = {
        "" : os.path.normpath("src")
    },
    package_data = {
        "colony" : ["res/*"]
    },
    entry_points = {
        "console_scripts" : [
            "cpm = colony_adm:main",
            "colony = colony_start:main",
            "colony_wsgi = colony_wsgi:main"
        ]
    },
    install_requires = [
        "appier"
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI"
    ]
)
