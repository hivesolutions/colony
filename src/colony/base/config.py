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

import os
import sys
import json

from . import util

FILE_NAME = "colony.json"
""" The default name of the file that is going to be
used for the loading of configuration values from json """

CASTS = {
    bool : lambda v: v if type(v) == bool else v == "1",
    list : lambda v: v if type(v) == list else v.split(";"),
    tuple : lambda v: v if type(v) == tuple else tuple(v.split(";"))
}
""" The map containing the various cast method
operation associated with the various data types,
they provide a different type of casting strategy """

CONFIGS = {}
""" The map that contains the key value association
for all the currently set global configurations """

GLOBAL_CONFIG = {
    "logging_format" : "%(asctime)s [%(levelname)s] %(message)s",
    "plugin_id_logging" : True,
    "thread_id_logging" : True
}
""" The plugin manager configuration, this value is
used only as part of the inner (private) configuration
of the colony infra-structure and should only be changed
with complete knowledge of the inner workings of the system """

def conf(name, default = None, cast = None):
    """
    Retrieves the configuration value for the provided value
    defaulting to the provided default value in case no value
    is found for the provided name.

    An optional cast operation may be performed on the value
    in case it's requested.

    @type name: String
    @param name: The name of the configuration value to be
    retrieved.
    @type default: Object
    @param default: The default value to be retrieved in case
    no value was found for the provided name.
    @type cast: Type
    @param cast: The cast operation to be performed in the
    resolved value (optional).
    @rtype: Object
    @return: The value for the configuration with the requested
    name or the default value if no value was found.
    """

    cast = CASTS.get(cast, cast)
    value = CONFIGS.get(name, default)
    if cast and not value == None: value = cast(value)
    return value

def conf_prefix(prefix):
    configs = dict()
    for name, value in CONFIGS.items():
        if not name.startswith(prefix): continue
        configs[name] = value
    return configs

def conf_s(name, value):
    global CONFIGS
    CONFIGS[name] = value

def load(path = None):
    load_file(path = os.path.expanduser("~"))
    load_file(path = util.resolve_manager())
    load_file(path = sys.prefix)
    load_file(path = path)
    load_env()

def load_file(path = None, encoding = "utf-8"):
    if path: file_path = os.path.join(path, FILE_NAME)
    else: file_path = FILE_NAME

    exists = os.path.exists(file_path)
    if not exists: return

    file = open(file_path, "rb")
    try: data = file.read()
    finally: file.close()
    if not data: return

    data = data.decode(encoding)
    data_j = json.loads(data)
    for key, value in data_j.items():
        CONFIGS[key] = value

def load_env():
    for key, value in os.environ.items():
        CONFIGS[key] = value

load()
