#!/bin/sh

# The nmsa_handler init script
# ----------------------------
# The aim of this script is to be as platform agnostic as possible

# LSB install information
### BEGIN INIT INFO
# Provides:             nmsa_handler
# Required-Start:       $remote_fs $syslog $network $time
# Required-Stop:        $remote_fs $syslog $network $time
# Default-Start:        2 3 4 5
# Default-Stop:
# Short-Description:    The NMSA Handler daemon
### END INIT INFO

# RHEL information
# chkconfig: 2345 80 20
# description: The NMSA Handler daemon

# Make sure we have an appropriate path (this shouldn't be necessary, but
# just to be safe on all platforms)
PATH="${PATH}:/usr/bin"

NMSA_TOGGLE="/opt/intel/eil/clientagent/home/.nmsa_enable"

NMSA_HANDLER="/opt/intel/eil/clientagent/bin/nmsa_handler.py"

. /opt/intel/eil/clientagent/lib/helper.sh
. /opt/intel/eil/clientagent/lib/globals.sh

check_nmsa_capable() {
    if [ -e "${NMSA_TOGGLE}" ] && [ -e "${NMSA_HANDLER}" ]; then
        # The system is capable
        return 0
    else
        # The system is not capable
        return 3
    fi
}

check_ipmi_running() {
    _FOUND=1
    for I in $(seq 0 10)
    do
        if [ -c "/dev/ipmi${I}" ]; then
            _FOUND=0
        fi
    done

    if [ "$_FOUND" -eq "1" ]; then
        if [ -n "$IS_RHEL" ] || [ -n "$IS_SLES" ]; then
            if [ -e "/etc/init.d/ipmi" ]; then
                /etc/init.d/ipmi start
            fi
        elif [ -n "$IS_DEB" ] || [ -n "$IS_ANGSTROM" ]; then
            if [ -e "/etc/init.d/ipmievd" ]; then
                /etc/init.d/ipmievd start
            fi
        else
            # Undefined thing! This is very very bad!
            trace "nmsa_handler.sh (init): Undefined or unsupported distro... failing..."
        fi
    fi
}

check_nmsa_handler_running() {
    if [ -e "/opt/intel/eil/clientagent/home/nmsa_handler.pid" ]; then
        # Verify that it's already running
        local PID1=$(cat /opt/intel/eil/clientagent/home/nmsa_handler.pid)
        if [ -d "/proc/${PID1}" ]; then
            # It's running
            return 0
        else
            # It's not running, we have a dangling PID file
            return 1
        fi
    else
        # It's not running
        return 3
    fi
}

# First, verify we are a system capable of running nmsa
check_nmsa_capable
_STATUS=$?
if [ "${_STATUS}" -eq "0" ]; then
    case "$1" in
    start)
        check_ipmi_running
        # Start the handler daemon
        check_nmsa_handler_running
        _STATUS=$?
        if [ "${_STATUS}" -eq "0" ]; then
            # According to the LSB, this is considered a success
            echo "nmsa_handler already running!"
            echo "If you think this is a mistake, check the pid file and"
            echo "associated process..."
        elif [ "${_STATUS}" -eq "1" ]; then
            # Daemon is not running, but pid file exists, let's kill old file
            # and restart
            rm -f /opt/intel/eil/clientagent/home/nmsa_handler.pid
            $NMSA_HANDLER start
        else
            # Okay to start
            $NMSA_HANDLER start
        fi

        exit 0
        ;;
    stop)
        # Stop the handler daemon
        check_nmsa_handler_running
        _STATUS=$?
        if [ "${_STATUS}" -eq "0" ]; then
            $NMSA_HANDLER stop
        elif [ "${_STATUS}" -eq "1" ]; then
            # Daemon is not running, but pid file exists
            rm -f /opt/intel/eil/clientagent/home/nmsa_handler.pid
        else
            echo "nmsa_handler is not running."
        fi

        exit 0
        ;;
    restart|try-restart|reload|force-reload)
        check_ipmi_running
        # Restart the handler daemon
        check_nmsa_handler_running
        _STATUS=$?
        if [ "${_STATUS}" -eq "0" ]; then
            $NMSA_HANDLER restart
        elif [ "${_STATUS}" -eq "1" ]; then
            # Daemon is not running, but pid file exists
            rm -f /opt/intel/eil/clientagent/home/nmsa_handler.pid
            $NMSA_HANDLER start
        else
            # Wasn't running, just restart
            $NMSA_HANDLER start
        fi

        exit 0
        ;;
    status)
        # Display status
        check_nmsa_handler_running
        _STATUS=$?
        if [ "${_STATUS}" -eq "0" ]; then
            # It's running
            PID1=$(cat /opt/intel/eil/clientagent/home/nmsa_handler.pid)
            echo "nmsa_handler start/running, process ${PID1}"
        elif [ "${_STATUS}" -eq "1" ]; then
            echo "nmsa_handler not running, pid file exists"
        else
            echo "nmsa_handler not running"
        fi

        exit $_STATUS
        ;;
    *)
        # Display usage options
        echo "Usage: /etc/init.d/nmsa_handler.sh {start|stop|status|restart}"

        exit 0
        ;;
    esac
fi

# If not capable, we just silently pass

exit 0

# vim:set ai et sts=4 sw=4 tw=80:
