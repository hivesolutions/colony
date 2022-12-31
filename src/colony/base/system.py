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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.4.4"
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
import re
import sys
import copy
import stat
import time
import signal
import inspect
import unittest
import tempfile
import threading
import traceback
import subprocess

import logging.handlers

import colony.libs

from . import util
from . import legacy
from . import config
from . import loggers
from . import exceptions
from . import information

GLOBAL_CONFIG = config.GLOBAL_CONFIG
""" The global static configuration of the manager that
is going to be used for some of the operations """

CPYTHON_ENVIRONMENT = util.CPYTHON_ENVIRONMENT
""" CPython environment value """

JYTHON_ENVIRONMENT = util.JYTHON_ENVIRONMENT
""" Jython environment value """

IRON_PYTHON_ENVIRONMENT = util.IRON_PYTHON_ENVIRONMENT
""" IronPython environment value """

DEFAULT_LOGGER = "default_messages"
""" The default logger name """

DEFAULT_LOGGING_LEVEL = logging.INFO
""" The default logging level to be used as the minimal
logging level to all the default (verbose) loggers """

DEFAULT_LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
""" The default logging format """

DEFAULT_LOGGING_FILE_NAME_PREFIX = "colony"
""" The default logging file name prefix """

DEFAULT_LOGGING_FILE_NAME_SEPARATOR = "_"
""" The default logging file name separator """

DEFAULT_LOGGING_FILE_NAME_EXTENSION = ".log"
""" The default logging file name extension """

DEFAULT_LOGGING_ERR_FILE_NAME_EXTENSION = ".err"
""" The default logging file name extension
for the error type of file logging """

DEFAULT_LOGGING_FILE_MODE = "a"
""" The default logging file mode """

DEFAULT_LOGGING_FILE_SIZE = 10485760
""" The default logging file size """

DEFAULT_LOGGING_FILE_BACKUP_COUNT = 5
""" The default logging file backup count """

DEFAULT_CONTAINERS_PATH = "containers"
""" The default containers path """

DEFAULT_LIBRARIES_PATH = "libraries"
""" The default libraries path """

DEFAULT_TEMPORARY_PATH = "tmp"
""" The default temporary path """

DEFAULT_VARIABLE_PATH = "var"
""" The default variable path """

DEFAULT_PLUGIN_PATH = "plugins"
""" The default plugin path """

DEFAULT_CONFIGURATION_PATH = "meta"
""" The default configuration path """

DEFAULT_PLUGIN_PATHS_FILE_PATH = "config/general/plugins.pth"
""" The default plugin paths file path """

DEFAULT_WORKSPACE_PATH = "~/.colony_workspace"
""" The default workspace path """

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

SPECIAL_VALUE_REGEX_VALUE = "%(?P<command>[a-zA-Z0-0_]*)(:(?P<arguments>[a-zA-Z0-9_.,]*))?%"
""" The special value regex value """

SPECIAL_VALUE_REGEX = re.compile(SPECIAL_VALUE_REGEX_VALUE)
""" The special value regex """

ALIAS_MAP = dict(
    devel = "development",
    prod = "production",
    runtime = "production"
)
""" The map that is going to be used for the final resolution
of the layout/run modes, this is used so that shorter names
may be used for this modes (simplified execution) """

class System(object):
    """
    The base system class from which all the back end
    plugin system classes may inherit to obtain some
    generalized behavior on the plugin access.
    """

    plugin = None
    """ The reference to the plugin that "owns" this
    system object, this may be used to reference the
    top level manager functions """

    def __init__(self, plugin):
        """
        Constructor of the class, received the "owner"
        plugin as the first argument to be stored for
        latter usage.

        :type plugin: Plugin
        :param plugin: The owner plugin for the system
        object to be created.
        """

        self.plugin = plugin

    def get_manager(self):
        """
        Retrieves the plugin manager reference associated
        with the current system, this method call depends
        on the definition of the owner plugin.

        :rtype: PluginManager
        :return: The plugin manager instance associated with
        the current execution context.
        """

        return self.plugin.manager

    def debug(self, *args, **kwargs):
        return self.plugin.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self.plugin.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.plugin.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.plugin.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        return self.plugin.critical(*args, **kwargs)

