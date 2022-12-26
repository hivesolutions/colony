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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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
import sys
import glob
import getopt
import warnings

import colony

USAGE = "Help:\n\
--help[-h] - prints this message\n\
--noloop[-n] - sets the manager to not use the loop mode\n\
--level[-v]=(LEVEL) - sets the logging verbosity level to be used\n\
--layout_mode[-l]=development/repository_svn/production - sets the layout mode to be used\n\
--run_mode[-r]=development/test/production - sets the run mode to be used\n\
--container[-c]=default - sets the container to be used\n\
--daemon_pid[-o]=(DAEMON_PID) - sets the pid of the parent daemon\n\
--config_file[-f]=(CONFIGURATION_FILE) - sets the file path to the configuration file\n\
--daemon_file[-d]=(DAEMON_FILE) - sets the file path to the daemon file\n\
--manager_dir[-m]=(PLUGIN_DIR) - sets the plugin directory to be used by the manager\n\
--logger_dir[-g]=(LOGGER_DIR) - sets the logger directory to be used by the manager for the logger\n\
--library_dir[-i]=(LIBRARY_DIR_1;LIBRARY_DIR_2;...) - sets the series of library directories to use\n\
--plugin_dir[-p]=(PLUGIN_DIR_1;PLUGIN_DIR_2;...) - sets the series of plugin directories to use"
""" The usage string for the command line arguments,
this is going to be display as part of the help string """

BRANDING_TEXT = "Hive Colony %s (Hive Solutions Lda. r%s:%s %s)"
""" The branding text value to be display at the start
of the process execution (contains user/system information) """

VERSION_PRE_TEXT = "Python "
""" The version pre text value """

HELP_TEXT = "Type \"help\" for more information."
""" The help text value """

DEFAULT_CONFIG_FILE_PATH = "config/python/devel.py"
""" The default configuration file path, that is going
to be used only in case it is available for under the
provided path, otherwise only the default base values
are used (security setting) """

RELATIVE_MANAGER_PATH = os.path.dirname(os.path.realpath(__file__))
""" The default manager path, considered to be the current
executing file's directory (by default)) """

DEFAULT_LOGGER_PATH = "log"
""" The default logger path """

PLUGIN_PATHS_FILE = "plugins.pth"
""" The colony plugin paths file """

# registers the ignore flag in the deprecation warnings so that
# no message with this kind of warning is printed (clean console)
warnings.filterwarnings("ignore", category = DeprecationWarning)

def usage():
    """
    Prints the usage for the command line, should be used
    to provide extra information about the way to use this
    command line to the user.
    """

    print(USAGE)

def print_information():
    """
    Prints the system information for the command line.
    This should be the first string presented to the end
    used when running the system.
    """

    print(BRANDING_TEXT % (
        colony.VERSION,
        colony.RELEASE,
        colony.BUILD,
        colony.RELEASE_DATE
    ))
    print(VERSION_PRE_TEXT + sys.version)
    print(HELP_TEXT)

