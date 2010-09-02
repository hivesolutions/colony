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

def main():
    # adds the default path to the system path
    sys.path.insert(0, os.path.normpath(os.path.realpath(DEFAULT_PATH_VALUE + "/../lib")))

    target_path = os.path.normpath(os.path.realpath(DEFAULT_PATH_VALUE + "/../../colony/plugins"))

    import colony_zip

    zip = colony_zip.Zip()

    zip.unzip(sys.argv[1], target_path)

    try:
        specification_file = open(target_path + "/specification.json")

        try:
            specification_contents = specification_file.read()
        finally:
            # closes the specification file
            specification_file.close()

        # loads the json specification file
        specification = json.loads(specification_contents)

        # retrieves the main file
        main_file = specification["main_file"]

        i, _b = os.path.splitext(main_file)

        new_specification_file = target_path + "/" + i + ".json"

        # renames the specification file
        os.rename(target_path + "/specification.json", new_specification_file)

    except Exception, exception:
        print str(exception)
        os.remove(target_path + "/specification.json")

    # 1. vejo qual e o manager path a ter respeito
    # 2. faço unpack do zip que la esta no cpx para o directorio do manager_path/colony/plugins
    # 3. renomear o specification.json para nome_do_ficheiro_principal.json

if __name__ == "__main__":
    main()
