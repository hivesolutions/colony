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

__revision__ = "$LastChangedRevision: 9958 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-09-01 10:45:10 +0100 (qua, 01 Set 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import re
import sys
import stat
import time
import types
import thread
import signal
import inspect
import tempfile
import threading
import traceback

import __builtin__

import logging.handlers

import colony.libs.path_util
import colony.libs.string_buffer_util

import colony.base.dummy_input

import colony.base.util
import colony.base.decorators

import colony.base.plugin_system_exceptions
import colony.base.plugin_system_information
import colony.base.plugin_system_configuration

plugin_manager_configuration = colony.base.plugin_system_configuration.plugin_manager_configuration
""" The plugin manager configuration """

CPYTHON_ENVIRONMENT = colony.base.util.CPYTHON_ENVIRONMENT
""" CPython environment value """

JYTHON_ENVIRONMENT = colony.base.util.JYTHON_ENVIRONMENT
""" Jython environment value """

IRON_PYTHON_ENVIRONMENT = colony.base.util.IRON_PYTHON_ENVIRONMENT
""" IronPython environment value """

DEFAULT_LOGGER = "default_messages"
""" The default logger name """

DEFAULT_LOGGING_LEVEL = logging.INFO
""" The default logging level """

DEFAULT_LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
""" The default logging format """

DEFAULT_LOGGING_FILE_NAME_PREFIX = "colony"
""" The default logging file name prefix """

DEFAULT_LOGGING_FILE_NAME_SEPARATOR = "_"
""" The default logging file name separator """

DEFAULT_LOGGING_FILE_NAME_EXTENSION = ".log"
""" The default logging file name extension """

DEFAULT_LOGGING_FILE_MODE = "a"
""" The default logging file mode """

DEFAULT_LOGGING_FILE_SIZE = 10485760
""" The deefault logging file size """

DEFAULT_LOGGING_FILE_BACKUP_COUNT = 5
""" The default logging file backup count """

DEFAULT_TEMPORARY_PATH = u"tmp"
""" The default temporary path """

DEFAULT_PLUGIN_PATH = u"plugins"
""" The default plugin path """

DEFAULT_CONFIGURATION_PATH = u"meta"
""" The default configuration path """

DEFAULT_WORKSPACE_PATH = u"~/.colony_workspace"
""" The default workspace path """

DEFAULT_EXECUTION_HANDLING_METHOD = "handle_execution"
""" The default execution handling method """

DEFAULT_LOOP_WAIT_TIMEOUT = 1.0
""" The default loop wait timeout """

DEFAULT_UNLOAD_SYSTEM_TIMEOUT = 600.0
""" The default unload system timeout """

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

SINGLETON_DIFFUSION_SCOPE = 1
""" The singleton diffusion scope """

SAME_DIFFUSION_SCOPE = 2
""" The same diffusion scope """

NEW_DIFFUSION_SCOPE = 3
""" The new diffusion scope """

FILE_REMOVED_TYPE = "file_removed"
""" The file removed plugin loading/unloading type """

PLUGIN_MANAGER_TYPE = "plugin_manager"
""" The plugin manager type """

PLUGIN_MANAGER_PLUGIN_VALIDATION_PREFIX = "is_valid_"
""" The prefix for the plugin manager plugin validation prefix """

PROCESS_COMMAND_METHOD_PREFIX = "process_command_"
""" The prefix for the process command method """

COMMAND_VALUE = "command"
""" The command value """

ARGUMENTS_VALUE = "arguments"
""" The arguments value """

SPECIAL_VALUE_REGEX_VALUE = "%(?P<command>[a-zA-Z0-0_]*)(:(?P<arguments>[a-zA-Z0-9_.,]*))?%"
""" The special value regex value """

SPECIAL_VALUE_REGEX = re.compile(SPECIAL_VALUE_REGEX_VALUE)
""" The special value regex """

COLONY_VALUE = "colony"
""" The colony value """

EXECUTE_VALUE = "execute"
""" The execute value """

EXIT_VALUE = "exit"
""" The exit value """

LOAD_VALUE = "load"
""" The load value """

LAZY_LOAD_VALUE = "lazy_load"
""" The lazy load value """

END_LOAD_VALUE = "end_load"
""" The end load value """

UNLOAD_VALUE = "unload"
""" The unload value """

END_UNLOAD_VALUE = "end_unload"
""" The end load value """

NULL_VALUE = "null"
""" The null value """

