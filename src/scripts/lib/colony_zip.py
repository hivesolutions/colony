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

__revision__ = "$LastChangedRevision: 10411 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-09-14 19:26:03 +0100 (ter, 14 Set 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import stat
import types
import zipfile
import cStringIO

BUFFER_LENGTH = 4096
""" The length for the zip operation buffer """

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

class Zip:
    """
    Provides functions to interact with zip files.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def get_directory_paths(self, file_path):
        """
        Returns a list with the paths to the directories contained in the specified zip file.

        @type path: String
        @param path: Path to the zip file.
        @rtype: List
        @return: List of directory paths.
        """

        def length_sorter(first_string, second_string):
            """
            Sorter function that takes into account the
            length of the string.

            @type first_string: String
            @param first_string: The first string to be compared.
            @type second_string: String
            @param second_string: The second string to be compared.
            @rtype: int
            @return: The result of the comparison.
            """

            # returns the result of the comparison of string
            # lengths (bigger or smaller)
            return [-1, 1][len(first_string) > len(second_string)]

        # creates the zip file from the file path
        zip_file = zipfile.ZipFile(file_path)

        # retrieves the name list from the zip file
        name_list = zip_file.namelist()

        # creates the directories list
        directories_list = []

        # iterates over the names in the
        # name list
        for name in name_list:
            # retrieves the
            tokens_list = name.split("/")

            # creates the paths list
            paths_list = []

            # iterates over all the token in the tokens
            # sublist (all except the last token)
            for token in tokens_list[:-1]:
                # sets the previous path
                previous_path = ""

                # in case the paths list is not empty
                if len(paths_list) > 0:
                    # sets the previous paths as the last
                    # element of the paths list
                    previous_path = paths_list[-1]

                # in case the token is not empty
                if not token == "":
                    # adds the complete path (previous path and the token)
                    # to the paths list
                    paths_list.append(previous_path + "/" + token)

            # extends the directories list with the
            # paths list
            directories_list.extend(paths_list)

        # creates a dictionary from the keys
        # and retrieves the keys (directories list)
        directories_list = dict.fromkeys(directories_list).keys()

        # sorts the directories list according to
        # the length sorter
        directories_list.sort(length_sorter)

        # returns the directories list
        return directories_list

    def is_file_path(self, path):
        """
        Indicates if the path is pointing to a file.

        @type path: String
        @param path: File system path.
        @rtype: bool
        @return: Boolean indicating if the path is pointing to a file.
        """

        # splits the path over the slash token
        tokens_list = path.split("/")

        # returns if the last token is empty
        return not tokens_list[-1] == ""

    def get_file_paths(self, file_path):
        """
        Returns a list with the paths to the files contained in the specified zip file.

        @type path: String
        @param path: Path to the zip file.
        @rtype: List
        @return: List of file paths.
        """

        def length_sorter(first_string, second_string):
            """
            Sorter function that takes into account the
            length of the string.

            @type first_string: String
            @param first_string: The first string to be compared.
            @type second_string: String
            @param second_string: The second string to be compared.
            @rtype: int
            @return: The result of the comparison.
            """

            # returns the result of the comparison of string
            # lengths (bigger or smaller)
            return [-1, 1][len(first_string) > len(second_string)]

        # creates the zip file from the file path
        zip_file = zipfile.ZipFile(file_path)

        # retrieves the name list from the zip file
        name_list = zip_file.namelist()

        # creates the files list
        files_list = []

        # iterates over all the names in the names list
        for name in name_list:
            # creates the file name in case it is a file
            file_name = [None, name][self.is_file_path(name)]

            # in case the file name is defined
            if file_name:
                # adds the file name to the files list
                files_list.append(file_name)

        # creates a dictionary from the keys
        # and retrieves the keys (files list)
        files_list = dict.fromkeys(files_list).keys()

        # sorts the files list according to
        # the length sorter
        files_list.sort(length_sorter)

        # returns the files list
        return files_list

    def create_directories(self, file_path, root_directory_path):
        """
        Creates the directory structure contained in the specified zip file.

        @type file_path: String
        @param file_path: Full path to the zip file.
        @type root_directory_path: String
        @param root_directory_path: Full path to the place where the directory structure will be created.
        """

        # retrieves the directory paths list from the file path
        directory_paths_list = self.get_directory_paths(file_path)

        # in case the root directory path does not exist
        if not os.path.isdir(root_directory_path):
            # creates the root directory path
            os.mkdir(root_directory_path)

        # iterates over the the directories in the directory
        # paths list
        for directories in directory_paths_list:
            # splits the directories in the slash token
            directories = directories.split("/")

            # starts the prefix value
            prefix = ""

            # iterates over the directories
            for directory in directories:
                # retrieves the directory name joining the prefix and
                # the directory name
                directory_name = os.path.join(prefix, directory)

                # joins the directory name with the root directory path
                # to creates the current directory path
                directory_path = os.path.join(root_directory_path, directory_name)

                # in case the directory is defined and the path does not
                # exist
                if directory and not os.path.isdir(directory_path):
                    # creates the directory for the directory path
                    os.mkdir(directory_path)

                # sets the prefix as the directory name
                prefix = directory_name

    def create_files(self, file_path, root_directory_path):
        """
        Extracts the files contained in the specified zip file.

        @type file_path: String
        @param file_path: Full path to the zip file.
        @type root_directory_path: String
        @param root_directory_path: Full path to the place where the files will be extracted to.
        """

        # opens the zip file for the given file path
        zip_file = zipfile.ZipFile(file_path)

        # retrieves the file paths
        file_paths_list = self.get_file_paths(file_path)

        # iterates over all the file names in the file paths list
        for file_name in file_paths_list:
            # retrieves the complete file path of the file name
            full_path = os.path.join(root_directory_path, file_name)

            # opens the file in write mode
            file = open(full_path, "wb")

            # reads the zip file contents
            zip_file_contents = zip_file.read(file_name)

            # creates a new string buffer
            string_buffer = cStringIO.StringIO()

            # writes the zip file contents into the string buffer
            string_buffer.write(zip_file_contents)

            # seeks to the beginning of the buffer
            string_buffer.seek(0)

            # reads the data from the string buffer
            data = string_buffer.read(BUFFER_LENGTH)

            # iterates while there is data available
            while data:
                # writes the data to the file
                file.write(data)

                # reads the data from the string buffer
                data = string_buffer.read(BUFFER_LENGTH)

            # closes the file
            file.close()

    def zip(self, zip_file_path, input_directory, file_path_list = None):
        """
        Compresses the contents of the provided directory into a zip file.

        @type zip_file_path: String
        @param zip_file_path: Full path to the zip file.
        @type input_directory: String
        @param input_directory: Full path to the directory one wants to compress.
        @type file_path_list: List
        @param file_path_list: Optional list of paths to the files one wants to zip.
        """

        # retrieves the absolute paths for both
        # zip file and the input directory
        zip_file_path = os.path.abspath(zip_file_path)
        input_directory = os.path.abspath(input_directory)

        # in case the input directory is valid and is a directory
        if input_directory and os.path.isdir(input_directory):
            # creates a  new zip file for writing in deflated mode
            zip_file = zipfile.ZipFile(zip_file_path, "w", compression = zipfile.ZIP_DEFLATED)

            # in case the file paths list does not exit
            if not file_path_list:
                # retrieves the fule paths from the input directory
                # as the file path list
                file_path_list = get_file_paths(input_directory)

            # iterates over all the file paths
            # in the file path list
            for file_path in file_path_list:
                # retrieves the file path by joining the path
                file_path = os.path.join(input_directory, file_path)

                # retrieves the output file path
                output_file_path = file_path[len(input_directory):len(file_path)]

                # retrieves the output file path type
                output_file_path_type = type(output_file_path)

                # in case the output file path type is unicode
                if output_file_path_type == types.UnicodeType:
                    # encodes the output file path with the default encoding
                    output_file_path_encoded = output_file_path.encode(DEFAULT_ENCODING)

                # writes the file in the path to the zip file
                zip_file.write(file_path, output_file_path_encoded)

            # closes the zip file
            zip_file.close()

    def unzip(self, zip_file_path, output_directory):
        """
        Extracts a zip file to the specified directory.

        @type zip_file_path: String
        @param zip_file_path: Full path to the zip file.
        @type output_directory: String
        @param output_directory: Full path to the directory where one wants to extract the zip file to.
        """

        # retrieves the zip file absolute path
        zip_file_path = os.path.abspath(zip_file_path)
        output_directory = os.path.abspath(output_directory)
        if os.path.isfile(zip_file_path):
            self.create_directories(zip_file_path, output_directory)
            self.create_files(zip_file_path, output_directory)

def get_file_paths(path, returned_path_list = None):
    """
    Returns a list with full paths to all files contained within the specified directory.

    @type path: String
    @param path: The root path from which all file paths will be retrieved.
    @type returned_path_list: List
    @param returned_path_list: The list where all the paths will be stored (used in recursive calls).
    @rtype: List
    @return: A list of absolute file paths.
    """

    # in case the returned path list is not defined
    if returned_path_list == None:
        # sets the default returned path list
        returned_path_list = []

    # retrieves the directory list for the path
    dir_list = os.listdir(path)

    # iterates over all the file in the directory
    for file_name in dir_list:
        # creates the full path by joining the path and the file name
        full_path = os.path.join(path, file_name)

        # retrieves the mode from the path
        mode = os.stat(full_path)[stat.ST_MODE]

        # in case the path is a directory
        if stat.S_ISDIR(mode):
            # retrieves the file paths for the directory path
            get_file_paths(full_path, returned_path_list)
        else:
            # adds the full path to the returned path
            returned_path_list.append(full_path)

    # returns the returned path list
    return returned_path_list
