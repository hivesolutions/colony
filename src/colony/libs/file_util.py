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
import tempfile
import threading

from colony.base import legacy

from . import list_util
from . import path_util

PATH_TUPLE_PROCESS_METHOD_PREFIX = "_process_path_tuple_"
""" The prefix to the path tuple process method """

ADD_OPERATION = "add"
""" The add operation """

ADD_NO_REPLACE_OPERATION = "add_no_replace"
""" The add no replace operation """

REMOVE_OPERATION = "remove"
""" The remove operation """

class FileRotator(object):
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

    closed = False
    """ The flag that controls the current status of the file rotator """

    def __init__(self, base_file_path, maximum_file_size = 1048576, file_count = 5):
        """
        Constructor of the class.

        :type base_file_path: String
        :param base_file_path: The base file path to be used.
        :type maximum_file_size: int
        :param maximum_file_size: The maximum file size.
        :type file_count: int
        :param file_count: The number of files to be used.
        """

        self.base_file_path = base_file_path
        self.maximum_file_size = maximum_file_size
        self.file_count = file_count

    def open(self):
        """
        Opens the file rotator.
        """

        # starts the rotator
        self._sart_rotator()

        # updates the closed status
        self.closed = False

    def close(self):
        """
        Closes the file rotator.
        """

        # stops the rotator
        self._stop_rotator()

        # updates the closed status
        self.closed = True

    def write(self, string_value, flush = True, encoding = "utf-8"):
        """
        Writes the given string value using
        the current file rotator.

        :type string_value: String
        :param string_value: The string value to be
        written.
        :type flush: bool
        :param flush: If the current file rotator should
        be flushed.
        """

        # retrieves the string value length
        string_value_length = len(string_value)

        # in case the string value overflow the current maximum file size
        if self.current_file_size + string_value_length > self.maximum_file_size:
            # updates the rotator
            self._update_rotator()

        # verifies if the provided string value is "decoded" as unicode
        # if that's the case runs the encoding process using the value
        # of the encoding attribute as the reference for the encoding
        is_unicode = type(string_value) == legacy.UNICODE
        if is_unicode: string_value = string_value.encode(encoding)

        # writes the string value to the current file, note that the
        # value that is being written is already encoded as bytes
        self.current_file.write(string_value)

        # flushes the data in the current file
        flush and self.current_file.flush()

        # increments the current file size with
        # the string value length
        self.current_file_size += string_value_length

    def is_closed(self):
        """
        Returns the current closed status
        for the internal file reference.

        :rtype: bool
        :return: The current closed status
        for the internal file reference.
        """

        return self.closed

    def _sart_rotator(self):
        """
        Starts the file rotator.
        """

        # opens the current file
        self._open_current_file()

    def _stop_rotator(self):
        """
        Stops the file rotator.
        """

        # closes the current file (in case it's open)
        self.current_file and self._close_current_file()

    def _open_current_file(self):
        """
        Opens the current file to be used.
        """

        # opens the current file
        self.current_file = open(self.base_file_path, "ab")

        # seeks to the end of the current file
        self.current_file.seek(0, os.SEEK_END)

        # sets the initial current file size
        self.current_file_size = self.current_file.tell()

    def _close_current_file(self, rename = False):
        """
        Closes the current file being used.
        In case the renaming flag is set the file is
        renamed to the first file in the rotator.

        :type rename: bool
        :param rename: If the renaming on the
        file should be done.
        """

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
        """
        Updates the current file rotator state.
        This procedure involves the renaming the current
        set of files in the rotator.
        It also removes the extra file that overflow the
        current file count.
        """

        # retrieves the file count range and runs the
        # reverse operation in it to obtains the correct
        # range value to be used in the rotator operation
        file_count_range = legacy.eager(range(1, self.file_count + 1))
        file_count_range.reverse()

        # iterates over the range of the
        # file count
        for index in file_count_range:
            # creates the target file path from the base
            # file path and the index string
            target_file_path = self.base_file_path + "." + str(index)

            # in case the target file path does not exist
            # there's nothing to be done, skips the loop
            if not os.path.exists(target_file_path): continue

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

