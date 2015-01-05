#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

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

        @type plugin: Plugin
        @param plugin: The owner plugin for the test
        object to be created.
        """

        self.plugin = plugin

    def get_bundle(self):
        return ()

    def set_up(self, test_case):
        if hasattr(self.plugin, "system"): test_case.system = self.plugin.system

    def tear_down(self, test_case):
        pass
