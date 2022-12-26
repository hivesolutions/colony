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

import unittest

import xml.dom.minidom

from colony.base import legacy

class ColonyTestCase(unittest.TestCase):
    """
    The base class to be used for all the colony
    based test cases. It should contain a series
    of facilities aimed at simplifying the creation
    of unit tests under the colony infra-structure.
    """

    @staticmethod
    def get_test_case():
        return self

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "The base Colony Framework test case"

    def setUp(self):
        if not hasattr(self, "plugin"): return
        if not hasattr(self.plugin, "test"): return
        self.test = self.plugin.test
        self.test.set_up(self)

    def tearDown(self):
        if not hasattr(self, "plugin"): return
        if not hasattr(self.plugin, "test"): return
        self.test.tear_down(self)

    def assert_type(self, value, expected_type):
        """
        Tests that the provided value is of the specified type.

        :type value: Object
        :param value: The value whose type will be compared
        against the expected type.
        :type expected_type: Type
        :param expected_type: The type that is expected for
        the provided value.
        """

        # retrieves the value's type and in case the type is
        # the expected on returns immediately as no  problem
        # exists for the current assertion call
        value_type = type(value)
        if value_type == expected_type: return

        # raises a failure exception as the type of the value
        # is not the one expected by the assert operation
        raise self.failureException(
            "value is of type %s instead of expected type %s" %
            (value_type, expected_type)
        )

    def assert_raises(self, expected_exception, function, *args, **kwargs):
        """
        Tests that the specified exception is raised when invoking
        the provided function with the respective arguments.

        The expected exception parameter may contain the type of the
        expected exception or the name of it.

        :type expected_exception: Exception/String
        :param expected_exception: The type or name of the exception
        that should be raised by the function.
        :type function: Function
        :param function: The function to be invoked.
        """

        try:
            # invokes the function that should trigger the evaluation process,
            # note that the execution is dynamic with the provided arguments
            function(*args, **kwargs)
        except BaseException as exception:
            # checks if the current exception assert mode is string or value
            # oriented and then uses the string mode flag to find out the correct
            # expected exception name (for exception string description)
            string_mode = True if type(expected_exception) in legacy.STRINGS else False
            expected_exception_name = expected_exception if string_mode else expected_exception.__name__

            # retrieves the exception class and then uses it
            # to retrieve the exception name
            exception_class = exception.__class__
            exception_name = exception_class.__name__

            # re-raises the proper exception in case the raised exception was
            # not the expected one (so that the test may fail correctly) using
            # the string based comparison as it's currently set
            if string_mode and not exception_name == expected_exception_name: raise

            # re-raises the proper exception in case the raised exception was
            # not the expected one (so that the test may fail correctly) uses
            # the class type verification as no string mode is enabled
            if not string_mode and not exception_class == expected_exception: raise
        else:
            # raises a failure exception in case no exception was raised, this is
            # the expected behavior as an exception was expected in situation
            raise self.failureException("%s exception was not raised" % expected_exception)

    def assert_valid_xml(self, xml_data):
        """
        Tests that the provided XML data is valid.

        :type xml_data: String
        :param xml_data: The string with the XML data.
        """

        # attempts to parse the XML data
        # to check if its valid
        try:
            # parses the XML data
            xml.dom.minidom.parseString(xml_data)
        except Exception:
            # raises a failure exception
            # in case the parse was unsuccessful
            raise self.failureException("XML data is invalid")
