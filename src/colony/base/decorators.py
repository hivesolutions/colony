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

from . import system
from . import legacy

METHOD_NAME_VALUE = "method_name"
""" The method name value """

def load_plugin(lazy_loading = False, metadata_enabled = True):
    """
    Decorator for the initial load of the plugin.

    :type lazy_loading: bool
    :param lazy_loading: The boolean flag to set the type of loading for the plugin.
    :type metadata_enabled: bool
    :param metadata_enabled: The boolean flag to set the metadata availability.
    :rtype: Function
    :return: The created decorator.
    """

    def create_decorator_interceptor(function):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        :type function: Function
        :param function: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the load allowed decorator.
            """

            # calls the callback function
            function(*args, **kwargs)

            # retrieves the plugin instance
            plugin = args[0]

            # retrieves the metadata map for the current plugin
            metadata_map = function.metadata

            # sets the metadata map in the plugin instance
            plugin.metadata_map = metadata_map

        # returns the decorator interceptor
        return decorator_interceptor

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the load allowed decorator.

        :type function: Function
        :param function: The function to be decorated.
        :rtype: Function
        :return: The decorator interceptor function.
        """

        # starts the matadata map for
        # the current function
        function.metadata = {}

        # sets the current load plugin function
        # for the load allowed reference
        load_plugin.current = function

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def plugin_meta_information(metadata_key, metadata_values = {}):
    """
    Decorator that sets a defined metadata value in a plugin.

    :type metadata_key: String
    :param metadata_key: The metadata key to process the metadata.
    :type metadata_values: Dictionary
    :param metadata_values: The dictionary containing the metadata values.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the plugin meta information decorator.

        :type function: Function
        :param function: The function to be decorated.
        :rtype: Function
        :return: The decorator interceptor function.
        """

        # retrieves the current load plugin function
        load_plugin_current = load_plugin.current

        # retrieves the metadata plugin map
        metadata_plugin_map = load_plugin_current.metadata

        # in case the metadata key does not exist in the metadata plugin map
        if not metadata_key in metadata_plugin_map:
            # creates a new list for the metadata key
            metadata_plugin_map[metadata_key] = []

        # retrieves the function name
        function_name = function.__name__

        # sets the value for the metadata method name
        metadata_values[METHOD_NAME_VALUE] = function_name

        # appends the metadata values to the list of values with the same metadata key
        metadata_plugin_map[metadata_key].append(metadata_values)

        # returns the function
        return function

    # returns the created decorator
    return decorator

def load_allowed(function):
    """
    Decorator that loads the allowed plugins into the defined methods.

    :type function: Function
    :param function: The function to be decorated.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator_interceptor(*args, **kwargs):
        """
        The interceptor function for the load allowed decorator.
        """

        # calls the callback function
        function(*args, **kwargs)

        # retrieves the allowed functions map
        allowed_functions_map = function.allowed_functions_map

        # unpacks the various arguments for the function
        original_plugin = args[0]
        allowed_plugin = args[1]
        capability = args[2]

        # iterates over all the capabilities in the allowed
        # functions map
        for capability_key in allowed_functions_map:
            # checks if the capability is a valid capability for the plugin
            # currently being handled and skips the current iteration
            # in case it's not
            if not system.is_capability_or_sub_capability(capability_key, capability):
                # continues the loop
                continue

            # retrieves the capability function name from the allowed
            # functions map
            capability_function = allowed_functions_map[capability]
            capability_function_name = capability_function.__name__

            # retrieves the capability method from the original plugin and
            # handles the capability
            capability_method = getattr(original_plugin, capability_function_name)
            capability_method(allowed_plugin, capability)

    # starts the allowed functions map for
    # the current function
    function.allowed_functions_map = {}

    # sets the current load allowed function
    # for the load allowed reference
    load_allowed.current = function

    # returns the decorator interceptor
    return decorator_interceptor

def load_allowed_capability(capability, load_plugin = False):
    """
    Decorator that marks a method for loading of allowed plugins.

    :type capability: String
    :param capability: The name of the capability to be loaded.
    :type load_plugin: bool
    :param load_plugin: The load plugin flag to set the test for plugin loading.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the load allowed capability decorator.

        :type function: Function
        :param function: The function to be decorated.
        :rtype: Function
        :return: The function to be decorated.
        """

        # retrieves the current load allowed function
        load_allowed_current = load_allowed.current

        # sets the current function for capability handling
        # in the current function
        load_allowed_current.allowed_functions_map[capability] = function

        # in case the load plugin test should be made before loading
        # the capability
        if load_plugin:
            # creates the new decorator interceptor function
            decorator_interceptor_function = create_load_plugin_interceptor(function)
        # otherwise the normal approach is set
        else:
            # sets the decorator interceptor function as the function
            decorator_interceptor_function = function

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def unload_allowed(function):
    """
    Decorator that unloads the allowed plugins into the defined methods.

    :type function: Function
    :param function: The function to be decorated.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator_interceptor(*args, **kwargs):
        """
        The interceptor function for the unload allowed decorator.
        """

        # calls the callback function
        function(*args, **kwargs)

        # retrieves the allowed functions map
        allowed_functions_map = function.allowed_functions_map

        # unpacks the various arguments for the function
        original_plugin = args[0]
        allowed_plugin = args[1]
        capability = args[2]

        # iterates over all the capabilities in the allowed
        # functions map
        for capability_key in allowed_functions_map:
            # checks if the capability is a valid capability for the plugin
            # currently being handled and skips the current iteration
            # in case it's not
            if not system.is_capability_or_sub_capability(capability_key, capability):
                # continues the loop
                continue

            # retrieves the capability function name from the allowed
            # functions map
            capability_function = allowed_functions_map[capability]
            capability_function_name = capability_function.__name__

            # retrieves the capability method from the original plugin and
            # handles the capability
            capability_method = getattr(original_plugin, capability_function_name)
            capability_method(allowed_plugin, capability)

    # starts the allowed functions map for
    # the current function
    function.allowed_functions_map = {}

    # sets the current unload allowed function
    # for the unload allowed reference
    unload_allowed.current = function

    # returns the decorator interceptor
    return decorator_interceptor

