#!/usr/bin/python
# -*- coding: Cp1252 -*-

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

__revision__ = "$LastChangedRevision: 10411 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-09-14 19:26:03 +0100 (ter, 14 Set 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import json
import time
import types
import shutil
import logging
import datetime
import tempfile

import colony_zip
import colony_file

DEFAULT_PATH_VALUE = os.path.dirname(os.path.realpath(__file__))
""" The default path """

DEFAULT_MANAGER_PATH_VALUE = os.path.normpath(os.path.realpath(DEFAULT_PATH_VALUE + "/../.."))
""" The default manager path """

TYPE_VALUE = "type"
""" The type value """

ID_VALUE = "id"
""" The id value """

VERSION_VALUE = "version"
""" The version value """

PLUGINS_VALUE = "plugins"
""" The plugins value """

MAIN_FILE_VALUE = "main_file"
""" The main file value """

RESOURCES_VALUE = "resources"
""" The resources value """

INSTALLED_PLUGINS_VALUE = "installed_plugins"
""" The installed plugins value """

VERSION_VALUE = "version"
""" The version value """

TIMESTAMP_VALUE = "timestamp"
""" The timestamp value """

LAST_MODIFIED_TIMESTAMP_VALUE = "last_modified_timestamp"
""" The last modified timestamp value """

LAST_MODIFIED_DATE_VALUE = "last_modified_date"
""" The last modified date value """

SPECIFICATION_FILE_NAME = "specification.json"
""" The specification file name """

RELATIVE_DEPLOY_PATH = "deploy"
""" The path relative to the manager path for the deploy source """

RELATIVE_PLUGINS_PATH = "plugins"
""" The path relative to the manager path for the plugins """

RELATIVE_REGISTRY_PATH = "var/registry"
""" The path relative to the manager path for the registry """

REQUIRED_VALUES = ("platform", "id", "version")
""" The tuple of required values """

COLONY_FILE_EXTENSIONS = (".cbx", ".cpx")
""" The tuple containing all the colony file extensions """

