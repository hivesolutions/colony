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
import time
import threading

DEFAULT_TIMEOUT = 60
""" The default timeout value """

DEFAULT_SLEEP_TIME = 0.5
""" The default sleep time """

loop_flag = True
""" The flag that controls the loop """

def check_daemon_file(daemon_file_path, target_pid):
    try:
        # in case the daemon file does not exist
        if not os.path.exists(daemon_file_path):
            # returns false (invalid)
            return False

        # opens the daemon file
        file = open(daemon_file_path)

        try:
            # reads the file contents
            contents = file.read()
        finally:
            # closes the file
            file.close()

        # in case the contents of the file are
        # the target pid contents
        if contents == target_pid:
            # returns true (valid)
            return True

        # returns false (invalid)
        return False
    except:
        # returns false (invalid)
        return False

def cancel_loop():
    # sets the loop flag as global
    global loop_flag

    # unsets the loop flag
    loop_flag = False

def main():
    # retrieves the arguments length
    arguments_length = len(sys.argv)

    # in case the argument length is insufficient
    if arguments_length < 3:
        # prints a message
        print "Insufficient arguments (required 3)"

        # exits in error
        exit(1)

    # retrieves the daemon file path
    daemon_file_path = sys.argv[1]

    # retrieves the target pid
    target_pid = sys.argv[2]

    # in case the number of arguments is bigger than three
    if arguments_length > 3:
        # retrieves the target timeout (converting to integer)
        target_timeout = int(sys.argv[3])
    else:
        # sets the default timeout as the target timeout
        target_timeout = DEFAULT_TIMEOUT

    # creates the timer for canceling of the loop
    timer = threading.Timer(target_timeout, cancel_loop)

    # starts the timer
    timer.start()

    try:
        # iterates continuously
        while loop_flag:
            # checks the daemon file
            if check_daemon_file(daemon_file_path, target_pid):
                # prints a message
                print "Valid daemon file found, removing file and exiting"

                # removes the daemon file
                os.remove(daemon_file_path)

                # prints a message
                print "Exiting"

                # cancels the timer
                timer.cancel()

                # exits in success
                exit(0)

            # sleeps for a while
            time.sleep(DEFAULT_SLEEP_TIME)

        # prints a message
        print "Timeout (%ss) reached without valid daemon file" % str(target_timeout)

        # cancels the timer
        timer.cancel()

        # exits in error
        exit(2)
    except Exception, exception:
        # prints a message
        print "Exception raised (%s), exiting in error" % unicode(exception)

        # cancels the timer
        timer.cancel()

        # exits in error
        exit(1)

if __name__ == "__main__":
    main()