class FileContext(object):
    """
    The file context class used to read and write
    contents from files.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def resolve_file_path(self, file_path):
        """
        Resolves the given file path, for the current
        environment it is the same value.

        :type file_path: String
        :param file_path: The file path to be resolved.
        :rtype: String
        :return: The resolved (real) file path.
        """

        # returns the file path (same value)
        return file_path

    def exists_file_path(self, file_path):
        """
        Tests if the given file path exists in
        the current environment.

        :type file_path: String
        :param file_path: The file path to be tested
        for existence.
        :rtype: bool
        :return: The result of the test for
        file existence.
        """

        # checks if the file path exists
        exists_file_path = os.path.exists(file_path)

        # returns the exists file path result
        return exists_file_path

    def is_directory_path(self, file_path):
        """
        Tests if the given file path refers a directory path in
        the current environment.

        :type file_path: String
        :param file_path: The file path to be tested
        for directory referral.
        :rtype: bool
        :return: The result of the test for
        directory referral.
        """

        # tests if the file path refers a directory path
        is_directory_path = os.path.isdir(file_path)

        # returns the is directory path result
        return is_directory_path

    def read_file(self, file_path):
        """
        Reads the contents from the given
        file path.

        :type file_path: String
        :param file_path: The path to the file
        to read from.
        :rtype: String
        :return: The (read) contents from the file.
        """

        # open the file
        file = open(file_path, "rb")

        try:
            # reads the file contents
            file_contents = file.read()
        finally:
            # closes the file
            file.close()

        # returns the file contents
        return file_contents

    def write_file(self, file_path, file_contents):
        """
        Writes the contents to the file in the
        given file path.

        :type file_path: String
        :param file_path: The path to the file to
        be written.
        :type file_contents: String
        :param file_contents: The contents to be
        written to the file.
        """

        # creates the directory for the file path
        self._create_directory(file_path)

        # open the file
        file = open(file_path, "wb")

        try:
            # writes the file contents
            file.write(file_contents)
        finally:
            # closes the file
            file.close()

    def remove_directory(self, directory_path, handle_exception = False):
        """
        Removes the directory in the given path.

        :type directory_path: String
        :param directory_path: The path to the directory
        to be removed.
        :type handle_exception: bool
        :param handle_exception: If an eventual raised exception shall
        be handled gracefully.
        """

        # in case the directory path does not exists
        if not os.path.exists(directory_path):
            # returns immediately
            return

        # retrieves the directory items
        directory_items = os.listdir(directory_path)

        try:
            # checks the directory for items and removes
            # the directory in the path (recursively)
            not directory_items and os.removedirs(directory_path)
        except Exception as exception:
            if not handle_exception: raise exception

    def remove_file(self, file_path, handle_exception = False):
        """
        Removes the file in the given path.

        :type directory_path: String
        :param directory_path: The path to the file
        to be removed.
        :type handle_exception: bool
        :param handle_exception: If an eventual raised exception shall
        be handled gracefully.
        """

        # in case the file path does not exists
        if not os.path.exists(file_path):
            # returns immediately
            return

        try:
            # removes the file path
            os.remove(file_path)
        except Exception as exception:
            if not handle_exception: raise exception

    def remove_directory_immediate(self, directory_path, handle_exception = False):
        """
        Removes the directory in the given directory path.

        :type directory_path: String
        :param directory_path: The path to the directory
        to be removed.
        :type handle_exception: bool
        :param handle_exception: If an eventual raised exception shall
        be handled gracefully.
        """

        # removes the directory in the (real) directory path
        path_util.remove_directory(directory_path, handle_exception)

    def get_file_path(self, file_path):
        """
        Retrieves a file path from the given file
        path.
        The returned file path is used in
        the current file context.

        :type file_path: String
        :param file_path: The file path to be used as base.
        :rtype: String
        :return: The file path to be used for writing.
        """

        # returns the file path
        return file_path

    def _create_directory(self, file_path):
        """
        Creates a directory from the given file path.

        :type file_path: String
        :param file_path: The path to the directory
        to be created.
        """

        # retrieves the directory path for the file path
        directory_path = os.path.dirname(file_path)

        # in case the directory path exists
        if os.path.exists(directory_path):
            # returns immediately
            return

        # creates the various required directories
        os.makedirs(directory_path)

class TransactionContext(object):
    """
    Generic transaction abstraction that hold the logic
    to the calling of the various transaction section
    callbacks for a "normal" workflow.
    """

    commit_callbacks_list = []
    """ The list of callbacks to be called upon commit """

    pre_commit_callbacks_list = []
    """ The list of callbacks to be called before commit """

    rollback_callbacks_list = []
    """ The list of callbacks to be called upon rollback """

    pre_rollback_callbacks_list = []
    """ The list of callbacks to be called before rollback """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.commit_callbacks_list = []
        self.pre_commit_callbacks_list = []
        self.rollback_callbacks_list = []
        self.pre_rollback_callbacks_list = []

    def add_commit_callback(self, callback):
        """
        Adds a new commit callback.
        This callback will be called upon the final
        commit is passed.

        :type callback: Function
        :param callback: The callback function to be called
        upon the final commit.
        """

        self.remove_commit_callback(callback)
        self.commit_callbacks_list.append(callback)

    def remove_commit_callback(self, callback):
        """
        Removes an existing commit callback.

        :type callback: Function
        :param callback: The callback function to be called
        upon the final commit.
        """

        if not callback in self.commit_callbacks_list: return
        self.commit_callbacks_list.remove(callback)

    def add_pre_commit_callback(self, callback):
        """
        Adds a new pre commit callback.
        This callback will be called upon the final
        commit is started.

        :type callback: Function
        :param callback: The callback function to be called
        upon the final commit.
        """

        self.remove_pre_commit_callback(callback)
        self.pre_commit_callbacks_list.append(callback)

    def remove_pre_commit_callback(self, callback):
        """
        Removes an existing pre commit callback.

        :type callback: Function
        :param callback: The callback function to be called
        upon the final commit.
        """

        if not callback in self.pre_commit_callbacks_list: return
        self.pre_commit_callbacks_list.remove(callback)

    def add_rollback_callback(self, callback):
        """
        Adds a new rollback callback.
        This callback will be called upon the final
        rollback is passed.

        :type callback: Function
        :param callback: The callback function to be called
        upon the final rollback.
        """

        self.remove_rollback_callback(callback)
        self.rollback_callbacks_list.append(callback)

    def remove_rollback_callback(self, callback):
        """
        Removes an existing rollback callback.

        :type callback: Function
        :param callback: The callback function to be called
        upon the final rollback.
        """

        if not callback in self.rollback_callbacks_list: return
        self.rollback_callbacks_list.remove(callback)

    def add_pre_rollback_callback(self, callback):
        """
        Adds a new pre rollback callback.
        This callback will be called upon the final
        rollback is started.

        :type callback: Function
        :param callback: The callback function to be called
        upon the final rollback.
        """

        self.remove_pre_rollback_callback(callback)
        self.pre_rollback_callbacks_list.append(callback)

    def remove_pre_rollback_callback(self, callback):
        """
        Removes an existing pre rollback callback.

        :type callback: Function
        :param callback: The callback function to be called
        upon the final rollback.
        """

        if not callback in self.pre_rollback_callbacks_list: return
        self.pre_rollback_callbacks_list.remove(callback)

    def _call_commit_callbacks(self):
        """
        Calls all the commit callback functions
        in the current list.
        This method should be called at the
        end of a commit.
        """

        # iterates over all the commit callback functions
        for commit_callback in self.commit_callbacks_list:
            # calls the the commit callback
            commit_callback()

        # empties the commit callbacks
        self.commit_callbacks_list = []

    def _call_pre_commit_callbacks(self):
        """
        Calls all the pre commit callback functions
        in the current list.
        This method should be called at the
        beginning of a commit.
        """

        # iterates over all the pre commit callback functions
        for pre_commit_callback in self.pre_commit_callbacks_list:
            # calls the the pre commit callback
            pre_commit_callback()

        # empties the pre commit callbacks
        self.pre_commit_callbacks_list = []

    def _call_rollback_callbacks(self):
        """
        Calls all the rollback callback functions
        in the current list.
        This method should be called at the
        end of a rollback.
        """

        # iterates over all the rollback callback functions
        for rollback_callback in self.rollback_callbacks_list:
            # calls the the rollback callback
            rollback_callback()

        # empties the rollback callbacks
        self.rollback_callbacks_list = []

    def _call_pre_rollback_callbacks(self):
        """
        Calls all the pre rollback callback functions
        in the current list.
        This method should be called at the
        beginning of a rollback.
        """

        # iterates over all the pre rollback callback functions
        for pre_rollback_callback in self.pre_rollback_callbacks_list:
            # calls the the pre rollback callback
            pre_rollback_callback()

        # empties the pre rollback callbacks
        self.pre_rollback_callbacks_list = []

class FileImmediateContext(FileContext, TransactionContext):
    """
    The file immediate context class that controls
    an immediate transaction involving the file system.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        FileContext.__init__(self)
        TransactionContext.__init__(self)

    def open(self):
        """
        Opens a new transaction context.
        """

        pass

    def commit(self, remove_duplicates = True):
        """
        Commits a new transaction context.
        All the pending file operations
        will be persisted.

        An optional argument may be unset if
        the duplicate operation are not meant
        to be removed.

        :type remove_duplicates: bool
        :param remove_duplicats: If duplicate operations
        are meant to be removed so that no duplicate
        operation are performed (performance impact).
        """

        # calls the pre (before) commit callbacks
        self._call_pre_commit_callbacks()

        # calls the "final" commit callbacks
        self._call_commit_callbacks()

    def rollback(self):
        """
        Reverts all the pending operations in
        the current transaction context.
        All the data pending persistence will
        be dropped.
        """

        # calls the pre (before) rollback callbacks
        self._call_pre_rollback_callbacks()

        # calls the "final" rollback callbacks
        self._call_rollback_callbacks()