def unload_allowed_capability(capability, load_plugin = False):
    """
    Decorator that marks a method for unloading of allowed plugins.

    :type capability: String
    :param capability: The name of the capability to be unloaded.
    :type load_plugin: bool
    :param load_plugin: The load plugin flag to set the test for plugin loading.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the unload allowed capability decorator.

        :type function: Function
        :param function: The function to be decorated.
        :rtype: Function
        :return: The function to be decorated.
        """

        # retrieves the current unload allowed function
        unload_allowed_current = unload_allowed.current

        # sets the current function for capability handling
        # in the current function
        unload_allowed_current.allowed_functions_map[capability] = function

        # in case the load plugin test should be made before unloading
        # the capability
        if load_plugin:
            # creates the new decorator interceptor function
            decorator_interceptor_function = create_load_plugin_interceptor(function)
        # otherwise the normal approach is set
        else:
            # sets the decorator interceptor function as the function
            decorator_interceptor_function = function

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def inject_dependencies(function):
    """
    Decorator that injects the dependencies into the defined methods.

    :type function: Function
    :param function: The function to be decorated.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator_interceptor(*args, **kwargs):
        """
        The interceptor function for the inject dependencies decorator.
        """

        # calls the callback function
        function(*args, **kwargs)

        # retrieves the dependency functions map
        dependency_functions_map = function.dependency_functions_map

        # retrieves the original plugin
        original_plugin = args[0]

        # retrieves the dependency plugin
        dependency_plugin = args[1]

        # creates the dependency plugin tuple
        dependency_plugin_tuple = (
            dependency_plugin.original_id,
            dependency_plugin.version
        )

        # creates the dependency plugin simple tuple
        # this tuple only contains the
        dependency_plugin_simple_tuple = (
            dependency_plugin.original_id,
            None
        )

        # tries to retrieve the set function using both the complete plugin id and
        # version approach and the version only approach
        set_function = dependency_functions_map.get(dependency_plugin_tuple, None)
        set_function = set_function or dependency_functions_map.get(dependency_plugin_simple_tuple, None)

        # in case the set function is not defined
        if not set_function:
            # returns immediately
            return

        # retrieves the set function name from the dependency functions map
        set_function = dependency_functions_map[dependency_plugin_simple_tuple]
        set_function_name = set_function.__name__

        # calls the set method from the original plugin instance
        set_method = getattr(original_plugin, set_function_name)
        set_method(dependency_plugin)

    # starts the dependency functions map for
    # the current function
    function.dependency_functions_map = {}

    # sets the current inject dependencies function
    # for the inject dependencies reference
    inject_dependencies.current = function

    # returns the decorator interceptor
    return decorator_interceptor

def plugin_inject(plugin_id, plugin_version = None, load_plugin = False):
    """
    Decorator that marks a method for injection of a dependency.

    :type plugin_id: String
    :param plugin_id: The id of the plugin dependency to be injected.
    :type plugin_version: String
    :param plugin_version: The version of the plugin dependency to be injected.
    :type load_plugin: bool
    :param load_plugin: The load plugin flag to set the test for plugin loading.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the plugin inject decorator.

        :type function: Function
        :param function: The function to be decorated.
        :rtype: Function
        :return: The function to be decorated.
        """

        # creates the dependency plugin tuple
        dependency_plugin_tuple = (
            plugin_id,
            plugin_version
        )

        # retrieves the current inject dependencies function
        inject_dependencies_current = inject_dependencies.current

        # sets the current function for dependency injection
        # in the current function
        inject_dependencies_current.dependency_functions_map[dependency_plugin_tuple] = function

        # in case the load plugin test should be made before injecting
        # the dependency
        if load_plugin:
            # creates the new decorator interceptor functions
            decorator_interceptor_function = create_load_plugin_interceptor(function)
        # otherwise the normal approach is set
        else:
            # sets the decorator interceptor function as the function
            decorator_interceptor_function = function

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def event_handler(function):
    """
    Decorator that redirects the event handling into the defined methods.

    :type function: Function
    :param function: The function to be decorated.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator_interceptor(*args, **kwargs):
        """
        The interceptor function for the event handler decorator.
        """

        # calls the callback function
        function(*args, **kwargs)

        # retrieves the event handler functions map
        event_handler_functions_map = function.event_handler_functions_map

        # unpacks the function arguments
        original_plugin = args[0]
        event_name = args[1]
        all_method_args = args[1:]

        # iterates over all the events in the evens in the event handler
        # functions map
        for event_name_key in event_handler_functions_map:
            # checks if the event is a valid event for the plugin
            # currently being handled and skips the current iteration
            # in case it's not
            if not system.is_event_or_sub_event(event_name_key, event_name):
                # continues the loop
                continue

            # retrieves the event handler function from event handler functions map
            event_handler_function = event_handler_functions_map[event_name_key]

            # retrieves the function name and the event handler method from the original
            # plugin
            event_handler_function_name = event_handler_function.__name__
            event_handler_method = getattr(original_plugin, event_handler_function_name)

            # retrieves the number of arguments for the function by
            # inspecting the specification of the function, this may
            # be an expensive operation and should be used with care
            spec = legacy.getargspec(event_handler_function)
            number_arguments = len(spec.args)

            # in case the length of the arguments is insufficient
            if len(all_method_args) < number_arguments:
                # adds padding to the call arguments
                call_args = list(all_method_args) + [None]
            else:
                # maintains the calling arguments
                call_args = all_method_args

            # calls the event handler method
            event_handler_method(*call_args)

    # starts the event handler functions map for
    # the current function
    function.event_handler_functions_map = {}

    # sets the current event handler function
    # for the event handler reference
    event_handler.current = function

    # returns the decorator interceptor
    return decorator_interceptor

