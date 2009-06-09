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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import getopt
import sys

import colony_configuration

import colony.plugins.plugin_system
import colony.plugins.util

USAGE = "Help:\n\
--help[-h] - prints this message\n\
--verbose[-v] - starts the program in verbose mode\n\
--debug[-d] - starts the program in debug mode\n\
--plugin-dir[-p]=(PLUGIN_DIR_1;PLUGIN_DIR_2;...) - sets the series of plugin directories to use"
""" The usage string for the command line arguments """

def usage():
    """
    Prints the usage for the command line.
    """

    print USAGE

def run(plugin_path, verbose = False, debug = False, noloop = False, container = "default", attributes_map = {}):
    """
    Starts the loading of the plugin manager.

    @type plugin_path: String
    @param plugin_path: The set of paths to the various plugin locations separated by a semi-column.
    @type verbose: bool
    @param verbose: If the log is going to be of type verbose.
    @type debug: bool
    @param debug: If the log is going to be of type debug.
    @type noloop: bool
    @param noloop: If the plugin manager is going to run in a loop.
    @type container: String
    @param container: The name of the plugin manager container.
    @type container: Dictionary
    @param container: The name of the plugin manager container.
    """

    # checks if the path is not empty
    if not plugin_path == None:
        plugin_paths = plugin_path.split(";")
    else:
        plugin_paths = []

    # sets the plugin manager as a global variable
    global plugin_manager

    # retrieves the current executing platform
    platform = colony.plugins.util.get_environment()

    # creates the plugin manager with the given plugin paths
    plugin_manager = colony.plugins.plugin_system.PluginManager(plugin_paths, platform, [], not noloop, container, attributes_map)

    # conditional logging import (depending on the current environment)
    if platform == colony.plugins.util.CPYTHON_ENVIRONMENT:
        import logging
    elif platform == colony.plugins.util.JYTHON_ENVIRONMENT:
        import colony.plugins.dummy_logging as logging
    elif platform == colony.plugins.util.IRON_PYTHON_ENVIRONMENT:
        import colony.plugins.dummy_logging as logging

    # sets the logging level for the plugin manager logger
    if debug:
        plugin_manager.start_logger(logging.DEBUG)
    elif verbose:
        plugin_manager.start_logger(logging.INFO)
    else:
        plugin_manager.start_logger(logging.WARN)

    # starts and loads the plugin system
    plugin_manager.load_system()

def main():
    """
    The main entry point of the application.
    """

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvdnc:a:m:p:", ["help", "verbose", "debug", "noloop", "container=", "attributes=", "manager_dir=", "plugin_dir="])
    except getopt.GetoptError, error:
        # prints help information and exit
        # will print something like "option -a not recognized"
        print str(error)
        usage()
        sys.exit(2)
    verbose = False
    debug = False
    noloop = False
    container = "default"
    attributes_map = None
    manager_path = None
    plugin_path = None
    for option, value in opts:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-d", "--debug"):
            debug = True
        elif option in ("-n", "--noloop"):
            noloop = True
        elif option in ("-c", "--container"):
            container = value
        elif option in ("-a", "--attributes"):
            attributes_map = parse_attributes(value)
        elif option in ("-m", "--manager_dir"):
            manager_path = value
        elif option in ("-p", "--plugin_dir"):
            plugin_path = value
        else:
            assert False, "unhandled option"

    # sets the prefix path for the plugins
    if manager_path:
        prefix_path = manager_path + "/../../"
    else:
        prefix_path = "../../"

    # parses the configuration options
    verbose, debug, plugin_path = parse_configuration(verbose, debug, plugin_path, prefix_path);

    # strips the plugin path around the semi-colon character
    plugin_path_striped = plugin_path.strip(";")

    # starts the running process
    run(plugin_path_striped, verbose, debug, noloop, container, attributes_map)

def parse_attributes(attributes_string):
    # creates an attributes map
    attributes_map = {}

    # strips the attributes string
    attributes_string_stripped = attributes_string.strip()

    # splits the attributes string
    attributes_string_list = attributes_string_stripped.split(",")

    # iterates over all the attributes string list
    for attributes_string_item in attributes_string_list:
        # strips the attributes string item
        attributes_string_item_stripped = attributes_string_item.strip()

        # splits the attributes string item
        attributes_string_item_splitted = attributes_string_item_stripped.split(":")

        if len(attributes_string_item_splitted) == 2:
            attribute_key, attribute_value = attributes_string_item_splitted
            attributes_map[attribute_key] = attribute_value

    return attributes_map

def parse_configuration(verbose, debug, plugin_path, prefix_path):
    # retrieves the colony configuration contents
    colony_configuration_contents = dir(colony_configuration)

    # in case the verbose variable is defined in the colony configuration
    if "verbose" in dir(colony_configuration):
        verbose = colony_configuration.verbose

    # in case the debug variable is defined in the colony configuration
    if "debug" in dir(colony_configuration):
        debug = colony_configuration.debug

    if plugin_path:
        plugin_path += ";"
    else:
        # creates a new plugin path string
        plugin_path = ""

    # iterates over all the colony configuration plugin paths
    for plugin_path_item in colony_configuration.plugin_path_list:
        parsed_plugin_path = plugin_path_item.replace("%prefix_path%", prefix_path)
        plugin_path += parsed_plugin_path + ";"

    return (verbose, debug, plugin_path)

if __name__ == "__main__":
    main()
