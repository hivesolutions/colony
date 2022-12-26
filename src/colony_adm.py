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

import re
import os
import sys
import glob
import shutil
import zipfile
import tempfile

import colony

INDENT = 0
""" The global reference to the indentation level that
is going to be printed at the start of each output
operation, this value should be used carefully to avoid
any thread related problems (not thread safe) """

DEFAULT_TARGET = "colony"
""" The default directory to be used as target in
case no target path is provided (default name) """

DEFAULT_ROOT = "COLONY_ROOT"
""" The default name for the file to be used to
indicate the root directory of a colony instance """

PACK_FILE = "colony.zip"
""" The name of the file that will be the packing
reference of the instance """

EXTENSIONS = dict(
    bundle = ".cbx",
    plugin = ".cpx",
    config = ".ccx"
)
""" The map associating the various types of
colony packages with the associated extension """

REMOVALS = (
    "colony.egg-info",
    "EGG-INFO"
)
""" The list of paths to be removed because there's
no use for them in the target colony instance """

REPO_URL = "https://colony.bemisc.com/"
""" The basic default open repository for colony packages
this is always going to be used together with the current
user wide configuration values """

STAGE_URL = "https://colony.stage.hive.pt/"
""" The test URL version of the colony repository, used
for the downloading of staging ready only packages """

def resolve_manager(path, ensure = True):
    manager_path = colony.resolve_manager(path)
    if ensure: colony.ensure_tree(manager_path)
    return manager_path

def output(message, flush = True):
    print((" " * INDENT) + message)
    if flush: sys.stdout.flush()

def indent():
    global INDENT
    INDENT += 1

def unindent():
    global INDENT
    INDENT -= 1

def help():
    output("CPM - package management for Colony Framework")
    print("")
    print("  cpm clone <target>           Clones the base colony instance into the target directory (new project)")
    print("  cpm cleanup <target>         Cleans the current instance removing extra files")
    print("  cpm pack <target>            Packs the current instance into a .zip file")
    print("  cpm generate [target] <...>  Generates a .json descriptor file for the provided python "\
        "file and then runs the build operation for the generated .json file, effectively build the package item"
    )
    print("  cpm build [descriptor] <...> Builds the target .json descriptor file into a package file")
    print("  cpm deploy [package]         Deploys the target .cbx ile into the current instance")
    print("  cpm info [package]           Prints information about the package to the standard output")
    print("  cpm install [name] <...>     Installs the package with the provided name from the remote repositories")
    print("  cpm upgrade                  Updates the complete set of packages deployed in the instance")
    print("  cpm require [path] <...>     Installs the complete set of packages defined in the requirements file")
    print("  cpm upload [target] <repo>   Generates a package for the provided path and then uploads it "\
        "to the currently configured primary repository, or another repository if defined"
    )

def version():
    output("CPM - package management for Colony Framework")

def env():
    # retrieves the current working directory (cwd)
    # in order to be used in as fallback case
    cwd = os.getcwd()

    # retrieves the complete set of information that is
    # going to be printed as part of the info printing
    manager_path = resolve_manager(cwd)

    # prints the complete set of information to the user
    # so that it may take some decisions on the interaction
    output("manager_path := %s" % manager_path)

def clone():
    # in case there are enough arguments for the
    # deduction of the target path uses the provided
    # parameters otherwise used the default name
    # for the target path
    if len(sys.argv) > 2: target = sys.argv[2]
    else: target = DEFAULT_TARGET

    # retrieves the complete (and normalized) colony
    # path and then uses it to create the new instance
    # (cloned from the current instance)
    colony_path = os.path.normpath(os.path.dirname(__file__))
    shutil.copytree(colony_path, target)

    # iterates over all the paths to be removed from
    # the newly creates instance (not required anymore)
    for path in REMOVALS:
        # joins the path for the removal with the target
        # path and then in case it exists removes it
        _path = os.path.join(target, path)
        if not os.path.exists(_path): continue
        shutil.rmtree(_path)

    # runs the cleanup process on the target path
    # so that unnecessary files are removed
    _cleanup(target)

    # opens the colony instance reference file (this
    # file indicates the root of the colony instance)
    root_file_path = os.path.join(target, DEFAULT_ROOT)
    try: root_file = open(root_file_path, "a")
    finally: root_file.close()