def event_handler_method(event_name, load_plugin = False):
    """
    Decorator that marks a method for event handling.

    :type event_name: String
    :param event_name: The name of the event to be handled by the marked method.
    :type load_plugin: bool
    :param load_plugin: The load plugin flag to set the test for plugin loading.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the event handler method decorator.

        :type function: Function
        :param function: The function to be decorated.
        :rtype: Function
        :return: The function to be decorated.
        """

        # retrieves the current event handler function
        event_handler_current = event_handler.current

        # sets the current function for event handling
        # in the current function
        event_handler_current.event_handler_functions_map[event_name] = function

        # in case the load plugin test should be made before handling
        # the event
        if load_plugin:
            # creates the new decorator interceptor functions
            decorator_interceptor_function = create_load_plugin_interceptor(function)
        # otherwise the normal approach is set
        else:
            # sets the decorator interceptor function as the function
            decorator_interceptor_function = function

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def set_configuration_property(function):
    """
    Decorator that redirects the setting of configuration properties into the defined methods.

    :type function: Function
    :param function: The function to be decorated.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator_interceptor(*args, **kwargs):
        """
        The interceptor function for the set configuration
        property decorator.
        """

        # calls the callback function
        function(*args, **kwargs)

        # retrieves the set configuration property functions map
        set_configuration_property_functions_map = function.set_configuration_property_functions_map

        # unpacks the function arguments
        original_plugin = args[0]
        property_name = args[1]
        property = args[2]

        # in case the property name is not defined in the set configuration
        # property functions map
        if not property_name in set_configuration_property_functions_map:
            # returns immediately
            return

        # retrieves the set configuration property function from set configuration property functions map
        set_configuration_property_function = set_configuration_property_functions_map[property_name]

        # retrieves the function name and the set configuration property method from the original
        # plugin
        set_configuration_property_function_name = set_configuration_property_function.__name__
        set_configuration_property_method = getattr(original_plugin, set_configuration_property_function_name)

        # calls the set configuration property method
        set_configuration_property_method(property_name, property)

    # starts the set configuration property functions map for
    # the current function
    function.set_configuration_property_functions_map = {}

    # sets the current set configuration property function
    # for the set configuration property reference
    set_configuration_property.current = function

    # returns the decorator interceptor
    return decorator_interceptor

def set_configuration_property_method(property_name, load_plugin = False):
    """
    Decorator that marks a method for set configuration property.

    :type property_name: String
    :param property_name: The name of the property to be set by the marked method.
    :type load_plugin: bool
    :param load_plugin: The load plugin flag to set the test for plugin loading.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the set configuration property decorator.

        :type function: Function
        :param function: The function to be decorated.
        :rtype: Function
        :return: The function to be decorated.
        """

        # retrieves the current set configuration property function
        set_configuration_property_current = set_configuration_property.current

        # sets the current function for set configuration property
        # in the current function
        set_configuration_property_current.set_configuration_property_functions_map[property_name] = function

        # in case the load plugin test should be made before setting
        # the configuration property
        if load_plugin:
            # creates the new decorator interceptor functions
            decorator_interceptor_function = create_load_plugin_interceptor(function)
        # otherwise the normal approach is set
        else:
            # sets the decorator interceptor function as the function
            decorator_interceptor_function = function

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def unset_configuration_property(function):
    """
    Decorator that redirects the unsetting of configuration
    properties into the defined methods.

    :type function: Function
    :param function: The function to be decorated.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator_interceptor(*args, **kwargs):
        """
        The interceptor function for the unset configuration
        property decorator.
        """

        # calls the callback function
        function(*args, **kwargs)

        # retrieves the unset configuration property functions map
        unset_configuration_property_functions_map = function.unset_configuration_property_functions_map

        # unpacks the function arguments
        original_plugin = args[0]
        property_name = args[1]

        # in case the property name is not defined in the unset configuration
        # property functions map
        if not property_name in unset_configuration_property_functions_map:
            # returns immediately
            return

        # retrieves the unset configuration property function from unset configuration property functions map
        unset_configuration_property_function = unset_configuration_property_functions_map[property_name]

        # retrieves the function name and the unset configuration property method from the original
        # plugin
        unset_configuration_property_function_name = unset_configuration_property_function.__name__
        unset_configuration_property_method = getattr(original_plugin, unset_configuration_property_function_name)

        # calls the unset configuration property method
        unset_configuration_property_method(property_name)

    # starts the unset configuration property functions map for
    # the current function
    function.unset_configuration_property_functions_map = {}

    # unsets the current unset configuration property function
    # for the unset configuration property reference
    unset_configuration_property.current = function

    # returns the decorator interceptor
    return decorator_interceptor

