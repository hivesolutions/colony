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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import stat
import sys
import thread
import inspect
import threading
import traceback
import time
import types
import string

import os.path

import colony.plugins.util
import colony.plugins.decorators

import colony.plugins.plugin_system_configuration
import colony.plugins.plugin_system_exceptions

plugin_manager_configuration = colony.plugins.plugin_system_configuration.plugin_manager_configuration
""" The plugin manager configuration """

CPYTHON_ENVIRONMENT = colony.plugins.util.CPYTHON_ENVIRONMENT
""" CPython environment value """

JYTHON_ENVIRONMENT = colony.plugins.util.JYTHON_ENVIRONMENT
""" Jython environment value """

IRON_PYTHON_ENVIRONMENT = colony.plugins.util.IRON_PYTHON_ENVIRONMENT
""" IronPython environment value """

# conditional logging import (depending on the current environment)
if colony.plugins.util.get_environment() == CPYTHON_ENVIRONMENT or colony.plugins.util.get_environment() == JYTHON_ENVIRONMENT:
    import logging
elif colony.plugins.util.get_environment() == IRON_PYTHON_ENVIRONMENT:
    import colony.plugins.dummy_logging as logging

DEFAULT_LOGGER = "default_messages"
""" The default logger name """

DEFAULT_LOGGING_LEVEL = logging.WARN
""" The default logging level """

DEFAULT_LOGGING_FORMAT = "%(asctime)s %(levelname)s %(message)s"
""" The default logging format """

EAGER_LOADING_TYPE = "eager_loading"
""" The eager loading plugin loading type """

LAZY_LOADING_TYPE = "lazy_loading"
""" The lazy loading plugin loading type """

PLUGIN_MANAGER_EXTENSION_TYPE = "plugin_manager_extension"
""" The plugin manager type """

MAIN_TYPE = "main"
""" The main plugin type """

STARTUP_TYPE = "startup"
""" The startup plugin type """

THREAD_TYPE = "thread"
""" The thread plugin type """

FULL_LOAD_TYPE = "full_load"
""" The full load plugin loading type """

DEPENDENCY_TYPE = "dependency"
""" The dependency plugin loading/unloading type """

ALLOWED_TYPE = "allowed"
""" The allowed plugin loading/unloading type """

FILE_REMOVED_TYPE = "file_removed"
""" The file removed plugin loading/unloading type """

PLUGIN_MANAGER_TYPE = "plugin_manager"
""" The plugin manager type """

PLUGIN_MANAGER_PLUGIN_VALIDATION_PREFIX = "is_valid_"
""" The prefix for the plugin manager plugin validation prefix """

