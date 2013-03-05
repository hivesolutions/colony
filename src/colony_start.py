#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import glob
import getopt
import logging
import warnings

import colony.base.util
import colony.base.system
import colony.base.information

USAGE = "Help:\n\
--help[-h] - prints this message\n\
--verbose[-v] - starts the program in verbose mode\n\
--debug[-d] - starts the program in debug mode\n\
--silent[-s] - starts the program in silent mode\n\
--noloop[-n] - sets the manager to not use the loop mode\n\
--layout_mode[-l]=development/repository_svn/production - sets the layout mode to be used\n\
--run_mode[-r]=development/test/production - sets the run mode to be used\n\
--container[-c]=default - sets the container to be used\n\
--daemon_pid[-o]=(DAEMON_PID) - sets the pid of the parent daemon\n\
--attributes[-a]=... - sets the attributes to be used\n\
--config_file[-f]=(CONFIGURATION_FILE) - sets the file path to the configuration file\n\
--daemon_file[-d]=(DAEMON_FILE) - sets the file path to the daemon file\n\
--manager_dir[-m]=(PLUGIN_DIR) - sets the plugin directory to be used by the manager\n\
--logger_dir[-g]=(LOGGER_DIR) - sets the logger directory to be used by the manager for the logger\n\
--library_dir[-i]=(LIBRARY_DIR_1;LIBRARY_DIR_2;...) - sets the series of library directories to use\n\
--plugin_dir[-p]=(PLUGIN_DIR_1;PLUGIN_DIR_2;...) - sets the series of plugin directories to use\r\
--execution_command[-e]=plugin_id:method [argument1 argument2 ...] - executes the given execution command at the end of loading"
""" The usage string for the command line arguments """

BRANDING_TEXT = "Hive Colony %s (Hive Solutions Lda. r%s:%s %s)"
""" The branding text value """

VERSION_PRE_TEXT = "Python "
""" The version pre text value """

HELP_TEXT = "Type \"help\" for more information."
""" The help text value """

COLONY_HOME_ENVIRONMENT = "COLONY_HOME"
""" The colony home environment variable name """

COLONY_LAYOUT_MODE_ENVIRONMENT = "COLONY_LAYOUT_MODE"
""" The colony layout mode environment variable name """

COLONY_RUN_MODE_ENVIRONMENT = "COLONY_RUN_MODE"
""" The colony run mode environment variable name """

DEFAULT_STRING_VALUE = "default"
""" The default string value """

DEFAULT_CONFIGURATION_FILE_PATH_VALUE = "config/python/devel.py"
""" The default configuration file path """

DEFAULT_MANAGER_PATH_VALUE = os.path.dirname(os.path.realpath(__file__))
""" The default manager path """

DEFAULT_LOGGER_PATH_VALUE = "log"
""" The default logger path """

PREFIX_PATH_PREFIX_VALUE = "%"
""" The prefix path prefix value """

PREFIX_PATH_SUFIX_VALUE = "_prefix_path%"
""" The prefix path sufix value """

LIBRARY_DIRECTORY = "colony/libs"
""" The colony library directory """

CONFIG_DIRECTORY = "config"
""" The colony config directory """

GENERAL_DIRECTORY = "general"
""" The colony general directory """

PLUGIN_PATHS_FILE = "plugins.pth"
""" The colony plugin paths file """

VERBOSE_VALUE = "verbose"
""" The verbose value """

DEBUG_VALUE = "debug"
""" The debug value """

SILENT_VALUE = "silent"
""" The silent value """

LAYOUT_MODE_VALUE = "layout_mode"
""" The layout mode value """

RUN_MODE_VALUE = "run_mode"
""" The run mode value """

PREFIX_PATHS_VALUE = "prefix_paths"
""" The prefix paths value """

STOP_ON_CYCLE_ERROR_VALUE = "stop_on_cycle_error"
""" The stop on cycle error value """

DAEMON_FILE_PATH_VALUE = "daemon_file_path"
""" The daemon file path value """

LOGGER_PATH_VALUE = "logger_path"
""" The logger path value """