def run(
    manager_path,
    logger_path,
    library_path,
    meta_path,
    plugin_path,
    mode = None,
    margs = [],
    level = "WARNING",
    layout_mode = "default",
    run_mode = "default",
    stop_on_cycle_error = True,
    loop = False,
    threads = True,
    signals = True,
    container = "default",
    prefix_paths = [],
    daemon_pid = None,
    daemon_file_path = None
):
    """
    Starts the loading of the plugin manager. This should be the
    primary start point of the plugin system when starting it as
    a stand alone process (eg: not using wsgi).

    :type manager_path: String
    :param manager_path: The manager base path for execution.
    :type logger_path: String
    :param logger_path: The manager base path for logger.
    :type library_path: String
    :param library_path: The set of paths to the various library
    locations separated by a semi-column.
    :type meta_path: String
    :param meta_path: The set of paths to the various meta
    locations separated by a semi-column.
    :type plugin_path: String
    :param plugin_path: The set of paths to the various plugin
    locations separated by a semi-column.
    :type mode: String
    :param mode: The mode that is going to be used for non
    standard execution of the plugin manager (eg: testing). This
    value is not set by default (for default execution).
    :type margs: List
    :param margs: The arguments (coming from command line) that
    are going to be provided at execution time to the function
    responsible for the mode execution, these arguments should
    consist on a series of string based values.
    :type level: String
    :param level: The logging level described as a string that is
    going to be used by the underlying colony logging infra-structure.
    :type layout_mode: String
    :param layout_mode: The layout mode to be used by the plugin system.
    :type run_mode: String
    :param run_mode: The run mode to be used by the plugin
    system, this value is critical for the type of execution
    of the colony system (eg: development, runtime, etc.)
    :type stop_on_cycle_error: bool
    :param stop_on_cycle_error: If the plugin system should stop
    on cycle error, a cycle error is an error that occurs during
    the startup process of the colony infra-structure.
    :type loop: bool
    :param loop: If the plugin manager is going to run in a loop.
    :type threads: bool
    :param threads: If the plugin manager is going to allow threads.
    :type signals: bool
    :param signals: If the plugin manager is going to register signals.
    :type container: String
    :param container: The name of the plugin manager container.
    :type prefix_paths: List
    :param prefix_paths: The list of manager path relative paths to be used as reference for sub-projects.
    :type daemon_pid: int
    :param daemon_pid: The pid of the daemon process running the instance of plugin manager.
    :type daemon_file_path: String
    :param daemon_file_path: The file path to the daemon file, for information control.
    :rtype: int
    :return: The return code.
    """

    # sets the plugin manager as a global variable, this value
    # may be used in more situations that the one defined in the
    # the current (local) scope
    global plugin_manager

    # checks if the library path is not valid, by splitting its
    # value around the separator token into a valid list
    if library_path: library_paths = library_path.split(";")
    else: library_paths = []

    # checks if the meta path is not valid, by splitting its
    # value around the separator token into a valid list
    if meta_path: meta_paths = meta_path.split(";")
    else: meta_paths = []

    # checks if the plugin path is not valid, by splitting its
    # value around the separator token into a valid list
    if plugin_path: plugin_paths = plugin_path.split(";")
    else: plugin_paths = []

    # retrieves the current executing platform, so that this
    # value may be passed to the next functions to be called
    # as part of this execution stack
    platform = colony.get_environment()

    # runs the ensure operation for the currently defined manager
    # path making sure that the complete directory structure exists
    colony.ensure_tree(manager_path)

    # creates the plugin manager with the given plugin paths, this
    # is the instance that is going to be used for the current loading
    plugin_manager = colony.PluginManager(
        manager_path = manager_path,
        logger_path = logger_path,
        library_paths = library_paths,
        meta_paths = meta_paths,
        plugin_paths = plugin_paths,
        platform = platform,
        init_complete_handlers = [],
        stop_on_cycle_error = stop_on_cycle_error,
        loop = loop,
        threads = threads,
        signals = signals,
        layout_mode = layout_mode,
        run_mode = run_mode,
        container = container,
        prefix_paths = prefix_paths,
        daemon_pid = daemon_pid,
        daemon_file_path = daemon_file_path
    )

    # resolves the string based level into the proper integer
    # that describes the logging level and then uses that value
    # to start the logging infra-structure of colony
    level = colony.getLevelName(level)
    plugin_manager.start_logger(level)

    # creates the callback function to be used in the process of
    # printing the branding information text to the standard output
    # informing the end user about the current environment
    callback = lambda: print_information()

    # starts and loads the plugin system, this is a blocking
    # call and the flow control is only returned at the end of
    # the execution of the colony infra-structure, then the
    # returned code is returned to the caller function
    return_code = plugin_manager.load_system(
        mode = mode,
        args = margs,
        callback = callback
    )
    return return_code

