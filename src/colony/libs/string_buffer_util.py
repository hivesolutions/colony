#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2022 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2022 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import copy

from colony.base import legacy

class StringBuffer(object):
    """
    The string buffer class, used to provide an
    in-memory file like object for fast access.

    The class is provided as an alternative to the
    pre-defined memory buffers.
    """

    softspace = 0
    """ The soft space value """

    closed = False
    """ The closed value """

    def __init__(self, fast = True, btype = None):
        """
        Constructor of the class.

        :type btype: Type
        :param btype: The default base type to be used for the result
        in case it's not provided a smart operation will try to determine
        the best type of string for the joining.
        :type fast: bool
        :param fast: The fast flag to control the string buffer type, notice
        that using the fast flag has it's toll in terms of features.
        """

        self.string_list = []
        self.current_value = str()
        self.btype = btype
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

        :type size: int
        :param size: The maximum size of the buffer to be read.
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

        The method implementation is a placeholder as runtime
        replacement will be performed at build time.

        :type string_value: String
        :param string_value: The string value to be written.
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

        :type offset: int
        :param offset: The offset of the jump.
        :type whence: int
        :param whence: The jump mode to be used.
        """

        if whence == os.SEEK_SET:
            self.current_position = offset
        elif whence == os.SEEK_END:
            self.current_position = self.current_size + offset
        elif whence == os.SEEK_CUR:
            if self.current_position + offset < self.current_size:
                self.current_position += offset
            else:
                self.current_position = self.current_size

    def eof(self):
        """
        Returns if the end of file (eof) has been reached.

        :rtype: bool
        :return: If the end of file has been reached.
        """

        return self.current_position == self.current_size

    def next(self):
        """
        Retrieves the next string item from the string buffer.

        :rtype: String
        :return: The next string item from the string buffer.
        """

        return None

    def tell(self):
        """
        Retrieves the current offset position in the string buffer.

        :rtype: int
        :return: The current offset position in the string buffer.
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

        :type size: int
        :param size: The maximum size of the line to be read.
        :rtype: String
        :return: The read line.
        """

        return None

    def readlines(self, sizehint = None):
        """
        Retrieves a series of lines from the string buffer,
        with the given maximum size.

        :type sizehint: int
        :param sizehint: The maximum size of the lines to be read.
        :rtype: List
        :return: The read lines.
        """

        return None

    def writelines(self, lines):
        """
        Writes the given lines to the string buffer.

        :type lines: List
        :param lines: The lines to be written to the string buffer.
        """

        # iterates over all the lines
        for line in lines:
            # writes the lines to the string buffer
            self.write(line + "\n")

    def isatty(self):
        """
        Returns if the file buffer is of type tty.

        :rtype: bool
        :return: If the file buffer is of type tty.
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

        :rtype: bool
        :return: If the current buffer is empty
        """

        return not self.current_size > 0

    def regenerate(self):
        """
        Regenerates the current value, this is an
        expensive operation and should be performed
        only in extreme situations.
        """

        # in case both the current buffer is not dirty
        # and the fast mode is not enabled the regeneration
        # operation is ignored, control flow returned
        if not self.dirty and not self.fast: return

        # runs the regenerate operation for the current
        # buffer so that the complete set of partial
        # values are joined as a simple buffer value
        self._regenerate()

    def duplicate(self):
        """
        Duplicates the string buffer, returning the
        duplicated value.

        :rtype: StringBuffer
        :return: The duplicated string buffer.
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

    def rollback_last(self, item_count = 1):
        """
        Rollsback the last write.

        :type item_count: int
        :param item_count: The number of items
        to be "rollbacked".
        """

        # iterates over the range of item count
        for _index in range(item_count):
            # pops an item from the string list
            self.string_list.pop()

    def get_last(self, index = -1):
        """
        Retrieves the last write.

        :type index: int
        :param index: The index to retrieve from
        the string list.
        :rtype: String
        :return: The last write.
        """

        # retrieves the absolute index
        absolute_index = abs(index)

        # retrieves the string list length
        string_list_length = len(self.string_list)

        # in case the absolute index "overflows"
        # the string list length
        if absolute_index > string_list_length:
            # return invalid
            return None

        # returns the "last" element
        return self.string_list[index]

    def output_file(self, path):
        """
        Outputs the current file contents to the file
        defined in the target path.

        This method provides a simple way to debug the
        information contained in the buffer.

        :type path: String
        :param path: The path to the file that is going
        to be used to place the buffer contents.
        """

        position = self.tell()
        self.seek(0)
        try:
            contents = self.read()
            file = open(path, "wb")
            try: file.write(contents)
            finally: file.close()
        finally:
            self.seek(position)

    def _write_fast(self, string_value):
        """
        Writes the string value in fast mode.

        :type string_value: String
        :param string_value: The string value to be written.
        """

        self.string_list.append(string_value)

    def _write_slow(self, string_value):
        """
        Writes the string value in slow mode.

        :type string_value: String
        :param string_value: The string value to be written.
        """

        self.string_list.append(string_value)
        self.dirty = True
        self.current_size += len(string_value)
        self.current_position = self.current_size

    def _regenerate(self):
        """
        Regenerates the current value (auxiliary method).

        This may be a very expensive method as it re-joins
        the complete set of parts of the current buffer.
        """

        # retrieves the base string or bytes value and uses
        # it to join the complete set of string values that
        # are part of the current buffer
        base = self._base_type()
        self.current_value = base.join(self.string_list)

        # recreates the string list with the current value
        self.string_list = [self.current_value]

        # unsets the dirty flag, so that the re-generate
        # operation is marked as not required until new
        # data is added to the current string buffer
        self.dirty = False

    def _base_type(self):
        """
        Determines the base string type value that may be used
        to join the various string value parts of the buffer.

        This is required so that no invalid types are used causing
        an exception to be raised in the joining.

        In case the current python interpreter does not allow
        byte buffers or in case the base type is fixed in the
        constructor, this method returns immediately.

        :rtype: String
        :return: The string value that may be used as the basis for
        the joining of the various components of the string list/buffer.
        """

        if not legacy.PYTHON_3: return ""
        if self.btype == str: return ""
        if self.btype == legacy.BYTES: return b""
        if self.btype == legacy.UNICODE: return legacy.u("")
        is_bytes = True
        for value in self.string_list:
            if not type(value) == str: continue
            is_bytes = False
            break
        return b"" if is_bytes else ""