class Plugin(object):
    """
    The abstract plugin class.
    Contains most of the basic utility function and handlers
    used during the plugin file cycle.

    All the concrete plugin implementation should inherit from
    this class so that they become compatible with the base
    colony specification for python.
    """

    id = None
    """ The id of the plugin, this is considered to be the
    primary identifier of the plugin and should be unique """

    name = None
    """ The name of the plugin as a more relaxed and verbose
    way of presenting the plugin """

    description = None
    """ The description of the plugin """

    version = None
    """ The version of the plugin """

    author = None
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

    events_fired = []
    """ The events fired by the plugin """

    events_handled = []
    """ The events that the plugin can handle """

    main_modules = []
    """ The main modules of the plugin, this value
    should reference the complete set of prefix values
    that should be used as reference for module operation
    for instance this value is going to be used as the
    reference for the reloading of modules for the
    autoloading operations """

    valid = True
    """ The valid flag of the plugin """

    logger = None
    """ The reference to the logger object that is
    going to be used by the plugin in the logging
    operation, this may come from an external source """

    timestamp = None
    """ The timestamp that stores the load time
    of the last load operation, this value is not
    set in case the plugin is not loaded """

    dependencies_loaded = []
    """ The list of dependency plugins loaded """

    allowed_loaded_capability = []
    """ The list of allowed plugins loaded with capability """

    event_plugins_fired_loaded_map = {}
    """ The map with the plugin associated with
    the name of the event fired """

    event_plugins_registered_loaded_map = {}
    """ The map with the plugin associated with
    the name of the event registered """

    event_plugin_manager_registered_loaded_list = []
    """ The list with all the events registered
    in the plugin manager """

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

        :type manager: PluginManager
        :param manager: The plugin manager of the system.
        """

        self.original_id = self.id
        self.manager = manager
        self.ready_semaphore = threading.Semaphore(0)
        self.ready_semaphore_lock = threading.Lock()

        self.ready_semaphore_release_count = 0

        self.logger = logging.getLogger(DEFAULT_LOGGER)
        self.dependencies_loaded = []
        self.allowed_loaded_capability = []
        self.event_plugins_fired_loaded_map = {}
        self.event_plugins_registered_loaded_map = {}
        self.event_plugin_manager_registered_loaded_list = []
        self.configuration_map = {}
        self.loaded = False
        self.lazy_loaded = False
        self.error_state = False

    def __repr__(self):
        """
        Returns the default representation of the class.

        :rtype: String
        :return: The default representation of the class.
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

        # iterates over the complete set of allowed capabilities to be able
        # to creates the required structures for the access to the loaded
        # allowed plugins, note that they have not been loaded yet into the
        # current plugin, so we can change the internal values of structures
        for capability in self.capabilities_allowed:
            setattr(self, capability, {})
            setattr(self, capability + "_plugins", [])

        # registers all the plugin manager events
        self.register_all_plugin_manager_events()

        # sets the values of a series of flags that control the state of the
        # current plugin, these values may be used in flow control
        self.loaded = True
        self.lazy_loaded = False
        self.error_state = False

        # resets the (load) timestamp value to the current
        # timestamp, with this value it will be possible to
        # calculate the uptime for the plugin
        self.timestamp = time.time()

        # generates the load plugin event
        self.manager.generate_event("plugin_manager.plugin.load_plugin", [self.id, self.version, self])

        # prints an info message
        self.info("Loading plugin '%s' v%s" % (self.name, self.version))

    def lazy_load_plugin(self):
        """
        Method called at the beginning of the lazy plugin loading process.
        """

        # registers all the plugin manager events
        self.register_all_plugin_manager_events()

        # sets the values of a series of flags that control the state of the
        # current plugin, these values may be used in flow control
        self.loaded = True
        self.lazy_loaded = True
        self.error_state = False

        # generates the lazy load plugin event
        self.manager.generate_event("plugin_manager.plugin.lazy_load_plugin", [self.id, self.version, self])

        # prints a debug message
        self.debug("Lazy loading plugin '%s' v%s" % (self.name, self.version))

    def end_load_plugin(self):
        """
        Method called at the end of the plugin loading process.
        """

        # generates the end load plugin event
        self.manager.generate_event("plugin_manager.plugin.end_load_plugin", [self.id, self.version, self])

        self.debug("Loading process for plugin '%s' v%s completed" % (self.name, self.version))

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

        # restores the timestamp value to the original (unset)
        # to avoid erroneous calculation of uptime values
        self.timestamp = None

        # resets the dependencies loaded (no dependencies
        # are loaded in the plugin at the end of the unload)
        self.dependencies_loaded = []

        # resets the allowed loaded capability (no allowed
        # are loaded in the plugin at the end of the unload)
        self.allowed_loaded_capability = []

        # generates the load plugin event
        self.manager.generate_event("plugin_manager.plugin.unload_plugin", [self.id, self.version, self])

        # prints an info message
        self.info("Unloading plugin '%s' v%s" % (self.name, self.version))

    def end_unload_plugin(self):
        """
        Method called at the end of the plugin unloading process.
        """

        # sets the error state as false
        self.error_state = False

        # generates the load plugin event
        self.manager.generate_event("plugin_manager.plugin.end_unload_plugin", [self.id, self.version, self])

        # prints an info message
        self.info("Unloading process for plugin '%s' v%s completed" % (self.name, self.version))

    def load_allowed(self, plugin, capability):
        """
        Method called at the loading of an allowed plugin.

        :type plugin: Plugin
        :param plugin: The allowed plugin that is being loaded.
        :type capability: String
        :param capability: Capability for which the plugin is being injected.
        """

        # creates the plugin capability tuple that is going to represent
        # the relation between the current plugin and the allowed one
        plugin_capability_tuple = (
            plugin,
            capability
        )

        # in case the plugin capability tuple already exists in
        # the allowed loaded capability list, an exception must
        # be raised indicating the problem (assertion)
        if plugin_capability_tuple in self.allowed_loaded_capability:
            raise exceptions.PluginSystemException(
                "invalid plugin allowed loading (duplicate) '%s' v%s in '%s' v%s" %
                (plugin.name, plugin.version, self.name, self.version)
            )

        # in case the current plugin does not have the capability plugins
        # definition set creates a new map for it and then registers the
        # newly allowed plugin in the map (for latter usage)
        if not hasattr(self, capability): setattr(self, capability, {})
        allowed = getattr(self, capability)
        allowed[plugin.short_name] = plugin

        # verifies if the current plugin already has the plugins list for
        # the current capability created and if that's not the case creates
        # a new list and then appends the current allowed plugin to the list
        if not hasattr(self, capability + "_plugins"):
            setattr(self, capability + "_plugins", [])
        allowed_list = getattr(self, capability + "_plugins")
        allowed_list.append(plugin)

        # adds the plugin capability tuple to the allowed loaded capability
        # and registers for all handled events
        self.allowed_loaded_capability.append(plugin_capability_tuple)
        self.register_all_handled_events_plugin(plugin)

        # prints a debug message about the loading of the plugin inside
        # the current plugin (for diagnostic purposes)
        self.debug(
            "Loading plugin '%s' v%s in '%s' v%s" %
            (plugin.name, plugin.version, self.name, self.version)
        )

    def unload_allowed(self, plugin, capability):
        """
        Method called at the unloading of an allowed plugin.

        :type plugin: Plugin
        :param plugin: The allowed plugin that is being unloaded.
        :type capability: String
        :param capability: Capability for which the plugin is being injected.
        """

        # creates the plugin capability tuple
        plugin_capability_tuple = (
            plugin,
            capability
        )

        # in case the plugin capability tuple does not exist in
        # the allowed loaded capability list, this is an error
        # and an exception must be raised indicating it
        if not plugin_capability_tuple in self.allowed_loaded_capability:
            raise exceptions.PluginSystemException(
                "invalid plugin allowed unloading (not existent) '%s' v%s in '%s' v%s" %
                (plugin.name, plugin.version, self.name, self.version)
            )

        # retrieves the map of allowed loaded plugin for the current
        # plugin and removes the reference to the plugin to be unloaded
        # from that map as it is no longer allowed in the current plugin
        allowed = getattr(self, capability)
        del allowed[plugin.short_name]

        # retrieves the list of allowed plugins for the current capability
        # that is currently registered and then removes the current plugin
        # from it as it's currently being unloaded (as expected)
        allowed_list = getattr(self, capability + "_plugins")
        allowed_list.remove(plugin)

        # removes the plugin capability tuple from the allowed loaded capability
        # and then unregisters for all handled events of the plugin to be unloaded
        self.allowed_loaded_capability.remove(plugin_capability_tuple)
        self.unregister_all_handled_events_plugin(plugin)

        # prints an info message about the unloading of the plugin
        # so that the developer is notified about the operation
        self.info(
            "Unloading plugin '%s' v%s in '%s' v%s" %
            (plugin.name, plugin.version, self.name, self.version)
        )

    def dependency_injected(self, plugin):
        """
        Method called at the injection of a plugin dependency.
        Should change the current plugin instance so that it
        is able to recognizes the newly injected plugin instance.

        :type plugin: Plugin
        :param plugin: The dependency plugin to be injected.
        """

        # adds the dependency that was injected into the list of
        # loaded dependencies and then "injects" the plugin into
        # the plugin where it is being loaded, then loads a message
        # about the injection of the dependency
        self.dependencies_loaded.append(plugin)
        setattr(self, plugin.short_name + "_plugin", plugin)
        self.debug(
            "Plugin dependency '%s' v%s injected in '%s' v%s" %
            (plugin.name, plugin.version, self.name, self.version)
        )

    def init_complete(self):
        """
        Method called at the end of the plugin manager initialization.
        """

        self.debug("Plugin '%s' v%s notified about the end of the plugin manager init process" % (self.name, self.version))

    def register_all_handled_events_plugin(self, plugin):
        """
        Registers all the allowed events from a given plugin in self.

        :type plugin: Plugin
        :param plugin: The plugin containing the events to be registered.
        """

        event_names_handled = [event_name for event_name in plugin.events_fired if is_event_or_super_event_in_list(event_name, self.events_handled)]

        for event_name_handled in event_names_handled:
            self.register_for_plugin_event(plugin, event_name_handled)

    def unregister_all_handled_events_plugin(self, plugin):
        """
        Unregisters all the allowed events from a given plugin in self.

        :type plugin: Plugin
        :param plugin: The plugin containing the events to be unregistered.
        """

        for event_name in self.event_plugins_registered_loaded_map:
            if plugin in self.event_plugins_registered_loaded_map[event_name]:
                self.unregister_for_plugin_event(plugin, event_name)

    def register_all_plugin_manager_events(self):
        """
        Registers all the plugin manager events in self.
        """

        event_names_handled = [event_name for event_name in self.events_handled if is_event_or_sub_event("plugin_manager", event_name)]

        for event_name_handled in event_names_handled:
            self.register_for_plugin_manager_event(event_name_handled)

    def unregister_all_plugin_manager_events(self):
        """
        Unregisters all the plugin manager events in self.
        """

        event_plugin_manager_registered_loaded_list = copy.copy(self.event_plugin_manager_registered_loaded_list)

        for event_name in event_plugin_manager_registered_loaded_list:
            self.unregister_for_plugin_manager_event(event_name)

    def register_for_plugin_event(self, plugin, event_name):
        """
        Registers a given event from a given plugin in self.

        :type plugin: Plugin
        :param plugin: The plugin containing the event to be registered.
        :type event_name: String
        :param event_name: The name of the event to be registered.
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

        :type plugin: Plugin
        :param plugin: The plugin containing the event to be unregistered.
        :type event_name: String
        :param event_name: The name of the event to be unregistered.
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

        :type event_neme: String
        :param event_name: The name of the event to be registered.
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

        :type event_name: String
        :param event_name: The name of the event to be unregistered.
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

        :type event_name: String
        :param event_name: The name of the event to be unregistered.
        """

        if event_name in self.event_plugins_registered_loaded_map:
            for plugin in self.event_plugins_registered_loaded_map[event_name]:
                if not plugin.is_loaded_or_lazy_loaded(): continue
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

        :type plugin: Plugin
        :param plugin: The plugin containing the handler to the event.
        :type event_name: String
        :param event_name: The name of the event to be registered.
        """

        if not event_name in self.event_plugins_fired_loaded_map:
            self.event_plugins_fired_loaded_map[event_name] = []

        if plugin in self.event_plugins_fired_loaded_map[event_name]: return
        self.event_plugins_fired_loaded_map[event_name].append(plugin)
        self.debug(
            "Registering event '%s' from '%s' v%s in '%s' v%s" %
            (event_name, plugin.name, plugin.version, self.name, self.version)
        )

    def unregister_plugin_event(self, plugin, event_name):
        """
        Unregisters a given event in the given plugin.

        :type plugin: Plugin
        :param plugin: The plugin containing the handler to the event.
        :type event_name: String
        :param event_name: The name of the event to be unregistered.
        """

        if not event_name in self.event_plugins_fired_loaded_map: return
        if not plugin in self.event_plugins_fired_loaded_map[event_name]: return
        self.event_plugins_fired_loaded_map[event_name].remove(plugin)
        self.debug(
            "Unregistering event '%s' from '%s' v%s in '%s' v%s" %
            (event_name, plugin.name, plugin.version, self.name, self.version)
        )

    def notify_handlers(self, event_name, event_args):
        """
        Notifies all the handlers for the event with the given name
        with the give arguments.

        :type event_name: String
        :param event_name: The name of the event to be notified.
        :type event_args: List
        :param event_args: The arguments to be passed to the handler.
        """

        # the names of the events fired by self
        event_names_list = legacy.keys(self.event_plugins_fired_loaded_map)

        # retrieves all the events and super events that match the generated event
        events_or_super_events_list = get_all_events_or_super_events_in_list(event_name, event_names_list)

        # iterates over all the events and super events for notification
        for event_or_super_event in events_or_super_events_list:
            if not event_or_super_event in self.event_plugins_fired_loaded_map: continue

            # iterates over all the plugins registered for notification
            for event_plugin_loaded in self.event_plugins_fired_loaded_map[event_or_super_event]:
                # prints a debug message
                self.debug(
                    "Notifying '%s' v%s about event '%s' generated in '%s' v%s" %
                    (
                        event_plugin_loaded.name,
                        event_plugin_loaded.version,
                        event_name,
                        self.name,
                        self.version
                    )
                )

                # calls the event handler for the event name with
                # the given event arguments
                event_plugin_loaded.event_handler(event_name, *event_args)

    def generate_event(self, event_name, event_args):
        """
        Generates an event and starts the process of handler notification.

        :type event_name: String
        :param event_name: The name of the event to be notified.
        :type event_args: List
        :param event_args: The arguments to be passed to the handler.
        """

        if not is_event_or_super_event_in_list(event_name, self.events_fired):
            return

        # prints a debug message
        self.debug("Event '%s' generated in '%s' v%s" % (event_name, self.name, self.version))

        # notifies the event handlers
        self.notify_handlers(event_name, event_args)

    def event_handler(self, event_name, *event_args):
        """
        The top level event handling method.

        :type event_name: String
        :param event_name: The name of the event triggered.
        :type event_args: List
        :param event_args: The arguments for the handler.
        """

        # prints a debug message
        self.debug("Event '%s' caught in '%s' v%s" % (event_name, self.name, self.version))

    def reload_main_modules(self):
        """
        Reloads the plugin main modules in the interpreter.
        The strategy to be executed implies that the modules
        currently loaded in the system that are prefixed with
        the names defined in the main modules should be reloaded
        or in case an error occurs in the import removed from
        the currently loading memory for modules.

        This is a dangerous operation and care should be taken
        to avoid any system state corruption.
        """

        # prints an info message about the reloading of the main modules
        # of the plugins that is going to be performed
        self.info("Reloading main modules in '%s' v%s" % (self.name, self.version))

        # creates the list that will hold the complete set of modules that
        # are considered valid for the reload of modules operation
        valids = []

        # iterates over all the main modules in order to reloaded them
        # under the current environment, required for new updating
        for main_module in self.main_modules:
            # gathers the complete set of loaded modules that are prefixed
            # by the name defined as the current main module in iteration
            # and then extends the complete set of valid modules with them
            # also adds the main module that is defined with such name
            prefix = main_module + "."
            modules = [module for module in sys.modules if module.startswith(prefix)]
            valids.extend(modules)
            valids.append(main_module)

        # creates the simple sorter lambda function that will sort the list
        # of valid modules for reloading and runs the sorting operation so that
        # the final list of valid modules for reload is defined from the larger
        # (longest module names) to the shortest as required for correct loading
        sorter = lambda item: len(item)
        valids = list(set(valids))
        valids.sort(key = sorter, reverse = True)

        # iterates over the complete set of valid modules for reloading and runs
        # and tries to run the reloading logic for each of them, in case it fails
        # with an import error (assumes cycle error) the module is removed and it
        # should be reloaded during the next import operation
        for valid in valids:
            module = sys.modules[valid]
            if not module: continue
            try: legacy.reload(module)
            except ImportError: del sys.modules[valid]

    def get_configuration_property(self, property_name):
        """
        Returns the configuration property for the given property name.

        :type property_name: String
        :param property_name: The property name to retrieve the property.
        :rtype: Object
        :return: The configuration property for the given property name.
        """

        return self.configuration_map.get(property_name, None)

    def set_configuration_property(self, property_name, property):
        """
        Sets the configuration property for the given property name.

        :type property_name: String
        :param property_name: The property name to set the property.
        :type property: String
        :param property: The property name to set.
        """

        self.info(
            "Setting configuration property '%s' in '%s' v%s" %
            (property_name, self.name, self.version)
        )

        self.configuration_map[property_name] = property

    def unset_configuration_property(self, property_name):
        """
        Unsets the configuration property for the given property name.

        :type property_name: String
        :param property_name: The property name to unset the property.
        """

        self.info(
            "Unsetting configuration property '%s' from '%s' v%s" %
            (property_name, self.name, self.version)
        )

        del self.configuration_map[property_name]

    def ensure(self):
        """
        Ensures that the current plugin instance is loaded,
        loading it if required.

        In case the loading was not possible and the plugin
        remains unloaded at the end of the call an exception is
        raised indicating the problem.
        """

        # retrieve the (plugin) manager currently associated
        # with the plugin and uses it to make sure the current
        # plugin is currently loaded
        self.manager.ensure(self)

    def is_loaded(self):
        """
        Returns the result of the loading test.

        :rtype: bool
        :return: The result of the loading test (if the plugin is loaded or not).
        """

        return self.loaded and not self.lazy_loaded and not self.error_state

    def is_lazy_loaded(self):
        """
        Returns the result of the lazy loading test.

        :rtype: bool
        :return: The result of the lazy loading test (if the
        plugin is lazy loaded or not).
        """

        return self.lazy_loaded and not self.error_state

    def is_loaded_or_lazy_loaded(self):
        """
        Returns the result of the loading and lazy loading tests.

        :rtype: bool
        :return: The result of the loading and lazy loading tests
        (if the plugin is loaded or lazy loaded or not).
        """

        return (self.loaded or self.lazy_loaded) and not self.error_state

    def is_replica(self):
        """
        Returns the result of the replica test.

        :rtype: bool
        :return: The result of the replica test (if the plugin
        is a replica or not).
        """

        return not self.id == self.original_id

    def get_attribute(self, attribute_name, default = None):
        """
        Retrieves the attribute for the given attribute name.

        :type attribute_name: String
        :param attribute_name: The name of the attribute name to retrieve.
        :type default: Object
        :param default: The default value to be returned in case an
        attribute with the given name is not found.
        :rtype: Object
        :return: The attribute for the given attribute name.
        """

        return self.attributes.get(attribute_name, default)

    def has_capability(self, capability):
        """
        Checks if the given capability (name) is contained in the
        current set of capabilities for the plugin.

        This checking is made recursively and so any sub capability is
        also going to be matched.

        :type capability: String
        :param capability: The capability to be checked for existence
        in the current plugin.
        :rtype: bool
        :return: If the provided capability (name) exists in the current
        plugin context.
        """

        return capability in self.capabilities

    def contains_metadata(self):
        """
        Returns the result of the metadata test.

        :rtype: bool
        :return: The result of the metadata test (if the plugin
        contains metadata or not).
        """

        if hasattr(self, "metadata_map"): return True
        else: return False

    def contains_metadata_key(self, metadata_key):
        """
        Returns the result of the metadata key test.

        :type metadata_key: String
        :param metadata_key: The value of the metadata key
        to test for metadata.
        :rtype: bool
        :return: The result of the metadata key test (if the
        plugin contains the metadata key or not).
        """

        if self.contains_metadata():
            if metadata_key in self.metadata_map: return True
            else: return False
        else: return False

    def get_metadata(self):
        """
        Returns the metadata of the plugin.

        :rtype: Dictionary
        :return: The metadata of the plugin.
        """

        if self.contains_metadata(): return self.metadata_map

    def get_metadata_key(self, metadata_key):
        """
        Returns the metadata key of the plugin.

        :type metadata_key: String
        :param metadata_key: The value of the metadata key to retrieve.
        :rtype: Object
        :return: The metadata key of the plugin.
        """

        if self.contains_metadata_key(metadata_key): return self.metadata_map[metadata_key]

    def treat_exception(self, exception):
        """
        Treats the exception at the most abstract level.

        :type exception: Exception
        :param exception: The exception object to be treated.
        """

        # prints and info message
        self.info("Exception '%s' generated in '%s' v%s" % (str(exception), self.name, self.version))

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

        :rtype: List
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

        :rtype: List
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

        :rtype: Tuple
        :return: Tuple representing the plugin (id and version).
        """

        return (
            self.id,
            self.version
        )

    def get_author_name(self):
        """
        Retrieves the name component of the author attribute
        for the current plugin.

        This method excludes the email part of the author.

        :rtype: String
        :return: The name component of the author attribute for
        the current plugin.
        """

        return self.author.split("<", 1)[0].strip()

    def get_uptime(self):
        """
        Retrieves a string describing the uptime value for
        the current plugin.

        This string is a descriptive string in english language
        and should be used for presentation to a non technical
        user (not enough flexibility).

        :rtype: String
        :return: The string describing the current plugin uptime
        in english language.
        """

        # in case the timestamp is not defined, it's not possible
        # to calculate the uptime string so it must be unset
        if self.timestamp == None:
            # sets the uptime string as invalid (not possible)
            # to calculate it
            uptime = None
        # otherwise the (load) timestamp is defined and the
        # uptime string may be created using it
        else:
            # calculates the delta (value) between the current time
            # value and the saved load timestamp then uses it to create
            # the uptime message to be returned
            delta = time.time() - self.timestamp
            uptime = colony.libs.format_seconds_smart(delta, mode = "extended_simple")

        # returns the message containing the description
        # about the uptime for the current plugin
        return uptime

    def log_stack_trace(self, level = logging.DEBUG):
        """
        Logs the current stack trace to the logger.
        The verbosity level may be controlled using
        the level parameter.

        :type level: int
        :param level: The verbosity level to be used
        in the logging for the printing of the series
        of stack trace messages.
        """

        # retrieves the execution information, note
        # that this execution information only exists
        # in case an exception has been raised
        _type, _value, traceback_list = sys.exc_info()

        # in case the traceback list is valid formats it
        # correctly otherwise falls-back to the empty tuple
        # as the default formated traceback (no traceback)
        formated_traceback = traceback.format_tb(traceback_list) if\
            traceback_list else ()

        # iterates over the traceback lines to log
        # them into the current logger
        for formated_traceback_line in formated_traceback:
            # strips the formated traceback line and then
            # logs the message with the formated traceback line
            # with the requested log level (as specified)
            formated_traceback_line_stripped = formated_traceback_line.rstrip()
            self.logger.log(level, formated_traceback_line_stripped)

    def debug(self, message):
        """
        Adds the given debug message to the logger.

        :type message: String
        :param message: The debug message to be added to the logger.
        """

        # formats the logger message then prints the
        # debug message to the current stream
        logger_message = self.format_logger_message(message)
        self.logger.debug(logger_message)

    def info(self, message):
        """
        Adds the given info message to the logger.

        :type message: String
        :param message: The info message to be added to the logger.
        """

        # formats the logger message then prints the
        # info message to the current stream
        logger_message = self.format_logger_message(message)
        self.logger.info(logger_message)

    def warning(self, message):
        """
        Adds the given warning message to the logger.

        :type message: String
        :param message: The warning message to be added to the logger.
        """

        # formats the logger message then prints the
        # warning message and logs the current stack trace
        logger_message = self.format_logger_message(message)
        self.logger.warning(logger_message)
        self.log_stack_trace(level = logging.INFO)

    def error(self, message):
        """
        Adds the given error message to the logger.

        :type message: String
        :param message: The error message to be added to the logger.
        """

        # formats the logger message then prints the
        # error message and logs the current stack trace
        logger_message = self.format_logger_message(message)
        self.logger.error(logger_message)
        self.log_stack_trace(level = logging.WARNING)

    def critical(self, message):
        """
        Adds the given critical message to the logger.

        :type message: String
        :param message: The critical message to be added to the logger.
        """

        # formats the logger message then prints the
        # critical message and logs the current stack trace
        logger_message = self.format_logger_message(message)
        self.logger.critical(logger_message)
        self.log_stack_trace(level = logging.ERROR)

    def format_logger_message(self, message):
        """
        Formats the given message into a logging message.

        :type message: String
        :param message: The message to be formated into logging message.
        :rtype: String
        :return: The formated logging message.
        """

        # the default formatting message
        formatting_message = str()

        # in case the plugin id logging option is activated
        if GLOBAL_CONFIG.get("plugin_id_logging", False):
            formatting_message += "[" + self.id + "] "

        # in case the thread id logging option is activated
        if GLOBAL_CONFIG.get("thread_id_logging", False):
            formatting_message += "[" + str(threading.current_thread().ident) + "] "

        # appends the formatting message to the logging message and
        # returns it to the caller method
        logger_message = formatting_message + message
        return logger_message

    def _get_capabilities_allowed_names(self):
        """
        Retrieves the names of all the allowed capabilities
        from this plugin.

        :rtype: List
        :return: The names of all the allowed capabilities
        from this plugin.
        """

        # starts the capabilities allowed names
        # list to hold the various allowed capabilities
        capabilities_allowed_names = []

        # iterates over all the capabilities allowed
        for capability_allowed in self.capabilities_allowed:
            # retrieves the capability allowed type
            capability_allowed_type = type(capability_allowed)

            if capability_allowed_type == tuple:
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

        :type manager: PluginManager
        :param manager: The plugin manager of the system.
        """

        Plugin.__init__(self, manager)

class PluginManager(object):
    """
    The top level manager class, this is the controller (hypervisor)
    of all the plugin instances handled by him.

    Main tasks of it include inversion of control handling and reverse
    dependency injection. Other tasks include logging and resource
    handling support.

    Any change in this class must be done with care and with complete
    knowledge of the system as major problems may arise from a superficial
    and careless change.
    """

    uid = None
    """ The unique identification of the manager, this
    should be generated in a way than no id collision
    exists event at a distribution level (uuid is the
    recommended approach for generation) """

    logger = None
    """ The logger reference to be used as the base
    element for all the logging operations to be done
    under the plugin manager """

    logger_handlers = {}
    """ The map that associates a logging handler name
    with the proper handler instance so that inner details
    may be retrieved from the handler, useful for
    promiscuous usage of the logging handlers """

    platform = None
    """ The current executing platform, should be a
    sub value for the python interpreters (eg: cpython
    jython or iron python) """

    condition = None
    """ The condition used in the event queue of the
    plugin manager, this thread synchronization mechanism
    will ensure no race conditions on event queue """

    init_complete = False
    """ The initialization complete flag, that indicates
    that the manager's infra-structure has been completely
    and correctly loaded (as expected) """

    blacklist = []
    """ List containing the identifiers or short names of the
    various plugins that are not meant to be loaded even if
    all the pre-conditions for loading are met """

    blacktest = []
    """ Set of identifiers and short names for the various plugins
    that event if the tests are ready to be executed should not
    be executed on user request (blacklisted) """

    init_complete_handlers = []
    """ The list of handlers to be called at the end of
    the plugin manager initialization """

    main_loop_active = True
    """ The boolean value for the main loop activation
    if this value in unset the manager's loop will stop
    and the plugins will be unloaded gracefully """

    allow_threads = True
    """ The boolean value indicating if threads are allowed
    to be created for the context of the plugin manager """

    install_signals = True
    """ The boolean value indicating if signal handlers should
    be registered for exiting the plugin manager """

    layout_mode = "default"
    """ The layout mode used in the plugin loading, this is
    a deprecated value that used to defined the layout of the
    file system structure supporting the colony instance """

    run_mode = "default"
    """ The run mode used in the plugin loading, this value
    should condition the way some of the logic is process, for
    instance if the development mode is defined less concert
    should be taken with security and performance as opposed to
    a run or production run modes """

    container = "default"
    """ The name of the plugin manager container, this is
    used for situations where the plugin manager is running
    under a "contained" environment (eg: wsgi, mod_python, etc.) """

    daemon_pid = None
    """ The pid of the daemon process running the instance
    of plugin manager, this is only used for situations where
    the manager is running as explicit daemon (background usage)  """

    daemon_file_path = None
    """ The file path to the daemon file, for information control,
    this file will store the pid of the created process """

    prefix_paths = []
    """ The list of manager path relative paths to be used as
    reference for sub-projects """

    configuration_path = DEFAULT_CONFIGURATION_PATH
    """ The current configuration path """

    workspace_path = DEFAULT_WORKSPACE_PATH
    """ The current workspace path """

    timestamp = 0
    """ The plugin manager timestamp, this value should be set
    at the start of the plugin manager, and so indicates the time
    of the start of the plugin manager (may be used to calculate
    the total uptime for the current manager instance) """

    plugin_manager_plugins_loaded = False
    """ The plugin manager plugins loaded flag """

    plugins = None
    """ The object that stores the references to all
    the loaded plugins instances (singletons) indexed
    in the object by their short name """

    retrieve_lock = None
    """ The lock that is used to control the access and
    retrieval of plugin instance, no two threads may retrieve
    plugins at the same as this would create some sync problems """

    current_id = 0
    """ The current id used for the plugin, this value should be
    unique and incremental per each instance created """

    replica_id = 0
    """ The replica id for the replica plugins """

    diffusion_scope_id = 0
    """ The diffusion scope id for the replica plugins """

    return_code = 0
    """ The return code to be used on return, this value will
    be returned as the result of process execution """

    event_queue = []
    """ The queue of events to be processed """

    manager_path = None
    """ The manager base path for execution """

    logger_path = None
    """ The manager base path for logger """

    library_paths = None
    """ The set of paths for the external libraries
    plugins """

    plugin_paths = None
    """ The set of paths for the loaded plugins """

    kill_system_timer = None
    """ The timer used to kill the system in
    extreme situations """

    referred_modules = []
    """ The referred modules """

    loaded_plugins = []
    """ The loaded plugins """

    loaded_plugins_map = {}
    """ The map with classes associated with strings
    containing the id of the plugin """

    loaded_plugins_id_map = {}
    """ The map with the id of the plugin associated
    with the plugin id """

    id_loaded_plugins_map = {}
    """ The map with the plugin id associated with
    the id of the plugin """

    loaded_plugins_descriptions = []
    """ The descriptions of the loaded plugins """

    plugin_classes = []
    """ The available plugin classes """

    plugin_classes_map = {}
    """ The map with classes associated with strings
    containing the id of the plugin """

    plugin_instances = []
    """ The instances of the created plugins """

    plugin_instances_map = {}
    """ The map with instances associated with strings
    containing the id of the plugin """

    plugin_names_map = {}
    """ The map with instances associated with strings
    containing the name of the plugin, this name is extracted
    from the original plugin file name (prefix) """

    plugin_dirs_map = {}
    """ The map associating directories with th
     id of the plugin """

    capabilities_plugin_instances_map = {}
    """ The map associating capabilities with
    plugin instances """

    capabilities_sub_capabilities_map = {}
    """ The map associating capabilities with
    sub capabilities """

    plugin_threads = []
    """ The list of active running threads """

    plugin_threads_map = {}
    """ The map associating the active running threads
    with the id of the plugin """

    plugin_dependent_plugins_map = {}
    """ The map associating the plugins that
    depend on the plugin with the id of the plugin """

    plugin_allowed_plugins_map = {}
    """ The map associating the plugins that allow
    the plugin with the id of the plugin """

    capabilities_plugins_map = {}
    """ The map associating the capabilities with
    the the plugin that supports the capability """

    diffusion_scope_loaded_plugins_map = {}
    """ The map associating the diffusion scope
    with the loaded plugins that exist in the scope """

    deleted_plugin_classes = []
    """ The list containing the classes for
    the deleted plugins """

    event_plugins_fired_loaded_map = {}
    """ The map with the plugin associated with
    the name of the event fired """

    def __init__(
        self,
        manager_path = "",
        logger_path = "log",
        library_paths = [],
        meta_paths = [],
        plugin_paths = [],
        platform = CPYTHON_ENVIRONMENT,
        init_complete_handlers = [],
        stop_on_cycle_error = True,
        loop = True,
        threads = True,
        signals = True,
        layout_mode = "default",
        run_mode = "default",
        container = "default",
        prefix_paths = [],
        daemon_pid = None,
        daemon_file_path = None
    ):
        """
        Constructor of the class.

        :type manager_path: List
        :param manager_path: The manager base path for execution.
        :type logger_path: String
        :param logger_path: The manager base path for logger.
        :type library_paths: List
        :param library_paths: The list of directory paths for the loading
        of the external libraries.
        :type meta_paths: List
        :param meta_paths: The list of directory paths for the loading
        of the external metadata information.
        :type plugin_paths: List
        :param plugin_paths: The list of directory paths for the loading
        of the plugins.
        :type platform: int
        :param platform: The current executing platform.
        :type init_complete_handlers: List
        :param init_complete_handlers: The list of handlers to be called at
        the end of the plugin manager initialization.
        :type stop_on_cycle_error: bool
        :param stop_on_cycle_error: The boolean value for the stop on cycle error.
        :type loop: bool
        :param loop: The boolean value for the main loop activation.
        :type threads: bool
        :param threads: The boolean indicating if threads may be used in the
        manager for both plugins and control.
        :type signals: bool
        :param signals: The boolean indicating if signal handlers should be
        registered for the exiting of the system.
        :type layout_mode: String
        :param layout_mode: The layout mode used in the plugin loading.
        :type run_mode: String
        :param run_mode: The run mode used in the plugin loading.
        :type container: String
        :param container: The name of the plugin manager container.
        :type prefix_paths: List
        :param prefix_paths: The list of manager path relative paths to be
        set as reference for sub-projects.
        :type daemon_pid: int
        :param daemon_pid: The pid of the daemon process running the instance
        of plugin manager.
        :type daemon_file_path: String
        :param daemon_file_path: The file path to the daemon file, for
        information control.
        """

        self.manager_path = manager_path
        self.logger_path = logger_path
        self.library_paths = library_paths
        self.meta_paths = meta_paths
        self.plugin_paths = plugin_paths
        self.platform = platform
        self.init_complete_handlers = init_complete_handlers
        self.stop_on_cycle_error = stop_on_cycle_error
        self.main_loop_active = loop
        self.allow_threads = threads
        self.install_signals = signals
        self.layout_mode = ALIAS_MAP.get(layout_mode, layout_mode)
        self.run_mode = ALIAS_MAP.get(run_mode, run_mode)
        self.container = container
        self.prefix_paths = prefix_paths
        self.daemon_pid = daemon_pid
        self.daemon_file_path = daemon_file_path

        self.uid = util.get_timestamp_uid()
        self.condition = threading.Condition()

        self.blacklist = config.conf("BLACKLIST", [], cast = list)
        self.blacktest = config.conf("BLACKTEST", [], cast = list)
        self.whitetest = config.conf("WHITETEST", [], cast = list)
        self.exec_delay = config.conf("EXEC_DELAY", 0.0, cast = float)

        self.plugins = util.Plugins()
        self.retrieve_lock = threading.RLock()
        self.current_id = 0
        self.logger_handlers = {}
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
        self.plugin_names_map = {}
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
        self.event_plugins_fired_loaded_map = {}

    def create_plugin(self, plugin_id, plugin_version):
        """
        Creates a new instance of the plugin with the given id
        and version.

        This is method generates a new (unique) diffusion scope for the
        new plugin instance that is going to be created.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to create an instance.
        :param plugin_version: plugin_version
        :param plugin_version: The version of the plugin to create an instance.
        :rtype: Plugin
        :return: The created plugin instance (with an unique diffusion scope).
        """

        # generates a new diffusion scope id and uses it to  create a new
        # plugin instance, returning it then to the caller method as requested
        # by the call to this method, note that the diffusion scope id should
        # be unique according to the plugin manager specification
        diffusion_scope_id = self.generate_diffusion_scope_id()
        plugin_instance = self._create_plugin(plugin_id, plugin_version, diffusion_scope_id)
        return plugin_instance

    def _create_plugin(self, plugin_id, plugin_version, diffusion_scope_id):
        """
        Creates a new instance of the plugin with the given id
        and version for the given diffusion scope id.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to create an instance.
        :param plugin_version: plugin_version
        :param plugin_version: The version of the plugin to create an instance.
        :param diffusion_scope_id: int
        :param diffusion_scope_id: The diffusion scope id to be used in the creation.
        :rtype: Plugin
        :return: The created plugin instance.
        """

        # in case the plugin id does not exist in the plugin classes map
        if not plugin_id in self.plugin_classes_map:
            # raises the plugin class not available exception
            raise exceptions.PluginClassNotAvailable("invalid plugin '%s' v%s" % (plugin_id, plugin_version))

        # retrieves the plugin class
        plugin_class = self.plugin_classes_map[plugin_id]

        # in case the plugin version is not the same (uses
        # the defined version comparison)
        if not colony.libs.version_cmp(plugin_class.version, plugin_version):
            # raises the plugin class not available exception
            raise exceptions.PluginClassNotAvailable("invalid plugin '%s' v%s" % (plugin_id, plugin_version))

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

        :rtype: int
        :return: The replica id.
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

        :rtype: int
        :return: The diffusion scope id.
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
        The start of the logger implies the creation of the
        various handlers and the update of their formatters.

        :type log_level: int
        :param log_level: The log level of the logger.
        """

        # retrieves the minimal log level between the current
        # log level and the default one (as specified)
        minimal_log_level = DEFAULT_LOGGING_LEVEL if\
            DEFAULT_LOGGING_LEVEL < log_level else log_level

        # creates the (complete) logger file name by concatenating the
        # various prefixes, name separators, run mode and file name extensions
        logger_file_name = DEFAULT_LOGGING_FILE_NAME_PREFIX +\
            DEFAULT_LOGGING_FILE_NAME_SEPARATOR + self.run_mode +\
            DEFAULT_LOGGING_FILE_NAME_EXTENSION
        logger_err_file_name = DEFAULT_LOGGING_FILE_NAME_PREFIX +\
            DEFAULT_LOGGING_FILE_NAME_SEPARATOR + self.run_mode +\
            DEFAULT_LOGGING_ERR_FILE_NAME_EXTENSION

        # creates the complete logger file path by adding the "complete"
        # logger file name to the "base" logger path, this is done both
        # for the "normal" logger path and for the error based path
        logger_file_path = self.logger_path + "/" + logger_file_name
        logger_err_file_path = self.logger_path + "/" + logger_err_file_name

        # retrieves the logger, sets the logger propagation
        # to avoid propagation and then updates the logger
        # level to the minimal log level
        logger = logging.getLogger(DEFAULT_LOGGER)
        logger.propagate = 0
        logger.setLevel(minimal_log_level)

        # creates the stream handler and sets the logger level
        # for the stream handler (the currently selected log level)
        # avoids extra "verbosity"
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)

        # creates the rotating file handler that will be used for
        # the "normal" colony logger and that logs the complete set
        # of event associated with it (as defined in specification)
        # note that the log level is set to the not set level
        rotating_file_handler = logging.handlers.RotatingFileHandler(
            logger_file_path,
            DEFAULT_LOGGING_FILE_MODE,
            DEFAULT_LOGGING_FILE_SIZE,
            DEFAULT_LOGGING_FILE_BACKUP_COUNT
        )
        rotating_file_handler.setLevel(logging.NOTSET)

        # creates the rotating error file handler that handles all the
        # warning or more type of messages only, this is done in order
        # to facilitate the debugging strategy in real-time production
        # servers (as defined in the proper colony specification)
        rotating_err_file_handler = logging.handlers.RotatingFileHandler(
            logger_err_file_path,
            DEFAULT_LOGGING_FILE_MODE,
            DEFAULT_LOGGING_FILE_SIZE,
            DEFAULT_LOGGING_FILE_BACKUP_COUNT
        )
        rotating_err_file_handler.setLevel(logging.WARNING)

        # creates the broadcast handler so that the logging messages
        # may be sent to the world (network broadcast), then sets the
        # minimal level in it so that the maximum amount of information
        # is logged "into it" (permissive logging)
        broadcast_handler = loggers.BroadcastHandler()
        broadcast_handler.setLevel(minimal_log_level)

        # creates the in memory handler object and then again sets
        # the minimal log level in it so that it may have the
        # maximum amount of information available for handling
        memory_handler = loggers.MemoryHandler()
        memory_handler.setLevel(minimal_log_level)

        # retrieves the logging format and uses it
        # to create the proper logging formatter
        logging_format = GLOBAL_CONFIG.get(
            "logging_format",
            DEFAULT_LOGGING_FORMAT
        )
        formatter = logging.Formatter(logging_format)

        # sets the formatter in the stream and rotating
        # file handlers (correctly formats the message)
        stream_handler.setFormatter(formatter)
        rotating_file_handler.setFormatter(formatter)
        rotating_err_file_handler.setFormatter(formatter)
        broadcast_handler.setFormatter(formatter)
        memory_handler.setFormatter(formatter)

        # adds the complete set of logging handler to the
        # current logger, so that they get notified once
        # a new "message" is going to emit
        logger.addHandler(stream_handler)
        logger.addHandler(rotating_file_handler)
        logger.addHandler(rotating_err_file_handler)
        logger.addHandler(broadcast_handler)
        logger.addHandler(memory_handler)

        # sets the logger in the current context, so that
        # it may be used latter for reference
        self.logger = logger

        # updates the reference to all of the logging handlers
        # associated with the current logger so that latter it's
        # possible to retrieve each of them based on their name
        self.logger_handlers["stream"] = stream_handler
        self.logger_handlers["rotating_file"] = rotating_file_handler
        self.logger_handlers["rotating_err_file"] = rotating_err_file_handler
        self.logger_handlers["broadcast"] = broadcast_handler
        self.logger_handlers["memory"] = memory_handler

    def load_system(self, mode = None, args = None, callback = None):
        """
        Starts the process of loading the plugin system.

        This is the main entry point of the system from
        which either a command is executed or the main
        loop is started (blocking call).

        The arguments parameter provides a simple way of
        customizing the mode based execution, ultimately
        these arguments should come from command line.

        An optional callback argument may be used to have
        a function called at the end of the loading process.

        The resulting integer value may be returned to the
        caller process as the result of the execution.

        :type mode: String
        :param mode: The type of execution mode that is going to
        be used for this loading, this should be unset for the
        default execution mode. This variable should be used for
        non standard modes (eg: testing).
        :type args: List
        :param args: The list of string based arguments coming
        from a command line system that should condition/control
        the mode based execution.
        :type callback: Function
        :param callback: The callback function to be called at the
        end of the current plugin manager's loading process. This
        may be used to execute final operations in it.
        :rtype: int
        :return: The return code from the execution, this value
        should be zero for no problem situation and any other
        value for an error situation.
        """

        try:
            # saves the initial time for the starting of the system
            # this value is going to be used to calculate the delta
            initial = time.time()

            # prints an info message about the initialization of
            # of the plugin manager, this should be one of the
            # first logging messages printed by the system
            self.info("Starting plugin manager...")
            self.info("Using %s run mode and %s layout mode" %
                (self.run_mode, self.layout_mode))

            # sets the plugin manager timestamp, should set it with
            # the current time (to be used for uptime calculus)
            self.set_timestamp()

            # applies the set of fixes for the context
            # of execution of the plugin system
            self.apply_fixes()

            # updates the workspace path and then checks the standard
            # input, replacing it with a non blocking support if required
            self.update_workspace_path()
            self.check_standard_input()

            # generates the system information map, that is going to be used
            # as the primary "solution" in the retrieval of system information
            self.generate_system_information_map()

            # iterates over the complete set of paths registered as base
            # paths for plugin loading, trying to find the plugin modules
            for plugin_path in self.plugin_paths:
                # retrieves all the modules from the plugin path and uses them
                # to extend the referred modules list
                plugin_path_modules = self.get_all_modules(plugin_path, suffix = "plugin")
                self.referred_modules.extend(plugin_path_modules)

            # defines the plugin system configuration, consisting of a map
            # containing directives that will condition the initialization
            configuration = dict(
                mode = mode,
                args = args,
                library_paths = self.library_paths,
                meta_paths = self.meta_paths,
                plugin_paths = self.plugin_paths,
                plugins = self.referred_modules
            )

            # starts the plugin loading process, this should create the
            # plugin instances and load the ones required to be loading
            # it should also execute the finish boot tasks (if required)
            self.init_plugin_system(configuration)

            # retrieves the current time as the final one and then uses
            # it to calculate the delta (used time) rounding into into
            # an integer value so that it's printed accordingly
            final = time.time()
            delta = int(final - initial)

            # prints an information message about the ending of the
            # plugin system startup process, this message should mark
            # the readiness of the system to received actions
            self.info("Startup process finished (took %d seconds)" % delta)

            # in case a callback function is defined for the end of the
            # loading process it must be correctly called (with no arguments)
            if callback: callback()

            # starts the main loop, this is a blocking call that should
            # return only at the end of the plugin manger life cycle
            self.main_loop()
        except BaseException as exception:
            # handles the system exception and changes the return code of
            # the call to an error value (notifies caller process)
            self._handle_system_exception(exception)
            self.return_code = 1

        # returns the return code, this value should be zero in case no
        # error has occurred or any other value otherwise
        return self.return_code

    def unload_system(self, thread_safe = True):
        """
        Unloads the plugin system from memory, exiting the system.
        A timer is installed to exit the system in a forced way
        (avoid locking of the process resources).

        :type thread_safe: bool
        :param thread_safe: If the unloading should use the event mechanism
        to provide thread safety.
        """

        # in case the system initialization is not complete
        # raises a colony exception to notify the problem
        if not self.init_complete:
            raise exceptions.ColonyException("trying to unload uninitialized plugin system")

        # creates the kill system timer, to kill the system
        # if it hangs in shutdown and starts it so that the
        # system will be able to kill itself after a timeout
        self.kill_system_timer = threading.Timer(
            DEFAULT_UNLOAD_SYSTEM_TIMEOUT,
            self._kill_system_timeout
        )
        self.kill_system_timer.start()

        # iterates over all the plugin instances running the unload process
        # for all of them and according to their set of skill/capabilities
        for plugin_instance in self.plugin_instances:

            # in case the plugin instance is not loaded there's
            # no need to unload it from the current context and
            # the current iteration step may be skipped
            if not plugin_instance.is_loaded(): continue

            # in case the current plugin instance is of type main
            # the special main type unloading process should be used
            if MAIN_TYPE in plugin_instance.capabilities:
                self._unload_plugin(plugin_instance, unloading_type = MAIN_TYPE)

            # otherwise in case the plugin is thread based the also
            # special mode for threads should be used instead
            elif THREAD_TYPE in plugin_instance.capabilities:
                self._unload_plugin(plugin_instance, unloading_type = THREAD_TYPE)

            # otherwise it should be a "normal" plugin and the normal
            # process for the plugin unloading should be used instead
            else: self._unload_plugin(plugin_instance)

        # in case thread safety is requested
        if thread_safe:
            # creates the exit event and adds it to the
            # event queue to be executed in back thread
            exit_event = util.QueueEvent("exit")
            self.add_event(exit_event)
        else:
            # unloads the thread based plugins
            self._unload_thread_plugins()

        # cancels the kill system timer
        self.kill_system_timer.cancel()

    def reload_system(self, thread_safe = True):
        """
        Reloads the current plugin system, all the memory resources
        are releases and then the process is restarted.

        :type thread_safe: bool
        :param thread_safe: If the unloading should use the event mechanism
        to provide thread safety.
        """

        # unloads the system
        self.unload_system(thread_safe)

        # re-launches the system (with the
        # new settings)
        self._relaunch_system()

    def main_loop(self, timeout = 1.0):
        """
        The main loop for the plugin manager, this is the call that
        is considered to be blocking most of the manager's time.

        :type timeout: float
        :param timeout: The timeout that is going to be used as part
        of the wait condition for the event queue of the main loop
        the bigger this value the greater time to respond.
        """

        # runs the plugin manager's main loop while the proper
        # active flag is set, this is used as the primary control
        # structure to be used for disabling the manager
        while self.main_loop_active:

            # acquires the condition so that the event queue
            # may be accessed in a safe fashion
            self.condition.acquire()

            # iterates while the event queue has no items waiting
            # for new items to arrive and be processed
            while not len(self.event_queue):
                try:
                    # waits for the condition to be notified
                    # this wait releases after the defined timeout
                    # in order to provide a away to process external interrupts
                    self.condition.wait(timeout)
                except RuntimeError: pass

            # pops the top item from the event queue and "redirect"
            # it for the processing phase of the workflow
            event = self.event_queue.pop(0)

            # in case the event is of type execute a method should
            # be executed with the argument that are part of the event
            if event.event_name == "execute":
                method = event.event_args[0]
                args = event.event_args[1:]
                method(*args)

            # in case the event is of type exit, the unloading
            # of the plugin system should be triggered
            elif event.event_name == "exit":
                # unloads the thread based plugins and then
                # returns the current control flow to caller
                self._unload_thread_plugins()
                return

            # releases the condition
            self.condition.release()

    def add_event(self, event):
        """
        Adds an event to the list of events in the plugin manager.

        The proper thread synchronization mechanisms are going to
        be used to ensure that the adding of the event is thread
        safe as expected by the specification

        :type event: Event
        :param event: The event to add to the list of events in
        the plugin manager.
        """

        # acquired the proper condition, then adds the event
        # to the proper queue, notifies and releases the condition
        # providing a safe access to the underlying queue
        self.condition.acquire()
        self.event_queue.append(event)
        self.condition.notify()
        self.condition.release()

    def expand_workspace_path(self):
        """
        Expands the workspace path, in order to
        avoid possible problems when accessing the colony
        workspace.
        """

        # expands the workspace path, meaning that if this
        # is an user related directory it will be expanded
        # into a fully (normalized) path
        self.workspace_path = os.path.expanduser(self.workspace_path)

    def create_workspace_path(self):
        """
        Creates the workspace path, in case it does
        not exists already.
        """

        # in case the workspace path already exists in the
        # current file system returns the control flow otherwise
        # starts the creation of the proper directory
        if os.path.exists(self.workspace_path): return
        os.mkdir(self.workspace_path)

    def update_workspace_path(self):
        """
        Updates the workspace path, expanding the workspace
        path and creating the workspace path if necessary.
        """

        # expands the workspace path to obtain a valid one an then
        # creates the workspace path directory if required
        self.expand_workspace_path()
        self.create_workspace_path()

    def check_standard_input(self):
        """
        Checks if the standard input to be used should
        be changed to a wait one in order to avoid possible
        blocking.
        """

        # verifies if the current execution mode requires a detached
        # support for the standard input and if that's not the case
        # replaces the current standard input with the wait input (no blocking)
        is_detached = self.daemon_pid or self.daemon_file_path
        if not is_detached: return
        sys.stdin = util.WaitInput()

    def apply_fixes(self):
        """
        Applies a series of fixes to the current environment
        so that operations from this point on will be using an
        uniform set of features.

        Most of the fixes use a "monkey patching" approach and
        should be used carefully to avoid unwanted behavior.
        """

        # applies the round fix so that all the python interpreter
        # version use an uniform rounding strategy and avoid the
        # typical errors for rounding operations
        colony.libs.round_apply()

    def get_all_modules(self, path, suffix = None):
        """
        Retrieves all the modules in a given path, the modules
        are considered to be the files that have the correct
        python file extension.

        An optional argument may be provided to filter the modules
        to be retrieved to the ones that match the proved suffix.

        :type path: String
        :param path: The path to retrieve the modules.
        :type suffix: String
        :param suffix: The optional suffix argument used to filter
        the modules according to their suffix in the name.
        :rtype: List
        :return: All the modules in the given path.
        """

        # starts the modules list, that will contain the complete set
        # of modules for the requested suffix value
        modules = []

        # in case the path does not exist
        if not os.path.exists(path):
            self.warning("Path '%s' does not exist in the current filesystem" % (path))
            return modules

        # retrieves the directory list for the path, this should
        # provide the complete set of file names in the directory
        dir_list = os.listdir(path)

        # iterates over all the file names
        # in the directory list
        for file_name in dir_list:
            # creates the full file path
            full_path = path + "/" + file_name

            # retrieves the file mode
            mode = os.stat(full_path)[stat.ST_MODE]

            # in case the current file in iteration
            # is a directory no need to continue, must
            # skip the current iteration
            if stat.S_ISDIR(mode): continue

            # splits the name of the file currently in
            # iteration and retrieves the extension from it
            module_name, extension = os.path.splitext(file_name)

            # in case the extension of the file is not a valid
            # one must skip the current iteration
            if not extension in (".py", ".pyc"): continue
            if suffix and not module_name.endswith(suffix): continue

            # checks if the module name is currently present
            # in the list of modules and in case it's not
            # adds the module into it
            if not module_name in modules: modules.append(module_name)

        # returns the modules list, containing the complete set of
        # modules that respect the provided set of rules
        return modules

    def init_plugin_system(self, configuration):
        """
        Starts the plugin loading process, this should be the step to
        start the various plugins classes and instances.

        It should also start the various conditional modes that may
        be activated through proper configuration.

        :type configuration: Dictionary
        :param configuration: The configuration structure that is going
        to be used for the conditional execution of the loading process.
        """

        # unpacks the complete set of configuration items that
        # are going to be used in the plugin system initialization
        mode = configuration.get("mode", None)
        args = configuration.get("args", None)
        library_paths = configuration.get("library_paths", [])
        plugin_paths = configuration.get("plugin_paths", [])
        plugins = configuration.get("plugins", [])

        # adds the defined library and plugin paths to the system python path
        self.set_python_path(library_paths, plugin_paths)

        # loads the plugin files into memory, this operation should import
        # the complete set of files that are considered to be part of the plugin
        self.load_plugins(plugins)

        # starts all the available the plugin manager plugins, loads them all
        # and set sets the plugin manager plugins as loaded in the system
        self.start_plugin_manager_plugins()
        self.load_plugin_manager_plugins()
        self.set_plugin_manager_plugins_loaded(True)

        # starts all the available the plugins, this operation should create
        # the singletons instances for all of the available plugin classes
        self.start_plugins()

        # loads the startup and the main plugins, the first represent the
        # plugins that should always run and the second the ones that trigger
        # a new thread loading and should also start at boot time
        self.load_startup_plugins()
        self.load_main_plugins()

        # installs the signal handlers, that are going to be used for operations
        # like the "killing" of the plugin system and others
        self.install_signal_handlers()

        # sets the init flag to true and then notifies the complete set
        # of targets for the notification of the end plugin system loading
        self.set_init_complete(True)
        self.notify_load_complete_loaded_plugins()
        self.notify_load_complete_handlers()
        self.notify_daemon_file()

        # runs the complete set of conditional modes for the initialization
        # of the system taking into account the mode configuration value note
        # that if the mode is not found or invalid and exception is raised
        self.exec_mode(mode, args = args)

    def set_python_path(self, library_paths, plugin_paths):
        """
        Updates the python path adding the defined list of library and plugin paths.

        :type library_paths: List
        :param library_paths: The list of library paths to add to the python path.
        :type plugin_paths: List
        :param plugin_paths: The list of plugin paths to add to the python path.
        """

        # iterates over all the library paths in library paths
        # to insert them into the appropriate interpreter
        # structures for further loading of the modules
        for library_path in library_paths:
            # in case the library path already exits in the
            # system path no need to continue with the process
            if library_path in sys.path: continue

            # normalizes the library path and inserts the
            # library path into the system path so that the
            # modules from it may be imported
            library_path = os.path.normpath(library_path)
            sys.path.insert(0, library_path)

        # iterates over all the plugin paths in plugin paths
        # to insert them into the appropriate interpreter
        # structures for further loading of the modules
        for plugin_path in plugin_paths:
            # in case the plugin path already exits in the
            # system path no need to continue with the process
            if plugin_path in sys.path: continue

            # normalizes the plugin path and inserts the
            # library path into the system path so that the
            # modules from it may be imported
            plugin_path = os.path.normpath(plugin_path)
            sys.path.insert(0, plugin_path)

    def load_plugins(self, plugins):
        """
        Runs the import module operation for each of the
        provided plugin items.

        The provided plugins should be a series of string
        based full module path values.

        :type plugins: List
        :param plugins: The list of plugins to be loaded
        these should be string based module references.
        """

        # prints an info message about the import operation
        # that is going to be performed in the plugin
        self.info("Loading plugins (importing %d main module files)..." % len(plugins))

        # iterates over all the plugins requested for loading and
        # runs the import operation for each of them in case that
        # operation is required by module inexistence
        for plugin in plugins:
            # in case the plugin module is already loaded continues
            # the loop as no loading is required for it, otherwise
            # runs the proper loading process for the plugin logging
            # an error in case an exception occurs in the importing
            if plugin in sys.modules: continue
            try: __import__(plugin)
            except Exception as exception:
                self.error("Problem importing module %s: %s" % (plugin, legacy.UNICODE(exception)))

        # prints an info message about the fact that the loading
        # operation for all of the requested plugin has finished
        self.info("Finished loading plugins")

    def start_plugin_manager_plugins(self):
        """
        Starts all the available plugin manager plugins, creating a
        singleton instance for each of them.
        """

        # retrieves all the plugin manager plugin classes available
        self.plugin_classes = self.get_all_plugin_classes(PluginManagerPlugin)

        # iterates over all the available plugin manager plugin classes
        for plugin in self.plugin_classes:
            # retrieves the plugin id
            plugin_id = plugin.id

            # sets the plugin class in the plugin classes map
            self.plugin_classes_map[plugin_id] = plugin

            # tests the plugin for loading, verifying that it's
            # current loaded and then starts the plugin
            if not plugin in self.loaded_plugins: continue
            self.start_plugin(plugin)

    def start_plugins(self):
        """
        Starts all the available plugins, creating a singleton
        instance for each of them.
        """

        # retrieves all the plugin classes available
        self.plugin_classes = self.get_all_plugin_classes()

        # iterates over all the available plugin classes
        for plugin in self.plugin_classes:
            # retrieves the plugin id
            plugin_id = plugin.id

            # sets the plugin class in the plugin classes map
            self.plugin_classes_map[plugin_id] = plugin

            # starts the plugin (creating the singleton) in
            # case the plugin is not currently loaded
            if not plugin in self.loaded_plugins: self.start_plugin(plugin)

    def start_plugin(self, plugin, use_path = True):
        """
        Starts the given plugin, creating a singleton instance.
        This method should also manipulate the created singleton
        by adding some attributes to it.

        :type plugin: Class
        :param plugin: The plugin to start.
        :type use_path: bool
        :param use_path: If the file path of the main plugin file
        should be used to infer the short name of the plugin.
        """

        # retrieves the plugin id and description for the plugin
        # to be started (main identification values)
        plugin_id = plugin.id
        plugin_description = plugin.description

        # instantiates the plugin to create the singleton plugin instance
        plugin_instance = plugin(self)

        # retrieves the path to the plugin file
        plugin_path = inspect.getfile(plugin)

        # retrieves the file system encoding
        file_system_encoding = sys.getfilesystemencoding()

        # decodes the plugin path using the file system encoding
        # and retrieves the absolute path from this value
        plugin_path = plugin_path.decode(file_system_encoding) if\
            legacy.is_bytes(plugin_path) else plugin_path
        absolute_plugin_path = os.path.abspath(plugin_path)

        # retrieves the path to the directory containing the plugin file
        plugin_dir = os.path.dirname(absolute_plugin_path)

        # in case the (file) path mode is enabled uses the name of the file
        # where the plugin class is defined to name the plugin, this is considered
        # to be the "safest" approach as it allows more flexibility in plugin name
        if use_path:
            plugin_name = os.path.splitext(os.path.basename(inspect.getfile(plugin)))[0][:-7]

        # retrieves the name of the plugin as the name of the class converted
        # to the underscore version of it and then removes the last part of
        # the string that contains the plugin suffix (this plugin name value
        # will be used for rapid retrieval of the plugin)
        else:
            plugin_name = colony.libs.to_underscore(plugin.__name__)[:-7]

        # updates the "private" name reference in the plugin with the one that
        # has just been computed using the target strategy
        plugin._name = plugin_name

        # sets the plugin instance reference in the plugins object, this will
        # allow a direct attribute access to the plugins instance
        setattr(self.plugins, plugin_name, plugin_instance)

        # sets the short name attribute in the plugin class indicating the name
        # associated with the plugin, this setting provides a simple shortcut
        # to access the short name concept for within the plugin instance
        setattr(plugin, "short_name", plugin_name)

        # starts all the plugin manager structures related with plugins
        self.loaded_plugins.append(plugin)
        self.loaded_plugins_map[plugin_id] = plugin
        self.loaded_plugins_id_map[plugin_id] = self.current_id
        self.id_loaded_plugins_map[self.current_id] = plugin_id
        self.loaded_plugins_descriptions.append(plugin_description)
        self.plugin_instances.append(plugin_instance)
        self.plugin_instances_map[plugin_id] = plugin_instance
        self.plugin_names_map[plugin_name] = plugin_instance
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

        :type plugin_id: String
        :param plugin: The id of the plugin to be removed from the plugin system.
        """

        # retrieves the referring plugin module
        module = self.get_plugin_module_name_by_id(plugin_id)

        # stops the referring plugin module
        self.stop_module(module)

    def stop_module(self, module):
        """
        Stops the given plugin module in the plugin manager.

        :type module: String
        :param module: The name of the plugin module to stop.
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

        :type plugin: Plugin
        :param plugin: The plugin to be removed from the plugin system.
        """

        # retrieves the plugin id and version and then retrieves
        # the "hidden" name value that should be computed at the
        # plugin starting time
        plugin_id = plugin.id
        plugin_description = plugin.description
        plugin_name = plugin._name

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

        # removes the previously set plugin instance reference from the
        # plugins object (no further access allowed)
        delattr(self.plugins, plugin_name)

        # removes all the plugin class resources
        self.loaded_plugins.remove(plugin)
        del self.loaded_plugins_map[plugin_id]
        del self.loaded_plugins_id_map[plugin_id]
        del self.id_loaded_plugins_map[current_id]
        self.loaded_plugins_descriptions.remove(plugin_description)

        # removes the generic plugin instance resources
        self.plugin_instances.remove(plugin_instance)
        del self.plugin_instances_map[plugin_id]
        del self.plugin_names_map[plugin_name]
        del self.plugin_dirs_map[plugin_id]

        # unregisters the plugin capabilities in the plugin manager
        self.unregister_plugin_capabilities(plugin_instance)

        # in case the plugin exists in the plugin threads map
        if plugin_id in self.plugin_threads_map:
            # retrieves the available thread for the plugin
            plugin_thread = self.plugin_threads_map[plugin_id]

            # creates the plugin exit event
            event = util.QueueEvent("exit")

            # adds the load event to the thread queue
            plugin_thread.add_event(event)

            # joins the plugin thread
            plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)

            # removes the plugin thread from the plugin threads map
            del self.plugin_threads_map[plugin_id]

    def add_plugin_path(self, plugin_path, persist = False):
        """
        Adds the given plugin path to the plugin paths
        registry for manager use.
        Optionally the plugin path may be persisted to the
        plugin paths file.

        :type plugin_path: String
        :param plugin_path: The plugin path to be added.
        :type persist: bool
        :param persist: If the plugin path should be persisted
        to the plugin paths file.
        """

        # adds the plugin path to the plugin paths
        self.plugin_paths.append(plugin_path)

        # in case the persist flag is set
        # persists the plugin path
        persist and self.persist_plugin_path(plugin_path)

    def remove_plugin_path(self, plugin_path):
        """
        Removes the given plugin path from the plugin paths
        registry for manager use.

        :type plugin_path: String
        :param plugin_path: The plugin path to be removed.
        """

        # removes the plugin path from the plugin paths
        self.plugin_paths.remove(plugin_path)

    def persist_plugin_path(self, plugin_path):
        """
        Persists the given plugin path into the plugin
        paths file, for later usage.

        :type plugin_path: String
        :param plugin_path: The plugin path to be persisted
        in the plugin paths file.
        """

        # retrieves the plugin paths file path
        plugin_paths_file_path = self.get_plugin_paths_file_path()

        # converts the plugin path to the best (possible)
        # plugin path, possibly a relative one
        plugin_path = self._get_best_plugin_path(plugin_path)

        # opens the plugin paths file for appending
        plugin_paths_file = open(plugin_paths_file_path, "a")

        try:
            # writes the plugin path and a new line separator
            plugin_paths_file.write(plugin_path + "\n")
        finally:
            # closes the plugin paths file
            plugin_paths_file.close()

    def get_all_plugin_classes(self, base_plugin_class = Plugin):
        """
        Retrieves all the available plugin classes, from the defined base plugin class.

        :type base_plugin_class: Class
        :param base_plugin_class: The base plugin class to retrieve the plugin classes.
        :rtype: List
        :return: The list of plugin classes.
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

        :type plugin: Class
        :param plugin: The plugin class to retrieve the sub classes.
        :type plugin_classes: List
        :param plugin_classes: The current list of plugin sub classes.
        :rtype: List
        :return: The list of all the sub classes for the given plugin class.
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

        :type plugin: Plugin
        :param plugin: The plugin to register the capabilities.
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

        :type plugin: Plugin
        :param plugin: The plugin to unregister the capabilities.
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

        for plugin in self.plugin_instances:
            if not PLUGIN_MANAGER_EXTENSION_TYPE in plugin.capabilities: continue
            self._load_plugin(plugin, loading_type = PLUGIN_MANAGER_EXTENSION_TYPE)

    def load_startup_plugins(self):
        """
        Loads the set of startup plugins, starting the system bootup process.
        """

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # searches for the startup type in the plugin capabilities
            # in case the plugins contains such capability must load
            # it because it's considered to be a startup plugin
            if STARTUP_TYPE in plugin.capabilities: self._load_plugin(plugin, loading_type = STARTUP_TYPE)

    def load_main_plugins(self):
        """
        Loads the set of main plugins, starting the system bootup process.
        """

        # iterates over all the plugin instances
        for plugin in self.plugin_instances:
            # searches for the main type in the plugin capabilities
            # in case the plugins contains such capability must load
            # it because it's considered to be a main plugin
            if MAIN_TYPE in plugin.capabilities: self._load_plugin(plugin, loading_type = MAIN_TYPE)

    def install_signal_handlers(self):
        """
        Installs the signal handlers for the plugin
        manager.
        """

        # in case the installation of the signal handlers is
        # currently disabled returns immediately avoids the
        # registration of the handlers
        if not self.install_signals: return

        # installs the sigterm handler for plugin manager kill
        # (may create problems with existing handlers)
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
        # there's no need to notify the file, must return
        # immediately to the caller method
        if not self.daemon_file_path: return

        # opens the file in write mode, so that it's possible
        # to write the pid value into it
        file = open(self.daemon_file_path, "wb")

        try:
            # in case the daemon pid is defined sets the
            # pid value with this value
            if self.daemon_pid: pid = self.daemon_pid
            # otherwise must retrieve the current process
            # pid value and use it instead
            else: pid = os.getpid()

            # converts the pid to string and write it into
            # the file (notification process)
            pid_string = str(pid)
            file.write(pid_string)
        finally:
            # closes the file, no further writing is allowed
            # on this file (avoids leaks)
            file.close()

    def exec_mode(self, mode, args = None):
        """
        Executes the provided mode of execution but only if
        the valid is correctly defined and the proper method
        for the running is defined in the manager.

        An exception will be raised in case the proper run method
        is not defined "inside" the manager.

        :type mode: String
        :param mode: The (execution) mode that is going to be
        used for the performing of the execution, should be
        a valid one and defined in the manager.
        :type args: List
        :param args: The arguments (coming from command line)
        that may be used to control/customize the execution
        of the target run mode, these values should consist
        of plain strings (to be casted at execution time).
        """

        if not mode: return
        if not hasattr(self, "run_" + mode): raise exceptions.ColonyException(
            "execution mode '%s' not found or invalid" % mode
        )
        self.info("Executing mode '%s'..." % mode)
        if self.exec_delay:
            self.info("Sleeping for %.2f seconds..." % self.exec_delay)
            time.sleep(self.exec_delay)
        args = args or ()
        method = getattr(self, "run_" + mode)
        method(args = args)

    def run_test(self, verbosity = 2, raise_e = True, args = []):
        """
        Runs the test mode for the current plugin manager, this should
        consist on the retrieval of the test capability aware plugins
        and running of the corresponding test.

        The method should return a boolean value indicating if the complete
        set of tests were correctly executed or not.

        :type verbosity: int
        :param verbosity: The amount of verbosity (larger more verbose)
        that is going to be used in the test runner.
        :type raise_e: bool
        :param raise_e: If an exception should be raised in case the tests
        execution process fails (one or more tests failed).
        :type args: List
        :param args: Sequence containing a series of string based arguments
        coming from the command line, these should be used to condition the
        way the method is going to perform its execution.
        :rtype: bool
        :return: If the execution of the unit tests from the proper plugins
        was successful or not, the details of the execution should be read
        from the currently defined standard output stream.
        """

        # starts the initial result value of the execution with the valid
        # value as the execution is considered to be successful by default
        result = True

        # verifies if any (command line) argument was provided if that's the
        # case tries to retrieve the associated plugins, otherwise retrieves
        # the complete set of "testable" plugins (all of them are going to run)
        if args: plugins = [self.get_plugin(arg) for arg in args]
        else: plugins = self.get_plugins_by_capability("test")

        # iterates over the complete set of plugins that are meant to be tested
        # and performs the unit testing for all of them (may take some time)
        for plugin in plugins:
            # verifies if the plugin (instance) is valid and if that's not the
            # case raises an exception because a very serious underlying problem
            # has occurred and notification is required
            if not plugin: raise exceptions.ColonyException(
                "problem loading a plugin for unit test execution"
            )

            # in case there's a valid while list defined then verifies that
            # the current plugin in iteration is valid by checking that either
            # the plugin's ID or name is present in the list
            if self.whitetest and not plugin.id in self.whitetest and\
                not plugin.name in self.whitetest:
                continue

            # verifies if the identifier or the short name of the plugin
            # are present in the black list for testing, if that's the case
            # the current plugin is skipped as no test is meant to be executed
            if plugin.id in self.blacktest: continue
            if plugin.short_name in self.blacktest: continue

            # in case the current plugin in iteration is not loaded, it's
            # not possible to load it's unit tests and so an exception must
            # be raised indicating that the issue preventing the plugin
            # from being loaded should be solved before unit test execution
            if not plugin.is_loaded(): raise exceptions.ColonyException(
                "failed to load '%s' v%s for unit test execution" %
                (plugin.id, plugin.version)
            )

            # creates a new test suite and a new loader instances that are
            # going to be used to load the tests for the current plugin
            suite = unittest.TestSuite()
            loader = unittest.TestLoader()

            # retrieves the bundle of test cases from the plugin and then
            # adds the corresponding tests to the suite (for execution)
            for test_case in plugin.test.get_bundle():
                test_case.plugin = plugin
                partial = loader.loadTestsFromTestCase(test_case)
                suite.addTest(partial)

            # creates the unit test runner and then runs the created suite
            # retrieving the final execution result that is used to compute
            # the result boolean value for the test execution
            runner = unittest.TextTestRunner(verbosity = verbosity)
            run_result = runner.run(suite)
            result = result and not run_result.errors
            result = result and not run_result.failures

        # unsets the main loop as active so that the current execution workflow
        # is avoided and the process workflow returned to the caller process
        self.main_loop_active = False

        # in case the raise (exception) flag is set and the result is invalid
        # and exception must be raised indicating the execution problem
        if raise_e and not result: raise exceptions.ColonyException(
            "failed to execute some of the unit tests"
        )

        # returns the "final" result value for the execution, taking into
        # account that one "simple" error will return invalid as boolean
        return result

    def __load_plugin(self, plugin, type = None, loading_type = None):
        """
        Loads the given plugin with the given type and loading type.
        The loading of the plugin consists the loading of the plugin itself (_load_plugin)
        and in the registration of the plugin in all the plugins that allow it.

        :type plugin: Plugin
        :param plugin: The plugin to be loaded.
        :type type: String
        :param type: The type of plugin to be loaded.
        :type loading_type: String
        :param loading_type: The loading type to be used.
        :rtype: bool
        :return: The result of the plugin load.
        """

        # in case the plugin is already loaded, there's no need
        # to continue with the loading process, returns immediately
        if plugin.is_loaded(): return True

        # in case the plugin is lazy loaded
        if (plugin.loading_type == LAZY_LOADING_TYPE and\
            not type == FULL_LOAD_TYPE) and plugin.is_lazy_loaded():
            return True

        # in case the plugin does not pass the test plugin load
        if not self.test_plugin_load(plugin):
            # prints an info message about the fact that the plugin
            # is not ready to be loaded and returns in error
            self.info("Plugin '%s' v%s not ready to be loaded" % (plugin.name, plugin.version))
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
        The loading of the plugin consists in the test for pre-conditions
        (dependencies),
        creation of thread (if necessary), loading (if necessary) and
        injection of dependencies, loading  of the plugin resources and
        loading (if necessary) and injection of allowed plugins.

        :type plugin: Plugin
        :param plugin: The plugin to be loaded.
        :type type: String
        :param type: The type of plugin to be loaded.
        :type loading_type: String
        :param loading_type: The loading type to be used.
        :rtype: bool
        @requires: The result of the plugin load.
        """

        # generates the init load plugin event
        self.generate_event("plugin_manager.init_load_plugin", [plugin.id, plugin.version, plugin])

        # in case there is an handler for the plugin loading
        if self.exists_plugin_manager_plugin_execute_conditional("_load_plugin", [plugin, type, loading_type]):
            return self.plugin_manager_plugin_execute_conditional("_load_plugin", [plugin, type, loading_type])

        # in case the return from the handler of the initialization
        # of the plugin load returns in error must propagate this
        # error to the caller method
        if not self.plugin_manager_plugin_execute("init_plugin_load", [plugin, type, loading_type]):
            return False

        # in case the plugin is already loaded no need
        # to load it again, returns in success
        if plugin.is_loaded(): return True

        # in case the plugin is lazy loaded and lazy loading
        # is allowed in context the method should return
        if (plugin.loading_type == LAZY_LOADING_TYPE and not type == FULL_LOAD_TYPE) and plugin.is_lazy_loaded():
            return True

        # in case the plugin load is not successful
        if not self.test_plugin_load(plugin):
            # prints the error message and returns the control flow
            # to the caller method in error
            self.info(
                "Plugin '%s' v%s not ready to be loaded" %
                (plugin.name, plugin.version)
            )
            return False

        # in case a type is defined, prints an information
        # message about this loading type
        if type: self.debug("Loading of type: '%s'" % (type))

        # in case the plugin to be loaded is either of type main or thread
        if loading_type == MAIN_TYPE or loading_type == THREAD_TYPE:

            if plugin.id in self.plugin_threads_map:
                # retrieves the available thread for the plugin
                plugin_thread = self.plugin_threads_map[plugin.id]

                # prints a debug message
                self.debug("Thread restarted for plugin '%s' v%s" % (plugin.name, plugin.version))
            else:
                # creates a new tread to run the main plugin
                plugin_thread = PluginThread(plugin)

                # starts the thread
                plugin_thread.start()

                # adds the plugin thread to the plugin threads list
                self.plugin_threads.append(plugin_thread)

                # sets the plugin thread in the plugin threads map
                self.plugin_threads_map[plugin.id] = plugin_thread

                # prints a debug message
                self.debug("New thread started for plugin '%s' v%s" % (plugin.name, plugin.version))

            # sets the plugin load as not completed
            plugin_thread.set_load_complete(False)

            # in case the loading type of the plugin is eager
            if plugin.loading_type == EAGER_LOADING_TYPE or type == FULL_LOAD_TYPE:
                # creates the plugin load event
                event = util.QueueEvent("load")
            else:
                # creates the plugin lazy load event
                event = util.QueueEvent("lazy_load")

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
                except Exception as exception:
                    # sets the exception in the plugin and then sets the error
                    # state flag in it, properly identifying the issue
                    plugin.exception = exception
                    plugin.error_state = True

        # in case the plugin is in an error state
        if plugin.error_state:
            # prints the error message and returns the control flow
            # to the caller method in error
            self.error(
                "Problem loading plugin '%s' v%s '%s'" %
                (plugin.name, plugin.version, legacy.UNICODE(plugin.exception))
            )
            return False

        # in case the loading type is lazy, the loading task is complete
        if plugin.loading_type == LAZY_LOADING_TYPE and not type == FULL_LOAD_TYPE:
            return True

        # resolves the capabilities of the plugin
        if not self.resolve_capabilities(plugin): return False

        # injects the plugin dependencies
        if not self.inject_dependencies(plugin): return False

        # in case the plugin to be loaded is either of type main or thread
        if loading_type == MAIN_TYPE or loading_type == THREAD_TYPE:
            # sets the plugin end load as not completed
            plugin_thread.set_end_load_complete(False)

            # creates the plugin end load event
            event = util.QueueEvent("end_load")

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
                except Exception as exception:
                    # sets the exception and the error state flag in
                    # the plugin so that the loading process is properly
                    # handled at the "front" of the operation
                    plugin.exception = exception
                    plugin.error_state = True

        # in case the plugin is in an error state, there's a problem
        # with the end loading process and the caller method must be
        # notified about the problem (to act on it)
        if plugin.error_state:
            # prints the error message and returns the control flow
            # to the caller method in error
            self.error(
                "Problem end loading plugin '%s' v%s '%s'" %
                (plugin.name, plugin.version, legacy.UNICODE(plugin.exception))
            )
            return False

        # injects the allowed plugins into the plugin and verifies that
        # everything went as expected in such injection
        if not self.inject_allowed(plugin): return False

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

        :type plugin: Plugin
        :param plugin: The plugin to be unloaded.
        :type type: String
        :param type: The type of plugin to be unloaded.
        :type loading_type: String
        :param unloading_type: The unloading type to be used.
        :rtype: bool
        @requires: The result of the plugin unload.
        """

        # in case the plugin is not loaded, there's no need to start
        # the unloading process for it and so it must return immediately
        if not plugin.is_loaded(): return True

        # in case an (unloading) type is defined a proper debug message
        # must be printed to notify the end user about the unloading
        if type: self.debug("Unloading of type: '%s'" % (type))

        # unloads the plugins that depend on the plugin being unloaded
        # this is required because if a plugins depends on the current
        # plugin to be unloaded its dependencies will not be met after
        for dependent_plugin in self.get_plugin_dependent_plugins_map(plugin.id):
            if not dependent_plugin.is_loaded(): continue
            if MAIN_TYPE in dependent_plugin.capabilities:
                self._unload_plugin(dependent_plugin, DEPENDENCY_TYPE, MAIN_TYPE)
            elif THREAD_TYPE in dependent_plugin.capabilities:
                self._unload_plugin(dependent_plugin, DEPENDENCY_TYPE, THREAD_TYPE)
            else:
                self._unload_plugin(dependent_plugin, DEPENDENCY_TYPE)

        # notifies the allowed plugins about the unload
        for allowed_plugin_info in self.get_plugin_allowed_plugins_map(plugin.id):
            # retrieves both the allowed plugin and the associated
            # capability for which it was loaded for
            allowed_plugin = allowed_plugin_info[0]
            allowed_capability = allowed_plugin_info[1]

            # verifies if the allowed plugin is loaded and in case it's
            # not continues the loop as there's nothing to be done,
            # otherwise starts the unloading of the allowed plugin
            if not allowed_plugin.is_loaded(): continue
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
            event = util.QueueEvent("unload")

            # adds the unload event to the thread queue
            plugin_thread.add_event(event)

            # acquires the ready semaphore for the beginning of the unloading process
            plugin.acquire_ready_semaphore()
        # otherwise it's a normal plugin type unload
        else:
            try:
                # calls the unload plugin method in the plugin (plugin shutdown process)
                plugin.unload_plugin()
            except Exception as exception:
                # prints the error message then sets the exception on the
                # plugin and sets its error state
                self.error("There was an exception: %s" % legacy.UNICODE(exception))
                plugin.exception = exception
                plugin.error_state = True

        # in case the plugin is in an error state
        if plugin.error_state:
            # prints the error message and returns the control flow
            # to the caller method in error
            self.error(
                "Problem unloading plugin '%s' v%s '%s'" %
                (plugin.name, plugin.version, legacy.UNICODE(plugin.exception))
            )
            return False

        # if it's a main or thread type unload
        if unloading_type == MAIN_TYPE or unloading_type == THREAD_TYPE:
            # retrieves the available thread for the plugin
            plugin_thread = self.plugin_threads_map[plugin.id]

            # sets the plugin end unload as not completed
            plugin_thread.set_end_unload_complete(False)

            # creates the plugin end unload event
            event = util.QueueEvent("end_unload")

            # adds the end unload event to the thread queue
            plugin_thread.add_event(event)

            # acquires the ready semaphore for the beginning of the end unloading process
            plugin.acquire_ready_semaphore()
        else:
            try:
                # calls the end unload plugin method in the plugin (plugin shutdown process)
                plugin.end_unload_plugin()
            except Exception as exception:
                # sets the exception in the plugin and then sets the
                # plugin error state flag, indicating that a problem occurred
                plugin.exception = exception
                plugin.error_state = True

        # in case the plugin is in an error state
        if plugin.error_state:
            # prints the error message and returns the control flow
            # to the caller method in error
            self.error(
                "Problem end unloading plugin '%s' v%s %s" %
                (plugin.name, plugin.version, legacy.UNICODE(plugin.exception))
            )
            return False

        # returns true
        return True

    def _unload_thread_plugins(self):
        """
        Unloads all the thread based plugins, unblocking them
        from the current workload. This is a blocking operation
        that may take some time to be finished.
        """

        # creates the exit event that will be used to "kill"
        # each of the plugin threads that is running
        exit_event = util.QueueEvent("exit")

        # iterates over all the available plugin threads
        # joining all the threads into the current thread
        # this is a blocking call that may take some time
        for plugin_thread in self.plugin_threads:
            # sends the exit event to the plugin thread and then
            # joins the plugin thread (waiting for the end of it)
            plugin_thread.add_event(exit_event)
            plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)

    def test_plugin_load(self, plugin):
        """
        Tests the given plugin, to check if the loading is possible.

        :type plugin: Plugin
        :param plugin: The plugin to be checked.
        :rtype: bool
        :return: The result of the plugin loading check.
        """

        # in case the plugin does not pass the test plugin load execution
        # in the plugin system
        if not self.plugin_manager_plugin_execute("test_plugin_load", [plugin]):
            return False

        # retrieves the plugin id (identifier) and name to be used
        # in some printing operations (value reference)
        plugin_id = plugin.id
        plugin_name = plugin.name

        # retrieves the plugin version
        plugin_version = plugin.version

        # verifies if the current plugin is not blacklisted for the current
        # manager and in case it's prints a message and returns in error
        if not self.test_blacklist(plugin):
            self.info(
                "Plugin '%s' v%s is blacklisted under the current manager" %
                (plugin_name, plugin_version)
            )
            return False

        # tests the plugin against the current thread specification
        # verifying if threads are available for the plugin
        if not self.test_threads(plugin):
            self.info(
                "Current thread permissions is not compatible with plugin '%s' v%s" %
                (plugin_name, plugin_version)
            )
            return False

        # tests the plugin against the current platform verifying if the
        # current platform is compatible with the plugin specification
        if not self.test_platform(plugin):
            self.info(
                "Current platform (%s) not compatible with plugin '%s' v%s" %
                (self.platform, plugin_name, plugin_version)
            )
            return False

        # tests the plugin for the availability of the dependencies checking
        # if the complete set of dependencies are available for the plugin
        if not self.test_dependencies(plugin):
            self.info(
                "Missing dependencies for plugin '%s' v%s" %
                (plugin_name, plugin_version)
            )
            return False

        # in case the plugin id does not exists in the loaded plugins
        # map must returns in error because it's not valid state
        if not plugin_id in self.loaded_plugins_map: return False

        # returns valid as the complete set of tests for the plugin have
        # be completed with success (no failures)
        return True

    def test_dependencies(self, plugin):
        """
        Tests if the dependencies for the given plugin are available.
        This test should not trigger the loading of the dependency
        plugin but only test if it's possible to load it.

        :type plugin: Plugin
        :param plugin: The plugin to be tested for dependencies.
        :rtype: bool
        :return: The result of the plugin dependencies available check.
        """

        # retrieves the plugin dependencies, that are going to be used
        # in the testing for availability (for loading)
        plugin_dependencies = plugin.dependencies

        # iterates over all the plugin dependencies to verify that they
        # are available for the loading process (as required)
        for plugin_dependency in plugin_dependencies:

            # in case the test dependency tests succeeds continues
            # the current loop to run more tests for dependencies
            if plugin_dependency.test_dependency(self): continue

            # prints a debug  message about the missing dependency
            # for the plugin and return in error (test failed)
            self.debug(
                "Problem with dependency '%s' for plugin '%s' v%s" %
                (str(plugin_dependency), plugin.name, plugin.version)
            )
            return False

        # returns valid meaning that the complete set of dependencies
        # is available for the loading of the plugin
        return True

    def test_platform(self, plugin):
        """
        Tests if the current platform is compatible with the given plugin,
        meaning that the current platform should be part of the registered
        list of available/compatible platforms for the plugin.

        :type plugin: Plugin
        :param plugin: The plugin to be tested for platform compatibility.
        :rtype: bool
        :return: The result of the plugin platform compatibility check.
        """

        # retrieves the plugin platforms list and then uses it
        # to verify if the current executing platform is present
        # under that list (platform is considered compatible)
        plugin_platforms_list = plugin.platforms
        return self.platform in plugin_platforms_list

    def test_threads(self, plugin):
        """
        Tests if the current thread permissions, allow the give plugin to
        be executed in the current environment.

        This test is only executed if the current manager does not allows
        threads creation and execution.

        :type plugin: Plugin
        :param plugin: The plugin to be tested for threads compatibility.
        :rtype: bool
        :return: The result of the plugin thread permissions check.
        """

        # in case the current environment does allows threads there's
        # no need to run the text and returns immediately in success
        if self.allow_threads: return True

        # iterates over all the capabilities that imply the creation of
        # threads in the current environment to test the current plugin
        # for the containing of such capabilities
        for capability in ("main", "thread", "threads"):
            # in case the plugin does not have the thread creation
            # capability the test should continue otherwise the test fails
            # and so a log message is printed and the function returns to
            # the calling method in failure
            if not capability in plugin.capabilities: continue
            self.info("Threads not allowed for plugin '%s' v%s" % (plugin.name, plugin.version))
            return False

        # returns value as all the tests have passed with success
        # the plugin should not create any threads as a consequence
        # of its execution in the environment
        return True

    def test_blacklist(self, plugin):
        """
        Verifies if the provided plugin is present in any of the
        currently loaded "blacklist", returning the appropriate
        value to the caller method.

        This test may be used to prevent the loading of the plugin
        under the current manager context.

        :type plugin: Plugin
        :param plugin: The plugin that is going to be tested for
        presence in the "blacklist".
        :rtype: bool
        :return: The result of the existence presence test of the
        plugin in the currently loaded "blacklist".
        """

        if plugin.id in self.blacklist: return False
        if plugin.short_name in self.blacklist: return False
        return True

    def resolve_capabilities(self, plugin):
        """
        Resolves the plugin capabilities, adding the plugin to the internal
        structures representing the association between capabilities and plugin
        instances.

        :type plugin: Plugin
        :param plugin: The plugin to have the capabilities resolved.
        :rtype: bool
        :return: The result of the resolution.
        """

        # adds itself to the map of plugins that have a given capability
        for plugin_capability_allowed in plugin.capabilities_allowed:
            self.add_capabilities_plugins_map(plugin_capability_allowed, plugin)

        # returns true
        return True

    def inject_dependencies(self, plugin):
        """
        Injects the dependencies into the given plugin.

        :type plugin: Plugin
        :param plugin: The plugin to haven the dependencies injected.
        :rtype: bool
        :return: The result of the injection.
        """

        # gets all the dependencies of the plugin
        plugin_dependencies = plugin.dependencies

        # iterates over all the dependencies of the plugin to be
        # able to "inject" them into the current plugin
        for plugin_dependency in plugin_dependencies:
            # in case the dependency is not of type plugin dependency
            # the current iteration step must be skipped
            if not plugin_dependency.__class__ == PluginDependency: continue

            # retrieves the dependency plugin instances (by id and version)
            dependency_plugin_instance = self._get_plugin_by_id_and_version(plugin_dependency.id, plugin_dependency.version)

            # in case the loading of the dependency plugin was not successful
            if not self.__load_plugin(dependency_plugin_instance, DEPENDENCY_TYPE):
                return False

            # in case the dependency plugin instance is not valid it's
            # not possible to inject it and iteration step is skipped
            if not dependency_plugin_instance: continue

            # calls the dependency inject method in the plugin
            # with the dependency plugin instances
            plugin.dependency_injected(dependency_plugin_instance)

            # adds the plugin to the plugin dependent plugins map for
            # the plugin dependency id
            self.add_plugin_dependent_plugins_map(plugin_dependency.id, plugin)

        # returns true
        return True

    def inject_allowed(self, plugin):
        """
        Injects all the allowed plugins for the given plugin.

        :type plugin: Plugin
        :param plugin: The plugin to inject the allowed plugins.
        """

        # gets all the capabilities allowed of the plugin
        plugin_capabilities_allowed = plugin.capabilities_allowed

        # iterates over all the capabilities of the plugin
        for plugin_capability_allowed in plugin_capabilities_allowed:
            # retrieves the plugin capability allowed type
            plugin_capability_allowed_type = type(plugin_capability_allowed)

            # in case the plugin capability allowed type is tuple
            if plugin_capability_allowed_type == tuple:
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

        :type plugin: Plugin
        :param plugin: The plugin to have the allowed plugin injected.
        :type allowed_plugin: Plugin
        :param allowed_plugin: The plugin to be injected as allowed in the plugin.
        :type capability: String/Tuple
        :param capability: The capability for witch the allowed plugin is being injected.
        """

        # in case both the plugin and the allowed plugins are valid and
        # the allowed plugin is not already "allowed" in the plugin
        # for the current capability
        if plugin and allowed_plugin and not (allowed_plugin, capability) in plugin.allowed_loaded_capability:
            # retrieves the capability type
            capability_type = type(capability)

            # in case the capability type is tuple
            if capability_type == tuple:
                # retrieves the real capability and diffusion policy
                capability, diffusion_policy = capability

                # in case the diffusion policy is same diffusion scope
                if diffusion_policy == SAME_DIFFUSION_SCOPE:
                    # in case the allowed plugin id already exists in the diffusion scope
                    if allowed_plugin.id in self.diffusion_scope_loaded_plugins_map[plugin.diffusion_scope]:
                        allowed_plugin = self.diffusion_scope_loaded_plugins_map[plugin.diffusion_scope][allowed_plugin.id]
                    else:
                        # prints a debug message
                        self.debug("Creating allowed plugin '%s' v%s as same diffusion scope" % (allowed_plugin.id, allowed_plugin.version))

                        # creates a new allowed plugin (in a the same diffusion scope as the plugin)
                        allowed_plugin = self._create_plugin(allowed_plugin.id, allowed_plugin.version, plugin.diffusion_scope)

                    # loads the allowed plugin (if necessary) with allowed type
                    self.__load_plugin(allowed_plugin, ALLOWED_TYPE)
                # in case the diffusion policy is new diffusion scope
                elif diffusion_policy == NEW_DIFFUSION_SCOPE:
                    # prints a debug message
                    self.debug("Creating allowed plugin '%s' v%s as new diffusion scope" % (allowed_plugin.id, allowed_plugin.version))

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

        :type plugin: Plugin
        :param plugin: The plugin to inject in the plugins that allow one of it's capabilities.
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

        :type diffusion_scope_id: int
        :param diffusion_scope_id: The diffusion scope id to be used.
        :type plugin_id: String
        :param plugin_id: The plugin id to be used.
        :type plugin_instance: Plugin
        :param plugin_instance: The plugin instance to be set.
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

        :type diffusion_scope_id: int
        :param diffusion_scope_id: The diffusion scope id to be used.
        :type plugin_id: String
        :param plugin_id: The plugin id to be used.
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
                if not allowed_plugins_list_element[0] == plugin: continue
                allowed_plugins_list.remove(allowed_plugins_list_element)
                break

    def add_capabilities_plugins_map(self, capability, plugin):
        """
        Adds a plugin to the capabilities plugins map.

        :type plugin: Plugin
        :param plugin: The plugin to be added to the capabilities plugins map.
        :type capability: String
        :param capability: The capability to be used as key in the
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

        :type capability: String
        :param capability: The capability to retrieve the list of plugins.
        :rtype: List
        :return: The list of plugins for the given capability.
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

        :type capability: String
        :param capability: The capability to be used to clear the capabilities
        plugins map.
        """

        self.capabilities_plugins_map[capability] = []

    def clear_capabilities_plugins_map_for_plugin(self, plugin_id):
        """
        Clears the capabilities plugins map, for the given plugin id.

        :type plugin_id: String
        :param plugin_id: The plugin id to be used to clear the capabilities
        plugins map.
        """

        # retrieves the plugin using the id
        plugin = self._get_plugin_by_id(plugin_id)

        for plugin_capability_allowed in plugin.capabilities_allowed:
            if not plugin_capability_allowed in self.capabilities_plugins_map: continue
            capability_plugins = self.capabilities_plugins_map[plugin_capability_allowed]
            if not plugin in capability_plugins: continue
            capability_plugins.remove(plugin)

    def load_plugin(self, plugin_id, type = None):
        """
        Loads a plugin for the given plugin id and type.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to be loaded.
        :type type: String
        :param type: The type of plugin to be loaded.
        :rtype: bool
        :return: The result of the load.
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
            self.info("Plugin '%s' v%s not ready to be loaded" % (plugin.name, plugin.version))
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

        :type plugin_id: String
        :param plugin_id: The id of the plugin to be unloaded.
        :type type: String
        :param type: The type of plugin to be unloaded.
        :rtype: bool
        :return: The result of the unload.
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

        :rtype: List
        :return: The list with all the started plugin instances.
        """

        return self.plugin_instances

    def get_all_loaded_plugins(self):
        """
        Retrieves all the loaded plugin instances.

        :rtype: List
        :return: The list with all the loaded plugin instances.
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

    def ensure(self, plugin):
        """
        Ensures that the provided plugin instance is loaded,
        loading it if required.

        In case the loading was not possible and the plugin
        remains unloaded at the end of the call an exception is
        raised indicating the problem.

        :type plugin: Plugin
        :param plugin: The plugin to be "ensured" to be loaded
        in the current system context.
        """

        # asserts that the plugin is loaded, this should load
        # the plugin properly, in case the plugin is not yet
        # loaded at the end of the call raises an exception
        # indicating the miss behavior
        self.assert_plugin(plugin)
        is_loaded = plugin.is_loaded()
        if not is_loaded:
            raise exceptions.ColonyException(
                "not possible to load plugin '%s'" % plugin.name
            )

    def assert_plugin(self, plugin):
        """
        "Asserts" the plugin and loads it if necessary.
        This method provides a mechanism for verified plugin
        loaded state.

        :type plugin: Plugin
        :param plugin: The plugin to be "assert" for loading.
        :rtype: Plugin
        :return: The "asserted" and loaded plugin.
        """

        # in case the plugin is not loaded (loading is
        # required), must trigger the loading process for
        # the current plugin in assertion
        if not plugin.is_loaded(): self._load_plugin(plugin)

        # returns the (loaded) plugin instance, should
        # be the same as the provided by parameter
        return plugin

    def get_plugin(self, plugin_id, plugin_version = None):
        """
        Retrieves an instance of a plugin with the given id.
        The retrieval of the plugin only uses the version is it's
        specified.

        Note that this method cannot be called at the same time
        from different threads as this would block the control
        flow to avoid unwanted sync problems.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve.
        :type plugin_version: String
        :param plugin_version: The version of the plugin to retrieve.
        :rtype: Plugin
        :return: The plugin with the given id and optionally version.
        """

        # acquires the retrieve lock so that no multiple retrieval
        # of plugins occur this would create some sync problems
        self.retrieve_lock.acquire()

        try:
            # retrieves the plugin (not sure about loading) and then
            # asserts it to be sure it's loaded (if possible)
            plugin = self._get_plugin(plugin_id, plugin_version)
            plugin = plugin and self.assert_plugin(plugin) or plugin
        finally:
            # releases the retrieve lock so that new retrieval of
            # plugins may occur (it's now possible)
            self.retrieve_lock.release()

        # returns the plugin (instance), this may be a newly initialized
        # instance or an instance already previously initialized
        return plugin

    def _get_plugin(self, plugin_id, plugin_version = None):
        """
        Retrieves an instance (not verified to be loaded) of
        a plugin with the given id.
        The retrieval of the plugin only uses the version is it's
        specified.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve.
        :type plugin_version: String
        :param plugin_version: The version of the plugin to retrieve.
        :rtype: Plugin
        :return: The plugin with the given id and optionally version.
        """

        # retrieves the plugin from the plugin instances map for
        # the given plugin id
        plugin = self.plugin_names_map.get(plugin_id, None)
        plugin = self.plugin_instances_map.get(plugin_id, plugin)

        # verifies if the plugin version is valid, it's considered to
        # be valid when it's not defined (anything counts) or when the
        # version matches the current plugin version
        version_valid = not plugin_version or colony.libs.version_cmp(
            plugin.version,
            plugin_version
        )

        # in case the version of the plugin is not valid returns invalid
        # as no valid plugin has been retrieved
        if not version_valid: return None

        # returns the plugin (instance)
        return plugin

    def get_plugin_by_id(self, plugin_id):
        """
        Retrieves an instance of a plugin with the given id.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve.
        :rtype: Plugin
        :return: The plugin with the given id.
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            return self.assert_plugin(plugin)

    def _get_plugin_by_id(self, plugin_id):
        """
        Retrieves an instance (not verified to be loaded) of a plugin with the given id.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve.
        :rtype: Plugin
        :return: The plugin with the given id.
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            return plugin

    def get_plugin_by_id_and_version(self, plugin_id, plugin_version):
        """
        Retrieves an instance of a plugin with the given id and version.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve.
        :type plugin_version: String
        :param plugin_version: The version of the plugin to retrieve.
        :rtype: Plugin
        :return: The plugin with the given id and version.
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            if colony.libs.version_cmp(plugin.version, plugin_version):
                return self.assert_plugin(plugin)

    def _get_plugin_by_id_and_version(self, plugin_id, plugin_version):
        """
        Retrieves an instance (not verified to be loaded) of a plugin with the given id and version.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve.
        :type plugin_version: String
        :param plugin_version: The version of the plugin to retrieve.
        :rtype: Plugin
        :return: The plugin with the given id and version.
        """

        if plugin_id in self.plugin_instances_map:
            plugin = self.plugin_instances_map[plugin_id]
            if colony.libs.version_cmp(plugin.version, plugin_version):
                return plugin

    def get_plugins_by_capability(self, capability):
        """
        Retrieves all the plugins with the given capability and sub capabilities.

        :type capability: String
        :param capability: The capability of the plugins to retrieve.
        :rtype: List
        :return: The list of plugins for the given capability and sub capabilities.
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
                    result.append(self.assert_plugin(plugin))

        # returns the results list
        return result

    def _get_plugins_by_capability_cache(self, capability):
        """
        Retrieves all the plugins (not verified to be loaded) with the
        given capability and sub capabilities (using cache system).

        :type capability: String
        :param capability: The capability of the plugins to retrieve.
        :rtype: List
        :return: The list of plugins for the given capability and
        sub capabilities.
        """

        # creates the results list to hold
        # the various plugin instances
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
        Retrieves all the plugins (not verified to be loaded) with
        the given capability and sub capabilities.

        :type capability: String
        :param capability: The capability of the plugins to retrieve.
        :rtype: List
        :return: The list of plugins for the given capability
        and sub capabilities.
        """

        # creates the results list to hold
        # the various plugin instances
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

        :type capability: String
        :param capability: The capability of the plugins to retrieve.
        :rtype: List
        :return: The list of plugins for the given capability.
        """

        # the results list
        result = []
        for plugin in self.plugin_instances:
            if not capability in plugin.capabilities: continue
            result.append(self.assert_plugin(plugin))
        return result

    def get_plugins_by_capability_allowed(self, capability_allowed):
        """
        Retrieves all the plugins with the given allowed capability and sub capabilities.

        :type capability_allowed: String
        :param capability_allowed: The capability allowed of the plugins to retrieve.
        :rtype: List
        :return: The list of plugins for the given capability allowed.
        """

        # the results list
        result = []

        # the capability converter to internal capability structure
        capability_structure = Capability(capability_allowed)

        for plugin in self.plugin_instances:
            plugin_capabilities_structure = convert_to_capability_list(plugin.capabilities_allowed)

            for plugin_capability_structure in plugin_capabilities_structure:
                if capability_structure.is_capability_or_sub_capability(plugin_capability_structure):
                    result.append(self.assert_plugin(plugin))

        return result

    def _get_plugins_by_capability_allowed(self, capability_allowed):
        """
        Retrieves all the plugins (not verified to be loaded) with
        the given allowed capability and sub capabilities.

        :type capability_allowed: String
        :param capability_allowed: The capability allowed of the
        plugins to retrieve.
        :rtype: List
        :return: The list of plugins for the given capability
        allowed.
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

    def get_plugins_by_event_fired(self, event_fired):
        result = []

        for plugin in self.plugin_instances:
            if not event_fired in plugin.events_fired: continue
            result.append(self.assert_plugin(plugin))

        return result

    def _get_plugins_by_event_fired(self, event_fired):
        result = []

        for plugin in self.plugin_instances:
            if not event_fired in plugin.events_fired: continue
            result.append(plugin)

        return result

    def get_plugins_by_event_handled(self, event_handled):
        result = []

        for plugin in self.plugin_instances:
            if not event_handled in plugin.events_handled: continue
            result.append(self.assert_plugin(plugin))

        return result

    def _get_plugins_by_event_handled(self, event_handled):
        result = []

        for plugin in self.plugin_instances:
            if not event_handled in plugin.events_handled: continue
            result.append(plugin)

        return result

    def get_plugins_by_dependency(self, plugin_id):
        """
        Retrieves all the plugins with a dependency with the given plugin id.

        :type plugin_id: String
        :param plugin_id: The id of the plugin dependency.
        :rtype: List
        :return: The list of plugins with a dependency with the given plugin id.
        """

        result = self._get_plugins_by_dependency(plugin_id)
        result = [self.assert_plugin(plugin) for plugin in result]
        return result

    def _get_plugins_by_dependency(self, plugin_id):
        """
        Retrieves all the plugins (not verified to be loaded) with a dependency
        with the given plugin id.

        :type plugin_id: String
        :param plugin_id: The id of the plugin dependency.
        :rtype: List
        :return: The list of plugins with a dependency with the given plugin id.
        """

        # the results list that will hold the complete set of plugins
        # that match the required plugin as a dependency
        result = []

        # iterates over all the plugin instances trying to find the plugins
        # that contain the request plugin dependency in its dependencies list
        for plugin in self.plugin_instances:

            # iterates over all the plugin dependencies trying to find a match
            # as requested by the method call (as defined in specification)
            for dependency in plugin.dependencies:
                # in case the dependency is not of type plugin dependency
                # must continue the loop not a valid dependency
                if not dependency.__class__ == PluginDependency: continue

                # in case the dependency plugin id is not the same must
                # continue the loop as this is not a valid plugin
                if dependency.id == plugin_id: continue

                # adds the current plugin plugin to the result list as it
                # contains the requested plugin in its dependencies
                result.append(self.assert_plugin(plugin))

        # returns the result, that should contain the complete set of plugins
        # that have the provided plugin as a dependency
        return result

    def get_plugins_allow_capability(self, capability):
        """
        Retrieves all the plugins that allow the given capability.

        :type capability: String
        :param capability: The capability to be tested.
        :rtype: List
        :return: The list of plugins that allow the given capability.
        """

        # the results list
        result = []

        # the capability converter to internal capability structure
        capability_structure = Capability(capability)

        for plugin in self.plugin_instances:
            plugin_capabilities_structure = convert_to_capability_list(plugin.capabilities_allowed)

            for plugin_capability_structure in plugin_capabilities_structure:
                if plugin_capability_structure.is_capability_or_sub_capability(capability_structure):
                    result.append(self.assert_plugin(plugin))

        return result

    def _get_plugins_allow_capability(self, capability):
        """
        Retrieves all the plugins (not verified to be loaded) that allow the given capability.

        :type capability: String
        :param capability: The capability to be tested.
        :rtype: List
        :return: The list of plugins that allow the given capability.
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

        :type file_path: String
        :param file_path: The base file path to be used as substitution
        base.
        :type not_found_valid: bool
        :param not_found_valid: If a file path should be returned even if
        the path is not found.
        :type create_path: bool
        :param create_path: If the file path should be created in case it
        does not exists.
        :rtype: String
        :return: The best file path of the possible file paths.
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

        :type string_value: String
        :param string_value: The base string value to be used as substitution
        base.
        :rtype: List
        :return: The list of possible string values, ordered by priority.
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
            command = special_value_match.group("command")
            arguments = special_value_match.group("arguments")

            # in case the arguments are defined
            if arguments:
                # splits the arguments value
                arguments_splitted = arguments.split(",")
            # otherwise
            else:
                # sets the arguments splitted as an empty list
                arguments_splitted = []

            # retrieves the process method for the current command
            process_method = getattr(self, "process_command_" + command)

            # runs the process method with the arguments
            # retrieving the values
            values = process_method(arguments_splitted)

            # retrieves the start and end position of the match
            start_position = special_value_match.start()
            end_position = special_value_match.end()

            # creates the values tuple with the start and end position
            # and with the values
            values_tuple = (
                start_position,
                end_position,
                values
            )

            # adds the value tuple to the value tuples list
            values_tuples_list.append(values_tuple)

        # creates the string buffers list with the initial string
        # buffer in it
        string_buffers_list = [colony.libs.StringBuffer()]

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
                if values_type in legacy.STRINGS:
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

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve the execution path.
        :rtype: String
        :return: The plugin execution path for the plugin with the given id.
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

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve the temporary
        plugin path.
        :type extra_path: String
        :param extra_path: The extra path to be appended.
        :rtype: String
        :return: The temporary plugin path for the given plugin id.
        """

        # retrieves the current temporary directory
        temporary_directory = tempfile.gettempdir()

        # creates the temporary plugin path
        temporary_plugin_path = temporary_directory + "/colony/" + plugin_id + "/" + extra_path

        # normalizes the temporary plugin path
        normalized_temporary_plugin_path = colony.libs.normalize_path(temporary_plugin_path)

        # returns the normalized temporary plugin path
        return normalized_temporary_plugin_path

    def get_temporary_plugin_generated_path_by_id(self, plugin_id):
        """
        Retrieves the temporary plugin generated path for the given plugin id.
        The path may refer a directory that is not created.
        The generated path is affected by a random value and should be unique.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve the temporary
        plugin generated path.
        :rtype: String
        :return: The temporary plugin generated path for the given plugin id.
        """

        # retrieves the temporary plugin path
        temporary_plugin_path = self.get_temporary_plugin_path_by_id(plugin_id)

        # retrieves the current time value (current time multiplied by a
        # factor of four) in integer
        current_time_value = int(time.time() * 10000)

        # creates the (final) temporary plugin path generated for the current time value
        temporary_plugin_generated_path = os.path.join(temporary_plugin_path, str(current_time_value))

        # normalizes the temporary plugin generated path
        normalized_temporary_plugin_generated_path = colony.libs.normalize_path(temporary_plugin_generated_path)

        # returns the normalized temporary plugin generated path
        return normalized_temporary_plugin_generated_path

    def get_plugin_configuration_paths_by_id(self, plugin_id, extra_paths = False):
        """
        Retrieves the plugin configuration paths for the given plugin id.
        The returned tuple contains a set of directories that may be used
        for plugin configuration purposes.
        The extra paths flag controls if all the "global" configuration paths
        shall be returned.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve the configuration paths.
        :type extra_paths: bool
        :param extra_paths: If the complete set of "global" paths should be retrieved
        or if only the first one shall be retrieved.
        :rtype: List
        :return: The plugin configuration paths for the plugin with the given id.
        """

        # retrieves the current configuration path
        configuration_path = self.get_configuration_path()

        # retrieves the current workspace path
        workspace_path = self.get_workspace_path()

        # retrieves the both the "global" configuration path
        # and the workspace (private) configuration path
        global_configuration_path = os.path.join(configuration_path, plugin_id)
        workspace_configuration_path = os.path.join(workspace_path, plugin_id)

        # retrieves the "meta" configuration paths according to the
        # value of the extra paths flag
        meta_configuration_paths = extra_paths and self.get_meta_paths() or []

        # starts the list of extra configuration paths
        # to be filled with the extra paths for the plugin id
        extra_configuration_paths = []

        # iterates over all the meta configuration paths to create
        # (the specific) extra configuration path for the meta
        # configuration path
        for meta_configuration_path in meta_configuration_paths:
            # retrieves the (specific) extra configuration path from the plugin
            # if, creating the extra configuration path
            extra_configuration_path = os.path.join(meta_configuration_path, plugin_id)
            extra_configuration_paths.append(extra_configuration_path)

        # creates a list containing all the configuration paths
        # and the converts it into a list
        configuration_paths_list = [global_configuration_path, workspace_configuration_path] + extra_configuration_paths
        configuration_paths_tuple = tuple(configuration_paths_list)

        # returns a tuple containing all the configuration paths
        return configuration_paths_tuple

    def get_plugin_configuration_file_by_id(self, plugin_id, configuration_file_path):
        """
        Retrieves the plugin configuration file for the given plugin id
        and configuration file path.

        :type plugin_id: String
        :param plugin_id: The plugin id to be used in the configuration
        file retrieval.
        :type configuration_file_path: String
        :param configuration_file_path: The path of the configuration file (relative to
        the base of the plugin configuration path).
        :rtype: File
        :return: The configuration file retrieved.
        """

        # retrieves the configuration paths for the plugin
        plugin_configuration_paths = self.get_plugin_configuration_paths_by_id(plugin_id)

        # iterates over all the plugin configuration paths, to check
        # if the configuration file exists in any of the paths
        for plugin_configuration_path in plugin_configuration_paths:
            # creates the configuration file full path from the configuration
            # file and the configuration file path
            configuration_file_full_path = os.path.join(plugin_configuration_path, configuration_file_path)

            # in case the configuration file full path does not exist
            if not os.path.exists(configuration_file_full_path):
                # continues the loop (not found)
                continue

            # opens the configuration file
            configuration_file = open(configuration_file_full_path)

            # returns the configuration file
            return configuration_file

    def get_plugin_module_name_by_id(self, plugin_id):
        """
        Retrieves the plugin module name for the given plugin id.

        :type plugin_id: String
        :param plugin_id: The id of the plugin to retrieve the plugin module name.
        :rtype: String
        :return: The plugin module name for the given plugin id.
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

        :type module: String
        :param module: The plugin module name to retrieve.
        :rtype: Plugin
        :return: The plugin for the given plugin module name.
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

        :type module: String
        :param module: The loaded plugin module name to retrieve.
        :rtype: Plugin
        :return: The loaded plugin for the given plugin module name.
        """

        loaded_plugins = self.get_all_loaded_plugins()

        for loaded_plugin in loaded_plugins:
            plugin_module = loaded_plugin.__module__

            if plugin_module == module:
                return loaded_plugin

    def get_plugin_class_by_module_name(self, module):
        """
        Retrieves a the plugin class for the given plugin module name.

        :type module: String
        :param module: The plugin module name to retrieve.
        :rtype: Class
        :return: The plugin class for the given plugin module name.
        """

        for plugin in self.loaded_plugins:
            plugin_module = plugin.__module__

            if plugin_module == module:
                return plugin

    def register_plugin_manager_event(self, plugin, event_name):
        """
        Registers a given plugin manager event in the given plugin.

        :type plugin: Plugin
        :param plugin: The plugin containing the handler to the event.
        :type event_name: String
        :param event_name: The name of the event to be registered.
        """

        if not event_name in self.event_plugins_fired_loaded_map:
            self.event_plugins_fired_loaded_map[event_name] = []

        if not plugin in self.event_plugins_fired_loaded_map[event_name]:
            self.event_plugins_fired_loaded_map[event_name].append(plugin)

            # prints a debug message
            self.debug("Registering event '%s' from '%s' v%s in plugin manager" % (event_name, plugin.name, plugin.version))

    def unregister_plugin_manager_event(self, plugin, event_name):
        """
        Unregisters a given plugin manager event in the given plugin.

        :type plugin: Plugin
        :param plugin: The plugin containing the handler to the event.
        :type event_name: String
        :param event_name: The name of the event to be unregistered.
        """

        if event_name in self.event_plugins_fired_loaded_map:
            if plugin in self.event_plugins_fired_loaded_map[event_name]:
                self.event_plugins_fired_loaded_map[event_name].remove(plugin)

                # prints a debug message
                self.debug("Unregistering event '%s' from '%s' v%s in plugin manager" % (event_name, plugin.name, plugin.version))

    def notify_handlers(self, event_name, event_args):
        """
        Notifies all the handlers for the event with the given name with the give arguments.

        :type event_name: String
        :param event_name: The name of the event to be notified.
        :type event_args: List
        :param event_args: The arguments to be passed to the handler.
        """

        # the names of the events fired by self
        event_names_list = legacy.keys(self.event_plugins_fired_loaded_map)

        # retrieves all the events and super events that match the generated event
        events_or_super_events_list = get_all_events_or_super_events_in_list(event_name, event_names_list)

        # iterates over all the events and super events for notification
        for event_or_super_event in events_or_super_events_list:
            if not event_or_super_event in self.event_plugins_fired_loaded_map: continue

            # iterates over all the plugins registered for notification to be able
            # to notify them about the new event that has just been triggered
            for event_plugin_loaded in self.event_plugins_fired_loaded_map[event_or_super_event]:
                self.debug(
                    "Notifying '%s' v%s about event '%s' generated in plugin manager" %
                    (event_plugin_loaded.name, event_plugin_loaded.version, event_name)
                )
                event_plugin_loaded.event_handler(event_name, *event_args)

    def generate_event(self, event_name, event_args):
        """
        Generates an event and starts the process of handler notification.

        :type event_name: String
        :param event_name: The name of the event to be notified.
        :type event_args: List
        :param event_args: The arguments to be passed to the handler.
        """

        # prints a debug message about the event that has been generated and
        # notifies the event handlers of the event name with the event arguments
        self.debug("Event '%s' generated in plugin manager" % (event_name))
        self.notify_handlers(event_name, event_args)

    def plugin_manager_plugin_execute(self, execution_type, arguments):
        """
        Executes a plugin manager call in all the plugin manager plugins with
        the defined execution type capability.

        :type execution_type: String
        :param execution_type: The type of execution.
        :type arguments: List
        :param arguments: The list of arguments for the execution.
        :rtype: bool
        :return: The boolean result of the AND operation between the call results.
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

        :type execution_type: String
        :param execution_type: The type of execution.
        :type arguments: List
        :param arguments: The list of arguments for the execution.
        :rtype: bool
        :return: The boolean result of the AND operation between the call results.
        """

        # in case the plugin manager plugins are already loaded
        if self.plugin_manager_plugins_loaded:

            # retrieves the init_plugin_load_plugins_list
            execute_plugins_list = self._get_plugins_by_capability_cache(PLUGIN_MANAGER_EXTENSION_TYPE + "." + execution_type)

            # iterates over all the init plugin load plugins
            for execute_plugin in execute_plugins_list:

                # retrieves the validation method
                validation_execute_call = getattr(
                    execute_plugin,
                    "is_valid_" + execution_type
                )

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

        :type execution_type: String
        :param execution_type: The type of execution.
        :type arguments: List
        :param arguments: The list of arguments for the execution.
        :rtype: bool
        :return: The result of the test (if successful or not).
        """

        # in case the plugin manager plugins are already loaded
        if self.plugin_manager_plugins_loaded:

            # retrieves the init_plugin_load_plugins_list
            execute_plugins_list = self._get_plugins_by_capability_cache(PLUGIN_MANAGER_EXTENSION_TYPE + "." + execution_type)

            # iterates over all the init plugin load plugins
            for execute_plugin in execute_plugins_list:

                # retrieves the validation method
                validation_execute_call = getattr(execute_plugin, "is_valid_" + execution_type)

                # runs the validation test
                if validation_execute_call(*arguments):
                    return True

        # returns false
        return False

    def generate_system_information_map(self):
        """
        Generates the map containing a set of information
        regarding global system settings.
        """

        self.system_information_map = dict(
            layout_mode = self.get_layout_mode(),
            run_mode = self.get_run_mode(),
            timestamp = self.get_timestamp(),
            version = self.get_version(),
            release = self.get_release(),
            build = self.get_build(),
            release_date = self.get_release_date(),
            release_date_time = self.get_release_date_time(),
            environment = self.get_environment()
        )

    def get_log_handler(self, name):
        """
        Retrieves the reference to the logger handler
        with the provided name as reference. In case no
        logging handler is found an invalid value is
        returned instead.

        :type name: String
        :param name: The name of the log handler to be
        retrieved.
        :rtype: Handler
        :return: The logging handler installed in the
        manager logger with the provided name or and invalid
        value in case it's not found.
        """

        return self.logger_handlers.get(name, None)

    def log_stack_trace(self, level = logging.DEBUG):
        """
        Logs the current stack trace to the logger.
        The verbosity level may be controlled using
        the level parameter.

        :type level: int
        :param level: The verbosity level to be used
        in the logging.
        """

        # retrieves the execution information
        _type, _value, traceback_list = sys.exc_info()

        # in case the traceback list is valid
        if traceback_list:
            formated_traceback = traceback.format_tb(traceback_list)
        # otherwise there is no traceback list
        else:
            formated_traceback = ()

        # iterates over the traceback lines to log
        # them into the current logger
        for formated_traceback_line in formated_traceback:
            # strips the formated traceback line
            formated_traceback_line_stripped = formated_traceback_line.rstrip()

            # prints a log message with the formated traceback line
            self.logger.log(level, formated_traceback_line_stripped)

    def debug(self, message):
        """
        Adds the given debug message to the logger.

        :type message: String
        :param message: The debug message to be added to the logger.
        """

        # in case no logger is defined it's not possible
        # to print the message as a debug
        if not self.logger: return

        # formats the logger message and prints it
        # as a debug message into the logger
        logger_message = self.format_logger_message(message)
        self.logger.debug(logger_message)

    def info(self, message):
        """
        Adds the given info message to the logger.

        :type message: String
        :param message: The info message to be added to the logger.
        """

        # in case no logger is defined it's not possible
        # to print the message as an info
        if not self.logger: return

        # formats the logger message and prints it
        # as an info message into the logger
        logger_message = self.format_logger_message(message)
        self.logger.info(logger_message)

    def warning(self, message):
        """
        Adds the given warning message to the logger.

        :type message: String
        :param message: The warning message to be added to the logger.
        """

        # in case no logger is defined it's not possible
        # to print the message as a warning
        if not self.logger: return

        # formats the logger message and prints it
        # as a warning message into the logger
        logger_message = self.format_logger_message(message)
        self.logger.warning(logger_message)

        # logs the stack trace
        self.log_stack_trace(level = logging.INFO)

    def error(self, message):
        """
        Adds the given error message to the logger.

        :type message: String
        :param message: The error message to be added to the logger.
        """

        # in case no logger is defined it's not possible
        # to print the message as an error
        if not self.logger: return

        # formats the logger message and prints it
        # as an error message into the logger
        logger_message = self.format_logger_message(message)
        self.logger.error(logger_message)

        # logs the stack trace
        self.log_stack_trace(level = logging.WARNING)

    def critical(self, message):
        """
        Adds the given critical message to the logger.

        :type message: String
        :param message: The critical message to be added to the logger.
        """

        # formats the logger message
        logger_message = self.format_logger_message(message)

        # prints the critical message
        self.logger.critical(logger_message)

        # logs the stack trace
        self.log_stack_trace(level = logging.ERROR)

    def format_logger_message(self, message):
        """
        Formats the given message into a logging message.

        :type message: String
        :param message: The message to be formated into logging message.
        :rtype: String
        :return: The formated logging message.
        """

        # the default formatting message
        formatting_message = str()

        # in case the plugin id logging option is activated
        if GLOBAL_CONFIG.get("plugin_id_logging", False):
            formatting_message += "[pt.hive.colony] "

        # in case the thread id logging option is activated
        if GLOBAL_CONFIG.get("thread_id_logging", False):
            formatting_message += "[" + str(threading.current_thread().ident) + "] "

        # appends the formatting message to the logging message
        logger_message = formatting_message + message

        # returns the logger message
        return logger_message

    def print_all_plugins(self):
        """
        Prints all the loaded plugins descriptions.
        """

        # iterates over all the plugin instances to
        # print their default description
        for plugin in self.plugin_instances: print(plugin)

    def get_prefix_paths(self):
        """
        Retrieves the list of manager path relative paths
        to be used as reference for sub-projects.

        :rtype: String
        :return: The list of manager path relative paths
        to be used as reference for sub-projects.
        """

        return self.prefix_paths

    def get_environment_variable(self, environment_variable_name):
        """
        Retrieves the environment variable for the given
        environment variable name.

        :type environment_variable_name: String
        :param environment_variable_name: The name of the environment
        variable to be retrieved.
        :rtype: String
        :return: The retrieved environment variable value.
        """

        return os.environ.get(environment_variable_name, "")

    def get_configuration_path(self):
        """
        Retrieves the current configuration path.

        :rtype: String
        :return: The current configuration path.
        """

        return os.path.join(self.manager_path, self.configuration_path)

    def get_meta_paths(self):
        """
        Retrieves the current meta paths.

        :rtype: String
        :return: The current meta paths.
        """

        return [os.path.join(self.manager_path, meta_path) for meta_path in\
            self.meta_paths if os.path.exists(os.path.join(self.manager_path, meta_path))]

    def get_workspace_path(self):
        """
        Retrieves the workspace path.

        :rtype: String
        :return: The workspace path.
        """

        # retrieves the workspace path
        return self.workspace_path

    def set_workspace_path(self, workspace_path):
        """
        Sets the workspace path, updating the workspace
        path after the setting.

        :type workspace_path: String
        :param workspace_path: The workspace path.
        """

        # sets the workspace path in the current instance and then
        # updates the workspace path (creating it if required)
        self.workspace_path = workspace_path
        self.update_workspace_path()

    def set_timestamp(self, timestamp = None):
        """
        Sets the timestamp value for the plugin manager.
        The value that will be set depends on the provided value, in
        case the provided value is invalid the current time is set.

        :type timestamp: float
        :param timestamp: The value to set in the plugin manager
        as the timestamp, used for loading time purposes.
        """

        # sets the plugin manager timestamp with the provided value or
        # with the current time value as a fallback procedure
        self.timestamp = timestamp or time.time()

    def set_plugin_manager_plugins_loaded(self, value = True):
        """
        Sets the value for the plugin_manager_plugins_loaded flag.

        :type value: bool
        :param value: The value to set for the plugin_manager_plugins_loaded flag.
        """

        self.plugin_manager_plugins_loaded = value

    def get_plugin_manager_plugins_loaded(self):
        """
        Retrieves the current plugin_manager_plugins_loaded flag value.

        :rtype: bool
        :return: The current plugin_manager_plugins_loaded flag value.
        """

        return self.plugin_manager_plugins_loaded

    def set_init_complete(self, value = True):
        """
        Sets the value for the init_complete flag.

        :type value: bool
        :param value: The value to set for the init_complete flag.
        """

        self.init_complete = value

    def get_init_complete(self):
        """
        Retrieves the current init_complete flag value.

        :rtype: bool
        :return: The current init_complete flag value.
        """

        return self.init_complete

    def get_manager_path(self):
        """
        Retrieves the manager base path for execution.

        :rtype: String
        :return: The manager base path for execution.
        """

        return self.manager_path

    def get_plugin_paths(self):
        """
        Retrieves the manager plugin paths for execution.

        :rtype: List
        :return: The manager plugin paths for execution.
        """

        return self.plugin_paths

    def get_main_plugin_path(self):
        """
        Retrieves the manager main plugin path for execution.

        :rtype: String
        :return: The manager main plugin path for execution.
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

    def get_containers_path(self):
        """
        Retrieves the manager containers path for execution.

        :rtype: String
        :return: The manager containers path for execution.
        """

        # retrieves the manager path
        manager_path = self.get_manager_path()

        # creates the containers path joining the manager path and the
        # default containers path
        containers_path = os.path.join(manager_path, DEFAULT_CONTAINERS_PATH)

        # returns the containers path
        return containers_path

    def get_libraries_path(self):
        """
        Retrieves the manager libraries path for execution.

        :rtype: String
        :return: The manager libraries path for execution.
        """

        # retrieves the manager path
        manager_path = self.get_manager_path()

        # creates the libraries path joining the manager path and the
        # default libraries path
        libraries_path = os.path.join(manager_path, DEFAULT_LIBRARIES_PATH)

        # returns the libraries path
        return libraries_path

    def get_temporary_path(self):
        """
        Retrieves the manager temporary path for execution.

        :rtype: String
        :return: The manager temporary path for execution.
        """

        # retrieves the manager path
        manager_path = self.get_manager_path()

        # creates the temporary path joining the manager path and the
        # default temporary path
        temporary_path = os.path.join(manager_path, DEFAULT_TEMPORARY_PATH)

        # returns the temporary path
        return temporary_path

    def get_variable_path(self):
        """
        Retrieves the manager variable path for execution.

        :rtype: String
        :return: The manager variable path for execution.
        """

        # retrieves the manager path
        manager_path = self.get_manager_path()

        # creates the variable path joining the manager path and the
        # default variable path
        variable_path = os.path.join(manager_path, DEFAULT_VARIABLE_PATH)

        # returns the variable path
        return variable_path

    def get_plugin_paths_file_path(self):
        """
        Retrieves the manager plugin paths file path for execution.

        :rtype: String
        :return: The manager plugin paths file path for execution.
        """

        # retrieves the manager path
        manager_path = self.get_manager_path()

        # creates the plugins path file path joining the manager path and the
        # default variable path
        plugin_paths_file_path = os.path.join(manager_path, DEFAULT_PLUGIN_PATHS_FILE_PATH)

        # returns the plugin paths file path
        return plugin_paths_file_path

    def get_layout_mode(self):
        """
        Retrieves the current base (plugin manager) layout mode.

        :rtype: String
        :return: The current base (plugin manager) layout mode.
        """

        return self.layout_mode

    def get_run_mode(self):
        """
        Retrieves the current base (plugin manager) run mode.

        :rtype: String
        :return: The current base (plugin manager) run mode.
        """

        return self.run_mode

    def get_timestamp(self):
        """
        Retrieves the current base (plugin manager) timestamp.

        :rtype: float
        :return: The current base (plugin manager) timestamp.
        """

        return self.timestamp

    def get_version(self):
        """
        Retrieves the current base (plugin manager) version.

        :rtype: String
        :return: The current base (plugin manager) version.
        """

        return information.VERSION

    def get_release(self):
        """
        Retrieves the current base (plugin manager) release.

        :rtype: String
        :return: The current base (plugin manager) release.
        """

        return information.RELEASE

    def get_build(self):
        """
        Retrieves the current base (plugin manager) build.

        :rtype: String
        :return: The current base (plugin manager) build.
        """

        return information.BUILD

    def get_release_date(self):
        """
        Retrieves the current base (plugin manager) release date.

        :rtype: String
        :return: The current base (plugin manager) release date.
        """

        return information.RELEASE_DATE

    def get_release_date_time(self):
        """
        Retrieves the current base (plugin manager) release date time.

        :rtype: String
        :return: The current base (plugin manager) release date time.
        """

        return information.RELEASE_DATE_TIME

    def get_environment(self):
        """
        Retrieves the current base (plugin manager) environment.

        :rtype: String
        :return: The current base (plugin manager) environment.
        """

        return information.ENVIRONMENT

    def get_system_information_map(self):
        """
        Retrieves a map containing a set of information
        regarding global system settings.

        :rtype: Dictionary
        :return: A map containing a set of information
        regarding global system settings.
        """

        return self.system_information_map

    def get_uptime(self):
        """
        Retrieves a string describing the uptime value for
        the currently loaded plugin system.

        This string is a descriptive string in english language
        and should be used for presentation to a non technical
        user (not enough flexibility).

        :rtype: String
        :return: The string describing the current plugin system's
        uptime in english language.
        """

        # calculates the delta (value) between the current time
        # value and the saved load timestamp then uses it to create
        # the uptime message to be returned
        delta = time.time() - self.timestamp
        uptime = colony.libs.format_seconds_smart(delta, mode = "extended_simple")

        # returns the message containing the description
        # about the uptime for the current plugin system
        return uptime

    def is_development(self):
        """
        Checks if the current run mode in execution is of type
        development, this check may be used to action conditional
        code execution for debugging purposes.

        :rtype: bool
        :return: Value indicating if the current run mode is of
        type development (for debugging purposes).
        """

        return self.run_mode == "development"

    def is_production(self):
        """
        Checks if the current run mode in execution is of type
        production, this check may be used to action conditional
        code execution for strict execution.

        :rtype: bool
        :return: Value indicating if the current run mode is of
        type production (for strict purposes).
        """

        return not self.is_development()

    def echo(self, value = "echo"):
        """
        Returns an echo value.

        :type value: String
        :param value: The value to be echoed.
        :rtype: String
        :return: The echo value.
        """

        return value

    def process_command_manager_path(self, arguments):
        """
        The process command method for the manager path command.

        :type arguments: String
        :param arguments: The arguments to the process command method.
        :rtype: Object
        :return: The result of the command processing.
        """

        return (
            self.manager_path,
        )

    def process_command_plugin_path(self, arguments):
        """
        The process command method for the plugin path command.

        :type arguments: String
        :param arguments: The arguments to the process command method.
        :rtype: Object
        :return: The result of the command processing.
        """

        return (
            self.get_plugin_path_by_id(*arguments),
        )

    def process_command_configuration(self, arguments):
        """
        The process command method for the configuration command.

        :type arguments: String
        :param arguments: The arguments to the process command method.
        :rtype: Object
        :return: The result of the command processing.
        """

        return self.get_plugin_configuration_paths_by_id(*arguments)

    def process_command_environment(self, arguments):
        """
        The process command method for the configuration command.

        :type arguments: String
        :param arguments: The arguments to the process command method.
        :rtype: Object
        :return: The result of the command processing.
        """

        return (
            self.get_environment_variable(*arguments),
        )

    def process_command_prefix(self, arguments):
        """
        The process command method for the prefix command.

        :type arguments: String
        :param arguments: The arguments to the process command method.
        :rtype: Object
        :return: The result of the command processing.
        """

        return (
            os.path.join(self.manager_path, self.prefix_paths.get(*arguments) or ""),
        )

    def _relaunch_system(self):
        """
        Re-launches the system through the creation
        of a new process.
        """

        # "re-starts the system with the current environment
        # argument values
        args = [sys.executable]
        args.extend(sys.argv)
        subprocess.Popen(args)

    def _kill_system_signal_handler(self, signum, frame):
        """
        Kills the system, due to signal occurrence, this unloading
        process should be properly logged into the currently defined
        logging infra-structure for debugging purposes.

        :type signum: int
        :param signum: The signal number that was raised and that is
        going to be logged as "responsible" for the unloading.
        :type frame: Frame
        :type frame: The frame value of the current system stat that
        may be used for traceability or debug.
        """

        try:
            # print a warning message about the start of the system unloading
            # then runs the unloading operation and ends with a message about
            # the end of the unloading operation process
            self.warning("Unloading system due to signal: '%s'" % signum)
            self.unload_system(True)
            self.warning("Unloaded system due to signal: '%s'" % signum)
        except Exception as exception:
            # prints an error message about the problem in the unloading process
            # then stops the blocking system structures and exists the current
            # process with an error value (notifies the operative system)
            self.error("Problem unloading the system '%s', killing the system..." % legacy.UNICODE(exception))
            self._stop_blocking_system_structures()
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
        # must returns immediately as there's nothing
        # to be canceled (nothing to be done)
        if not self.kill_system_timer: return

        # cancels the kill system timer, this shold avoid
        # any possible locking problems with the system
        self.kill_system_timer.cancel()

    def _kill_system_timeout(self):
        """
        Kills the system, due to unload timeout occurrence.
        """

        # prints an error message
        self.error("Unloading timeout (%.2f seconds) reached, killing the system..." % DEFAULT_UNLOAD_SYSTEM_TIMEOUT)

        # exits in error
        exit(2)

    def _handle_system_exception(self, exception):
        """
        Handles the given system base exception.
        These exception occur at the highest level of the plugin framework.
        The handling is sever and culminates in the unloading of the
        plugin framework.

        :type exception: BaseException
        :param exception: The exception to be handled, the kind of exception
        gathered may be of any type and that should be expected.
        """

        try:
            # retrieves the exception type and the message that is
            # going to be used to represent the message
            exception_type = exception.__class__.__name__
            exception_message = legacy.UNICODE(exception) or "Unknown error"

            # print an information message about the unloading
            # of the current system, this is printed at the beginning
            # of the unloading process of the plugin system
            self.info(
                "Unloading system due to exception: '%s' of type '%s'" %
                (exception_message, exception_type)
            )

            # starts the unloading of the system, this is a blocking
            # method call and may take some time to be completed
            self.unload_system(False)

            # print an information message about the unloading
            # that has completed for the current system
            self.info(
                "Unloaded system due to exception: '%s' of type '%s'" %
                (exception_message, exception_type)
            )
        except (KeyboardInterrupt, SystemExit) as exception:
            # retrieves the message that is going to be used for the
            # representation of the exception in the logging
            exception_message = legacy.UNICODE(exception) or "Unknown error"

            # prints an error message about the problem in the unloading
            # of the current plugin system, required for debugging
            self.error("Problem unloading the system '%s', killing the system..." % exception_message)

            # stops the blocking system structures and then exits
            # the current process with an error code indicating that
            # the exit was not achieved success (problem in unload)
            self._stop_blocking_system_structures()
            exit(2)

    def _get_best_plugin_path(self, plugin_path):
        """
        Converts the given plugin path into the
        best fitting plugin path, counting with the
        possible relative paths.

        :type plugin_path: String
        :param plugin_path: The plugin path to be converted
        :rtype: String
        :return: The converted plugin path.
        """

        # retrieves the manager path
        manager_path = self.get_manager_path()

        # normalizes the plugin path
        plugin_path = os.path.normcase(plugin_path)

        # checks if the plugin path is absolute
        plugin_path_absolute = os.path.abspath(plugin_path)

        # in case the plugin path is not absolute (relative)
        if not plugin_path_absolute:
            # returns the plugin path immediately
            # as nothing is better than a relative path
            return plugin_path

        # retrieves the relative path between the manager path and the plugin
        # path
        plugin_relative_path = colony.libs.relative_path(plugin_path, manager_path)

        # checks if the plugin relative path is a back-reference
        plugin_relative_path_back = plugin_relative_path.startswith("..")

        # sets the plugin path to the absolute value or the relative
        # value in case it fits best (no back references allowed)
        plugin_path = plugin_relative_path_back and plugin_path or plugin_relative_path

        # returns the resulting plugin path
        return plugin_path

class Dependency(object):
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

        :type mandatory: bool
        :param mandatory: The mandatory value.
        :type conditions_list: List
        :param conditions_list: The list of conditions.
        """

        self.mandatory = mandatory
        self.conditions_list = conditions_list

    def test_dependency(self, manager):
        """
        Tests the environment for the plugin manager.

        :type manager: PluginManager
        :param manager: The current plugin manager in use.
        :rtype: bool
        :return: The result of the test (if successful or not).
        """

        return True

    def test_conditions(self):
        """
        Tests the available conditions, in case at least one of
        the conditions fails the return value is invalid otherwise
        the return value is valid.

        :rtype: bool
        :return: The result of the test (if successful or not).
        """

        # iterates over all the conditions returning
        # an invalid value in case at least one of the
        # test fails to be successful
        for condition in self.conditions_list:
            if condition.test_condition(): continue
            return False

        return True

    def get_tuple(self):
        """
        Retrieves a tuple representing the dependency.

        :rtype: Tuple
        :return: A tuple representing the dependency.
        """

        return ()