# registers the ignore flag in the deprecation warnings so that
# no message with this kind of warning is printed (clean console)
warnings.filterwarnings("ignore", category = DeprecationWarning)

def usage():
    """
    Prints the usage for the command line.
    """

    print USAGE

def print_information():
    """
    Prints the system information for the command line.
    This should be the first string presented to the end
    used when running the system.
    """

    # print the branding information text
    print BRANDING_TEXT % (
        colony.base.information.VERSION,
        colony.base.information.RELEASE,
        colony.base.information.BUILD,
        colony.base.information.RELEASE_DATE
    )

    # print the python information
    print VERSION_PRE_TEXT + sys.version

    # prints some help information
    print HELP_TEXT

def run(manager_path, logger_path, library_path, meta_path, plugin_path, verbose = False, debug = False, silent = False, layout_mode = DEFAULT_STRING_VALUE, run_mode = DEFAULT_STRING_VALUE, stop_on_cycle_error = True, loop = False, threads = True, signals = True, container = DEFAULT_STRING_VALUE, prefix_paths = [], daemon_pid = None, daemon_file_path = None, execution_command = None, attributes_map = {}):
    """
    Starts the loading of the plugin manager.

    @type manager_path: String
    @param manager_path: The manager base path for execution.
    @type logger_path: String
    @param logger_path: The manager base path for logger.
    @type library_path: String
    @param library_path: The set of paths to the various library locations separated by a semi-column.
    @type meta_path: String
    @param meta_path: The set of paths to the various meta locations separated by a semi-column.
    @type plugin_path: String
    @param plugin_path: The set of paths to the various plugin locations separated by a semi-column.
    @type verbose: bool
    @param verbose: If the log is going to be of type verbose.
    @type debug: bool
    @param debug: If the log is going to be of type debug.
    @type silent: bool
    @param silent: If the log is going to be of type silent.
    @type layout_mode: String
    @param layout_mode: The layout mode to be used by the plugin system.
    @type run_mode: String
    @param run_mode: The run mode to be used by the plugin system.
    @type stop_on_cycle_error: bool
    @param stop_on_cycle_error: If the plugin system should stop on cycle error.
    @type loop: bool
    @param loop: If the plugin manager is going to run in a loop.
    @type threads: bool
    @param threads: If the plugin manager is going to allow threads.
    @type signals: bool
    @param signals: If the plugin manager is going to register signals.
    @type container: String
    @param container: The name of the plugin manager container.
    @type prefix_paths: List
    @param prefix_paths: The list of manager path relative paths to be used as reference for sub-projects.
    @type daemon_pid: int
    @param daemon_pid: The pid of the daemon process running the instance of plugin manager.
    @type daemon_file_path: String
    @param daemon_file_path: The file path to the daemon file, for information control.
    @type execution_command: String
    @param execution_command: The command to be executed by the plugin manager (script mode).
    @type attributes_map: Dictionary
    @param attributes_map: The name of the plugin manager container.
    @rtype: int
    @return: The return code.
    """

    # print the branding information text
    print_information()

    # checks if the library path is not valid
    if not library_path == None:
        library_paths = library_path.split(";")
    else:
        library_paths = []

    # checks if the meta path is not valid
    if not meta_path == None:
        meta_paths = meta_path.split(";")
    else:
        meta_paths = []

    # checks if the plugin path is not valid
    if not plugin_path == None:
        plugin_paths = plugin_path.split(";")
    else:
        plugin_paths = []

    # sets the plugin manager as a global variable
    global plugin_manager

    # retrieves the current executing platform
    platform = colony.base.util.get_environment()

    # creates the plugin manager with the given plugin paths
    plugin_manager = colony.base.system.PluginManager(
        manager_path,
        logger_path,
        library_paths,
        meta_paths,
        plugin_paths,
        platform,
        [],
        stop_on_cycle_error,
        loop,
        threads,
        signals,
        layout_mode,
        run_mode,
        container,
        prefix_paths,
        daemon_pid,
        daemon_file_path,
        execution_command,
        attributes_map
    )

    # sets the logging level for the plugin manager logger
    if debug: plugin_manager.start_logger(logging.DEBUG)
    elif verbose: plugin_manager.start_logger(logging.INFO)
    elif silent: plugin_manager.start_logger(logging.ERROR)
    else: plugin_manager.start_logger(logging.WARN)

    # starts and loads the plugin system
    return_code = plugin_manager.load_system()

    # returns the return code
    return return_code

