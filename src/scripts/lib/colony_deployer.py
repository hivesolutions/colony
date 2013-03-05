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
import colony_crypt
import colony_exceptions

DEFAULT_PATH_VALUE = os.path.dirname(os.path.realpath(__file__))
""" The default path """

DEFAULT_MANAGER_PATH_VALUE = os.path.normpath(os.path.realpath(DEFAULT_PATH_VALUE + "/../.."))
""" The default manager path """

TYPE_VALUE = "type"
""" The type value """

ID_VALUE = "id"
""" The id value """

TYPE_VALUE = "type"
""" The type value """

SUB_TYPE_VALUE = "sub_type"
""" The sub type value """

VERSION_VALUE = "version"
""" The version value """

CONFIGURATION_ID_VALUE = "configuration_id"
""" The configuration id value """

PLUGINS_VALUE = "plugins"
""" The plugins value """

CONTAINERS_VALUE = "containers"
""" The containers value """

MAIN_FILE_VALUE = "main_file"
""" The main file value """

RESOURCES_VALUE = "resources"
""" The resources value """

KEEP_RESOURCES_VALUE = "keep_resources"
""" The keep resources value """

EXTRA_RESOURCES_VALUE = "extra_resources"
""" The extra resources value """

INSTALLED_PACKAGES_VALUE = "installed_packages"
""" The installed packages value """

INSTALLED_BUNDLES_VALUE = "installed_bundles"
""" The installed bundles value """

INSTALLED_PLUGINS_VALUE = "installed_plugins"
""" The installed plugins value """

INSTALLED_CONTAINERS_VALUE = "installed_containers"
""" The installed containers value """

TIMESTAMP_VALUE = "timestamp"
""" The timestamp value """

HASH_DIGEST_VALUE = "hash_digest"
""" The hash digest value """

LAST_MODIFIED_TIMESTAMP_VALUE = "last_modified_timestamp"
""" The last modified timestamp value """

LAST_MODIFIED_DATE_VALUE = "last_modified_date"
""" The last modified date value """

BUNDLE_VALUE = "bundle"
""" The bundle value """

PLUGIN_VALUE = "plugin"
""" The plugin value """

CONTAINER_VALUE = "container"
""" The container value """

PLUGIN_SYSTEM_VALUE = "plugin_system"
""" The plugin system value """

LIBRARY_VALUE = "library"
""" The library value """

CONFIGURATION_VALUE = "configuration"
""" The configuration value """

DUPLICATE_FILES_VALUE = "duplicate_files"
""" The duplicate files """

PACKAGES_FILE_NAME = "packages.json"
""" The packages file name """

BUNDLES_FILE_NAME = "bundles.json"
""" The bundles file name """

PLUGINS_FILE_NAME = "plugins.json"
""" The plugins file name """

CONTAINERS_FILE_NAME = "containers.json"
""" The containers file name """

DUPLICATES_FILE_NAME = "duplicates.json"
""" The duplicates file name """

SPECIFICATION_FILE_NAME = "spec.json"
""" The specification file name """

RELATIVE_DEPLOY_PATH = "deploy"
""" The path relative to the manager path for the deploy source """

RELATIVE_BUNDLES_PATH = "bundles"
""" The path relative to the manager path for the bundles """

RELATIVE_PLUGINS_PATH = "plugins"
""" The path relative to the manager path for the plugins """

RELATIVE_CONTAINERS_PATH = "containers"
""" The path relative to the manager path for the containers """

RELATIVE_LIBRARIES_PATH = "libraries"
""" The path relative to the manager path for the libraries """

RELATIVE_CONFIGURATION_PATH = "meta"
""" The path relative to the manager path for the configuration """

RELATIVE_REGISTRY_PATH = "var/registry"
""" The path relative to the manager path for the registry """

REQUIRED_VALUES = (
    "type",
    "id",
    "version"
)
""" The tuple of required values """

JSON_FILE_EXTENSION = ".json"
""" The json file extension """

COLONY_BUNDLE_FILE_EXTENSION = ".cbx"
""" The colony bundle file extension """

COLONY_PLUGIN_FILE_EXTENSION = ".cpx"
""" The colony plugin file extension """

COLONY_CONTAINER_FILE_EXTENSION = ".ccx"
""" The colony container file extension """