class PluginDependency(Dependency):
    """
    The plugin dependency class.
    """

    id = None
    """ The identifier of the plugin that is being represented
    by the current dependency instance """

    version = None
    """ The version of the plugin that is going to be
    used for the plugin dependency representation """

    diffusion_policy = SINGLETON_DIFFUSION_SCOPE
    """ The diffusion policy for the dependency """

    def __init__(
        self,
        id,
        version = "x.x.x",
        diffusion_policy = SINGLETON_DIFFUSION_SCOPE,
        mandatory = True,
        conditions_list = []
    ):
        """
        Constructor of the class.

        :type id: String
        :param id: The plugin id.
        :type version: String
        :param version: The plugin version.
        :type diffusion_policy: int
        :param diffusion_policy: The diffusion policy.
        :type mandatory: bool
        :param mandatory: The mandatory value.
        :type conditions_list: List
        :param conditions_list: The list of conditions.
        """

        Dependency.__init__(self, mandatory, conditions_list)
        self.id = id
        self.version = version
        self.diffusion_policy = diffusion_policy

    def __repr__(self):
        """
        Returns the default representation of the class.

        :rtype: String
        :return: The default representation of the class.
        """

        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.id,
            self.version,
        )

    def test_dependency(self, manager):
        """
        Tests the environment for the plugin dependency and the given plugin manager.

        :type manager: PluginManager
        :param manager: The current plugin manager in use.
        :rtype: bool
        :return: The result of the test (if successful or not).
        """

        Dependency.test_dependency(self, manager)

        # in case some of the conditions are not fulfilled plugin
        # the loading of the plugin fails
        if not self.test_conditions(): return True

        # retrieves the plugin id and version for the
        # plugin dependency so that it can be tested
        # for version matching
        plugin_id = self.id
        plugin_version = self.version

        # in case the plugin is not present in the loaded
        # plugins map, returns immediately in failure, otherwise
        # retrieves the plugin from the map and then tries to fund
        # out if there is a version mismatch
        if not plugin_id in manager.loaded_plugins_map: return False
        plugin = manager.loaded_plugins_map[plugin_id]
        if not colony.libs.version_cmp(plugin.version, plugin_version): return False

        # in case the plugin load test is not successful
        if not manager.test_plugin_load(plugin): return False

        return True

    def get_tuple(self):
        """
        Retrieves a tuple representing the plugin dependency.

        :rtype: Tuple
        :return: A tuple representing the plugin dependency.
        """

        return (
            self.id,
            self.version
        )

    def get_map(self):
        """
        Retrieves the map based representation of the current plugin
        dependency, this value may be used as a portable way to represent
        the current dependency.

        :rtype: Dictionary
        :return: The map based representation of the current plugin
        dependency to be used in a portable way.
        """

        return dict(
            type = "plugin",
            id = self.id,
            version = self.version
        )