def cleanup():
    """
    Cleans the target colony instance removing all the
    non mandatory files from the various internal directories.

    The removed files include python compiled files, extra
    directories, etc.

    The strategy used is conservative so whenever in doubt
    the process will not remove the file.
    """

    # retrieves the current working directory (cwd)
    # in order to be used in as fallback case
    cwd = os.getcwd()

    # in case there are enough arguments for the
    # deduction of the target path uses the provided
    # parameters otherwise used the default name
    # for the target path
    if len(sys.argv) > 2: target = sys.argv[2]
    else: target = resolve_manager(cwd)

    # in case not target was expanded the current directory
    # is used (assumes) the administration file is stored
    # at the same location as the colony instance
    target = target or os.path.normpath(os.path.dirname(__file__))

    # in case not target path is defined must raise
    # a runtime error
    if not target: raise RuntimeError("No instance found")

    # runs the cleanup command on the target path
    # so that all the non required files are removed
    _cleanup(target)

def pack():
    # retrieves the current working directory (cwd)
    # in order to be used in as fallback case
    cwd = os.getcwd()

    # in case there are enough arguments for the
    # deduction of the target path uses the provided
    # parameters otherwise used the default name
    # for the target path
    if len(sys.argv) > 2: target = sys.argv[2]
    else: target = resolve_manager(cwd)

    # in case not target was expanded the current directory
    # is used (assumes) the administration file is stored
    # at the same location as the colony instance
    target = target or os.path.normpath(os.path.dirname(__file__))

    # in case not target path is defined must raise
    # a runtime error, because it's not possible to proceed
    if not target: raise RuntimeError("No instance found")

    # runs the pack command on the target path
    # to create the packed file for the colony instance
    _pack(target)

def generate():
    # in case there're not enough arguments to be
    # able to retrieve the specification file raises
    # a runtime error
    if len(sys.argv) < 3: raise RuntimeError("No plugin file provided")

    # retrieves the target plugin file paths and uses them
    # for the generation of the descriptor file that should
    # represent the same plugin in terms of meat information
    targets = sys.argv[2:]
    for target in targets: _generate(target)

def build():
    # in case there're not enough arguments to be
    # able to retrieve the specification file raises
    # a runtime error
    if len(sys.argv) < 3: raise RuntimeError("No descriptor provided")

    # retrieves the descriptor file from the arguments and
    # uses it to run the build structure
    descriptors = sys.argv[2:]
    for descriptor in descriptors: _build(descriptor)

def deploy():
    # in case there're not enough arguments to be
    # able to retrieve the specification file raises
    # a runtime error, the name of the file is required
    if len(sys.argv) < 3: raise RuntimeError("No package provided")

    # retrieves the package files from the arguments and
    # uses them to run the deploy the packages into the currently
    # defined global instance (default colony instance)
    packages = sys.argv[2:]
    for package in packages: _deploy(package)

def install():
    # in case there're not enough arguments to be
    # able to retrieve the package file for install
    if len(sys.argv) < 3: raise RuntimeError("No name of package provided")

    # runs the install operation using the provided names
    # as reference, note that these names may contain an
    # optional version value attached to them
    names = sys.argv[2:]
    for name in names: _install(name)

def require():
    # in case there're not enough arguments to be
    # able to retrieve the requirements file
    if len(sys.argv) < 3: raise RuntimeError("No requirements file provided")

    # runs the requirements operation with the provided
    # paths, this is a recursive operation and may take
    # a while to reach the complete and final state
    paths = sys.argv[2:]
    for path in paths: _require(path)

def upgrade():
    _upgrade()

def upload():
    # in case there're not enough arguments to be
    # able to retrieve the specification file raises
    # a runtime error, the name of the file is required
    if len(sys.argv) < 3: raise RuntimeError("No plugin file provided")

    # in case there's an extra argument provided it's assumed
    # that it's the name of the target repo
    if len(sys.argv) > 3: repo = sys.argv[3]
    else: repo = "colony"

    # runs the upload operation for the target path, this
    # should be a base file to be packed and then uploaded
    # to the currently defined repository
    target = sys.argv[2]
    _upload(target, repo = repo)

def info():
    # in case there're not enough arguments to be
    # able to retrieve the specification file raises
    # a runtime error, the name of the file is required
    if len(sys.argv) < 3: raise RuntimeError("No package provided")

    # retrieves the package file from the arguments and
    # uses it to runs the information command to be able
    # to print some information about the package
    package = sys.argv[2]
    _info(package)

def _cleanup(path, empty_extra = True):
    # retrieves the path to the series of sub
    # directories to be "cleaned"
    log_path = os.path.join(path, "log")
    meta_path = os.path.join(path, "meta")

    # removes the files using extension based rules
    # on the defined directories, this should normalize
    # the directory structure and avoid problems
    _cleanup_files(path, re.compile(".*\.pyc$"))
    _cleanup_files(log_path, re.compile(".*\.log$"))
    _cleanup_files(log_path, re.compile(".*\.log.[0-9]+$"))
    _cleanup_files(log_path, re.compile(".*\.err$"))
    _cleanup_files(log_path, re.compile(".*\.err.[0-9]+$"))
    empty_extra and _cleanup_directories(meta_path, re.compile(""))

