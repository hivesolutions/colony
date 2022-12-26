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

import unittest

class Test(object):
    """
    The base and abstract test class from which all the
    colony test back end class will inherit from. It
    should contain the basic infra-structure for a rapid
    creation of tests to be executed in colony.
    """

    plugin = None
    """ The reference to the plugin that "owns" this
    test object, this may be used to reference the
    top level manager functions """

    def __init__(self, plugin):
        """
        Constructor of the class, received the "owner"
        plugin as the first argument to be stored for
        latter usage.

        :type plugin: Plugin
        :param plugin: The owner plugin for the test
        object to be created.
        """

        self.plugin = plugin

    def get_bundle(self):
        return ()

    def set_up(self, test_case):
        if hasattr(self.plugin, "system"): test_case.system = self.plugin.system

    def tear_down(self, test_case):
        pass

    def run_all(self, plugin = None, runner = None, verbosity = 1):
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()

        for test_case in self.get_bundle():
            test_case.plugin = plugin
            partial = loader.loadTestsFromTestCase(test_case)
            suite.addTest(partial)

        runner = runner or unittest.TextTestRunner(verbosity = verbosity)
        return runner.run(suite)
