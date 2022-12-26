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

__date__ = "$LastChangedDate: 2011-01-15 17:29:58 +0000 (sÃ¡b, 15 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2022 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

PUBLIC_VALUE = "__public__"
""" The public value """

def public(function):
    """
    Decorator used to assign the public attribute to methods.

    :type function: Function
    :param function: The function to sets the public visibility.
    :rtype: Function
    :return: The sent function (returned as a normal decorator).
    """

    # sets the (decorated) function as public and then returns
    # the function to the caller (default decorator behavior)
    function.__public__ = True
    return function

class Protected(object):
    """
    Base class of all classes that want to hide protected
    attributes from public access.
    This class should be carefully used as it may
    create unexpected side effects.
    """

    def __new__(cls, *args, **kwargs):
        # creates a new object reference, note that
        # the object is created without arguments,
        # avoiding possible runtime errors
        object_reference = object.__new__(cls)

        # initializes the class reference with the new
        # object reference and the arguments
        cls.__init__(object_reference, *args, **kwargs)

        def __getattr__(self, name):
            # retrieves the attribute from the object reference
            attribute = getattr(object_reference, name)

            # in case the attribute is public
            if hasattr(attribute, PUBLIC_VALUE):
                # returns the attribute (valid)
                return attribute
            # in case the class is public
            elif hasattr(cls, PUBLIC_VALUE):
                # in case the name is in the public
                # attributes list
                if name in cls.__public__:
                    # returns the attribute (valid)
                    return attribute

            # raises the attribute error, meaning that the attribute
            # exits but it's not exposed as a public attribute
            raise AttributeError(
                "attribute '%s' of class '%s' is not public" %\
                (name, cls.__name__)
            )

        def __setattr__(self, name, value):
            cls.__setattr__(self, name, value)

        def is_own_magic(cls, name, without = []):
            """
            Checks if the given name is a magic attribute
            in the class.

            :type name: String
            :param name: The name to be tested for "magic".
            :type without: List
            :param without: The list of attributes to exclude magic.
            :rtype: bool
            :return: The result of the "magic" test.
            """

            # in case the name is magic and is not in the without list
            return not name in without and name.startswith("__") and name.endswith("__")

        # creates a new proxy instance with the protected name
        Proxy = type("Protected(%s)" % cls.__name__, (), {})

        # retrieves the class names
        class_names = dir(cls)

        # retrieves the proxy names
        proxy_names = dir(Proxy)

        # iterates over all the class names
        for class_name in class_names:
            # tests to check if the name is magic
            if not is_own_magic(cls, class_name, proxy_names):
                # continues the loop
                continue

            try:
                # retrieves the attribute
                attribute = getattr(object_reference, class_name)

                # sets the attribute in the proxy
                setattr(Proxy, class_name, attribute)
            except TypeError:
                pass

        # sets the new retrieve attribute and
        # set attribute references
        Proxy.__getattr__ = __getattr__
        Proxy.__setattr__ = __setattr__

        # creates a new proxy instance
        proxy_instance = Proxy()

        # sets the proxy instance in the object reference
        object_reference._proxy_instance = proxy_instance

        # returns the proxy instance
        return proxy_instance
