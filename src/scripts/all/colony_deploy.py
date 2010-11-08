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

__revision__ = "$LastChangedRevision: 9911 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-08-30 11:04:12 +0100 (seg, 30 Ago 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import json
import types
import shutil
import getopt
import tempfile

VERSION = "${out value=colony_deploy.version /}"
""" The version value """

RELEASE = "${out value=release_version /}"
""" The release value """

BUILD = "${out value=build_version /}"
""" The build value """

RELEASE_DATE = "${out value=date /}"
"""" The release date value """

USAGE = "Help:\n\
--help[-h] - prints this message\n\
--verbose[-v] - starts the program in verbose mode\n\
--manager_dir[-m]=(PLUGIN_DIR) - sets the plugin directory to be used by the deployer"
""" The usage string for the command line arguments """

BRANDING_TEXT = "Hive Colony Deployer %s (Hive Solutions Lda. r%s:%s %s)"
""" The branding text value """

VERSION_PRE_TEXT = "Python "
""" The version pre text value """

DEFAULT_PATH_VALUE = os.path.dirname(os.path.realpath(__file__))
""" The default path """

DEFAULT_MANAGER_PATH_VALUE = os.path.normpath(os.path.realpath(DEFAULT_PATH_VALUE + "/../.."))
""" The default manager path """

MAIN_FILE_VALUE = "main_file"
""" The main file value """

RESOURCES_VALUE = "resources"
""" The resources value """

COLONY_HOME_ENVIRONMENT = "COLONY_HOME"
""" The colony home environment variable name """

SEPCIFICATION_FILE_NAME = "specification.json"
""" The specification file name """

RELATIVE_DEPLOYMENT_PATH = "plugins"
""" The path relative to the manager path for the deployment """

REQUIRED_VALUES = ("platform", "id", "version")
""" The tuple of required values """

def print_information():
    """
    Prints the system information for the command line.
    """

    # print the branding information text
    print BRANDING_TEXT % (VERSION, RELEASE, BUILD, RELEASE_DATE)

    # print the python information
    print VERSION_PRE_TEXT + sys.version

def usage():
    """
    Prints the usage for the command line.
    """

    print USAGE

def update_system_path():
    """
    Updates the current system path, with the extra
    paths required for the normal functioning.
    """

    # adds the default path to the system path
    sys.path.insert(0, os.path.normpath(os.path.realpath(DEFAULT_PATH_VALUE + "/../lib")))

def log(message, verbose):
    if not verbose:
        return

    print message