class Deployer:
    """
    The deployer class responsible for the management
    of the deployment structures.
    """

    manager_path = None
    """ The path to the manager """

    def __init__(self, manager_path):
        """
        Constructor of the class.

        @type manager_path: String
        @param manager_path: The manager path.
        """

        self.manager_path = manager_path

    def log(self, message):
        """
        Logs the given message for the given
        verbose setting.

        @type message: String
        @param message: The message to be logged.
        """

        # retrieves the logger
        logger = logging.getLogger("default")

        # prints a debug message
        logger.debug(message)

    def deploy_info(self, package_path):
        """
        Deploys the package by printing it's information.
        This deployment is just virtual and only
        prints information.

        @type package_path: String
        @param package_path: The path to the package to be "deployed".
        """

        # in case the package path does not exist
        if not os.path.exists(package_path):
            # raises an exception
            raise Exception("The package path '%s' does not exist" % package_path)

        # creates a new zip (manager)
        zip = colony_zip.Zip()

        # prints a log message
        self.log("Reading specification file")

        # reads the specification file contents from the zip file
        specification_file_contents = zip.read(package_path, SPECIFICATION_FILE_NAME)

        # loads the json specification file contents
        specification = json.loads(specification_file_contents)

        # prints the specification
        self.print_specification(specification)

    def deploy_flush(self):
        """
        Deploys the package in flush mode.
        The flush mode allows the multiple deployment of
        all the files in the deploy directory.
        """

        # creates the deploy path
        deploy_path = os.path.normpath(self.manager_path + "/" + RELATIVE_DEPLOY_PATH)

        # list the deploy path
        deploy_files = os.listdir(deploy_path)

        # iterates over all the file to
        # be deployed
        for deploy_file in deploy_files:
            # splits the deploy file into base and extension
            _deploy_file_base, deploy_file_extension = os.path.splitext(deploy_file)

            # in case the deploy file extension
            # is not a colony valid file extension
            if not deploy_file_extension in COLONY_FILE_EXTENSIONS:
                # continues the loop
                continue

            # creates the deploy full path by joining
            # the deploy path and the deploy file (name)
            deploy_full_path = os.path.join(deploy_path, deploy_file)

            # deploys the package in the given path to target
            # manager path
            self.deploy_package(deploy_full_path, self.manager_path)

            # removes the deploy file (using the full path)
            os.remove(deploy_full_path)

    def unzip_package(self, package_path):
        # creates a new temporary path
        temporary_path = tempfile.mkdtemp()

        # in case the package path does not exist
        if not os.path.exists(package_path):
            # raises an exception
            raise Exception("The package path '%s' does not exist" % package_path)

        # prints a log message
        self.log("Unpacking package file '%s' using zip decoder" % (package_path))

        # creates a new zip (manager)
        zip = colony_zip.Zip()

        # unzips the package to the temporary path
        zip.unzip(package_path, temporary_path)

        # returns the temporary path
        return temporary_path

    def load_specification(self, specification_file_path):
        # prints a log message
        self.log("Opening specification file '%s'" % (specification_file_path))

        # reads the specification file contents
        specification_file_contents = colony_file.read_file(specification_file_path)

        # loads the json specification file contents
        specification = json.loads(specification_file_contents)

        # returns the specification
        return specification

    def deploy_package(self, package_path):
        """
        Deploys the package in the given package path to the
        appropriate targets.

        @type package_path: String
        @param package_path: The path to the package to be deployed.
        """

        # prints a log message
        self.log("Deploying '%s' to '%s'" % (package_path, self.manager_path))

        # unpacks the package to a temporary path
        temporary_path = self.unzip_package(package_path)

        # creates the specification file path
        specification_file_path = os.path.normpath(temporary_path + "/" + SPECIFICATION_FILE_NAME)

        try:
            # loads the specification from the specification file path
            specification = self.load_specification(specification_file_path)

            # retrieves the type
            type = specification[TYPE_VALUE]

            # in case the type is bundle
            if type == "bundle":
                # deploys the bundle package, using the current paths
                self.deploy_bundle_package(package_path, temporary_path)
            # in case the type is plugin
            elif type == "plugin":
                # deploys the plugin package, using the current paths
                self.deploy_plugin_package(package_path, temporary_path)
            # otherwise there is an error
            else:
                # raises an exception
                raise Exception("Invalid packaging type")
        except Exception, exception:
            # prints a log message
            self.log("Problem deploying '%s' with error '%s'" % (package_path, str(exception)))

            # re-raises the exception
            raise
        finally:
            # prints a log message
            self.log("Removing temporary path '%s'" % temporary_path)

            # removes the temporary path (directory)
            self.remove_directory(temporary_path)

        # prints a log message
        self.log("Finished deployment")

    def deploy_bundle_package(self, package_path, temporary_path):
        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the specification file path
        specification_file_path = os.path.normpath(temporary_path + "/" + SPECIFICATION_FILE_NAME)

        # loads the specification from the specification file path
        specification = self.load_specification(specification_file_path)

        # retrieves the id
        id = specification[ID_VALUE]

        # retrieves the version
        version = specification[VERSION_VALUE]

        # retrieves the plugins
        plugins = specification[PLUGINS_VALUE]

        # prints a log message
        self.log("Deploying bundle package '%s' v'%s'" % (id, version))

        # iterates over all the plugins
        for plugin in plugins:
            # retrieves the plugin id
            plugin_id = plugin[ID_VALUE]

            # retrieves the plugin version
            plugin_version = plugin[VERSION_VALUE]

            # creates the plugin file name
            plugin_file_name = plugin_id + "_" + plugin_version + ".cpx"

            # retrieves the plugin file path
            plugin_file_path = os.path.normpath(temporary_path + "/plugins/" + plugin_file_name)

            # unpacks the package to a temporary path
            temporary_path = self.unzip_package(plugin_file_path)

            # deploys the plugin package, using the current paths
            self.deploy_plugin_package(plugin_file_path, temporary_path)

        # copies the package file to the registry
        shutil.copy(package_path, registry_path + "/bundles")

    def deploy_plugin_package(self, package_path, temporary_path):
        # retrieves the target path
        target_path = os.path.normpath(self.manager_path + "/" + RELATIVE_PLUGINS_PATH)

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the specification file path
        specification_file_path = os.path.normpath(temporary_path + "/" + SPECIFICATION_FILE_NAME)

        # loads the specification from the specification file path
        specification = self.load_specification(specification_file_path)

        # retrieves the id
        id = specification[ID_VALUE]

        # retrieves the version
        version = specification[VERSION_VALUE]

        # retrieves the main file
        main_file = specification[MAIN_FILE_VALUE]

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # prints a log message
        self.log("Deploying plugin package '%s' v'%s'" % (id, version))

        # prints a log message
        self.log("Moving resources from '%s' to '%s'" % (temporary_path, target_path))

        # iterates over all the resources
        for resource in resources:
            # retrieves the resource file path
            resource_file_path = os.path.normpath(temporary_path + "/resources/" + resource)

            # creates the new resource file path
            new_resource_file_path = os.path.normpath(target_path + "/" + resource)

            # retrieves the new resource directory path
            new_resource_directory_path = os.path.dirname(new_resource_file_path)

            # prints a log message
            self.log("Moving resource file '%s' to '%s'" % (resource_file_path, new_resource_file_path))

            # in case the new resource directory path does not exist
            if not os.path.exists(new_resource_directory_path):
                # creates the new resource directory path (directories)
                os.makedirs(new_resource_directory_path)

            # copies the resource file as the new resource file
            shutil.copy(resource_file_path, new_resource_file_path)

        # prints a log message
        self.log("Moving main file '%s' to '%s'" % (resource_file_path, new_resource_file_path))

        # splits the main file name into name and extension
        main_file_name, _mail_file_extension = os.path.splitext(main_file)

        # creates the new specification file name
        new_specification_file_name = main_file_name + ".json"

        # creates the new specification file path
        new_specification_file_path = os.path.normpath(target_path + "/" + new_specification_file_name)

        # copies the specification file as the new specification file
        shutil.copy(specification_file_path, new_specification_file_path)

        # reads the plugins file contents
        plugins_file_contents = colony_file.read_file(registry_path + "/plugins.json")

        # loads the plugin file contents from json
        plugins = json.loads(plugins_file_contents)

        # retrieves the installed plugins
        installed_plugins = plugins.get(INSTALLED_PLUGINS_VALUE, {})

        # retrieves the current time
        current_time = time.time()

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # formats the current date time
        current_date_time_formated = current_date_time.strftime("%d-%m-%Y %H:%M:%S")

        # sets the installed plugin map
        installed_plugins[id] = {
            VERSION_VALUE : version,
            TIMESTAMP_VALUE : current_time
        }

        # updates the plugins map with the current time
        # and date time values
        plugins[LAST_MODIFIED_TIMESTAMP_VALUE] = current_time
        plugins[LAST_MODIFIED_DATE_VALUE] = current_date_time_formated

        # serializes the plugins
        plugins_serialized = json.dumps(plugins)

        # writes the plugins file contents
        colony_file.write_file(registry_path + "/plugins.json", plugins_serialized)

        # copies the package file to the registry
        shutil.copy(package_path, registry_path + "/plugins")

    def validate_specification(self, specification):
        """
        Validates the given specification map, checking if
        all the required values are set.
        In case the validation fails an exception is raised.

        @type specification: Dictionary
        @param specification: The map containing the specification
        values.
        """

        # iterates over all the required values in the required values list
        for required_value in REQUIRED_VALUES:
            # in case the required value is not in the specification
            if not required_value in specification:
                # raises an exception
                raise Exception("Required value '%s' missing in specification file" % (required_value))

    def print_specification(self, specification):
        """
        Prints the specification map information to the
        console.

        @type specification: Dictionary
        @param specification: The map containing the specification
        values.
        """

        # retrieves the required (mandatory) values
        platform = specification["platform"]
        id = specification["id"]
        version = specification["version"]

        # retrieves the optional values
        sub_platforms = specification.get("sub_platforms", [])
        name = specification.get("name", "")
        short_name = specification.get("short_name", "")
        description = specification.get("description", "")
        author = specification.get("author", "")
        capabilities = specification.get("capabilities", [])
        capabilities_allowed = specification.get("capabilities_allowed", [])
        dependencies = specification.get("dependencies", [])
        main_file = specification.get("main_file", [])
        resources = specification.get("resources", [])

        # prints the various values
        self.print_value("Platform", platform)
        self.print_value("Sub-Platforms", sub_platforms)
        self.print_value("Id", id)
        self.print_value("Name", name)
        self.print_value("Short Name", short_name)
        self.print_value("Description", description)
        self.print_value("Version", version)
        self.print_value("Author", author)
        self.print_value("Capabilities", capabilities)
        self.print_value("Capabilities Allowed", capabilities_allowed)
        self.print_value("Dependencies", dependencies)
        self.print_value("Main File", main_file)
        self.print_value("Resources", resources)

    def print_value(self, key, value):
        """
        Prints the key value composite value.
        The output is redirected to the standard output.

        @type key: String
        @param key: The key value to be printed.
        @type value: String
        @param value: The value value to be printed.
        """

        # retrieves the type of the value
        value_type = type(value)

        # in case the value is a string
        if value_type in types.StringTypes:
            print key + ": " + value
        # in case the value is a list (of strings)
        elif value_type == types.ListType:
            # prints the key
            print key,

            # prints the value
            print ":" + str(value)

    def remove_directory(self, directory_path):
        """
        Removes the given directory path recursively.
        Directories containing files will have their contents removed
        before being removed.

        @type directory_path: String
        @param directory_path: The path to the directory to be removed.
        """

        # creates the list of paths for the directory path
        paths_list = [os.path.join(directory_path, file_path) for file_path in os.listdir(directory_path)]

        # iterates over all the paths in the paths
        # list to remove them
        for path in paths_list:
            # in case the path is a directory
            if os.path.isdir(path):
                # removes the directory
                self.remove_directory(path)
            else:
                # removes the path
                os.remove(path)

        # removes the directory
        os.rmdir(directory_path)
