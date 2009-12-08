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

import plugin_system

def load_plugin(plugin_id, plugin_version, lazy_loading = False, metadata_enabled = True):
    """
    Decorator for the initial load of the plugin.

    @type plugin_id: String
    @param plugin_id: The id of the plugin to be loaded with allowed plugins.
    @type plugin_version: String
    @param plugin_version: The version of the plugin to be loaded with allowed plugins.
    @type lazy_loading: bool
    @param lazy_loading: The boolean flag to set the type of loading for the plugin.
    @type metadata_enabled: bool
    @param metadata_enabled: The boolean flag to set the metadata availability.
    @rtype: function
    @return: The created decorator.
    """

    def create_decorator_interceptor(func):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        @type func: function
        @param func: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the load_allowed decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # calls the callback function
            func(*args, **kwargs)

            # retrieves the plugin instance
            plugin = args[0]

            # retrieves the plugin tupple from the plugin information
            plugin_tuple = (plugin.id, plugin.version)

            # retrieves the metadata map for the current plugin
            metadata_map = load_plugin.load_plugin_map[plugin_tuple]["metadata"]

            # sets the metadata map in the plugin instance
            plugin.metadata_map = metadata_map

        return decorator_interceptor

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the load_allowed decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The decorator interceptor function.
        """

        # creates the plugin tuple using the plugin id and version
        plugin_tuple = (plugin_id, plugin_version)

        if not load_plugin.load_plugin_map:
            load_plugin.load_plugin_map = {}
        load_plugin.load_plugin_map[plugin_tuple] = {}

        load_plugin.load_plugin_map[plugin_tuple]["metadata"] = {}

        load_plugin.plugin_id = plugin_id
        load_plugin.plugin_version = plugin_version

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(func)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

load_plugin.load_plugin_map = None

def plugin_meta_information(metadata_key, metadata_values = {}):
    """
    Decorator that sets a defined metadata value in a plugin.

    @type metadata_key: String
    @param metadata_key: The metadata key to process the metadata.
    @type metadata_values: Dictionary
    @param metadata_values: The dictionary containing the metadata values.
    @rtype: function
    @return: The created decorator.
    """

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the plugin_meta_information decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The decorator interceptor function.
        """

        # creates the load plugin tuple
        load_plugin_tuple = (load_plugin.plugin_id, load_plugin.plugin_version)

        # retrieves the metadata plugin map
        metadata_plugin_map = load_plugin.load_plugin_map[load_plugin_tuple]["metadata"]

        # in case the metadata key does not exist in the metadata plugin map
        if not metadata_key in metadata_plugin_map:
            metadata_plugin_map[metadata_key] = []

        # retrieves the function name
        function_name = func.__name__

        # sets the value for the metadata method name
        metadata_values["method_name"] = function_name

        # appends the metadata values to the list of values with the same metadata key
        metadata_plugin_map[metadata_key].append(metadata_values)

        return func

    # returns the created decorator
    return decorator

