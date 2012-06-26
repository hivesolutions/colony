#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision: 17846 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-11-15 21:58:28 +0000 (ter, 15 Nov 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import shutil
import zipfile

DEFAULT_TARGET = "colony"
""" The default directory to be used as target in
case no target path is provided (default name) """

DEFAULT_ROOT = "COLONY_ROOT"
""" The default name for the file to be used to
indicate the root directory of a colony instance """

PACK_FILE = "colony.zip"
""" The name of the file that will be the packing
reference of the instance """

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

    # in case not target path is defined must raise
    # a runtime error
    if not target: raise RuntimeError("no instance found")

    # runs the pack command on the target path
    # to create the packed file for the colony instance
    _pack(target)

def _cleanup(path):
    # retrieves the path to the series of sub
    # directories to be "cleaned"
    log_path = os.path.join(path, "log")

    # removes the files using extension based rules
    # on the defined directories
    _cleanup_files(path, ".pyc")
    _cleanup_files(log_path, ".log")

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
        if _path.endswith(extension): os.remove(_path)

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
    # retrieves the operation from the provided arguments
    # and retrieves the associated function to be executed
    operation = sys.argv[1]
    _globals = globals()
    function = _globals.get(operation, None)
    if function: function()
    else: raise RuntimeError("invalid operation")

if __name__ == "__main__":
    main()