def execute(cwd = None, force_exit = True):
    """
    The main entry point of the application, should parse
    the provided command line arguments and then start the
    execution of the colony plugin system.

    An optional force exit flag controls if the exit function
    should always be used in exit.

    :type cwd: String
    :param cwd: The "original" current working directory to
    be used for situations where the "cwd" has been changed
    so that files generated are put on the colony path. This
    is created as a legacy operation.
    :type force_exit: bool
    :param force_exit: If in case the return code is a valid
    one, the exit function should "still" be used to return
    the control flow immediately to the caller process.
    """

    # verifies if the cwd value is defined an in case it's not
    # retrieves the real cwd values as to be used for operations
    cwd = cwd or os.getcwd()

    try:
        # defines the options retrieval schema/template and runs it
        # retrieves the various options and the remaining arguments
        # that have not been parsed by the processor
        options, args = getopt.getopt(
            sys.argv[1:],
            "hnv:l:r:c:o:f:d:m:g:i:t:p:",
            [
                 "help"
                 "noloop",
                 "level="
                 "layout_mode=",
                 "run_mode=",
                 "container=",
                 "daemon_pid=",
                 "config_file=",
                 "daemon_file=",
                 "manager_dir=",
                 "logger_dir=",
                 "library_dir=",
                 "meta_dir=",
                 "plugin_dir="
            ]
        )
    except getopt.GetoptError as error:
        # prints the error description so that the user is able
        # to react to the error, then prints the possible usage
        # for the command and exists in error
        print(str(error))
        usage()
        sys.exit(2)

    # retrieves the execution mode for colony as the first non parsed
    # value from the command line (as expected)
    if args: mode = args[0]
    else: mode = None

    # retrieves the complete set of arguments that are going to be
    # provided for the mode execution, these arguments are considered
    # to be (mode) context specific and valuable only inside context
    margs = args[1:]

    # retrieves the file system encoding
    file_system_encoding = sys.getfilesystemencoding()

    # starts the options values
    loop = True
    level = None
    threads = True
    signals = True
    layout_mode = None
    run_mode = None
    container = "default"
    daemon_pid = None
    config_file_path = DEFAULT_CONFIG_FILE_PATH
    daemon_file_path = None
    manager_path = colony.resolve_manager(RELATIVE_MANAGER_PATH)
    logger_path = DEFAULT_LOGGER_PATH
    library_path = None
    meta_path = None
    plugin_path = None

    # iterates over all the options to be able to parse its value
    # starting it from the command line
    for option, value in options:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option in ("-n", "--noloop"):
            loop = False
        elif option in ("-v", "--level"):
            level = value
        elif option in ("-l", "--layout_mode"):
            layout_mode = value
        elif option in ("-r", "--run_mode"):
            run_mode = value
        elif option in ("-c", "--container"):
            container = value
        elif option in ("-o", "--daemon_pid"):
            daemon_pid = int(value)
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
        else:
            assert False, "unhandled option"

    # parses the configuration options, retrieving the various values that
    # control the execution of the plugin system
    mode, level, layout_mode, run_mode, stop_on_cycle_error,\
    prefix_paths, daemon_file_path, logger_path, library_path, meta_path,\
    plugin_path = parse_configuration(
        cwd,
        mode,
        config_file_path,
        level,
        layout_mode,
        run_mode,
        daemon_file_path,
        logger_path,
        library_path,
        meta_path,
        plugin_path,
        manager_path
    )

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

    # starts the running process, this should launch the manager
    # and then start the main loop of execution returning the
    # return code (result of execution) to the caller process
    return_code = run(
        manager_path,
        logger_path,
        library_path_striped,
        meta_path_striped,
        plugin_path_striped,
        mode = mode,
        margs = margs,
        level = level,
        layout_mode = layout_mode,
        run_mode = run_mode,
        stop_on_cycle_error = stop_on_cycle_error,
        loop = loop,
        threads = threads,
        signals = signals,
        container = container,
        prefix_paths = prefix_paths,
        daemon_pid = daemon_pid,
        daemon_file_path = daemon_file_path
    )

    # in case the return code is not success or the force
    # exit flag is set then calls the exit function
    if not return_code == 0 or force_exit: exit(return_code)

