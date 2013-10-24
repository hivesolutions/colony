#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import atm

def build(file = None):
    # runs the initial assertion for the various commands
    # that are mandatory for execution, this should avoid
    # errors in the middle of the build
    atm.assert_c(("git", "python --version", "colony_admin version"))

    # starts the build process with the configuration file
    # that was provided to the configuration script
    atm.build(file, arch = "all")

    # retrieves the various values from the global configuration
    # that are going to be used around the configuration
    name_ver = atm.conf("name_ver")
    name_arc = atm.conf("name_arc")
    name_raw = atm.conf("name_raw")
    name_src = atm.conf("name_src")

    # creates the various paths to the folders to be used
    # for the build operation, from the ones already loaded
    repo_f = atm.path("repo")
    result_f = atm.path("result")
    tmp_f = atm.path("tmp")
    dist_f = atm.path("dist")
    build_f = atm.path("build")

    # clones the current repository using the git command and then
    # copies the resulting directory to the result and temporary
    # directories, to be used latter in the build
    atm.git(clean = True)
    atm.copy(repo_f, result_f)
    atm.copy(repo_f, os.path.join(tmp_f, name_src))

    # changes the current directory to the repository one and runs
    # the python tests and source build on it, then copies the
    # resulting source build file to the distribution directory
    os.chdir(repo_f)
    atm.pytest()
    atm.pysdist()
    atm.copy(os.path.join("dist", name_ver + ".zip"), dist_f)

    # changes the current directory to the source directory of the
    # repository and runs the colony container builder then copies
    # the result from it to the distribution folder
    os.chdir(os.path.join(repo_f, "src"))
    atm.colony(descriptor = "container.json")
    atm.move("pt.hive.colony.ccx", dist_f)

    # changes the current directory to the source one in the result
    # directory (contents are considered the "binaries") and then
    # creates a tar file with its contents (contents should be raw)
    os.chdir(os.path.join(result_f, "src"))
    atm.tar(name_raw + ".tar")
    atm.move(name_raw + ".tar", dist_f)

    # changes the current directory to the build one and creates a
    # capsule executable using the "just" created raw tar file, the
    # metadata values will be used from the current context
    os.chdir(build_f)
    atm.capsule(
        os.path.join(dist_f, name_arc + ".exe"),
        os.path.join(dist_f, name_raw + ".tar")
    )

    # creates the various compressed files for both the archive and
    # source directories (distribution files)
    os.chdir(tmp_f)
    atm.compress(name_src, target = dist_f)

    # creates the various hash files for the complete set of files in
    # the distribution directory
    os.chdir(dist_f)
    atm.hash_d()

def run():
    # parses the various arguments provided by the
    # command line and retrieves it defaulting to
    # pre-defined values in case they do not exist
    arguments = atm.parse_args(names = ())
    file = arguments.get("file", None)

    # starts the build process with the parameters
    # retrieved from the current environment
    build(
        file = file
    )

def cleanup():
    atm.cleanup()

if __name__ == "__main__":
    try: run()
    finally: cleanup()