class Plugin(object):
    """
    The abstract plugin class
    """

    id = "none"
    """ The id of the plugin """

    name = "none"
    """ The name of the plugin """

    short_name = "none"
    """ The short name of the plugin """

    description = "none"
    """ The description of the plugin """

    version = "none"
    """ The version of the plugin """

    author = "none"
    """ The author of the plugin """

    loading_type = EAGER_LOADING_TYPE
    """ The type of loading of the plugin """

    platforms = []
    """ The compatible platforms of the plugin """

    capabilities = []
    """ The capabilities of the plugin """

    capabilities_allowed = []
    """ The capabilities allowed by the plugin """

    dependencies = []
    """ The dependencies of the plugin """

    events_handled = []
    """ The events handled by the plugin """

    events_registrable = []
    """ The events that the plugin can register for """

    main_modules = []
    """ The main modules of the plugin """

    valid = True
    """ The valid flag of the plugin """

    logger = None
    """ The logger used """

    dependencies_loaded = []
    """ The list of dependency plugins loaded """

    allowed_loaded = []
    """ The list of allowed plugins loaded """

    event_plugins_handled_loaded_map = {}
    """ The map with the plugin associated with the name of the event handled """

    event_plugins_registered_loaded_map = {}
    """ The map with the plugin associated with the name of the event registered """

    event_plugin_manager_registered_loaded_list = []
    """ The list with all the events registered in the plugin manager """

    configuration_map = {}
    """ The configuration of the plugin """

    loaded = False
    """ The loading flag """

    lazy_loaded = False
    """ The lazy loading flag """

    ready_semaphore = None
    """ The ready semaphore """

    manager = None
    """ The parent plugin manager """

    def __init__(self, manager = None):
        """
        Constructor of the class

        @type manager: PluginManager
        @param manager: The plugin manager of the system
        """

        self.manager = manager
        self.ready_semaphore = threading.Semaphore(0)

        self.logger = logging.getLogger(DEFAULT_LOGGER)
        self.dependencies_loaded = []
        self.allowed_loaded = []
        self.event_plugins_handled_loaded_map = {}
        self.event_plugins_registered_loaded_map = {}
        self.event_plugin_manager_registered_loaded_list = []
        self.configuration_map = {}
        self.loaded = False

    def __repr__(self):
        """
        Returns the default representation of the class

        @rtype: String
        @return: The default representation of the class
        """

        return "<%s, %s, %s, %r>" % (
            self.__class__.__name__,
            self.name,
            self.version,
            self.capabilities,
        )

    def load_plugin(self):
        """
        Method called at the beginning of the plugin loading process
        """

        # registers all the plugin manager events
        self.register_all_plugin_manager_events()

        # sets the loaded flag as true
        self.loaded = True

        # sets the loaded flag as true
        self.lazy_loaded = False

        self.info("Loading plugin '%s' v%s" % (self.short_name, self.version))

    def lazy_load_plugin(self):
        """
        Method called at the beginning of the lazy plugin loading process
        """

        # registers all the plugin manager events
        self.register_all_plugin_manager_events()

        # sets the loaded flag as true
        self.loaded = True

        # sets the loaded flag as true
        self.lazy_loaded = True

        self.info("Lazy loading plugin '%s' v%s" % (self.short_name, self.version))

    def end_load_plugin(self):
        """
        Method called at the end of the plugin loading process
        """

        self.info("Loading process for plugin '%s' v%s completed" % (self.short_name, self.version))

    def unload_plugin(self):
        """
        Method called at the beginning of the plugin unloading process
        """

        # unregisters all the plugin manager events
        self.unregister_all_plugin_manager_events()

        self.unregister_all_for_plugin()
        self.loaded = False
        self.allowed_loaded = []
        self.dependencies_loaded = []
        self.info("Unloading plugin '%s' v%s" % (self.short_name, self.version))

    def end_unload_plugin(self):
        """
        Method called at the end of the plugin unloading process
        """

        self.info("Unloading process for plugin '%s' v%s completed" % (self.short_name, self.version))

    def load_allowed(self, plugin, capability):
        """
        Method called at the loading of an allowed plugin

        @type plugin: Plugin
        @param plugin: The allowed plugin that is being loaded
        @type capability: String
        @param capability: Capability for which the plugin is being injected
        """

        self.allowed_loaded.append(plugin)
        self.register_all_registrable_events_plugin(plugin)
        self.info("Loading plugin '%s' v%s in '%s' v%s" % (plugin.short_name, plugin.version, self.short_name, self.version))

    def unload_allowed(self, plugin, capability):
        """
        Method called at the unloading of an allowed plugin

        @type plugin: Plugin
        @param plugin: The allowed plugin that is being unloaded
        @type capability: String
        @param capability: Capability for which the plugin is being injected
        """

        self.allowed_loaded.remove(plugin)
        self.unregister_all_registrable_events_plugin(plugin)
        self.info("Unloading plugin '%s' v%s in '%s' v%s" % (plugin.short_name, plugin.version, self.short_name, self.version))

    def dependency_injected(self, plugin):
        """
        Method called at the injection of a plugin dependency

        @type plugin: Plugin
        @param plugin: The dependency plugin to be injected
        """

        self.dependencies_loaded.append(plugin)
        self.info("Plugin dependency '%s' v%s injected in '%s' v%s" % (plugin.short_name, plugin.version, self.short_name, self.version))

    def init_complete(self):
        """
        Method called at the end of the plugin manager initialization
        """

        self.info("Plugin '%s' v%s notified about the end of the plugin manager init process" % (self.short_name, self.version))

    def register_all_registrable_events_plugin(self, plugin):
        """
        Registers all the allowed events from a given plugin in self

        @param plugin: The plugin containing the events to be registered
        """

        event_names_registrable = [event_name for event_name in plugin.events_handled if is_event_or_super_event_in_list(event_name, self.events_registrable)]

        for event_name_registrable in event_names_registrable:
            self.register_for_plugin_event(plugin, event_name_registrable)

    def unregister_all_registrable_events_plugin(self, plugin):
        """
        Unregisters all the allowed events from a given plugin in self

        @param plugin: The plugin containing the events to be unregistered
        """

        for event_name in self.event_plugins_registered_loaded_map:
            if plugin in self.event_plugins_registered_loaded_map[event_name]:
                self.unregister_for_plugin_event(plugin, event_name)

    def register_all_plugin_manager_events(self):
        """
        Registers all the plugin manager events in self
        """

        event_names_registrable = [event_name for event_name in self.events_registrable if is_event_or_sub_event(PLUGIN_MANAGER_TYPE, event_name)]

        for event_name_registrable in event_names_registrable:
            self.register_for_plugin_manager_event(event_name_registrable)

    def unregister_all_plugin_manager_events(self):
        """
        Unregisters all the plugin manager events in self
        """

        for event_name in self.event_plugin_manager_registered_loaded_list:
            self.unregister_for_plugin_manager_event(event_name)

    def register_for_plugin_event(self, plugin, event_name):
        """
        Registers a given event from a given plugin in self

        @type plugin: Plugin
        @param plugin: The plugin containing the event to be registered
        @type event_name: String
        @param event_name: The name of the event to be registered
        """

        # in case the plugin is not loaded or lazy loaded
        if not plugin.is_loaded_or_lazy_loaded():
            return

        # registers the plugin event in the plugin containing the event
        plugin.register_plugin_event(self, event_name)

        # in case it's the first plugin to be registered for the given event
        if not event_name in self.event_plugins_registered_loaded_map:
            self.event_plugins_registered_loaded_map[event_name] = []

        # appends the plugin containing the event to be registered to the plugin events map
        self.event_plugins_registered_loaded_map[event_name].append(plugin)

    def unregister_for_plugin_event(self, plugin, event_name):
        """
        Unregisters a given event from a given plugin in self

        @type plugin: Plugin
        @param plugin: The plugin containing the event to be unregistered
        @type event_name: String
        @param event_name: The name of the event to be unregistered
        """

        # in case the plugin is not loaded or lazy loaded
        if not plugin.is_loaded_or_lazy_loaded():
            return

        # unregisters the plugin event in the plugin containing the event
        plugin.unregister_plugin_event(self, event_name)

        if event_name in self.event_plugins_registered_loaded_map:
            if plugin in self.event_plugins_registered_loaded_map[event_name]:
                self.event_plugins_registered_loaded_map[event_name].remove(plugin)

    def register_for_plugin_manager_event(self, event_name):
        """
        Registers a given plugin manager event in self

        @type event_neme: String
        @param event_name: The name of the event to be registered
        """

        # retrieves the plugin manager
        plugin_manager = self.manager

        # registers the plugin event in the plugin manager containing the event
        plugin_manager.register_plugin_manager_event(self, event_name)

        # appends the plugin manager containing the event to be registered to the plugin manager events map
        self.event_plugin_manager_registered_loaded_list.append(event_name)

    def unregister_for_plugin_manager_event(self, event_name):
        """
        Unregisters a given plugin manager event in self

        @type event_name: String
        @param event_name: The name of the event to be unregistered
        """

        # retrieves the plugin manager
        plugin_manager = self.manager

        # unregisters the plugin event in the plugin manager containing the event
        plugin_manager.unregister_plugin_manager_event(self, event_name)

        if event_name in self.event_plugin_manager_registered_loaded_list:
            self.event_plugin_manager_registered_loaded_list.remove(event_name)

    def unregister_all_for_plugin_event(self, event_name):
        """
        Unregisters all the handlers for the event with the given name

        @type event_name: String
        @param event_name: The name of the event to be unregistered
        """

        if event_name in self.event_plugins_registered_loaded_map:
            for plugin in self.event_plugins_registered_loaded_map[event_name]:
                if plugin.is_loaded_or_lazy_loaded():
                    self.unregister_for_plugin_event(plugin, event_name)

    def unregister_all_for_plugin(self):
        """
        Unregisters all the event handlers for the events of self
        """

        for event_name in self.event_plugins_registered_loaded_map:
            self.unregister_all_for_plugin_event(event_name)

    def register_plugin_event(self, plugin, event_name):
        """
        Registers a given event in the given plugin

        @type plugin: Plugin
        @param plugin: The plugin containing the handler to the event
        @type event_name: String
        @param event_name: The name of the event to be registered
        """

        if not event_name in self.event_plugins_handled_loaded_map:
            self.event_plugins_handled_loaded_map[event_name] = []

        if not plugin in self.event_plugins_handled_loaded_map[event_name]:
            self.event_plugins_handled_loaded_map[event_name].append(plugin)
            self.info("Registering event '%s' from '%s' v%s in '%s' v%s" % (event_name, plugin.short_name, plugin.version, self.short_name, self.version))

    def unregister_plugin_event(self, plugin, event_name):
        """
        Unregisters a given event in the given plugin

        @type plugin: Plugin
        @param plugin: The plugin containing the handler to the event
        @type event_name: String
        @param event_name: The name of the event to be unregistered
        """

        if event_name in self.event_plugins_handled_loaded_map:
            if plugin in self.event_plugins_handled_loaded_map[event_name]:
                self.event_plugins_handled_loaded_map[event_name].remove(plugin)
                self.info("Unregistering event '%s' from '%s' v%s in '%s' v%s" % (event_name, plugin.short_name, plugin.version, self.short_name, self.version))

    def notify_handlers(self, event_name, event_args):
        """
        Notifies all the handlers for the event with the given name with the give arguments

        @type event_name: String
        @param event_name: The name of the event to be notified
        @type event_args: List
        @param event_args: The arguments to be passed to the handler
        """

        # the names of the events handled by self
        event_names_list = self.event_plugins_handled_loaded_map.keys()

        # retrieves all the events and super events that match the generated event
        events_or_super_events_list = get_all_events_or_super_events_in_list(event_name, event_names_list)

        # iterates over all the events and super events for notification
        for event_or_super_event in events_or_super_events_list:
            if event_or_super_event in self.event_plugins_handled_loaded_map:
                # iterates over all the plugins registered for notification
                for event_plugin_loaded in self.event_plugins_handled_loaded_map[event_or_super_event]:
                    self.info("Notifying '%s' v%s about event '%s' generated in '%s' v%s" % (event_plugin_loaded.short_name, event_plugin_loaded.version, event_name, self.short_name, self.version))

                    event_plugin_loaded.event_handler(event_name, *event_args)

    def generate_event(self, event_name, event_args):
        """
        Generates an event and starts the process of handler notification

        @type event_name: String
        @param event_name: The name of the event to be notified
        @type event_args: List
        @param event_args: The arguments to be passed to the handler
        """

        if not is_event_or_super_event_in_list(event_name, self.events_handled):
            return
        self.info("Event '%s' generated in '%s' v%s" % (event_name, self.short_name, self.version))

        self.notify_handlers(event_name, event_args)

    def event_handler(self, event_name, *event_args):
        """
        The top level event handling method

        @type event_name: String
        @param event_name: The name of the event triggered
        @type event_args: List
        @param event_args: The arguments for the handler
        """

        self.info("Event '%s' caught in '%s' v%s" % (event_name, self.short_name, self.version))

    def reload_main_modules(self):
        """
        Reloads the plugin main modules in the interpreter
        """

        self.info("Reloading main modules in '%s' v%s" % (self.short_name, self.version))

        # iterates over all the main modules
        for main_module in self.main_modules:
            # in case the main module is already loaded
            if main_module in sys.modules:
                # retrieves the main module value
                main_module_value = sys.modules[main_module]

                # reloads the main module
                reload(main_module_value)

    def get_configuration_property(self, property_name):
        """
        Returns the configuration property for the given property name.

        @type property_name: String
        @param property_name: The property name to retrieve the property.
        @rtype: Object
        @return: The configuration property for the given property name.
        """

        return self.configuration_map[property_name]

    def set_configuration_property(self, property_name, property):
        """
        Sets the configuration property for the given property name.

        @type property_name: String
        @param property_name: The property name to set the property.
        @type property: String
        @param property: The property name to set.
        """

        self.configuration_map[property_name] = property

    def is_loaded(self):
        """
        Returns the result of the loading test

        @rtype: bool
        @return: The result of the loading test (if the plugin is loaded or not)
        """

        return self.loaded and not self.lazy_loaded

    def is_lazy_loaded(self):
        """
        Returns the result of the lazy loading test

        @rtype: bool
        @return: The result of the lazy loading test (if the plugin is lazy loaded or not)
        """

        return self.lazy_loaded

    def is_loaded_or_lazy_loaded(self):
        """
        Returns the result of the loading and lazy loading tests

        @rtype: bool
        @return: The result of the loading and lazy loading tests (if the plugin is loaded or lazy loaded or not)
        """

        return self.loaded or self.lazy_loaded

    def contains_metadata(self):
        """
        Returns the result of the metadata test

        @rtype: bool
        @return: The result of the metadata test (if the plugin contains metadata or not)
        """

        if hasattr(self, "metadata_map"):
            return True
        else:
            return False

    def contains_metadata_key(self, metadata_key):
        """
        Returns the result of the metadata key test

        @type metadata_key: String
        @param metadata_key: The value of the metadata key to test for metadata
        @rtype: bool
        @return: The result of the metadata key test (if the plugin contains the metadata key or not)
        """

        if self.contains_metadata():
            if metadata_key in self.metadata_map:
                return True
            else:
                return False
        else:
            return False

    def get_metadata(self):
        """
        Returns the metadata of the plugin

        @rtype: Dictionary
        @return: The metadata of the plugin
        """

        if self.contains_metadata():
            return self.metadata_map

    def get_metadata_key(self, metadata_key):
        """
        Returns the metadata key of the plugin

        @type metadata_key: String
        @param metadata_key: The value of the metadata key to retrieve
        @rtype: Object
        @return: The metadata key of the plugin
        """

        if self.contains_metadata_key(metadata_key):
            return self.metadata_map[metadata_key]

    def treat_exception(self, exception):
        """
        Treats the exception at the most abstract level

        @type exception: Exception
        @param exception: The exception object to be treated
        """

        self.info("Exception '%s' generated in '%s' v%s" % (str(exception), self.short_name, self.version))
        self.manager.unload_plugin(self.id)

    def release_ready_semaphore(self):
        """
        Releases the ready semaphore (usefull for thread enabled plugins)
        """

        # releases the ready semaphore
        self.ready_semaphore.release()

    def get_all_plugin_dependencies(self):
        """
        Retrieves all the plugin dependencies of the plugin

        @rtype: List
        @requires: A list containing all the plugin dependencies of the plugin
        """

        plugin_dependencies = []

        for dependency in self.dependencies:
            if isinstance(dependency, PluginDependency):
                plugin_dependencies.append(dependency)

        return plugin_dependencies

    def get_all_package_dependencies(self):
        """
        Retrieves all the packages dependencies of the plugin

        @rtype: List
        @requires: A list containing all the package dependencies of the plugin
        """

        package_dependencies = []

        for dependency in self.dependencies:
            if isinstance(dependency, PackageDependency):
                package_dependencies.append(dependency)

        return package_dependencies

    def get_tuple(self):
        """
        Retrieves a tuple representing the plugin (id and version)

        @rtype: Tuple
        @return: Tuple representing the plugin (id and version)
        """

        return (self.id, self.version)

    def log_stack_trace(self):
        """
        Logs the current stack trace to the plugin manager logger
        """

        formated_traceback = traceback.format_tb(sys.exc_traceback)

        # iterates over the traceback lines
        for formated_traceback_line in formated_traceback:
            self.debug(formated_traceback_line)

    def debug(self, message):
        """
        Adds the given debug message to the logger

        @type message: String
        @param message: The debug message to be added to the logger
        """

        logger_message = self.format_logger_message(message)
        self.logger.debug(logger_message)

    def info(self, message):
        """
        Adds the given info message to the logger

        @type message: String
        @param message: The info message to be added to the logger
        """

        logger_message = self.format_logger_message(message)
        self.logger.info(logger_message)

    def warning(self, message):
        """
        Adds the given warning message to the logger

        @type message: String
        @param message: The warning message to be added to the logger
        """

        logger_message = self.format_logger_message(message)
        self.logger.warning(logger_message)

    def error(self, message):
        """
        Adds the given error message to the logger

        @type message: String
        @param message: The error message to be added to the logger
        """

        logger_message = self.format_logger_message(message)
        self.logger.error(logger_message)

    def critical(self, message):
        """
        Adds the given critical message to the logger

        @type message: String
        @param message: The critical message to be added to the logger
        """

        logger_message = self.format_logger_message(message)
        self.logger.critical(logger_message)

    def format_logger_message(self, message):
        """
        Formats the given message into a logging message

        @type message: String
        @param message: The message to be formated into logging message
        @rtype: String
        @return: The formated logging message
        """

        # the default formatting message
        formatting_message = ""

        # in case the plugin id logging option is activated
        if plugin_manager_configuration.get("plugin_id_logging", False):
            formatting_message += "[" + self.id + "] "

        # in case the thread id logging option is activated
        if plugin_manager_configuration.get("thread_id_logging", False):
            formatting_message += "[" + str(thread.get_ident()) + "] "

        # appends the formatting message to the logging message
        logger_message = formatting_message + message

        return logger_message

class PluginManagerPlugin(Plugin):
    """
    The plugin manager plugin class, used to extend the plugin manager functionality
    """

    valid = False

    def __init__(self, manager = None):
        Plugin.__init__(self, manager)

