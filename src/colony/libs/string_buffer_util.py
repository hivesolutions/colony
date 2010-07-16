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
import copy

class StringBuffer:
    """
    The string buffer class.
    """

    softspace = 0
    """ The soft space value """

    closed = False
    """ The closed value """

    def __init__(self, fast = True):
        """
        Constructor of the class.

        @type fast: bool
        @param fast: The fast flag to control the string buffer type.
        """

        self.string_list = []
        self.current_value = str()
        self.dirty = False
        self.current_position = 0
        self.current_size = 0
        self.fast = fast

        if fast:
            self.write = self._write_fast
        else:
            self.write = self._write_slow

    def read(self, size = None):
        """
        Reads a buffer from the string buffer with the
        given maximum size.

        @type size: int
        @param size: The maximum size of the buffer to be read.
        """

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
        """
        Writes the given string value to the string buffer.

        @type string_value: String
        @param string_value: The string value to be written.
        """

        pass

    def close(self):
        """
        Closes the string buffer.
        """

        pass

    def flush(self):
        """
        Flushes the string buffer.
        """

        pass

    def reset(self):
        """
        Resets the string buffer.
        """

        self.string_list = []
        self.current_value = str()
        self.dirty = False
        self.current_position = 0
        self.current_size = 0

    def seek(self, offset, whence = os.SEEK_SET):
        """
        Seeks the string buffer to the given offset with the given jump mode,
        defined with the whence.

        @type offset: int
        @param offset: The offset of the jump.
        @type whence: int
        @param whence: The jump mode to be used.
        """

        if whence == os.SEEK_SET:
            self.current_position = offset
        elif whence == os.SEEK_END:
            self.current_position = self.current_size - offset
        elif whence == os.SEEK_CUR:
            if self.current_position + offset < self.current_size:
                self.current_position += offset
            else:
                self.current_position = self.current_size

    def eof(self):
        """
        Returns if the end of file (eof) has been reached.

        @rtype: bool
        @return: If the end of file has been reached.
        """

        return self.current_position == self.current_size

    def next(self):
        """
        Retrieves the next string item from the string buffer.

        @rtype: String
        @return: The next string item from the string buffer.
        """

        return None

    def tell(self):
        """
        Retrieves the current offset position in the string buffer.

        @rtype: int
        @return: The current offset position in the string buffer.
        """

        return self.current_position

    def truncate(self):
        """
        Truncates the string buffer value.
        """

        pass

    def readline(self, size = None):
        """
        Retrieves a line from the string buffer,
        with the given maximum size.

        @type size: int
        @param size: The maximum size of the line to be read.
        @rtype: String
        @return: The read line.
        """

        return None

    def readlines(self, sizehint = None):
        """
        Retrieves a series of lines from the string buffer,
        with the given maximum size.

        @type sizehint: int
        @param sizehint: The maximum size of the lines to be read.
        @rtype: List
        @return: The read lines.
        """

        return None

    def writelines(self, lines):
        """
        Writes the given lines to the string buffer.

        @type lines: List
        @param lines: The lines to be written to the string buffer.
        """

        # iterates over all the lines
        for line in lines:
            # writes the lines to the string buffer
            self.write(line + "\n")

    def isatty(self):
        """
        Returns if the file buffer is of type tty.

        @rtype: bool
        @return: If the file buffer is of type tty.
        """

        return False

    def getvalue(self):
        """
        Retrieves the current string value.
        """

        return self.get_value()

    def get_value(self):
        """
        Retrieves the current string value.
        """

        # regenerates the current value
        self.regenerate()

        # returns the current value
        return self.current_value

    def is_empty(self):
        """
        Returns if the current buffer is empty.

        @rtype: bool
        @return: If the current buffer is empty
        """

        return not self.current_size > 0

    def regenerate(self):
        """
        Regenerates the current value.
        """

        # in case the buffer is dirty
        # or the mode fast is enabled
        if self.dirty or self.fast:
            # regenerates the current value
            self._regenerate()

    def duplicate(self):
        """
        Duplicates the string buffer, returning the
        duplicated value.

        @rtype: StringBuffer
        @return: The duplicated string buffer.
        """

        # creates the new string buffer instance
        duplicated_string_buffer = StringBuffer()

        # sets the duplicated string buffer values
        duplicated_string_buffer.string_list = copy.copy(self.string_list)
        duplicated_string_buffer.current_value = copy.copy(self.current_value)
        duplicated_string_buffer.dirty = self.dirty
        duplicated_string_buffer.current_position = self.current_position
        duplicated_string_buffer.fast = self.fast

        # returns the duplicated string buffer
        return duplicated_string_buffer

    def rollback_last(self):
        """
        Rollsback the last write.
        """

        return self.string_list.pop()

    def get_last(self):
        """
        Retrieves the last write.

        @rtype: String
        @return: The last write.
        """

        return self.string_list[-1]

    def _write_fast(self, string_value):
        """
        Writes the string value in fast mode.

        @type string_value: String
        @param string_value: The string value to be written.
        """

        self.string_list.append(string_value)

    def _write_slow(self, string_value):
        """
        Writes the string value in slow mode.

        @type string_value: String
        @param string_value: The string value to be written.
        """

        self.string_list.append(string_value)
        self.dirty = True
        self.current_size += len(string_value)
        self.current_position = self.current_size

    def _regenerate(self):
        """
        Regenerates the current value (auxiliary method).
        """

        # joins all the string list elements
        self.current_value = "".join(self.string_list)

        # recreates the string list with the current value
        self.string_list = [self.current_value]

        # unsets the dirty flag
        self.dirty = False