def main():
    """
    The main entry point of the application.
    """

    try:
        options, _args = getopt.getopt(
            sys.argv[1:],
            "hvdsnl:r:c:o:a:f:d:m:g:i:t:p:e:",
            [
                 "help",
                 "verbose",
                 "debug",
                 "silent",
                 "noloop",
                 "layout_mode=",
                 "run_mode=",
                 "container=",
                 "daemon_pid=",
                 "attributes=",
                 "config_file=",
                 "daemon_file=",
                 "manager_dir=",
                 "logger_dir=",
                 "library_dir=",
                 "meta_dir=",
                 "plugin_dir=",
                 "execution_command="
            ]
        )
    except getopt.GetoptError, error:
        # prints the error description
        print str(error)

        # prints usage information
        usage()

        # exits in error
        sys.exit(2)

    # retrieves the file system encoding
    file_system_encoding = sys.getfilesystemencoding()

    # starts the options values
    verbose = False
    debug = False
    silent = False
    loop = True
    threads = True
    signals = True
    layout_mode = DEFAULT_STRING_VALUE
    run_mode = DEFAULT_STRING_VALUE
    container = DEFAULT_STRING_VALUE
    daemon_pid = None
    attributes_map = None
    config_file_path = DEFAULT_CONFIGURATION_FILE_PATH_VALUE
    daemon_file_path = None
    manager_path = os.environ.get(COLONY_HOME_ENVIRONMENT, DEFAULT_MANAGER_PATH_VALUE).decode(file_system_encoding)
    logger_path = DEFAULT_LOGGER_PATH_VALUE
    library_path = None
    meta_path = None
    plugin_path = None
    execution_command = None

    # iterates over all the options
    for option, value in options:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-d", "--debug"):
            debug = True
        elif option in ("-s", "--silent"):
            silent = True
        elif option in ("-n", "--noloop"):
            loop = False
        elif option in ("-l", "--layout_mode"):
            layout_mode = value
        elif option in ("-r", "--run_mode"):
            run_mode = value
        elif option in ("-c", "--container"):
            container = value
        elif option in ("-o", "--daemon_pid"):
            daemon_pid = int(value)
        elif option in ("-a", "--attributes"):
            attributes_map = parse_attributes(value)
        elif option in ("-f", "--config_file"):
            config_file_path = value.decode(file_system_encoding)
        elif option in ("-d", "--daemon_file"):
            daemon_file_path = value.decode(file_system_encoding)
        elif option in ("-m", "--manager_dir"):
            manager_path = value.decode(file_system_encoding)
        elif option in ("-g", "--logger_dir"):
            logger_path = value.decode(file_system_encoding)
        elif option in ("-i", "--library_dir"):
            library_path = value.decode(file_system_encoding)
        elif option in ("-t", "--meta_dir"):
            meta_path = value.decode(file_system_encoding)
        elif option in ("-p", "--plugin_dir"):
            plugin_path = value.decode(file_system_encoding)
        elif option in ("-e", "--execution_command"):
            execution_command = value.decode(file_system_encoding)
        else:
            assert False, "unhandled option"

    # parses the configuration options, retrieving the various values that
    # control the execution of the plugin system
    verbose, debug, silent, layout_mode, run_mode, stop_on_cycle_error, prefix_paths, daemon_file_path, logger_path, library_path, meta_path, plugin_path = parse_configuration(config_file_path, verbose, debug, silent, layout_mode, run_mode, daemon_file_path, logger_path, library_path, meta_path, plugin_path, manager_path)

    # configures the system using the layout mode, the run mode
    # and the  manager path
    configure_system(layout_mode, run_mode, manager_path)

    # in case the daemon file path is valid and not an absolute path
    # must the (complete) daemon file path prepending the manager path
    if daemon_file_path and not os.path.isabs(daemon_file_path):
        daemon_file_path = manager_path + "/" + daemon_file_path

    # in case the logger path is not an absolute path, must create
    # the (complete) logger path prepending the manager path
    if not os.path.isabs(logger_path): logger_path = manager_path + "/" + logger_path

    # strips the various component location paths around the
    # semi-colon character so that it's possible to send them
    library_path_striped = library_path.strip(";")
    meta_path_striped = meta_path.strip(";")
    plugin_path_striped = plugin_path.strip(";")

    # starts the running process
    return_code = run(
        manager_path,
        logger_path,
        library_path_striped,
        meta_path_striped,
        plugin_path_striped,
        verbose,
        debug,
        silent,
        layout_mode,
        run_mode,
        stop_on_cycle_error,
        loop,
        threads,
        signals,
        container,
        prefix_paths,
        daemon_pid,
        daemon_file_path,
        execution_command,
        attributes_map
    )

    # exits the process with return code
    exit(return_code)

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

        # in case the length of the tuple is two (is valid)
        if len(attributes_string_item_splitted) == 2:
            # unpacks the attribute tuple
            attribute_key, attribute_value = attributes_string_item_splitted

            # sets the attribute in the attributes map
            attributes_map[attribute_key] = attribute_value

    # returns the attributes map
    return attributes_map