class PluginManager:
    """
    The plugin manager class
    """

    uid = None
    """ The unique identification """

    logger = None
    """ The logger used """

    platform = None
    """ The current executing platform """

    semaphore = None
    """ The semaphore used in the event queue """

    init_complete = False
    """ The initialization complete flag """

    init_complete_handlers = []
    """ The list of handlers to be called at the end of the plugin manager initialization """

    main_loop_active = True
    """ The boolean value for the main loop activation """

    container = "default"
    """ The name of the plugin manager container """

    attributes_map = {}
    """ The attributes map """

    plugin_manager_plugins_loaded = False
    """ The plugin manager plugins loaded flag """

    current_id = 0
    """ The current id used for the plugin """

    event_queue = []
    """ The queue of events to be processed """

    plugin_paths = None
    """ The set of paths for the loaded plugins """

    refered_modules = []
    """ The refered modules """

    loaded_plugins = []
    """ The loaded plugins """

    loaded_plugins_map = {}
    """ The map with classes associated with strings containing the id of the plugin """

    loaded_plugins_id_map = {}
    """ The map with the id of the plugin associated with the plugin id """

    id_loaded_plugins_map = {}
    """ The map with the plugin id associated with the id of the plugin """

    loaded_plugins_descriptions = []
    """ The descriptions of the loaded plugins """

    plugin_instances = []
    """ The instances of the created plugins """

    plugin_instances_map = {}
    """ The map with instances associated with strings containing the id of the plugin """

    plugin_dirs_map = {}
    """ The map associating directories with the id of the plugin """

    capabilities_plugin_instances_map = {}
    """ The map associating capabilities with plugin instances """

    capabilities_sub_capabilities_map = {}
    """ The map associating capabilities with sub capabilities """

    plugin_threads = []
    """ The list of active running threads """

    plugin_threads_map = {}
    """ The map associating the active running threads with the id of the plugin """

    plugin_dependent_plugins_map = {}
    """ The map associating the plugins that depend on the plugin with the id of the plugin """

    plugin_allowed_plugins_map = {}
    """ The map associating the plugins that allow the plugin with the id of the plugin """

    capabilities_plugins_map = {}
    """ The map associating the capabilities  with the the plugin that supports the capability """

    deleted_plugin_classes = []
    """ The list containing the classes for the deleted plugins """

    event_plugins_handled_loaded_map = {}
    """ The map with the plugin associated with the name of the event handled """

    def __init__(self, plugin_paths = None, platform = CPYTHON_ENVIRONMENT, init_complete_handlers = [], main_loop_active = True, container = "default", attributes_map = {}):
        """
        Constructor of the class

        @type plugin_paths: List
        @param plugin_paths: The list of directory paths for the loading of the plugins
        @type platform: int
        @param platform: The current executing platform
        @type init_complete_handlers: List
        @param init_complete_handlers: The list of handlers to be called at the end of the plugin manager initialization
        @type main_loop_active: bool
        @param main_loop_active: The boolean value for the main loop activation
        @type container: String
        @param container: The name of the plugin manager container
        @type attributes_map: Dictionary
        @param attributes_map: The map associating the attribute key and the attribute value
        """

        self.plugin_paths = plugin_paths
        self.platform = platform
        self.init_complete_handlers = init_complete_handlers
        self.main_loop_active = main_loop_active
        self.container = container
        self.attributes_map = attributes_map

        self.uid = colony.plugins.util.get_timestamp_uid()
        self.semaphore = threading.BoundedSemaphore()

        self.current_id = 0
        self.event_queue = []
        self.refered_modules = []
        self.loaded_plugins = []
        self.loaded_plugins_map = {}
        self.loaded_plugins_id_map = {}
        self.id_loaded_plugins_map = {}
        self.loaded_plugins_descriptions = []
        self.plugin_instances = []
        self.plugin_instances_map = {}
        self.plugin_dirs_map = {}
        self.capabilities_plugin_instances_map = {}
        self.capabilities_sub_capabilities_map = {}
        self.plugin_threads = []
        self.plugin_threads_map = {}
        self.plugin_dependent_plugins_map = {}
        self.plugin_allowed_plugins_map = {}
        self.capabilities_plugins_map = {}
        self.deleted_plugin_classes = []
        self.event_plugins_handled_loaded_map = {}

    def start_logger(self, log_level = DEFAULT_LOGGING_LEVEL):
        """
        Starts the logging system with the given log level

        @type log_level: int
        @param log_level: The log level of the logger
        """

        logger = logging.getLogger(DEFAULT_LOGGER)
        logger.setLevel(log_level)
        stream_handler = logging.StreamHandler()
        logging_format = plugin_manager_configuration.get("logging_format", DEFAULT_LOGGING_FORMAT)
        formatter = logging.Formatter(logging_format)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        self.logger = logger

    def load_system(self):
        """
        Starts the process of loading the plugin system
        """

        self.logger.info("Starting plugin manager...")

        # gets all modules from all plugin paths
        for plugin_path in self.plugin_paths:
            self.refered_modules.extend(self.get_all_modules(plugin_path))

        # starts the plugin loading process
        self.init_plugin_system({"plugin_paths": self.plugin_paths, "plugins": self.refered_modules})

        # starts the main loop
        self.main_loop()

    def unload_system(self):
        """
        Unloads the plugin system from memory, exiting the system
        """

        for plugin_instance in self.plugin_instances:
            if plugin_instance.is_loaded():
                self._unload_plugin(plugin_instance, None)

        exit_event = colony.plugins.util.Event("exit")
        self.add_event(exit_event)

    def main_loop(self):
        """
        The main loop for the plugin manager
        """

        # main loop cycle
        while self.main_loop_active:
            self.semaphore.acquire()
            while len(self.event_queue):
                event = self.event_queue.pop(0)
                if event.event_name == "execute":
                    execution_method = event.event_args[0]
                    execution_arguments = event.event_args[1:]
                    execution_method(*execution_arguments)
                elif event.event_name == "exit":
                    # creates the exit event
                    exit_event = colony.plugins.util.Event("exit")

                    # iterates over all the available plugin threads
                    # joining all the threads
                    for plugin_thread in self.plugin_threads:
                        # sends the exit event to the plugin thread
                        plugin_thread.add_event(exit_event)
                        plugin_thread.join()

                    # returns the methos exiting the plugin system
                    return

    def add_event(self, event):
        """
        Adds an event to the list of events in the plugin manager

        @type event: Event
        @param event: The event to add to the list of events in the plugin manager
        """

        self.event_queue.append(event)
        self.semaphore.release()

    def get_all_modules(self, path):
        """
        Retrieves all the modules in a given path

        @type path: String
        @param path: The path to retrieve the modules
        """

        modules = []

        if not os.path.exists(path):
            self.logger.warning("Path '%s' does not exist in the current filesystem" % (path))
            return modules

        dir_list = os.listdir(path)
        for file_name in dir_list:
            full_path = path + "/" + file_name
            mode = os.stat(full_path)[stat.ST_MODE]
            if not stat.S_ISDIR(mode):
                split = os.path.splitext(file_name)
                extension = split[-1]
                if extension == ".py" or extension == ".pyc":
                    module_name = string.join(split[:-1], "")
                    if not module_name in modules:
                        modules.append(module_name)
        return modules

    def init_plugin_system(self, configuration):
        """
        Starts the plugin loading process

        @type configuration: Dictionary
        @param configuration: The configuration structure
        """

        # adds the defined plugin paths to the system python path
        self.set_python_path(configuration["plugin_paths"])

        # loads the plugin files into memory
        self.load_plugins(configuration["plugins"])

        # starts all the available the plugin manager plugins
        self.start_plugin_manager_plugins()

        # loads the plugin manager plugins
        self.load_plugin_manager_plugins()

        # sets the plugin manager plugins loaded to true
        self.set_plugin_manager_plugins_loaded(True)

        # starts all the available the plugins
        self.start_plugins()

        # loads the startup plugins
        self.load_startup_plugins()

        # loads the main plugins
        self.load_main_plugins()

        # sets the init flag to true
        self.set_init_complete(True)

        # notifies all the loaded plugins about the init load complete
        self.notify_load_complete_loaded_plugins()

        # notifies all the init complete handlers about the init load complete
        self.notify_load_complete_handlers()

    def set_python_path(self, plugin_paths):
        """
        Updates the python path adding the defined list of plugin paths

        @type plugin_paths: List
        @param plugin_paths: The list of python paths to add to the python path
        """

        # iterates over all the plugin paths in plugin_paths
        for plugin_path in plugin_paths:
            # if the path is not in the python lib
            # path inserts the path into it
            if not plugin_path in sys.path:
                sys.path.insert(0, plugin_path)

    def load_plugins(self, plugins):
        """
        Imports a module starting the plugin

        @type plugins: List
        @param plugins: The list of plugins to be loaded
        """

        # iterates over all the available plugins
        for plugin in plugins:
            # in case the plugin module is not currently loaded
            if not plugin in sys.modules:
                # imports the plugin module file
                __import__(plugin)

    def start_plugin_manager_plugins(self):
        """
        Starts all the available plugin manger plugins, creating a singleton instance for each of them
        """

        # retrieves all the plugin manger plugin classes available
        plugin_classes = self.get_all_plugin_classes(PluginManagerPlugin)

        # iterates over all the available plugin manger plugin classes
        for plugin in plugin_classes:
            # tests the plugin for loading
            if not plugin in self.loaded_plugins:
                # starts the plugin
                self.start_plugin(plugin)

    def start_plugins(self):
        """
        Starts all the available plugins, creating a singleton instance for each of them
        """

        # retrieves all the plugin classes available
        plugin_classes = self.get_all_plugin_classes()

        # iterates over all the available plugin classes
        for plugin in plugin_classes:
            # tests the plugin for loading
            if not plugin in self.loaded_plugins:
                # starts the plugin
                self.start_plugin(plugin)

    def start_plugin(self, plugin):
        """
        Starts the given plugin, creating a singleton instance

        @type plugin: Class
        @param plugin: The plugin to start
        """

        # retrieves the plugin id
        plugin_id = plugin.id

        # retrieves the plugin version
        plugin_version = plugin.version

        # retrieves the plugin description
        plugin_description = plugin.description

        # instanciates the plugin to create the singleton plugin instance
        plugin_instance = plugin(self)

        # retrieves the path to the plugin file
        plugin_path = inspect.getfile(plugin)

        # retrieves the absolute path to the plugin file
        absolute_plugin_path = os.path.abspath(plugin_path)

        # retrieves the path to the directory containing the plugin file
        plugin_dir = os.path.dirname(absolute_plugin_path)

        # starts all the plugin manager structures relateds with plugins
        self.loaded_plugins.append(plugin)
        self.loaded_plugins_map[plugin_id] = plugin
        self.loaded_plugins_id_map[plugin_id] = self.current_id
        self.id_loaded_plugins_map[self.current_id] = plugin_id
        self.loaded_plugins_descriptions.append(plugin_description)
        self.plugin_instances.append(plugin_instance)
        self.plugin_instances_map[plugin_id] = plugin_instance
        self.plugin_dirs_map[plugin_id] = plugin_dir

        # registers the plugin capabilities in the plugin manager
        self.register_plugin_capabilities(plugin_instance)

        # increments the current id
        self.current_id += 1

    def stop_plugin_complete_by_id(self, plugin_id):
        """
        Stops a plugin with the given id, removing it and the refering module from the plugin system

        @type plugin_id: String
        @param plugin: The id of the plugin to be removed from the plugin system
        """

        # retrieves the refering plugin module
        module = self.get_plugin_module_name_by_id(plugin_id)

        # stops the refering plugin module
        self.stop_module(module)

    def stop_module(self, module):
        """
        Stops the given plugin module in the plugin manager

        @type module: String
        @param module: The name of the plugin module to stop
        """

        # retrieves the module object from the loaded modules
        module_obj = sys.modules[module]

        # retrieves the plugin class for the given module
        plugin_class = self.get_plugin_class_by_module_name(module)

        # stops the plugin
        self.stop_plugin(plugin_class)

        # removes the plugin class from the plugin
        delattr(module_obj, plugin_class.__name__)

        # adds the plugin class to the list of deleted plugin classes
        self.deleted_plugin_classes.append(plugin_class)

        # deletes the module from the list of loaded modules
        del sys.modules[module]

    def stop_plugin(self, plugin):
        """
        Stops a plugin, removing it from the plugin system

        @type plugin: Plugin
        @param plugin: The plugin to be removed from the plugin system
        """

        # retrieves the plugin id
        plugin_id = plugin.id

        # retrieves the plugin version
        plugin_version = plugin.version

        # retrieves the plugin description
        plugin_description = plugin.description

        # retrieves the temporary internal plugin id
        current_id = self.loaded_plugins_id_map[plugin_id]

        # retrives the plugin instance
        plugin_instance = self.plugin_instances_map[plugin_id]

        # in case the plugin is loaded the plugin is unloaded
        if plugin_instance.is_loaded():
            self._unload_plugin(plugin_instance, FILE_REMOVED_TYPE)

        # removes all the plugin class resources
        self.loaded_plugins.remove(plugin)
        del self.loaded_plugins_map[plugin_id]
        del self.loaded_plugins_id_map[plugin_id]
        del self.id_loaded_plugins_map[current_id]
        self.loaded_plugins_descriptions.remove(plugin_description)

        # removes the generic plugin instance resources
        self.plugin_instances.remove(plugin_instance)
        del self.plugin_instances_map[plugin_id]
        del self.plugin_dirs_map[plugin_id]

        # unregisters the plugin capabilities in the plugin manager
        self.unregister_plugin_capabilities(plugin_instance)

        # unregisters the decorator information associated with the plugin
        colony.plugins.decorators.unregister_plugin_decorators(plugin_id, plugin_version)

        # in case the plugin exists in the plugin threads map
        if plugin_id in self.plugin_threads_map:
            # retrieves the available thread for the plugin
            plugin_thread = self.plugin_threads_map[plugin_id]

            # creates the plugin exit event
            event = colony.plugins.util.Event("exit")

            # adds the load event to the thread queue
            plugin_thread.add_event(event)

            # joins the plugin thread
            plugin_thread.join()

            # removes the plugin thread from the plugin threads map
            del self.plugin_threads_map[plugin_id]

    def get_all_plugin_classes(self, base_plugin_class = Plugin):
        """
        Retrieves all the available plugin classes, from the defined base plugin class

        @type base_plugin_class: Class
        @param base_plugin_class: The base plugin class to retrieve the plugin classes
        @rtype: List
        @return: The list of plugin classes
        """

        plugin_classes = []
        self.get_plugin_sub_classes(base_plugin_class, plugin_classes)
        return plugin_classes

    def get_plugin_sub_classes(self, plugin, plugin_classes):
        """
        Retrieves all the sub classes for the given plugin class

        @type plugin: Class
        @param plugin: The plugin class to retrieve the sub classes
        @type plugin_classes: List
        @param plugin_classes: The current list of plugin sub classes
        @rtype: List
        @return: The list of all the sub classes for the given plugin class
        """

        # retrieves all the plugin sub classes
        sub_classes = plugin.__subclasses__()

        # iterates over all the plugin sub classes
        for sub_class in sub_classes:
            self.get_plugin_sub_classes(sub_class, plugin_classes)
            if sub_class.valid and not sub_class in self.deleted_plugin_classes:
                plugin_classes.append(sub_class)

    def register_plugin_capabilities(self, plugin):
        """
        Registers all the available capabilities for the given plugin

        @type plugin: String
        @param plugin: The plugin to register the capabilities
        """

        # iterates over all the plugin instance capabilities
        for capability in plugin.capabilities:
            capability_and_super_capabilites_list = capability_and_super_capabilites(capability)

            for capability_or_super_capability_index in range(len(capability_and_super_capabilites_list)):
                capability = capability_and_super_capabilites_list[capability_or_super_capability_index]
                sub_capabilities_list = capability_and_super_capabilites_list[capability_or_super_capability_index + 1:]

                if not capability in self.capabilities_plugin_instances_map:
                    self.capabilities_plugin_instances_map[capability] = []
                self.capabilities_plugin_instances_map[capability].append(plugin)

                if not capability in self.capabilities_sub_capabilities_map:
                    self.capabilities_sub_capabilities_map[capability] = []

                for sub_capability in sub_capabilities_list:
                    if not sub_capability in self.capabilities_sub_capabilities_map[capability]:
                        self.capabilities_sub_capabilities_map[capability].append(sub_capability)

    def unregister_plugin_capabilities(self, plugin):
        """
        Unregisters all the available capabilities for the given plugin

        @type plugin: String
        @param plugin: The plugin to unregister the capabilities
        """

        # iterates over all the plugin instance capabilities
        for capability in plugin.capabilities:
            capability_and_super_capabilites_list = capability_and_super_capabilites(capability)

            for capability_or_super_capability_index in range(len(capability_and_super_capabilites_list)):
                capability = capability_and_super_capabilites_list[capability_or_super_capability_index]
                sub_capabilities_list = capability_and_super_capabilites_list[capability_or_super_capability_index + 1:]

                if capability in self.capabilities_plugin_instances_map:
                    if plugin in self.capabilities_plugin_instances_map[capability]:
                        self.capabilities_plugin_instances_map[capability].remove(plugin)

                if capability in self.capabilities_sub_capabilities_map:
                    for sub_capability in sub_capabilities_list:
                        if sub_capability in self.capabilities_sub_capabilities_map[capability]:
                            if len(self.capabilities_plugin_instances_map[sub_capability]) == 0:
                                self.capabilities_sub_capabilities_map[capability].remove(sub_capability)

    def load_plugin_manager_plugins(self):
        """
        Loads the set of plugin manager plugins
        """

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # searches for the plugin manager extension type in the plugin capabilities
            if PLUGIN_MANAGER_EXTENSION_TYPE in plugin.capabilities:
                # loads the plugin
                self._load_plugin(plugin, None, PLUGIN_MANAGER_EXTENSION_TYPE)

    def load_startup_plugins(self):
        """
        Loads the set of startup plugins, starting the system bootup process
        """

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # searches for the startup type in the plugin capabilities
            if STARTUP_TYPE in plugin.capabilities:
                # loads the plugin
                self._load_plugin(plugin, None, STARTUP_TYPE)

    def load_main_plugins(self):
        """
        Loads the set of main plugins, staritng the system bootup process
        """

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # searches for the main type in the plugin capabilities
            if MAIN_TYPE in plugin.capabilities:
                # loads the plugin
                self._load_plugin(plugin, None, MAIN_TYPE)

    def notify_load_complete_loaded_plugins(self):
        """
        Notifies the loaded plugins about the load complete
        """

        # retrieves the loaded plugins list
        loaded_plugins_list = self.get_all_loaded_plugins()

        # iterates over all the loaded plugins
        for loaded_plugin in loaded_plugins_list:
            # notifies the plugin about the load complete
            loaded_plugin.init_complete()

    def notify_load_complete_handlers(self):
        """
        Notifies the init complete handlers about the load complete
        """

        # iterates over all the init complete handlers
        for init_complete_handler in self.init_complete_handlers:
            init_complete_handler()

    def __load_plugin(self, plugin, type = None, loading_type = None):

        # in case the plugin is loaded
        if plugin.is_loaded():
            return True

        # in case the plugin is lazy loaded
        if (plugin.loading_type == LAZY_LOADING_TYPE and not type == FULL_LOAD_TYPE) and plugin.is_lazy_loaded():
            return True

        if not self.test_plugin_load(plugin):
            self.logger.info("Plugin '%s' v%s not ready to be loaded" % (plugin.short_name, plugin.version))
            return False

        if not loading_type and MAIN_TYPE in plugin.capabilities:
            if not self._load_plugin(plugin, type, MAIN_TYPE):
                return False
        elif not loading_type and THREAD_TYPE in plugin.capabilities:
            if not self._load_plugin(plugin, type, THREAD_TYPE):
                return False
        else:
            if not self._load_plugin(plugin, type, loading_type):
                return False

        self.inject_all_allowed(plugin)

        return True

    def _load_plugin(self, plugin, type = None, loading_type = None):

        # in case there is an handler for the plugin loading
        if self.exists_plugin_manager_plugin_execute_conditional("_load_plugin", [plugin, type, loading_type]):
            return self.plugin_manager_plugin_execute_conditional("_load_plugin", [plugin, type, loading_type])

        # in case the return from the handler of the initialization of the plugin load returns false
        if not self.plugin_manager_plugin_execute("init_plugin_load", [plugin, type, loading_type]):
            return False

        # in case the plugin is loaded
        if plugin.is_loaded():
            return True

        # in case the plugin is lazy loaded
        if (plugin.loading_type == LAZY_LOADING_TYPE and not type == FULL_LOAD_TYPE) and plugin.is_lazy_loaded():
            return True

        if not self.test_plugin_load(plugin):
            self.logger.info("Plugin '%s' v%s not ready to be loaded" % (plugin.short_name, plugin.version))
            return False

        if type:
            self.logger.info("Loading of type: '%s'" % (type))

        # in case the plugin to be loaded is either of type main or thread
        if loading_type == MAIN_TYPE or loading_type == THREAD_TYPE:
            if plugin.id in self.plugin_threads_map:
                # retrieves the available thread for the plugin
                plugin_thread = self.plugin_threads_map[plugin.id]

                self.logger.info("Thread restarted for plugin '%s' v%s" % (plugin.short_name, plugin.version))
            else:
                # creates a new tread to run the main plugin
                plugin_thread = PluginThread(plugin)

                # starts the thread
                plugin_thread.start()

                self.plugin_threads.append(plugin_thread)
                self.plugin_threads_map[plugin.id] = plugin_thread

                self.logger.info("New thread started for plugin '%s' v%s" % (plugin.short_name, plugin.version))

            # sets the plugin load as not completed
            plugin_thread.set_load_complete(False);

            # in case the loading type of the plugin is eager
            if plugin.loading_type == EAGER_LOADING_TYPE or type == FULL_LOAD_TYPE:
                # creates the plugin load event
                event = colony.plugins.util.Event("load")
            else:
                # creates the plugin lazy load event
                event = colony.plugins.util.Event("lazy_load")

            # adds the load event to the thread queue
            plugin_thread.add_event(event)

            # acquires the ready semaphore for the beginning of the loading process
            plugin.ready_semaphore.acquire()
        else:
            # in case the loading type of the plugin is eager
            if plugin.loading_type == EAGER_LOADING_TYPE or type == FULL_LOAD_TYPE:
                # calls the load plugin method in the plugin (plugin bootup process)
                plugin.load_plugin()
            elif plugin.loading_type == LAZY_LOADING_TYPE:
                # calls the lazy load plugin method in the plugin (plugin bootup process)
                plugin.lazy_load_plugin()

        # in case the loading type is lazy, the loading task is complete
        if plugin.loading_type == LAZY_LOADING_TYPE and not type == FULL_LOAD_TYPE:
            return True

        # resolves the capabilities of the plugin
        if not self.resolve_capabilities(plugin):
            return False

        # injects the plugin dependencies
        if not self.inject_dependencies(plugin):
            return False

        # in case the plugin to be loaded is either of type main or thread
        if loading_type == MAIN_TYPE or loading_type == THREAD_TYPE:
            # sets the plugin end load as not completed
            plugin_thread.set_end_load_complete(False);

            # creates the plugin end load event
            event = colony.plugins.util.Event("end_load")

            # adds the end load event to the thread queue
            plugin_thread.add_event(event)

            # acquires the ready semaphore for the beginning of the end loading process
            plugin.ready_semaphore.acquire()
        else:
            # calls the end load plugin method in the plugin (plugin bootup process)
            plugin.end_load_plugin()

        # injects the allowed plugins into the plugin
        if not self.inject_allowed(plugin):
            return False

        # retrieves the current loading state for the plugin manager
        if self.get_init_complete():
            # notifies the plugin about the load complete
            plugin.init_complete()

        # generates the loaded plugin event
        self.generate_event("plugin_manager.loaded_plugin", [plugin.id, plugin.version, plugin])

        return True

    def _unload_plugin(self, plugin, type = None, unloading_type = None):

        # in case the plugin is not loaded
        if not plugin.is_loaded():
            return True

        if type:
            self.logger.info("Unloading of type: '%s'" % (type))

        # unloads the plugins that depend on the plugin being unloaded
        for dependent_plugin in self.get_plugin_dependent_plugins_map(plugin.id):
            if dependent_plugin.is_loaded():
                self._unload_plugin(dependent_plugin, DEPENDENCY_TYPE)

        # notifies the allowed plugins about the unload
        for allowed_plugin_info in self.get_plugin_allowed_plugins_map(plugin.id):
            allowed_plugin = allowed_plugin_info[0]
            allowed_capability = allowed_plugin_info[1]
            if allowed_plugin.is_loaded():
                allowed_plugin.unload_allowed(plugin, allowed_capability)

        # clears the map for the dependent plugins
        self.clear_plugin_dependent_plugins_map(plugin.id)

        # clears the map for the allowed plugins
        self.clear_plugin_allowed_plugins_map(plugin.id)

        # clears the map for the capabilities plugins
        self.clear_capabilities_plugins_map_for_plugin(plugin.id)

        # unloads the plugin
        plugin.unload_plugin()

        # finishes the unloading process of the plugin
        plugin.end_unload_plugin()

        # if it's a main or thread type unload
        if unloading_type == MAIN_TYPE or unloading_type == THREAD_TYPE:
            pass

        return True

    def test_plugin_load(self, plugin):

        if not self.plugin_manager_plugin_execute("test_plugin_load", [plugin]):
            return False

        # retrieves the plugin id
        plugin_id = plugin.id

        # retrieves the plugin version
        plugin_version = plugin.version

        # tests the plugin against the current platform
        if not self.test_platform_compatible(plugin):
            self.logger.info("Current platform (%s) not compatible with plugin '%s' v%s" % (self.platform, plugin.short_name, plugin.version))
            return False

        # tests the plugin for the availability of the dependencies
        if not self.test_dependencies_available(plugin):
            self.logger.info("Missing dependencies for plugin '%s' v%s" % (plugin.short_name, plugin.version))
            return False

        if not plugin_id in self.loaded_plugins_map:
            return False

        return True

    def test_dependencies_available(self, plugin):
        plugin_dependencies = plugin.dependencies

        # iterates over all the plugin dependencies
        for plugin_dependency in plugin_dependencies:

            # in case the test dependency tests fails
            if not plugin_dependency.test_dependency(self):
                self.logger.info("Problem with dependency for plugin '%s' v%s" % (plugin.short_name, plugin.version))
                return False

        return True

    def test_platform_compatible(self, plugin):
        plugin_platforms_list = plugin.platforms

        if self.platform in plugin_platforms_list:
            return True
        else:
            return False

    def resolve_capabilities(self, plugin):
        # adds itself to the map of plugins that have a given capability
        for plugin_capability_allowed in plugin.capabilities_allowed:
            self.add_capabilities_plugins_map(plugin_capability_allowed, plugin)

        return True

    def inject_dependencies(self, plugin):
        # gets all the dependencies of the plugin
        plugin_dependencies = plugin.dependencies

        # iterates over all the dependencies of the plugin
        for plugin_dependency in plugin_dependencies:
            if plugin_dependency.__class__ == PluginDependency:
                dependency_plugin_instance = self._get_plugin_by_id_and_version(plugin_dependency.plugin_id, plugin_dependency.plugin_version)
                if not self.__load_plugin(dependency_plugin_instance, DEPENDENCY_TYPE):
                    return False
                if dependency_plugin_instance:
                    plugin.dependency_injected(dependency_plugin_instance)
                    self.add_plugin_dependent_plugins_map(plugin_dependency.plugin_id, plugin)

        return True

    def inject_allowed(self, plugin):
        """
        Injects all the allowed plugins for the given plugin

        @type plugin: Plugin
        @param plugin: The plugin to inject the dependencies
        """

        # gets all the capabilities allowed of the plugin
        plugin_capabilities_allowed = plugin.capabilities_allowed

        # iterates over all the capabilities of the plugin
        for plugin_capability_allowed in plugin_capabilities_allowed:
            # gets all the plugins of the defined capability
            allowed_plugins = self._get_plugins_by_capability_cache(plugin_capability_allowed)

            # iterates over all the plugins of the defined capability
            for allowed_plugin in allowed_plugins:
                if self.__load_plugin(allowed_plugin, ALLOWED_TYPE):
                    self._inject_allowed(plugin, allowed_plugin, plugin_capability_allowed)

        return True

    def _inject_allowed(self, plugin, allowed_plugin, capability):
        if plugin and allowed_plugin and not allowed_plugin in plugin.allowed_loaded:
            plugin.load_allowed(allowed_plugin, capability)
            self.add_plugin_allowed_plugins_map(allowed_plugin.id, [plugin, capability])

    def inject_all_allowed(self, plugin):
        """
        Injects the plugin in all the plugins that allow one of it's capabilities

        @type plugin: Plugin
        @param plugin: The plugin to inject in the plugins that allow one of it's capabilities
        """

        # gets all the capabilities of the plugin
        plugin_capabilities = plugin.capabilities

        # iterates over all of the plugin capabilities
        for plugin_capability in plugin_capabilities:
            capability_plugins = self.get_capabilities_plugins_map(plugin_capability)

            for capability_plugin in capability_plugins:
                if capability_plugin.is_loaded():
                    self._inject_allowed(capability_plugin, plugin, plugin_capability)

    def add_plugin_dependent_plugins_map(self, plugin_id, dependency_plugin_instance):
        if not plugin_id in self.plugin_dependent_plugins_map:
            self.plugin_dependent_plugins_map[plugin_id] = []
        self.plugin_dependent_plugins_map[plugin_id].append(dependency_plugin_instance)

    def get_plugin_dependent_plugins_map(self, plugin_id):
        if plugin_id in self.plugin_dependent_plugins_map:
            return self.plugin_dependent_plugins_map[plugin_id]
        else:
            return []

    def clear_plugin_dependent_plugins_map(self, plugin_id):
        self.plugin_dependent_plugins_map[plugin_id] = []

    def add_plugin_allowed_plugins_map(self, plugin_id, allowed_plugin_info_list):
        if not plugin_id in self.plugin_allowed_plugins_map:
            self.plugin_allowed_plugins_map[plugin_id] = []
        self.plugin_allowed_plugins_map[plugin_id].append(allowed_plugin_info_list)

    def get_plugin_allowed_plugins_map(self, plugin_id):
        if plugin_id in self.plugin_allowed_plugins_map:
            return self.plugin_allowed_plugins_map[plugin_id]
        else:
            return []

    def clear_plugin_allowed_plugins_map(self, plugin_id):
        self.plugin_allowed_plugins_map[plugin_id] = []
        plugin = self._get_plugin_by_id(plugin_id)

        # removes the element plugin from the other allowed plugin lists
        for plugin_allowed_plugins_map_key in self.plugin_allowed_plugins_map:
            allowed_plugins_list = self.plugin_allowed_plugins_map[plugin_allowed_plugins_map_key]
            for allowed_plugins_list_element in allowed_plugins_list:
                if allowed_plugins_list_element[0] == plugin:
                    allowed_plugins_list.remove(allowed_plugins_list_element)
                    break

    def add_capabilities_plugins_map(self, capability, plugin):
        if not capability in self.capabilities_plugins_map:
            self.capabilities_plugins_map[capability] = []
        self.capabilities_plugins_map[capability].append(plugin)

    def get_capabilities_plugins_map(self, capability):
        if capability in self.capabilities_plugins_map:
            return self.capabilities_plugins_map[capability]
        else:
            return []

    def clear_capabilities_plugins_map(self, capability):
        self.capabilities_plugins_map[capability] = []

    def clear_capabilities_plugins_map_for_plugin(self, plugin_id):
        plugin = self._get_plugin_by_id(plugin_id)

        for plugin_capability_allowed in plugin.capabilities_allowed:
            if plugin_capability_allowed in self.capabilities_plugins_map:
                capability_plugins = self.capabilities_plugins_map[plugin_capability_allowed]
                if plugin in capability_plugins:
                    capability_plugins.remove(plugin)

    def load_plugin(self, plugin_id, type = None):
        # retrieves the plugin
        plugin = self._get_plugin_by_id(plugin_id)

        # in case the plugin is loaded
        if plugin.is_loaded():
            return True

        # in case the plugin is lazy loaded
        if (plugin.loading_type == LAZY_LOADING_TYPE and not type == FULL_LOAD_TYPE) and plugin.is_lazy_loaded():
            return True

        # test the plugin
        if not self.test_plugin_load(plugin):
            self.logger.info("Plugin '%s' v%s not ready to be loaded" % (plugin.short_name, plugin.version))
            return False

        if MAIN_TYPE in plugin.capabilities:
            if not self._load_plugin(plugin, type, MAIN_TYPE):
                return False
        elif THREAD_TYPE in plugin.capabilities:
            if not self._load_plugin(plugin, type, THREAD_TYPE):
                return False
        else:
            if not self._load_plugin(plugin, type):
                return False

        self.inject_all_allowed(plugin)

        return True

    def unload_plugin(self, plugin_id, type = None):
        plugin = self._get_plugin_by_id(plugin_id)

        # in case the plugin is not loaded
        if not plugin.is_loaded():
            return

        if MAIN_TYPE in plugin.capabilities:
            if not self._unload_plugin(plugin, type, MAIN_TYPE):
                return False
        elif THREAD_TYPE in plugin.capabilities:
            if not self._unload_plugin(plugin, type, THREAD_TYPE):
                return False
        else:
            if not self._unload_plugin(plugin, type):
                return False

        return True;

    def get_all_plugins(self):
        """
        Retrieves all the started plugin instances

        @rtype: List
        @return: The list with all the started plugin instances
        """

        return self.plugin_instances

    def get_all_loaded_plugins(self):
        """
        Retrieves all the loaded plugin instances

        @rtype: List
        @return: The list with all the loaded plugin instances
        """

        loaded_plugins_instances = []

        for plugin_instance in self.plugin_instances:
            if plugin_instance.is_loaded():
                loaded_plugins_instances.append(plugin_instance)

        return loaded_plugins_instances

    def get_plugin(self, plugin):
        """
        Retrieves a plugin and loads it if necessary

        @type plugin: Plugin
        @param plugin: The plugin to retrieve
        @rtype: Plugin
        @return: The retrieved plugin
        """

        if not plugin.is_loaded():
            self._load_plugin(plugin)
        return plugin

    def get_plugin_by_id(self, plugin_id):
        """
        Retrieves an instance of a plugin with the given id

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve
        @rtype: Plugin
        @return: The plugin with the given id
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            return self.get_plugin(plugin)

    def _get_plugin_by_id(self, plugin_id):
        """
        Retrieves an instance (not verified to be loaded) of a plugin with the given id

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve
        @rtype: Plugin
        @return: The plugin with the given id
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            return plugin

    def get_plugin_by_id_and_version(self, plugin_id, plugin_version):
        """
        Retrieves an instance of a plugin with the given id and version

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve
        @type plugin_version: String
        @param plugin_version: The version of the plugin to retrieve
        @rtype: Plugin
        @return: The plugin with the given id and version
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            if plugin.version == plugin_version:
                return self.get_plugin(plugin)

    def _get_plugin_by_id_and_version(self, plugin_id, plugin_version):
        """
        Retrieves an instance (not verified to be loaded) of a plugin with the given id and version

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve
        @type plugin_version: String
        @param plugin_version: The version of the plugin to retrieve
        @rtype: Plugin
        @return: The plugin with the given id and version
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            if plugin.version == plugin_version:
                return plugin

    def get_plugins_by_capability(self, capability):
        """
        Retrieves all the plugins with the given capability and sub capabilities

        @type capability: String
        @param capability: The capability of the plugins to retrieve
        @rtype: List
        @return: The list of plugins for the given capability and sub capabilities
        """

        # the results list
        result = []

        # the capability converter to internal capability structure
        capability_structure = Capability(capability)

        for plugin in self.plugin_instances:
            plugin_capabilities_structure = convert_to_capability_list(plugin.capabilities)

            for plugin_capability_structure in plugin_capabilities_structure:
                if capability_structure.is_capability_or_sub_capability(plugin_capability_structure):
                    result.append(self.get_plugin(plugin))

        return result

    def _get_plugins_by_capability_cache(self, capability):
        """
        Retrieves all the plugins (not verified to be loaded) with the given capability and sub capabilities (using cache system)

        @type capability: String
        @param capability: The capability of the plugins to retrieve
        @rtype: List
        @return: The list of plugins for the given capability and sub capabilities
        """

        # the results list
        result = []

        if not capability in self.capabilities_sub_capabilities_map:
            return result

        capability_and_sub_capabilities_list = [capability] + self.capabilities_sub_capabilities_map[capability]

        for capability_or_sub_capability in capability_and_sub_capabilities_list:
            plugin_instances = self.capabilities_plugin_instances_map[capability_or_sub_capability]
            result += plugin_instances

        return result

    def _get_plugins_by_capability(self, capability):
        """
        Retrieves all the plugins (not verified to be loaded) with the given capability and sub capabilities

        @type capability: String
        @param capability: The capability of the plugins to retrieve
        @rtype: List
        @return: The list of plugins for the given capability and sub capabilities
        """

        # the results list
        result = []

        # the capability converter to internal capbility structure
        capability_structure = Capability(capability)

        for plugin in self.plugin_instances:
            plugin_capabilities_structure = convert_to_capability_list(plugin.capabilities)

            for plugin_capability_structure in plugin_capabilities_structure:
                if capability_structure.is_capability_or_sub_capability(plugin_capability_structure):
                    result.append(plugin)

        return result

    def __get_plugins_by_capability(self, capability):
        """
        Retrieves all the plugins with the given capability

        @type capability: String
        @param capability: The capability of the plugins to retrieve
        @rtype: List
        @return: The list of plugins for the given capability
        """

        # the results list
        result = []
        for plugin in self.plugin_instances:
            if capability in plugin.capabilities:
                result.append(self.get_plugin(plugin))
        return result

    def get_plugins_by_capability_allowed(self, capability_allowed):
        """
        Retrieves all the plugins with the given allowed capability and sub capabilities

        @type capability_allowed: String
        @param capability_allowed: The capability allowed of the plugins to retrieve
        @rtype: List
        @return: The list of plugins for the given capability allowed
        """

        # the results list
        result = []

        # the capability converter to internal capability structure
        capability_structure = Capability(capability_allowed)

        for plugin in self.plugin_instances:
            plugin_capabilities_structure = convert_to_capability_list(plugin.capabilities_allowed)

            for plugin_capability_structure in plugin_capabilities_structure:
                if capability_structure.is_capability_or_sub_capability(plugin_capability_structure):
                    result.append(self.get_plugin(plugin))

        return result

    def _get_plugins_by_capability_allowed(self, capability_allowed):
        """
        Retrieves all the plugins (not verified to be loaded) with the given allowed capability and sub capabilities

        @type capability_allowed: String
        @param capability_allowed: The capability allowed of the plugins to retrieve
        @rtype: List
        @return: The list of plugins for the given capability allowed
        """

        # the results list
        result = []

        # the capability converter to internal capability structure
        capability_structure = Capability(capability_allowed)

        for plugin in self.plugin_instances:
            plugin_capabilities_structure = convert_to_capability_list(plugin.capabilities_allowed)

            for plugin_capability_structure in plugin_capabilities_structure:
                if capability_structure.is_capability_or_sub_capability(plugin_capability_structure):
                    result.append(plugin)

        return result

    def get_plugins_by_event_handled(self, event_handled):
        # the results list
        result = []

        for plugin in self.plugin_instances:
            if event_handled in plugin.events_handled:
                result.append(self.get_plugin(plugin))

        return result

    def _get_plugins_by_event_handled(self, event_handled):
        # the results list
        result = []

        for plugin in self.plugin_instances:
            if event_handled in plugin.events_handled:
                result.append(plugin)

        return result

    def get_plugins_by_event_registrable(self, event_registrable):
        # the results list
        result = []

        for plugin in self.plugin_instances:
            if event_registrable in plugin.events_registrable:
                result.append(self.get_plugin(plugin))

        return result

    def _get_plugins_by_event_registrable(self, event_registrable):
        # the results list
        result = []

        for plugin in self.plugin_instances:
            if event_registrable in plugin.events_registrable:
                result.append(plugin)

        return result

    def get_plugins_by_dependency(self, plugin_id):
        """
        Retrieves all the plugins with a dependency with the given plugin id

        @type plugin_id: String
        @param plugin_id: The id of the plugin dependency
        @rtype: List
        @return: The list of plugins with a dependency with the given plugin id
        """

        # the results list
        result = []

        for plugin in self.plugin_instances:
            for dependency in plugin.dependencies:
               if dependency.__class__.__name__ == "PluginDependency":
                    if dependency.plugin_id == plugin_id:
                        result.append(self.get_plugin(plugin))
        return result

    def _get_plugins_by_dependency(self, plugin_id):
        # the results list
        result = []

        for plugin in self.plugin_instances:
            for dependency in plugin.dependencies:
               if dependency.__class__.__name__ == "PluginDependency":
                    if dependency.plugin_id == plugin_id:
                        result.append(plugin)
        return result

    def get_plugins_allow_capability(self, capability):
        """
        Retrieves all the plugins that allow the given capability

        @type capability: String
        @param capability: The capability to be tested
        @rtype: List
        @return: The list of plugins that allow the given capability
        """

        # the results list
        result = []

        # the capability converter to internal capability structure
        capability_structure = Capability(capability)

        for plugin in self.plugin_instances:
            plugin_capabilities_structure = convert_to_capability_list(plugin.capabilities_allowed)

            for plugin_capability_structure in plugin_capabilities_structure:
                if plugin_capability_structure.is_capability_or_sub_capability(capability_structure):
                    result.append(self.get_plugin(plugin))

        return result

    def _get_plugins_allow_capability(self, capability):
        """
        Retrieves all the plugins (not verified to be loaded) that allow the given capability

        @type capability: String
        @param capability: The capability to be tested
        @rtype: List
        @return: The list of plugins that allow the given capability
        """

        # the results list
        result = []

        # the capability converter to internal capability structure
        capability_structure = Capability(capability)

        for plugin in self.plugin_instances:
            plugin_capabilities_structure = convert_to_capability_list(plugin.capabilities_allowed)

            for plugin_capability_structure in plugin_capabilities_structure:
                if plugin_capability_structure.is_capability_or_sub_capability(capability_structure):
                    result.append(plugin)

        return result

    def get_plugin_path_by_id(self, plugin_id):
        """
        Retrieves the plugin execution path for the given plugin id

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the execution path
        @rtype: String
        @return: The plugin execution path for the plugin with the given id
        """

        if plugin_id in self.plugin_dirs_map:
            return self.plugin_dirs_map[plugin_id]

    def get_plugin_module_name_by_id(self, plugin_id):
        """
        Retrieves the plugin module name for the given plugin id

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the plugin module name
        @rtype: String
        @return: The plugin module name for the given plugin id
        """

        plugin = self._get_plugin_by_id(plugin_id)

        if plugin:
            return plugin.__module__

    def get_plugin_by_module_name(self, module):
        """
        Retrieves an instance of a plugin for the given plugin module name

        @type module: String
        @param module: The plugin module name to retrieve
        @rtype: Plugin
        @return: The plugin for the given plugin module name
        """

        plugins = self.get_all_plugins()

        for plugin in plugins:
            plugin_module = plugin.__module__

            if plugin_module == module:
                return plugin

    def get_loaded_plugin_by_module_name(self, module):
        """
        Retrieves an instance of a loaded plugin for the given plugin module name

        @type module: String
        @param module: The loaded plugin module name to retrieve
        @rtype: Plugin
        @return: The loaded plugin for the given plugin module name
        """

        loaded_plugins = self.get_all_loaded_plugins()

        for loaded_plugin in loaded_plugins:
            plugin_module = plugin.__module__

            if plugin_module == module:
                return loaded_plugin

    def get_plugin_class_by_module_name(self, module):
        """
        Retrieves a the plugin class for the given plugin module name

        @type module: String
        @param module: The plugin module name to retrieve
        @rtype: Class
        @return: The plugin class for the given plugin module name
        """

        for plugin in self.loaded_plugins:
            plugin_module = plugin.__module__

            if plugin_module == module:
                return plugin

    def register_plugin_manager_event(self, plugin, event_name):
        """
        Registers a given plugin manager event in the given plugin

        @type plugin: Plugin
        @param plugin: The plugin containing the handler to the event
        @type event_name: String
        @param event_name: The name of the event to be registered
        """

        if not event_name in self.event_plugins_handled_loaded_map:
            self.event_plugins_handled_loaded_map[event_name] = []

        if not plugin in self.event_plugins_handled_loaded_map[event_name]:
            self.event_plugins_handled_loaded_map[event_name].append(plugin)
            self.logger.info("Registering event '%s' from '%s' v%s in plugin manager" % (event_name, plugin.short_name, plugin.version))

    def unregister_plugin_manager_event(self, plugin, event_name):
        """
        Unregisters a given plugin manager event in the given plugin

        @type plugin: Plugin
        @param plugin: The plugin containing the handler to the event
        @type event_name: String
        @param event_name: The name of the event to be unregistered
        """

        if event_name in self.event_plugins_handled_loaded_map:
            if plugin in self.event_plugins_handled_loaded_map[event_name]:
                self.event_plugins_handled_loaded_map[event_name].remove(plugin)
                self.logger.info("Unregistering event '%s' from '%s' v%s in plugin manager" % (event_name, plugin.short_name, plugin.version))

    def notify_handlers(self, event_name, event_args):
        """
        Notifies all the handlers for the event with the given name with the give arguments

        @type event_name: String
        @param event_name: The name of the event to be notified
        @type event_args: List
        @param event_args: The arguments to be passed to the handler
        """

        # the names of the events handled by self
        event_names_list = self.event_plugins_handled_loaded_map.keys()

        # retrieves all the events and super events that match the generated event
        events_or_super_events_list = get_all_events_or_super_events_in_list(event_name, event_names_list)

        # iterates over all the events and super events for notification
        for event_or_super_event in events_or_super_events_list:
            if event_or_super_event in self.event_plugins_handled_loaded_map:
                # iterates over all the plugins registered for notification
                for event_plugin_loaded in self.event_plugins_handled_loaded_map[event_or_super_event]:
                    self.logger.info("Notifying '%s' v%s about event '%s' generated in plugin manager" % (event_plugin_loaded.short_name, event_plugin_loaded.version, event_name))

                    event_plugin_loaded.event_handler(event_name, *event_args)

    def generate_event(self, event_name, event_args):
        """
        Generates an event and starts the process of handler notification

        @type event_name: String
        @param event_name: The name of the event to be notified
        @type event_args: List
        @param event_args: The arguments to be passed to the handler
        """

        self.logger.info("Event '%s' generated in plugin manager" % (event_name))

        self.notify_handlers(event_name, event_args)

    def plugin_manager_plugin_execute(self, execution_type, arguments):
        """
        Executes a plugin manager call in all the plugin manager plugins with
        the defined execution type capability

        @type execution_type: String
        @param execution_type: The type of execution
        @type arguments: List
        @param arguments: The list of arguments for the execution
        @rtype: bool
        @return: The boolean result of the AND operation between the call results
        """

        # in case the plugin manager plugins are already loaded
        if self.plugin_manager_plugins_loaded:

            # retrieves the init_plugin_load_plugins_list
            execute_plugins_list = self._get_plugins_by_capability_cache(PLUGIN_MANAGER_EXTENSION_TYPE + "." + execution_type)

            # iterates over all the init plugin load plugins
            for execute_plugin in execute_plugins_list:

                # retrieves the method
                execute_call = getattr(execute_plugin, execution_type)

                # calls the method and retrives the return value
                return_value = execute_call(*arguments)

                # calls the method
                if not return_value:
                    return False

        return True

    def plugin_manager_plugin_execute_conditional(self, execution_type, arguments):
        """
        Executes a plugin manager call in all the plugin manager plugins with
        the defined execution type capability (the execution is conditional)

        @type execution_type: String
        @param execution_type: The type of execution
        @type arguments: List
        @param arguments: The list of arguments for the execution
        @rtype: bool
        @return: The boolean result of the AND operation between the call results
        """

        # in case the plugin manager plugins are already loaded
        if self.plugin_manager_plugins_loaded:

            # retrieves the init_plugin_load_plugins_list
            execute_plugins_list = self._get_plugins_by_capability_cache(PLUGIN_MANAGER_EXTENSION_TYPE + "." + execution_type)

            # iterates over all the init plugin load plugins
            for execute_plugin in execute_plugins_list:

                # retrieves the validation method
                validation_execute_call = getattr(execute_plugin, PLUGIN_MANAGER_PLUGIN_VALIDATION_PREFIX + execution_type)

                # runs the validation test
                if validation_execute_call(*arguments):
                    # retrieves the method
                    execute_call = getattr(execute_plugin, execution_type)

                    # calls the method and retrives the return value
                    return_value = execute_call(*arguments)

                    # calls the method
                    if not return_value:
                        return False

        return True

    def exists_plugin_manager_plugin_execute_conditional(self, execution_type, arguments):
        """
        Tests all the available plugin manager plugins of the type execution_type
        in the search of one that is available for execution

        @type execution_type: String
        @param execution_type: The type of execution
        @type arguments: List
        @param arguments: The list of arguments for the execution
        @rtype: bool
        @return: The result of the test (if successful or not)
        """

        # in case the plugin manager plugins are already loaded
        if self.plugin_manager_plugins_loaded:

            # retrieves the init_plugin_load_plugins_list
            execute_plugins_list = self._get_plugins_by_capability_cache(PLUGIN_MANAGER_EXTENSION_TYPE + "." + execution_type)

            # iterates over all the init plugin load plugins
            for execute_plugin in execute_plugins_list:

                # retrieves the validation method
                validation_execute_call = getattr(execute_plugin, PLUGIN_MANAGER_PLUGIN_VALIDATION_PREFIX + execution_type)

                # runs the validation test
                if validation_execute_call(*arguments):
                    return True

        return False

    def print_all_plugins(self):
        """
        Prints all the loaded plugins descriptions
        """

        for plugin in self.plugin_instances:
            print plugin

    def set_plugin_manager_plugins_loaded(self, value = True):
        """
        Sets the value for the plugin_manager_plugins_loaded flag

        @type value: bool
        @param value: The value to set for the plugin_manager_plugins_loaded flag
        """

        self.plugin_manager_plugins_loaded = value

    def get_plugin_manager_plugins_loaded(self):
        """
        Retrieves the current plugin_manager_plugins_loaded flag value

        @rtype: bool
        @return: The current plugin_manager_plugins_loaded flag value
        """

        return self.plugin_manager_plugins_loaded

    def set_init_complete(self, value = True):
        """
        Sets the value for the init_complete flag

        @type value: bool
        @param value: The value to set for the init_complete flag
        """

        self.init_complete = value

    def get_init_complete(self):
        """
        Retrieves the current init_complete flag value

        @rtype: bool
        @return: The current init_complete flag value
        """

        return self.init_complete

    def echo(self, value = "echo"):
        """
        Returns an echo value.

        @type value: String
        @param value: The value to be echoed.
        @rtype: String
        @return: The echo value.
        """

        return value

