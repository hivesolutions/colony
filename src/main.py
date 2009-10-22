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
--noloop[-n] - sets the manager to not use the loop mode\n\
--layout_mode[-l]=development/svn_repository/production - sets the layout mode to be used\n\
--run_mode[-r]=development/test/production - sets the run mode to be used\n\
--container[-c]=default - sets the container to be used\n\
--attributes[-a]=... - sets the attributes to be used\n\
--manager_dir[-m]=(PLUGIN_DIR) - sets the plugin directory to be used by the manager\n\
--plugin_dir[-p]=(PLUGIN_DIR_1;PLUGIN_DIR_2;...) - sets the series of plugin directories to use"
""" The usage string for the command line arguments """

DEFAULT_STRING_VALUE = "default"
""" The default string value """

DEFAULT_MANAGER_PATH_VALUE = "."
""" The default manager path """

PREFIX_PATH_PREFIX_VALUE = "%"
""" The prefix path prefix value """

PREFIX_PATH_SUFIX_VALUE = "_prefix_path%"
""" The prefix path sufix value """

LIBRARY_DIRECTORY = "colony/libs"
""" The colony library directory """

def usage():
    """
    Prints the usage for the command line.
    """

    print USAGE

def run(manager_path, plugin_path, verbose = False, debug = False, layout_mode = DEFAULT_STRING_VALUE, run_mode = DEFAULT_STRING_VALUE, stop_on_cycle_error = True, noloop = False, container = DEFAULT_STRING_VALUE, attributes_map = {}):
    """
    Starts the loading of the plugin manager.

    @type manager_path: String
    @param manager_path: The manager base path for execution.
    @type plugin_path: String
    @param plugin_path: The set of paths to the various plugin locations separated by a semi-column.
    @type verbose: bool
    @param verbose: If the log is going to be of type verbose.
    @type debug: bool
    @param debug: If the log is going to be of type debug.
    @type layout_mode: String
    @param layout_mode: The layout mode to be used by the plugin system.
    @type run_mode: String
    @param run_mode: The run mode to be used by the plugin system.
    @type stop_on_cycle_error: bool
    @param stop_on_cycle_error: If the plugin system should stop on cycle error.
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
    plugin_manager = colony.plugins.plugin_system.PluginManager(manager_path, plugin_paths, platform, [], stop_on_cycle_error, not noloop, layout_mode, run_mode, container, attributes_map)

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
        opts, args = getopt.getopt(sys.argv[1:], "hvdnl:r:c:a:m:p:", ["help", "verbose", "debug", "noloop", "layout_mode=", "run_mode=", "container=", "attributes=", "manager_dir=", "plugin_dir="])
    except getopt.GetoptError, error:
        # prints help information and exit
        # will print something like "option -a not recognized"
        print str(error)
        usage()
        sys.exit(2)
    verbose = False
    debug = False
    noloop = False
    layout_mode = DEFAULT_STRING_VALUE
    run_mode = DEFAULT_STRING_VALUE
    container = DEFAULT_STRING_VALUE
    attributes_map = None
    manager_path = DEFAULT_MANAGER_PATH_VALUE
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
        elif option in ("-l", "--layout_mode"):
            layout_mode = value
        elif option in ("-r", "--run_mode"):
            run_mode = value
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

    # configures the system path
    configure_path(manager_path)

    # parses the configuration options
    verbose, debug, layout_mode, run_mode, stop_on_cycle_error, plugin_path = parse_configuration(verbose, debug, layout_mode, run_mode, plugin_path, manager_path)

    # strips the plugin path around the semi-colon character
    plugin_path_striped = plugin_path.strip(";")

    # starts the running process
    run(manager_path, plugin_path_striped, verbose, debug, layout_mode, run_mode, stop_on_cycle_error, noloop, container, attributes_map)

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

def parse_configuration(verbose, debug, layout_mode, run_mode, plugin_path, manager_path):
    """
    Parses the configuration using the given values as default values.

    @type verbose: bool
    @param verbose: If the log is going to be of type verbose.
    @type debug: bool
    @param debug: If the log is going to be of type debug.
    @type layout_mode: String
    @param layout_mode: The layout mode to be used by the plugin system.
    @type run_mode: String
    @param run_mode: The run mode to be used by the plugin system.
    @type plugin_path: String
    @param plugin_path: The set of paths to the various plugin locations separated by a semi-column.
    @type manager_path: String
    @param manager_path: The path to the plugin system.
    @rtype: Tuple
    @return: The tuple with the values parsed value.
    """

    # retrieves the colony configuration contents
    colony_configuration_contents = dir(colony_configuration)

    # in case the verbose variable is defined in the colony configuration
    if not debug and "verbose" in dir(colony_configuration):
        verbose = colony_configuration.verbose

    # in case the debug variable is defined in the colony configuration
    if not debug and "debug" in dir(colony_configuration):
        debug = colony_configuration.debug

    # in case the layout mode variable is defined in the colony configuration
    if layout_mode == DEFAULT_STRING_VALUE and "layout_mode" in dir(colony_configuration):
        layout_mode = colony_configuration.layout_mode

    # in case the run mode variable is defined in the colony configuration
    if run_mode == DEFAULT_STRING_VALUE and "run_mode" in dir(colony_configuration):
        run_mode = colony_configuration.run_mode

    # in case the prefix paths variable is defined in the colony configuration
    if "prefix_paths" in dir(colony_configuration):
        prefix_paths = colony_configuration.prefix_paths

    # in case the stop on cycle error variable is defined in the colony configuration
    if "stop_on_cycle_error" in dir(colony_configuration):
        stop_on_cycle_error = colony_configuration.stop_on_cycle_error

    # in case the plugin path is defined
    if plugin_path:
        # appends a separator to the plugin path
        plugin_path += ";"
    else:
        # creates a new plugin path string
        plugin_path = ""

    # retrieves the current prefix paths
    current_prefix_paths = prefix_paths[layout_mode]

    # iterates over all the colony configuration plugin paths
    for plugin_path_item in colony_configuration.plugin_path_list:
        # sets the initial parsed plugin path
        parsed_plugin_path = manager_path + "/" + plugin_path_item

        # iterates over all the current prefix paths
        for current_prefix_path in current_prefix_paths:
            # retrieves the current prefix path name
            current_prefix_path_name = PREFIX_PATH_PREFIX_VALUE + current_prefix_path + PREFIX_PATH_SUFIX_VALUE

            # retrieves the current prefix path value
            current_prefix_path_value = current_prefix_paths[current_prefix_path]

            # replaces the current prefix path name with the current prefix path value
            parsed_plugin_path = parsed_plugin_path.replace(current_prefix_path_name, current_prefix_path_value)

        # adds the parsed plugin path to the plugin path
        plugin_path += parsed_plugin_path + ";"

    return (verbose, debug, layout_mode, run_mode, stop_on_cycle_error, plugin_path)

def configure_path(manager_path):
    """
    Configures the system path for the given manager path.

    @type manager_path: String
    @param manager_path: The manager path to configure the system path.
    """

    # constructs the library path
    library_path = manager_path + "/" + LIBRARY_DIRECTORY

    # inserts the library path into the system path
    sys.path.insert(0, library_path)

if __name__ == "__main__":
    main()
