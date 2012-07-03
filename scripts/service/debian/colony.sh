#!/bin/sh
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

# __author__    = Luís Martinho <lmartinho@hive.pt> & João Magalhães <joamag@hive.pt>
# __version__   = 1.0.0
# __revision__  = $LastChangedRevision$
# __date__      = $LastChangedDate$
# __copyright__ = Copyright (c) 2008-2012 Hive Solutions Lda.
# __license__   = GNU General Public License (GPL), Version 3

### BEGIN INIT INFO
# Provides:          colony
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Colony initscript
# Description:       Starts or stops the hive colony framework service.
### END INIT INFO

# Author: Luís Martinho <lmartinho@hive.pt>

# sets the path variables
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="Colony Service daemon"
NAME=colony_wrapper
DAEMON=/usr/local/sbin/$NAME
DAEMON_ARGS=""
PIDFILE=/var/run/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME

# exits in case the package is not installed
[ -x "$DAEMON" ] || exit 0

# reads the configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# loads the verbose setting and other rcS variables
. /lib/init/vars.sh

# defines lsb log_* functions
. /lib/lsb/init-functions

# overrides the verbose setting
VERBOSE=yes

# Function that starts the daemon/service.
do_start() {
    # returns
    #   0 if daemon has been started
    #   1 if daemon was already running
    #   2 if daemon could not be started

    # in case the pid file already exists
    if [ -e $PIDFILE ]; then
        return 1
    fi

    # tests the daemonn to check if it is already running
    start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON --test > /dev/null || return 1

    # touches the pid file to lock the starting process
    touch $PIDFILE

    # launches the daemon and checks if it was successful
    start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON -- $DAEMON_ARGS || (rm -f $PIDFILE && return 2)

    # returns valid
    return 0
}

# Function that stops the daemon/service.
do_stop() {
    # returns
    #   0 if daemon has been stopped
    #   1 if daemon was already stopped
    #   2 if daemon could not be stopped
    #   other if a failure occurred

    # stops the daemon
    start-stop-daemon --stop --quiet --retry=TERM/30/KILL/5 --pidfile $PIDFILE

    # sets the retval with the return value
    RETVAL="$?"

    # in case the return value is two (not stopped), returns immediately
    [ "$RETVAL" = 2 ] && return 2

    # Waits for children to finish too if this is a daemon that forks
    # and if the daemon is only ever run from this initscript.
    # If the above conditions are not satisfied then adds some other code
    # that waits for the process to drop all resources that could be
    # needed by services started subsequently. A last resort is to
    # sleep for some time.
    start-stop-daemon --stop --quiet --oknodo --retry=0/30/KILL/5 --exec $DAEMON

    # in case the return value is two (not stopped), returns immediately
    [ "$?" = 2 ] && return 2

    # removes the pid file, many daemons don't delete their pidfiles when they exit
    rm -f $PIDFILE

    # returns the return value
    return "$RETVAL"
}

# Function that sends a SIGHUP to the daemon/service.
do_reload() {
    # in case the daemon can reload its configuration without
    # restarting (for example, when it is sent a SIGHUP), then implement that here
    start-stop-daemon --stop --signal 1 --quiet --pidfile $PIDFILE --name $NAME

    # returns valid
    return 0
}

# switches over the service option
case "$1" in
    start)
        # prints a log message
        [ "$VERBOSE" != no ] && log_daemon_msg "Starting $DESC" "$NAME"

        # calls the do start function
        do_start
        case "$?" in
            0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
            2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
        esac
        ;;
    stop)
        [ "$VERBOSE" != no ] && log_daemon_msg "Stopping $DESC" "$NAME"

        # call the do stop function
        do_stop

        case "$?" in
            0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
            2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
        esac
        ;;
    restart|force-reload)
        # prints a log message
        log_daemon_msg "Restarting $DESC" "$NAME"

        # calls the do stop function
        do_stop

        case "$?" in
              0|1)
                do_start
                case "$?" in
                    0) log_end_msg 0 ;;
                    1) log_end_msg 1 ;; # old process is still running
                    *) log_end_msg 1 ;; # failed to start
                esac
                ;;
              *)
                # failed to stop
                log_end_msg 1
                ;;
        esac
        ;;
    *)
        # prints the usage message
        echo "Usage: $SCRIPTNAME {start|stop|restart|force-reload}" >&2

        # exits
        exit 3
        ;;
esac
:
