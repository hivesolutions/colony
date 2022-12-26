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

def visit(ast_node_class):

    def decorator(function, *args, **kwargs):
        function.ast_node_class = ast_node_class
        return function

    return decorator

def dispatch_visit(map_name = "node_method_map"):

    def create_interceptor(function):

        def decorator_interceptor(*args, **kwargs):
            # unpacks the first two "unnamed" arguments as the self
            # instance reference and the node element to be visited
            self = args[0]
            node = args[1]

            # verifies if the current instance contains the node method
            # map if that's the case retrieves otherwise falls back to an
            # empty dictionary (for code compatibility)
            has_map = hasattr(self, map_name)
            node_method_map = self.node_method_map if has_map else dict()

            # retrieves the class for the node argument and then
            # gathers the complete mro class definition to be able
            # to iterate over the class hierarchy
            node_class = node.__class__
            mro = node_class.mro()

            # iterates over the complete class hierarchy for the provided
            # node (from bottom to up) so that the best match for the
            # visit operation is found and properly called
            for mro_item in mro:
                # in case the current mro item class level is nor found
                # skips the current iteration (cannot visit at this level)
                if not mro_item in node_method_map: continue

                # the current class level is valid and so the proper method
                # is retrieved from the map and then called with the provided
                # arguments, note that a before visit and an after visit calls
                # are done so that proper "notification" exists
                visit_method = node_method_map[mro_item]
                self.before_visit(*args[1:], **kwargs)
                visit_method(*args, **kwargs)
                self.after_visit(*args[1:], **kwargs)

                # returns the control flow to the caller method, note that no
                # value is returned as this is a simple visit operation
                return

            # in case no visit has been made a normal fallback operation is
            # performed by calling the "original" function/method
            return function(*args, **kwargs)

        return decorator_interceptor

    def decorator(function, *args, **kwargs):
        interceptor = create_interceptor(function)
        return interceptor

    return decorator