class Plugin(object):
    """
    The abstract plugin class.
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

    attributes = {}
    """ The attributes of the plugin """

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

    allowed_loaded_capability = {}
    """ The list of allowed plugins loaded with capability """

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

    error_state = False
    """ The error state flag """

    exception = None
    """ The exception associated with the error state """

    ready_semaphore = None
    """ The ready semaphore """

    ready_semaphore_lock = None
    """ The ready semaphore lock """

    ready_semaphore_release_count = 0
    """ The ready semaphore release count """

    original_id = None
    """ The original id of the plugin """

    diffusion_scope_id = None
    """ The diffusion scope id of the plugin """

    manager = None
    """ The parent plugin manager """

    def __init__(self, manager = None):
        """
        Constructor of the class.

        @type manager: PluginManager
        @param manager: The plugin manager of the system.
        """

        self.original_id = self.id
        self.manager = manager
        self.ready_semaphore = threading.Semaphore(0)
        self.ready_semaphore_lock = threading.Lock()

        self.ready_semaphore_release_count = 0

        self.logger = logging.getLogger(DEFAULT_LOGGER)
        self.dependencies_loaded = []
        self.allowed_loaded = []
        self.allowed_loaded_capability = []
        self.event_plugins_handled_loaded_map = {}
        self.event_plugins_registered_loaded_map = {}
        self.event_plugin_manager_registered_loaded_list = []
        self.configuration_map = {}
        self.loaded = False
        self.lazy_loaded = False
        self.error_state = False

    def __repr__(self):
        """
        Returns the default representation of the class.

        @rtype: String
        @return: The default representation of the class.
        """

        return "<%s, %s, %s, %r>" % (
            self.__class__.__name__,
            self.name,
            self.version,
            self.capabilities,
        )

    def load_plugin(self):
        """
        Method called at the beginning of the plugin loading process.
        """

        # registers all the plugin manager events
        self.register_all_plugin_manager_events()

        # sets the loaded flag as true
        self.loaded = True

        # sets the loaded flag as true
        self.lazy_loaded = False

        # sets the error state as false
        self.error_state = False

        # generates the load plugin event
        self.manager.generate_event("plugin_manager.plugin.load_plugin", [self.id, self.version, self])

        self.info("Loading plugin '%s' v%s" % (self.short_name, self.version))

    def lazy_load_plugin(self):
        """
        Method called at the beginning of the lazy plugin loading process.
        """

        # registers all the plugin manager events
        self.register_all_plugin_manager_events()

        # sets the loaded flag as true
        self.loaded = True

        # sets the loaded flag as true
        self.lazy_loaded = True

        # sets the error state as false
        self.error_state = False

        # generates the lazy load plugin event
        self.manager.generate_event("plugin_manager.plugin.lazy_load_plugin", [self.id, self.version, self])

        # prints an info message
        self.info("Lazy loading plugin '%s' v%s" % (self.short_name, self.version))

    def end_load_plugin(self):
        """
        Method called at the end of the plugin loading process.
        """

        # generates the end load plugin event
        self.manager.generate_event("plugin_manager.plugin.end_load_plugin", [self.id, self.version, self])

        self.info("Loading process for plugin '%s' v%s completed" % (self.short_name, self.version))

    def unload_plugin(self):
        """
        Method called at the beginning of the plugin unloading process.
        """

        # unregisters all the plugin manager events
        self.unregister_all_plugin_manager_events()

        self.unregister_all_for_plugin()
        self.loaded = False

        # sets the error state as false
        self.error_state = False

        self.allowed_loaded = []
        self.dependencies_loaded = []

        # generates the load plugin event
        self.manager.generate_event("plugin_manager.plugin.unload_plugin", [self.id, self.version, self])

        self.info("Unloading plugin '%s' v%s" % (self.short_name, self.version))

    def end_unload_plugin(self):
        """
        Method called at the end of the plugin unloading process.
        """

        # sets the error state as false
        self.error_state = False

        # generates the load plugin event
        self.manager.generate_event("plugin_manager.plugin.end_unload_plugin", [self.id, self.version, self])

        self.info("Unloading process for plugin '%s' v%s completed" % (self.short_name, self.version))

    def load_allowed(self, plugin, capability):
        """
        Method called at the loading of an allowed plugin.

        @type plugin: Plugin
        @param plugin: The allowed plugin that is being loaded.
        @type capability: String
        @param capability: Capability for which the plugin is being injected.
        """

        self.allowed_loaded.append(plugin)
        self.allowed_loaded_capability.append((plugin, capability))
        self.register_all_registrable_events_plugin(plugin)
        self.info("Loading plugin '%s' v%s in '%s' v%s" % (plugin.short_name, plugin.version, self.short_name, self.version))

    def unload_allowed(self, plugin, capability):
        """
        Method called at the unloading of an allowed plugin.

        @type plugin: Plugin
        @param plugin: The allowed plugin that is being unloaded.
        @type capability: String
        @param capability: Capability for which the plugin is being injected.
        """

        self.allowed_loaded.remove(plugin)
        self.allowed_loaded_capability.remove((plugin, capability))
        self.unregister_all_registrable_events_plugin(plugin)
        self.info("Unloading plugin '%s' v%s in '%s' v%s" % (plugin.short_name, plugin.version, self.short_name, self.version))

    def dependency_injected(self, plugin):
        """
        Method called at the injection of a plugin dependency.

        @type plugin: Plugin
        @param plugin: The dependency plugin to be injected.
        """

        self.dependencies_loaded.append(plugin)
        self.info("Plugin dependency '%s' v%s injected in '%s' v%s" % (plugin.short_name, plugin.version, self.short_name, self.version))

    def init_complete(self):
        """
        Method called at the end of the plugin manager initialization.
        """

        self.info("Plugin '%s' v%s notified about the end of the plugin manager init process" % (self.short_name, self.version))

    def register_all_registrable_events_plugin(self, plugin):
        """
        Registers all the allowed events from a given plugin in self.

        @type plugin: Plugin
        @param plugin: The plugin containing the events to be registered.
        """

        event_names_registrable = [event_name for event_name in plugin.events_handled if is_event_or_super_event_in_list(event_name, self.events_registrable)]

        for event_name_registrable in event_names_registrable:
            self.register_for_plugin_event(plugin, event_name_registrable)

    def unregister_all_registrable_events_plugin(self, plugin):
        """
        Unregisters all the allowed events from a given plugin in self.

        @type plugin: Plugin
        @param plugin: The plugin containing the events to be unregistered.
        """

        for event_name in self.event_plugins_registered_loaded_map:
            if plugin in self.event_plugins_registered_loaded_map[event_name]:
                self.unregister_for_plugin_event(plugin, event_name)

    def register_all_plugin_manager_events(self):
        """
        Registers all the plugin manager events in self.
        """

        event_names_registrable = [event_name for event_name in self.events_registrable if is_event_or_sub_event(PLUGIN_MANAGER_TYPE, event_name)]

        for event_name_registrable in event_names_registrable:
            self.register_for_plugin_manager_event(event_name_registrable)

    def unregister_all_plugin_manager_events(self):
        """
        Unregisters all the plugin manager events in self.
        """

        for event_name in self.event_plugin_manager_registered_loaded_list:
            self.unregister_for_plugin_manager_event(event_name)

    def register_for_plugin_event(self, plugin, event_name):
        """
        Registers a given event from a given plugin in self.

        @type plugin: Plugin
        @param plugin: The plugin containing the event to be registered.
        @type event_name: String
        @param event_name: The name of the event to be registered.
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
        Unregisters a given event from a given plugin in self.

        @type plugin: Plugin
        @param plugin: The plugin containing the event to be unregistered.
        @type event_name: String
        @param event_name: The name of the event to be unregistered.
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
        Registers a given plugin manager event in self.

        @type event_neme: String
        @param event_name: The name of the event to be registered.
        """

        # retrieves the plugin manager
        plugin_manager = self.manager

        # registers the plugin event in the plugin manager containing the event
        plugin_manager.register_plugin_manager_event(self, event_name)

        # appends the plugin manager containing the event to be registered to the plugin manager events map
        self.event_plugin_manager_registered_loaded_list.append(event_name)

    def unregister_for_plugin_manager_event(self, event_name):
        """
        Unregisters a given plugin manager event in self.

        @type event_name: String
        @param event_name: The name of the event to be unregistered.
        """

        # retrieves the plugin manager
        plugin_manager = self.manager

        # unregisters the plugin event in the plugin manager containing the event
        plugin_manager.unregister_plugin_manager_event(self, event_name)

        if event_name in self.event_plugin_manager_registered_loaded_list:
            self.event_plugin_manager_registered_loaded_list.remove(event_name)

    def unregister_all_for_plugin_event(self, event_name):
        """
        Unregisters all the handlers for the event with the given name.

        @type event_name: String
        @param event_name: The name of the event to be unregistered.
        """

        if event_name in self.event_plugins_registered_loaded_map:
            for plugin in self.event_plugins_registered_loaded_map[event_name]:
                if plugin.is_loaded_or_lazy_loaded():
                    self.unregister_for_plugin_event(plugin, event_name)

    def unregister_all_for_plugin(self):
        """
        Unregisters all the event handlers for the events of self.
        """

        for event_name in self.event_plugins_registered_loaded_map:
            self.unregister_all_for_plugin_event(event_name)

    def register_plugin_event(self, plugin, event_name):
        """
        Registers a given event in the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin containing the handler to the event.
        @type event_name: String
        @param event_name: The name of the event to be registered.
        """

        if not event_name in self.event_plugins_handled_loaded_map:
            self.event_plugins_handled_loaded_map[event_name] = []

        if not plugin in self.event_plugins_handled_loaded_map[event_name]:
            self.event_plugins_handled_loaded_map[event_name].append(plugin)
            self.info("Registering event '%s' from '%s' v%s in '%s' v%s" % (event_name, plugin.short_name, plugin.version, self.short_name, self.version))

    def unregister_plugin_event(self, plugin, event_name):
        """
        Unregisters a given event in the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin containing the handler to the event.
        @type event_name: String
        @param event_name: The name of the event to be unregistered.
        """

        if event_name in self.event_plugins_handled_loaded_map:
            if plugin in self.event_plugins_handled_loaded_map[event_name]:
                self.event_plugins_handled_loaded_map[event_name].remove(plugin)
                self.info("Unregistering event '%s' from '%s' v%s in '%s' v%s" % (event_name, plugin.short_name, plugin.version, self.short_name, self.version))

    def notify_handlers(self, event_name, event_args):
        """
        Notifies all the handlers for the event with the given name with the give arguments.

        @type event_name: String
        @param event_name: The name of the event to be notified.
        @type event_args: List
        @param event_args: The arguments to be passed to the handler.
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
        Generates an event and starts the process of handler notification.

        @type event_name: String
        @param event_name: The name of the event to be notified.
        @type event_args: List
        @param event_args: The arguments to be passed to the handler.
        """

        if not is_event_or_super_event_in_list(event_name, self.events_handled):
            return

        # prints an info message
        self.info("Event '%s' generated in '%s' v%s" % (event_name, self.short_name, self.version))

        # notifies the event handlers
        self.notify_handlers(event_name, event_args)

    def event_handler(self, event_name, *event_args):
        """
        The top level event handling method.

        @type event_name: String
        @param event_name: The name of the event triggered.
        @type event_args: List
        @param event_args: The arguments for the handler.
        """

        # prints an info message
        self.info("Event '%s' caught in '%s' v%s" % (event_name, self.short_name, self.version))

    def reload_main_modules(self):
        """
        Reloads the plugin main modules in the interpreter.
        """

        # prints an info message
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

        return self.configuration_map.get(property_name, None)

    def set_configuration_property(self, property_name, property):
        """
        Sets the configuration property for the given property name.

        @type property_name: String
        @param property_name: The property name to set the property.
        @type property: String
        @param property: The property name to set.
        """

        self.info("Setting configuration property '%s' in '%s' v%s" % (property_name, self.short_name, self.version))

        self.configuration_map[property_name] = property

    def unset_configuration_property(self, property_name):
        """
        Unsets the configuration property for the given property name.

        @type property_name: String
        @param property_name: The property name to unset the property.
        """

        self.info("Unsetting configuration property '%s' from '%s' v%s" % (property_name, self.short_name, self.version))

        del self.configuration_map[property_name]

    def is_loaded(self):
        """
        Returns the result of the loading test.

        @rtype: bool
        @return: The result of the loading test (if the plugin is loaded or not).
        """

        return self.loaded and not self.lazy_loaded and not self.error_state

    def is_lazy_loaded(self):
        """
        Returns the result of the lazy loading test.

        @rtype: bool
        @return: The result of the lazy loading test (if the plugin is lazy loaded or not).
        """

        return self.lazy_loaded and not self.error_state

    def is_loaded_or_lazy_loaded(self):
        """
        Returns the result of the loading and lazy loading tests.

        @rtype: bool
        @return: The result of the loading and lazy loading tests (if the plugin is loaded or lazy loaded or not).
        """

        return (self.loaded or self.lazy_loaded) and not self.error_state

    def is_replica(self):
        """
        Returns the result of the replica test.

        @rtype: bool
        @return: The result of the replica test (if the plugin is a replica or not).
        """

        return not self.id == self.original_id

    def get_attribute(self, attribute_name):
        """
        Retrieves the attribute for the given attribute name.

        @type attribute_name: String
        @param attribute_name: The name of the attribute name to retrieve.
        @rtype: Object
        @return: The attribute for the given attribute name.
        """

        return self.attributes.get(attribute_name, None)

    def contains_metadata(self):
        """
        Returns the result of the metadata test.

        @rtype: bool
        @return: The result of the metadata test (if the plugin contains metadata or not).
        """

        if hasattr(self, "metadata_map"):
            return True
        else:
            return False

    def contains_metadata_key(self, metadata_key):
        """
        Returns the result of the metadata key test.

        @type metadata_key: String
        @param metadata_key: The value of the metadata key to test for metadata.
        @rtype: bool
        @return: The result of the metadata key test (if the plugin contains the metadata key or not).
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
        Returns the metadata of the plugin.

        @rtype: Dictionary
        @return: The metadata of the plugin.
        """

        if self.contains_metadata():
            return self.metadata_map

    def get_metadata_key(self, metadata_key):
        """
        Returns the metadata key of the plugin.

        @type metadata_key: String
        @param metadata_key: The value of the metadata key to retrieve.
        @rtype: Object
        @return: The metadata key of the plugin.
        """

        if self.contains_metadata_key(metadata_key):
            return self.metadata_map[metadata_key]

    def treat_exception(self, exception):
        """
        Treats the exception at the most abstract level.

        @type exception: Exception
        @param exception: The exception object to be treated.
        """

        # prints and info message
        self.info("Exception '%s' generated in '%s' v%s" % (str(exception), self.short_name, self.version))

        # unloads the plugin
        self.manager.unload_plugin(self.id)

    def acquire_ready_semaphore(self):
        """
        Acquires the ready semaphore (useful for thread enabled plugins).
        """

        # acquires the ready semaphore
        self.ready_semaphore.acquire()

    def release_ready_semaphore(self):
        """
        Releases the ready semaphore (useful for thread enabled plugins).
        """

        # acquires the ready semaphore lock
        self.ready_semaphore_lock.acquire()

        # increment the ready semaphore release count
        self.ready_semaphore_release_count += 1

        # releases the ready semaphore
        self.ready_semaphore.release()

        # releases the ready semaphore lock
        self.ready_semaphore_lock.release()

    def ready_semaphore_status(self):
        """
        Retrieves the status of the ready semaphore (useful for thread enabled plugins).
        """

        # retrieves thre ready semaphore condition
        ready_semaphore_condition = self.ready_semaphore._Semaphore__cond

        # retrieves the ready semaphore condition lock
        ready_semaphore_condition_lock = ready_semaphore_condition._Condition__lock

        return not ready_semaphore_condition_lock.locked()

    def get_all_plugin_dependencies(self):
        """
        Retrieves all the plugin dependencies of the plugin.

        @rtype: List
        @requires: A list containing all the plugin dependencies of the plugin.
        """

        plugin_dependencies = []

        for dependency in self.dependencies:
            if isinstance(dependency, PluginDependency):
                plugin_dependencies.append(dependency)

        return plugin_dependencies

    def get_all_package_dependencies(self):
        """
        Retrieves all the packages dependencies of the plugin.

        @rtype: List
        @requires: A list containing all the package dependencies of the plugin.
        """

        package_dependencies = []

        for dependency in self.dependencies:
            if isinstance(dependency, PackageDependency):
                package_dependencies.append(dependency)

        return package_dependencies

    def get_tuple(self):
        """
        Retrieves a tuple representing the plugin (id and version).

        @rtype: Tuple
        @return: Tuple representing the plugin (id and version).
        """

        return (self.id, self.version)

    def log_stack_trace(self):
        """
        Logs the current stack trace to the plugin manager logger.
        """

        # retrieves the execution information
        _type, _value, traceback_list = sys.exc_info()

        # in case the traceback list is valid
        if traceback_list:
            formated_traceback = traceback.format_tb(traceback_list)
        else:
            formated_traceback = ()

        # iterates over the traceback lines
        for formated_traceback_line in formated_traceback:
            # strips the formated traceback line
            formated_traceback_line_stripped = formated_traceback_line.rstrip()

            # prints an debug message with the formated traceback line
            self.logger.debug(formated_traceback_line_stripped)

    def debug(self, message):
        """
        Adds the given debug message to the logger.

        @type message: String
        @param message: The debug message to be added to the logger.
        """

        # formats the logger message
        logger_message = self.format_logger_message(message)

        # prints the debug message
        self.logger.debug(logger_message)

    def info(self, message):
        """
        Adds the given info message to the logger.

        @type message: String
        @param message: The info message to be added to the logger.
        """

        # formats the logger message
        logger_message = self.format_logger_message(message)

        # prints the info message
        self.logger.info(logger_message)

    def warning(self, message):
        """
        Adds the given warning message to the logger.

        @type message: String
        @param message: The warning message to be added to the logger.
        """

        # formats the logger message
        logger_message = self.format_logger_message(message)

        # prints the warning message
        self.logger.warning(logger_message)

        # logs the stack trace
        self.log_stack_trace()

    def error(self, message):
        """
        Adds the given error message to the logger.

        @type message: String
        @param message: The error message to be added to the logger.
        """

        # formats the logger message
        logger_message = self.format_logger_message(message)

        # prints the error message
        self.logger.error(logger_message)

        # logs the stack trace
        self.log_stack_trace()

    def critical(self, message):
        """
        Adds the given critical message to the logger.

        @type message: String
        @param message: The critical message to be added to the logger.
        """

        # formats the logger message
        logger_message = self.format_logger_message(message)

        # prints the critical message
        self.logger.critical(logger_message)

        # logs the stack trace
        self.log_stack_trace()

    def format_logger_message(self, message):
        """
        Formats the given message into a logging message.

        @type message: String
        @param message: The message to be formated into logging message.
        @rtype: String
        @return: The formated logging message.
        """

        # the default formatting message
        formatting_message = str()

        # in case the plugin id logging option is activated
        if plugin_manager_configuration.get("plugin_id_logging", False):
            formatting_message += "[" + self.id + "] "

        # in case the thread id logging option is activated
        if plugin_manager_configuration.get("thread_id_logging", False):
            formatting_message += "[" + str(thread.get_ident()) + "] "

        # appends the formatting message to the logging message
        logger_message = formatting_message + message

        # returns the logger message
        return logger_message

    def _get_capabilities_allowed_names(self):
        """
        Retrieves the names of all the allowed capabilities
        from this plugin.

        @rtype: List
        @return: The names of all the allowed capabilities
        from this plugin.
        """

        # starts the capabilities allowed names
        capabilities_allowed_names = []

        # iterates over all the capability allowed
        for capability_allowed in self.capabilities_allowed:
            # retrieves the capability allowed type
            capability_allowed_type = type(capability_allowed)

            if capability_allowed_type == types.TupleType:
                capability_allowed_name = capability_allowed[0]
            else:
                capability_allowed_name = capability_allowed

            # adds the capability allowed name to the capabilities
            # allowed names
            capabilities_allowed_names.append(capability_allowed_name)

        # returns the capabilities allowed names
        return capabilities_allowed_names

class PluginManagerPlugin(Plugin):
    """
    The plugin manager plugin class, used to extend the plugin manager functionality.
    """

    valid = False
    """ The valid flag of the plugin """

    def __init__(self, manager = None):
        """
        Constructor of the class.

        @type manager: PluginManager
        @param manager: The plugin manager of the system.
        """

        Plugin.__init__(self, manager)

class PluginManager:
    """
    The plugin manager class.
    """

    uid = None
    """ The unique identification """

    logger = None
    """ The logger used """

    platform = None
    """ The current executing platform """

    condition = None
    """ The condition used in the event queue """

    init_complete = False
    """ The initialization complete flag """

    init_complete_handlers = []
    """ The list of handlers to be called at the end of the plugin manager initialization """

    main_loop_active = True
    """ The boolean value for the main loop activation """

    layout_mode = "default"
    """ The layout mode used in the plugin loading """

    run_mode = "default"
    """ The run mode used in the plugin loading """

    container = "default"
    """ The name of the plugin manager container """

    daemon_pid = None
    """ The pid of the daemon process running the instance of plugin manager  """

    daemon_file_path = None
    """ The file path to the daemon file, for information control """

    execution_command = None
    """ The command to be executed on start (script mode) """

    configuration_path = DEFAULT_CONFIGURATION_PATH
    """ The current configuration path """

    workspace_path = DEFAULT_WORKSPACE_PATH
    """ The current workspace path """

    attributes_map = {}
    """ The attributes map """

    plugin_manager_timestamp = 0
    """ The plugin manager timestamp """

    plugin_manager_plugins_loaded = False
    """ The plugin manager plugins loaded flag """

    current_id = 0
    """ The current id used for the plugin """

    replica_id = 0
    """ The replica id for the replica plugins """

    diffusion_scope_id = 0
    """ The diffusion scope id for the replica plugins """

    return_code = 0
    """ The return code to be used on return """

    event_queue = []
    """ The queue of events to be processed """

    manager_path = None
    """ The manager base path for execution """

    logger_path = None
    """ The manager base path for logger """

    library_paths = None
    """ The set of paths for the external libraries plugins """

    plugin_paths = None
    """ The set of paths for the loaded plugins """

    kill_system_timer = None
    """ The timer used to kill the system in extreme situations """

    referred_modules = []
    """ The referred modules """

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

    plugin_classes = []
    """ The available plugin classes """

    plugin_classes_map = {}
    """ The map with classes associated with strings containing the id of the plugin """

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
    """ The map associating the capabilities with the the plugin that supports the capability """

    diffusion_scope_loaded_plugins_map = {}
    """ The map associating the diffusion scope with the loaded plugins that exist in the scope """

    deleted_plugin_classes = []
    """ The list containing the classes for the deleted plugins """

    event_plugins_handled_loaded_map = {}
    """ The map with the plugin associated with the name of the event handled """

    def __init__(self, manager_path = None, logger_path = None, library_paths = None, plugin_paths = None, platform = CPYTHON_ENVIRONMENT, init_complete_handlers = [], stop_on_cycle_error = True, main_loop_active = True, layout_mode = "default", run_mode = "default", container = "default", daemon_pid = None, daemon_file_path = None, execution_command = None, attributes_map = {}):
        """
        Constructor of the class.

        @type manager_path: List
        @param manager_path: The manager base path for execution.
        @type logger_path: String
        @param logger_path: The manager base path for logger.
        @type library_paths: List
        @param library_paths: The list of directory paths for the loading of the external libraries.
        @type plugin_paths: List
        @param plugin_paths: The list of directory paths for the loading of the plugins.
        @type platform: int
        @param platform: The current executing platform.
        @type init_complete_handlers: List
        @param init_complete_handlers: The list of handlers to be called at the end of the plugin manager initialization.
        @type stop_on_cycle_error: bool
        @param stop_on_cycle_error: The boolean value for the stop on cycle error.
        @type main_loop_active: bool
        @param main_loop_active: The boolean value for the main loop activation.
        @type layout_mode: String
        @param layout_mode: The layout mode used in the plugin loading.
        @type run_mode: String
        @param run_mode: The run mode used in the plugin loading.
        @type container: String
        @param container: The name of the plugin manager container.
        @type daemon_pid: int
        @param daemon_pid: The pid of the daemon process running the instance of plugin manager.
        @type daemon_file_path: String
        @param daemon_file_path: The file path to the daemon file, for information control.
        @type execution_command: String
        @param execution_command: The command to be executed on start (script mode).
        @type attributes_map: Dictionary
        @param attributes_map: The map associating the attribute key and the attribute value.
        """

        self.manager_path = manager_path
        self.logger_path = logger_path
        self.library_paths = library_paths
        self.plugin_paths = plugin_paths
        self.platform = platform
        self.init_complete_handlers = init_complete_handlers
        self.stop_on_cycle_error = stop_on_cycle_error
        self.main_loop_active = main_loop_active
        self.layout_mode = layout_mode
        self.run_mode = run_mode
        self.container = container
        self.daemon_pid = daemon_pid
        self.daemon_file_path = daemon_file_path
        self.execution_command = execution_command
        self.attributes_map = attributes_map

        self.uid = colony.base.util.get_timestamp_uid()
        self.condition = threading.Condition()

        self.current_id = 0
        self.event_queue = []
        self.referred_modules = []
        self.loaded_plugins = []
        self.loaded_plugins_map = {}
        self.loaded_plugins_id_map = {}
        self.id_loaded_plugins_map = {}
        self.loaded_plugins_descriptions = []
        self.plugin_classes = []
        self.plugin_classes_map = {}
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
        self.diffusion_scope_loaded_plugins_map = {}
        self.deleted_plugin_classes = []
        self.event_plugins_handled_loaded_map = {}

    def create_plugin(self, plugin_id, plugin_version):
        """
        Creates a new instance of the plugin with the given id
        and version.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to create an instance.
        @param plugin_version: plugin_version
        @param plugin_version: The version of the plugin to create an instance.
        @rtype: Plugin
        @return: The created plugin instance.
        """

        # @todo: important diffusion scope
        # tenho de pensar em como posso obter as classes para criar novas instancias
        # tenho de pensar como e ke as classes vao ser updatadas de modo a gerir autoloaders e afins

        # tenho de criar novas estruturas: esta estrutura serve para associar o origianl id com todas as instances do tipo replica
        # para depois quando se faze o reload do modulo tb fazemos reload das replicas
        # originalModuleIdClassHash.get(moduleOriginalId)

        # tenho de as manter actualizadas .... quando descarrego modulos, etc....
        # tenho de actualizar sempre que faco start_plugins (porque e neste momento que vai ser feito o refresh)

        # generates a new diffusion scope id
        diffusion_scope_id = self.generate_diffusion_scope_id()

        # creates a new plugin instance in the new diffusion scope id
        plugin_instance = self._create_plugin(plugin_id, plugin_version, diffusion_scope_id)

        # returns the created plugin instance
        return plugin_instance

    def _create_plugin(self, plugin_id, plugin_version, diffusion_scope_id):
        """
        Creates a new instance of the plugin with the given id
        and version for the given diffusion scope id.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to create an instance.
        @param plugin_version: plugin_version
        @param plugin_version: The version of the plugin to create an instance.
        @param diffusion_scope_id: int
        @param diffusion_scope_id: The diffusion scope id to be used in the creation.
        @rtype: Plugin
        @return: The created plugin instance.
        """

        # in case the plugin id does not exist in the plugin classes map
        if not plugin_id in self.plugin_classes_map:
            # raises the plugin class not available exception
            raise colony.base.plugin_system_exceptions.PluginClassNotAvailable("invalid plugin '%s' v%s" % (plugin_id, plugin_version))

        # retrieves the plugin class
        plugin_class = self.plugin_classes_map[plugin_id]

        # in case the plugin version is not the same
        if not plugin_class.version == plugin_version:
            # raises the plugin class not available exception
            raise colony.base.plugin_system_exceptions.PluginClassNotAvailable("invalid plugin '%s' v%s" % (plugin_id, plugin_version))

        # retrieves the generated replica id
        replica_id = self.generate_replica_id()

        # creates the plugin instance id
        plugin_instance_id = plugin_id + "[" + str(replica_id) + "]"

        # retrieves the plugin description
        plugin_description = plugin_class.description

        # instantiates the plugin to create the plugin instance
        plugin_instance = plugin_class(self)

        # sets the plugin instance id as the generated one
        plugin_instance.id = plugin_instance_id

        # sets the plugin diffusion scope id as the defined one
        plugin_instance.diffusion_scope_id = diffusion_scope_id

        # retrieves the path to the plugin file
        plugin_path = inspect.getfile(plugin_class)

        # retrieves the file system encoding
        file_system_encoding = sys.getfilesystemencoding()

        # decodes the plugin path using the file system encoding
        plugin_path = plugin_path.decode(file_system_encoding)

        # retrieves the absolute path to the plugin file
        absolute_plugin_path = os.path.abspath(plugin_path)

        # retrieves the path to the directory containing the plugin file
        plugin_dir = os.path.dirname(absolute_plugin_path)

        # starts all the plugin manager structures related with plugins
        self.loaded_plugins_map[plugin_instance_id] = plugin_class
        self.loaded_plugins_id_map[plugin_instance_id] = self.current_id
        self.id_loaded_plugins_map[self.current_id] = plugin_instance_id
        self.loaded_plugins_descriptions.append(plugin_description)
        self.plugin_instances.append(plugin_instance)
        self.plugin_instances_map[plugin_instance_id] = plugin_instance
        self.plugin_dirs_map[plugin_instance_id] = plugin_dir

        # sets the plugin instance in the diffusion scope loaded plugins map
        self.set_plugin_instance_diffusion_scope_loaded_plugins_map(diffusion_scope_id, plugin_id, plugin_instance)

        # registers the plugin capabilities in the plugin manager
        self.register_plugin_capabilities(plugin_instance)

        # increments the current id
        self.current_id += 1

        # returns the plugin instance
        return plugin_instance

    def generate_replica_id(self):
        """
        Generates the replica id.

        @rtype: int
        @return: The replica id.
        """

        # retrieves the replica id
        replica_id = self.replica_id

        # increments the replica id
        self.replica_id += 1

        # returns the current replica scope
        return replica_id

    def generate_diffusion_scope_id(self):
        """
        Generates the diffusion scope id.

        @rtype: int
        @return: The diffusion scope id.
        """

        # retrieves the diffusion scope id
        diffusion_scope_id = self.diffusion_scope_id

        # increments the diffusion scope id
        self.diffusion_scope_id += 1

        # returns the current diffusion scope
        return diffusion_scope_id

    def start_logger(self, log_level = DEFAULT_LOGGING_LEVEL):
        """
        Starts the logging system with the given log level.

        @type log_level: int
        @param log_level: The log level of the logger.
        """

        # retrieves the minimal log level between the current log level and the default one
        minimal_log_level = DEFAULT_LOGGING_LEVEL < log_level and DEFAULT_LOGGING_LEVEL or log_level

        # creates the logger file name
        logger_file_name = DEFAULT_LOGGING_FILE_NAME_PREFIX + DEFAULT_LOGGING_FILE_NAME_SEPARATOR + self.run_mode + DEFAULT_LOGGING_FILE_NAME_EXTENSION

        # creates the logger file path
        logger_file_path = self.logger_path + "/" + logger_file_name

        # retrieves the logger
        logger = logging.getLogger(DEFAULT_LOGGER)

        # sets the logger propagation to avoid propagation
        logger.propagate = 0

        # sets the logger level to the minimal log level
        logger.setLevel(minimal_log_level)

        # creates the stream handler
        stream_handler = logging.StreamHandler()

        # sets the logger level for the stream handler (the currently selected log level)
        stream_handler.setLevel(log_level)

        # creates the rotating file handler
        rotating_file_handler = logging.handlers.RotatingFileHandler(logger_file_path, DEFAULT_LOGGING_FILE_MODE, DEFAULT_LOGGING_FILE_SIZE, DEFAULT_LOGGING_FILE_BACKUP_COUNT)

        # retrieves the logging format
        logging_format = plugin_manager_configuration.get("logging_format", DEFAULT_LOGGING_FORMAT)

        # creates the logging formatter
        formatter = logging.Formatter(logging_format)

        # sets the formatter in the stream handler
        stream_handler.setFormatter(formatter)

        # sets the formatter in the rotating file handler
        rotating_file_handler.setFormatter(formatter)

        # adds the stream handler to the logger
        logger.addHandler(stream_handler)

        # adds the rotating file handler to the logger
        logger.addHandler(rotating_file_handler)

        # sets the logger
        self.logger = logger

    def load_system(self):
        """
        Starts the process of loading the plugin system.

        @rtype: int
        @return: The return code.
        """

        try:
            # prints an info message
            self.logger.info("Starting plugin manager...")

            # updates the workspace path
            self.update_workspace_path()

            # checks the standard input
            self.check_standard_input()

            # gets all modules from all plugin paths
            for plugin_path in self.plugin_paths:
                # extends the referred modules with all the plugin modules
                self.referred_modules.extend(self.get_all_modules(plugin_path))

            # starts the plugin loading process
            self.init_plugin_system({"library_paths" : self.library_paths, "plugin_paths" : self.plugin_paths, "plugins" : self.referred_modules})

            # starts the main loop
            self.main_loop()
        except BaseException, exception:
            # handles the system exception
            self._handle_system_exception(exception)

            # sets the return code to error
            self.return_code = 1

        # returns the return code
        return self.return_code

    def unload_system(self, thread_safe = True):
        """
        Unloads the plugin system from memory, exiting the system.

        @type thread_safe: bool
        @param thread_safe: If the unloading should use the event mechanism
        to provide thread safety.
        """

        # creates the kill system timer, to kill the system
        # if it hangs in shutdown
        self.kill_system_timer = threading.Timer(DEFAULT_UNLOAD_SYSTEM_TIMEOUT, self._kill_system_timeout)

        # starts the kill system timer
        self.kill_system_timer.start()

        # iterates over all the plugin instances
        for plugin_instance in self.plugin_instances:
            # in case the plugin instance is loaded
            if plugin_instance.is_loaded():
                # in case the plugin contains the main type capability
                if MAIN_TYPE in plugin_instance.capabilities:
                    # unloads the plugin using the main type unloading
                    self._unload_plugin(plugin_instance, None, MAIN_TYPE)
                # in case the plugin contains the thread type capability
                elif THREAD_TYPE in plugin_instance.capabilities:
                    # unloads the plugin using the thread type unloading
                    self._unload_plugin(plugin_instance, None, THREAD_TYPE)
                # otherwise
                else:
                    # unloads the plugin normally
                    self._unload_plugin(plugin_instance, None)

        # in case thread safety is requested
        if thread_safe:
            # creates the exit event
            exit_event = colony.base.util.Event(EXIT_VALUE)

            # adds the exit event to the event queue
            self.add_event(exit_event)
        else:
            # unloads the thread based plugins
            self._unload_thread_plugins()

        # cancels the kill system timer
        self.kill_system_timer.cancel()

    def main_loop(self):
        """
        The main loop for the plugin manager.
        """

        # main loop cycle
        while self.main_loop_active:
            # acquires the condition
            self.condition.acquire()

            # iterates while the event queue has no items
            while not len(self.event_queue):
                try:
                    # waits for the condition to be notified
                    # this wait releases after the defined timeout
                    # in order to provide a away to process external interrupts
                    self.condition.wait(DEFAULT_LOOP_WAIT_TIMEOUT)
                except RuntimeError:
                    # timeout occurred (ignores it)
                    pass

            # pops the top item
            event = self.event_queue.pop(0)

            if event.event_name == EXECUTE_VALUE:
                execution_method = event.event_args[0]
                execution_arguments = event.event_args[1:]
                execution_method(*execution_arguments)
            elif event.event_name == EXIT_VALUE:
                # unloads the thread based plugins
                self._unload_thread_plugins()

                # returns the method exiting the plugin system
                return

            # releases the condition
            self.condition.release()

    def add_event(self, event):
        """
        Adds an event to the list of events in the plugin manager.

        @type event: Event
        @param event: The event to add to the list of events in the plugin manager.
        """

        # acquires the condition
        self.condition.acquire()

        # adds the event to the event queue
        self.event_queue.append(event)

        # notifies the condition
        self.condition.notify()

        # releases the condition
        self.condition.release()

    def expand_workspace_path(self):
        """
        Expands the workspace path, in order to
        avoid possible problems when accessing the colony
        workspace.
        """

        # expands the workspace path
        self.workspace_path = os.path.expanduser(self.workspace_path)

    def create_workspace_path(self):
        """
        Creates the workspace path, in case it does
        not exists already.
        """

        # in case the workspace path does not exists
        if not os.path.exists(self.workspace_path):
            # creates the workspace path as a directory
            os.mkdir(self.workspace_path)

    def update_workspace_path(self):
        """
        Updates the workspace path, expanding the workspace
        path and creating the workspace path if necessary.
        """

        # expands the workspace path
        self.expand_workspace_path()

        # creates the workspace path directory
        # if necessary
        self.create_workspace_path()

    def check_standard_input(self):
        """
        Checks if the standard input to be used should
        be changed to a dummy one in order to avoid possible
        blocking.
        """

        # in case there the execution of type script or is a daemon
        if self.execution_command or self.daemon_pid or self.daemon_file_path:
            # sets the standard input as a dummy input object (for no blocking)
            sys.stdin = colony.base.dummy_input.DummyInput()

    def get_all_modules(self, path):
        """
        Retrieves all the modules in a given path.

        @type path: String
        @param path: The path to retrieve the modules.
        @rtype: List
        @return: All the modules in the given path.
        """

        # starts the modules list
        modules = []

        # in case the path does not exist
        if not os.path.exists(path):
            self.logger.warning("Path '%s' does not exist in the current filesystem" % (path))
            return modules

        # retrieves the directory list for the path
        dir_list = os.listdir(path)

        # iterates over all the file names
        # in the directory list
        for file_name in dir_list:
            # creates the full file path
            full_path = path + "/" + file_name

            # retrieves the file mode
            mode = os.stat(full_path)[stat.ST_MODE]

            # in case the file is not a directory
            if not stat.S_ISDIR(mode):
                # splits the path
                split = os.path.splitext(file_name)

                # retrieves the extension
                extension = split[-1]

                # in case the extension is a valid python extension
                if extension == ".py" or extension == ".pyc":
                    # retrieves the module name from the file name
                    module_name = "".join(split[:-1])

                    # in case the module name is not defined
                    # in the modules list
                    if not module_name in modules:
                        # adds the module name to the modules list
                        modules.append(module_name)

        # returns the modules list
        return modules

    def init_plugin_system(self, configuration):
        """
        Starts the plugin loading process.

        @type configuration: Dictionary
        @param configuration: The configuration structure.
        """

        # adds the defined library and plugin paths to the system python path
        self.set_python_path(configuration["library_paths"], configuration["plugin_paths"])

        # loads the plugin files into memory
        self.load_plugins(configuration["plugins"])

        # starts all the available the plugin manager plugins
        self.start_plugin_manager_plugins()

        # loads the plugin manager plugins
        self.load_plugin_manager_plugins()

        # sets the plugin manager timestamp
        self.set_plugin_manager_timestamp()

        # sets the plugin manager plugins loaded to true
        self.set_plugin_manager_plugins_loaded(True)

        # starts all the available the plugins
        self.start_plugins()

        # loads the startup plugins
        self.load_startup_plugins()

        # loads the main plugins
        self.load_main_plugins()

        # installs the signal handlers
        self.install_signal_handlers()

        # sets the init flag to true
        self.set_init_complete(True)

        # notifies all the loaded plugins about the init load complete
        self.notify_load_complete_loaded_plugins()

        # notifies all the init complete handlers about the init load complete
        self.notify_load_complete_handlers()

        # notifies the daemon file
        self.notify_daemon_file()

        # executes the execution command
        self.execute_command()

    def set_python_path(self, library_paths, plugin_paths):
        """
        Updates the python path adding the defined list of library and plugin paths.

        @type library_paths: List
        @param library_paths: The list of library paths to add to the python path.
        @type plugin_paths: List
        @param plugin_paths: The list of plugin paths to add to the python path.
        """

        # iterates over all the library paths in library paths
        for library_path in library_paths:
            # if the path is not in the python lib
            # path inserts the path into it
            if not library_path in sys.path:
                # normalizes the library path
                library_path = os.path.normpath(library_path)

                # inserts the library path in the system path
                sys.path.insert(0, library_path)

        # iterates over all the plugin paths in plugin paths
        for plugin_path in plugin_paths:
            # if the path is not in the python lib
            # path inserts the path into it
            if not plugin_path in sys.path:
                # normalizes the library path
                plugin_path = os.path.normpath(plugin_path)

                # inserts the plugin path in the system path
                sys.path.insert(0, plugin_path)

    def load_plugins(self, plugins):
        """
        Imports a module starting the plugin.

        @type plugins: List
        @param plugins: The list of plugins to be loaded.
        """

        # prints an info message
        self.logger.info("Loading plugins (importing %d main module files)..." % len(plugins))

        # iterates over all the available plugins
        for plugin in plugins:
            # in case the plugin module is not currently loaded
            if not plugin in sys.modules:
                try:
                    # imports the plugin module file
                    __import__(plugin)
                except BaseException, exception:
                    # prints an error message
                    self.logger.error("Problem importing module %s: %s" % (plugin, unicode(exception)))

        # prints an info message
        self.logger.info("Finished loading plugins")

    def start_plugin_manager_plugins(self):
        """
        Starts all the available plugin manager plugins, creating a singleton instance for each of them.
        """

        # retrieves all the plugin manager plugin classes available
        self.plugin_classes = self.get_all_plugin_classes(PluginManagerPlugin)

        # iterates over all the available plugin manager plugin classes
        for plugin in self.plugin_classes:
            # retrieves the plugin id
            plugin_id = plugin.id

            # sets the plugin class in the plugin classes map
            self.plugin_classes_map[plugin_id] = plugin

            # tests the plugin for loading
            if not plugin in self.loaded_plugins:
                # starts the plugin
                self.start_plugin(plugin)

    def start_plugins(self):
        """
        Starts all the available plugins, creating a singleton instance for each of them.
        """

        # retrieves all the plugin classes available
        self.plugin_classes = self.get_all_plugin_classes()

        # iterates over all the available plugin classes
        for plugin in self.plugin_classes:
            # retrieves the plugin id
            plugin_id = plugin.id

            # sets the plugin class in the plugin classes map
            self.plugin_classes_map[plugin_id] = plugin

            # tests the plugin for loading
            if not plugin in self.loaded_plugins:
                # starts the plugin
                self.start_plugin(plugin)

    def start_plugin(self, plugin):
        """
        Starts the given plugin, creating a singleton instance.

        @type plugin: Class
        @param plugin: The plugin to start.
        """

        # retrieves the plugin id
        plugin_id = plugin.id

        # retrieves the plugin description
        plugin_description = plugin.description

        # instantiates the plugin to create the singleton plugin instance
        plugin_instance = plugin(self)

        # retrieves the path to the plugin file
        plugin_path = inspect.getfile(plugin)

        # retrieves the file system encoding
        file_system_encoding = sys.getfilesystemencoding()

        # decodes the plugin path using the file system encoding
        plugin_path = plugin_path.decode(file_system_encoding)

        # retrieves the absolute path to the plugin file
        absolute_plugin_path = os.path.abspath(plugin_path)

        # retrieves the path to the directory containing the plugin file
        plugin_dir = os.path.dirname(absolute_plugin_path)

        # starts all the plugin manager structures related with plugins
        self.loaded_plugins.append(plugin)
        self.loaded_plugins_map[plugin_id] = plugin
        self.loaded_plugins_id_map[plugin_id] = self.current_id
        self.id_loaded_plugins_map[self.current_id] = plugin_id
        self.loaded_plugins_descriptions.append(plugin_description)
        self.plugin_instances.append(plugin_instance)
        self.plugin_instances_map[plugin_id] = plugin_instance
        self.plugin_dirs_map[plugin_id] = plugin_dir

        # sets the plugin instance in the diffusion scope loaded plugins map
        self.set_plugin_instance_diffusion_scope_loaded_plugins_map(None, plugin_id, plugin_instance)

        # registers the plugin capabilities in the plugin manager
        self.register_plugin_capabilities(plugin_instance)

        # increments the current id
        self.current_id += 1

    def stop_plugin_complete_by_id(self, plugin_id):
        """
        Stops a plugin with the given id, removing it and the referring module from the plugin system.

        @type plugin_id: String
        @param plugin: The id of the plugin to be removed from the plugin system.
        """

        # retrieves the referring plugin module
        module = self.get_plugin_module_name_by_id(plugin_id)

        # stops the referring plugin module
        self.stop_module(module)

    def stop_module(self, module):
        """
        Stops the given plugin module in the plugin manager.

        @type module: String
        @param module: The name of the plugin module to stop.
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
        Stops a plugin, removing it from the plugin system.

        @type plugin: Plugin
        @param plugin: The plugin to be removed from the plugin system.
        """

        # retrieves the plugin id
        plugin_id = plugin.id

        # retrieves the plugin version
        plugin_version = plugin.version

        # retrieves the plugin description
        plugin_description = plugin.description

        # retrieves the temporary internal plugin id
        current_id = self.loaded_plugins_id_map[plugin_id]

        # retrieves the plugin instance
        plugin_instance = self.plugin_instances_map[plugin_id]

        # in case the plugin is loaded the plugin is unloaded
        if plugin_instance.is_loaded():
            if MAIN_TYPE in plugin.capabilities:
                self._unload_plugin(plugin_instance, FILE_REMOVED_TYPE, MAIN_TYPE)
            elif THREAD_TYPE in plugin.capabilities:
                self._unload_plugin(plugin_instance, FILE_REMOVED_TYPE, THREAD_TYPE)
            else:
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
        colony.base.decorators.unregister_plugin_decorators(plugin_id, plugin_version)

        # in case the plugin exists in the plugin threads map
        if plugin_id in self.plugin_threads_map:
            # retrieves the available thread for the plugin
            plugin_thread = self.plugin_threads_map[plugin_id]

            # creates the plugin exit event
            event = colony.base.util.Event(EXIT_VALUE)

            # adds the load event to the thread queue
            plugin_thread.add_event(event)

            # joins the plugin thread
            plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)

            # removes the plugin thread from the plugin threads map
            del self.plugin_threads_map[plugin_id]

    def get_all_plugin_classes(self, base_plugin_class = Plugin):
        """
        Retrieves all the available plugin classes, from the defined base plugin class.

        @type base_plugin_class: Class
        @param base_plugin_class: The base plugin class to retrieve the plugin classes.
        @rtype: List
        @return: The list of plugin classes.
        """

        # creates the plugin classes list
        plugin_classes = []

        # retrieves the plugin sub classes (loads the sub classes into
        # the plugin classes list)
        self.get_plugin_sub_classes(base_plugin_class, plugin_classes)

        # returns the plugin classes list
        return plugin_classes

    def get_plugin_sub_classes(self, plugin, plugin_classes):
        """
        Retrieves all the sub classes for the given plugin class.

        @type plugin: Class
        @param plugin: The plugin class to retrieve the sub classes.
        @type plugin_classes: List
        @param plugin_classes: The current list of plugin sub classes.
        @rtype: List
        @return: The list of all the sub classes for the given plugin class.
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
        Registers all the available capabilities for the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin to register the capabilities.
        """

        # iterates over all the plugin instance capabilities
        for capability in plugin.capabilities:
            # retrieves the capability and super capabilities list
            capability_and_super_capabilites_list = capability_and_super_capabilites(capability)

            # retrieves the capability and super capabilities list length
            capability_and_super_capabilites_list_length = len(capability_and_super_capabilites_list)

            # iterates over the capability or super capabilities list length range
            for capability_or_super_capability_index in range(capability_and_super_capabilites_list_length):
                # retrieves the capability from the capability and super capabilities list
                capability = capability_and_super_capabilites_list[capability_or_super_capability_index]

                # retrieves the sub capabilities list from the the capability and super capabilities list
                sub_capabilities_list = capability_and_super_capabilites_list[capability_or_super_capability_index + 1:]

                # in case the capability does not exists in the capabilities plugin instances map
                if not capability in self.capabilities_plugin_instances_map:
                    # creates a new list as the value for the capability in the
                    # capabilities plugin instances map
                    self.capabilities_plugin_instances_map[capability] = []

                # adds the plugin to the capabilities plugin instances map for the capability
                self.capabilities_plugin_instances_map[capability].append(plugin)

                # in case the capability does not exists in the capabilities and sub capabilities map
                if not capability in self.capabilities_sub_capabilities_map:
                    # creates a new list as the value for the capability in the
                    # capabilities and sub capabilities map
                    self.capabilities_sub_capabilities_map[capability] = []

                # iterates over all the sub capabilities in the sub capabilities list
                for sub_capability in sub_capabilities_list:
                    # in case the sub capability is not defined for the capability in the
                    # capabilities sub capabilities map
                    if not sub_capability in self.capabilities_sub_capabilities_map[capability]:
                        # adds the sub capability to the capabilities sub capabilities map for the capability
                        self.capabilities_sub_capabilities_map[capability].append(sub_capability)

    def unregister_plugin_capabilities(self, plugin):
        """
        Unregisters all the available capabilities for the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin to unregister the capabilities.
        """

        # iterates over all the plugin instance capabilities
        for capability in plugin.capabilities:
            # retrieves the capability and super capabilities list
            capability_and_super_capabilites_list = capability_and_super_capabilites(capability)

            # retrieves the capability and super capabilities list length
            capability_and_super_capabilites_list_length = len(capability_and_super_capabilites_list)

            # iterates over the capability and super capabilities list length range
            for capability_or_super_capability_index in range(capability_and_super_capabilites_list_length):
                # retrieves the capability from the capability and super capabilities list
                capability = capability_and_super_capabilites_list[capability_or_super_capability_index]

                # retrieves the sub capabilities list from the the capability and super capabilities list
                sub_capabilities_list = capability_and_super_capabilites_list[capability_or_super_capability_index + 1:]

                # in case the capability exists in the capabilities plugin instances map
                if capability in self.capabilities_plugin_instances_map:
                    # in case the plugin exists in the value for the capability in the
                    # capabilities plugin instances map
                    if plugin in self.capabilities_plugin_instances_map[capability]:
                        # removes the plugin from the capabilities plugin instances map value for
                        # the capability
                        self.capabilities_plugin_instances_map[capability].remove(plugin)

                # in case the capability exists in the capabilities and sub capabilities map
                if capability in self.capabilities_sub_capabilities_map:
                    # iterates over all the sub capabilities in the sub capabilities list
                    for sub_capability in sub_capabilities_list:
                        # in case the sub capability exists the in the capabilities sub capabilities map
                        # for the capability
                        if sub_capability in self.capabilities_sub_capabilities_map[capability]:
                            # in case this is the only instance to be registered with the given sub capability
                            if len(self.capabilities_plugin_instances_map[sub_capability]) == 0:
                                # removes the sub capability from the value of capabilities sub capabilities map
                                # for the given capability
                                self.capabilities_sub_capabilities_map[capability].remove(sub_capability)

    def load_plugin_manager_plugins(self):
        """
        Loads the set of plugin manager plugins.
        """

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # searches for the plugin manager extension type in the plugin capabilities
            if PLUGIN_MANAGER_EXTENSION_TYPE in plugin.capabilities:
                # loads the plugin
                self._load_plugin(plugin, None, PLUGIN_MANAGER_EXTENSION_TYPE)

    def load_startup_plugins(self):
        """
        Loads the set of startup plugins, starting the system bootup process.
        """

        # in case an execution command is defined
        if self.execution_command:
            # returns immediately
            return

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # searches for the startup type in the plugin capabilities
            if STARTUP_TYPE in plugin.capabilities:
                # loads the plugin
                self._load_plugin(plugin, None, STARTUP_TYPE)

    def load_main_plugins(self):
        """
        Loads the set of main plugins, starting the system bootup process.
        """

        # in case an execution command is defined
        if self.execution_command:
            # returns immediately
            return

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # searches for the main type in the plugin capabilities
            if MAIN_TYPE in plugin.capabilities:
                # loads the plugin
                self._load_plugin(plugin, None, MAIN_TYPE)

    def install_signal_handlers(self):
        """
        Installs the signal handlers for the plugin
        manager.
        """

        # installs the sigterm handler for plugin manager kill
        signal.signal(signal.SIGTERM, self._kill_system_signal_handler)

    def notify_load_complete_loaded_plugins(self):
        """
        Notifies the loaded plugins about the load complete.
        """

        # retrieves the loaded plugins list
        loaded_plugins_list = self.get_all_loaded_plugins()

        # iterates over all the loaded plugins
        for loaded_plugin in loaded_plugins_list:
            # notifies the plugin about the load complete
            loaded_plugin.init_complete()

    def notify_load_complete_handlers(self):
        """
        Notifies the init complete handlers about the load complete.
        """

        # iterates over all the init complete handlers
        for init_complete_handler in self.init_complete_handlers:
            init_complete_handler()

    def notify_daemon_file(self):
        """
        Notifies the daemon file, about the finalization
        of the loading of the plugin system.
        """

        # in case the daemon file path is not defined
        if not self.daemon_file_path:
            # returns immediately
            return

        # opens the file in write mode
        file = open(self.daemon_file_path, "wb")

        try:
            # in case the daemon pid is defined
            if self.daemon_pid:
                # sets the pid as the daemon pid
                pid = self.daemon_pid
            else:
                # retrieves the current process pid
                pid = os.getpid()

            # converts the pid to string
            pid_string = str(pid)

            # writes the pid string to the file
            file.write(pid_string)
        finally:
            # closes the file
            file.close()

    def execute_command(self):
        """
        Executes the currently defined execution command (if any).
        """

        # in case an execution command is not defined
        if not self.execution_command:
            # returns immediately
            return

        # splits the execution command stripping every value
        execution_command_splitted = [value.strip() for value in self.execution_command.split(" ", 1)]

        # retrieves both the base and argument values
        base = execution_command_splitted[0]
        argument_values = len(execution_command_splitted) > 1 and execution_command_splitted[1] or None

        # retrieves the arguments splitting them in case the arguments value
        # is not an invalid value
        arguments = argument_values and argument_values.split("$") or []

        # creates the arguments list
        arguments_list = []

        # iterates over the arguments
        for argument in arguments:
            # splits the argument
            argument_split = argument.rsplit("%", 1)

            # retrieves the argument split length
            argument_split_length = len(argument_split)

            # retrieves the argument value from the first
            # element of the argument split
            argument_value = argument_split[0]

            # in case the length of the argument split
            # is two
            if argument_split_length == 2:
                # retrieves the argument type
                argument_type = argument_split[1]

                # in case the argument type is null
                if argument_type == NULL_VALUE:
                    # sets the argument value as none
                    argument_value = None
                else:
                    # retrieves the type converted function
                    type_converter_function = getattr(__builtin__, argument_type)

                    # uses the type converter function to convert the
                    # argument value
                    argument_value = type_converter_function(argument_value)
            elif argument_split_length > 2:
                # raises the invalid argument exception
                raise colony.base.plugin_system_exceptions.InvalidArgument(argument)

            # adds the argument value to the arguments list
            arguments_list.append(argument_value)

        # sets the arguments as the arguments list
        arguments = arguments_list

        # splits the base value
        base_splitted = base.split(":")

        # retrieves the length of the base splitted
        base_splitted_length = len(base_splitted)

        # retrieves the plugin id from the base value
        plugin_id = base_splitted[0]

        # retrieves the name of the method to be called
        method_name = base_splitted_length > 1 and base_splitted[1] or DEFAULT_EXECUTION_HANDLING_METHOD

        # creates the full method name with the plugin id and the method name
        full_method_name = plugin_id + ":" + method_name

        # retrieves the plugin for the plugin id
        plugin = self._get_plugin_by_id(plugin_id)

        try:
            # in case the plugin was not retrieved successfully
            if not plugin:
                # raises the invalid command exception
                raise colony.base.plugin_system_exceptions.InvalidCommand("plugin not found '%s'" % plugin_id)

            # loads the plugin
            self.__load_plugin(plugin)

            # in case the plugin does not have a method with the given name
            if not hasattr(plugin, method_name):
                # raises the invalid command exception
                raise colony.base.plugin_system_exceptions.InvalidCommand("method not found '%s' for plugin '%s'" % (method_name, plugin_id))

            # retrieves the method from the plugin
            method = getattr(plugin, method_name)

            # retrieves the length of the arguments
            argments_length = len(arguments)

            # calculates the expected arguments length
            expected_arguments_length = method.func_code.co_argcount - 1

            # in case the length of the arguments list is different
            # than the expected arguments length
            if not argments_length == expected_arguments_length:
                # raises the invalid command exception
                raise colony.base.plugin_system_exceptions.InvalidCommand("invalid number of arguments for method '%s' (expected %d given %d)" % (full_method_name, expected_arguments_length, argments_length))

            # calls the method with the given arguments
            method(*arguments)
        except Exception, exception:
            # prints an error message
            self.logger.error("Error while executing command: " + unicode(exception))

            # logs the stack trace
            self.log_stack_trace()

            # sets the return code to error
            self.return_code = 1

        # unsets the main loop (disables the loop)
        self.main_loop_active = False

        # unloads the system using no thread safety
        self.unload_system(False)

    def __load_plugin(self, plugin, type = None, loading_type = None):
        """
        Loads the given plugin with the given type and loading type.
        The loading of the plugin consists the loading of the plugin itself (_load_plugin)
        and in the registration of the plugin in all the plugins that allow it.

        @type plugin: Plugin
        @param plugin: The plugin to be loaded.
        @type type: String
        @param type: The type of plugin to be loaded.
        @type loading_type: String
        @param loading_type: The loading type to be used.
        @rtype: bool
        @requires: The result of the plugin load.
        """

        # in case the plugin is loaded
        if plugin.is_loaded():
            return True

        # in case the plugin is lazy loaded
        if (plugin.loading_type == LAZY_LOADING_TYPE and not type == FULL_LOAD_TYPE) and plugin.is_lazy_loaded():
            return True

        # in case the plugin does not pass the test plugin load
        if not self.test_plugin_load(plugin):
            # prints an info message
            self.logger.info("Plugin '%s' v%s not ready to be loaded" % (plugin.short_name, plugin.version))

            # returns false
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

        # injects the plugin in all the plugins that allow
        # one of it's capabilities.
        self.inject_all_allowed(plugin)

        # returns true
        return True

    def _load_plugin(self, plugin, type = None, loading_type = None):
        """
        Loads the given plugin with the given type and loading type.
        The loading of the plugin consists in the test for pre-conditions (dependencies),
        creation of thread (if necessary), loading (if necessary) and injection of dependencies, loading
        of the plugin resources and loading (if necessary) and injection of allowed plugins.

        @type plugin: Plugin
        @param plugin: The plugin to be loaded.
        @type type: String
        @param type: The type of plugin to be loaded.
        @type loading_type: String
        @param loading_type: The loading type to be used.
        @rtype: bool
        @requires: The result of the plugin load.
        """

        # generates the init load plugin event
        self.generate_event("plugin_manager.init_load_plugin", [plugin.id, plugin.version, plugin])

        # in case there is an handler for the plugin loading
        if self.exists_plugin_manager_plugin_execute_conditional("_load_plugin", [plugin, type, loading_type]):
            return self.plugin_manager_plugin_execute_conditional("_load_plugin", [plugin, type, loading_type])

        # in case the return from the handler of the initialization of the plugin load returns false
        if not self.plugin_manager_plugin_execute("init_plugin_load", [plugin, type, loading_type]):
            # returns false
            return False

        # in case the plugin is loaded
        if plugin.is_loaded():
            # returns true
            return True

        # in case the plugin is lazy loaded
        if (plugin.loading_type == LAZY_LOADING_TYPE and not type == FULL_LOAD_TYPE) and plugin.is_lazy_loaded():
            # returns true
            return True

        # in case the plugin load is not successful
        if not self.test_plugin_load(plugin):
            # prints an info message
            self.logger.info("Plugin '%s' v%s not ready to be loaded" % (plugin.short_name, plugin.version))

            # returns false
            return False

        # in case a type is defined
        if type:
            # prints an info message
            self.logger.info("Loading of type: '%s'" % (type))

        # in case the plugin to be loaded is either of type main or thread
        if loading_type == MAIN_TYPE or loading_type == THREAD_TYPE:
            if plugin.id in self.plugin_threads_map:
                # retrieves the available thread for the plugin
                plugin_thread = self.plugin_threads_map[plugin.id]

                # prints an info message
                self.logger.info("Thread restarted for plugin '%s' v%s" % (plugin.short_name, plugin.version))
            else:
                # creates a new tread to run the main plugin
                plugin_thread = PluginThread(plugin)

                # starts the thread
                plugin_thread.start()

                # adds the plugin thread to the plugin threads list
                self.plugin_threads.append(plugin_thread)

                # sets the plugin thread in the plugin threads map
                self.plugin_threads_map[plugin.id] = plugin_thread

                # prints an info message
                self.logger.info("New thread started for plugin '%s' v%s" % (plugin.short_name, plugin.version))

            # sets the plugin load as not completed
            plugin_thread.set_load_complete(False)

            # in case the loading type of the plugin is eager
            if plugin.loading_type == EAGER_LOADING_TYPE or type == FULL_LOAD_TYPE:
                # creates the plugin load event
                event = colony.base.util.Event(LOAD_VALUE)
            else:
                # creates the plugin lazy load event
                event = colony.base.util.Event(LAZY_LOAD_VALUE)

            # adds the load event to the thread queue
            plugin_thread.add_event(event)

            # acquires the ready semaphore for the beginning of the loading process
            plugin.acquire_ready_semaphore()
        else:
            if self.stop_on_cycle_error:
                # in case the loading type of the plugin is eager
                if plugin.loading_type == EAGER_LOADING_TYPE or type == FULL_LOAD_TYPE:
                    # calls the load plugin method in the plugin (plugin bootup process)
                    plugin.load_plugin()
                elif plugin.loading_type == LAZY_LOADING_TYPE:
                    # calls the lazy load plugin method in the plugin (plugin bootup process)
                    plugin.lazy_load_plugin()
            else:
                try:
                    # in case the loading type of the plugin is eager
                    if plugin.loading_type == EAGER_LOADING_TYPE or type == FULL_LOAD_TYPE:
                        # calls the load plugin method in the plugin (plugin bootup process)
                        plugin.load_plugin()
                    elif plugin.loading_type == LAZY_LOADING_TYPE:
                        # calls the lazy load plugin method in the plugin (plugin bootup process)
                        plugin.lazy_load_plugin()
                except BaseException, exception:
                    # sets the exception in the plugin
                    plugin.exception = exception

                    # sets the plugin error state flag
                    plugin.error_state = True

        # in case the plugin is in an error state
        if plugin.error_state:
            # prints the error message
            self.logger.error("Problem loading plugin '%s' v%s '%s'" % (plugin.short_name, plugin.version, unicode(plugin.exception)))

            # returns false in the loading process
            return False

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
            plugin_thread.set_end_load_complete(False)

            # creates the plugin end load event
            event = colony.base.util.Event(END_LOAD_VALUE)

            # adds the end load event to the thread queue
            plugin_thread.add_event(event)

            # acquires the ready semaphore for the beginning of the end loading process
            plugin.acquire_ready_semaphore()
        else:
            if self.stop_on_cycle_error:
                # calls the end load plugin method in the plugin (plugin bootup process)
                plugin.end_load_plugin()
            else:
                try:
                    # calls the end load plugin method in the plugin (plugin bootup process)
                    plugin.end_load_plugin()
                except BaseException, exception:
                    # sets the exception in the plugin
                    plugin.exception = exception

                    # sets the plugin error state flag
                    plugin.error_state = True

        # in case the plugin is in an error state
        if plugin.error_state:
            # prints the error message
            self.logger.error("Problem end loading plugin '%s' v%s '%s'" % (plugin.short_name, plugin.version, unicode(plugin.exception)))

            # returns false in the loading process
            return False

        # injects the allowed plugins into the plugin
        if not self.inject_allowed(plugin):
            return False

        # retrieves the current loading state for the plugin manager
        if self.get_init_complete():
            # notifies the plugin about the load complete
            plugin.init_complete()

        # generates the end load plugin event
        self.generate_event("plugin_manager.end_load_plugin", [plugin.id, plugin.version, plugin])

        # returns true
        return True

    def _unload_plugin(self, plugin, type = None, unloading_type = None):
        """
        Unloads the given plugin with the given type and unloading type.
        The unloading of the plugin consists in the unloading of the dependent plugins,
        notification of the plugins where the plugins is allowed and in the unloading
        of the plugin resources.

        @type plugin: Plugin
        @param plugin: The plugin to be unloaded.
        @type type: String
        @param type: The type of plugin to be unloaded.
        @type loading_type: String
        @param unloading_type: The unloading type to be used.
        @rtype: bool
        @requires: The result of the plugin unload.
        """

        # in case the plugin is not loaded
        if not plugin.is_loaded():
            # returns true
            return True

        # in case a type is defined
        if type:
            # prints an info message
            self.logger.info("Unloading of type: '%s'" % (type))

        # unloads the plugins that depend on the plugin being unloaded
        for dependent_plugin in self.get_plugin_dependent_plugins_map(plugin.id):
            # in case the dependent plugin is loaded
            if dependent_plugin.is_loaded():
                if MAIN_TYPE in dependent_plugin.capabilities:
                    self._unload_plugin(dependent_plugin, DEPENDENCY_TYPE, MAIN_TYPE)
                elif THREAD_TYPE in dependent_plugin.capabilities:
                    self._unload_plugin(dependent_plugin, DEPENDENCY_TYPE, THREAD_TYPE)
                else:
                    self._unload_plugin(dependent_plugin, DEPENDENCY_TYPE)

        # notifies the allowed plugins about the unload
        for allowed_plugin_info in self.get_plugin_allowed_plugins_map(plugin.id):
            # retrieves the allowed plugin
            allowed_plugin = allowed_plugin_info[0]

            # retrieves the allowed capability
            allowed_capability = allowed_plugin_info[1]

            # in case the allowed plugin is loaded
            if allowed_plugin.is_loaded():
                allowed_plugin.unload_allowed(plugin, allowed_capability)

        # clears the map for the dependent plugins
        self.clear_plugin_dependent_plugins_map(plugin.id)

        # clears the map for the allowed plugins
        self.clear_plugin_allowed_plugins_map(plugin.id)

        # clears the map for the capabilities plugins
        self.clear_capabilities_plugins_map_for_plugin(plugin.id)

        # if it's a main or thread type unload
        if unloading_type == MAIN_TYPE or unloading_type == THREAD_TYPE:
            # retrieves the available thread for the plugin
            plugin_thread = self.plugin_threads_map[plugin.id]

            # sets the plugin unload as not completed
            plugin_thread.set_unload_complete(False)

            # creates the plugin unload event
            event = colony.base.util.Event(UNLOAD_VALUE)

            # adds the unload event to the thread queue
            plugin_thread.add_event(event)

            # acquires the ready semaphore for the beginning of the unloading process
            plugin.acquire_ready_semaphore()
        else:
            try:
                # calls the unload plugin method in the plugin (plugin shutdown process)
                plugin.unload_plugin()
            except BaseException, exception:
                # prints the error message
                self.logger.error("There was an exception: %s" % unicode(exception))

                # sets the exception in the plugin
                plugin.exception = exception

                # sets the plugin error state flag
                plugin.error_state = True

        # in case the plugin is in an error state
        if plugin.error_state:
            # prints the error message
            self.logger.error("Problem unloading plugin '%s' v%s '%s'" % (plugin.short_name, plugin.version, unicode(plugin.exception)))

            # returns false in the unloading process
            return False

        # if it's a main or thread type unload
        if unloading_type == MAIN_TYPE or unloading_type == THREAD_TYPE:
            # retrieves the available thread for the plugin
            plugin_thread = self.plugin_threads_map[plugin.id]

            # sets the plugin end unload as not completed
            plugin_thread.set_end_unload_complete(False)

            # creates the plugin end unload event
            event = colony.base.util.Event(END_UNLOAD_VALUE)

            # adds the end unload event to the thread queue
            plugin_thread.add_event(event)

            # acquires the ready semaphore for the beginning of the end unloading process
            plugin.acquire_ready_semaphore()
        else:
            try:
                # calls the end unload plugin method in the plugin (plugin shutdown process)
                plugin.end_unload_plugin()
            except BaseException, exception:
                # sets the exception in the plugin
                plugin.exception = exception

                # sets the plugin error state flag
                plugin.error_state = True

        # in case the plugin is in an error state
        if plugin.error_state:
            # prints the error message
            self.logger.error("Problem end unloading plugin '%s' v%s %s" % (plugin.short_name, plugin.version, unicode(plugin.exception)))

            # returns false in the unloading process
            return False

        # returns true
        return True

    def _unload_thread_plugins(self):
        """
        Unloads all the thread based plugins.
        """

        # creates the exit event
        exit_event = colony.base.util.Event(EXIT_VALUE)

        # iterates over all the available plugin threads
        # joining all the threads
        for plugin_thread in self.plugin_threads:
            # sends the exit event to the plugin thread
            plugin_thread.add_event(exit_event)

            # joins the plugin thread (waiting for the end of it)
            plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)

    def test_plugin_load(self, plugin):
        """
        Tests the given plugin, to check if the loading is possible.

        @type plugin: Plugin
        @param plugin: The plugin to be checked.
        @rtype: bool
        @return: The result of the plugin loading check.
        """

        # in case the plugin does not pass the test plugin load execution
        # in the plugin system
        if not self.plugin_manager_plugin_execute("test_plugin_load", [plugin]):
            return False

        # retrieves the plugin id
        plugin_id = plugin.id

        # retrieves the plugin short name
        plugin_short_name = plugin.short_name

        # retrieves the plugin version
        plugin_version = plugin.version

        # tests the plugin against the current platform
        if not self.test_platform_compatible(plugin):
            # prints an info message
            self.logger.info("Current platform (%s) not compatible with plugin '%s' v%s" % (self.platform, plugin_short_name, plugin_version))

            # returns false
            return False

        # tests the plugin for the availability of the dependencies
        if not self.test_dependencies_available(plugin):
            # prints an info message
            self.logger.info("Missing dependencies for plugin '%s' v%s" % (plugin_short_name, plugin_version))

            # returns false
            return False

        # in case the plugin id does not exists in the loaded plugins map
        if not plugin_id in self.loaded_plugins_map:
            # returns false
            return False

        # returns true
        return True

    def test_dependencies_available(self, plugin):
        """
        Tests if the dependencies for the given plugin are available.

        @type plugin: Plugin
        @param plugin: The plugin to be tested for dependencies.
        @rtype: bool
        @return: The result of the plugin dependencies available check.
        """

        # retrieves the plugin dependencies
        plugin_dependencies = plugin.dependencies

        # iterates over all the plugin dependencies
        for plugin_dependency in plugin_dependencies:

            # in case the test dependency tests fails
            if not plugin_dependency.test_dependency(self):
                # prints an info message
                self.logger.info("Problem with dependency for plugin '%s' v%s" % (plugin.short_name, plugin.version))

                # returns false
                return False

        # returns true
        return True

    def test_platform_compatible(self, plugin):
        """
        Tests if the current platform is compatible with the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin to be tested for platform compatibility.
        @rtype: bool
        @return: The result of the plugin platform compatibility check.
        """

        # retrieves the plugin platforms list
        plugin_platforms_list = plugin.platforms

        # in case the current platform is in the
        # plugin platforms list
        if self.platform in plugin_platforms_list:
            # returns true
            return True
        # otherwise
        else:
            # returns false
            return False

    def resolve_capabilities(self, plugin):
        """
        Resolves the plugin capabilities, adding the plugin to the internal
        structures representing the association between capabilities and plugin
        instances.

        @type plugin: Plugin
        @param plugin: The plugin to have the capabilities resolved.
        @rtype: bool
        @return: The result of the resolution.
        """

        # adds itself to the map of plugins that have a given capability
        for plugin_capability_allowed in plugin.capabilities_allowed:
            self.add_capabilities_plugins_map(plugin_capability_allowed, plugin)

        # returns true
        return True

    def inject_dependencies(self, plugin):
        """
        Injects the dependencies into the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin to haven the dependencies injected.
        @rtype: bool
        @return: The result of the injection.
        """

        # gets all the dependencies of the plugin
        plugin_dependencies = plugin.dependencies

        # iterates over all the dependencies of the plugin
        for plugin_dependency in plugin_dependencies:
            # in case the dependency is of type plugin dependency
            if plugin_dependency.__class__ == PluginDependency:
                # retrieves the dependency plugin instances (by id and version)
                dependency_plugin_instance = self._get_plugin_by_id_and_version(plugin_dependency.plugin_id, plugin_dependency.plugin_version)

                # in case the loading of the dependency plugin was not successful
                if not self.__load_plugin(dependency_plugin_instance, DEPENDENCY_TYPE):
                    # returns false
                    return False

                # in case the dependency plugin isntance is valid
                if dependency_plugin_instance:
                    # calls the dependency inject method in the plugin
                    # with the dependency plugin instances
                    plugin.dependency_injected(dependency_plugin_instance)

                    # adds the plugin to the plugin dependent plugins map for
                    # the plugin dependency id
                    self.add_plugin_dependent_plugins_map(plugin_dependency.plugin_id, plugin)

        # returns true
        return True

    def inject_allowed(self, plugin):
        """
        Injects all the allowed plugins for the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin to inject the allowed plugins.
        """

        # gets all the capabilities allowed of the plugin
        plugin_capabilities_allowed = plugin.capabilities_allowed

        # iterates over all the capabilities of the plugin
        for plugin_capability_allowed in plugin_capabilities_allowed:
            # retrieves the plugin capability allowed type
            plugin_capability_allowed_type = type(plugin_capability_allowed)

            # in case the plugin capability allowed type is tuple
            if plugin_capability_allowed_type == types.TupleType:
                # retrieves the plugin capability allowed string and diffusion policy
                plugin_capability_allowed_string, _diffusion_policy = plugin_capability_allowed
            else:
                # sets the plugin capability allowed string as
                # the plugin capability allowed value
                plugin_capability_allowed_string = plugin_capability_allowed

            # gets all the plugins of the defined capability
            allowed_plugins = self._get_plugins_by_capability_cache(plugin_capability_allowed_string)

            # iterates over all the plugins of the defined capability
            for allowed_plugin in allowed_plugins:
                # loads the plugin (if necessary) with allowed type
                if self.__load_plugin(allowed_plugin, ALLOWED_TYPE):
                    # injects the allowed plugin in the plugin with the given capability
                    self._inject_allowed(plugin, allowed_plugin, plugin_capability_allowed)

        # returns true
        return True

    def _inject_allowed(self, plugin, allowed_plugin, capability):
        """
        Injects the given allowed plugin in the given plugin for the
        given capability.

        @type plugin: Plugin
        @param plugin: The plugin to have the allowed plugin injected.
        @type allowed_plugin: Plugin
        @param allowed_plugin: The plugin to be injected as allowed in the plugin.
        @type capability: String/Tuple
        @param capability: The capability for witch the allowed plugin is being injected.
        """

        # in case both the plugin and the allowed plugins are valid and
        # the allowed plugin is not already "allowed" in the plugin
        # for the current capability
        if plugin and allowed_plugin and not (allowed_plugin, capability) in plugin.allowed_loaded_capability:
            # retrieves the capability type
            capability_type = type(capability)

            # in case the capability type is tuple
            if capability_type == types.TupleType:
                # retrieves the real capability and diffusion policy
                capability, diffusion_policy = capability

                # in case the diffusion policy is same diffusion scope
                if diffusion_policy == SAME_DIFFUSION_SCOPE:
                    # in case the allowed plugin id already exists in the diffusion scope
                    if allowed_plugin.id in self.diffusion_scope_loaded_plugins_map[plugin.diffusion_scope]:
                        allowed_plugin = self.diffusion_scope_loaded_plugins_map[plugin.diffusion_scope][allowed_plugin.id]
                    else:
                        # prints an info message
                        self.logger.info("Creating allowed plugin '%s' v%s as same diffusion scope" % (allowed_plugin.id, allowed_plugin.version))

                        # creates a new allowed plugin (in a the same diffusion scope as the plugin)
                        allowed_plugin = self._create_plugin(allowed_plugin.id, allowed_plugin.version, plugin.diffusion_scope)

                    # loads the allowed plugin (if necessary) with allowed type
                    self.__load_plugin(allowed_plugin, ALLOWED_TYPE)
                # in case the diffusion policy is new diffusion scope
                elif diffusion_policy == NEW_DIFFUSION_SCOPE:
                    # prints an info message
                    self.logger.info("Creating allowed plugin '%s' v%s as new diffusion scope" % (allowed_plugin.id, allowed_plugin.version))

                    # creates a new allowed plugin (in a new diffusion scope)
                    allowed_plugin = self.create_plugin(allowed_plugin.id, allowed_plugin.version)

                    # loads the allowed plugin (if necessary) with allowed type
                    self.__load_plugin(allowed_plugin, ALLOWED_TYPE)

            # calls the load allowed in the plugin with the allowed plugin
            plugin.load_allowed(allowed_plugin, capability)

            # adds the allowed plugin to the allowed plugins map for the given allowed plugin
            # and capability
            self.add_plugin_allowed_plugins_map(allowed_plugin.id, (plugin, capability))

    def inject_all_allowed(self, plugin):
        """
        Injects the plugin in all the plugins that allow one of it's capabilities.

        @type plugin: Plugin
        @param plugin: The plugin to inject in the plugins that allow one of it's capabilities.
        """

        # gets all the capabilities of the plugin
        plugin_capabilities = plugin.capabilities

        # iterates over all of the plugin capabilities
        for plugin_capability in plugin_capabilities:
            capability_plugins = self.get_capabilities_plugins_map(plugin_capability)

            for capability_plugin in capability_plugins:
                if capability_plugin.is_loaded():
                    self._inject_allowed(capability_plugin, plugin, plugin_capability)

    def set_plugin_instance_diffusion_scope_loaded_plugins_map(self, diffusion_scope_id, plugin_id, plugin_instance):
        """
        Sets the given plugin instance in the diffusion scope loaded plugins map.

        @type diffusion_scope_id: int
        @param diffusion_scope_id: The diffusion scope id to be used.
        @type plugin_id: String
        @param plugin_id: The plugin id to be used.
        @type plugin_instance: Plugin
        @param plugin_instance: The plugin instance to be set.
        """

        # in case the diffusion scope id does not exist in the diffusion scope loaded plugins map
        if not diffusion_scope_id in self.diffusion_scope_loaded_plugins_map:
            # sets the diffusion scope id in the diffusion scope
            # loaded plugins map as an empty map
            self.diffusion_scope_loaded_plugins_map[diffusion_scope_id] = {}

        # sets the plugin instance in the diffusion scope loaded plugins map for the diffusion scope id
        # and plugin id
        self.diffusion_scope_loaded_plugins_map[diffusion_scope_id][plugin_id] = plugin_instance

    def unset_plugin_instance_diffusion_scope_loaded_plugins_map(self, diffusion_scope_id, plugin_id):
        """
        Unsets the given plugin instance in the diffusion scope loaded plugins map.

        @type diffusion_scope_id: int
        @param diffusion_scope_id: The diffusion scope id to be used.
        @type plugin_id: String
        @param plugin_id: The plugin id to be used.
        """

        # unsets the plugin instance in the diffusion scope loaded plugins map for the diffusion scope id
        # and plugin id
        del self.diffusion_scope_loaded_plugins_map[diffusion_scope_id][plugin_id]

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
        """
        Adds a plugin to the capabilities plugins map.

        @type plugin: Plugin
        @param plugin: The plugin to be added to the capabilities plugins map.
        @type capability: String
        @param capability: The capability to be used as key in the
        capabilities plugins map.
        """

        # in case the capability does not exist in the
        # capabilities plugins map
        if not capability in self.capabilities_plugins_map:
            # sets an empty list as value for the capability in
            # the capabilities plugins map
            self.capabilities_plugins_map[capability] = []

        # adds the plugin to the capabilities plugins map for the given
        # capability
        self.capabilities_plugins_map[capability].append(plugin)

    def get_capabilities_plugins_map(self, capability):
        """
        Retrieves the list of plugins for the given capability, according
        to the capabilities plugins map.

        @type capability: String
        @param capability: The capability to retrieve the list of plugins.
        @rtype: List
        @return: The list of plugins for the given capability.
        """

        # in case the capability exists in the capabilities plugins map
        if capability in self.capabilities_plugins_map:
            # returns the list of plugins for the given capability, from
            # the capabilities plugins map
            return self.capabilities_plugins_map[capability]
        # otherwise
        else:
            # returns an empty list
            return []

    def clear_capabilities_plugins_map(self, capability):
        """
        Clears the capabilities plugins map, for the given capability.

        @type capability: String
        @param capability: The capability to be used to clear the capabilities
        plugins map.
        """

        self.capabilities_plugins_map[capability] = []

    def clear_capabilities_plugins_map_for_plugin(self, plugin_id):
        """
        Clears the capabilities plugins map, for the given plugin id.

        @type plugin_id: String
        @param plugin_id: The plugin id to be used to clear the capabilities
        plugins map.
        """

        # retrieves the plugin using the id
        plugin = self._get_plugin_by_id(plugin_id)

        for plugin_capability_allowed in plugin.capabilities_allowed:
            if plugin_capability_allowed in self.capabilities_plugins_map:
                capability_plugins = self.capabilities_plugins_map[plugin_capability_allowed]
                if plugin in capability_plugins:
                    capability_plugins.remove(plugin)

    def load_plugin(self, plugin_id, type = None):
        """
        Loads a plugin for the given plugin id and type.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be loaded.
        @type type: String
        @param type: The type of plugin to be loaded.
        @rtype: bool
        @return: The result of the load.
        """

        # retrieves the plugin using the id
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

        # returns true
        return True

    def unload_plugin(self, plugin_id, type = None):
        """
        Unloads a plugin for the given plugin id and type.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be unloaded.
        @type type: String
        @param type: The type of plugin to be unloaded.
        @rtype: bool
        @return: The result of the unload.
        """

        # retrieves the plugin using the id
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

        return True

    def get_all_plugins(self):
        """
        Retrieves all the started plugin instances.

        @rtype: List
        @return: The list with all the started plugin instances.
        """

        return self.plugin_instances

    def get_all_loaded_plugins(self):
        """
        Retrieves all the loaded plugin instances.

        @rtype: List
        @return: The list with all the loaded plugin instances.
        """

        # creates the loaded plugins instances list
        loaded_plugins_instances = []

        # iterates over all the plugin instances
        for plugin_instance in self.plugin_instances:
            # in case the plugin instance is loaded
            if plugin_instance.is_loaded():
                # adds the plugin instance to the loaded plugins instances list
                loaded_plugins_instances.append(plugin_instance)

        # returns the loaded plugins instances
        return loaded_plugins_instances

    def get_plugin(self, plugin):
        """
        Retrieves a plugin and loads it if necessary.

        @type plugin: Plugin
        @param plugin: The plugin to retrieve.
        @rtype: Plugin
        @return: The retrieved plugin.
        """

        # in case the plugin is not loaded
        if not plugin.is_loaded():
            # loads the plugin
            self._load_plugin(plugin)

        # returns the (loaded) plugin
        return plugin

    def get_plugin_by_id(self, plugin_id):
        """
        Retrieves an instance of a plugin with the given id.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve.
        @rtype: Plugin
        @return: The plugin with the given id.
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            return self.get_plugin(plugin)

    def _get_plugin_by_id(self, plugin_id):
        """
        Retrieves an instance (not verified to be loaded) of a plugin with the given id.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve.
        @rtype: Plugin
        @return: The plugin with the given id.
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            return plugin

    def get_plugin_by_id_and_version(self, plugin_id, plugin_version):
        """
        Retrieves an instance of a plugin with the given id and version.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to retrieve.
        @rtype: Plugin
        @return: The plugin with the given id and version.
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            if plugin.version == plugin_version:
                return self.get_plugin(plugin)

    def _get_plugin_by_id_and_version(self, plugin_id, plugin_version):
        """
        Retrieves an instance (not verified to be loaded) of a plugin with the given id and version.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to retrieve.
        @rtype: Plugin
        @return: The plugin with the given id and version.
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            if plugin.version == plugin_version:
                return plugin

    def get_plugins_by_capability(self, capability):
        """
        Retrieves all the plugins with the given capability and sub capabilities.

        @type capability: String
        @param capability: The capability of the plugins to retrieve.
        @rtype: List
        @return: The list of plugins for the given capability and sub capabilities.
        """

        # the results list
        result = []

        # the capability converted to internal capability structure
        capability_structure = Capability(capability)

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # retrieves the plugin capabilities structure
            plugin_capabilities_structure = convert_to_capability_list(plugin.capabilities)

            # iterates over all the plugin capabilities structure
            for plugin_capability_structure in plugin_capabilities_structure:
                # in case the plugin capability structure is capability is sub
                # capability of the capability structure
                if capability_structure.is_capability_or_sub_capability(plugin_capability_structure):
                    # adds the plugin to the results list
                    result.append(self.get_plugin(plugin))

        # returns the results list
        return result

    def _get_plugins_by_capability_cache(self, capability):
        """
        Retrieves all the plugins (not verified to be loaded) with the given capability and sub capabilities (using cache system).

        @type capability: String
        @param capability: The capability of the plugins to retrieve.
        @rtype: List
        @return: The list of plugins for the given capability and sub capabilities.
        """

        # the results list
        result = []

        # in case the capability does not exist in the capabilities sub capabilities map
        if not capability in self.capabilities_sub_capabilities_map:
            # returns the result (empty list)
            return result

        # retrieves the capability and sub capabilities list for the current capability
        capability_and_sub_capabilities_list = [capability] + self.capabilities_sub_capabilities_map[capability]

        # iterates over all the capabilities (or sub capabilities) in the
        # capability and sub capabilities list
        for capability_or_sub_capability in capability_and_sub_capabilities_list:
            # retrieves the plugin instances that have the given capability
            plugin_instances = self.capabilities_plugin_instances_map[capability_or_sub_capability]

            # adds the plugin instances to the result
            result += plugin_instances

        # returns the result
        return result

    def _get_plugins_by_capability(self, capability):
        """
        Retrieves all the plugins (not verified to be loaded) with the given capability and sub capabilities.

        @type capability: String
        @param capability: The capability of the plugins to retrieve.
        @rtype: List
        @return: The list of plugins for the given capability and sub capabilities.
        """

        # the results list
        result = []

        # the capability converter to internal capability structure
        capability_structure = Capability(capability)

        for plugin in self.plugin_instances:
            plugin_capabilities_structure = convert_to_capability_list(plugin.capabilities)

            for plugin_capability_structure in plugin_capabilities_structure:
                if capability_structure.is_capability_or_sub_capability(plugin_capability_structure):
                    result.append(plugin)

        return result

    def __get_plugins_by_capability(self, capability):
        """
        Retrieves all the plugins with the given capability.

        @type capability: String
        @param capability: The capability of the plugins to retrieve.
        @rtype: List
        @return: The list of plugins for the given capability.
        """

        # the results list
        result = []
        for plugin in self.plugin_instances:
            if capability in plugin.capabilities:
                result.append(self.get_plugin(plugin))
        return result

    def get_plugins_by_capability_allowed(self, capability_allowed):
        """
        Retrieves all the plugins with the given allowed capability and sub capabilities.

        @type capability_allowed: String
        @param capability_allowed: The capability allowed of the plugins to retrieve.
        @rtype: List
        @return: The list of plugins for the given capability allowed.
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
        Retrieves all the plugins (not verified to be loaded) with the given allowed capability and sub capabilities.

        @type capability_allowed: String
        @param capability_allowed: The capability allowed of the plugins to retrieve.
        @rtype: List
        @return: The list of plugins for the given capability allowed.
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
        Retrieves all the plugins with a dependency with the given plugin id.

        @type plugin_id: String
        @param plugin_id: The id of the plugin dependency.
        @rtype: List
        @return: The list of plugins with a dependency with the given plugin id.
        """

        # the results list
        result = []

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # iterates over all the plugin dependencies
            for dependency in plugin.dependencies:
                # in case the dependency is of type plugin dependency
                if dependency.__class__ == PluginDependency:
                    # in case the dependency plugin id is the same
                    if dependency.plugin_id == plugin_id:
                        # appends the plugin to the result
                        result.append(self.get_plugin(plugin))
        return result

    def _get_plugins_by_dependency(self, plugin_id):
        """
        Retrieves all the plugins (not verified to be loaded) with a dependency
        with the given plugin id.

        @type plugin_id: String
        @param plugin_id: The id of the plugin dependency.
        @rtype: List
        @return: The list of plugins with a dependency with the given plugin id.
        """

        # the results list
        result = []

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # iterates over all the plugin dependencies
            for dependency in plugin.dependencies:
                # in case the dependency is of type plugin dependency
                if dependency.__class__ == PluginDependency:
                    # in case the dependency plugin id is the same
                    if dependency.plugin_id == plugin_id:
                        # appends the plugin to the result
                        result.append(plugin)

        # returns the result
        return result

    def get_plugins_allow_capability(self, capability):
        """
        Retrieves all the plugins that allow the given capability.

        @type capability: String
        @param capability: The capability to be tested.
        @rtype: List
        @return: The list of plugins that allow the given capability.
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
        Retrieves all the plugins (not verified to be loaded) that allow the given capability.

        @type capability: String
        @param capability: The capability to be tested.
        @rtype: List
        @return: The list of plugins that allow the given capability.
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

    def resolve_file_path(self, file_path, not_found_valid = False, create_path = False):
        """
        Resolves the given file path, substituting the given commands
        in the file path for the "real" values, and returning the best
        file path of the possible file paths.

        @type file_path: String
        @param file_path: The base file path to be used as substitution
        base.
        @type not_found_valid: bool
        @param not_found_valid: If a file path should be returned even if
        the path is not found.
        @type create_path: bool
        @param create_path: If the file path should be created in case it
        does not exists.
        @rtype: String
        @return: The best file path of the possible file paths.
        """

        # retrieves the string values list from the file path
        string_values_list = self.resolve_string_value(file_path)

        # in case the string values list
        # is invalid
        if not string_values_list:
            # returns invalid
            return None

        # iterates over all the string values in
        # the string values list
        for string_value in string_values_list:
            # in case the paths exists
            if os.path.exists(string_value):
                # returns the string value
                return string_value

        # in case the not found valid flag is
        # active, the first result should be returned
        if not_found_valid:
            # sets the string value as the first
            # string value
            string_value = string_values_list[0]

            # in case the create path flag is set
            if create_path:
                # retrieves the string value directory
                string_value_directory = os.path.dirname(string_value)

                # in case the path does not exists
                if not os.path.exists(string_value_directory):
                    # creates the directories
                    os.makedirs(string_value_directory)

            # returns the string value
            return string_value

    def resolve_string_value(self, string_value):
        """
        Resolves the given string value, substituting the given commands
        in the file path for the "real" values, and returning the list
        of possible string values, ordered by priority.

        @type string_value: String
        @param string_value: The base string value to be used as substitution
        base.
        @rtype: List
        @return: The list of possible string values, ordered by priority.
        """

        # in case the string value is invalid
        # (empty or none)
        if not string_value:
            # returns an empty list
            return []

        # finds all the matches using the special value regex
        # over the string value
        special_value_matches = SPECIAL_VALUE_REGEX.finditer(string_value)

        # creates the value tuples list
        values_tuples_list = []

        # iterates over all the special values matches
        for special_value_match in special_value_matches:
            # retrieves the command and the argument for the current match
            command = special_value_match.group(COMMAND_VALUE)
            arguments = special_value_match.group(ARGUMENTS_VALUE)

            # in case the arguments are defined
            if arguments:
                # splits the arguments value
                arguments_splitted = arguments.split(",")
            # otherwise
            else:
                # sets the arguments splitted as an empty list
                arguments_splitted = []

            # retrieves the process method for the current command
            process_method = getattr(self, PROCESS_COMMAND_METHOD_PREFIX + command)

            # runs the process method with the arguments
            # retrieving the values
            values = process_method(arguments_splitted)

            # retrieves the start and end position of the match
            start_position = special_value_match.start()
            end_position = special_value_match.end()

            # creates the values tuple with the start and end position
            # and with the values
            values_tuple = (start_position, end_position, values)

            # adds the value tuple to the value tuples list
            values_tuples_list.append(values_tuple)

        # creates the string buffers list with the initial string
        # buffer in it
        string_buffers_list = [colony.libs.string_buffer_util.StringBuffer()]

        # initializes the current index
        current_index = 0

        # iterates over all the value tuples in
        # the value tuples list
        for values_tuple in values_tuples_list:
            # unpacks the tuple retrieving the start position
            # the end position and the values
            start_position, end_position, values = values_tuple

            # retrieves the previous value (the value before the the substitution)
            previous_value = string_value[current_index:start_position]

            # retrieves the values type
            values_type = type(values)

            # creates the new string buffers list
            new_string_buffers_list = []

            # iterates over all the string buffers in
            # the string buffers list
            for string_buffer in string_buffers_list:
                # writes the previous value into
                # the string buffer
                string_buffer.write(previous_value)

                # in case the values is a string
                if values_type in types.StringTypes:
                    # writes the values (simple string) into
                    # the string buffer
                    string_buffer.write(values)
                # otherwise it must be a list and must be processed
                # as such
                else:
                    # retrieves the values length
                    values_length = len(values)

                    # retrieves the first value
                    first_value = values[0]

                    # iterates over the range of values minus one
                    for index in range(values_length - 1):
                        # retrieves the current value
                        current_value = values[index + 1]

                        # creates the new string buffer as a duplicate
                        new_string_buffer = string_buffer.duplicate()
                        new_string_buffer.write(current_value)
                        new_string_buffers_list.append(new_string_buffer)

                    # writes the first value into the string buffer
                    string_buffer.write(first_value)

            # extends the string buffers list with the "new" string
            # buffers list
            string_buffers_list.extend(new_string_buffers_list)

            # updates the current index with the end position
            current_index = end_position

        # retrieves the next value
        next_value = string_value[current_index:]

        # iterates over all the string buffer in the
        # string buffers list
        for string_buffer in string_buffers_list:
            # writes the next value into
            # the string buffer
            string_buffer.write(next_value)

        # converts the various string buffers into values to create
        # the string values list
        string_values_list = [value.get_value() for value in string_buffers_list]

        # returns the string values list
        return string_values_list

    def get_plugin_path_by_id(self, plugin_id):
        """
        Retrieves the plugin execution path for the given plugin id.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the execution path.
        @rtype: String
        @return: The plugin execution path for the plugin with the given id.
        """

        # in case the plugin id exists in the
        # plugin dirs map
        if plugin_id in self.plugin_dirs_map:
            # returns the value of the plugin id
            # in the plugin dirs map (plugin path)
            return self.plugin_dirs_map[plugin_id]

    def get_temporary_plugin_path_by_id(self, plugin_id, extra_path = ""):
        """
        Retrieves the temporary plugin path for the given plugin id.
        The path may refer a directory that is not created.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the temporary
        plugin path.
        @type: extra_path
        @param extra_path: The extra path to be appended.
        @rtype: String
        @return: The temporary plugin path for the given plugin id.
        """

        # retrieves the current temporary directory
        temporary_directory = tempfile.gettempdir()

        # creates the temporary plugin path
        temporary_plugin_path = temporary_directory + "/" + COLONY_VALUE + "/" + plugin_id + "/" + extra_path

        # normalizes the temporary plugin path
        normalized_temporary_plugin_path = colony.libs.path_util.normalize_path(temporary_plugin_path)

        # returns the normalized temporary plugin path
        return normalized_temporary_plugin_path

    def get_temporary_plugin_generated_path_by_id(self, plugin_id):
        """
        Retrieves the temporary plugin generated path for the given plugin id.
        The path may refer a directory that is not created.
        The generated path is affected by a random value and should be unique.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the temporary
        plugin generated path.
        @rtype: String
        @return: The temporary plugin generated path for the given plugin id.
        """

        # retrieves the temporary plugin path
        temporary_plugin_path = self.get_temporary_plugin_path_by_id(plugin_id)

        # retrieves the current time value (current time multiplied by a
        # factor of four) in integer
        current_time_value = int(time.time() * 10000)

        # creates the (final) temporary plugin path generated for the current time value
        temporary_plugin_generated_path = temporary_plugin_path + "/" + str(current_time_value)

        # normalizes the temporary plugin generated path
        normalized_temporary_plugin_generated_path = colony.libs.path_util.normalize_path(temporary_plugin_generated_path)

        # returns the normalized temporary plugin generated path
        return normalized_temporary_plugin_generated_path

    def get_plugin_configuration_paths_by_id(self, plugin_id):
        """
        Retrieves the plugin configuration paths for the given plugin id.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the configuration paths.
        @rtype: List
        @return: The plugin configuration paths for the plugin with the given id.
        """

        # retrieves the current configuration path
        configuration_path = self.get_configuration_path()

        # retrieves the current workspace path
        workspace_path = self.get_workspace_path()

        return (configuration_path + "/" + plugin_id, workspace_path + "/" + plugin_id)

    def get_plugin_configuration_file_by_id(self, plugin_id, configuration_file_path):
        """
        Retrieves the plugin configuration file for the given plugin id
        and configuration file path.

        @type plugin_id: String
        @param plugin_id: The plugin id to be used in the configuration
        file retrieval.
        @type configuration_file_path: String
        @param configuration_file_path: The path of the configuration file (relative to
        the base of the plugin configuration path).
        @rtype: File
        @return: The configuration file retrieved.
        """

        # retrieves the configuration paths for the plugin
        plugin_configuration_paths = self.get_plugin_configuration_paths_by_id(plugin_id)

        # iterates over all the plugin configuration paths, to check
        # if the configuration file exists in any of the paths
        for plugin_configuration_path in plugin_configuration_paths:
            # creates the configuration file full path from the configuration
            # file and the configuration file path
            configuration_file_full_path = plugin_configuration_path + "/" + configuration_file_path

            # in case the configuration file full path exists
            if os.path.exists(configuration_file_full_path):
                # opens the configuration file
                configuration_file = open(configuration_file_full_path)

                # returns the configuration file
                return configuration_file

    def get_plugin_module_name_by_id(self, plugin_id):
        """
        Retrieves the plugin module name for the given plugin id.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the plugin module name.
        @rtype: String
        @return: The plugin module name for the given plugin id.
        """

        # retrieves the plugin (by id)
        plugin = self._get_plugin_by_id(plugin_id)

        # in case the plugin is valid
        if plugin:
            # returns the plugin module
            return plugin.__module__

    def get_plugin_by_module_name(self, module):
        """
        Retrieves an instance of a plugin for the given plugin module name.

        @type module: String
        @param module: The plugin module name to retrieve.
        @rtype: Plugin
        @return: The plugin for the given plugin module name.
        """

        # retrieves all the plugins
        plugins = self.get_all_plugins()

        # iterates over all the plugins
        for plugin in plugins:
            # retrieves the plugin module
            plugin_module = plugin.__module__

            # in case the plugin module is the same as the given
            if plugin_module == module:
                # returns the plugin
                return plugin

    def get_loaded_plugin_by_module_name(self, module):
        """
        Retrieves an instance of a loaded plugin for the given plugin module name.

        @type module: String
        @param module: The loaded plugin module name to retrieve.
        @rtype: Plugin
        @return: The loaded plugin for the given plugin module name.
        """

        loaded_plugins = self.get_all_loaded_plugins()

        for loaded_plugin in loaded_plugins:
            plugin_module = loaded_plugin.__module__

            if plugin_module == module:
                return loaded_plugin

    def get_plugin_class_by_module_name(self, module):
        """
        Retrieves a the plugin class for the given plugin module name.

        @type module: String
        @param module: The plugin module name to retrieve.
        @rtype: Class
        @return: The plugin class for the given plugin module name.
        """

        for plugin in self.loaded_plugins:
            plugin_module = plugin.__module__

            if plugin_module == module:
                return plugin

    def register_plugin_manager_event(self, plugin, event_name):
        """
        Registers a given plugin manager event in the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin containing the handler to the event.
        @type event_name: String
        @param event_name: The name of the event to be registered.
        """

        if not event_name in self.event_plugins_handled_loaded_map:
            self.event_plugins_handled_loaded_map[event_name] = []

        if not plugin in self.event_plugins_handled_loaded_map[event_name]:
            self.event_plugins_handled_loaded_map[event_name].append(plugin)

            # prints an info message
            self.logger.info("Registering event '%s' from '%s' v%s in plugin manager" % (event_name, plugin.short_name, plugin.version))

    def unregister_plugin_manager_event(self, plugin, event_name):
        """
        Unregisters a given plugin manager event in the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin containing the handler to the event.
        @type event_name: String
        @param event_name: The name of the event to be unregistered.
        """

        if event_name in self.event_plugins_handled_loaded_map:
            if plugin in self.event_plugins_handled_loaded_map[event_name]:
                self.event_plugins_handled_loaded_map[event_name].remove(plugin)

                # prints an info message
                self.logger.info("Unregistering event '%s' from '%s' v%s in plugin manager" % (event_name, plugin.short_name, plugin.version))

    def notify_handlers(self, event_name, event_args):
        """
        Notifies all the handlers for the event with the given name with the give arguments.

        @type event_name: String
        @param event_name: The name of the event to be notified.
        @type event_args: List
        @param event_args: The arguments to be passed to the handler.
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
        Generates an event and starts the process of handler notification.

        @type event_name: String
        @param event_name: The name of the event to be notified.
        @type event_args: List
        @param event_args: The arguments to be passed to the handler.
        """

        # prints an info message
        self.logger.info("Event '%s' generated in plugin manager" % (event_name))

        # notifies the event handlers of the event name with the event arguments
        self.notify_handlers(event_name, event_args)

    def plugin_manager_plugin_execute(self, execution_type, arguments):
        """
        Executes a plugin manager call in all the plugin manager plugins with
        the defined execution type capability.

        @type execution_type: String
        @param execution_type: The type of execution.
        @type arguments: List
        @param arguments: The list of arguments for the execution.
        @rtype: bool
        @return: The boolean result of the AND operation between the call results.
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
        the defined execution type capability (the execution is conditional).

        @type execution_type: String
        @param execution_type: The type of execution.
        @type arguments: List
        @param arguments: The list of arguments for the execution.
        @rtype: bool
        @return: The boolean result of the AND operation between the call results.
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

                    # calls the method and retrieves the return value
                    return_value = execute_call(*arguments)

                    # calls the method
                    if not return_value:
                        return False

        return True

    def exists_plugin_manager_plugin_execute_conditional(self, execution_type, arguments):
        """
        Tests all the available plugin manager plugins of the type execution_type
        in the search of one that is available for execution.

        @type execution_type: String
        @param execution_type: The type of execution.
        @type arguments: List
        @param arguments: The list of arguments for the execution.
        @rtype: bool
        @return: The result of the test (if successful or not).
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

        # returns false
        return False

    def log_stack_trace(self):
        """
        Logs the current stack trace to the logger.
        """

        # retrieves the execution information
        _type, _value, traceback_list = sys.exc_info()

        # in case the traceback list is valid
        if traceback_list:
            formated_traceback = traceback.format_tb(traceback_list)
        else:
            formated_traceback = ()

        # iterates over the traceback lines
        for formated_traceback_line in formated_traceback:
            # strips the formated traceback line
            formated_traceback_line_stripped = formated_traceback_line.rstrip()

            # prints an error message with the formated traceback line
            self.logger.error(formated_traceback_line_stripped)

    def print_all_plugins(self):
        """
        Prints all the loaded plugins descriptions.
        """

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # prints the plugin
            print plugin

    def get_environment_variable(self, environment_variable_name):
        """
        Retrieves the environment variable for the given
        environment variable name.

        @type environment_variable_name: String
        @param environment_variable_name: The name of the environment
        variable to be retrieved.
        @rtype: String
        @return: The retrieved environment variable value.
        """

        return os.environ.get(environment_variable_name, "")

    def get_configuration_path(self):
        """
        Retrieves the current configuration path.

        @rtype: String
        @return: The current configuration path.
        """

        return self.manager_path + "/" + self.configuration_path

    def get_workspace_path(self):
        """
        Retrieves the workspace path.

        @rtype: String
        @param: The workspace path.
        """

        # retrieves the workspace path
        return self.workspace_path

    def set_workspace_path(self, workspace_path):
        """
        Sets the workspace path, updating the workspace
        path after the setting.

        @type workspace_path: String
        @param workspace_path: The workspace path.
        """

        # sets the workspace path
        self.workspace_path = workspace_path

        # updates the workspace path
        self.update_workspace_path()

    def set_plugin_manager_timestamp(self, plugin_manager_timestamp = None):
        """
        Sets the timestamp value for the plugin manager.

        @type plugin_manager_timestamp: float
        @param plugin_manager_timestamp: The value to set in the plugin manager as the timestamp,
        used for loading time purposes.
        """

        # in case no plugin manager timestamp is defined
        if not plugin_manager_timestamp:
            # sets the plugin manager timestamp as the current time
            plugin_manager_timestamp = time.time()

        # sets the timestamp
        self.plugin_manager_timestamp = plugin_manager_timestamp

    def set_plugin_manager_plugins_loaded(self, value = True):
        """
        Sets the value for the plugin_manager_plugins_loaded flag.

        @type value: bool
        @param value: The value to set for the plugin_manager_plugins_loaded flag.
        """

        self.plugin_manager_plugins_loaded = value

    def get_plugin_manager_plugins_loaded(self):
        """
        Retrieves the current plugin_manager_plugins_loaded flag value.

        @rtype: bool
        @return: The current plugin_manager_plugins_loaded flag value.
        """

        return self.plugin_manager_plugins_loaded

    def set_init_complete(self, value = True):
        """
        Sets the value for the init_complete flag.

        @type value: bool
        @param value: The value to set for the init_complete flag.
        """

        self.init_complete = value

    def get_init_complete(self):
        """
        Retrieves the current init_complete flag value.

        @rtype: bool
        @return: The current init_complete flag value.
        """

        return self.init_complete

    def get_manager_path(self):
        """
        Retrieves the manager base path for execution.

        @rtype: String
        @return: The manager base path for execution.
        """

        return self.manager_path

    def get_plugin_paths(self):
        """
        Retrieves the manager plugin paths for execution.

        @rtype: List
        @return: The manager plugin paths for execution.
        """

        return self.plugin_paths

    def get_main_plugin_path(self):
        """
        Retrieves the manager main plugin path for execution.

        @rtype: String
        @return: The manager main plugin path for execution.
        """

        # retrieves the manager path
        manager_path = self.get_manager_path()

        # retrieves the plugin paths
        plugin_paths = self.get_plugin_paths()

        # in case the list of plugin paths is
        # valid (contains paths)
        if plugin_paths:
            # retrieves the main plugin path as the first
            # path in the plugin paths
            main_plugin_path = plugin_paths[0]
        else:
            # retrieves the main plugin path
            # as the default plugin path
            main_plugin_path = DEFAULT_PLUGIN_PATH

        # creates the main plugin full path joining the manager path and the
        # main plugin path
        main_plugin_full_path = os.path.join(manager_path, main_plugin_path)

        # returns the main plugin (full) path
        return main_plugin_full_path

    def get_temporary_path(self):
        """
        Retrieves the manager temporary path for execution.

        @rtype: String
        @return: The manager temporary path for execution.
        """

        # retrieves the manager path
        manager_path = self.get_manager_path()

        # creates the main plugin full path joining the manager path and the
        # default temporary path
        temporary_path = os.path.join(manager_path, DEFAULT_TEMPORARY_PATH)

        # returns the temporary path
        return temporary_path

    def get_layout_mode(self):
        """
        Retrieves the current base (plugin manager) layout mode.

        @rtype: String
        @return: The current base (plugin manager) layout mode.
        """

        return self.layout_mode

    def get_run_mode(self):
        """
        Retrieves the current base (plugin manager) run mode.

        @rtype: String
        @return: The current base (plugin manager) run mode.
        """

        return self.run_mode

    def get_version(self):
        """
        Retrieves the current base (plugin manager) version.

        @rtype: String
        @return: The current base (plugin manager) version.
        """

        return colony.base.plugin_system_information.VERSION

    def get_release(self):
        """
        Retrieves the current base (plugin manager) release.

        @rtype: String
        @return: The current base (plugin manager) release.
        """

        return colony.base.plugin_system_information.RELEASE

    def get_build(self):
        """
        Retrieves the current base (plugin manager) build.

        @rtype: String
        @return: The current base (plugin manager) build.
        """

        return colony.base.plugin_system_information.BUILD

    def get_release_date(self):
        """
        Retrieves the current base (plugin manager) release date.

        @rtype: String
        @return: The current base (plugin manager) release date.
        """

        return colony.base.plugin_system_information.RELEASE_DATE

    def get_release_date_time(self):
        """
        Retrieves the current base (plugin manager) release date time.

        @rtype: String
        @return: The current base (plugin manager) release date time.
        """

        return colony.base.plugin_system_information.RELEASE_DATE_TIME

    def get_environment(self):
        """
        Retrieves the current base (plugin manager) environment.

        @rtype: String
        @return: The current base (plugin manager) environment.
        """

        return colony.base.plugin_system_information.ENVIRONMENT

    def echo(self, value = "echo"):
        """
        Returns an echo value.

        @type value: String
        @param value: The value to be echoed.
        @rtype: String
        @return: The echo value.
        """

        return value

    def process_command_manager_path(self, arguments):
        """
        The process command method for the manager path command.

        @type arguments: String
        @param arguments: The arguments to the process command method.
        @rtype: Object
        @return: The result of the command processing.
        """

        return (self.manager_path,)

    def process_command_plugin_path(self, arguments):
        """
        The process command method for the plugin path command.

        @type arguments: String
        @param arguments: The arguments to the process command method.
        @rtype: Object
        @return: The result of the command processing.
        """

        return (self.get_plugin_path_by_id(*arguments),)

    def process_command_configuration(self, arguments):
        """
        The process command method for the configuration command.

        @type arguments: String
        @param arguments: The arguments to the process command method.
        @rtype: Object
        @return: The result of the command processing.
        """

        return self.get_plugin_configuration_paths_by_id(*arguments)

    def process_command_environment(self, arguments):
        """
        The process command method for the configuration command.

        @type arguments: String
        @param arguments: The arguments to the process command method.
        @rtype: Object
        @return: The result of the command processing.
        """

        return (self.get_environment_variable(*arguments),)

    def _kill_system_signal_handler(self, signum, frame):
        """
        Kills the system, due to signal occurrence.

        @type signum: int
        @param signum: The signal number.
        @type frame: Frame
        @type frame: The frame value.
        """

        try:
            # print a warning message
            self.logger.warning("Unloading system due to signal: '%s'" % signum)

            # unloads the system
            self.unload_system(True)

            # print a warning message
            self.logger.warning("Unloaded system due to signal: '%s'" % signum)
        except Exception, exception:
            # prints an error message
            self.logger.error("Problem unloading the system '%s', killing the system..." % unicode(exception))

            # stops the blocking system structures
            self._stop_blocking_system_structures()

            # exits in error
            exit(2)

    def _stop_blocking_system_structures(self):
        """
        Stops all the blocking system structures.
        These blocking structures could create a situation
        where a lock would block the system.
        """

        # stops the kill system timer
        self._stop_kill_system_timer()

    def _stop_kill_system_timer(self):
        """
        Stops the kill system timer, avoiding possible
        locking problems.
        """

        # in case the kill system timer is not defined
        if not self.kill_system_timer:
            # returns immediatly
            return

        # cancels the kill system timer
        self.kill_system_timer.cancel()

    def _kill_system_timeout(self):
        """
        Kills the system, due to unload timeout occurrence.
        """

        # prints an error message
        self.logger.error("Unloading timeout (%.2f seconds) reached, killing the system..." % DEFAULT_UNLOAD_SYSTEM_TIMEOUT)

        # exits in error
        exit(2)

    def _handle_system_exception(self, exception):
        """
        Handles the given system base exception.
        These exception occur at the highest level of the plugin framework.
        The handling is sever and culminates in the unloading of the
        plugin framework.

        @type exception: BaseException
        @param exception: The exception to be handled.
        """

        try:
            # retrieves the exception type
            exception_type = exception.__class__.__name__

            # print a warning message
            self.logger.warning("Unloading system due to exception: '%s' of type '%s'" % (unicode(exception), exception_type))

            # unloads the system
            self.unload_system(False)

            # print a warning message
            self.logger.warning("Unloaded system due to exception: '%s' of type '%s'" % (unicode(exception), exception_type))
        except KeyboardInterrupt, exception:
            # prints an error message
            self.logger.error("Problem unloading the system '%s', killing the system..." % unicode(exception))

            # stops the blocking system structures
            self._stop_blocking_system_structures()

            # exits in error
            exit(2)

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

    diffusion_policy = SINGLETON_DIFFUSION_SCOPE
    """ The diffusion policy """

    def __init__(self, plugin_id = "none", plugin_version = "none", diffusion_policy = SINGLETON_DIFFUSION_SCOPE, mandatory = True, conditions_list = []):
        """
        Constructor of the class.

        @type plugin_id: String
        @param plugin_id: The plugin id.
        @type plugin_version: String
        @param plugin_version: The plugin version.
        @type diffusion_policy: int
        @param diffusion_policy: The diffusion policy.
        @type mandatory: bool
        @param mandatory: The mandatory value.
        @type conditions_list: List
        @param conditions_list: The list of conditions.
        """

        Dependency.__init__(self, mandatory, conditions_list)
        self.plugin_id = plugin_id
        self.plugin_version = plugin_version
        self.diffusion_policy = diffusion_policy

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
            return False

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
        self.package_import_name = package_import_name
        self.package_version = package_version
        self.package_url = package_url

    def __repr__(self):
        """
        Returns the default representation of the class.

        @rtype: String
        @return: The default representation of the class.
        """

        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.package_name,
            self.package_version
        )

    def test_dependency(self, manager):
        """
        Tests the environment for the package dependency and the given plugin manager.

        @type manager: PluginManager
        @param manager: The current plugin manager in use.
        @rtype: bool
        @return: The result of the test (if successful or not).
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
            except ImportError:
                manager.logger.info("Package '%s' v%s does not exist in your system" % (package_name, package_version))
                if not package_url == "none":
                    manager.logger.info("You can download the package at %s" % package_url)

                return False
        elif package_import_name_type == types.ListType:
            for package_import_name_item in package_import_name:
                try:
                    # tries to find (import) the given module
                    __import__(package_import_name_item)
                except ImportError:
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
        @return: The result of the test (if successful or not).
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
        @return: The result of the test (if successful or not).
        """

        if not Condition.test_condition(self):
            return False

        # retrieves the current operative system name
        current_operative_system_name = colony.base.util.get_operative_system()

        # in case the current operative system is the same as the defined in the condition
        if current_operative_system_name == self.operative_system_name:
            return True
        else:
            return False