def unset_configuration_property_method(property_name, load_plugin = False):
    """
    Decorator that marks a method for unset configuration property.

    :type property_name: String
    :param property_name: The name of the property to be unset by the marked method.
    :type load_plugin: bool
    :param load_plugin: The load plugin flag to unset the test for plugin loading.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the unset configuration property decorator.

        :type function: Function
        :param function: The function to be decorated.
        :rtype: Function
        :return: The function to be decorated.
        """

        # retrieves the current unset configuration property function
        unset_configuration_property_current = unset_configuration_property.current

        # unsets the current function for unset configuration property
        # in the current function
        unset_configuration_property_current.unset_configuration_property_functions_map[property_name] = function

        # in case the load plugin test should be made before unsetting
        # the configuration property
        if load_plugin:
            # creates the new decorator interceptor functions
            decorator_interceptor_function = create_load_plugin_interceptor(function)
        # otherwise the normal approach is unset
        else:
            # unsets the decorator interceptor function as the function
            decorator_interceptor_function = function

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def plugin_call(load_plugin = True):
    """
    Decorator that intercepts a plugin front-end call method.

    :type load_plugin: bool
    :param load_plugin: The load plugin flag to set the test for plugin loading.
    :rtype: Function
    :return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the plugin call decorator.

        :type function: Function
        :param function: The function to be decorated.
        :rtype: Function
        :return: The decorator interceptor function.
        """

        if load_plugin:
            decorator_interceptor_function = create_load_plugin_interceptor(function)
        else:
            decorator_interceptor_function = function

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def create_load_plugin_interceptor(function):
    """
    Creates a load plugin interceptor, that loads a lazy plugin on the fly.

    :type function: Function
    :param function: The callback function.
    """

    def decorator_interceptor(*args, **kwargs):
        """
        The interceptor function for the decorator.
        """

        # retrieves the original plugin instance
        original_plugin = args[0]

        # in case the plugin is not yet loaded
        if not original_plugin.is_loaded():
            plugin_manager = original_plugin.manager
            original_plugin_id = original_plugin.id

            # in case the plugin load was unsuccessful
            if not plugin_manager.load_plugin(original_plugin_id, system.FULL_LOAD_TYPE):
                return None

        # calls the callback function
        return function(*args, **kwargs)

    # returns the decorator interceptor
    return decorator_interceptor
