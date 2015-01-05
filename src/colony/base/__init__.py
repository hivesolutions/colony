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

from . import config
from . import decorators
from . import exceptions
from . import information
from . import legacy
from . import loggers
from . import system
from . import test
from . import util

from .config import conf, conf_prefix, conf_s
from .decorators import load_plugin, plugin_meta_information, load_allowed, load_allowed_capability,\
    unload_allowed, unload_allowed_capability, inject_dependencies, plugin_inject, event_handler,\
    event_handler_method, set_configuration_property, set_configuration_property_method,\
    unset_configuration_property, unset_configuration_property_method, plugin_call, create_load_plugin_interceptor
from .exceptions import ColonyException, PluginSystemException, PluginClassNotAvailable, InvalidCommand,\
    InvalidArgument, OperationNotComplete
from .information import VERSION, RELEASE, BUILD, RELEASE_DATE, RELEASE_DATE_TIME, ENVIRONMENT_VERSION,\
    ENVIRONMENT, DEFAULT_ENCODING, DATE_FORMAT, DATE_TIME_FORMAT, INFORMATION_PATH
from .loggers import BroadcastHandler, MemoryHandler
from .system import System, Plugin, PluginManagerPlugin, PluginManager, Dependency, PluginDependency,\
    PackageDependency, Condition, OperativeSystemCondition, Capability, Event, PluginThread,\
    PluginEventThread
from .test import Test
from .util import CPYTHON_ENVIRONMENT, JYTHON_ENVIRONMENT, IRON_PYTHON_ENVIRONMENT, WINDOWS_OS, MAC_OS,\
    UNIX_OS, OTHER_OS, UID_PRECISION, WaitInput, QueueEvent, Plugins, module_import, resolve_manager,\
    ensure_tree, is_master, get_environment, get_operative_system, get_timestamp_uid