def _cleanup_directories(path, extension):
    # verifies that the provided path exists and is
    # a valid directory, in case it does not returns
    # immediately to avoid any problem
    if not os.path.isdir(path): return

    # lists all the entries in the provided path
    # in order to filter the ones to be removed
    entries = os.listdir(path)

    # iterates over all the entries to check the ones
    # that correspond to directories and run the cleanup
    # on each of their files
    for entry in entries:
        _path = os.path.join(path, entry)
        if not os.path.isdir(_path): continue
        _cleanup_files(_path, extension)

def _cleanup_files(path, extension):
    # verifies that the provided path exists and is
    # a valid directory, in case it does not returns
    # immediately to avoid any problem
    if not os.path.isdir(path): return

    # lists all the entries in the provided path
    # in order to filter the ones to be removed
    entries = os.listdir(path)

    # iterates over all the entries to treat them
    # in case it's necessary
    for entry in entries:
        # joins the path with the entry to create
        # the complete entry path, then runs the
        # appropriate iteration loop operations
        _path = os.path.join(path, entry)
        if os.path.isdir(_path): _cleanup_files(_path, extension); continue
        if extension.match(_path): os.remove(_path)

    # verifies that the (directory) path exists otherwise
    # returns immediately then lists the directory to check
    # if there are still files contained in it and in case
    # there is returns immediately, then proceeds with the
    # directory removal for the current path
    if not os.path.exists(path): return
    if os.listdir(path): return
    os.rmdir(path)

def _pack(path):
    # runs the cleanup process for the provided path
    # in order to prepare the current structure for
    # the packing of the files
    _cleanup(path)

    # joins the current path with the top level reference
    # path and then joins the pack file name to it
    _path = os.path.join(path, "..")
    archive_path = os.path.join(_path, PACK_FILE)
    archive_path = os.path.normpath(archive_path)

    # opens the archive path as a zip file for writing and
    # then writes the current "instance" directory into the zip
    file = zipfile.ZipFile(
        archive_path,
        mode = "w",
        compression = zipfile.ZIP_DEFLATED,
        allowZip64 = True
    )
    try: _zip_directory(path, "/", file)
    finally: file.close()

    # prints a message about the packing operation that has just
    # been performed on the current running colony instance
    output("Packed %s into %s" % (path, archive_path))

def _generate(path, build = True, delete = True):
    # normalizes the path so that the value that is going to be
    # used from no on is going to be the correct one according
    # to the current operative system specifications
    path = os.path.abspath(path)
    path = os.path.normpath(path)

    # verifies the type of generation that is going to be performed, taking into
    # account some of the characteristics of the provided path
    is_plugin = path.endswith(".py")
    is_config = os.path.isdir(path) and ".project" in os.listdir(path)

    # verifies the type of generation that is meant to be performed and runs it,
    # in case no valid type is found for the provided path an exception is raised
    # indicating the problem (as expected by the current specification)
    if is_plugin: descriptor_path = _generate_plugin(path)
    elif is_config: descriptor_path = _generate_config(path)
    else: raise RuntimeError("Invalid path provided for generation")

    # sets the default result value (nothing is returned by default) so the value is
    # not defined (unset/invalid value)
    result = None

    # in case the build flag is active the generated descriptor file is used to build
    # a new package file for the currently associated package
    if build: result = _build(descriptor_path)

    # in the descriptor is meant to be delete (not going to be used anymore) the proper
    # file must be removed from the current file system
    if delete: os.remove(descriptor_path)

    # returns the final result value that may be undefined in case no sub operations
    # have been called for the current master operation
    return result