class PackageDependency(Dependency):
    """
    The package dependency class, used to describe a dependency
    on a python simple package. Should encapsulate the various
    concepts that define the package.
    """

    name = None
    """ The name of the package defined as a simple
    human readable description of it """

    import_name = None
    """ The name of the python based import, this name
    should respect the value of the import as it is going
    to be used for the testing of package existence """

    version = "1.0.0"
    """ The version of the package that the dependency is
    defined this value may or may not be used for the test
    of packaged existence (not required) """

    url = None
    """ The URL where from which the package may be retrieved
    this may be the product page for the package """

    def __init__(
        self,
        name,
        import_name,
        version = "1.0.0",
        url = None,
        mandatory = True,
        conditions_list = []
    ):
        """
        Constructor of the class.

        :type name: String
        :param name: The package name.
        :type import_name: String
        :param import_name: The package import name.
        :type version: String
        :param version: The package version.
        :type url: String
        :param url: The package URL.
        :type mandatory: bool
        :param mandatory: The mandatory value.
        :type conditions_list: List
        :param conditions_list: The list of conditions.
        """

        Dependency.__init__(self, mandatory, conditions_list)
        self.name = name
        self.import_name = import_name
        self.version = version
        self.url = url

    def __repr__(self):
        """
        Returns the default representation of the class.

        :rtype: String
        :return: The default representation of the class.
        """

        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.name,
            self.version
        )

    def test_dependency(self, manager):
        """
        Tests the environment for the package dependency and the
        given plugin manager. Meaning that the complete set of
        packages for the current dependency are going to be tested
        for the proper existence.

        :type manager: PluginManager
        :param manager: The current plugin manager in use.
        :rtype: bool
        :return: The result of the test (if successful or not).
        """

        Dependency.test_dependency(self, manager)

        # in case some of the conditions are not fulfilled, an invalid
        # value must be returned to the caller method
        if not self.test_conditions(): return True

        # retrieves the package import name type so that it may be used
        # to verify if the package is a set of packages (list type) or
        # just a single package, and in case it's a single package converts
        # it into a single item sequence to be compliant with a sequence
        import_name_t = type(self.import_name)
        is_sequence = import_name_t in (list, tuple)
        import_name = self.import_name if is_sequence else (self.import_name,)

        # iterates over the complete set of package items in the import name
        # value and tries to import every single one of them, in case one of
        # the import fails a message is logged and an invalid value is returned
        for import_name_item in import_name:
            # creates an unsets the imported flag that will control the import
            # process, if this value is set after the loop at least one of the
            # alias imports has been successful
            imported = False

            # verifies if the current import name item is of type and in case it's
            # not coerces the value into a portable sequence so that it's able to
            # iterate over the complete set of items to import them properly
            is_sequence = type(import_name_item) in (list, tuple)
            import_name_items = import_name_item if is_sequence else (import_name_item,)
            for _import_name_item in import_name_items:
                try: __import__(_import_name_item)
                except ImportError: continue
                else: imported = True; break

            # verifies if the imported flag has been set, if that's the case at least
            # one of the alias imports has been imported with success (available) and as
            # such nothing need to be done for the fallback process
            if imported: continue

            # verifies if the (plugin) manager logger is available and if that't not the
            # case returns immediately (in error) otherwise prints the logging messages
            if not manager.logger: return False
            manager.logger.info("Package '%s' v%s does not exist in your system" % (self.name, self.version))
            if self.url: manager.logger.info("You can download the package at %s" % self.url)
            return False

        # returns a valid value to the caller method as the complete set of packages
        # were able to be imported with success (no problems occurred)
        return True

    def get_tuple(self):
        """
        Retrieves a tuple representing the package dependency,
        this value should include both the name and the proper
        version of it.

        :rtype: Tuple
        :return: A tuple representing the package dependency
        with both of its name and version.
        """

        return (
            self.package_name,
            self.package_version
        )

    def get_map(self):
        """
        Retrieves the map based representation of the current package
        dependency, this value may be used as a portable way to represent
        the current dependency.

        :rtype: Dictionary
        :return: The map based representation of the current package
        dependency to be used in a portable way.
        """

        return dict(
            type = "package",
            name = self.name,
            version = self.version
        )

