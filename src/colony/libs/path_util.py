#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import sys
import stat

BUFFER_SIZE = 4096
""" The size of the buffer for file operations """

LONG_PATH_PREFIX = u"\\\\?\\"
""" The windows long path prefix """

CURRENT_DIRECTORY = "."
""" The current directory string """

PARENT_DIRECTORY = ".."
""" The parent directory string """

SEPARATOR = "/"
""" The directory separator string """

NT_PLATFORM_VALUE = "nt"
""" The nt platform value """

CE_PLATFORM_VALUE = "ce"
""" The ce platform value """

DOS_PLATFORM_VALUE = "dos"
""" The dos platform value """

WINDOWS_PLATFORMS_VALUE = (
    NT_PLATFORM_VALUE,
    CE_PLATFORM_VALUE,
    DOS_PLATFORM_VALUE
)
""" The windows platform value """

def normalize_path(path):
    """
    Normalizes the given path, using the characteristics
    of the current environment.
    In windows this function adds support for long path names.

    @type path: String
    @param path: The path to be normalized.
    @rtype: String
    @return: The normalized path.
    """

    # normalizes the path
    normalized_path = os.path.normpath(path)

    # retrieves the current os name
    os_name = os.name

    # in case the current operative system is windows based and
    # the normalized path does not start with the long path prefix
    if os_name in WINDOWS_PLATFORMS_VALUE and not normalized_path.startswith(LONG_PATH_PREFIX):
        # creates the path in the windows mode, adds
        # the support for long path names with the prefix token
        normalized_path = LONG_PATH_PREFIX + normalized_path

    # returns the normalized path
    return normalized_path

def align_path(path):
    """
    Aligns the given path, converting all the system specific
    characters into the defined virtual separators.
    The retrieved path is system independent.

    @type path: String
    @param path: The path to the aligned (become system independent).
    @rtype: String
    @return: The aligned path (system independent).
    """

    # aligns the path replacing the backslashes with
    # "normal" slashes
    aligned_path = path.replace("\\", "/")

    # returns the aligned path
    return aligned_path

def copy_directory(source_path, target_path, replace_files = True):
    """
    Copies the directory in the given source path to the
    target path.
    The copy is recursive and so the sub directories are copied too.
    The directory in the target path is created if not existent
    or overwritten if existent.

    @type source_path: String
    @param source_path: The path to the source directory.
    @type target_path: String
    @param target_path: The path to the target directory.
    @type replace_files: bool
    @param replace_files: If the files should be replaced
    in case duplicate files are found.
    """

    # in case the source path is not a directory
    if not os.path.isdir(source_path):
        # raises an exception
        raise Exception("Source path is not a directory: '%s" % source_path)

    # in case the target path does not exist
    if not os.path.exists(target_path):
        # creates the target path directory
        os.makedirs(target_path)

    # in case the target path is not a directory
    if not os.path.isdir(target_path):
        # raises an exception
        raise Exception("Target path is not a directory: '%s" % target_path)

    # retrieves the directory list from the source path
    directory_list = os.listdir(source_path)

    # iterates over all the entry names in the
    # directory list
    for entry_name in directory_list:
        # creates the entry full path from the source path
        # and the entry name
        entry_full_path = os.path.join(source_path, entry_name)

        # creates the target full path
        target_full_path = os.path.join(target_path, entry_name)

        # retrieves the mode
        mode = os.stat(entry_full_path)[stat.ST_MODE]

        # in case it is a directory
        if stat.S_ISDIR(mode):
            # copies the (sub) directory
            copy_directory(entry_full_path, target_full_path, replace_files)
        # otherwise it's a file and must be copied
        else:
            # checks if the target full path exists
            target_full_path_exists = os.path.exists(target_full_path)

            # in case the replace files flag is not set and the
            # target full path exists (avoids replacing file)
            if not replace_files and target_full_path_exists:
                # continues the loop (no copy)
                continue

            # copies the entry to the target path
            copy_file(entry_full_path, target_full_path)