def _generate_plugin(path, use_path = True):
    # imports the JSON module so that it's possible
    # to generate the colony descriptor file
    import json

    # retrieves the base name of the provided path so that it
    # may be "safely" used for some of the situations
    base = os.path.basename(path)
    base_dir = os.path.dirname(path)

    # prints a debug information message about the generation
    # of descriptor process that is going to be started
    output("Generating plugin descriptor for %s" % base)

    # starts some of the temporary variables that are going to be
    # used as part of the plugin structure finding process
    plugin = None
    variables = dict()

    # executes the main plugin python file so that it's possible
    # to retrieve the plugin structure and process it, at the end
    # of the "finding iteration" the plugin should have been found
    colony.legacy.execfile(path, variables)
    for name, value in variables.items():
        if not name.endswith("Plugin"): continue
        plugin = value

    # in case no plugin structure has been found an exception is raised
    # indicating that no plugin has been found (problem situation)
    if not plugin: raise RuntimeError("No plugin found")

    # in case the (file) path mode is enabled uses the name of the file
    # where the plugin class is defined to name the plugin, this is considered
    # to be the "safest" approach as it allows more flexibility in plugin name
    if use_path:
        short_name = os.path.splitext(os.path.basename(path))[0][:-7]

    # uses the typical approach to the generation of the plugin short name
    # this strategy is defined as the standard one and should be respected
    # by any plugin considered to be compliant with colony
    else:
        short_name = colony.to_underscore(plugin.__name__)[:-7]

    # initializes the loop that is going to discover the type of directory
    # structure for the current plugin (either inexistent, direct or indirect)
    mode = "indirect"
    target = None
    names = os.listdir(base_dir)
    for name in names:
        current = os.path.join(base_dir, name)
        if not os.path.isdir(current): continue
        if name in (short_name, short_name + "_c"): mode = "direct"; break
        else: target = name

    # runs the proper resources gathering strategy taking into account the type
    # of plugin directory structure that has just been found in the previous step
    if mode == "direct": resources = _gather_direct(short_name, base_dir, name)
    elif mode == "indirect": resources = _gather_indirect(short_name, base_dir, target)
    else: resources = _gather_invalid(short_name, base_dir, name)

    # prepends the current plugin file to the list of resource, this is considered
    # to be the main resource to be included in the package
    resources.insert(0, base)

    # filters the resources that have been gathered so that only the ones that
    # matter are defined in the structure and then creates the sequence of dependency
    # maps that are going to be defining the dependencies of the plugin
    resources = _fitler_resources(resources)
    dependencies = [dependency.get_map() for dependency in plugin.dependencies]

    # creates the "final" plugin definition structure with the complete set of
    # attributes of the plugin and then dumps the structure using the JSON serializer
    # as this is the default serialization model of the descriptor files
    structure = dict(
        type = "plugin",
        platform = "python",
        sub_platforms = plugin.platforms,
        id = plugin.id,
        name = plugin.name,
        short_name = short_name,
        description = plugin.description,
        version = plugin.version,
        author = plugin.author,
        capabilities = plugin.capabilities,
        capabilities_allowed = plugin.capabilities_allowed,
        dependencies = dependencies,
        resources = resources
    )
    structure_s = json.dumps(structure)

    # verifies if the data type of the provided structure string
    # is unicode based if that's the case encodes the structure
    # using the default encoding associated with JSON
    if colony.legacy.is_unicode(structure_s):
        structure_s = structure_s.encode("utf-8")

    # creates the final path of the descriptor file and writes the serialized contents
    # into the file closing it for writing at the end, note that the target file is
    # defined by convention from the plugin's short name
    descriptor_path = os.path.join(base_dir, short_name + "_plugin.json")
    descriptor_file = open(descriptor_path, "wb")
    try: descriptor_file.write(structure_s)
    finally: descriptor_file.close()

    # prints a debug message about the descriptor file that has just been generated
    # so that the user is notified about the generated file
    output("Generated plugin descriptor into %s" % descriptor_path)

    # returns the generated descriptor path to the caller method so that it may be
    # used latter for any reference operation as expected
    return descriptor_path

def _generate_config(path):
    import json

    base = os.path.basename(path)
    base_dir = os.path.dirname(path)
    parent = os.path.basename(base_dir)
    name = parent + "_" + base

    description = "Configuration package (%s)" % name
    version = "0.0.0"
    author = "John Doe <john@doe.com>"

    output("Generating config descriptor for %s" % name)

    resources = _gather_config(path)
    resources = _fitler_resources(resources)

    structure = dict(
        type = "config",
        id = name,
        name = name,
        short_name = name,
        description = description,
        version = version,
        author = author,
        resources = resources
    )
    structure_s = json.dumps(structure)

    if colony.legacy.is_unicode(structure_s):
        structure_s = structure_s.encode("utf-8")

    descriptor_path = os.path.join(path, name + "_config.json")
    descriptor_file = open(descriptor_path, "wb")
    try: descriptor_file.write(structure_s)
    finally: descriptor_file.close()

    output("Generated config descriptor into %s" % descriptor_path)

    return descriptor_path