class Dependency:
    """
    The dependency class.
    """

    mandatory = True
    """ The mandatory value """

    conditions_list = True
    """ The list of conditions """

    def __init__(self, mandatory = True, conditions_list = []):
        """
        Constructor of the class.

        @type mandatory: bool
        @param mandatory: The mandatory value.
        @type conditions_list: List
        @param conditions_list: The list of conditions.
        """

        self.mandatory = mandatory
        self.conditions_list = conditions_list

    def test_dependency(self, manager):
        """
        Tests the environment for the plugin manager.

        @type manager: PluginManager
        @param manager: The current plugin manager in use.
        @rtype: bool
        @return: The result of the test (if successful or not).
        """

        return True

    def test_conditions(self):
        """
        Tests the available conditions.

        @rtype: bool
        @return: The result of the test (if successful or not).
        """

        # iterates over all the conditions
        for condition in self.conditions_list:
            if not condition.test_condition():
                return False

        return True

    def get_tuple(self):
        """
        Retrieves a tuple representing the dependency.

        @rtype: Tuple
        @return: A tuple representing the dependency.
        """

        return ()

class PluginDependency(Dependency):
    """
    The plugin dependency class.
    """

    plugin_id = "none"
    """ The plugin id """

    plugin_version = "none"
    """ The plugin version """

    def __init__(self, plugin_id = "none", plugin_version = "none", mandatory = True, conditions_list = []):
        """
        Constructor of the class.

        @type plugin_id: String
        @param plugin_id: The plugin id.
        @type plugin_version: String
        @param plugin_version: The plugin version.
        @type mandatory: bool
        @param mandatory: The mandatory value.
        @type conditions_list: List
        @param conditions_list: The list of conditions.
        """

        Dependency.__init__(self, mandatory, conditions_list)
        self.plugin_id = plugin_id
        self.plugin_version = plugin_version

    def __repr__(self):
        """
        Returns the default representation of the class.

        @rtype: String
        @return: The default representation of the class.
        """

        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.plugin_id,
            self.plugin_version,
        )

    def test_dependency(self, manager):
        """
        Tests the environment for the plugin dependency and the given plugin manager.

        @type manager: PluginManager
        @param manager: The current plugin manager in use.
        @rtype: bool
        @return: The result of the test (if successful or not).
        """

        Dependency.test_dependency(self, manager)

        # in case some of the conditions are not fulfilled plugin
        if not self.test_conditions():
            return True

        # retrieves the plugin id for the plugin dependency
        plugin_id = self.plugin_id

        # retrieves the plugin version for the plugin dependency
        plugin_version = self.plugin_version

        if not plugin_id in manager.loaded_plugins_map:
            return False

        plugin = manager.loaded_plugins_map[plugin_id]

        if not plugin.version == plugin_version:
            return False

        # in case the plugin load test is not successful
        if not manager.test_plugin_load(plugin):
            return False;

        return True

    def get_tuple(self):
        """
        Retrieves a tuple representing the plugin dependency.

        @rtype: Tuple
        @return: A tuple representing the plugin dependency.
        """

        return (self.plugin_id, self.plugin_version)

