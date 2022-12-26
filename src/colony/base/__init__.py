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

from . import config
from . import decorators
from . import exceptions
from . import information
from . import legacy
from . import loggers
from . import system
from . import test
from . import util

from .config import conf, conf_prefix, conf_suffix, conf_s, conf_r, conf_d, conf_ctx
from .decorators import load_plugin, plugin_meta_information, load_allowed, load_allowed_capability,\
    unload_allowed, unload_allowed_capability, inject_dependencies, plugin_inject, event_handler,\
    event_handler_method, set_configuration_property, set_configuration_property_method,\
    unset_configuration_property, unset_configuration_property_method, plugin_call, create_load_plugin_interceptor
from .exceptions import ColonyException, OperationalError, AssertionError, PluginSystemException,\
    PluginClassNotAvailable, InvalidCommand, InvalidArgument, SecurityError, OperationNotComplete, OperationRestart
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
