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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 3219 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-05-26 11:52:00 +0100 (ter, 26 Mai 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

class FileRotator:
    """
    Class for handling of writing in files
    with a rotating capability.
    """

    base_file_path = None
    """ The base file path """

    maximum_file_size = None
    """ The maximum file size """

    file_count = None
    """ The number of file to maintained """

    current_file = None
    """ The current file in use """

    current_file_size = None
    """ The size of the current file in use """

    def __init__(self, base_file_path, maximum_file_size = 1048576, file_count = 5):
        self.base_file_path = base_file_path
        self.maximum_file_size = maximum_file_size
        self.file_count = file_count

    def open(self):
        # starts the rotator
        self._sart_rotator()

    def close(self):
        # stops the rotator
        self._stop_rotator()

    def write(self, string_value, flush = True):
        # retrieves the string value length
        string_value_length = len(string_value)

        # in case the string value overflow the current maximum file size
        if self.current_file_size + string_value_length > self.maximum_file_size:
            # updates the rotator
            self._update_rotator()

        # writes the string value to the
        # current file
        self.current_file.write(string_value)

        # flushes the data in the current file
        flush and self.current_file.flush()

        # increments the current file size with
        # the string value length
        self.current_file_size += string_value_length

    def _sart_rotator(self):
        # opens the current file
        self._open_current_file()

    def _stop_rotator(self):
        # closes the current file (in case it's open)
        self.current_file and self._close_current_file()

    def _open_current_file(self):
        # opens the current file
        self.current_file = open(self.base_file_path, "ab")

        # seeks to the end of the current file
        self.current_file.seek(0, os.SEEK_END)

        # sets the initial current file size
        self.current_file_size = self.current_file.tell()

        print self.current_file_size

    def _close_current_file(self, rename = False):
        # flushes the current file
        self.current_file.flush()

        # closes the current file
        self.current_file.close()

        # in case the rename flag is not set
        if not rename:
            # returns immediately
            return

        # creates the target file path for the
        # base file path
        target_file_path = self.base_file_path + ".1"

        # renames the file with to the first incremental index
        os.rename(self.base_file_path, target_file_path)

    def _update_rotator(self):
        # retrieves the file count range
        file_count_range = range(1, self.file_count + 1)

        # reverses the file count range
        file_count_range.reverse()

        # iterates over the range of the
        # file count
        for index in file_count_range:
            # creates the target file path from the base
            # file path and the index string
            target_file_path = self.base_file_path + "." + str(index)

            # in case the target file path exists
            if os.path.exists(target_file_path):
                # in case the index is small than
                # the file count
                if index < self.file_count:
                    # renames the file with an incremented index
                    os.rename(target_file_path, self.base_file_path + "." + str(index + 1))
                # otherwise (overflow occurred)
                else:
                    # removes the target file
                    os.remove(target_file_path)

        # closes the current file
        self.current_file and self._close_current_file(True)

        # opens the current file
        self._open_current_file()