COLONY_FILE_EXTENSIONS = (
    COLONY_BUNDLE_FILE_EXTENSION,
    COLONY_PLUGIN_FILE_EXTENSION,
    COLONY_CONTAINER_FILE_EXTENSION
)
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

    def log(self, message, level = logging.DEBUG):
        """
        Logs the given message for the given
        logging level setting.

        @type message: String
        @param message: The message to be logged.
        @type level: Level
        @param level: The level of logging to be used.
        """

        # retrieves the logger
        logger = logging.getLogger("default")

        # prints a debug message
        logger.log(level, message)

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
            # raises a deployer exception
            raise colony_exceptions.DeployerException("the package path '%s' does not exist" % package_path)

        # creates a new zip (manager)
        zip = colony_zip.Zip()

        # prints a log message
        self.log("Reading specification file", logging.INFO)

        # reads the specification file contents from the zip file
        specification_file_contents = zip.read(package_path, SPECIFICATION_FILE_NAME)

        # loads the json specification file contents
        specification = json.loads(specification_file_contents)

        # validates the specification
        self.validate_specification(specification)

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

            # deploys the package in the given path
            self.deploy_package(deploy_full_path)

            # removes the deploy file (using the full path)
            os.remove(deploy_full_path)

    def exists_package(self, package_id):
        """
        Tests if the package with the given id exists in the
        current appropriate target.

        @type package_id: String
        @param package_id: The id of the package to be tested
        for existence.
        @rtype: bool
        @return: The result of the existence package test.
        """

        # retrieves the packages structure
        packages = self._get_packages()

        # retrieves the installed packages
        installed_packages = packages.get(INSTALLED_PACKAGES_VALUE, {})

        # checks if the package exists in the installed packages
        exists_package = package_id in installed_packages

        # returns the exists package (flag)
        return exists_package

    def deploy_package(self, package_path):
        """
        Deploys the package in the given package path to the
        appropriate targets.

        @type package_path: String
        @param package_path: The path to the package to be deployed.
        """

        # prints a log message
        self.log("Deploying '%s' to '%s'" % (package_path, self.manager_path), logging.INFO)

        # unpacks the package to a temporary path
        temporary_path = self._unzip_package(package_path)

        try:
            # creates the specification file path
            specification_file_path = os.path.normpath(temporary_path + "/" + SPECIFICATION_FILE_NAME)

            # opens the specification from the specification file path
            specification = self._open_specification(specification_file_path)

            # retrieves the type
            type = specification[TYPE_VALUE]

            # retrieves the id
            id = specification[ID_VALUE]

            # retrieves the version
            version = specification[VERSION_VALUE]

            # checks if the package is already installed
            # (in case it "exists")
            exists_package = self.exists_package(id)

            # in case the package exists remove the package
            # with the current id
            exists_package and self.remove_package(id)

            # in case the type is bundle
            if type == BUNDLE_VALUE:
                # deploys the bundle package, using the current paths
                self.deploy_bundle_package(package_path, temporary_path)
            # in case the type is plugin
            elif type == PLUGIN_VALUE:
                # deploys the plugin package, using the current paths
                self.deploy_plugin_package(package_path, temporary_path)
            # in case the type is container
            elif type == CONTAINER_VALUE:
                # deploys the container package, using the current paths
                self.deploy_container_package(package_path, temporary_path)
            # otherwise there is an error
            else:
                # raises a deployer exception
                raise colony_exceptions.DeployerException("invalid packaging type: %s" % type)
        except Exception, exception:
            # prints a log message
            self.log("Problem deploying '%s' with error '%s'" % (package_path, str(exception)))

            # re-raises the exception
            raise
        finally:
            # prints a log message
            self.log("Removing temporary path '%s'" % temporary_path)

            # removes the temporary path (directory)
            colony_file.remove_directory(temporary_path)

        # retrieves the package item key
        package_item_key = id

        # generates the hash digest map for the package file
        hash_digest_map = colony_crypt.generate_hash_digest_map(package_path)

        # creates the package item value
        package_item_value = {
            TYPE_VALUE : type,
            VERSION_VALUE : version,
            HASH_DIGEST_VALUE : hash_digest_map
        }

        # adds the package with the given key and value
        self._add_package_item(package_item_key, package_item_value)

        # prints a log message
        self.log("Finished deploying '%s' to '%s'" % (package_path, self.manager_path), logging.INFO)

    def deploy_bundle_package(self, package_path, temporary_path):
        """
        Deploys the given bundle package, using the contents of the
        given temporary path.

        @type package_path: String
        @param package_path: The path to the package to be deployed.
        @type temporary_path: String
        @param temporary_path: The path to the temporary directory with
        the contents of the package.
        """

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the specification file path
        specification_file_path = os.path.normpath(temporary_path + "/" + SPECIFICATION_FILE_NAME)

        # opens the specification from the specification file path
        specification = self._open_specification(specification_file_path)

        # retrieves the id
        id = specification[ID_VALUE]

        # retrieves the version
        version = specification[VERSION_VALUE]

        # retrieves the plugins
        plugins = specification.get(PLUGINS_VALUE, [])

        # retrieves the containers
        containers = specification.get(CONTAINERS_VALUE, [])

        # prints a log message
        self.log("Deploying bundle package '%s' v'%s'" % (id, version))

        # iterates over all the plugins
        for plugin in plugins:
            # retrieves the plugin id and version
            plugin_id = plugin[ID_VALUE]
            plugin_version = plugin[VERSION_VALUE]

            # creates the plugin file name and then uses
            # it to creates the plugin file path
            plugin_file_name = plugin_id + "_" + plugin_version + COLONY_PLUGIN_FILE_EXTENSION
            plugin_file_path = os.path.normpath(temporary_path + "/plugins/" + plugin_file_name)

            # unpacks the package to a temporary (plugin) path
            temporary_plugin_path = self._unzip_package(plugin_file_path)

            try:
                # deploys the plugin package, using the current paths
                self.deploy_plugin_package(plugin_file_path, temporary_plugin_path)
            finally:
                # prints a log message
                self.log("Removing temporary (plugin) path '%s'" % temporary_plugin_path)

                # removes the temporary (plugin) path (directory)
                colony_file.remove_directory(temporary_plugin_path)

            # retrieves the package item key
            package_item_key = plugin_id

            # generates the hash digest map for the package file
            hash_digest_map = colony_crypt.generate_hash_digest_map(plugin_file_path)

            # creates the package item value
            package_item_value = {
                TYPE_VALUE : PLUGIN_VALUE,
                VERSION_VALUE : plugin_version,
                HASH_DIGEST_VALUE : hash_digest_map
            }

            # adds the package with the given key and value
            self._add_package_item(package_item_key, package_item_value)

        # iterates over all the containers,
        # to deploy them
        for container in containers:
            # retrieves the container id and version
            container_id = container[ID_VALUE]
            container_version = container[VERSION_VALUE]

            # creates the container file name and then uses
            # it to creates the container file path
            container_file_name = container_id + "_" + container_version + COLONY_CONTAINER_FILE_EXTENSION
            container_file_path = os.path.normpath(temporary_path + "/containers/" + container_file_name)

            # unpacks the package to a temporary (container) path
            temporary_container_path = self._unzip_package(container_file_path)

            try:
                # deploys the container package, using the current paths
                self.deploy_container_package(container_file_path, temporary_container_path)
            finally:
                # prints a log message
                self.log("Removing temporary (container) path '%s'" % temporary_container_path)

                # removes the temporary (container) path (directory)
                colony_file.remove_directory(temporary_container_path)

            # retrieves the package item key
            package_item_key = container_id

            # generates the hash digest map for the package file
            hash_digest_map = colony_crypt.generate_hash_digest_map(container_file_path)

            # creates the package item value
            package_item_value = {
                TYPE_VALUE : CONTAINER_VALUE,
                VERSION_VALUE : container_version,
                HASH_DIGEST_VALUE : hash_digest_map
            }

            # adds the package with the given key and value
            self._add_package_item(package_item_key, package_item_value)

        # retrieves the bundle item key
        bundle_item_key = id

        # generates the hash digest map for the bundle file
        hash_digest_map = colony_crypt.generate_hash_digest_map(package_path)

        # creates the bundle item value
        bundle_item_value = {
            VERSION_VALUE : version,
            HASH_DIGEST_VALUE : hash_digest_map
        }

        # adds the bundle with the given key and value
        self._add_bundle_item(bundle_item_key, bundle_item_value)

        # creates the proper bundle file name from the id and version of the bundle
        # and then uses it in the copy of the package file into the registry
        bundle_file_name = id + "_" + version + COLONY_BUNDLE_FILE_EXTENSION
        shutil.copy(package_path, registry_path + "/bundles/" + bundle_file_name)

    def deploy_plugin_package(self, package_path, temporary_path):
        """
        Deploys the given plugin package, using the contents of the
        given temporary path.

        @type package_path: String
        @param package_path: The path to the package to be deployed.
        @type temporary_path: String
        @param temporary_path: The path to the temporary directory with
        the contents of the package.
        """

        # retrieves the target path
        target_path = os.path.normpath(self.manager_path + "/" + RELATIVE_PLUGINS_PATH)

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the specification file path
        specification_file_path = os.path.normpath(temporary_path + "/" + SPECIFICATION_FILE_NAME)

        # opens the specification from the specification file path
        specification = self._open_specification(specification_file_path)

        # retrieves the id
        id = specification[ID_VALUE]

        # retrieves the version
        version = specification[VERSION_VALUE]

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # retrieves the keep resources
        keep_resources = specification.get(KEEP_RESOURCES_VALUE, [])

        # prints a log message
        self.log("Deploying plugin package '%s' v'%s'" % (id, version))

        # prints a log message
        self.log("Moving resources from '%s' to '%s'" % (temporary_path, target_path))

        # retrieves the duplicates structure (from file)
        duplicates_structure = self._get_duplicates_structure()

        # retrieves the duplicate files structure
        duplicate_files_structure = duplicates_structure.get(DUPLICATE_FILES_VALUE, {})

        # iterates over all the resources
        for resource in resources:
            # checks if the current resource is of type
            # keep resource
            is_keep_resource = resource in keep_resources

            # retrieves the resource file path
            resource_file_path = os.path.normpath(temporary_path + "/resources/" + resource)

            # creates the new resource file path
            new_resource_file_path = os.path.normpath(target_path + "/" + resource)

            # retrieves the new resource directory path
            new_resource_directory_path = os.path.dirname(new_resource_file_path)

            # checks if the new resource file path already exists
            new_resource_file_path_exists = os.path.exists(new_resource_file_path)

            # in case the new resource file path exists
            # and the resource should be kept
            if new_resource_file_path_exists and is_keep_resource:
                # prints a log message
                self.log("Skipping resource file (keep) '%s'" % resource_file_path)

                # continues the loop (no need
                # to run a copy)
                continue

            # prints a log message
            self.log("Moving resource file '%s' to '%s'" % (resource_file_path, new_resource_file_path))

            # in case the new resource directory path does not exist
            if not os.path.exists(new_resource_directory_path):
                # creates the new resource directory path (directories)
                os.makedirs(new_resource_directory_path)

            # in case the new resource file path already exists we're
            # in a presence of a "duplicate"
            if os.path.exists(new_resource_file_path):
                # "calculates" the relative path between the new resource file
                # path and the manager path
                new_resource_relative_path = os.path.relpath(new_resource_file_path, self.manager_path)

                # aligns the path replacing the backslashes with
                # "normal" slashes
                new_resource_relative_path = self.__align_path(new_resource_relative_path)

                # retrieves the number of times the file is "duplicated"
                duplicate_file_count = duplicate_files_structure.get(new_resource_relative_path, 0)

                # increments the duplicate count by one
                duplicate_file_count += 1

                # sets the duplicate file count in the duplicate files structure
                duplicate_files_structure[new_resource_relative_path] = duplicate_file_count

            # copies the resource file as the new resource file
            shutil.copy(resource_file_path, new_resource_file_path)

        # persists the duplicates structure
        self._persist_duplicates_structure(duplicates_structure)

        # retrieves the plugin item key
        plugin_item_key = id

        # generates the hash digest map for the plugin file
        hash_digest_map = colony_crypt.generate_hash_digest_map(package_path)

        # creates the plugin item value
        plugin_item_value = {
            VERSION_VALUE : version,
            HASH_DIGEST_VALUE : hash_digest_map
        }

        # adds the plugin with the given key and value
        self._add_plugin_item(plugin_item_key, plugin_item_value)

        # creates the proper plugin file name from the id and version of the plugin
        # and then uses it in the copy of the package file into the registry
        plugin_file_name = id + "_" + version + COLONY_PLUGIN_FILE_EXTENSION
        shutil.copy(package_path, registry_path + "/plugins/" + plugin_file_name)

    def deploy_container_package(self, package_path, temporary_path):
        """
        Deploys the given container package, using the contents of the
        given temporary path.

        @type package_path: String
        @param package_path: The path to the package to be deployed.
        @type temporary_path: String
        @param temporary_path: The path to the temporary directory with
        the contents of the package.
        """

        # retrieves the target path
        target_path = os.path.normpath(self.manager_path + "/" + RELATIVE_CONTAINERS_PATH)

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the specification file path
        specification_file_path = os.path.normpath(temporary_path + "/" + SPECIFICATION_FILE_NAME)

        # opens the specification from the specification file path
        specification = self._open_specification(specification_file_path)

        # retrieves the sub type
        sub_type = specification[SUB_TYPE_VALUE]

        # retrieves the id
        id = specification[ID_VALUE]

        # retrieves the version
        version = specification[VERSION_VALUE]

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # retrieves the keep resources
        keep_resources = specification.get(KEEP_RESOURCES_VALUE, [])

        # retrieves the target (exclusive) path to be used
        # uniquely by this container
        target_exclusive_path = os.path.normpath(target_path + "/" + id)

        # prints a log message
        self.log("Deploying container package '%s' v'%s'" % (id, version))

        # prints a log message
        self.log("Moving resources from '%s' to '%s'" % (temporary_path, target_exclusive_path))

        # retrieves the duplicates structure (from file)
        duplicates_structure = self._get_duplicates_structure()

        # retrieves the duplicate files structure
        duplicate_files_structure = duplicates_structure.get(DUPLICATE_FILES_VALUE, {})

        # iterates over all the resources
        for resource in resources:
            # checks if the current resource is of type
            # keep resource
            is_keep_resource = resource in keep_resources

            # retrieves the resource file path
            resource_file_path = os.path.normpath(temporary_path + "/resources/" + resource)

            # creates the new resource file path
            new_resource_file_path = os.path.normpath(target_exclusive_path + "/" + resource)

            # retrieves the new resource directory path
            new_resource_directory_path = os.path.dirname(new_resource_file_path)

            # checks if the new resource file path already exists
            new_resource_file_path_exists = os.path.exists(new_resource_file_path)

            # in case the new resource file path exists
            # and the resource should be kept
            if new_resource_file_path_exists and is_keep_resource:
                # prints a log message
                self.log("Skipping resource file (keep) '%s'" % resource_file_path)

                # continues the loop (no need
                # to run a copy)
                continue

            # prints a log message
            self.log("Moving resource file '%s' to '%s'" % (resource_file_path, new_resource_file_path))

            # in case the new resource directory path does not exist
            if not os.path.exists(new_resource_directory_path):
                # creates the new resource directory path (directories)
                os.makedirs(new_resource_directory_path)

            # in case the new resource file path already exists we're
            # in a presence of a "duplicate"
            if new_resource_file_path_exists:
                # "calculates" the relative path between the new resource file
                # path and the manager path
                new_resource_relative_path = os.path.relpath(new_resource_file_path, self.manager_path)

                # aligns the path replacing the backslashes with
                # "normal" slashes
                new_resource_relative_path = self.__align_path(new_resource_relative_path)

                # retrieves the number of times the file is "duplicated"
                duplicate_file_count = duplicate_files_structure.get(new_resource_relative_path, 0)

                # increments the duplicate count by one
                duplicate_file_count += 1

                # sets the duplicate file count in the duplicate files structure
                duplicate_files_structure[new_resource_relative_path] = duplicate_file_count

            # copies the resource file as the new resource file
            shutil.copy(resource_file_path, new_resource_file_path)

        # in case the sub type is plugin system
        if sub_type == PLUGIN_SYSTEM_VALUE:
            # deploys the plugin system package, using the current paths
            self.deploy_plugin_system_package(package_path, temporary_path)
        # in case the sub type is library
        elif sub_type == LIBRARY_VALUE:
            # deploys the library package, using the current paths
            self.deploy_library_package(package_path, temporary_path)
        # in case the sub type is configuration
        elif sub_type == CONFIGURATION_VALUE:
            # deploys the configuration package, using the current paths
            self.deploy_configuration_package(package_path, temporary_path)

        # persists the duplicates structure
        self._persist_duplicates_structure(duplicates_structure)

        # retrieves the container item key
        container_item_key = id

        # generates the hash digest map for the container file
        hash_digest_map = colony_crypt.generate_hash_digest_map(package_path)

        # creates the container item value
        container_item_value = {
            VERSION_VALUE : version,
            HASH_DIGEST_VALUE : hash_digest_map
        }

        # adds the container with the given key and value
        self._add_container_item(container_item_key, container_item_value)

        # creates the proper container file name from the id and version of the container
        # and then uses it in the copy of the package file into the registry
        container_file_name = id + "_" + version + COLONY_CONTAINER_FILE_EXTENSION
        shutil.copy(package_path, registry_path + "/containers/" + container_file_name)

    def deploy_plugin_system_package(self, package_path, temporary_path):
        """
        Deploys the given plugin system package, using the contents of the
        given temporary path.

        @type package_path: String
        @param package_path: The path to the package to be deployed.
        @type temporary_path: String
        @param temporary_path: The path to the temporary directory with
        the contents of the package.
        """

        # retrieves the target path
        target_path = os.path.normpath(self.manager_path)

        # creates the specification file path
        specification_file_path = os.path.normpath(temporary_path + "/" + SPECIFICATION_FILE_NAME)

        # opens the specification from the specification file path
        specification = self._open_specification(specification_file_path)

        # retrieves the id
        id = specification[ID_VALUE]

        # retrieves the version
        version = specification[VERSION_VALUE]

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # retrieves the keep resources
        keep_resources = specification.get(KEEP_RESOURCES_VALUE, [])

        # prints a log message
        self.log("Deploying plugin system package '%s' v'%s'" % (id, version))

        # prints a log message
        self.log("Moving resources from '%s' to '%s'" % (temporary_path, target_path))

        # iterates over all the resources
        for resource in resources:
            # checks if the current resource is of type
            # keep resource
            is_keep_resource = resource in keep_resources

            # retrieves the resource file path
            resource_file_path = os.path.normpath(temporary_path + "/resources/" + resource)

            # creates the new resource file path
            new_resource_file_path = os.path.normpath(target_path + "/" + resource)

            # retrieves the new resource directory path
            new_resource_directory_path = os.path.dirname(new_resource_file_path)

            # checks if the new resource file path already exists
            new_resource_file_path_exists = os.path.exists(new_resource_file_path)

            # in case the new resource file path exists
            # and the resource should be kept
            if new_resource_file_path_exists and is_keep_resource:
                # prints a log message
                self.log("Skipping resource file (keep) '%s'" % resource_file_path)

                # continues the loop (no need
                # to run a copy)
                continue

            # prints a log message
            self.log("Moving resource file '%s' to '%s'" % (resource_file_path, new_resource_file_path))

            # in case the new resource directory path does not exist
            if not os.path.exists(new_resource_directory_path):
                # creates the new resource directory path (directories)
                os.makedirs(new_resource_directory_path)

            # copies the resource file as the new resource file
            shutil.copy(resource_file_path, new_resource_file_path)

    def deploy_library_package(self, package_path, temporary_path):
        """
        Deploys the given library package, using the contents of the
        given temporary path.

        @type package_path: String
        @param package_path: The path to the package to be deployed.
        @type temporary_path: String
        @param temporary_path: The path to the temporary directory with
        the contents of the package.
        """

        # retrieves the target path
        target_path = os.path.normpath(self.manager_path + "/" + RELATIVE_LIBRARIES_PATH)

        # creates the specification file path
        specification_file_path = os.path.normpath(temporary_path + "/" + SPECIFICATION_FILE_NAME)

        # opens the specification from the specification file path
        specification = self._open_specification(specification_file_path)

        # retrieves the id
        id = specification[ID_VALUE]

        # retrieves the version
        version = specification[VERSION_VALUE]

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # retrieves the keep resources
        keep_resources = specification.get(KEEP_RESOURCES_VALUE, [])

        # prints a log message
        self.log("Deploying library package '%s' v'%s'" % (id, version))

        # prints a log message
        self.log("Moving resources from '%s' to '%s'" % (temporary_path, target_path))

        # iterates over all the resources
        for resource in resources:
            # checks if the current resource is of type
            # keep resource
            is_keep_resource = resource in keep_resources

            # retrieves the resource file path
            resource_file_path = os.path.normpath(temporary_path + "/resources/" + resource)

            # creates the new resource file path
            new_resource_file_path = os.path.normpath(target_path + "/" + resource)

            # retrieves the new resource directory path
            new_resource_directory_path = os.path.dirname(new_resource_file_path)

            # checks if the new resource file path already exists
            new_resource_file_path_exists = os.path.exists(new_resource_file_path)

            # in case the new resource file path exists
            # and the resource should be kept
            if new_resource_file_path_exists and is_keep_resource:
                # prints a log message
                self.log("Skipping resource file (keep) '%s'" % resource_file_path)

                # continues the loop (no need
                # to run a copy)
                continue

            # prints a log message
            self.log("Moving resource file '%s' to '%s'" % (resource_file_path, new_resource_file_path))

            # in case the new resource directory path does not exist
            if not os.path.exists(new_resource_directory_path):
                # creates the new resource directory path (directories)
                os.makedirs(new_resource_directory_path)

            # copies the resource file as the new resource file
            shutil.copy(resource_file_path, new_resource_file_path)

    def deploy_configuration_package(self, package_path, temporary_path):
        """
        Deploys the given configuration package, using the contents of the
        given temporary path.

        @type package_path: String
        @param package_path: The path to the package to be deployed.
        @type temporary_path: String
        @param temporary_path: The path to the temporary directory with
        the contents of the package.
        """

        # retrieves the target path
        target_path = os.path.normpath(self.manager_path + "/" + RELATIVE_CONFIGURATION_PATH)

        # creates the specification file path
        specification_file_path = os.path.normpath(temporary_path + "/" + SPECIFICATION_FILE_NAME)

        # opens the specification from the specification file path
        specification = self._open_specification(specification_file_path)

        # retrieves the id
        id = specification[ID_VALUE]

        # retrieves the version
        version = specification[VERSION_VALUE]

        # retrieves the configuration id
        configuration_id = specification[CONFIGURATION_ID_VALUE]

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # retrieves the keep resources
        keep_resources = specification.get(KEEP_RESOURCES_VALUE, [])

        # retrieves the target (exclusive) path to be used
        # uniquely by this container
        target_exclusive_path = os.path.normpath(target_path + "/" + configuration_id)

        # prints a log message
        self.log("Deploying configuration package '%s' v'%s'" % (id, version))

        # prints a log message
        self.log("Moving resources from '%s' to '%s'" % (temporary_path, target_exclusive_path))

        # iterates over all the resources
        for resource in resources:
            # checks if the current resource is of type
            # keep resource
            is_keep_resource = resource in keep_resources

            # retrieves the resource file path
            resource_file_path = os.path.normpath(temporary_path + "/resources/" + resource)

            # creates the new resource file path
            new_resource_file_path = os.path.normpath(target_exclusive_path + "/" + resource)

            # retrieves the new resource directory path
            new_resource_directory_path = os.path.dirname(new_resource_file_path)

            # checks if the new resource file path already exists
            new_resource_file_path_exists = os.path.exists(new_resource_file_path)

            # in case the new resource file path exists
            # and the resource should be kept
            if new_resource_file_path_exists and is_keep_resource:
                # prints a log message
                self.log("Skipping resource file (keep) '%s'" % resource_file_path)

                # continues the loop (no need
                # to run a copy)
                continue

            # prints a log message
            self.log("Moving resource file '%s' to '%s'" % (resource_file_path, new_resource_file_path))

            # in case the new resource directory path does not exist
            if not os.path.exists(new_resource_directory_path):
                # creates the new resource directory path (directories)
                os.makedirs(new_resource_directory_path)

            # copies the resource file as the new resource file
            shutil.copy(resource_file_path, new_resource_file_path)

    def remove_package(self, package_id, package_version = None):
        """
        Removes the package with the given id and version.
        The version is optional and may not be defined, in that
        case all the versions of the package are removed.

        @type package_id: String
        @param package_id: The id of the package to be removed.
        @type package_version: String
        @param package_version: The version of the package to be removed.
        """

        # prints a log message
        self.log("Removing '%s' from '%s'" % (package_id, self.manager_path), logging.INFO)

        # retrieves the packages structure
        packages = self._get_packages()

        # retrieves the installed packages
        installed_packages = packages.get(INSTALLED_PACKAGES_VALUE, {})

        # in case the package id is not found in the installed packages
        if not package_id in installed_packages:
            # raises a deployer exception
            raise colony_exceptions.DeployerException("package '%s' v'%s' is not installed" % (package_id, package_version))

        # retrieves the package (information) from the
        # installed packages
        package = installed_packages[package_id]

        # retrieves the type
        type = package[TYPE_VALUE]

        # in case the type is bundle
        if type == BUNDLE_VALUE:
            # removes the bundle package
            self.remove_bundle_package(package_id, package_version)
        # in case the type is plugin
        elif type == PLUGIN_VALUE:
            # removes the plugin package
            self.remove_plugin_package(package_id, package_version)
        # in case the type is container
        elif type == CONTAINER_VALUE:
            # removes the container package
            self.remove_container_package(package_id, package_version)
        # otherwise there is an error
        else:
            # raises a deployer exception
            raise colony_exceptions.DeployerException("invalid packaging type: %s" % type)

        # retrieves the package item key
        package_item_key = package_id

        # removes the package with the given key
        self._remove_package_item(package_item_key)

        # prints a log message
        self.log("Finished removing '%s' from'%s'" % (package_id, self.manager_path), logging.INFO)

    def remove_bundle_package(self, package_id, package_version):
        """
        Removes the bundle package with the given id and version.

        @type package_id: String
        @param package_id: The id of the bundle package to be removed.
        @type package_version: String
        @param package_version: The version of the bundle package to be removed.
        """

        # prints a log message
        self.log("Removing bundle package '%s' v'%s'" % (package_id, package_version))

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # retrieves the bundles structure
        bundles = self._get_bundles()

        # retrieves the installed bundles
        installed_bundles = bundles.get(INSTALLED_BUNDLES_VALUE, {})

        # in case the package id is not found in the installed bundles
        if not package_id in installed_bundles:
            # raises a deployer exception
            raise colony_exceptions.DeployerException("bundle '%s' v'%s' is not installed" % (package_id, package_version))

        # retrieves the bundle (information) from the
        # installed bundles
        bundle = installed_bundles[package_id]

        # sets the bundle id as the package id
        bundle_id = package_id

        # retrieves the bundle version as the as the package version
        # or from the bundle structure
        bundle_version = package_version or bundle[VERSION_VALUE]

        # creates the bundle file name from the bundle
        # id and version and uses it to create the full bundle path
        bundle_file_name = bundle_id + "_" + bundle_version + COLONY_BUNDLE_FILE_EXTENSION
        bundle_path = os.path.normpath(registry_path + "/" + RELATIVE_BUNDLES_PATH + "/" + bundle_file_name)

        # creates a new zip (manager)
        zip = colony_zip.Zip()

        # reads the specification file contents from the zip file
        specification_file_contents = zip.read(bundle_path, SPECIFICATION_FILE_NAME)

        # loads the json specification file contents
        specification = json.loads(specification_file_contents)

        # validates the specification
        self.validate_specification(specification)

        # retrieves the plugins
        plugins = specification.get(PLUGINS_VALUE, [])

        # retrieves the containers
        containers = specification.get(CONTAINERS_VALUE, [])

        # iterates over all the plugins
        for plugin in plugins:
            # retrieves the plugin id
            plugin_id = plugin[ID_VALUE]

            # retrieves the plugin version
            plugin_version = plugin[VERSION_VALUE]

            # removes the plugin with the given id
            self.remove_plugin_package(plugin_id, plugin_version)

            # retrieves the package item key
            package_item_key = plugin_id

            # remove the package with the given key
            self._remove_package_item(package_item_key)

        # iterates over all the containers
        for container in containers:
            # retrieves the container id
            container_id = container[ID_VALUE]

            # retrieves the container version
            container_version = container[VERSION_VALUE]

            # removes the container with the given id
            self.remove_container_package(container_id, container_version)

            # retrieves the package item key
            package_item_key = container_id

            # remove the package with the given key
            self._remove_package_item(package_item_key)

        # prints a log message
        self.log("Removing bundle file '%s'" % bundle_path)

        # removes the bundle file
        os.remove(bundle_path)

        # removes the bundle item
        self._remove_bundle_item(package_id)

    def remove_plugin_package(self, package_id, package_version):
        """
        Removes the plugin package with the given id and version.

        @type package_id: String
        @param package_id: The id of the plugin package to be removed.
        @type package_version: String
        @param package_version: The version of the plugin package to be removed.
        """

        # prints a log message
        self.log("Removing plugin package '%s' v'%s'" % (package_id, package_version))

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the plugins path
        plugins_path = os.path.normpath(self.manager_path + "/" + RELATIVE_PLUGINS_PATH)

        # retrieves the plugins structure
        plugins = self._get_plugins()

        # retrieves the installed plugins
        installed_plugins = plugins.get(INSTALLED_PLUGINS_VALUE, {})

        # in case the package id is not found in the installed plugins
        if not package_id in installed_plugins:
            # raises a deployer exception
            raise colony_exceptions.DeployerException("plugin '%s' v'%s' is not installed" % (package_id, package_version))

        # retrieves the plugin (information) from the
        # installed plugins
        plugin = installed_plugins[package_id]

        # sets the plugin id as the package id
        plugin_id = package_id

        # retrieves the plugin version as the package version
        # or from the plugin structure
        plugin_version = package_version or plugin[VERSION_VALUE]

        # creates the plugin file name from the plugin
        # id and version and uses it to create the full plugin path
        plugin_file_name = plugin_id + "_" + plugin_version + COLONY_PLUGIN_FILE_EXTENSION
        plugin_path = os.path.normpath(registry_path + "/" + RELATIVE_PLUGINS_PATH + "/" + plugin_file_name)

        # creates a new zip (manager)
        zip = colony_zip.Zip()

        # reads the specification file contents from the zip file
        specification_file_contents = zip.read(plugin_path, SPECIFICATION_FILE_NAME)

        # loads the json specification file contents
        specification = json.loads(specification_file_contents)

        # validates the specification
        self.validate_specification(specification)

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # retrieves the keep resources
        keep_resources = specification.get(KEEP_RESOURCES_VALUE, [])

        # retrieves the extra resources
        extra_resources = specification.get(EXTRA_RESOURCES_VALUE, [])

        # extends the resources list with the extra resources
        resources = [value for value in resources if not value in keep_resources]
        resources.extend(extra_resources)

        # creates the list of directory paths for (possible)
        # later removal
        directory_path_list = []

        # retrieves the duplicates structure (from file)
        duplicates_structure = self._get_duplicates_structure()

        # retrieves the duplicate files structure
        duplicate_files_structure = duplicates_structure.get(DUPLICATE_FILES_VALUE, {})

        # iterates over all the resources
        for resource in resources:
            # creates the (complete) resource file path
            resource_file_path = os.path.normpath(plugins_path + "/" + resource)

            # "calculates" the relative path between the resource file
            # path and the manager path
            resource_relative_path = os.path.relpath(resource_file_path, self.manager_path)

            # aligns the path replacing the backslashes with
            # "normal" slashes
            resource_relative_path = self.__align_path(resource_relative_path)

            # retrieves the number of times the file is "duplicated"
            duplicate_file_count = duplicate_files_structure.get(resource_relative_path, 0)

            # checks if the file should be removed
            remove_file = duplicate_file_count == 0

            # decrements the duplicate count by one
            duplicate_file_count -= 1

            # in case the duplicate file count is superior to zero
            if duplicate_file_count > 0:
                # sets the duplicate file count in the duplicate files structure
                duplicate_files_structure[resource_relative_path] = duplicate_file_count
            # otherwise in case the resource relative path reference
            # exists in the duplicate files structure
            elif resource_relative_path in duplicate_files_structure:
                # removes the resource relative path from the duplicate
                # files structure
                del duplicate_files_structure[resource_relative_path]

            # in case the remove file is not set
            if not remove_file:
                # prints a log message
                self.log("Skipping resource file (duplicate) '%s'" % resource_file_path)

                # continues the loop no need to remove a file that
                # is duplicated
                continue

            # in case the resource file path does not exists
            if not os.path.exists(resource_file_path):
                # prints a log message
                self.log("Skipping resource file '%s'" % resource_file_path)

                # continues the loop
                continue

            # prints a log message
            self.log("Removing resource file '%s'" % resource_file_path)

            # removes the resource file in the resource file path
            os.remove(resource_file_path)

            # retrieves the resource file directory path
            resource_file_directory_path = os.path.dirname(resource_file_path)

            # in case the resource file directory path is not yet
            # present in the directory path list
            if not resource_file_directory_path in directory_path_list:
                # adds the file directory path to the
                # directory path list
                directory_path_list.append(resource_file_directory_path)

        # persists the duplicates structure
        self._persist_duplicates_structure(duplicates_structure)

        # prints a log message
        self.log("Removing empty directories for plugin file '%s'" % plugin_path)

        # iterates over all the directory paths
        for directory_path in directory_path_list:
            # in case the directory path does not refers
            # a directory or in case it contains element
            if not os.path.isdir(directory_path) or os.listdir(directory_path):
                # continues the loop
                continue

            try:
                # removes the directories in the directory path
                os.removedirs(directory_path)
            except:
                # prints a log message
                self.log("Problem removing directory '%s'" % directory_path)

        # prints a log message
        self.log("Removing plugin file '%s'" % plugin_path)

        # removes the plugin file
        os.remove(plugin_path)

        # removes the plugin item
        self._remove_plugin_item(package_id)

    def remove_container_package(self, package_id, package_version):
        """
        Removes the container package with the given id and version.

        @type package_id: String
        @param package_id: The id of the container package to be removed.
        @type package_version: String
        @param package_version: The version of the container package to be removed.
        """

        # prints a log message
        self.log("Removing container package '%s' v'%s'" % (package_id, package_version))

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the containers path
        containers_path = os.path.normpath(self.manager_path + "/" + RELATIVE_CONTAINERS_PATH)

        # retrieves the containers structure
        containers = self._get_containers()

        # retrieves the installed containers
        installed_containers = containers.get(INSTALLED_CONTAINERS_VALUE, {})

        # in case the package id is not found in the installed containers
        if not package_id in installed_containers:
            # raises a deployer exception
            raise colony_exceptions.DeployerException("container '%s' v'%s' is not installed" % (package_id, package_version))

        # retrieves the container (information) from the
        # installed containers
        container = installed_containers[package_id]

        # sets the container id as the package id
        container_id = package_id

        # "calculates" the containers exclusive path to be used for unique usage
        containers_exclusive_path = os.path.normpath(containers_path + "/" + container_id)

        # retrieves the container version as the package version
        # or from the container structure
        container_version = package_version or container[VERSION_VALUE]

        # creates the container file name from the container
        # id and version and uses it to create the full container path
        container_file_name = container_id + "_" + container_version + COLONY_CONTAINER_FILE_EXTENSION
        container_path = os.path.normpath(registry_path + "/" + RELATIVE_CONTAINERS_PATH + "/" + container_file_name)

        # creates a new zip (manager)
        zip = colony_zip.Zip()

        # reads the specification file contents from the zip file
        specification_file_contents = zip.read(container_path, SPECIFICATION_FILE_NAME)

        # loads the json specification file contents
        specification = json.loads(specification_file_contents)

        # validates the specification
        self.validate_specification(specification)

        # retrieves the sub type
        sub_type = specification[SUB_TYPE_VALUE]

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # retrieves the keep resources
        keep_resources = specification.get(KEEP_RESOURCES_VALUE, [])

        # retrieves the extra resources
        extra_resources = specification.get(EXTRA_RESOURCES_VALUE, [])

        # extends the resources list with the extra resources
        resources = [value for value in resources if not value in keep_resources]
        resources.extend(extra_resources)

        # creates the list of directory paths for (possible)
        # later removal
        directory_path_list = []

        # retrieves the duplicates structure (from file)
        duplicates_structure = self._get_duplicates_structure()

        # retrieves the duplicate files structure
        duplicate_files_structure = duplicates_structure.get(DUPLICATE_FILES_VALUE, {})

        # iterates over all the resources
        for resource in resources:
            # creates the (complete) resource file path
            resource_file_path = os.path.normpath(containers_exclusive_path + "/" + resource)

            # "calculates" the relative path between the resource file
            # path and the manager path
            resource_relative_path = os.path.relpath(resource_file_path, self.manager_path)

            # aligns the path replacing the backslashes with
            # "normal" slashes
            resource_relative_path = self.__align_path(resource_relative_path)

            # retrieves the number of times the file is "duplicated"
            duplicate_file_count = duplicate_files_structure.get(resource_relative_path, 0)

            # checks if the file should be removed
            remove_file = duplicate_file_count == 0

            # decrements the duplicate count by one
            duplicate_file_count -= 1

            # in case the duplicate file count is superior to zero
            if duplicate_file_count > 0:
                # sets the duplicate file count in the duplicate files structure
                duplicate_files_structure[resource_relative_path] = duplicate_file_count
            # otherwise in case the resource relative path reference
            # exists in the duplicate files structure
            elif resource_relative_path in duplicate_files_structure:
                # removes the resource relative path from the duplicate
                # files structure
                del duplicate_files_structure[resource_relative_path]

            # in case the remove file is not set
            if not remove_file:
                # prints a log message
                self.log("Skipping resource file (duplicate) '%s'" % resource_file_path)

                # continues the loop no need to remove a file that
                # is duplicated
                continue

            # in case the resource file path does not exists
            if not os.path.exists(resource_file_path):
                # prints a log message
                self.log("Skipping resource file '%s'" % resource_file_path)

                # continues the loop
                continue

            # prints a log message
            self.log("Removing resource file '%s'" % resource_file_path)

            # removes the resource file in the resource file path
            os.remove(resource_file_path)

            # retrieves the resource file directory path
            resource_file_directory_path = os.path.dirname(resource_file_path)

            # in case the resource file directory path is not yet
            # present in the directory path list
            if not resource_file_directory_path in directory_path_list:
                # adds the file directory path to the
                # directory path list
                directory_path_list.append(resource_file_directory_path)

        # in case the sub type is plugin system
        if sub_type == PLUGIN_SYSTEM_VALUE:
            # removes the plugin system package
            self.remove_plugin_system_package(package_id, package_version, specification)
        # in case the sub type is library
        elif sub_type == LIBRARY_VALUE:
            # removes the library package
            self.remove_library_package(package_id, package_version, specification)
        # in case the sub type is configuration
        elif sub_type == CONFIGURATION_VALUE:
            # removes the configuration package
            self.remove_configuration_package(package_id, package_version, specification)

        # persists the duplicates structure
        self._persist_duplicates_structure(duplicates_structure)

        # prints a log message
        self.log("Removing empty directories for container file '%s'" % container_path)

        # iterates over all the directory paths
        for directory_path in directory_path_list:
            # in case the directory path does not refers
            # a directory or in case it contains element
            if not os.path.isdir(directory_path) or os.listdir(directory_path):
                # continues the loop
                continue

            try:
                # removes the directories in the directory path
                os.removedirs(directory_path)
            except:
                # prints a log message
                self.log("Problem removing directory '%s'" % directory_path)

        # prints a log message
        self.log("Removing container file '%s'" % container_path)

        # removes the container file
        os.remove(container_path)

        # removes the container item
        self._remove_container_item(package_id)

    def remove_plugin_system_package(self, package_id, package_version, specification):
        """
        Removes the plugin system package with the given id and version.

        @type package_id: String
        @param package_id: The id of the plugin system package to be removed.
        @type package_version: String
        @param package_version: The version of the plugin system package to be removed.
        """

        # prints a log message
        self.log("Removing plugin system package '%s' v'%s'" % (package_id, package_version))

        # creates the plugin system path
        plugin_system_path = os.path.normpath(self.manager_path)

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # retrieves the keep resources
        keep_resources = specification.get(KEEP_RESOURCES_VALUE, [])

        # retrieves the extra resources
        extra_resources = specification.get(EXTRA_RESOURCES_VALUE, [])

        # extends the resources list with the extra resources
        resources = [value for value in resources if not value in keep_resources]
        resources.extend(extra_resources)

        # creates the list of directory paths for (possible)
        # later removal
        directory_path_list = []

        # iterates over all the resources
        for resource in resources:
            # creates the (complete) resource file path
            resource_file_path = os.path.normpath(plugin_system_path + "/" + resource)

            # in case the resource file path does not exists
            if not os.path.exists(resource_file_path):
                # prints a log message
                self.log("Skipping resource file '%s'" % resource_file_path)

                # continues the loop
                continue

            # prints a log message
            self.log("Removing resource file '%s'" % resource_file_path)

            # removes the resource file in the resource file path
            os.remove(resource_file_path)

            # retrieves the resource file directory path
            resource_file_directory_path = os.path.dirname(resource_file_path)

            # in case the resource file directory path is not yet
            # present in the directory path list
            if not resource_file_directory_path in directory_path_list:
                # adds the file directory path to the
                # directory path list
                directory_path_list.append(resource_file_directory_path)

        # prints a log message
        self.log("Removing empty directories for plugin system file")

        # iterates over all the directory paths
        for directory_path in directory_path_list:
            # in case the directory path does not refers
            # a directory or in case it contains element
            if not os.path.isdir(directory_path) or os.listdir(directory_path):
                # continues the loop
                continue

            try:
                # removes the directories in the directory path
                os.removedirs(directory_path)
            except:
                # prints a log message
                self.log("Problem removing directory '%s'" % directory_path)

    def remove_library_package(self, package_id, package_version, specification):
        """
        Removes the library package with the given id and version.

        @type package_id: String
        @param package_id: The id of the library package to be removed.
        @type package_version: String
        @param package_version: The version of the library package to be removed.
        """

        # prints a log message
        self.log("Removing library package '%s' v'%s'" % (package_id, package_version))

        # creates the libraries path
        libraries_path = os.path.normpath(self.manager_path + "/" + RELATIVE_LIBRARIES_PATH)

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # retrieves the keep resources
        keep_resources = specification.get(KEEP_RESOURCES_VALUE, [])

        # retrieves the extra resources
        extra_resources = specification.get(EXTRA_RESOURCES_VALUE, [])

        # extends the resources list with the extra resources
        resources = [value for value in resources if not value in keep_resources]
        resources.extend(extra_resources)

        # creates the list of directory paths for (possible)
        # later removal
        directory_path_list = []

        # iterates over all the resources
        for resource in resources:
            # creates the (complete) resource file path
            resource_file_path = os.path.normpath(libraries_path + "/" + resource)

            # in case the resource file path does not exists
            if not os.path.exists(resource_file_path):
                # prints a log message
                self.log("Skipping resource file '%s'" % resource_file_path)

                # continues the loop
                continue

            # prints a log message
            self.log("Removing resource file '%s'" % resource_file_path)

            # removes the resource file in the resource file path
            os.remove(resource_file_path)

            # retrieves the resource file directory path
            resource_file_directory_path = os.path.dirname(resource_file_path)

            # in case the resource file directory path is not yet
            # present in the directory path list
            if not resource_file_directory_path in directory_path_list:
                # adds the file directory path to the
                # directory path list
                directory_path_list.append(resource_file_directory_path)

        # prints a log message
        self.log("Removing empty directories for library file")

        # iterates over all the directory paths
        for directory_path in directory_path_list:
            # in case the directory path does not refers
            # a directory or in case it contains element
            if not os.path.isdir(directory_path) or os.listdir(directory_path):
                # continues the loop
                continue

            try:
                # removes the directories in the directory path
                os.removedirs(directory_path)
            except:
                # prints a log message
                self.log("Problem removing directory '%s'" % directory_path)

    def remove_configuration_package(self, package_id, package_version, specification):
        """
        Removes the configuration package with the given id and version.

        @type package_id: String
        @param package_id: The id of the configuration package to be removed.
        @type package_version: String
        @param package_version: The version of the configuration package to be removed.
        """

        # prints a log message
        self.log("Removing configuration package '%s' v'%s'" % (package_id, package_version))

        # creates the configuration path
        configuration_path = os.path.normpath(self.manager_path + "/" + RELATIVE_CONFIGURATION_PATH)

        # retrieves the configuration id
        configuration_id = specification.get(CONFIGURATION_ID_VALUE, [])

        # retrieves the resources
        resources = specification[RESOURCES_VALUE]

        # retrieves the keep resources
        keep_resources = specification.get(KEEP_RESOURCES_VALUE, [])

        # retrieves the extra resources
        extra_resources = specification.get(EXTRA_RESOURCES_VALUE, [])

        # "calculates" the configuration exclusive path to be used for unique usage
        configuration_exclusive_path = os.path.normpath(configuration_path + "/" + configuration_id)

        # extends the resources list with the extra resources
        resources = [value for value in resources if not value in keep_resources]
        resources.extend(extra_resources)

        # creates the list of directory paths for (possible)
        # later removal
        directory_path_list = []

        # iterates over all the resources
        for resource in resources:
            # creates the (complete) resource file path
            resource_file_path = os.path.normpath(configuration_exclusive_path + "/" + resource)

            # in case the resource file path does not exists
            if not os.path.exists(resource_file_path):
                # prints a log message
                self.log("Skipping resource file '%s'" % resource_file_path)

                # continues the loop
                continue

            # prints a log message
            self.log("Removing resource file '%s'" % resource_file_path)

            # removes the resource file in the resource file path
            os.remove(resource_file_path)

            # retrieves the resource file directory path
            resource_file_directory_path = os.path.dirname(resource_file_path)

            # in case the resource file directory path is not yet
            # present in the directory path list
            if not resource_file_directory_path in directory_path_list:
                # adds the file directory path to the
                # directory path list
                directory_path_list.append(resource_file_directory_path)

        # prints a log message
        self.log("Removing empty directories for library file")

        # iterates over all the directory paths
        for directory_path in directory_path_list:
            # in case the directory path does not refers
            # a directory or in case it contains element
            if not os.path.isdir(directory_path) or os.listdir(directory_path):
                # continues the loop
                continue

            try:
                # removes the directories in the directory path
                os.removedirs(directory_path)
            except:
                # prints a log message
                self.log("Problem removing directory '%s'" % directory_path)

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
                # raises a deployer exception
                raise colony_exceptions.DeployerException("required value '%s' missing in specification file" % (required_value))

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
        description = specification.get("description", "")
        author = specification.get("author", "")
        capabilities = specification.get("capabilities", [])
        capabilities_allowed = specification.get("capabilities_allowed", [])
        dependencies = specification.get("dependencies", [])
        main_file = specification.get("main_file", None)
        resources = specification.get("resources", [])

        # prints the various values
        self.print_value("Platform", platform)
        self.print_value("Sub-Platforms", sub_platforms)
        self.print_value("Id", id)
        self.print_value("Name", name)
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

    def _unzip_package(self, package_path):
        """
        Unzips (unpacks) the package in the given package path
        to a generated temporary path.

        @type package_path: String
        @param package_path: The path to the package to be unpacked.
        @rtype: String
        @return: The generated temporary path for the package contents.
        """

        # creates a new temporary path
        temporary_path = tempfile.mkdtemp()

        # in case the package path does not exist
        if not os.path.exists(package_path):
            # raises a deployer exception
            raise colony_exceptions.DeployerException("the package path '%s' does not exist" % package_path)

        # prints a log message
        self.log("Unpacking package file '%s' using zip decoder" % (package_path))

        # creates a new zip (manager)
        zip = colony_zip.Zip()

        # unzips the package to the temporary path
        zip.unzip(package_path, temporary_path)

        # returns the temporary path
        return temporary_path

    def _open_specification(self, specification_file_path):
        """
        Opens and interprets the specification file in the given
        file path.
        The returned value is a map containing the specification.

        @type specification_file_path: String
        @param specification_file_path: The specification file path.
        @rtype: Dictionary
        @return: The map containing the specification.
        """

        # prints a log message
        self.log("Opening specification file '%s'" % (specification_file_path))

        # reads the specification file contents
        specification_file_contents = colony_file.read_file(specification_file_path)

        # loads the json specification file contents
        specification = json.loads(specification_file_contents)

        # validates the specification
        self.validate_specification(specification)

        # returns the specification
        return specification

    def _touch_structure(self, structure):
        """
        Touches the structure, updating the timestamp
        references present in it.

        @type structure: Dictionary
        @param structure: The structure to be update with with
        new timestamps.
        """

        # retrieves the current time
        current_time = time.time()

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # formats the current date time
        current_date_time_formated = current_date_time.strftime("%d-%m-%Y %H:%M:%S")

        # updates the structure map with the current time
        # and date time values
        structure[LAST_MODIFIED_TIMESTAMP_VALUE] = current_time
        structure[LAST_MODIFIED_DATE_VALUE] = current_date_time_formated

    def _get_packages(self):
        """
        Retrieves the packages structure.

        @rtype: Dictionary
        @return: The retrieved bundles structure.
        """

        return self.__get_structure(PACKAGES_FILE_NAME)

    def _get_bundles(self):
        """
        Retrieves the bundles structure.

        @rtype: Dictionary
        @return: The retrieved bundles structure.
        """

        return self.__get_structure(BUNDLES_FILE_NAME)

    def _get_plugins(self):
        """
        Retrieves the plugins structure.

        @rtype: Dictionary
        @return: The retrieved plugins structure.
        """

        return self.__get_structure(PLUGINS_FILE_NAME)

    def _get_containers(self):
        """
        Retrieves the containers structure.

        @rtype: Dictionary
        @return: The retrieved containers structure.
        """

        return self.__get_structure(CONTAINERS_FILE_NAME)

    def _add_package_item(self, item_key, item_value, update_time = True):
        """
        Adds a package item to the packages file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, update_time, PACKAGES_FILE_NAME, INSTALLED_PACKAGES_VALUE)

    def _add_bundle_item(self, item_key, item_value, update_time = True):
        """
        Adds a bundle item to the bundles file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, update_time, BUNDLES_FILE_NAME, INSTALLED_BUNDLES_VALUE)

    def _add_plugin_item(self, item_key, item_value, update_time = True):
        """
        Adds a plugin item to the plugins file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, update_time, PLUGINS_FILE_NAME, INSTALLED_PLUGINS_VALUE)

    def _add_container_item(self, item_key, item_value, update_time = True):
        """
        Adds a container item to the containers file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, update_time, CONTAINERS_FILE_NAME, INSTALLED_CONTAINERS_VALUE)

    def _remove_package_item(self, item_key):
        """
        Removes a package item from the packages file structure.

        @type item_key: String
        @param item_key: The key to the item to be removed.
        """

        self.__remove_structure_item(item_key, PACKAGES_FILE_NAME, INSTALLED_PACKAGES_VALUE)

    def _remove_bundle_item(self, item_key):
        """
        Removes a bundle item from the bundles file structure.

        @type item_key: String
        @param item_key: The key to the item to be removed.
        """

        self.__remove_structure_item(item_key, BUNDLES_FILE_NAME, INSTALLED_BUNDLES_VALUE)

    def _remove_plugin_item(self, item_key):
        """
        Removes a plugin item from the bundles file structure.

        @type item_key: String
        @param item_key: The key to the item to be removed.
        """

        self.__remove_structure_item(item_key, PLUGINS_FILE_NAME, INSTALLED_PLUGINS_VALUE)

    def _remove_container_item(self, item_key):
        """
        Removes a container item from the bundles file structure.

        @type item_key: String
        @param item_key: The key to the item to be removed.
        """

        self.__remove_structure_item(item_key, CONTAINERS_FILE_NAME, INSTALLED_CONTAINERS_VALUE)

    def _get_duplicates_structure(self):
        """
        Retrieves the duplicates structure from the file system.

        @rtype: Dictionary
        @return: The duplicates structure retrieved from the
        file system.
        """

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.normpath(registry_path + "/" + DUPLICATES_FILE_NAME)

        # reads the structure file contents
        structure_file_contents = colony_file.read_file(structure_file_path)

        # loads the structure file contents from json
        structure = json.loads(structure_file_contents)

        # returns the structure
        return structure

    def _persist_duplicates_structure(self, duplicates_structure):
        """
        Persists the given duplicates structure into
        the file system.

        @type duplicates_structure: Dictionary
        @param duplicates_structure: The duplicates structure to be
        persisted into the file system.
        """

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.normpath(registry_path + "/" + DUPLICATES_FILE_NAME)

        # touches the duplicates structure (internal structure)
        # updating the dates in it
        self._touch_structure(duplicates_structure)

        # serializes the structure
        structure_serialized = json.dumps(duplicates_structure)

        # writes the structure file contents
        colony_file.write_file(structure_file_path, structure_serialized)

    def __get_structure(self, structure_file_name):
        """
        Retrieves the structure from the structure file.

        @type structure_file_name: String
        @param structure_file_name: The name of the structure file to be used.
        @rtype: Dictionary
        @return: The structure retrieved from the structure file.
        """

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.normpath(registry_path + "/" + structure_file_name)

        # reads the structure file contents
        structure_file_contents = colony_file.read_file(structure_file_path)

        # loads the structure file contents from json
        structure = json.loads(structure_file_contents)

        # returns the structure
        return structure

    def __add_structure_item(self, item_key, item_value, update_time, structure_file_name, structure_key_name):
        """
        Adds a new structure item to an existing structures file.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        @type structure_file_name: String
        @param structure_file_name: The name of the structure file to be used.
        @type structure_key_name: String
        @param structure_key_name: The key to the structure base item.
        """

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.normpath(registry_path + "/" + structure_file_name)

        # reads the structure file contents
        structure_file_contents = colony_file.read_file(structure_file_path)

        # loads the structure file contents from json
        structure = json.loads(structure_file_contents)

        # retrieves the installed structure
        installed_structure = structure.get(structure_key_name, {})

        # in case the update time flag is set
        if update_time:
            # retrieves the current time
            current_time = time.time()

            # sets the item value
            item_value[TIMESTAMP_VALUE] = current_time

        # sets the installed structure map
        installed_structure[item_key] = item_value

        # touches the structure (internal structure)
        # updating the dates in it
        self._touch_structure(structure)

        # serializes the structure
        structure_serialized = json.dumps(structure)

        # writes the structure file contents
        colony_file.write_file(structure_file_path, structure_serialized)

    def __remove_structure_item(self, item_key, structure_file_name, structure_key_name):
        """
        Removes a structure item from an existing structures file.

        @type item_key: String
        @param item_key: The key to the item to be removed.
        @type structure_file_name: String
        @param structure_file_name: The name of the structure file to be used.
        @type structure_key_name: String
        @param structure_key_name: The key to the structure base item.
        """

        # retrieves the registry path
        registry_path = os.path.normpath(self.manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.normpath(registry_path + "/" + structure_file_name)

        # reads the structure file contents
        structure_file_contents = colony_file.read_file(structure_file_path)

        # loads the structure file contents from json
        structure = json.loads(structure_file_contents)

        # retrieves the installed structure
        installed_structure = structure.get(structure_key_name, {})

        # in case the item key is not present in the
        # installed structure
        if not item_key in installed_structure:
            # raises a deployer exception
            raise colony_exceptions.DeployerException("item key '%s' does not exist" % item_key)

        # removes the item from the installed structure
        del installed_structure[item_key]

        # touches the structure (internal structure)
        # updating the dates in it
        self._touch_structure(structure)

        # serializes the structure
        structure_serialized = json.dumps(structure)

        # writes the structure file contents
        colony_file.write_file(structure_file_path, structure_serialized)

    def __align_path(self, path):
        """
        Aligns the given path, converting all the system specific
        characters into the defined virtual separators.
        The retrieved path is system independent.

        @type path: String
        @param path: The path to the aligned (become system independent).
        @rtype: String
        @return: The aligned path (system independent).
        """

        # aligns the path replacing the backslashes with
        # "normal" slashes
        aligned_path = path.replace("\\", "/")

        # returns the aligned path
        return aligned_path