class Capability:
    """
    Class that describes a neutral structure for a capability.
    """

    list_value = []
    """ The value of the capability described as a list """

    def __init__(self, string_value = None):
        """
        Constructor of the class.

        @type string_value: String
        @param string_value: The capability string value.
        """

        # in case the string value is valid
        if string_value:
            # splits the string value to retrieve the list value
            self.list_value = string_value.split(".")
        else:
            # sets the list value as an empty list
            self.list_value = []

    def __eq__(self, capability):
        # retrieves the list value for self
        list_value_self = self.list_value

        # retrieves the list value for capability
        list_value_capability = capability.list_value

        # in case some of the lists is invalid
        if not list_value_self or not list_value_capability:
            # returns false
            return False

        # retrieves the length of the list value for self
        length_self = len(list_value_self)

        # retrieves the length of the list value for capability
        length_capability = len(list_value_capability)

        # in case the lengths for the list are different
        if not length_self == length_capability:
            # returns false
            return False

        # iterates over all the lists
        for index in range(length_self):
            # compares both values
            if list_value_self[index] != list_value_capability[index]:
                # returns false
                return False

        # returns true
        return True

    def __ne__(self, capability):
        # retrieves the not value of the equals method
        return not self.__eq__(capability)

    def capability_and_super_capabilites(self):
        """
        Retrieves the list of the capability and all super capabilities.

        @rtype: List
        @return: The list of the capability and all super capabilities.
        """

        # creates the capability and super capabilities list
        capability_and_super_capabilites_list = []

        # retrieves the list value
        list_value_self = self.list_value

        # start the current capability value
        curent_capability_value = None

        # iterates over the list of values self
        for value_self in list_value_self:
            # in case the current capability value is valied
            if curent_capability_value:
                # appends the value self and a dot to the current capability value
                curent_capability_value += "." + value_self
            # otherwise (initial iteration)
            else:
                # sets the current capability value as the value self
                curent_capability_value = value_self

            # adds the current capability value to the capability
            # and super capabilities list
            capability_and_super_capabilites_list.append(curent_capability_value)

        # returns the capability and super capabilities list
        return capability_and_super_capabilites_list

    def is_sub_capability(self, capability):
        """
        Tests if the given capability is sub capability.

        @type capability: Capability
        @param capability: The capability to be tested.
        @rtype: bool
        @return: The result of the is sub capability test.
        """

        # retrieves the list value self
        list_value_self = self.list_value

        # retrieves the list value capability
        list_value_capability = capability.list_value

        # in case any of the lists is empty or invalid
        if not list_value_self or not list_value_capability:
            # returns false
            return False

        # retrieves the list value self length
        list_value_self_length = len(list_value_self)

        # retrieves the list value capability length
        list_value_capability_length = len(list_value_capability)

        # in case the list value capability length is less or
        # equal than list value self length
        if list_value_capability_length <= list_value_self_length:
            # returns false
            return False

        # iterates over the list value self range
        for index in range(list_value_self_length):
            # in case the values of each list are different
            if list_value_self[index] != list_value_capability[index]:
                # returns false
                return False

        # returns true
        return True

    def is_capability_or_sub_capability(self, capability):
        """
        Tests if the given capability is a capability or sub capability.

        @type capability: Capability
        @param capability: The capability to be tested.
        @rtype: bool
        @return: The result of the is capability or sub capability test.
        """

        # in case the capability is equal or sub capability
        if self.__eq__(capability) or self.is_sub_capability(capability):
            # returns true
            return True
        # otherwise
        else:
            # returns false
            return False