def _build(path, short_name = True):
    # imports the JSON module so that it's possible
    # to parse the colony descriptor file
    import json

    # opens the descriptor file to be read in the binary
    # format and loads its JSON contents to be used
    file = open(path, "rb")
    try: data = file.read()
    finally: file.close()

    # decodes the "raw" data using the default JSON encoding
    # and then runs the proper JSON decoding/loading
    data = data.decode("utf-8")
    descriptor = json.loads(data)

    # retrieves the various attributes from the descriptor
    # file and uses them to infer in some properties
    type = descriptor["type"]
    id = descriptor["id"]
    resources = descriptor.get("resources", [])
    extension = EXTENSIONS.get(type, ".cpx")

    # verifies if the proper type of the current package and then
    # sets the appropriate flags taking that into account
    is_plugin = type == "plugin"
    is_config = type == "config"

    # retrieves the base name for the file and removes the
    # extension from it so that the short name for it is
    # correctly retrieved taking into account the package type
    base_name = os.path.basename(path)
    if is_plugin: base_name = colony.to_underscore(base_name)[:-12]
    elif is_config: base_name = colony.to_underscore(base_name)[:-12]
    else: base_name = colony.to_underscore(base_name)[:-5]

    # retrieves the resources directory for the resources
    # from the base directory of the JSON descriptor and
    # then creates the name of the file from the id
    resources_directory = os.path.dirname(path)
    name = base_name + extension if short_name else id + extension

    # opens the target zip file to be used in write
    # mode (it's going to receive the data)
    file = zipfile.ZipFile(
        name,
        mode = "w",
        compression = zipfile.ZIP_DEFLATED,
        allowZip64 = True
    )

    try:
        # iterates over all the resources to be written
        # in the packing file to zip them
        for resource in resources:
            # creates the full path to the resource from the
            # resources directory and the re-calculates the
            # the resources path with a prefix and writes
            # the resource into the target file
            _resource = os.path.join(resources_directory, resource)
            _relative = "resources/" + resource
            file.write(_resource, _relative)

        # writes the specification file into the packing file
        # to be used as meta data information
        file.write(path, "spec.json")
    finally:
        # closes the file to avoid any leak of file
        # descriptors and to flush the pending data
        file.close()

    # returns the generated package name to the caller method
    # as this is the resulting object for the operation
    return name

def _deploy(path, timestamp = None):
    import json

    # retrieves the currently working directory as this is going
    # to be used for some of the path resolution processes
    cwd = os.getcwd()

    # creates a new temporary directory path where the contents of
    # the package file are going to be extracted
    temp_path = tempfile.mkdtemp()

    # reads the package (zip file) and then extracts the complete
    # set of it's contents into the temporary directory so that they
    # may be manipulated and then properly used
    file = zipfile.ZipFile(path, mode = "r")
    try: file.extractall(temp_path)
    finally: file.close()

    # retrieves the path of the specification file and reads it's JSON
    # contents so that it's possible to retrieve more information about
    # the package that is currently being deployed
    spec_path = os.path.join(temp_path, "spec.json")
    file = open(spec_path, "rb")
    try: data = file.read()
    finally: file.close()
    os.remove(spec_path)

    # decodes the "raw" data using the default JSON encoding
    # and then runs the proper JSON decoding/loading
    data = data.decode("utf-8")
    descriptor = json.loads(data)

    # attaches the timestamp to the descriptor map in case it's been defined
    # by the passing arguments, this is required for compliance
    descriptor["timestamp"] = timestamp

    # retrieves the proper type from the descriptor and uses it to calculate
    # both the target value and the suffix that are going to be used in the
    # deployment operation to be performed (as expected)
    type = descriptor.get("type", "plugin")
    if type == "plugin": target = "plugins"; suffix = "_plugin"
    elif type == "config": target = "meta"; suffix = "_config"
    else: RuntimeError("invalid package type")

    # resolves the associated manager path and then uses it to
    # gather the path where the package is going to be deployed
    manager_path = resolve_manager(cwd)
    target_path = os.path.join(manager_path, target)

    # retrieves some of the descriptor information and uses it to create
    # the reference to the target path of the package deployment
    short_name = descriptor["short_name"]
    short_path = os.path.join(target_path, short_name + suffix)
    spec_path = os.path.join(short_path, "spec.json")
    resources_path = os.path.join(temp_path, "resources")

    # in case the target deployment path already exists (must be an upgrade)
    # it must be removed to avoid overlapping in files, this is considered
    # to be a safe operation only for upgrade operations
    if os.path.exists(short_path): shutil.rmtree(short_path)

    # moves the resources part of the package into the target path for the
    # package in the manager tree and then removes the temporary path
    shutil.move(resources_path, short_path)
    shutil.rmtree(temp_path)

    # dumps the current descriptor object for the item that is going to be
    # deployed and then writes the contents of it into the info based file
    # that is going to be used as a meta information provid3er
    descriptor_s = json.dumps(descriptor)
    is_unicode = colony.legacy.is_unicode(descriptor_s)
    if is_unicode: descriptor_s = descriptor_s.encode("utf-8")
    file = open(spec_path, "wb")
    try: file.write(descriptor_s)
    finally: file.close()

def _info(path):
    # retrieves the descriptor as a dictionary for the requested package
    # path, this should contain a valid dictionary with the information
    # read from the spec file associated with the package
    descriptor = _read(path)

    # retries the proper package type from the descriptor and uses it to
    # defined the correct method to be called for the info command
    type = descriptor.get("type", "plugin")
    if type == "plugin": _info_plugin(descriptor)
    elif type == "config": _info_config(descriptor)
    else: RuntimeError("invalid package type")