class Condition(object):
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

        :rtype: bool
        :return: The result of the test (if successful or not).
        """

        return True

class OperativeSystemCondition(Condition):
    """
    The operative system condition class.
    """

    operative_system_name = None
    """ The operative system name, that is going to
    be "tested" as part of this condition structure """

    def __init__(self, operative_system_name = None):
        """
        Constructor of the class.

        :type operative_system_name: String
        :param operative_system_name: The operative system name.
        """

        self.operative_system_name = operative_system_name

    def test_condition(self):
        """
        Test the condition returning the result of the test.

        :rtype: bool
        :return: The result of the test (if successful or not).
        """

        if not Condition.test_condition(self): return False
        current_name = util.get_operative_system()
        is_same = current_name == self.operative_system_name
        if is_same: return True
        else: return False

class Capability(object):
    """
    Class that describes a neutral structure for a capability.
    """

    list_value = []
    """ The value of the capability described as a list """

    def __init__(self, string_value = None):
        """
        Constructor of the class.

        :type string_value: String
        :param string_value: The capability string value.
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
            if not list_value_self[index] == list_value_capability[index]:
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

        :rtype: List
        :return: The list of the capability and all super capabilities.
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

        :type capability: Capability
        :param capability: The capability to be tested.
        :rtype: bool
        :return: The result of the is sub capability test.
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
            if not list_value_self[index] == list_value_capability[index]:
                # returns false
                return False

        # returns true
        return True

    def is_capability_or_sub_capability(self, capability):
        """
        Tests if the given capability is a capability or sub capability.

        :type capability: Capability
        :param capability: The capability to be tested.
        :rtype: bool
        :return: The result of the is capability or sub capability test.
        """

        # in case the capability is equal or sub capability
        if self.__eq__(capability) or self.is_sub_capability(capability):
            # returns true
            return True
        # otherwise
        else:
            # returns false
            return False

