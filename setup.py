#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import glob
import datetime
import setuptools

BASE_DATA_FILES = [
    ("config", ["src/config/README"]),
    ("containers", ["src/containers/README"]),
    ("deploy", ["src/deploy/README"]),
    ("libraries", ["src/libraries/README"]),
    ("log", ["src/log/README"]),
    ("meta", ["src/meta/README"]),
    ("plugins", ["src/plugins/README"]),
    ("scripts", ["src/scripts/README"]),
    ("tmp", ["src/tmp/README"]),
    ("var", ["src/var/README"])
]
""" The base data files to be used """

DATE_FORMAT = "%b %d %Y"
""" The format used to convert dates to strings """

DATE_TIME_FORMAT = "%b %d %Y %H:%M:%S"
""" The format used to convert date times to strings """

def find_data_files(source_path, target_path, patterns):
    """
    Finds data files in the given source path and maps them
    into the target path.
    The list of patterns in glob format represents the filters.

    @type source_path: String
    @param source_path: The source path to find the data files.
    @type target_path: String
    @param target_path: The target path to the data files.
    @type patterns: List
    @param patterns: The list of patterns for file matching.
    @rtype: List
    @return: The list of data file references.
    """

    # in case the source path or the target path contain
    # a glob pattern
    if glob.has_magic(source_path) or glob.has_magic(target_path):
        # raises an exception
        raise ValueError("magic not allowed in source and target")

    # creates the data files map, responsible for mapping
    # the various directories with the existent data files
    data_files_map = {}

    # iterates over all the patterns to be able to filter
    # the file that match the provided patterns
    for pattern in patterns:
        # joins the source path and the pattern
        # to create the "complete" pattern
        pattern = os.path.join(source_path, pattern)

        # iterates over all the filenames in the
        # glob pattern
        for file_name in glob.glob(pattern):
            # in case there is no file to be read
            # must skip the current loop
            if not os.path.isfile(file_name): continue

            # retrieves the relative file path between
            # the source path and the file name
            relative_file_path = os.path.relpath(file_name, source_path)

            # creates the target file path using the
            # target path and the relative path and then
            # retrieves its directory name as the path
            target_file_path = os.path.join(target_path, relative_file_path)
            path = os.path.dirname(target_file_path)

            # adds the filename to the data files map
            data_files_map.setdefault(path, []).append(file_name)

    # retrieves the data files items and then sorts
    # them according to the default order
    data_files_items = data_files_map.items()
    data_files_items = sorted(data_files_items)

    # returns the data files items
    return data_files_items

# finds the scripts data files
scripts_data_files = find_data_files("src/scripts", "scripts", ["all/*", "lib/*", "unix/*", "win32/*"])

# finds the config data files
config_data_files = find_data_files("src/config", "config", ["general/*", "python/*.py"])

# creates the "complete" data files
data_files = BASE_DATA_FILES + scripts_data_files + config_data_files

# retrieves the current root directory (from the
# currently executing file) and in case its not
# the top level root directory changed the current
# executing directory into it (avoids relative path
# problems in executing setuptools)
root_directory = os.path.dirname(__file__)
if not root_directory == "": os.chdir(root_directory)

class ProcessCommand(setuptools.Command):

    description = "custom process command to modify a series of files with the\
    appropriate template values"
    """ The text based description for the current module,
    it's going to be displayed in the command line help """

    user_options = []
    """ The list containing the various user provided
    options from the command line """

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        self._replace("src/colony/base/information.py", "src/colony.json")

    def _replace(self, file_path, json_path):
        # tries to import the json module, it may
        # fails as older version of the python
        # interpreter do not contain it
        import json

        # opens the json symbols file and loads the
        # description map from it to be used to populate
        # the template input
        json_file = open(json_path, "rb")
        try: symbols = json.load(json_file, "utf-8")
        finally: json_file.close()

        # opens the file in the file path for reading
        # in the binary forms, then reads all the contents
        # from it so that they may be replaced by template
        file = open(file_path, "rb")
        try: file_contents = file.read()
        finally: file.close()

        # tries to find the separation string (token) in the
        # file contents and if it's not possible to find it
        # returns immediately to avoid problems
        index = file_contents.find("### % END_INFORMATION % ###")
        if index == -1: return

        # sets the file contents as the sub string comprehending
        # the contents until the separation string
        file_contents = file_contents[:index]

        # retrieves the current datetime and formats it
        # according to the two pre-defined formats
        current_datetime = datetime.datetime.utcnow()
        current_date_string = current_datetime.strftime(DATE_FORMAT)
        current_date_time_string = current_datetime.strftime(DATE_TIME_FORMAT)

        # sets both the date string and the date time string
        # in the symbols map for template reference
        symbols["date"] = current_date_string
        symbols["date_time"] = current_date_time_string

        # sets the generated flag in the symbols table to indicate
        # that the symbols have been already generated (performance)
        symbols["generated"] = "1"

        # decodes the file contents and then runs the formatting
        # engine on top of it so that the symbols are exposed
        # to the string then re-encodes it back to be written
        file_contents = file_contents.decode("utf-8")
        result_contents = file_contents % symbols
        result_contents = result_contents.encode("utf-8")

        # opens the (output) file path and writes the resulting
        # contents into it closing it at the end
        file = open(file_path, "wb")
        try: file.write(result_contents)
        finally: file.close()

setuptools.setup(
    name = "colony",
    version = "1.0.8",
    author = "Hive Solutions Lda.",
    author_email = "development@hive.pt",
    description = "Colony Framework",
    license = "GNU General Public License (GPL), Version 3",
    keywords = "colony plugin framework web",
    url = "http://getcolony.com",
    zip_safe = False,
    scripts = [
        "scripts/pypi/colony.bat",
        "scripts/pypi/colony_admin.py",
        "scripts/pypi/colony_pypi.py",
        "scripts/pypi/colony_adm.bat",
        "scripts/pypi/colony_admin.bat"
    ],
    py_modules = [
        "colony_admin",
        "colony_start",
        "colony_wsgi"
    ],
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
        "" : os.path.normpath("src")
    },
    data_files = data_files,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI"
    ],
    cmdclass = {
        "process" : ProcessCommand
    }
)