def parse_configuration(config_file_path, verbose, debug, silent, layout_mode, run_mode, daemon_file_path, logger_path, library_path, meta_path, plugin_path, manager_path):
    """
    Parses the configuration using the given values as default values.
    The configuration file used is given as a parameter to the function.

    @type config_file_path: Sting
    @param config_file_path: The path to the configuration file.
    @type verbose: bool
    @param verbose: If the log is going to be of type verbose.
    @type debug: bool
    @param debug: If the log is going to be of type debug.
    @type silent: bool
    @param silent: If the log is going to be of type silent.
    @type layout_mode: String
    @param layout_mode: The layout mode to be used by the plugin system.
    @type run_mode: String
    @param run_mode: The run mode to be used by the plugin system.
    @type daemon_file_path: String
    @param daemon_file_path: The file path to the daemon file, for information control.
    @type logger_path: String
    @param logger_path: The path to the logger.
    @type library_path: String
    @param library_path: The set of paths to the various library locations separated by a semi-column.
    @type meta_path: String
    @param meta_path: The set of paths to the various meta locations separated by a semi-column.
    @type plugin_path: String
    @param plugin_path: The set of paths to the various plugin locations separated by a semi-column.
    @type manager_path: String
    @param manager_path: The path to the plugin system.
    @rtype: Tuple
    @return: The tuple with the values parsed value.
    """

    # retrieves the configuration directory from the configuration
    # file path (the directory is going to be used to include the module)
    configuration_directory_path = os.path.dirname(config_file_path)

    # in case the configuration directory path is not an absolute path
    if not os.path.isabs(configuration_directory_path):
        # creates the (complete) configuration directory path
        # prepending the manager path
        configuration_directory_path = os.path.normpath(manager_path + "/" + configuration_directory_path)

    # in case the configuration directory path is valid inserts it into the system path
    configuration_directory_path and sys.path.insert(0, configuration_directory_path)

    # retrieves the configuration file base path from the configuration file path
    config_file_base_path = os.path.basename(config_file_path)

    # retrieves the configuration module name and the configuration
    # module extension by splitting the configuration base path into
    # base name and extension and then imports the referring module
    configuration_module_name, _configuration_module_extension = os.path.splitext(config_file_base_path)
    colony_configuration = __import__(configuration_module_name)

    # retrieves the colony configuration contents
    colony_configuration_contents = dir(colony_configuration)

    # in case the verbose variable is defined in the colony configuration
    if not verbose and VERBOSE_VALUE in colony_configuration_contents:
        verbose = colony_configuration.verbose

    # in case the debug variable is defined in the colony configuration
    if not debug and DEBUG_VALUE in colony_configuration_contents:
        debug = colony_configuration.debug

    # in case the silent variable is defined in the colony configuration
    if not silent and SILENT_VALUE in colony_configuration_contents:
        silent = colony_configuration.silent

    # in case the layout mode variable is defined in the colony configuration
    if layout_mode == DEFAULT_STRING_VALUE and LAYOUT_MODE_VALUE in colony_configuration_contents:
        layout_mode = colony_configuration.layout_mode

    # in case the run mode variable is defined in the colony configuration
    if run_mode == DEFAULT_STRING_VALUE and RUN_MODE_VALUE in colony_configuration_contents:
        run_mode = colony_configuration.run_mode

    # in case the prefix paths variable is defined in the
    # colony configuration
    if PREFIX_PATHS_VALUE in colony_configuration_contents:
        prefix_paths = colony_configuration.prefix_paths

    # in case the stop on cycle error variable is defined
    # in the colony configuration
    if STOP_ON_CYCLE_ERROR_VALUE in colony_configuration_contents:
        stop_on_cycle_error = colony_configuration.stop_on_cycle_error

    # in case the daemon file path variable is defined
    # in the colony configuration
    if DAEMON_FILE_PATH_VALUE in colony_configuration_contents:
        daemon_file_path = colony_configuration.daemon_file_path

    # in case the logger path variable is defined in the
    # colony configuration
    if LOGGER_PATH_VALUE in colony_configuration_contents:
        logger_path = colony_configuration.logger_path

    # in case the library path is defined, must appends a
    # separator to the library path to mark the initial separation
    # otherwise creates a new library path string initializing the
    # value to an empty string so that it can be extended
    if library_path: library_path += ";"
    else: library_path = ""

    # in case the meta path is defined, must appends a
    # separator to the meta path to mark the initial separation
    # otherwise creates a new meta path string initializing the
    # value to an empty string so that it can be extended
    if meta_path: meta_path += ";"
    else: meta_path = ""

    # in case the plugin path is defined, must appends a
    # separator to the plugin path to mark the initial separation
    # otherwise creates a new plugin path string initializing the
    # value to an empty string so that it can be extended
    if plugin_path: plugin_path += ";"
    else: plugin_path = ""

    # retrieves the current prefix paths
    current_prefix_paths = prefix_paths[layout_mode]

    # retrieves the extra library path as the dereferenced values
    # from the colony configuration library path list and adds the
    # extra library path to the library path
    extra_library_path = convert_reference_path_list(
        manager_path,
        current_prefix_paths,
        colony_configuration.library_path_list
    )
    library_path += extra_library_path

    # retrieves the extra meta path as the dereferenced values
    # from the colony configuration meta path list and adds the
    # extra meta path to the meta path
    extra_meta_path = convert_reference_path_list(
        manager_path,
        current_prefix_paths,
        colony_configuration.meta_path_list
    )
    meta_path += extra_meta_path

    # loads the plugin paths file path and adds the plugin paths
    # file path to the plugin path
    plugin_paths_file_path = load_plugin_paths_file(manager_path)
    plugin_path += plugin_paths_file_path

    # retrieves the extra plugin path as the dereferenced values
    # from the colony configuration plugin path list and adds the
    # extra plugin path to the plugin path
    extra_plugin_path = convert_reference_path_list(
        manager_path,
        current_prefix_paths,
        colony_configuration.plugin_path_list
    )
    plugin_path += extra_plugin_path

    return (
        verbose,
        debug,
        silent,
        layout_mode,
        run_mode,
        stop_on_cycle_error,
        current_prefix_paths,
        daemon_file_path,
        logger_path,
        library_path,
        meta_path,
        plugin_path
    )