def copy_file(source_path, target_path):
    """
    Copies a file in the given source path to the
    target path.
    The file in the target path is created if not existent
    or overwritten if existent.

    @type source_path: String
    @param source_path: The path to the source file.
    @type target_path: String
    @param target_path: The path to the target file.
    """

    # opens the source file
    source_file = open(source_path, "rb")

    # opens the target file
    target_file = open(target_path, "wb")

    try:
        # iterates continuously
        while True:
            # reads contents from the source file
            contents = source_file.read(BUFFER_SIZE)

            # in case the contents are not valid
            if not contents:
                # breaks the cycle
                break

            # writes the contents in the target file
            target_file.write(contents)
    finally:
        # closes the source file
        source_file.close()

        # closes the target file
        target_file.close()

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

def link(target_path, link_path, link_name = True):
    """
    Creates a link between the target path and the link
    path given.
    In case the link name flag is set the link is relative
    and only the base name of the link path is used.

    @type target_path: String
    @param target_path: The target path to the link.
    @type link_path: String
    @param link_path: The path to the link.
    @type link_name: bool
    @param link_name: If the link base name should be used
    instead of the full path.
    """

    # in case the current platform is windows
    if os.name == NT_PLATFORM_VALUE:
        # copies the directory (copy link)
        copy_link(target_path, link_path)
    else:
        # retrieves the base name of the target path
        # as the target path name
        target_path_name = os.path.basename(target_path)

        # selects the correct target path based in the link name flag
        target_path = link_name and target_path_name or target_path

        # creates the symbolic link to the target path
        # using the link path
        os.symlink(target_path, link_path) #@UndefinedVariable

def copy_link(target_path, link_path):
    """
    Copies the target path into the path defined
    in the link path.
    This function acts as a stub for the symlink function.

    @type target_path: String
    @param target_path: The target path to the link.
    @type link_path: String
    @param link_path: The path to the "link".
    """

    # in case the directory exists
    if os.path.exists(link_path):
        # removes the directory in the link path
        remove_directory(link_path)

    # copies the directory in the target path to the link path
    copy_directory(target_path, link_path)

def ensure_file_path(file_path, default_file_path):
    """
    Ensures that the given file path is set with
    contents.
    In case the file does not exists the file in the default
    file path is copied to the file path.

    @type file_path: String
    @param file_path: The file path to ensure contents.
    @type default_file_path: String
    @param default_file_path: The path to the file to be
    used in case the file path does not exist.
    """

    # checks if the file exists
    file_exists = os.path.exists(file_path)

    # in case the file already exists
    if file_exists:
        # returns immediately
        return

    # retrieves the file directory path
    file_directory_path = os.path.dirname(file_path)

    # checks if the file directory path exists
    file_directory_path_exists = os.path.isdir(file_directory_path)

    # in case the file directory path does not exists creates the
    # directories required recursively
    not file_directory_path_exists and os.makedirs(file_directory_path)

    # opens the default file
    default_file = open(default_file_path, "rb")

    try:
        # reads the default file contents
        default_file_contents = default_file.read()
    finally:
        # closes the default file
        default_file.close()

    # opens the file
    file = open(file_path, "wb")

    try:
        # writes the default file contents to it
        # in order to set the value
        file.write(default_file_contents)
    finally:
        # closes the file
        file.close()