class Event:
    """
    Class that describes a neutral structure for an event.
    """

    list_value = []
    """ The value of the event described as a list """

    def __init__(self, string_value = None):
        """
        Constructor of the class.

        @type string_value: String
        @param string_value: The event string value.
        """

        # in case the string value is valid
        if string_value:
            # splits the string value to retrieve the list value
            self.list_value = string_value.split(".")
        else:
            # sets the list value as an empty list
            self.list_value = []

    def __eq__(self, event):
        # retrieves the list value for self
        list_value_self = self.list_value

        # retrieves the list value for event
        list_value_event = event.list_value

        # in case some of the lists is invalid
        if not list_value_self or not list_value_event:
            # returns false
            return False

        # retrieves the length of the list value for self
        length_self = len(list_value_self)

        # retrieves the length of the list value for event
        length_event = len(list_value_event)

        # in case the lengths for the list are different
        if not length_self == length_event:
            # returns false
            return False

        # iterates over all the lists
        for index in range(length_self):
            # compares both values
            if list_value_self[index] != list_value_event[index]:
                # returns false
                return False

        # returns true
        return True

    def __ne__(self, event):
        return not self.__eq__(event)

    def is_sub_event(self, event):
        """
        Tests if the given event is sub event.

        @type event: Event
        @param event: The event to be tested.
        @rtype: bool
        @return: The result of the is sub event test.
        """

        # retrieves the list value self
        list_value_self = self.list_value

        # retrieves the list value event
        list_value_event = event.list_value

        # in case any of the lists is empty or invalid
        if not list_value_self or not list_value_event:
            # returns false
            return False

        # retrieves the list value self length
        list_value_self_length = len(list_value_self)

        # retrieves the list value event length
        list_value_event_length = len(list_value_event)

        # in case the list value event length is less or
        # equal than list value self length
        if list_value_event_length <= list_value_self_length:
            return False

        # iterates over the list value self range
        for index in range(list_value_self_length):
            # in case the values of each list are different
            if list_value_self[index] != list_value_event[index]:
                # returns false
                return False

        # returns true
        return True

    def is_event_or_sub_event(self, event):
        """
        Tests if the given event is a event or sub event.

        @type event: Event
        @param event: The event to be tested.
        @rtype: bool
        @return: The result of the is event or sub event test.
        """

        # in case the capability is equal or sub capability
        if self.__eq__(event) or self.is_sub_event(event):
            # returns true
            return True
        # otherwise
        else:
            # returns false
            return False

