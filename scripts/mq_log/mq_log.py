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

# creates the context and the socket
# to be able to communicate with the server
context = zmq.Context()
socket = context.socket(zmq.SUB)

USAGE = "Help:\n\
--help[-h] - prints this message\n\
--host[-h]=(HOSTNAME:PORT) - sets the hostname for the connection to be created\n\
--plugin[-p]=(PLUGIN_1,PLUGIN_2) - sets a plugin wildcard based filter on the log\n\
--level[-l]=(PLUGIN_1,PLUGIN_2) - sets a level wildcard based filter on the log\n"
""" The usage string for the command line arguments """

def usage():
    print "Supports wildcards...."

try:
    options, _args = getopt.getopt(sys.argv[1:], "h:p:l:", ["host=", "plugin=", "level="])
except getopt.GetoptError, error:
    # prints the error description
    print str(error)

    # prints usage information
    usage()

    # exits in error
    sys.exit(2)

host = "localhost:5600"
plugins = None
levels = None

for option, value in options:
    if option in ("-h", "--host"):
        host = value
    elif option in ("-p", "--plugin"):
        plugins = [value.strip() for value in value.split(",")]
    elif option in ("-l", "--levels"):
        levels = [value.strip() for value in value.split(",")]

print "Starting logging updates for colony"
socket.connect ("tcp://" + host)
socket.setsockopt(zmq.SUBSCRIBE, "colony")

while True:
    # receives a string from the socket and splits it to retrieve
    # the header and the value from it, then splits the value again
    # to retrieve the various components of it
    string = socket.recv()
    header, value = string.split(" ", 1)
    data, time, level, plugin, thread, message = value.split(" ", 5)

    level = level.strip("[]")
    plugin = plugin.strip("[]")

    if plugins and not [value for value in plugins if fnmatch.fnmatch(plugin, value)]: continue
    if levels and not [value for value in levels if fnmatch.fnmatch(level, value)]: continue
    print "[%s]" % level, message
