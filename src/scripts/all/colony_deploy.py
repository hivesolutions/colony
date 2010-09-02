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

__revision__ = "$LastChangedRevision: 9911 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-08-30 11:04:12 +0100 (seg, 30 Ago 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import json

DEFAULT_PATH_VALUE = os.path.dirname(os.path.realpath(__file__))
""" The default path """

def update_path():
    # adds the default path to the system path
    sys.path.insert(0, os.path.normpath(os.path.realpath(DEFAULT_PATH_VALUE + "/../lib")))

def main():
    import colony_zip

    # creates the target path
    target_path = os.path.normpath(os.path.realpath(DEFAULT_PATH_VALUE + "/../../colony/plugins"))

    # creates the specification file path
    specification_file_path = target_path + "/specification.json"

    # retrieves the package path
    package_path = sys.argv[1]

    # creates a new zip (manager)
    zip = colony_zip.Zip()

    # unzips the package to the target path
    zip.unzip(package_path, target_path)

    try:
        # opens the specification file
        specification_file = open(specification_file_path)

        try:
            # reads the specification file, retrieving the contents
            specification_file_contents = specification_file.read()
        finally:
            # closes the specification file
            specification_file.close()

        # loads the json specification file contents
        specification = json.loads(specification_file_contents)

        # retrieves the main file
        main_file = specification["main_file"]

        # splits the main file name into name and extension
        main_file_name, _mail_file_extension = os.path.splitext(main_file)

        # creates the new specification file path
        new_specification_file_path = target_path + "/" + main_file_name + ".json"

        # renames the specification file
        os.rename(specification_file_path, new_specification_file_path)
    except:
        # removes the specification file
        os.remove(target_path + "/specification.json")

    # 1. vejo qual e o manager path a ter respeito
    # 2. faço unpack do zip que la esta no cpx para o directorio do manager_path/colony/plugins
    # 3. renomear o specification.json para nome_do_ficheiro_principal.json

if __name__ == "__main__":
    main()