def capability_and_super_capabilites(capability):
    """
    Retrieves the list of the capability and all super capabilities.

    @type capability: String
    @param capability: The capability to retrieve the the list of the
    capability and all super capabilities.
    @rtype: List
    @return: The list of the capability and all super capabilities.
    """

    # creates the capability structure from the capability string
    capability_structure = Capability(capability)

    # returns the list of the capability and all super capabilities
    return capability_structure.capability_and_super_capabilites()

def is_capability_or_sub_capability(base_capability, capability):
    """
    Tests if the given capability is capability or sub capability
    of the given base capability.

    @type base_capability: String
    @param base_capability: The base capability to be used for test.
    @type capability: String
    @param capability: The capability to be tested.
    @rtype: bool
    @return: The result of the test.
    """

    # creates the base capability structure from
    # the base capability string
    base_capability_structure = Capability(base_capability)

    # creates the capability structure from the capability string
    capability_structure = Capability(capability)

    # returns the result of the is capability or sub capability test
    return base_capability_structure.is_capability_or_sub_capability(capability_structure)

def is_capability_or_sub_capability_in_list(base_capability, capability_list):
    """
    Tests if any of the capabilities in the capability list is capability or
    sub capability of the given base capability.

    @type base_capability: String
    @param base_capability: The base capability to be used for test.
    @type capability_list: List
    @param capability_list: The list of capabilities to be tested.
    @rtype: bool
    @return: The result of the test.
    """

    # iterates over all the capabilities in the capability list
    for capability in capability_list:
        # tests if the capability is capability or
        # sub capability of the base capability
        if is_capability_or_sub_capability(base_capability, capability):
            # returns true
            return True

    # returns false
    return False