class FileTransactionContext(FileContext, TransactionContext):
    """
    The file transaction context class that controls
    a transaction involving the file system.
    """

    transaction_level = 0
    """ The current transaction level in use """

    temporary_path = None
    """ The temporary path to be used in the file transaction """

    path_tuples_list = []
    """ The list of path tuples associated with the transaction """

    access_lock = None
    """ The lock controlling the access to the file transaction """

    def __init__(self, temporary_path = None):
        """
        Constructor of the class.

        :type temporary_path: String
        :param temporary_path: The temporary path to be used
        for the transaction temporary files.
        """

        FileContext.__init__(self)
        TransactionContext.__init__(self)
        self.temporary_path = temporary_path or tempfile.mkdtemp()

        self.path_tuples_list = []
        self.access_lock = threading.RLock()

    def resolve_file_path(self, file_path):
        """
        Resolves the given file path, checking if it
        exists and if it is valid.

        :type file_path: String
        :param file_path: The file path to be resolved.
        :rtype: String
        :return: The resolved (real) file path.
        """

        # retrieves the virtual file path for the file path
        virtual_file_path = self._get_virtual_file_path(file_path)

        # checks if the virtual file path exists
        virtual_file_path_exists = os.path.exists(virtual_file_path)

        # resolves the file path taking into account the
        # existence of the virtual file path
        real_file_path = virtual_file_path_exists and virtual_file_path or file_path

        # returns the real file path
        return real_file_path

    def exists_file_path(self, file_path):
        """
        Tests if the given file path exists in
        the current virtual environment.

        :type file_path: String
        :param file_path: The file path to be tested
        for existence.
        :rtype: bool
        :return: The result of the test for
        file existence.
        """

        # resolves the virtual file path
        virtual_file_path = self._get_virtual_file_path(file_path)

        # tests if the file has been already (potentially) removed
        removed_file_path = self._is_removed_file_path(file_path)

        # tests if both the (real) file path and the virtual
        # file path exist
        file_path_exists = os.path.exists(file_path)
        virtual_file_path_exists = os.path.exists(virtual_file_path)

        # tests if the file path exists, checks the condition
        # that if the (real) file path exists the removed file path
        # must not exist otherwise if the virtual file path exists
        # the file also exists
        exists_file_path = (file_path_exists and not removed_file_path) or virtual_file_path_exists

        # returns the exists file path result
        return exists_file_path

    def is_directory_path(self, file_path):
        """
        Tests if the given file path refers a directory path in
        the current virtual environment.

        :type file_path: String
        :param file_path: The file path to be tested
        for directory referral.
        :rtype: bool
        :return: The result of the test for
        directory referral.
        """

        # resolves the file path (real file path)
        real_file_path = self.resolve_file_path(file_path)

        # tests if the file path refers a directory path
        is_directory_path = os.path.isdir(real_file_path)

        # returns the is directory path result
        return is_directory_path

    def read_file(self, file_path):
        """
        Reads the given file contents from a file.
        In case a transaction exists the contents read
        are the virtual ones.

        :type file_path: String
        :param file_path: The path to the file to be
        read.
        :rtype: String
        :return: The read file contents.
        """

        # resolves the file path (real file path)
        real_file_path = self.resolve_file_path(file_path)

        # reads the file using the file context (virtual file path used)
        file_contents = FileContext.read_file(self, real_file_path)

        # returns the file contents
        return file_contents

    def write_file(self, file_path, file_contents, replace_file = True):
        """
        Writes the given file contents to a file in
        the given file path.
        This write is not persisted immediately and
        pushed to a transaction.

        :type file_path: String
        :param file_path: The path to the file to be
        written.
        :type file_contents: String
        :param file_contents: The contents to be written
        to the file.
        :type replace_file: bool
        :param replace_file: If the file should be replaced
        in case existent file is found.
        """

        # retrieves the virtual file path for the file path
        virtual_file_path = self._get_virtual_file_path(file_path)

        # writes the file using the file context (virtual file path used)
        FileContext.write_file(self, virtual_file_path, file_contents)

        # sets the operation based on the value of the replace file flag
        operation = replace_file and ADD_OPERATION or ADD_NO_REPLACE_OPERATION

        # creates a path tuple with the virtual file path
        # and the file path for the operation add
        path_tuple = (
            operation,
            virtual_file_path,
            file_path
        )

        # adds the path tuple
        self._add_path_tuple(path_tuple)

    def remove_directory(self, directory_path, handle_exception = False):
        """
        Removes the directory in the given path.
        This removal is not persisted immediately and
        pushed to a transaction.

        :type directory_path: String
        :param directory_path: The path to the directory
        to be removed.
        :type handle_exception: bool
        :param handle_exception: If an eventual raised exception shall
        be handled gracefully.
        """

        # retrieves the virtual directory path for the file path
        virtual_directory_path = self._get_virtual_file_path(directory_path)

        # in case the virtual directory path exists
        if os.path.exists(virtual_directory_path):
            # retrieves the (virtual) directory items
            virtual_directory_items = os.listdir(virtual_directory_path)

            try:
                # checks the virtual directory for items and removes
                # the directory in the virtual path (recursively)
                not virtual_directory_items and os.removedirs(virtual_directory_path)
            except Exception as exception:
                if not handle_exception: raise exception

        # creates a path tuple with the directory path
        # the operation remove, the recursive flag is set
        path_tuple = (
            REMOVE_OPERATION,
            directory_path,
            handle_exception,
            True
        )

        # adds the path tuple
        self._add_path_tuple(path_tuple)

    def remove_file(self, file_path, handle_exception = False):
        """
        Removes the file in the given path.
        This removal is not persisted immediately and
        pushed to a transaction.

        :type directory_path: String
        :param directory_path: The path to the file
        to be removed.
        :type handle_exception: bool
        :param handle_exception: If an eventual raised exception shall
        be handled gracefully.
        """

        # retrieves the virtual file path for the file path
        virtual_file_path = self._get_virtual_file_path(file_path)

        # in case the virtual file path exists
        if os.path.exists(virtual_file_path):
            try:
                # removes the virtual file path
                os.remove(virtual_file_path)
            except Exception as exception:
                if not handle_exception: raise exception

        # creates a path tuple with the file path
        # the operation remove, the recursive flag is unset
        path_tuple = (
            REMOVE_OPERATION,
            file_path,
            handle_exception,
            False
        )

        # adds the path tuple
        self._add_path_tuple(path_tuple)

    def remove_directory_immediate(self, directory_path, handle_exception = False):
        """
        Removes the directory in the given directory path.
        In case a transaction exists the directory to be
        removed is the virtual one.

        :type directory_path: String
        :param directory_path: The path to the directory
        to be removed.
        :type handle_exception: bool
        :param handle_exception: If an eventual raised exception shall
        be handled gracefully.
        """

        # resolves the directory path (real directory path)
        real_directory_path = self.resolve_file_path(directory_path)

        try:
            # removes the directory in the (real) directory path
            path_util.remove_directory(real_directory_path)
        except Exception as exception:
            if not handle_exception: raise exception

    def get_file_path(self, file_path, replace_files = True):
        """
        Retrieves a file path to be used for writing.
        The file path to be used will be used in a
        transaction environment and context.

        :type file_path: String
        :param file_path: The file path to be used as base.
        :type replace_files: bool
        :param replace_files: If the files should be replaced
        in case duplicate files are found.
        :rtype: String
        :return: The file path to be used for writing.
        """

        # retrieves the virtual file path for the file path
        virtual_file_path = self._get_virtual_file_path(file_path)

        # sets the operation based on the value of the replace files flag
        operation = replace_files and ADD_OPERATION or ADD_NO_REPLACE_OPERATION

        # creates a path tuple with the virtual file path
        # and the file path
        path_tuple = (
            operation,
            virtual_file_path,
            file_path
        )

        # adds the path tuple
        self._add_path_tuple(path_tuple)

        # returns the virtual file path
        return virtual_file_path

    def open(self):
        """
        Opens a new transaction context.
        """

        # acquires the access lock
        self.access_lock.acquire()

        try:
            # increments the transaction level
            self.transaction_level += 1
        finally:
            # releases the access lock
            self.access_lock.release()

    def commit(self, remove_duplicates = True):
        """
        Commits a new transaction context.
        All the pending file operations
        will be persisted.

        An optional argument may be unset if
        the duplicate operation are not meant
        to be removed.

        :type remove_duplicates: bool
        :param remove_duplicats: If duplicate operations
        are meant to be removed so that no duplicate
        operation are performed (performance impact).
        """

        # acquires the access lock
        self.access_lock.acquire()

        try:
            # decrements the transaction level
            self.transaction_level -= 1

            # in case the transaction level is positive
            if self.transaction_level > 0:
                # returns immediately
                return
            # in case the transaction level is negative
            elif self.transaction_level < 0:
                # raises the runtime error
                raise RuntimeError("Invalid transaction level")

            # calls the pre (before) commit callbacks
            self._call_pre_commit_callbacks()

            # creates a no duplicates list from the path tuples
            # list, this will ensure that no duplicate operations
            # exist (this is a critical performance trick)
            path_tuples_list = remove_duplicates and list_util.list_no_duplicates(self.path_tuples_list) or self.path_tuples_list

            # iterates over all the path tuples in
            # path tuples list
            for path_tuple in path_tuples_list:
                # retrieves the operation (name)
                operation = path_tuple[0]

                # creates the path tuple process method name from the operation
                path_tuple_process_method_name = PATH_TUPLE_PROCESS_METHOD_PREFIX + operation

                # retrieves the path tuple process method
                path_tuple_process_method = getattr(self, path_tuple_process_method_name)

                # calls the path tuple process method
                path_tuple_process_method(path_tuple)

            # runs the cleanup
            self._cleanup()

            # runs the reset
            self._reset()

            # calls the "final" commit callbacks
            self._call_commit_callbacks()
        finally:
            # releases the access lock
            self.access_lock.release()

    def rollback(self):
        """
        Reverts all the pending operations in
        the current transaction context.
        All the data pending persistence will
        be dropped.
        """

        # acquires the access lock
        self.access_lock.acquire()

        try:
            # in case the transaction level is zero
            if self.transaction_level == 0:
                # returns immediately
                return
            # in case the transaction level is negative
            elif self.transaction_level < 0:
                # raises the runtime error
                raise RuntimeError("Invalid transaction level")

            # calls the pre (before) rollback callbacks
            self._call_pre_rollback_callbacks()

            # runs the cleanup
            self._cleanup()

            # runs the reset
            self._reset()

            # calls the "final" rollback callbacks
            self._call_rollback_callbacks()
        finally:
            # releases the access lock
            self.access_lock.release()

    def _reset(self):
        """
        Resets the state of the transaction file.
        """

        # empties the path tuples list
        self.path_tuples_list = []

        # resets the transaction level
        self.transaction_level = 0

        # in case the temporary path is a directory removes
        # the temporary path
        os.path.isdir(self.temporary_path) and path_util.remove_directory(self.temporary_path)

    def _cleanup(self):
        """
        Cleans the current temporary path.
        All the data in the temporary path
        will be deleted.
        """

        # retrieves the temporary path items
        temporary_path_items = os.listdir(self.temporary_path)

        # iterates over all the temporary path items
        for temporary_path_item in temporary_path_items:
            # creates the temporary complete path item, by joining the
            # temporary path and the temporary path item
            temporary_complete_path_item = os.path.join(self.temporary_path, temporary_path_item)

            # in case the path does not exist (no need to proceed
            # with removal)
            if not os.path.exists(temporary_complete_path_item):
                # continues the loop
                continue

            # in case the temporary item is a directory
            if os.path.isdir(temporary_complete_path_item):
                # removes the directory in the temporary
                # complete path item
                path_util.remove_directory(temporary_complete_path_item)
            # otherwise it must be a "normal" file
            else:
                # removes the temporary complete path item
                os.remove(temporary_complete_path_item)

    def _add_path_tuple(self, path_tuple):
        """
        Adds a path tuple to the current path
        tuples list.

        :type path_tuple: Tuple
        :param path_tuple: The path tuple to
        be added to the tuples list.
        """

        # adds the path tuple to the path tuples list
        self.path_tuples_list.append(path_tuple)

    def _get_virtual_file_path(self, file_path):
        """
        Retrieves the "virtual" file path for the given
        file path.

        :type file_path: String
        :param file_path: The file path to retrieve
        the "virtual" file path.
        :rtype: String
        :return: The virtual file path.
        """

        # splits the file path into drive and
        # base file path
        _drive, base_file_path = os.path.splitdrive(file_path)

        # strips the base file path
        base_file_path = base_file_path.lstrip("\\/")

        # joins the temporary path and the
        # base file path
        virtual_file_path = os.path.join(self.temporary_path, base_file_path)

        # normalizes the virtual file path
        virtual_file_path = os.path.normpath(virtual_file_path)

        # returns the virtual file path
        return virtual_file_path

    def _is_removed_file_path(self, file_path):
        """
        Checks if the given file path has been removed in
        the current context.
        The fact that the file has been removed in the
        current context foes not imply that it does not exists
        in the context.
        If a write operation has been made after a removal
        the file should be accounted as existent.

        This is a very slow operation and should be used carefully
        otherwise the operation may become clogged.

        :type file_path: String
        :param file_path: The path to the file to be checked
        for removal.
        :rtype: bool
        :return: The result of the file removal check.
        """

        # iterates over all the path tuples in
        # path tuples list to check for the ones
        # that may remove the path
        for path_tuple in self.path_tuples_list:
            # retrieves the first item from the path
            # tuple, the operation value
            operation = path_tuple[0]

            # in case the operation is not of type remove
            # continues the loop no removal
            if not operation == REMOVE_OPERATION: continue

            # unpacks the path tuple (for a remove operation)
            operation, _file_path, _handle_exception, recursive = path_tuple

            # in case the recursive flag is not set (possibly just a
            # normal file an not a directory) and the file path does
            # not matches the one required skips extra verification
            if not recursive and not file_path == _file_path: continue

            # checks if the current iteration file path is
            # a parent path to the path being checked
            is_parent_path = path_util.is_parent_path(file_path, _file_path)

            # in case it's not a parent path continues
            # the loop no removal detected
            if not is_parent_path: continue

            # removal detected
            return True

        # returns false (no removal detected)
        return False

    def _process_path_tuple_add(self, path_tuple):
        """
        Processes a path tuple of type add.
        The remote tuple refers paths to be added
        in persistence.

        :type path_tuple: String
        :param path_tuple: The tuple with the path contents.
        """

        # unpacks the path tuple
        _operation, virtual_file_path, file_path = path_tuple

        # in case the path does not exist (no need to proceed
        # with persistence), it represents a case where a temporary
        # path was request but not used for writing
        if not os.path.exists(virtual_file_path):
            # returns immediately
            return

        # in case the virtual file path is a directory
        if os.path.isdir(virtual_file_path):
            # copies the directory in the virtual path to the directory in the file path
            path_util.copy_directory(virtual_file_path, file_path)
        # otherwise it must be a "normal" file
        else:
            # copies the file in the virtual path to the file in the file path
            path_util.copy_file(virtual_file_path, file_path)

    def _process_path_tuple_add_no_replace(self, path_tuple):
        """
        Processes a path tuple of type add no replace.
        The remote tuple refers paths to be added
        in persistence.
        In this mode no files are replaced in case of name
        collision.

        :type path_tuple: String
        :param path_tuple: The tuple with the path contents.
        """

        # unpacks the path tuple
        _operation, virtual_file_path, file_path = path_tuple

        # in case the path does not exist (no need to proceed
        # with persistence), it represents a case where a temporary
        # path was request but not used for writing
        if not os.path.exists(virtual_file_path):
            # returns immediately
            return

        # in case the virtual file path is a directory
        if os.path.isdir(virtual_file_path):
            # copies the directory in the virtual path to the directory in the file path
            # the copy of the directory is made without replacing existent files
            path_util.copy_directory(virtual_file_path, file_path, False)
        # otherwise it must be a "normal" file
        else:
            # copies the file in the virtual path to the file in the file path
            # the copy of the file is made without replacing an eventual
            # existent file
            path_util.copy_file(virtual_file_path, file_path, False)

    def _process_path_tuple_remove(self, path_tuple):
        """
        Processes a path tuple of type remove.
        The remote tuple refers paths to be removed
        in persistence.

        :type path_tuple: String
        :param path_tuple: The tuple with the path contents.
        """

        # unpacks the path tuple
        _operation, file_path, handle_exception, recursive = path_tuple

        # in case the path does not exist (no need to proceed
        # with removal)
        if not os.path.exists(file_path):
            # returns immediately
            return

        # in case the file path is a directory
        if os.path.isdir(file_path):
            # retrieves the directory items
            directory_items = os.listdir(file_path)

            # in case the recursive mode is active
            if recursive:
                try:
                    # checks the directory for items and removes
                    # the directory in the path (recursively)
                    not directory_items and os.removedirs(file_path)
                except Exception as exception:
                    if not handle_exception: raise exception
            # in case the removal is not recursive
            else:
                try:
                    # checks the directory for items and removes
                    # the directory in the path
                    not directory_items and os.remove(file_path)
                except Exception as exception:
                    if not handle_exception: raise exception
        # otherwise it must be a "normal" file
        else:
            try:
                # removes the file path
                os.remove(file_path)
            except Exception as exception:
                if not handle_exception: raise exception
