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

import os
import sys
import inspect

def get_instance_module_directory(instance):
    """
    Retrieves the directory path from the given
    instance value.

    :type instance: Object
    :param instance: The instance value to be used to
    retrieve the module.
    :rtype: String
    :return: The path to the directory that contains
    the module with the given instance.
    """

    # retrieves the module name
    module_name = instance.__module__

    # retrieves the module from the modules map
    module = sys.modules[module_name]

    # retrieves the module file path
    module_file_path = module.__file__

    # retrieve the module directory path
    module_directory_path = os.path.dirname(module_file_path)

    # returns the module directory path
    return module_directory_path

def get_call_module_directory(depth_level = 1):
    """
    Retrieves the directory path for the calling
    module in the given depth level of the call stack.
    This function is extremely dangerous as it may
    not work in a large range of python implementations.

    :type depth_level: int
    :param depth_level: The depth level of the call
    stack to be reached to retrieve the module.
    :rtype: String
    :return: The path to the directory that contains
    the module reference in the given level of
    the call stack.
    """

    # retrieves the current call stack
    call_stack = inspect.stack()

    # retrieves the call stack element for the
    # required depth
    call_stack_element = call_stack[depth_level + 1]

    # retrieves the call stack element's frame
    call_stack_element_frame = call_stack_element[0]

    # retrieves the (call) module from the call stack element frame
    module = inspect.getmodule(call_stack_element_frame)

    # retrieves the module file path
    module_file_path = module.__file__

    # retrieve the module directory path
    module_directory_path = os.path.dirname(module_file_path)

    # returns the module directory path
    return module_directory_path