def parse_configuration(
    cwd,
    mode,
    config_file_path,
    level,
    layout_mode,
    run_mode,
    daemon_file_path,
    logger_path,
    library_path,
    meta_path,
    plugin_path,
    manager_path
):
    """
    Parses the configuration using the given values as default values.
    The configuration file used is given as a parameter to the function.

    :type cwd: String
    :param cwd: The (original) current working directory to be used
    in the resolution of the relative import values.
    :type mode: String
    :param mode: The mode that is going to be used for non
    standard execution of the plugin manager (eg: testing). This
    value is not set by default (for default execution).
    :type config_file_path: Sting
    :param config_file_path: The path to the configuration file.
    :type level: String
    :param level: The logging level value described as a string
    that is going to be used in the plugin system.
    :type layout_mode: String
    :param layout_mode: The layout mode to be used by the plugin system.
    :type run_mode: String
    :param run_mode: The run mode to be used by the plugin system.
    :type daemon_file_path: String
    :param daemon_file_path: The file path to the daemon file,
    for information control.
    :type logger_path: String
    :param logger_path: The path to the logger.
    :type library_path: String
    :param library_path: The set of paths to the various library
    locations separated by a semi-column.
    :type meta_path: String
    :param meta_path: The set of paths to the various meta locations
    separated by a semi-column.
    :type plugin_path: String
    :param plugin_path: The set of paths to the various plugin
    locations separated by a semi-column.
    :type manager_path: String
    :param manager_path: The path to the plugin system.
    :rtype: Tuple
    :return: The tuple with the values parsed value.
    """

    # retrieves the configuration directory from the configuration
    # file path (the directory is going to be used to include the module)
    config_dir = os.path.dirname(config_file_path)

    # in case the configuration directory path is not an absolute path
    if not os.path.isabs(config_dir):
        # creates the (complete) configuration directory path
        # prepending the manager path
        config_dir = os.path.normpath(manager_path + "/" + config_dir)

    # in case the configuration directory path is valid inserts it into the system path
    config_dir and sys.path.insert(0, config_dir)

    # retrieves the configuration file base path from the configuration file path
    config_file_base_path = os.path.basename(config_file_path)

    # retrieves the configuration module name and the configuration
    # module extension by splitting the configuration base path into
    # base name and extension and then imports the referring module
    config_module, _configuration_module_extension = os.path.splitext(config_file_base_path)
    try: config = __import__(config_module)
    except ImportError: import colony.config.base as module; config = module

    # retrieves the contents of the configuration file that has just
    # been loaded, this is the default operation to be performed
    names = dir(config)

    # sets the proper configuration attributes taking into account the
    # presence or not of such attributes in the loaded file
    if "level" in names: level = level or config.level
    if "layout_mode" in names: layout_mode = layout_mode or config.layout_mode
    if "run_mode" in names: run_mode = run_mode or config.run_mode
    if "prefix_paths" in names: prefix_paths = config.prefix_paths
    if "stop_on_cycle_error" in names: stop_on_cycle_error = config.stop_on_cycle_error
    if "daemon_file_path" in names: daemon_file_path = config.daemon_file_path
    if "logger_path" in names: logger_path = config.logger_path

    # tries to load some of the environment "loadable" properties for the
    # starting of the colony infra-structure, defaulting to the provided
    # values in case they are present (as expected), then in case there's
    # still no valid values for such variables default values are used
    mode = colony.conf("MODE", mode)
    level = colony.conf("LEVEL", level)
    layout_mode = colony.conf("LAYOUT_MODE", layout_mode)
    run_mode = colony.conf("RUN_MODE", run_mode)
    layout_mode = layout_mode or "default"
    run_mode = run_mode or "default"

    # retrieves the complete set of configuration variables associated
    # with the various paths to be used by colony and then adds the
    # proper static file based configuration values to them, so that
    # these list are properly started with the initial values
    library_path_list = colony.conf("LIBRARY_PATH", [], cast = list)
    meta_path_list = colony.conf("META_PATH", [], cast = list)
    plugin_path_list = colony.conf("PLUGIN_PATH", [], cast = list)
    library_path_list = library_path_list + config.library_path_list
    meta_path_list = meta_path_list + config.meta_path_list
    plugin_path_list = plugin_path_list + config.plugin_path_list

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
        cwd,
        manager_path,
        current_prefix_paths,
        library_path_list
    )
    library_path += extra_library_path

    # retrieves the extra meta path as the dereferenced values
    # from the colony configuration meta path list and adds the
    # extra meta path to the meta path
    extra_meta_path = convert_reference_path_list(
        cwd,
        manager_path,
        current_prefix_paths,
        meta_path_list
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
        cwd,
        manager_path,
        current_prefix_paths,
        plugin_path_list
    )
    plugin_path += extra_plugin_path

    return (
        mode,
        level,
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

def convert_reference_path_list(cwd, manager_path, current_prefix_paths, reference_path_list):
    """
    Converts the given list of reference paths. The reference
    paths include references of type %reference_name% to include
    base paths that are dereferenced at runtime based in the current
    layout configuration or other variables.

    :type cwd: String
    :param cwd: The (original) current working directory to be used
    in the resolution of the relative import values.
    :type manager_path: String
    :param manager_path: The path to the manager.
    :type current_prefix_paths: List
    :param current_prefix_paths: The prefix paths currently in use.
    :type reference_path_list: List
    :param reference_path_list: The list of reference paths.
    :rtype: String
    :return: A string converted reference path containing all
    the dereferenced paths.
    """

    # initializes the converted reference path, this is the value
    # to be returned by this function with the complete path string
    # to be used by the plugin system
    converted_reference_path = str()

    # iterates over all the reference paths, in order to normalize
    # resolver and integrate them into the reference path
    for reference_path in reference_path_list:
        # verifies if the current reference path is a local one (using
        # the prefix value) and in case it's not prepends the manager
        # path to it as the base path (usual situation)
        is_local = reference_path.startswith("./")
        if is_local: dereferenced_path = cwd + "/" + reference_path
        else: dereferenced_path = manager_path + "/" + reference_path

        # iterates over all the current prefix paths to dereference
        # them into the path "along" the various prefix paths
        for current_prefix_path in current_prefix_paths:
            # retrieves the current prefix path name and value
            # to be used in the dereferencing of the path, then
            # executes the dereferencing operation substituting the
            # "wildcard" references in the paths
            current_prefix_path_name = "%" + current_prefix_path + "_prefix_path%"
            current_prefix_path_value = current_prefix_paths[current_prefix_path]
            dereferenced_path = dereferenced_path.replace(
                current_prefix_path_name,
                current_prefix_path_value
            )

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

    :type manager_path: String
    :param manager_path: The path to the manager.
    :rtype: String
    :return: A string with the paths loaded from the file.
    """

    # creates the config general path from the manager path
    config_general_path = manager_path + "/config/general"

    # crates the plugin paths file path (from the config general path)
    plugin_paths_file_path = config_general_path + "/" + PLUGIN_PATHS_FILE

    # in case the plugin paths file does not exists (the
    # file is not mandatory) must return immediately because
    # no further processing is taking place
    if not os.path.exists(plugin_paths_file_path): return ""

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

    :type layout_mode: String
    :param layout_mode: The layout mode to configure the system.
    :type run_mode: String
    :param run_mode: The run mode to configure the system.
    :type manager_path: String
    :param manager_path: The manager path to configure the system.
    """

    # sets the various colony related environment variables
    # so that the current process may expose them to any
    # created child process (context exposure)
    os.environ["COLONY_LAYOUT_MODE"] = layout_mode
    os.environ["COLONY_RUN_MODE"] = run_mode
    os.environ["COLONY_HOME"] = manager_path

    # constructs the library path and normalizes it
    library_path = manager_path + "/colony/libs"
    library_path = os.path.normpath(library_path)

    # inserts the library path into the system path
    sys.path.insert(0, library_path)

def main():
    """
    Execution function for the colony infra-structure may be used
    for the entry point definition.

    Note that a call to this function may change the current working
    directory for the executing process.
    """

    path = os.path.dirname(__file__)
    path = os.path.normpath((os.path.abspath(path)))
    _path = os.getcwd()
    try:
        os.chdir(path)
        execute(cwd = _path)
    finally:
        os.chdir(_path)

if __name__ == "__main__":
    main()
else:
    __path__ = []
