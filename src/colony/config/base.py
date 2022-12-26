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

prefix_paths = {
    "default" : {
    }
}
""" The prefix path maps, contains a series of associated
values, should be used with care (mostly maintained for legacy reasons) """

plugin_path_list = [
    "plugins",
    "plugins/*plugin"
]
""" The list of plugin paths, these directories are going
to be searched for plugin files (via criteria) and the
plugins that exist there are going to be loaded """

library_path_list = [
    "libraries"
]
""" The list of library paths, these paths are going to
be exported to the global system path and may be used
independently of the execution location """

meta_path_list = [
    "meta",
    "meta/*config"
]
""" The list of meta paths, that should contain configuration
directory structures, the runtime loaded properties will
depend of these values """

logger_path = "log"
""" The path to the logger directory, this should be a path
relative to the current execution manager path, if this path
does not exists it may be created at runtime """

level = "WARNING"
""" The verbosity level that is going to be used as part of
the colony logging infra-structure, this value will affect all
of the currently attached loggers """

stop_on_cycle_error = False
""" If the plugin loading system should stop whenever an exception
is raised as part of the loading cycle (change with case) """

daemon_file_path = None
""" The path to the daemon (pid) file that is going to be used by
the executing colony instance, should only be used for detached processes"""
