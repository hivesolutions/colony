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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 9712 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-08-10 13:42:37 +0100 (ter, 10 Ago 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

import main

USAGE = "Usage: plugin_id:method [argument1[%type1]$argument2[%type2] ...]\n\
Executes an execution command in the colony plugin manager"
""" The usage string for the command line arguments """

def usage():
    """
    Prints the usage for the command line.
    """

    print USAGE

if __name__ == "__main__":
    # in case the number of arguments is invalid
    if len(sys.argv) < 2:
        # prints the description of the error
        print str("Error: Invalid number of arguments (see --help)")

        # exits in error
        sys.exit(2)

    if sys.argv[1] == "--help":
        # prints usage information
        usage()

        # exits in error
        sys.exit(2)

    # retrieves the command joining the last part of the command line
    command = " ".join(sys.argv[1:])

    # sets the new argument values
    sys.argv = [sys.argv[0]]

    # adds the silent option
    sys.argv.append("--silent")

    # adds the execution command
    sys.argv.append("--execution_command=" + command)

    # calls the main function
    main.main()
