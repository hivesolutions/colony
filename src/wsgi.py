#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import glob

base_path = os.path.dirname(__file__)
if not base_path in sys.path: sys.path.insert(0, base_path)

import colony.base.system

############## REFACTOR #####################

plugin_paths = glob.glob(os.path.join(base_path, "../../*/src"))
plugin_paths += glob.glob(os.path.join(base_path, "../../*/*/src"))
plugin_paths = [os.path.abspath(plugin_path) for plugin_path in plugin_paths]

meta_paths = glob.glob(os.path.join(base_path, "../../*config/*"))
meta_paths = [os.path.abspath(meta_path) for meta_path in meta_paths]

############## REFACTOR #####################

# creates the plugin manager instance with the current file path
# as the manager path and the corresponding relative log path,
# then provides the plugin and meta paths and unsets the global
# loop strategy (avoids blocking the process)
plugin_manager = colony.base.system.PluginManager(
    manager_path = base_path,
    logger_path = os.path.join(base_path, "log"),
    plugin_paths = plugin_paths,
    meta_paths = meta_paths,
    loop = False,
    run_mode = "development"
)
return_code = plugin_manager.load_system()

def application(environ, start_response):
    # retrieves the wsgi plugin and uses it to handle
    # the wsgi request (request redirection) any inner
    # exception should be handled and an error http
    # message should be returned to the end user
    wsgi_plugin = plugin_manager.get_plugin_by_id("pt.hive.colony.plugins.wsgi")
    return wsgi_plugin.handle(environ, start_response)

if __name__ == "__main__":
    import wsgiref.simple_server
    httpd = wsgiref.simple_server.make_server("", 8000, application)
    httpd.serve_forever()
