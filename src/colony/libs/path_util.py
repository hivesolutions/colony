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

__version__ = "1.0.3"
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
import sys
import stat

BUFFER_SIZE = 4096
""" The size of the buffer for file operations """

LONG_PATH_PREFIX = "\\\\?\\"
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

    :type path: String
    :param path: The path to be normalized.
    :rtype: String
    :return: The normalized path.
    """

    # retrieves the current os name
    os_name = os.name

    # in case the current operative system is windows based and
    # the normalized path does start with the long path prefix it
    # must be removed to allow a "normal" path normalization
    if os_name in WINDOWS_PLATFORMS_VALUE and path.startswith(LONG_PATH_PREFIX):
        # removes the long path prefix from the path
        path = path[4:]

    # checks if the path is absolute
    is_absolute_path = os.path.isabs(path)

    # in case the path is not absolute (creates problem in windows
    # long path support)
    if os_name in WINDOWS_PLATFORMS_VALUE and not is_absolute_path:
        # converts the path to absolute
        path = os.path.abspath(path)

    # normalizes the path
    normalized_path = os.path.normpath(path)

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

    :type path: String
    :param path: The path to the aligned (become system independent).
    :rtype: String
    :return: The aligned path (system independent).
    """

    # aligns the path replacing the backslashes with
    # "normal" slashes
    aligned_path = path.replace("\\", "/")

    # returns the aligned path
    return aligned_path

def copy_directory(source_path, target_path, replace_files = True, copy_hidden = True):
    """
    Copies the directory in the given source path to the
    target path.
    The copy is recursive and so the sub directories are copied too.
    The directory in the target path is created if not existent
    or overwritten if existent.
    It's possible to control the copying of hidden files using the
    optional copy hidden flag parameter.

    :type source_path: String
    :param source_path: The path to the source directory.
    :type target_path: String
    :param target_path: The path to the target directory.
    :type replace_files: bool
    :param replace_files: If the files should be replaced
    in case duplicate files are found.
    :type copy_hidden: bool
    :param copy_hidden: If the files considered by the os to
    be of type hidden should be copied..
    """

    # normalizes both the target and source paths
    # (avoids path problems in various platforms)
    source_path = normalize_path(source_path)
    target_path = normalize_path(target_path)

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
        # and the entry name and normalizes it
        entry_full_path = os.path.join(source_path, entry_name)
        entry_full_path = normalize_path(entry_full_path)

        # creates the target full path and normalizes it
        target_full_path = os.path.join(target_path, entry_name)
        target_full_path = normalize_path(target_full_path)

        # retrieve the base name for the current entry
        # for hidden checking
        entry_base_name = os.path.basename(entry_full_path)

        # in case the copy hidden flag is not set and the base
        # name refers a hidden file or directory
        if not copy_hidden and entry_base_name.startswith("."):
            # continues the loop (no copy)
            continue

        # retrieves the mode
        mode = os.lstat(entry_full_path)[stat.ST_MODE]

        # in case it is a directory
        if stat.S_ISDIR(mode):
            # copies the (sub) directory
            copy_directory(entry_full_path, target_full_path, replace_files, copy_hidden)
        # in case it is a symbolic link (special
        # care must be taken in such case)
        elif stat.S_ISLNK(mode):
            # copies the symbolic link to the target path
            copy_link(entry_full_path, target_full_path, replace_files)
        # otherwise it's a file and must be copied
        else:
            # copies the entry to the target path
            copy_file(entry_full_path, target_full_path, replace_files)

def copy_link(source_path, target_path, replace_file = True):
    """
    Copies a symbolic link in the given source path to the
    target path.
    The symbolic link in the target path is created if not existent
    or overwritten if existent.

    :type source_path: String
    :param source_path: The path to the source symbolic link.
    :type target_path: String
    :param target_path: The path to the target symbolic link.
    :type replace_file: bool
    :param replace_file: If the file should be replaced
    in existent symbolic link is found.
    """

    # checks if the target path (symbolic link) exists
    target_file_exists = os.path.exists(target_path)

    # in case the replace file flag is not set and the
    # target path (symbolic link) exists (avoids
    # replacing symbolic link)
    if not replace_file and target_file_exists:
        # returns immediately (no copy)
        return

    # reads the link target (path) from the source path
    # and then uses that value to create the link in the
    # target path (link copy)
    link_target = os.readlink(source_path) #@UndefinedVariable
    os.symlink(link_target, target_path) #@UndefinedVariable