def relative_path_windows(path, start_path = CURRENT_DIRECTORY):
    """
    "Calculates" the relative path between the base path
    and the given "start" path.
    This version of the calculus is target at windows platforms.

    @type path: String
    @param path: The path to be used as "target".
    @type start_path: String
    @param start_path: The path to be used as starting point.
    @rtype: String
    @return: The relative path between both paths.
    """

    # in case the path is not defined (error)
    if not path:
        # raises a base value error
        raise ValueError("no path specified")

    # retrieves the various util values from the start
    # path and path
    start_is_unc, start_prefix, start_list = _abspath_split(start_path)
    path_is_unc, path_prefix, path_list = _abspath_split(path)

    # in case one of the paths is of type unc and the other
    # is not (error)
    if path_is_unc ^ start_is_unc:
        # raises a value error
        raise ValueError("cannot mix unc and non-unc paths %s and %s" % (path, start_path))
    # in
    if path_prefix.lower() != start_prefix.lower():
        if path_is_unc:
            # raises a value error
            raise ValueError("path is on unc root %s, start on unc root %s" % (path_prefix, start_prefix))
        else:
            # raises a value error
            raise ValueError("path is on drive %s, start on drive %s" % (path_prefix, start_prefix))

    # works out how much of the file path
    # is shared by start and path
    index = 0

    # iterates over both sub paths list to check for differences
    for start_sub_path, sub_path in zip(start_list, path_list):
        # in case the sub paths are different
        if start_sub_path.lower() != sub_path.lower():
            # breaks the loop
            break

        # increment the index
        index += 1

    # calculates the "relatives" list using the start list and path list
    # as reference
    relatives_list = [PARENT_DIRECTORY] * (len(start_list) - index) + path_list[index:]

    # in case the are not relatives list
    # (is the same directory)
    if not relatives_list:
        # returns the current directory
        return CURRENT_DIRECTORY

    # returns the result of joining all
    # the relatives list
    return os.path.join(*relatives_list)

def relative_path_posix(path, start = CURRENT_DIRECTORY):
    """
    "Calculates" the relative path between the base path
    and the given "start" path.
    This version of the calculus is target at posix platforms.

    @type path: String
    @param path: The path to be used as "target".
    @type start_path: String
    @param start_path: The path to be used as starting point.
    @rtype: String
    @return: The relative path between both paths.
    """

    # in case the path is not defined (error)
    if not path:
        # raises a base value error
        raise ValueError("no path specified")

    # retrieves the sub paths list for both the start path and the path
    start_list = [value for value in os.path.abspath(start).split(SEPARATOR) if value]
    path_list = [value for value in os.path.abspath(path).split(SEPARATOR) if value]

    # works out how much of the file path is shared by start and path
    index = len(os.path.commonprefix([start_list, path_list]))

    # calculates the "relatives" list using the start list and path list
    # as reference
    relatives_list = [PARENT_DIRECTORY] * (len(start_list) - index) + path_list[index:]

    # in case the are not relatives list
    # (is the same directory)
    if not relatives_list:
        # returns the current directory
        return CURRENT_DIRECTORY

    # returns the result of joining all
    # the relatives list
    return os.path.join(*relatives_list)

def _abspath_split(path):
    """
    Method for util splitting of the path into
    is unc, prefix and path list.
    The values are returned in a tuple.

    @type path: String
    @param path: The path to be checked.
    @rtype: Tuple
    @return: A tuple containing the is unc, prefix and
    path list util values.
    """

    # normalizes the path and the retrieves
    # the absolute path and then splits it into
    # prefix and rest
    path = os.path.normpath(path)
    absolute_path = os.path.abspath(path)
    prefix, rest = os.path.splitunc(absolute_path)

    # converts the prefix to boolean for checking
    # if the path is unc based
    is_unc = bool(prefix)
    if not is_unc:
        # splits the absolute path for drive checking
        prefix, rest = os.path.splitdrive(absolute_path)

    # retrieves the list of various (sub) paths from the rest
    path_list = [value for value in rest.split(SEPARATOR) if value]

    # returns the tuple value
    return is_unc, prefix, path_list

# checks if the current platform is of type windows
if NT_PLATFORM_VALUE in sys.builtin_module_names or CE_PLATFORM_VALUE in sys.builtin_module_names:
    # sets the separator value and the relative
    # path method values (for windows)
    SEPARATOR = "\\"
    relative_path = relative_path_windows
# otherwise it should be a posix environment
else:
    # sets the separator value and the relative
    # path method values (for posix)
    SEPARATOR = "/"
    relative_path = relative_path_posix
