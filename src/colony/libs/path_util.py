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
import stat

BUFFER_SIZE = 4096
""" The size of the buffer for file operations """

LONG_PATH_PREFIX = u"\\\\?\\"
""" The windows long path prefix """

NT_PLATFORM_VALUE = "nt"
""" The nt platform value """

DOS_PLATFORM_VALUE = "dos"
""" The dos platform value """

WINDOWS_PLATFORMS_VALUE = (NT_PLATFORM_VALUE, DOS_PLATFORM_VALUE)
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

def copy_directory(source_path, target_path):
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
            copy_directory(entry_full_path, target_full_path)
        else:
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
