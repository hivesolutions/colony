#!/bin/sh
#
# colony        This starts and stops colony
#
# chkconfig: 2345 11 88
# description: This starts the Colony Plugin System, \
#              which runs a modular system in python.
#
# processname: /sbin/colony
# config: /etc/sysconfig/auditd
# config: /etc/colony/colony.conf
# pidfile: /var/run/colony.pid
#
# Return values according to LSB for all commands but status:
# 0 - success
# 1 - generic or unspecified error
# 2 - invalid or excess argument(s)
# 3 - unimplemented feature (e.g. "reload")
# 4 - insufficient privilege
# 5 - program is not installed
# 6 - program is not configured
# 7 - program is not running
#

PATH=/sbin:/bin:/usr/bin:/usr/sbin
prog="auditd"

# source function library
. /etc/init.d/functions

# allow anyone to run status
if [ "$1" = "status" ] ; then
    status $prog
    RETVAL=$?
    exit $RETVAL
fi

# checks that we are root... so non-root users stop here
test $EUID = 0 || exit 4

# check config
test -f /etc/sysconfig/auditd && . /etc/sysconfig/auditd

RETVAL=0

start(){
    test -x /sbin/auditd  || exit 5
    test -f /etc/audit/auditd.conf  || exit 6

    echo -n $"Starting $prog: "

# Localization for auditd is controlled in /etc/synconfig/auditd
    if [ -z "$AUDITD_LANG" -o "$AUDITD_LANG" = "none" -o "$AUDITD_LANG" = "NONE" ]; then
        unset LANG LC_TIME LC_ALL LC_MESSAGES LC_NUMERIC LC_MONETARY LC_COLLATE
    else
        LANG="$AUDITD_LANG"
        LC_TIME="$AUDITD_LANG"
        LC_ALL="$AUDITD_LANG"
        LC_MESSAGES="$AUDITD_LANG"
        LC_NUMERIC="$AUDITD_LANG"
        LC_MONETARY="$AUDITD_LANG"
        LC_COLLATE="$AUDITD_LANG"
        export LANG LC_TIME LC_ALL LC_MESSAGES LC_NUMERIC LC_MONETARY LC_COLLATE
    fi
    unset HOME MAIL USER USERNAME
    daemon $prog "$EXTRAOPTIONS"
    RETVAL=$?
    echo
    if test $RETVAL = 0 ; then
        touch /var/lock/subsys/auditd
        # Load the default rules
        test -f /etc/audit/audit.rules && /sbin/auditctl -R /etc/audit/audit.rules >/dev/null
    fi
    return $RETVAL
}

stop(){
    echo -n $"Stopping $prog: "
    killproc $prog
    RETVAL=$?
    echo
    rm -f /var/lock/subsys/auditd
    # Remove watches so shutdown works cleanly
    if test x"$AUDITD_CLEAN_STOP" != "x" ; then
        if test "`echo $AUDITD_CLEAN_STOP | tr 'NO' 'no'`" != "no"
        then
            /sbin/auditctl -D >/dev/null
        fi
    fi
    if test x"$AUDITD_STOP_DISABLE" != "x" ; then
        if test "`echo $AUDITD_STOP_DISABLE | tr 'NO' 'no'`" != "no"
        then
            /sbin/auditctl -e 0 >/dev/null
        fi
    fi
    return $RETVAL
}

reload(){
    test -f /etc/audit/auditd.conf  || exit 6
    echo -n $"Reloading configuration: "
    killproc $prog -HUP
    RETVAL=$?
    echo
    return $RETVAL
}

rotate(){
    echo -n $"Rotating logs: "
    killproc $prog -USR1
    RETVAL=$?
    echo
    return $RETVAL
}

resume(){
    echo -n $"Resuming logging: "
    killproc $prog -USR2
    RETVAL=$?
    echo
    return $RETVAL
}

restart(){
    test -f /etc/audit/auditd.conf  || exit 6
    stop
    start
}

condrestart(){
    [ -e /var/lock/subsys/auditd ] && restart
    return 0
}


# See how we were called.
case "$1" in
    start)
    start
    ;;
    stop)
    stop
    ;;
    restart)
    restart
    ;;
    reload)
    reload
    ;;
    rotate)
    rotate
    ;;
    resume)
    resume
    ;;
    condrestart)
    condrestart
    ;;
    *)
    echo $"Usage: $0 {start|stop|status|restart|condrestart|reload|rotate|resume}"
    RETVAL=3
esac

exit $RETVAL