class PackageDependency(Dependency):
    """
    The package dependency class.
    """

    package_name = "none"
    """ The package name """

    package_import_name = "none"
    """ The package import name """

    package_version = "none"
    """ The package version """

    package_url = "none"
    """ The package url """

    def __init__(self, package_name = "none", package_import_name = "none", package_version = "none", package_url = "none", mandatory = True, conditions_list = []):
        """
        Constructor of the class.

        @type package_name: String
        @param package_name: The package name.
        @type package_import_name: String
        @param package_import_name: The package import name.
        @type package_version: String
        @param package_version: The package version.
        @type package_url: String
        @param package_url: The package url.
        @type mandatory: bool
        @param mandatory: The mandatory value.
        @type conditions_list: List
        @param conditions_list: The list of conditions.
        """

        Dependency.__init__(self, mandatory, conditions_list)
        self.package_name = package_name
        self.package_import_name= package_import_name
        self.package_version = package_version
        self.package_url = package_url

    def __repr__(self):
        """
        Returns the default representation of the class

        @rtype: String
        @return: The default representation of the class
        """

        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.package_name,
            self.package_version
        )

    def test_dependency(self, manager):
        """
        Tests the environment for the package dependency and the given plugin manager

        @type manager: PluginManager
        @param manager: The current plugin manager in use
        @rtype: bool
        @return: The result of the test (if successful or not)
        """

        Dependency.test_dependency(self, manager)

        # in case some of the conditions are not fulfilled plugin
        if not self.test_conditions():
            return True

        # retrieves the package name for the package dependency
        package_name = self.package_name

        # retrieves the package import name for the package dependency
        package_import_name = self.package_import_name

        # retrieves the package version for the package dependency
        package_version = self.package_version

        # retrieves the package url for the package dependency
        package_url = self.package_url

        # retrieves the package import name type
        package_import_name_type = type(package_import_name)

        if package_import_name_type == types.StringType:
            try:
                # tries to find (import) the given module
                __import__(package_import_name)
            except ImportError, import_error:
                manager.logger.info("Package '%s' v%s does not exist in your system" % (package_name, package_version))
                if not package_url == "none":
                    manager.logger.info("You can download the package at %s" % package_url)

                return False
        elif package_import_name_type == types.ListType:
            for package_import_name_item in package_import_name:
                try:
                    # tries to find (import) the given module
                    __import__(package_import_name_item)
                except ImportError, import_error:
                    manager.logger.info("Package '%s' v%s does not exist in your system" % (package_name, package_version))
                    if not package_url == "none":
                        manager.logger.info("You can download the package at %s" % package_url)

                    return False

        return True

    def get_tuple(self):
        """
        Retrieves a tuple representing the package dependency.

        @rtype: Tuple
        @return: A tuple representing the package dependency.
        """

        return (self.package_name, self.package_version)

