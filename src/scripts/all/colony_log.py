#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import zmq
import sys
import fnmatch
import getopt

VERSION = "${out value=colony_version /}"
""" The version value """

RELEASE = "${out value=release_version /}"
""" The release value """

BUILD = "${out value=build_version /}"
""" The build value """

RELEASE_DATE = "${out value=date /}"
""" The release date value """

USAGE = "Help:\n\
--help[-h] - prints this message\n\
--host[-h]=(HOSTNAME:PORT) - sets the hostname for the connection to be created\n\
--plugin[-p]=(PLUGIN_1,PLUGIN_2) - sets a plugin wildcard based filter on the log\n\
--level[-l]=(PLUGIN_1,PLUGIN_2) - sets a level wildcard based filter on the log\n"
""" The usage string for the command line arguments """

BRANDING_TEXT = "Hive Colony Log %s (Hive Solutions Lda. r%s:%s %s)"
""" The branding text value """

VERSION_PRE_TEXT = "Python "
""" The version pre text value """

def print_information():
    """
    Prints the system information for the command line.
    The printed information should simulate the normal
    copyright and version information present in many
    unix based commands.
    """

    # print both the branding information text
    # and the version information
    print BRANDING_TEXT % (VERSION, RELEASE, BUILD, RELEASE_DATE)
    print VERSION_PRE_TEXT + sys.version

def usage():
    """
    Prints the usage for the command line.
    """

    print USAGE

def main():
    try:
        # processes the arguments options
        options, _args = getopt.getopt(sys.argv[1:], "h:p:l:", ["host=", "plugin=", "level="])
    except getopt.GetoptError, error:
        # prints the error description
        print str(error)

        # prints usage information
        usage()

        # exits in error
        sys.exit(2)

    # starts the default values for the host the
    # plugins and the (debug) levels
    host = "localhost:5600"
    plugins = None
    levels = None

    # iterates over all the options
    for option, value in options:
        if option in ("-h", "--host"):
            host = value
        elif option in ("-p", "--plugin"):
            plugins = [value.strip() for value in value.split(",")]
        elif option in ("-l", "--levels"):
            levels = [value.strip() for value in value.split(",")]

    # prints the console information
    print_information()

    # creates the context and the socket
    # to be able to communicate with the server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    # connects to the defined host, and sets the proper
    # subscription options (only listen to colony messages)
    socket.connect("tcp://" + host)
    socket.setsockopt(zmq.SUBSCRIBE, "colony")

    # iterates continuously to print the received log messages
    # when receiving them (application loop)
    while True:
        # receives the string (message) from the socket then splits
        # it around the first value (removes the header) and then
        # unpacks it around it's major values
        string = socket.recv()
        _header, value = string.split(" ", 1)
        date, time, level, plugin, thread, message = value.split(" ", 5)

        # retrieves the appropriate level and plugin values
        # without the surrounding brace values
        level = level.strip("[]")
        plugin = plugin.strip("[]")

        # checks both the current plugin value and the current level
        # value against the previously defined "filters" in case they
        # match the values (wildcard matching) print the log entry
        if plugins and not [value for value in plugins if fnmatch.fnmatch(plugin, value)]: continue
        if levels and not [value for value in levels if fnmatch.fnmatch(level, value)]: continue
        print "%s %s [%s] [%s] %s %s" % (date, time, level, plugin, thread, message)

if __name__ == "__main__":
    # runs the main
    main()