def main():
    import colony_zip

    # in case the number of command line arguments
    # is len than two
    if len(sys.argv) < 2:
        # raises an exception
        raise Exception("Invalid number of arguments")

    # retrieves the first argument
    first_argument = sys.argv[1]

    # retrieves the first character of the first argument
    first_argument_character = first_argument[0]

    # in case the first argument is an option
    if first_argument_character in ("-", "--"):
        # the option arguments are all the arguments
        option_arguments = sys.argv[1:]
    else:
        # the first argument is the package file
        option_arguments = sys.argv[2:]

    # processes the arguments options
    options, _args = getopt.getopt(option_arguments, "hvm:", ["help", "verbose", "manager_dir="])

    # retrieves the file system encoding
    file_system_encoding = sys.getfilesystemencoding()

    # starts the options values
    verbose = False

    # retrieves the manager path
    manager_path = os.environ.get(COLONY_HOME_ENVIRONMENT, DEFAULT_MANAGER_PATH_VALUE).decode(file_system_encoding)

    # iterates over all the options
    for option, value in options:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-m", "--manager_dir"):
            manager_path = value.decode(file_system_encoding)

    # prints the console information
    print_information()

    # creates the target path
    target_path = os.path.normpath(manager_path + "/" + RELATIVE_DEPLOYMENT_PATH)

    # creates a new temporary path
    temporary_path = tempfile.mkdtemp()

    # creates the specification file path
    specification_file_path = os.path.normpath(temporary_path + "/" + SEPCIFICATION_FILE_NAME)

    # retrieves the package path
    package_path = sys.argv[1]

    # in case the package path does not exist
    if not os.path.exists(package_path):
        # raises an exception
        raise Exception("The package path '%s' does not exist" % package_path)

    # prints a log message
    log("Deploying '%s' to '%s'" % (package_path, manager_path), True)

    # prints a log message
    log("Unpacking package file '%s' using zip decoder" % (package_path), verbose)

    # creates a new zip (manager)
    zip = colony_zip.Zip()

    # unzips the package to the temporary path
    zip.unzip(package_path, temporary_path)

    try:
        # prints a log message
        log("Opening specification file '%s'" % (specification_file_path), verbose)

        # opens the specification file
        specification_file = open(specification_file_path)

        try:
            # reads the specification file, retrieving the contents
            specification_file_contents = specification_file.read()
        finally:
            # closes the specification file
            specification_file.close()

        # loads the json specification file contents
        specification = json.loads(specification_file_contents)

        # retrieves the main file
        main_file = specification[MAIN_FILE_VALUE]

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # prints a log message
        log("Moving resources from '%s' to '%s'" % (temporary_path, target_path), verbose)

        # iterates over all the resources
        for resource in resources:
            # retrieves the resource file path
            resource_file_path = os.path.normpath(temporary_path + "/resources/" + resource)

            # creates the new resource file path
            new_resource_file_path = os.path.normpath(target_path + "/" + resource)

            # retrieves the new resource directory path
            new_resource_directory_path = os.path.dirname(new_resource_file_path)

            # prints a log message
            log("Moving resource file '%s' to '%s'" % (resource_file_path, new_resource_file_path), verbose)

            # in case the new resource directory path does not exist
            if not os.path.exists(new_resource_directory_path):
                # creates the new resource directory path (directories)
                os.makedirs(new_resource_directory_path)

            # copies the resource file as the new resource file
            shutil.copy(resource_file_path, new_resource_file_path)

        # prints a log message
        log("Moving main file '%s' to '%s'" % (resource_file_path, new_resource_file_path), verbose)

        # splits the main file name into name and extension
        main_file_name, _mail_file_extension = os.path.splitext(main_file)

        # creates the new specification file name
        new_specification_file_name = main_file_name + ".json"

        # creates the new specification file path
        new_specification_file_path = os.path.normpath(target_path + "/" + new_specification_file_name)

        # copies the specification file as the new specification file
        shutil.copy(specification_file_path, new_specification_file_path)
    except:
        # re-raises the exception
        raise
    finally:
        # prints a log message
        log("Removing temporary path '%s'" % temporary_path, verbose)

        # removes the temporary path (directory)
        remove_directory(temporary_path)

    # prints a log message
    log("Finished deployment", verbose)

def validate_specification(specification):
    """
    Validates the given specification map, checking if
    all the required values are set.
    In case the validation fails an exception is raised.

    @type specification: Dictionary
    @param specification: The map containing the specification
    values.
    """

    # iterates over all the required values in the required values list
    for required_value in REQUIRED_VALUES:
        # in case the required value is not in the specification
        if not required_value in specification:
            # raises an exception
            raise Exception("Required value '%s' missing in specification file" % (required_value))

def print_specification(specification):
    """
    Prints the specification map information to the
    console.

    @type specification: Dictionary
    @param specification: The map containing the specification
    values.
    """

    # retrieves the required (mandatory) values
    platform = specification["platform"]
    id = specification["id"]
    version = specification["version"]

    # retrieves the optional values
    sub_platforms = specification.get("sub_platforms", [])
    name = specification.get("name", "")
    short_name = specification.get("short_name", "")
    description = specification.get("description", "")
    author = specification.get("author", "")
    capabilities = specification.get("capabilities", [])
    capabilities_allowed = specification.get("capabilities_allowed", [])
    dependencies = specification.get("dependencies", [])
    main_file = specification.get("main_file", [])
    resources = specification.get("resources", [])

    # prints the various values
    print_value("Platform", platform)
    print_value("Sub-Platforms", sub_platforms)
    print_value("Id", id)
    print_value("Name", name)
    print_value("Short Name", short_name)
    print_value("Description", description)
    print_value("Version", version)
    print_value("Author", author)
    print_value("Capabilities", capabilities)
    print_value("Capabilities Allowed", capabilities_allowed)
    print_value("Dependencies", dependencies)
    print_value("Main File", main_file)
    print_value("Resources", resources)

def print_value(key, value):
    # retrieves the type of the value
    value_type = type(value)

    # in case the value is a string
    if value_type in types.StringTypes:
        print key + ": " + value
    # in case the value is a list (of strings)
    elif value_type == types.ListType:
        print key,

        print ":" + str(value)

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

if __name__ == "__main__":
    update_system_path()

    try:
        main()
    except Exception, exception:
        # prints the error information
        print "Error: " + unicode(exception)

        # exits in error
        sys.exit(2)