def copy_file(source_path, target_path, replace_file = True):
    """
    Copies a file in the given source path to the
    target path.
    The file in the target path is created if not existent
    or overwritten if existent.

    :type source_path: String
    :param source_path: The path to the source file.
    :type target_path: String
    :param target_path: The path to the target file.
    :type replace_file: bool
    :param replace_file: If the file should be replaced
    in existent files is found.
    """

    # normalizes both the target and source paths
    # (avoids path problems in various platforms)
    source_path = normalize_path(source_path)
    target_path = normalize_path(target_path)

    # checks if the target path (file) exists
    target_file_exists = os.path.exists(target_path)

    # in case the replace file flag is not set and the
    # target path (file) exists (avoids replacing file)
    if not replace_file and target_file_exists:
        # returns immediately (no copy)
        return

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

    :type directory_path: String
    :param directory_path: The path to the directory to be removed.
    """

    # normalizes the directory path
    # (avoids path problems in various platforms)
    directory_path = normalize_path(directory_path)

    # creates the list of paths for the directory path
    paths_list = [os.path.join(directory_path, file_path) for file_path in os.listdir(directory_path)]

    # iterates over all the paths in the paths
    # list to remove them
    for path in paths_list:
        # normalizes the path (avoids
        # problems in various platforms)
        path = normalize_path(path)

        # in case the path is a directory
        if os.path.isdir(path):
            # removes the directory
            remove_directory(path)
        # otherwise it must be a "normal" file
        else:
            # removes the path
            os.remove(path)

    # removes the directory
    os.rmdir(directory_path)

def link(target_path, link_path, link_name = True, replace = False):
    """
    Creates a link between the target path and the link
    path given.
    In case the link name flag is set the link is relative
    and only the base name of the link path is used, this
    should provide extra flexibility to the link.

    An optional replace flag may be set so that the link is
    removed in case it already exists.

    :type target_path: String
    :param target_path: The target path to the link.
    :type link_path: String
    :param link_path: The path to the link.
    :type link_name: bool
    :param link_name: If the link base name should be used
    instead of the full path.
    :type replace: bool
    :param replace: If the link path should be replace (overwritten)
    in case it already exists (file overlapping).
    """

    # in case there is an existent link in the link path
    # it must be removed (the link may be a directory), this
    # behavior is only accomplished when the replace flag
    # parameter is set
    if replace and os.path.islink(link_path): os.remove(link_path)
    elif replace and os.path.isdir(link_path): remove_directory(link_path)

    # in case the current platform is windows
    if os.name == NT_PLATFORM_VALUE:
        # copies the directory (symbolic link through
        # the copy method)
        link_copy(target_path, link_path)
    # otherwise the platform probably supports the
    # normal file linking system (symbolic link)
    else:
        # retrieves the base name of the target path
        # as the target path name
        target_path_name = os.path.basename(target_path)

        # selects the correct target path based in the link name flag
        target_path = link_name and target_path_name or target_path

        # creates the symbolic link to the target path
        # using the link path
        os.symlink(target_path, link_path) #@UndefinedVariable

def link_copy(target_path, link_path):
    """
    Copies the target path into the path defined
    in the link path.
    This function acts as a stub for the symlink function.

    :type target_path: String
    :param target_path: The target path to the link.
    :type link_path: String
    :param link_path: The path to the "link".
    """

    # in case the directory exists
    if os.path.exists(link_path):
        # removes the directory in the link path
        remove_directory(link_path)

    # in case the target path reference a directory
    # a directory copy must be done
    if os.path.isdir(target_path):
        # copies the directory in the target path to the link path
        copy_directory(target_path, link_path)
    # otherwise a "simple" file copy is done
    else:
        # copies the file in the target path to the link path
        copy_file(target_path, link_path)

def ensure_file_path(file_path, default_file_path):
    """
    Ensures that the given file path is set with
    contents.
    In case the file does not exists the file in the default
    file path is copied to the file path.

    :type file_path: String
    :param file_path: The file path to ensure contents.
    :type default_file_path: String
    :param default_file_path: The path to the file to be
    used in case the file path does not exist.
    """

    # normalizes both the base and default
    # file paths (avoids path problems in
    # various platforms)
    file_path = normalize_path(file_path)
    default_file_path = normalize_path(default_file_path)

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

def is_parent_path(path, parent_path):
    """
    Checks if the given parent path is a parent
    to the given path.
    A parent path is a path that contains the given
    path at any relative depth.

    :type path: String
    :param path: The (base) path for the checking.
    :type parent_path: String
    :param parent_path: The path to be checked for
    parenting.
    :rtype: bool
    :return: The result of the checking for parenting.
    """

    # checks the relative path between the path and
    # the parent path
    _relative_path = relative_path(path, parent_path)

    # in case the relative path start with the
    # parent directory character
    if _relative_path.startswith(PARENT_DIRECTORY):
        # returns false (invalid)
        return False
    # otherwise it muse be a parent path
    else:
        # returns false (invalid)
        return True

def _relative_path_windows(path, start_path = CURRENT_DIRECTORY):
    """
    "Calculates" the relative path between the base path
    and the given "start" path.
    This version of the calculus is target at windows platforms.

    :type path: String
    :param path: The path to be used as "target".
    :type start_path: String
    :param start_path: The path to be used as starting point.
    :rtype: String
    :return: The relative path between both paths.
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

def _relative_path_posix(path, start = CURRENT_DIRECTORY):
    """
    "Calculates" the relative path between the base path
    and the given "start" path.
    This version of the calculus is target at posix platforms.

    :type path: String
    :param path: The path to be used as "target".
    :type start_path: String
    :param start_path: The path to be used as starting point.
    :rtype: String
    :return: The relative path between both paths.
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

    :type path: String
    :param path: The path to be checked.
    :rtype: Tuple
    :return: A tuple containing the is unc, prefix and
    path list util values.
    """

    # normalizes the path and the retrieves
    # the absolute path and then splits it into
    # prefix and rest
    path = os.path.normpath(path)
    absolute_path = os.path.abspath(path)
    prefix, rest = os.path.splitunc(absolute_path) #@UndefinedVariable

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
    relative_path = _relative_path_windows
# otherwise it should be a posix environment
else:
    # sets the separator value and the relative
    # path method values (for posix)
    SEPARATOR = "/"
    relative_path = _relative_path_posix