class Event(object):
    """
    Class that describes a neutral structure for an event.
    """

    list_value = []
    """ The value of the event described as a list """

    def __init__(self, string_value = None):
        """
        Constructor of the class.

        :type string_value: String
        :param string_value: The event string value.
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
            if not list_value_self[index] == list_value_event[index]:
                # returns false
                return False

        # returns true
        return True

    def __ne__(self, event):
        return not self.__eq__(event)

    def is_sub_event(self, event):
        """
        Tests if the given event is sub event.

        :type event: Event
        :param event: The event to be tested.
        :rtype: bool
        :return: The result of the is sub event test.
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
            if not list_value_self[index] == list_value_event[index]:
                # returns false
                return False

        # returns true
        return True

    def is_event_or_sub_event(self, event):
        """
        Tests if the given event is a event or sub event.

        :type event: Event
        :param event: The event to be tested.
        :rtype: bool
        :return: The result of the is event or sub event test.
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

    :type capability: String
    :param capability: The capability to retrieve the the list of the
    capability and all super capabilities.
    :rtype: List
    :return: The list of the capability and all super capabilities.
    """

    # creates the capability structure from the capability string
    capability_structure = Capability(capability)

    # returns the list of the capability and all super capabilities
    return capability_structure.capability_and_super_capabilites()

