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

def read_file(file_path, mode = "rb"):
    """
    reads the file contents from the file
    in the given file path.

    @type file_path: String
    @param file_path: The file path to be used.
    @type mode: String
    @param mode: The read mode to be used.
    @rtype: String
    @return: The read file contents.
    """

    # opens the file in the current mode
    file = open(file_path, mode)

    try:
        # rads the file contents from the file
        file_contents = file.read()
    finally:
        # closes the file
        file.close()

    # returns the file contents
    return file_contents

def write_file(file_path, file_contents, mode = "wb"):
    """
    Writes the given file contents to the file
    in the given file path.

    @type file_path: String
    @param file_path: The file path to be used.
    @type file_contents: String
    @param file_contents: The contents to be written.
    @type mode: String
    @param mode: The write mode to be used.
    """

    # opens the file in the current mode
    file = open(file_path, mode)

    try:
        # writes the file contents to the file
        file.write(file_contents)
    finally:
        # closes the file
        file.close()

def remove_directory(directory_path):
    """
    Removes the given directory path recursively.
    Directories containing files will have their contents removed
    before being removed.

    @type directory_path: String
    @param directory_path: The path to the directory to be removed.
    """

    # creates the list of paths for the directory path
    paths_list = [os.path.join(directory_path, file_path) for file_path in os.listdir(directory_path)]

    # iterates over all the paths in the paths
    # list to remove them
    for path in paths_list:
        # in case the path is a directory
        if os.path.isdir(path):
            # removes the directory
            remove_directory(path)
        else:
            # removes the path
            os.remove(path)

    # removes the directory
    os.rmdir(directory_path)