def convert_to_capability_list(capability_list):
    """
    Converts the given capability list (list of strings),
    into a list of capability objects (structures).

    @type capability_list: List
    @para capability_list: The list of capability strings.
    @rtype: List
    @return: The list of converted capability objects (structures).
    """

    # creates the list of capability structures
    capability_list_structure = []

    # iterates over all the capabilities in the capability list
    for capability in capability_list:
        # retrieves the capability type
        capability_type = type(capability)

        # in case the capability type is tuple
        if capability_type == types.TupleType:
            # retrieves the capability value and diffusion policy
            capability_value, _diffusion_policy = capability
        else:
            # sets the capability values as the capability itself
            capability_value = capability

        # creates the capability structure from the
        # capability string
        capability_structure = Capability(capability_value)

        # adds the capability structure to the list
        # of capability structures
        capability_list_structure.append(capability_structure)

    # returns the list of capability structures
    return capability_list_structure

def is_event_or_sub_event(base_event, event):
    """
    Tests if the given event is event or sub event
    of the given base event.

    @type base_event: String
    @param base_event: The base event to be used for test.
    @type event: String
    @param event: The event to be tested.
    @rtype: bool
    @return: The result of the test.
    """

    # creates the base event structure from
    # the base event string
    base_event_structure = Event(base_event)

    # creates the event structure from the event string
    event_structure = Event(event)

    # returns the result of the is event or sub event test
    return base_event_structure.is_event_or_sub_event(event_structure)