def _info_plugin(descriptor):
    output("id           := %s" % descriptor["id"])
    output("name         := %s" % descriptor["name"])
    output("short name   := %s" % descriptor["short_name"])
    output("version      := %s" % descriptor["version"])
    output("author       := %s" % descriptor["author"])
    output("description  := %s" % descriptor["description"])
    output("dependencies := %s" % ", ".join(descriptor["dependencies"]))
    output("capabilities := %s" % ", ".join(descriptor["capabilities"]))
    output("allowed      := %s" % ", ".join(descriptor["capabilities_allowed"]))

def _info_config(descriptor):
    output("id           := %s" % descriptor["id"])
    output("name         := %s" % descriptor["name"])
    output("short name   := %s" % descriptor["short_name"])
    output("version      := %s" % descriptor["version"])
    output("author       := %s" % descriptor["author"])
    output("description  := %s" % descriptor["description"])

def _install(name = None, id = None, version = None, upgrade = False):
    import appier

    # verifies if the provided version string is wildcard based and
    # for such situations invalidated the version value (sets to invalid)
    if version == "x.x.x": version = None

    # constructs the proper description string taking into account
    # if the name or the id has been provided and then prints a
    # message about the installation operation that is going to start
    description = name or id
    output("Installing package %s" % description)

    # creates the map containing the various parameters that are
    # going to be sent as part of the filtering process for the
    # remote request of package retrieval
    params = dict(filters = [])
    if name: params["filters"].append("name:equals:%s" % name)
    if id: params["filters"].append("identifier:equals:%s" % id)

    # retrieves the proper repository URL that is currently defined
    # then enforces the value to be a valid sequence, so that the
    # logic is defined as cycle of URL based package detection
    repo_url = colony.conf("REPO_URL", REPO_URL)
    if not type(repo_url) in (list, tuple): repo_url = (("colony", repo_url),)

    # starts the variable that will hold the found package at invalid
    # so that the value is set only when a repo contains a package
    # matching the defined criteria
    package = None

    # iterates over the complete set of repositories defined in the
    # repository URL value trying to find the proper package, note
    # that the package is found when at least one result is returned
    # matching the provided criteria (as defined in specification)
    for _name, _repo_url in repo_url:
        url = _repo_url + "packages"
        result = appier.get(url, params = params)
        package = result[0] if result else dict()
        is_valid = True if package else False
        is_valid &= package["name"] == name if package and name else True
        is_valid &= package["identifier"] == id if package and id else True
        if not is_valid: package = None
        if not package: continue
        repo_url = _repo_url
        break

    # in case no package has been found for any of the defined repos
    # an exception must be raised indicating the problem to the user
    if not package: raise RuntimeError("Package not found")

    # constructs the proper URL for package information retrieval and
    # runs it so that the complete set of information (including dependencies)
    # is gathered providing the system with the complete set of options
    url = repo_url + "packages/%s/info" % package["name"]
    info = appier.get(url, params = dict(version = version))

    # verifies if the package is already installed under the current
    # system and if that's the case returns immediately as there's
    # nothing remaining to be done for such situation
    if _exists(info, upgrade = upgrade):
        output("Package %s is already installed, skipping" % description)
        return

    # runs the dependencies operation for the current package information
    # this operation should be able to install all the requirements for
    # the current package in transit (avoid package corruption)
    try: indent(); _dependencies(info, upgrade = upgrade)
    finally: unindent()

    # prints information about the starting of the package download, this
    # is required for the user to be notified about such action
    output("Downloading %s" % description)

    # creates the proper package retrieval URL and runs the remote get request
    # to try to retrieve the package contents of so that they are installed
    url = repo_url + "packages/%s" % info["short_name"]
    data = appier.get(url, params = dict(version = info["version"]))

    # creates a new temporary directory for the new bundle file that is going
    # to be created and stores it under such directory (for deployment)
    temp_path = tempfile.mkdtemp()
    target_path = os.path.join(temp_path, "%s.cbx" % info["short_name"])
    file = open(target_path, "wb")
    try: file.write(data)
    finally: file.close()

    # runs the deployment process for the package bundle that has been retrieved
    # and then removes the temporary directory path, as it's no longer required
    _deploy(target_path, timestamp = info["timestamp"])
    shutil.rmtree(temp_path)

    # prints a message about the end of the installation process for the current
    # package, this will allow the user to be aware of the end of operation
    output("Finished installing %s" % description)

def _require(path, upgrade = False):
    # opens the file located at the provided path and reads the
    # complete set of contents from it, this should be a small
    # to medium size file so there should be no problems
    file = open(path, "rb")
    try: contents = file.read()
    finally: file.close()

    # decodes the provided contents using the expected encoding
    # of the require file (as defined is specification)
    contents = contents.decode("utf-8")

    # splits the lines in the current file and removes the ones
    # that are not considered valid, after that runs the install
    # operation for each one of the dependency requests
    lines = contents.split("\n")
    lines = [line.strip() for line in lines if line.strip()]
    for line in lines: _install(line, upgrade = upgrade)

