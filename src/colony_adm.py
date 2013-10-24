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

__author__ = "João Magalhães <joamag@hive.pt>"
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

import re
import os
import sys
import shutil
import zipfile

import colony.libs.string_util

DEFAULT_TARGET = "colony"
""" The default directory to be used as target in
case no target path is provided (default name) """

DEFAULT_ROOT = "COLONY_ROOT"
""" The default name for the file to be used to
indicate the root directory of a colony instance """

PACK_FILE = "colony.zip"
""" The name of the file that will be the packing
reference of the instance """

EXTENSIONS = {
    "bundle" : ".cbx",
    "plugin" : ".cpx",
    "container" : ".ccx"
}
""" The map associating the various types of
colony packages with the associated extension """

REMOVALS = (
    "colony.egg-info",
    "EGG-INFO"
)
""" The list of paths to be removed because there's
no use for them in the target colony instance """

def get_base_path(path):
    # iterates continuously while the root path is not
    # reached or a root file paths is not found
    while True:
        # creates the possible root file path and then
        # tests for its existence in such case returns
        # the directory path as the base one (found)
        # otherwise must continue the loop (top directory)
        # but only if this is not the top level root directory
        root_file_path = os.path.join(path, DEFAULT_ROOT)
        if os.path.exists(root_file_path): return path
        if os.path.dirname(path) == path: break
        path = os.path.join(path, "..")
        path = os.path.normpath(path)

    # returns invalid no base path was found
    # not possible to find it
    return None

def version():
    print "colony admin - admin tool for colony framework"

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
    try: root_file = file(root_file_path, "a")
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
    else: target = get_base_path(cwd)

    # in case not target was expanded the current directory
    # is used (assumes) the administration file is stored
    # at the same location as the colony instance
    target = target or os.path.normpath(os.path.dirname(__file__))

    # in case not target path is defined must raise
    # a runtime error
    if not target: raise RuntimeError("no instance found")

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
    else: target = get_base_path(cwd)

    # in case not target was expanded the current directory
    # is used (assumes) the administration file is stored
    # at the same location as the colony instance
    target = target or os.path.normpath(os.path.dirname(__file__))

    # in case not target path is defined must raise
    # a runtime error
    if not target: raise RuntimeError("no instance found")

    # runs the pack command on the target path
    # to create the packed file for the colony instance
    _pack(target)

def build():
    # in case there're not enough arguments to be
    # able to retrieve the specification file raises
    # a runtime error
    if len(sys.argv) < 3: raise RuntimeError("no descriptor provided")

    # retrieves the target file from the arguments and
    # uses it to run the build structure
    target = sys.argv[2]
    _build(target)

def deploy():
    pass

def _cleanup(path, empty_extra = True):
    # retrieves the path to the series of sub
    # directories to be "cleaned"
    log_path = os.path.join(path, "log")
    meta_path = os.path.join(path, "meta")

    # removes the files using extension based rules
    # on the defined directories
    _cleanup_files(path, re.compile(".*\.pyc$"))
    _cleanup_files(log_path, re.compile(".*\.log$"))
    _cleanup_files(log_path, re.compile(".*\.log.[0-9]+$"))
    empty_extra and _cleanup_directories(meta_path, re.compile(""))

def _cleanup_directories(path, extension):
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

    # opens the archive path as a zip file for writing and
    # then writes the current "instance" directory into the zip
    file = zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED)
    try: _zip_directory(path, "/", file)
    finally: file.close()

def _build(path, short_name = False):
    # imports the json module so that it's possible
    # to parse the colony descriptor file
    import json

    # opens the descriptor file to be read in the binary
    # format and loads its json contents to be used
    file = open(path, "rb")
    try: descriptor = json.load(file, "utf-8")
    finally: file.close()

    # retrieves the various attributes from the descriptor
    # file and uses them to infer in some properties
    type = descriptor["type"]
    id = descriptor["id"]
    resources = descriptor.get("resources", [])
    extension = EXTENSIONS.get(type, ".cpx")

    # retrieves the base name for the file and removes the
    # extension from it so that the short name for it is
    # correctly retrieved
    base_name = os.path.basename(path)
    plugin_name = colony.libs.string_util.to_underscore(base_name)[:-12]

    # retrieves the resources directory for the resources
    # from the base directory of the json descriptor and
    # then creates the name of the file from the id
    resources_directory = os.path.dirname(path)
    name = plugin_name + extension if short_name else id + extension

    # opens the target zip file to be used in write
    # mode (it's going to receive the data)
    file = zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED)

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

def _zip_directory(path, relative, file):
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
    # in case the number of arguments is not sufficient
    # raises an exception indicating the problem
    if len(sys.argv) < 2: raise RuntimeError("operation not defined")

    # retrieves the operation from the provided arguments
    # and retrieves the associated function to be executed
    operation = sys.argv[1]
    _globals = globals()
    function = _globals.get(operation, None)
    if function: function()
    else: raise RuntimeError("invalid operation")

if __name__ == "__main__":
    main()