def is_event_or_super_event(base_event, event):
    """
    Tests if the given event is event or super event
    of the given base event.

    @type base_event: String
    @param base_event: The base event to be used for test.
    @type event: String
    @param event: The event to be tested.
    @rtype: bool
    @return: The result of the test.
    """

    # returns the result of the is event or sub event test
    # inverting the arguments
    return is_event_or_sub_event(event, base_event)

def is_event_or_sub_event_in_list(base_event, event_list):
    """
    Tests if any of the event in the event list is event or
    sub event of the given base event.

    @type base_event: String
    @param base_event: The base event to be used for test.
    @type event_list: List
    @param event_list: The list of events to be tested.
    @rtype: bool
    @return: The result of the test.
    """

    # iterates over all the events in the event list
    for event in event_list:
        # tests if the event is event or
        # sub event of the base event
        if is_event_or_sub_event(base_event, event):
            # returns true
            return True

    # returns false
    return False

def is_event_or_super_event_in_list(base_event, event_list):
    """
    Tests if any of the event in the event list is event or
    super event of the given base event.

    @type base_event: String
    @param base_event: The base event to be used for test.
    @type event_list: List
    @param event_list: The list of events to be tested.
    @rtype: bool
    @return: The result of the test.
    """

    # iterates over all the events in the event list
    for event in event_list:
        # tests if the event is event or
        # super event of the base event
        if is_event_or_super_event(base_event, event):
            # returns true
            return True

    # returns false
    return False

