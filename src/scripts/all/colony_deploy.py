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
import getopt
import logging

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
--flush[-f] - flushes the current deploy directory\n\
--info[-i] - prints information about the package\n\
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

COLONY_HOME_ENVIRONMENT = "COLONY_HOME"
""" The colony home environment variable name """

COLONY_FILE_EXTENSIONS = (".cbx", ".cpx")
""" The tuple containing all the colony file extensions """

def update_system_path():
    """
    Updates the current system path, with the extra
    paths required for the normal functioning.
    """

    # adds the default path to the system path
    sys.path.insert(0, os.path.normpath(os.path.realpath(DEFAULT_PATH_VALUE + "/../lib")))

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

def main():
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
    options, _args = getopt.getopt(option_arguments, "hfivm:", ["help", "flush", "info", "verbose", "manager_dir="])

    # retrieves the file system encoding
    file_system_encoding = sys.getfilesystemencoding()

    # starts the options values
    flush = False
    info = False
    verbose = False

    # retrieves the manager path
    manager_path = os.environ.get(COLONY_HOME_ENVIRONMENT, DEFAULT_MANAGER_PATH_VALUE).decode(file_system_encoding)

    # iterates over all the options
    for option, value in options:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option in ("-f", "--flush"):
            flush = True
        elif option in ("-i", "--info"):
            info = True
        elif option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-m", "--manager_dir"):
            manager_path = value.decode(file_system_encoding)

    # prints the console information
    print_information()

    # retrieves the package path
    package_path = sys.argv[1]

    # retrieves the logger
    logger = logging.getLogger("default")

    # creates a new stream handler
    stream_handler = logging.StreamHandler()

    # adds the stream handler to the logger
    logger.addHandler(stream_handler)

    # creates a new deployer object
    deployer = colony_deployer.Deployer(manager_path)

    # in case the verbose flag is set
    if verbose:
        # sets the logger level to debug
        logger.setLevel(logging.DEBUG)

        # sets the stream handler level to debug
        stream_handler.setLevel(logging.DEBUG)

    # in case the info flag is set
    if info:
        # prints the deploy info
        deployer.deploy_info(package_path)

        # returns immediately
        return

    # in case the flush flag is set, there is
    # a flushing of the deploy directory
    if flush:
        # deploys the the items in the deploy path
        # for flushing purposes
        deployer.deploy_flush()

        # returns immediately
        return

    # deploys the package in the given path
    deployer.deploy_package(package_path)

if __name__ == "__main__":
    # updates the system path
    update_system_path()

    try:
        # imports the colony references
        import colony_deployer

        # runs the main
        main()
    except Exception, exception:
        # prints the error information
        print "Error: " + unicode(exception)

        # exits in error
        sys.exit(2)