def convert_reference_path_list(manager_path, current_prefix_paths, reference_path_list):
    """
    Converts the given list of reference paths. The reference
    paths include references of type %reference_name% to include
    base paths that are dereferenced at runtime based in the current
    layout configuration or other variables.

    @type manager_path: String
    @param manager_path: The path to the manager.
    @type current_prefix_paths: List
    @param current_prefix_paths: The prefix paths currently in use.
    @type reference_path_list: List
    @param reference_path_list: The list of reference paths.
    @rtype: String
    @return: A string converted reference path containing all the dereferenced paths.
    """

    # initializes the converted reference path, this is the value
    # to be returned by this function with the complete path string
    # to be used by the plugin system
    converted_reference_path = str()

    # iterates over all the reference paths, in order to normalize
    # resolver and integrate them into the reference path
    for reference_path in reference_path_list:
        # sets the initial dereferenced path
        dereferenced_path = manager_path + "/" + reference_path

        # iterates over all the current prefix paths to dereference
        # them into the path "along" the various prefix paths
        for current_prefix_path in current_prefix_paths:
            # retrieves the current prefix path name and value
            # to be used in the dereferencing of the path, then
            # executes the dereferencing operation substituting the
            # "wildcard" references in the paths
            current_prefix_path_name = PREFIX_PATH_PREFIX_VALUE + current_prefix_path + PREFIX_PATH_SUFIX_VALUE
            current_prefix_path_value = current_prefix_paths[current_prefix_path]
            dereferenced_path = dereferenced_path.replace(current_prefix_path_name, current_prefix_path_value)

        # runs the glob based resolver to resolver the "wildcard" patterns
        # that may be present in the path, this operation should return
        # a list of paths from the resolved "wildcard" them iterates over
        # these paths to add them to the converted reference path
        dereferenced_paths = glob.glob(dereferenced_path)
        for dereferenced_path in dereferenced_paths:
            # resolves the dereferenced path as an absolute path and
            # adds it to the converted reference string path (linear
            # version of the path separated by tokens)
            dereferenced_path = os.path.abspath(dereferenced_path)
            converted_reference_path += dereferenced_path + ";"

    # returns the converted reference path
    return converted_reference_path