def _upgrade():
    # starts the initial list of gathered plugins and config as
    # an empty list, this is going to be populated with the items
    # found for the current instance from the file system
    plugins = []
    configs = []

    # retrieves the current working directory and uses it to compute
    # the final manager path that is going to be used for discovery
    cwd = os.getcwd()
    manager_path = resolve_manager(cwd)

    # "calculates" both the path to the plugins directory and to the
    # meta information directory, both of them will be used to gather
    # the information on the current instace's deployment
    plugins_path = os.path.join(manager_path, "plugins")
    meta_path = os.path.join(manager_path, "meta")

    # iterates over the complete set of items in the plugins path in
    # order to be able to discover the currently installed plugins
    for item in os.listdir(plugins_path):
        if not item.endswith("_plugin"): continue
        plugins.append(item[:-7])

    # gather the information on the currently installed configs by
    # fetching information on the meta path (target config location)
    for item in os.listdir(meta_path):
        if not item.endswith("_config"): continue
        configs.append(item[:-7])

    # iterates over both the plugins and the configs to try to upgrade
    # the complete set of items as requested by the operation
    for plugin in plugins: _install(plugin, upgrade = True)
    for config in configs: _install(config, upgrade = True)

def _upload(path, repo = "colony", generate = True, delete = True):
    import json
    import appier

    # tries to runs the expansion of the glob for the provided path and
    # in case it expands to multiple values the same upload operation is
    # run on each of the items that compromise the expansion
    expansion = glob.glob(path)
    is_multiple = len(expansion) > 1
    if is_multiple:
        for item in expansion: _upload(
            item,
            repo = repo,
            generate = generate,
            delete = delete
        )
        return
    if not expansion: raise RuntimeError("No path found for '%s'" % path)
    path = expansion[0]

    # in case the generate flag is active the package file is generated
    # for the path and then the descriptor information dictionary is read
    # so that it's possible to properly upload the file to the repository
    if generate: path = _generate(path)
    descriptor = _read(path)

    # opens the path of the package file that is going to be uploaded
    # in order to be able to read the full contents of it, these are
    # going to be the contents to be uploaded to the repository
    file = open(path, "rb")
    try: contents = file.read()
    finally: file.close()

    # tries to retrieve the currently targeted repository info taking
    # into account both the environment and the static values
    repo_url = colony.conf("REPO_URL", REPO_URL)
    repo_username = colony.conf("REPO_USERNAME", "root")
    repo_password = colony.conf("REPO_PASSWORD", "root")

    # enforces the repository URL to be defined as a sequence for better
    # handling of the logic and then retrieves the requested target
    # repository base URL value, raising an exception in case it's not found
    if not type(repo_url) in (list, tuple): repo_url = (("colony", repo_url),)
    repo_url = dict(repo_url)
    repo_url = repo_url.get(repo)
    repo_url = colony.conf("REPO_URL_" + repo.upper(), repo_url)
    if not repo_url: raise RuntimeError("URL for repository '%s' not found" % repo)

    # prints a message about the upload operation that is going to occur
    # so that the end user knows where the upload is going
    output("Uploading %s into %s repo (%s)" % (descriptor["short_name"], repo, repo_url))

    # creates the URL format, taking into account the defined URL and the
    # current descriptor and then runs the upload, using a post operation
    url = repo_url + "packages"
    login_url = repo_url + "api/admin/login"
    auth = appier.post(login_url, params = dict(
        username = repo_username,
        password = repo_password
    ))
    appier.post(url, data_m = dict(
        sid = auth["sid"],
        identifier = descriptor["id"],
        name = descriptor["short_name"],
        version = descriptor["version"],
        type = descriptor["type"],
        info = json.dumps(descriptor),
        contents = ("contents", contents)
    ))

    # in case the delete flag is active the package file is delete after
    # a proper upload operation is performed (house keeping)
    if delete: os.remove(path)

def _read(path):
    import json

    # creates a new temporary directory path where the contents of
    # the package file are going to be extracted
    temp_path = tempfile.mkdtemp()

    # reads the package (zip file) and then extracts the complete
    # set of it's contents into the temporary directory so that they
    # may be manipulated and then properly used
    file = zipfile.ZipFile(path, mode = "r")
    try: file.extractall(temp_path)
    finally: file.close()

    # retrieves the path of the specification file and reads it's JSON
    # contents so that it's possible to retrieve more information about
    # the package that is going to have information printed
    spec_path = os.path.join(temp_path, "spec.json")
    file = open(spec_path, "rb")
    try: data = file.read()
    finally: file.close()
    shutil.rmtree(temp_path)

    # decodes the "raw" data using the default JSON encoding
    # and then runs the proper JSON decoding/loading
    data = data.decode("utf-8")
    descriptor = json.loads(data)

    # returns the read descriptor dictionary to the caller metho/function
    # so that it may be used to interpret the current package in action
    return descriptor

