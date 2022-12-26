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
import time

from . import legacy

CPYTHON_ENVIRONMENT = "cpython"
""" CPython environment value """

JYTHON_ENVIRONMENT = "jython"
""" Jython environment value """

IRON_PYTHON_ENVIRONMENT = "iron_python"
""" IronPython environment value """

WINDOWS_OS = "windows"
""" The windows os value """

MAC_OS = "mac"
""" The mac os value """

UNIX_OS = "unix"
""" The unix os value """

OTHER_OS = "other"
""" The other os value """

UID_PRECISION = 8
""" Unique id precision """

class WaitInput(object):
    """
    Wait input file used to overcome the problem
    with being stuck in the console input.
    This file like object reads something as a virtual
    timeout object avoid the proper read and unblocking
    the current in/out operation.
    """

    def readline(self):
        """
        Reads a "line" from the wait input.
        This is an empty read as all it does
        is wait for a while and then return.
        """

        # sleeps for a little bit
        time.sleep(1.0)

        # returns an empty (wait string)
        return ""

class QueueEvent(object):
    """
    The class that describes an event to be
    used in a generic event queue.
    """

    event_name = None
    """ The name of the event """

    event_args = []
    """ The arguments of the event """

    def __init__(self, event_name, event_args = []):
        """
        Constructor of the class.

        :type event_name: String
        :param event_name: The name of the event.
        :type event_args: List
        :param event_args: The arguments of the event.
        """

        self.event_name = event_name
        self.event_args = event_args

class Plugins(object):
    """
    Class used as storage for the various plugin
    instance references indexed by their name.
    """

    pass

def module_import(module_name):
    """
    Imports the module with the given name, this import
    operation is recursive meaning that inner packages
    are also going to be imported.

    :type module_name: String
    :param module_name: The name of the module to be imported,
    this value may contain multiple "sub" packages.
    :rtype: module
    :return: The imported module as a variable reference.
    """

    module = __import__(module_name)
    components = module_name.split(".")
    for component in components[1:]:
        module = getattr(module, component)
    return module

def resolve_manager(exec_path = None):
    """
    Master resolver for the manager path, it's responsible
    for the decision to use the current and possible master
    directory structure or the personal (home directory based)
    strategy that is used as fallback.

    Note that the master structure should only be used for
    development purposes.

    :type exec_path: String
    :param exec_path: The currently executing path, should be
    retrieved from the first file to be executed in the call
    stack, this is the path to be inspected for master.
    :rtype: String
    :return: The final "resolved" manager path after the proper
    validation operations have been done.
    """

    is_venv = hasattr(sys, "real_prefix")
    personal_path = sys.prefix if is_venv else os.path.expanduser("~")
    personal_path = os.path.join(personal_path, ".colony")
    master_path = os.environ.get("COLONY_HOME", exec_path)
    manager_path = master_path if is_master(master_path) else personal_path
    manager_path = os.path.abspath(manager_path)
    manager_path = os.path.normpath(manager_path)
    return manager_path

def ensure_tree(path):
    """
    Ensures that the proper colony plugin system directory
    structure is created under the provided path.

    Note that the top level directory will be created in case
    it does not exists, the permissions used for such operation
    will be the default ones (may be not secure enough).

    :type path: String
    :param path: The file path of the root plugin system directory
    for which the structure is going to be created.
    """

    is_personal = not is_master(path)
    config_path = os.path.join(path, "config")
    containers_path = os.path.join(path, "containers")
    deploy_path = os.path.join(path, "deploy")
    libraries_path = os.path.join(path, "libraries")
    log_path = os.path.join(path, "log")
    meta_path = os.path.join(path, "meta")
    plugins_path = os.path.join(path, "plugins")
    scripts_path = os.path.join(path, "scripts")
    tmp_path = os.path.join(path, "tmp")
    var_path = os.path.join(path, "var")
    env_path = os.path.join(path, "colony.json")
    if not os.path.exists(path): os.makedirs(path)
    if not os.path.exists(config_path): os.makedirs(config_path)
    if not os.path.exists(containers_path): os.makedirs(containers_path)
    if not os.path.exists(deploy_path): os.makedirs(deploy_path)
    if not os.path.exists(libraries_path): os.makedirs(libraries_path)
    if not os.path.exists(log_path): os.makedirs(log_path)
    if not os.path.exists(meta_path): os.makedirs(meta_path)
    if not os.path.exists(plugins_path): os.makedirs(plugins_path)
    if not os.path.exists(scripts_path): os.makedirs(scripts_path)
    if not os.path.exists(tmp_path): os.makedirs(tmp_path)
    if not os.path.exists(var_path): os.makedirs(var_path)
    if not os.path.exists(env_path) and is_personal: open(env_path, "a").close()

def is_master(path):
    """
    Verifies if the provided file path is considered to be the
    root path of a colony master directory structure. A colony
    master directory structure is considered to be a directory
    structure where the colony package system and the other
    directories mix together (typically used for development).

    This structure is the opposite of the personal strategy where
    the colony instance is stored separated to the logic of colony
    typically used for production environments.

    :type path: String
    :param path: The file path that is going to be verified to
    be part of a colony master directory structure.
    :rtype: bool
    :return: If the provided path is considered to be a normalized
    master directory structure for colony.
    """

    if path == None: return False
    package_path = os.path.join(path, "colony")
    plugins_path = os.path.join(path, "plugins")
    return os.path.isdir(package_path) and os.path.isdir(plugins_path)

def get_environment():
    """
    Retrieves the current python environment, there
    should be multiple environments depending on the
    kind of python interpreter being used.

    :rtype: String
    :return: The type of the current python environment,
    taking into account the current interpreter information.
    """

    platform = sys.platform
    if not platform.find("java") == -1: return JYTHON_ENVIRONMENT
    elif not platform.find("cli") == -1: return IRON_PYTHON_ENVIRONMENT
    else: return CPYTHON_ENVIRONMENT

def get_operative_system():
    """
    Retrieves the current operative system, this is a
    normalized operation that uses the underlying python
    infra-structure and normalizes the result.

    :rtype: String
    :return: The type of the current operative system.
    """

    os_name = os.name
    if os_name == "nt" or os_name == "dos": return WINDOWS_OS
    elif os_name == "mac": return MAC_OS
    elif os_name == "posix": return UNIX_OS
    return OTHER_OS

def get_timestamp_uid():
    """
    Retrieves a unique id based in the current timestamp.
    This value should not be used for high accuracy or
    cryptographic operations as it's not very unique and
    it is not entropy safe.

    :rtype: String
    :return: A unique id based in the current timestamp.
    """

    timestamp = time.time()
    float_value = timestamp * (10 ** UID_PRECISION)
    integer_value = legacy.LONG(float_value)
    string_value = str(integer_value)
    return string_value