def load_allowed(plugin_id, plugin_version, load_plugin = False):
    """
    Decorator that loads the allowed plugins into the defined methods.

    @type plugin_id: String
    @param plugin_id: The id of the plugin to be loaded with allowed plugins.
    @type plugin_version: String
    @param plugin_version: The version of the plugin to be loaded with allowed plugins.
    @type load_plugin: bool
    @param load_plugin: The load plugin flag to set the test for plugin loading.
    @rtype: function
    @return: The created decorator.
    """

    def create_decorator_interceptor(func):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        @type func: function
        @param func: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the load_allowed decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # calls the callback function
            func(*args, **kwargs)

            original_plugin = args[0]
            allowed_plugin = args[1]
            capability = args[2]

            original_plugin_tuple = (original_plugin.id, original_plugin.version)
            allowed_plugin_tuple = (allowed_plugin.id, allowed_plugin.version)

            if original_plugin_tuple in load_allowed.load_allowed_map:
                allowed_functions_map = load_allowed.load_allowed_map[original_plugin_tuple]
                for capability_key in allowed_functions_map:
                    if plugin_system.is_capability_or_sub_capability(capability_key, capability):
                        capability_function = allowed_functions_map[capability]
                        capability_function_name = capability_function.__name__
                        capability_method = getattr(original_plugin, capability_function_name)
                        capability_method(allowed_plugin, capability)

        return decorator_interceptor

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the load_allowed decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The decorator interceptor function.
        """

        # creates the plugin tuple using the plugin id and version
        plugin_tuple = (plugin_id, plugin_version)

        if not load_allowed.load_allowed_map:
            load_allowed.load_allowed_map = {}
        load_allowed.load_allowed_map[plugin_tuple] = {}

        load_allowed.plugin_id = plugin_id
        load_allowed.plugin_version = plugin_version

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(func)

        if load_plugin:
            decorator_interceptor_function = create_load_plugin_interceptor(decorator_interceptor_function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def load_allowed_capability(capability, load_plugin = False):
    """
    Decorator that marks a method for loading of allowed plugins.

    @type capability: String
    @param capability: The name of the capability to be loaded.
    @type load_plugin: bool
    @param load_plugin: The load plugin flag to set the test for plugin loading.
    @rtype: function
    @return: The created decorator.
    """

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the load_allowed_capability decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The function to be decorated.
        """

        load_allowed.func = func

        load_allowed_tuple = (load_allowed.plugin_id, load_allowed.plugin_version)
        load_allowed.load_allowed_map[load_allowed_tuple][capability] = load_allowed.func

        if load_plugin:
            decorator_interceptor_function = create_load_plugin_interceptor(func)
        else:
            decorator_interceptor_function = func

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

load_allowed.load_allowed_map = None

def unload_allowed(plugin_id, plugin_version, load_plugin = False):
    """
    Decorator that unloads the allowed plugins into the defined methods.

    @type plugin_id: String
    @param plugin_id: The id of the plugin to be unloaded with allowed plugins.
    @type plugin_version: String
    @param plugin_version: The version of the plugin to be unloaded with allowed plugins.
    @type load_plugin: bool
    @param load_plugin: The load plugin flag to set the test for plugin loading.
    @rtype: function
    @return: The created decorator.
    """

    def create_decorator_interceptor(func):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        @type func: function
        @param func: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the unload_allowed decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # calls the callback function
            func(*args, **kwargs)

            original_plugin = args[0]
            allowed_plugin = args[1]
            capability = args[2]

            original_plugin_tuple = (original_plugin.id, original_plugin.version)
            allowed_plugin_tuple = (allowed_plugin.id, allowed_plugin.version)

            if original_plugin_tuple in unload_allowed.unload_allowed_map:
                allowed_functions_map = unload_allowed.unload_allowed_map[original_plugin_tuple]
                for capability_key in allowed_functions_map:
                    if plugin_system.is_capability_or_sub_capability(capability_key, capability):
                        capability_function = allowed_functions_map[capability]
                        capability_function_name = capability_function.__name__
                        capability_method = getattr(original_plugin, capability_function_name)
                        capability_method(allowed_plugin, capability)

        return decorator_interceptor

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the unload_allowed decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The decorator interceptor function.
        """

        # creates the plugin tuple using the plugin id and version
        plugin_tuple = (plugin_id, plugin_version)

        if not unload_allowed.unload_allowed_map:
            unload_allowed.unload_allowed_map = {}
        unload_allowed.unload_allowed_map[plugin_tuple] = {}

        unload_allowed.plugin_id = plugin_id
        unload_allowed.plugin_version = plugin_version

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(func)

        if load_plugin:
            decorator_interceptor_function = create_load_plugin_interceptor(decorator_interceptor_function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def unload_allowed_capability(capability, load_plugin = False):
    """
    Decorator that marks a method for unloading of allowed plugins.

    @type capability: String
    @param capability: The name of the capability to be unloaded.
    @type load_plugin: bool
    @param load_plugin: The load plugin flag to set the test for plugin loading.
    @rtype: function
    @return: The created decorator.
    """

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the unload_allowed_capability decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The function to be decorated.
        """

        unload_allowed.func = func

        unload_allowed_tuple = (unload_allowed.plugin_id, unload_allowed.plugin_version)
        unload_allowed.unload_allowed_map[unload_allowed_tuple][capability] = unload_allowed.func

        if load_plugin:
            decorator_interceptor_function = create_load_plugin_interceptor(func)
        else:
            decorator_interceptor_function = func

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

unload_allowed.unload_allowed_map = None