def _exists(info, upgrade = False):
    import json

    cwd = os.getcwd()
    manager_path = resolve_manager(cwd)

    type = info.get("type", "plugin")
    if type == "plugin": target = "plugins"; suffix = "_plugin"
    elif type == "config": target = "meta"; suffix = "_config"
    else: RuntimeError("invalid package type")

    target_path = os.path.join(manager_path, target)

    short_name = info["short_name"]
    short_path = os.path.join(target_path, short_name + suffix)

    if not os.path.exists(short_path): return False
    if not upgrade: return True

    spec_path = os.path.join(short_path, "spec.json")
    file = open(spec_path, "rb")
    try: data = file.read()
    finally: file.close()

    data = data.decode("utf-8")
    descriptor = json.loads(data)
    if not info["version"] == descriptor["version"]: return False
    if info["timestamp"] > descriptor["timestamp"]: return False

    return True

def _dependencies(info, upgrade = False):
    dependencies = info.get("dependencies", [])
    for dependency in dependencies:
        if dependency["type"] in ("package",): continue
        _install(
            id = dependency["id"],
            version = dependency["version"],
            upgrade = upgrade
        )

def _fitler_resources(resources, exclusion = (".pyc", ".temp", ".tmp")):
    filtered = []
    for resource in resources:
        if resource.endswith(exclusion): continue
        filtered.append(resource)
    return filtered

def _gather_config(base_path):
    valid = []
    result = []

    items = os.listdir(base_path)
    for item in items:
        path = os.path.join(base_path, item)
        if item.startswith("."): continue
        if not os.path.isdir(path): continue
        valid.append(path)

    for _valid in valid:
        for root, _dirs, files in os.walk(_valid):
            relative = os.path.relpath(root, base_path)
            relative = relative.replace("\\", "/")
            files = [relative + "/" + file for file in files]
            result.extend(files)

    return result

def _gather_direct(short_name, base_dir, name):
    result = []

    root_path = os.path.join(base_dir, name)
    exists = os.path.exists(root_path)
    if not exists: root_path = os.path.join(base_dir, name + "_c")

    for root, _dirs, files in os.walk(root_path):
        relative = os.path.relpath(root, root_path)
        relative = relative.replace("\\", "/")
        if relative == ".": relative = name
        else: relative = name + "/" + relative
        files = [relative + "/" + file for file in files]
        result.extend(files)

    return result

def _gather_indirect(short_name, base_dir, name):
    root_path = os.path.join(base_dir, name)

    target = None
    names = os.listdir(root_path)
    for _name in names:
        if short_name.endswith(_name): target = _name; break
        elif short_name.startswith(_name): target = _name; break

    if not target: return []

    result = [name + "/__init__.py"]

    base_path = os.path.join(root_path, target)
    for root, _dirs, files in os.walk(base_path):
        relative = os.path.relpath(root, root_path)
        relative = relative.replace("\\", "/")
        relative = name + "/" + relative
        files = [relative + "/" + file for file in files]
        result.extend(files)

    return result

def _gather_invalid(short_name, base_dir, name):
    output("No directory found for plugin %s" % short_name)
    return []

def _zip_directory(path, relative, file):
    # verifies that the provided path exists and is
    # a valid directory, in case it does not returns
    # immediately to avoid any problem, the provided
    # zip file is not going to contain of the data
    if not os.path.isdir(path): return

    # retrieves the list of entries for the path to
    # be compressed into the zip
    entries = os.listdir(path)

    # iterates over the list of entries to zip them
    # or enter in a new recursion level
    for entry in entries:
        # create the fill entry path by joining the entry
        # name to the (base) path of the directory and
        # then creates also the relative path
        _path = os.path.join(path, entry)
        _relative = os.path.join(relative, entry)

        # checks if the path is a directory and in such case runs
        # the recursion step, otherwise writes the file directly
        # into the "target" zip file
        if os.path.isdir(_path): _zip_directory(_path, _relative, file)
        else: file.write(_path, _relative)

def main():
    # retrieves the operation from the provided arguments
    # and retrieves the associated function to be executed
    operation = "help" if len(sys.argv) < 2 else sys.argv[1]
    _globals = globals()
    function = _globals.get(operation, None)
    if function: function()
    else: raise RuntimeError("Invalid operation")

if __name__ == "__main__":
    main()
else:
    __path__ = []