def load_plugin_paths_file(manager_path):
    """
    Loads the plugin paths file, creating the base plugin
    paths contained in the file.

    @type manager_path: String
    @param manager_path: The path to the manager.
    @rtype: String
    @return: A string with the paths loaded from the file.
    """

    # creates the config general path from the manager path
    config_general_path = manager_path + "/" + CONFIG_DIRECTORY + "/" + GENERAL_DIRECTORY

    # crates the plugin paths file path (from the config general path)
    plugin_paths_file_path = config_general_path + "/" + PLUGIN_PATHS_FILE

    # in case the plugin paths file does not exists (the
    # file is not mandatory) must return immediately because
    # no further processing is taking place
    if not os.path.exists(plugin_paths_file_path): return

    # opens the plugin paths file for reading then reads the
    # plugin path files contents, and the closes file to avoid
    # any further reading that could cause memory leaks
    plugin_paths_file = open(plugin_paths_file_path, "r")
    try: plugin_paths_file_contents = plugin_paths_file.read()
    finally: plugin_paths_file.close()

    # splits the paths over the newline character and then
    # filters the invalid values (white spaces)
    paths = plugin_paths_file_contents.split("\n")
    paths = [value for value in paths if value]

    # initializes the converted reference path
    plugin_paths_string_value = str()

    # iterates over all the paths to creates the
    # plugins paths string
    for path in paths:
        # in case the path is not an absolute path
        # creates the (complete) path prepending
        # the manager path and then adds the path
        # to the plugin paths string value
        if not os.path.isabs(path): path = manager_path + "/" + path
        plugin_paths_string_value += path + ";"

    # returns the plugin paths string value
    return plugin_paths_string_value

def configure_system(layout_mode, run_mode, manager_path):
    """
    Configures the system for the given attributes.

    @type layout_mode: String
    @param layout_mode: The layout mode to configure the system.
    @type run_mode: String
    @param run_mode: The run mode to configure the system.
    @type manager_path: String
    @param manager_path: The manager path to configure the system.
    """

    # sets the various colony related environment variables
    # so that the current process may expose them to any
    # created child process (context exposure)
    os.environ[COLONY_LAYOUT_MODE_ENVIRONMENT] = layout_mode
    os.environ[COLONY_RUN_MODE_ENVIRONMENT] = run_mode
    os.environ[COLONY_HOME_ENVIRONMENT] = manager_path

    # constructs the library path and normalizes it
    library_path = manager_path + "/" + LIBRARY_DIRECTORY
    library_path = os.path.normpath(library_path)

    # inserts the library path into the system path
    sys.path.insert(0, library_path)

if __name__ == "__main__":
    main()