def inject_dependencies(plugin_id, plugin_version, load_plugin = False):
    """
    Decorator that injects the dependencies into the defined methods.

    @type plugin_id: String
    @param plugin_id: The id of the plugin to be injected with dependencies.
    @type plugin_version: String
    @param plugin_version: The version of the plugin to be injected with dependencies.
    @type load_plugin: bool
    @param load_plugin: The load plugin flag to set the test for plugin loading.
    @rtype: function
    @return: The created decorator.
    """

    def create_decorator_interceptor(func):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        @type func: function
        @param func: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the inject_dependencies decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # calls the callback function
            func(*args, **kwargs)

            original_plugin = args[0]
            dependency_plugin = args[1]

            original_plugin_tuple = (original_plugin.id, original_plugin.version)
            dependency_plugin_tuple = (dependency_plugin.id, dependency_plugin.version)

            if original_plugin_tuple in inject_dependencies.inject_dependencies_map:
                dependency_functions_map = inject_dependencies.inject_dependencies_map[original_plugin_tuple]
                if dependency_plugin_tuple in dependency_functions_map:
                    set_function = dependency_functions_map[dependency_plugin_tuple]
                    set_function_name = set_function.__name__
                    set_method = getattr(original_plugin, set_function_name)
                    set_method(dependency_plugin)
                elif (dependency_plugin.id, None) in dependency_functions_map:
                    set_function = dependency_functions_map[(dependency_plugin.id, None)]
                    set_function_name = set_function.__name__
                    set_method = getattr(original_plugin, set_function_name)
                    set_method(dependency_plugin)

        return decorator_interceptor

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the inject_dependencies decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The decorator interceptor function.
        """

        # creates the plugin tuple using the plugin id and version
        plugin_tuple = (plugin_id, plugin_version)

        if not inject_dependencies.inject_dependencies_map:
            inject_dependencies.inject_dependencies_map = {}
        inject_dependencies.inject_dependencies_map[plugin_tuple] = {}

        inject_dependencies.plugin_id = plugin_id
        inject_dependencies.plugin_version = plugin_version

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(func)

        if load_plugin:
            decorator_interceptor_function = create_load_plugin_interceptor(decorator_interceptor_function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def plugin_inject(plugin_id, plugin_version = None, load_plugin = False):
    """
    Decorator that marks a method for injection of a dependency.

    @type plugin_id: String
    @param plugin_id: The id of the plugin dependency to be injected.
    @type plugin_version: String
    @param plugin_version: The version of the plugin dependency to be injected.
    @type load_plugin: bool
    @param load_plugin: The load plugin flag to set the test for plugin loading.
    @rtype: function
    @return: The created decorator.
    """

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the plugin_inject decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The function to be decorated.
        """

        plugin_inject.func = func

        inject_dependencies_tuple = (inject_dependencies.plugin_id, inject_dependencies.plugin_version)
        inject_dependencies.inject_dependencies_map[inject_dependencies_tuple][plugin_id, plugin_version] = plugin_inject.func

        if load_plugin:
            decorator_interceptor_function = create_load_plugin_interceptor(func)
        else:
            decorator_interceptor_function = func

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

inject_dependencies.inject_dependencies_map = None