def is_capability_or_sub_capability(base_capability, capability):
    """
    Tests if the given capability is capability or sub capability
    of the given base capability.

    :type base_capability: String
    :param base_capability: The base capability to be used for test.
    :type capability: String
    :param capability: The capability to be tested.
    :rtype: bool
    :return: The result of the test.
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

    :type base_capability: String
    :param base_capability: The base capability to be used for test.
    :type capability_list: List
    :param capability_list: The list of capabilities to be tested.
    :rtype: bool
    :return: The result of the test.
    """

    for capability in capability_list:
        is_valid = is_capability_or_sub_capability(base_capability, capability)
        if not is_valid: continue
        return True

    return False

def convert_to_capability_list(capability_list):
    """
    Converts the given capability list (list of strings),
    into a list of capability objects (structures).

    :type capability_list: List
    :param capability_list: The list of capability strings.
    :rtype: List
    :return: The list of converted capability objects (structures).
    """

    # creates the list of capability structures
    capability_list_structure = []

    # iterates over all the capabilities in the capability list
    for capability in capability_list:
        # retrieves the capability type
        capability_type = type(capability)

        # in case the capability type is tuple
        if capability_type == tuple:
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

    :type base_event: String
    :param base_event: The base event to be used for test.
    :type event: String
    :param event: The event to be tested.
    :rtype: bool
    :return: The result of the test.
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

    :type base_event: String
    :param base_event: The base event to be used for test.
    :type event: String
    :param event: The event to be tested.
    :rtype: bool
    :return: The result of the test.
    """

    # returns the result of the is event or sub event test
    # inverting the arguments
    return is_event_or_sub_event(event, base_event)

def is_event_or_sub_event_in_list(base_event, event_list):
    """
    Tests if any of the event in the event list is event or
    sub event of the given base event.

    :type base_event: String
    :param base_event: The base event to be used for test.
    :type event_list: List
    :param event_list: The list of events to be tested.
    :rtype: bool
    :return: The result of the test.
    """

    for event in event_list:
        is_valid = is_event_or_sub_event(base_event, event)
        if not is_valid: continue
        return True

    return False

def is_event_or_super_event_in_list(base_event, event_list):
    """
    Tests if any of the event in the event list is event or
    super event of the given base event.

    :type base_event: String
    :param base_event: The base event to be used for test.
    :type event_list: List
    :param event_list: The list of events to be tested.
    :rtype: bool
    :return: The result of the test.
    """

    for event in event_list:
        is_valid = is_event_or_super_event(base_event, event)
        if not is_valid: continue
        return True

    return False

def get_all_events_or_super_events_in_list(base_event, event_list):
    """
    Retrieves all the events or super events in the list.
    Filters the event list, retrieving only the event that are events or
    super events of the base event.

    :type base_event: String
    :param base_event: The base event to be used for filtering.
    :type event_list: List
    :param event_list: The list of events to be filtered.
    :rtype: List
    :return: The filtered list of events.
    """

    # creates the events or super events list
    events_or_super_events_list = []

    # iterates over all the events in the events list
    for event in event_list:
        # tests if the event is event or super event
        # of the base event and and adds it to the list
        # in case such validation is successful
        if not is_event_or_super_event(base_event, event): continue
        events_or_super_events_list.append(event)

    # returns the events or super events list
    return events_or_super_events_list

def convert_to_event_list(event_list):
    """
    Converts the given event list (list of strings),
    into a list of event objects (structures).

    :type event_list: List
    :param event_list: The list of event strings.
    :rtype: List
    :return: The list of converted event objects (structures).
    """

    # creates the list of event structures
    event_list_structure = []

    # iterates over all the events in the event list
    for event in event_list:
        # creates the event structure from the event
        # string and adds the event structure to the list
        # of event structures
        event_structure = Event(event)
        event_list_structure.append(event_structure)

    # returns the list of event structures
    return event_list_structure

class PluginThread(threading.Thread):
    """
    The plugin thread class, that is used to encapsulate
    the execution of a thread based plugin inside a new
    thread. These threads are "joined" at the end of the
    plugin manager execution (as expected).
    """

    plugin = None
    """ The reference to plugin to be used in the
    threads main execution process """

    load_complete = False
    """ The load complete flag """

    end_load_complete = False
    """ The end load complete flag """

    unload_complete = False
    """ The unload complete flag """

    end_unload_complete = False
    """ The end unload complete flag """

    load_plugin_thread = None
    """ The thread that controls the load plugin
    method call """

    end_load_plugin_thread = None
    """ The thread that controls the end load
    plugin method call """

    unload_plugin_thread = None
    """ The thread that controls the unload
    plugin method call """

    end_unload_plugin_thread = None
    """ The thread that controls the end unload
    plugin method call """

    event_queue = []
    """ The queue of events to be processed """

    condition = None
    """ The plugin thread condition """

    def __init__(self, plugin):
        """
        Constructor of the class.

        :type plugin: Plugin
        :param plugin: The plugin to be used.
        """

        threading.Thread.__init__(self)
        self.plugin = plugin

        self.daemon = True
        self.condition = threading.Condition()

        self.event_queue = []
        self.load_complete = False

    def set_load_complete(self, value):
        self.load_complete = value

    def set_end_load_complete(self, value):
        self.end_load_complete = value

    def set_unload_complete(self, value):
        self.unload_complete = value

    def set_end_unload_complete(self, value):
        self.end_unload_complete = value

    def add_event(self, event):
        """
        Adds an event to the event queue of the current plugin
        thread, this is done using the required synchronization
        mechanisms so that so race conditions are triggered.

        :type event: String
        :param event: The event to be added to the event queue.
        """

        self.condition.acquire()
        self.event_queue.append(event)
        self.condition.notify()
        self.condition.release()

    def process_event(self, event):
        """
        Processes the given queue event.

        :type event: Event
        :param event: The event to be processed.
        :rtype: bool
        :return: If the upper loop should be terminated.
        """

        if event.event_name == "exit":
            if self.load_plugin_thread and self.load_plugin_thread.isAlive() if\
                hasattr(self.load_plugin_thread, "isAlive") else self.load_plugin_thread.is_alive():
                self.load_plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)
            if self.end_load_plugin_thread and self.end_load_plugin_thread.isAlive() if\
                hasattr(self.end_load_plugin_thread, "isAlive") else self.end_load_plugin_thread.is_alive():
                self.end_load_plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)
            if self.unload_plugin_thread and self.unload_plugin_thread.isAlive() if\
                hasattr(self.unload_plugin_thread, "isAlive") else self.unload_plugin_thread.is_alive():
                self.unload_plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)
            if self.end_unload_plugin_thread and self.end_unload_plugin_thread.isAlive() if\
                hasattr(self.end_unload_plugin_thread, "isAlive") else self.end_unload_plugin_thread.is_alive():
                self.end_unload_plugin_thread.join(DEFAULT_UNLOAD_SYSTEM_TIMEOUT)
            return True
        elif event.event_name == "load":
            self.load_plugin_thread = PluginEventThread(self.plugin, self.plugin.load_plugin)
            self.load_plugin_thread.start()
            self.load_complete = True
        elif event.event_name == "lazy_load":
            self.lazy_load_plugin_thread = PluginEventThread(self.plugin, self.plugin.lazy_load_plugin)
            self.lazy_load_plugin_thread.start()
            self.load_complete = True
        elif event.event_name == "end_load":
            self.end_load_plugin_thread = PluginEventThread(self.plugin, self.plugin.end_load_plugin)
            self.end_load_plugin_thread.start()
            self.end_load_complete = True
        elif event.event_name == "unload":
            self.unload_plugin_thread = PluginEventThread(self.plugin, self.plugin.unload_plugin)
            self.unload_plugin_thread.start()
            self.unload_complete = True
        elif event.event_name == "end_unload":
            self.end_unload_plugin_thread = PluginEventThread(self.plugin, self.plugin.end_unload_plugin)
            self.end_unload_plugin_thread.start()
            self.end_unload_complete = True

    def run(self):
        """
        Starts running the thread, this should be considered
        the thread's main loop and consists of an even queue
        based iteration that processes requests.
        """

        while True:
            self.condition.acquire()
            while not len(self.event_queue):
                self.condition.wait()

            event = self.event_queue.pop(0)
            if self.process_event(event):
                self.condition.release()
                return

            self.condition.release()

class PluginEventThread(threading.Thread):
    """
    The plugin event thread class.
    """

    plugin = None
    """ The plugin that contains the method to be executed """

    method = None
    """ The method for the event thread """

    def __init__(self, plugin, method):
        """
        Constructor of the class.

        :type plugin: Plugin
        :param plugin: The plugin that contains the method to be executed.
        :type method: Method
        :param method: The method for the event thread.
        """

        threading.Thread.__init__(self)

        self.plugin = plugin
        self.method = method

        self.daemon = True

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
            except Exception as exception:
                # prints an error message to the current logging infra-structure
                # then sets the exception in the plugin instance and signals the
                # error state in the plugin (to be used latter)
                self.plugin.error("Problem starting thread plugin: " + legacy.UNICODE(exception))
                self.plugin.exception = exception
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
