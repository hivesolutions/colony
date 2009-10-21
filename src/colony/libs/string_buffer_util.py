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

__revision__ = "$LastChangedRevision: 3219 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-05-26 11:52:00 +0100 (ter, 26 Mai 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

class StringBuffer:
    """
    The string buffer class.
    """

    softspace = 0

    closed = False

    def __init__(self, fast = True):
        self.string_list = []
        self.current_value = ""
        self.dirty = False
        self.current_position = 0
        self.current_size = 0
        self.fast = fast

        if fast:
            self.write = self.write_fast
        else:
            self.write = self.write_slow

    def read(self, size = None):
        # regenerates the current value
        self.regenerate()

        if size:
            return_value = self.current_value[self.current_position:self.current_position + size]
            self.seek(size, os.SEEK_CUR)
        else:
            return_value = self.current_value[self.current_position:]
            self.seek(self.current_size, os.SEEK_SET)

        # returns the return value
        return return_value

    def write(self, string_value):
        pass

    def write_fast(self, string_value):
        self.string_list.append(string_value)

    def write_slow(self, string_value):
        self.string_list.append(string_value)
        self.dirty = True
        self.current_size += len(string_value)
        self.current_position = self.current_size

    def close(self):
        pass

    def flush(self):
        pass

    def reset(self):
        self.string_list = []
        self.current_value = ""
        self.dirty = False
        self.current_position = 0
        self.current_size = 0

    def seek(self, offset, whence = os.SEEK_SET):
        if whence == os.SEEK_SET:
            self.current_position = offset
        elif whence == os.SEEK_END:
            self.current_position = self.current_size - offset
        elif whence == os.SEEK_CUR:
            if self.current_position + offset < self.current_size:
                self.current_position += offset
            else:
                self.current_position = self.current_size

    def next(self):
        return None

    def tell(self):
        return self.current_position

    def truncate(self):
        pass

    def readline(self):
        return None

    def readlines(self):
        return None

    def writelines(self, lines):
        for line in lines:
            self.write(line + "\n")

    def isatty(self):
        return False

    def getvalue(self):
        return self.get_value()

    def get_value(self):
        # regenerates the current value
        self.regenerate()

        # returns the current value
        return self.current_value

    def regenerate(self):
        # in case the buffer is dirty
        # or the mode fast is enabled
        if self.dirty or self.fast:
            # regenerates the current value
            self._regenerate()

    def _regenerate(self):
        self.current_value = "".join(self.string_list)