def event_handler(plugin_id, plugin_version, load_plugin = False):
    """
    Decorator that redirects the event handling into the defined methods.

    @type plugin_id: String
    @param plugin_id: The id of the plugin to take care of the event handling.
    @type plugin_version: String
    @param plugin_version: The version of the plugin to take care of the event handling.
    @type load_plugin: bool
    @param load_plugin: The load plugin flag to set the test for plugin loading.
    @rtype: function
    @return: The created decorator.
    """

    def create_decorator_interceptor(func):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        @type func: function
        @param func: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the event_handler decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # calls the callback function
            func(*args, **kwargs)

            original_plugin = args[0]
            event_name = args[1]
            event_args = args[2:]
            all_method_args = args[1:]

            original_plugin_tuple = (original_plugin.id, original_plugin.version)

            if original_plugin_tuple in event_handler.event_handler_methods_map:
                event_handler_functions_map = event_handler.event_handler_methods_map[original_plugin_tuple]
                for event_name_key in event_handler_functions_map:
                    if plugin_system.is_event_or_sub_event(event_name_key, event_name):
                        event_handler_function = event_handler_functions_map[event_name_key]
                        event_handler_function_name = event_handler_function.__name__
                        event_handler_method = getattr(original_plugin, event_handler_function_name)

                        # retrieves the number of arguments for the function
                        number_arguments = event_handler_function.func_code.co_argcount

                        # in case the length of the arguments is insufficient
                        if len(all_method_args) < number_arguments:
                            # adds padding to the call arguments
                            call_args = list(all_method_args) + [None]
                        else:
                            # maintains the calling arguments
                            call_args = all_method_args

                        # calls the event handler method
                        event_handler_method(*call_args)

        return decorator_interceptor

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the event_handler decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The decorator interceptor function.
        """

        # creates the plugin tuple using the plugin id and version
        plugin_tuple = (plugin_id, plugin_version)

        if not event_handler.event_handler_methods_map:
            event_handler.event_handler_methods_map = {}
        event_handler.event_handler_methods_map[plugin_tuple] = {}

        event_handler.plugin_id = plugin_id
        event_handler.plugin_version = plugin_version

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(func)

        if load_plugin:
            decorator_interceptor_function = create_load_plugin_interceptor(decorator_interceptor_function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def event_handler_method(event_name, load_plugin = False):
    """
    Decorator that marks a method for event handling.

    @type event_name: String
    @param event_name: The name of the event to be handled by the marked method.
    @type load_plugin: bool
    @param load_plugin: The load plugin flag to set the test for plugin loading.
    @rtype: function
    @return: The created decorator.
    """

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the event_handler_method decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The function to be decorated.
        """

        event_handler_method.func = func

        event_handler_tuple = (event_handler.plugin_id, event_handler.plugin_version)
        event_handler.event_handler_methods_map[event_handler_tuple][event_name] = event_handler_method.func

        if load_plugin:
            decorator_interceptor_function = create_load_plugin_interceptor(func)
        else:
            decorator_interceptor_function = func

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

event_handler.event_handler_methods_map = None

def plugin_call(load_plugin = True):
    """
    Decorator that intercepts a plugin front-end call method.

    @type load_plugin: bool
    @param load_plugin: The load plugin flag to set the test for plugin loading.
    @rtype: function
    @return: The created decorator.
    """

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the plugin_call decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The decorator interceptor function.
        """

        if load_plugin:
            decorator_interceptor_function = create_load_plugin_interceptor(func)
        else:
            decorator_interceptor_function = func

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def create_load_plugin_interceptor(func):
    """
    Creates a load plugin interceptor, that loads a lazy plugin on the fly.

    @type func: function
    @param func: The callback function.
    """

    def decorator_interceptor(*args, **kwargs):
        """
        The interceptor function for the decorator.

        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        """

        # retrieves the original plugin instance
        original_plugin = args[0]

        # in case the plugin is not yet loaded
        if not original_plugin.is_loaded():
            plugin_manager = original_plugin.manager
            original_plugin_id = original_plugin.id

            # in case the plugin load was unsucessfull
            if not plugin_manager.load_plugin(original_plugin_id, plugin_system.FULL_LOAD_TYPE):
                return None

        # calls the callback function
        return func(*args, **kwargs)

    return decorator_interceptor

def unregister_plugin_decorators(plugin_id, plugin_version):
    """
    Unregisters the decorators for the plugin with the given id and version.

    @type plugin_id: String
    @param plugin_id: The id of the plugin to unregister the decorators.
    @type plugin_version: String
    @param plugin_version: The version of the plugin to unregister the decorators.
    """

    # creates the plugin tuple for the refered plugin
    plugin_tuple = (plugin_id, plugin_version)

    if load_allowed.load_allowed_map and plugin_tuple in load_allowed.load_allowed_map:
        del load_allowed.load_allowed_map[plugin_tuple]
    if unload_allowed.unload_allowed_map and plugin_tuple in unload_allowed.unload_allowed_map:
        del unload_allowed.unload_allowed_map[plugin_tuple]
    if inject_dependencies.inject_dependencies_map and plugin_tuple in inject_dependencies.inject_dependencies_map:
        del inject_dependencies.inject_dependencies_map[plugin_tuple]
    if event_handler.event_handler_methods_map and plugin_tuple in event_handler.event_handler_methods_map:
        del event_handler.event_handler_methods_map[plugin_tuple]