class Condition:
    """
    The condition class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def test_condition(self):
        """
        Test the condition returning the result of the test.

        @rtype: bool
        @return: The result of the test (if successfull or not).
        """

        return True

class OperativeSystemCondition(Condition):
    """
    The operative system condition class.
    """

    operative_system_name = "none"
    """ The operative system name """

    def __init__(self, operative_system_name = "none"):
        """
        Constructor of the class.

        @type operative_system_name: String
        @param operative_system_name: The operative system name.
        """

        self.operative_system_name = operative_system_name

    def test_condition(self):
        """
        Test the condition returning the result of the test.

        @rtype: bool
        @return: The result of the test (if successfull or not).
        """

        if not Condition.test_condition(self):
            return False

        # retrieves the current operative system name
        current_operative_system_name = colony.plugins.util.get_operative_system()

        # in case the current operative system is the same as the defined in the condition
        if current_operative_system_name == self.operative_system_name:
            return True
        else:
            return False

class Capability:
    """
    Class that describes a neutral structure for a capability
    """

    list_value = []
    """ The value of the capability described as a list """

    def __init__(self, string_value = None):
        if string_value:
            self.list_value = string_value.split(".")
        else:
            self.list_value = []

    def __eq__(a, b):
        list_value_a = a.list_value
        list_value_b = b.list_value

        if not list_value_a or not list_value_b:
            return False

        len_a = len(list_value_a)
        len_b = len(list_value_b)

        if not len_a == len_b:
            return False

        for index in range(len_a):
            if list_value_a[index] != list_value_b[index]:
                return False

        return True

    def __ne__(a, b):
        return not self.__eq__(a, b)

    def eq(a, b):
        return self.__eq__(a, b)

    def ne(a, b):
        return self.__neq__(a, b)

    def capability_and_super_capabilites(self):
        """
        Retrieves the list of the capability and all super capabilities

        @rtype: List
        @return: The of the capability and all super capabilities
        """

        capability_and_super_capabilites_list = []

        # retrieves the list value
        list_value_self = self.list_value

        curent_capability_value = None

        for value_self in list_value_self:
            if curent_capability_value:
                curent_capability_value = curent_capability_value + "." + value_self
            else:
                curent_capability_value = value_self
            capability_and_super_capabilites_list.append(curent_capability_value)

        return capability_and_super_capabilites_list

    def is_sub_capability(self, capability):

        list_value_self = self.list_value
        list_value_capability = capability.list_value

        if not list_value_self or not list_value_capability:
            return False

        len_self = len(list_value_self)
        len_capability = len(list_value_capability)

        if len_capability <= len_self:
            return False

        for index in range(len_self):
            if list_value_self[index] != list_value_capability[index]:
                return False

        return True

    def is_capability_or_sub_capability(self, capability):
        if self.__eq__(capability) or self.is_sub_capability(capability):
            return True
        else:
            return False

class Event:
    """
    Class that describes a neutral structure for an event
    """

    list_value = []
    """ The value of the event described as a list """

    def __init__(self, string_value = None):
        if string_value:
            self.list_value = string_value.split(".")
        else:
            self.list_value = []

    def __eq__(a, b):
        list_value_a = a.list_value
        list_value_b = b.list_value

        if not list_value_a or not list_value_b:
            return False

        len_a = len(list_value_a)
        len_b = len(list_value_b)

        if not len_a == len_b:
            return False

        for index in range(len_a):
            if list_value_a[index] != list_value_b[index]:
                return False

        return True

    def __ne__(a, b):
        return not self.__eq__(a, b)

    def eq(a, b):
        return self.__eq__(a, b)

    def ne(a, b):
        return self.__neq__(a, b)

    def is_sub_event(self, event):

        list_value_self = self.list_value
        list_value_event = event.list_value

        if not list_value_self or not list_value_event:
            return False

        len_self = len(list_value_self)
        len_event = len(list_value_event)

        if len_event <= len_self:
            return False

        for index in range(len_self):
            if list_value_self[index] != list_value_event[index]:
                return False

        return True

    def is_event_or_sub_event(self, event):
        if self.__eq__(event) or self.is_sub_event(event):
            return True
        else:
            return False

def capability_and_super_capabilites(capability):
    """
    Retrieves the list of the capability and all super capabilities

    @rtype: List
    @return: The of the capability and all super capabilities
    """

    capability_structure = Capability(capability)

    return capability_structure.capability_and_super_capabilites()

def is_capability_or_sub_capability(base_capability, capability):

    base_capability_structure = Capability(base_capability)
    capability_structure = Capability(capability)

    return base_capability_structure.is_capability_or_sub_capability(capability_structure)

def is_capability_or_sub_capability_in_list(base_capability, capability_list):

    for capability in capability_list:
        if is_capability_or_sub_capability(base_capability, capability):
            return True

    return False

def convert_to_capability_list(capability_list):

    capability_list_structure = []

    for capability in capability_list:
        capability_structure = Capability(capability)
        capability_list_structure.append(capability_structure)

    return capability_list_structure

def is_event_or_sub_event(base_event, event):

    base_event_structure = Event(base_event)
    event_structure = Event(event)

    return base_event_structure.is_event_or_sub_event(event_structure)

def is_event_or_super_event(base_event, event):
    return is_event_or_sub_event(event, base_event)

def is_event_or_sub_event_in_list(base_event, event_list):

    for event in event_list:
        if is_event_or_sub_event(base_event, event):
            return True

    return False

def is_event_or_super_event_in_list(base_event, event_list):

    for event in event_list:
        if is_event_or_super_event(base_event, event):
            return True

    return False

def get_all_events_or_super_events_in_list(base_event, event_list):
    events_or_super_events_list = []

    for event in event_list:
        if is_event_or_super_event(base_event, event):
            events_or_super_events_list.append(event)

    return events_or_super_events_list

def convert_to_event_list(event_list):

    event_list_structure = []

    for event in event_list:
        event_structure = Event(event)
        event_list_structure.append(event_structure)

    return event_list_structure

class PluginThread(threading.Thread):

    plugin = None
    load_complete = False
    end_load_complete = False

    load_plugin_thread = None
    """ The thread that controls the load plugin method call """

    end_load_plugin_thread = None
    """ The thread that controls the end load plugin method call """

    event_queue = []
    """ The queue of events to be processed """

    semaphore = None

    def __init__ (self, plugin):
        threading.Thread.__init__(self)
        self.plugin = plugin
        self.semaphore = threading.Semaphore()

        self.event_queue = []
        self.load_complete = False

    def set_load_complete(self, value):
        self.load_complete = value

    def set_end_load_complete(self, value):
        self.end_load_complete = value

    def add_event(self, event):
        self.event_queue.append(event)
        self.semaphore.release()

    def flush_queue(self):
        if len(self.event_queue):
            event = self.event_queue.pop(0)
            if event.event_name == "exit":
                if self.load_plugin_thread.isAlive():
                    self.load_plugin_thread.join()
                if self.end_load_plugin_thread.isAlive():
                    self.end_load_plugin_thread.join()
                return True
            elif event.event_name == "load":
                self.load_plugin_thread = PluginEventThread(self.plugin.load_plugin)
                self.load_plugin_thread.start()
                self.load_complete = True
            elif event.event_name == "lazy_load":
                self.lazy_load_plugin_thread = PluginEventThread(self.plugin.lazy_load_plugin)
                self.lazy_load_plugin_thread.start()
                self.load_complete = True
            elif event.event_name == "end_load":
                self.end_load_plugin_thread = PluginEventThread(self.plugin.end_load_plugin)
                self.end_load_plugin_thread.start()
                self.end_load_complete = True
            elif event.event_name == "unload":
                pass

    def run(self):
        while True:
            self.semaphore.acquire()
            if self.flush_queue():
                return

class PluginEventThread(threading.Thread):
    """
    The plugin event thread class.
    """

    method = None;
    """ The method for the event thread """

    def __init__ (self, method):
        """
        Constructor of the class

        @type method: BusinessDummyBusinessLogicPlugin
        @param method: The method for the event thread.
        """

        threading.Thread.__init__(self)
        self.method = method

    def run(self):
        """
        The method to start running the thread.
        """

        # calls the event thread method
        self.method()