def get_all_events_or_super_events_in_list(base_event, event_list):
    """
    Retrieves all the events or super events in the list.
    Filters the event list, retrieving only the event thar are events or
    super events of the base event.

    @type base_event: String
    @param base_event: The base event to be used for filtering.
    @type event_list: List
    @param event_list: The list of events to be filtered.
    @rtype: List
    @return: The filtered list of events.
    """

    # creates the events or super events list
    events_or_super_events_list = []

    # iterates over all the events in the events list
    for event in event_list:
        # tests if the event is event or
        # super event of the base event
        if is_event_or_super_event(base_event, event):
            # adds the event to the events or super events list
            events_or_super_events_list.append(event)

    # returns the events or super events list
    return events_or_super_events_list

def convert_to_event_list(event_list):
    """
    Converts the given event list (list of strings),
    into a list of event objects (structures).

    @type event_list: List
    @para event_list: The list of event strings.
    @rtype: List
    @return: The list of converted event objects (structures).
    """

    # creates the list of event structures
    event_list_structure = []

    # iterates over all the events in the event list
    for event in event_list:
        # creates the event structure from the
        # event string
        event_structure = Event(event)

        # adds the event structure to the list
        # of event structures
        event_list_structure.append(event_structure)

    # returns the list of event structures
    return event_list_structure

class PluginThread(threading.Thread):
    """
    The plugin thread class.
    """

    plugin = None
    """ The plugin to be used """

    load_complete = False
    """ The load complete flag """

    end_load_complete = False
    """ The end load complete flag """

    unload_complete = False
    """ The unload complete flag """

    end_unload_complete = False
    """ The end unload complete flag """

    load_plugin_thread = None
    """ The thread that controls the load plugin method call """

    end_load_plugin_thread = None
    """ The thread that controls the end load plugin method call """

    unload_plugin_thread = None
    """ The thread that controls the unload plugin method call """

    end_unload_plugin_thread = None
    """ The thread that controls the end unload plugin method call """

    event_queue = []
    """ The queue of events to be processed """

    condition = None
    """ The plugin thread condition """

    def __init__ (self, plugin):
        """
        Constructor of the class.

        @type plugin: Plugin
        @param plugin: The plugin to be used.
        """

        threading.Thread.__init__(self)
        self.plugin = plugin
        self.condition = threading.Condition()

        self.event_queue = []
        self.load_complete = False

    def set_load_complete(self, value):
        """
        Sets the load complete.

        @type value: bool
        @param value: The load complete.
        """

        self.load_complete = value

    def set_end_load_complete(self, value):
        """
        Sets the end load complete.

        @type value: bool
        @param value: The end load complete.
        """

        self.end_load_complete = value

    def set_unload_complete(self, value):
        """
        Sets the unload complete.

        @type value: bool
        @param value: The unload complete.
        """

        self.unload_complete = value

    def set_end_unload_complete(self, value):
        """
        Sets the end unload complete.

        @type value: bool
        @param value: The end unload complete.
        """

        self.end_unload_complete = value

    def add_event(self, event):
        """
        Adds an event to the event queue.

        @type event: String
        @param event: The event to be added to the event queue.
        """

        # acquires the condition
        self.condition.acquire()

        # adds the event to the event queue
        self.event_queue.append(event)

        # notifies the condition
        self.condition.notify()

        # releases the condition
        self.condition.release()

    def process_event(self, event):
        """
        Processes the given queue event.

        @type event: Event
        @param event: The event to be processed.
        @rtype: bool
        @return: If the upper loop should be terminated.
        """

        if event.event_name == EXIT_VALUE:
            if self.load_plugin_thread and self.load_plugin_thread.isAlive():
                self.load_plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)
            if self.end_load_plugin_thread and self.end_load_plugin_thread.isAlive():
                self.end_load_plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)
            if self.unload_plugin_thread and self.unload_plugin_thread.isAlive():
                self.unload_plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)
            if self.end_unload_plugin_thread and self.end_unload_plugin_thread.isAlive():
                self.end_unload_plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)
            return True
        elif event.event_name == LOAD_VALUE:
            self.load_plugin_thread = PluginEventThread(self.plugin, self.plugin.load_plugin)
            self.load_plugin_thread.start()
            self.load_complete = True
        elif event.event_name == LAZY_LOAD_VALUE:
            self.lazy_load_plugin_thread = PluginEventThread(self.plugin, self.plugin.lazy_load_plugin)
            self.lazy_load_plugin_thread.start()
            self.load_complete = True
        elif event.event_name == END_LOAD_VALUE:
            self.end_load_plugin_thread = PluginEventThread(self.plugin, self.plugin.end_load_plugin)
            self.end_load_plugin_thread.start()
            self.end_load_complete = True
        elif event.event_name == UNLOAD_VALUE:
            self.unload_plugin_thread = PluginEventThread(self.plugin, self.plugin.unload_plugin)
            self.unload_plugin_thread.start()
            self.unload_complete = True
        elif event.event_name == END_UNLOAD_VALUE:
            self.end_unload_plugin_thread = PluginEventThread(self.plugin, self.plugin.end_unload_plugin)
            self.end_unload_plugin_thread.start()
            self.end_unload_complete = True

    def run(self):
        """
        Starts running the thread.
        """

        # loops continuously
        while True:
            # acquires the condition
            self.condition.acquire()

            # iterates while the event queue is empty
            while not len(self.event_queue):
                # waits for the condition
                self.condition.wait()

            # retrieves the event
            event = self.event_queue.pop(0)

            # processes the event
            if self.process_event(event):
                # releases the condition
                self.condition.release()

                # returns immediately
                return

            # releases the condition
            self.condition.release()

class PluginEventThread(threading.Thread):
    """
    The plugin event thread class.
    """

    plugin = None
    """ The plugin that contains the method to be executed """

    method = None
    """ The method for the event thread """

    def __init__ (self, plugin, method):
        """
        Constructor of the class.

        @type plugin: Plugin
        @param plugin: The plugin that contains the method to be executed.
        @type method: Method
        @param method: The method for the event thread.
        """

        threading.Thread.__init__(self)

        self.plugin = plugin
        self.method = method

    def run(self):
        """
        The method to start running the thread.
        """

        if self.plugin.manager.stop_on_cycle_error:
            # retrieves the original semaphore release count
            original_semaphore_release_count = self.plugin.ready_semaphore_release_count

            # calls the event thread method
            self.method()
        else:
            try:
                # retrieves the original semaphore release count
                original_semaphore_release_count = self.plugin.ready_semaphore_release_count

                # calls the event thread method
                self.method()
            except BaseException, exception:
                # prints an error message
                self.plugin.error("Problem starting thread plugin: " + unicode(exception))

                # sets the exception in the plugin
                self.plugin.exception = exception

                # sets the plugin error state flag
                self.plugin.error_state = True

        # acquires the ready semaphore lock
        self.plugin.ready_semaphore_lock.acquire()

        # retrieves the original semaphore release count
        new_semaphore_release_count = self.plugin.ready_semaphore_release_count

        # releases the ready semaphore lock
        self.plugin.ready_semaphore_lock.release()

        # in case the semaphore is locked waiting for the release
        if new_semaphore_release_count == original_semaphore_release_count:
            # releases the ready semaphore
            self.plugin.release_ready_semaphore()

            # prints log message
            self.plugin.error("No Semaphore released upon thread call")
