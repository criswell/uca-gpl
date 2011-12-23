#!/bin/sh

# The eil_steward init script
# ---------------------------
# The aim of this script is to be as platform agnostic as possible

# LSB install information
### BEGIN INIT INFO
# Provides:             eil_steward
# Required-Start:       $remote_fs $syslog $network $time
# Required-Stop:        $remote_fs $syslog $network $time
# Default-Start:        2 3 4 5
# Default-Stop:
# Short-Description:    The EIL Linux Client Agent steward
### END INIT INFO

# RHEL information
# chkconfig: 2345 80 20
# description: The EIL Linux Client Agent steward

# Make sure we have an appropriate path (this shouldn't be necessary, but
# just to be safe on all platforms)
PATH="${PATH}:/usr/bin"

BIN_STEWARD="/opt/intel/eil/clientagent/bin/eil_steward"

check_steward_running() {
    if [ -e "/opt/intel/eil/clientagent/home/client-agent.pid" ]; then
        # Verify that it's already running
        local PID1=$(cat /opt/intel/eil/clientagent/home/client-agent.pid)
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

case "$1" in
start)
    # Start the steward service
    check_steward_running
    _STATUS=$?
    if [ "${_STATUS}" -eq "0" ]; then
        # According to the LSB, this is considered a success
        echo "eil_steward already running!"
        echo "If you think this is a mistake, check the pid file and"
        echo "associated process..."
    elif [ "${_STATUS}" -eq "1" ]; then
        # Service is not running, but pid file exists, let's kill old file
        # and restart
        rm -f /opt/intel/eil/clientagent/home/client-agent.pid
        $BIN_STEWARD
    else
        # Okay to start
        $BIN_STEWARD
    fi

    exit 0
    ;;
stop)
    # Stop the steward service
    check_steward_running
    _STATUS=$?
    if [ "${_STATUS}" -eq "0" ]; then
        # Send it SIGHUP
        PID1=$(cat /opt/intel/eil/clientagent/home/client-agent.pid)
        kill -1 ${PID1}
    elif [ "${_STATUS}" -eq "1" ]; then
        # Service is not running, but pid file exists
        rm -f /opt/intel/eil/clientagent/home/client-agent.pid
    else
        echo "eil_steward is not running."
    fi

    exit 0
    ;;
restart|try-restart|reload|force-reload)
    # Restart the steward service
    check_steward_running
    _STATUS=$?
    if [ "${_STATUS}" -eq "0" ]; then
        # Send it SIGHUP
        PID1=$(cat /opt/intel/eil/clientagent/home/client-agent.pid)
        kill -1 ${PID1}

        # Give it a bit to stop what it was doing
        sleep 5
        $BIN_STEWARD
    elif [ "${_STATUS}" -eq "1" ]; then
        # Service is not running, but pid file exists
        rm -f /opt/intel/eil/clientagent/home/client-agent.pid
        $BIN_STEWARD
    else
        # Wasn't running, just restart
        $BIN_STEWARD
    fi

    exit 0
    ;;
status)
    # Display status
    check_steward_running
    _STATUS=$?
    if [ "${_STATUS}" -eq "0" ]; then
        # It's running
        PID1=$(cat /opt/intel/eil/clientagent/home/client-agent.pid)
        echo "eil_steward start/running, process ${PID1}"
    elif [ "${_STATUS}" -eq "1" ]; then
        echo "eil_steward not running, pid file exists"
    else
        echo "eil_steward not running"
    fi

    exit $_STATUS
    ;;
asset)
    # Issue SIGUSR1 to refresh asset information
    check_steward_running
    _STATUS=$?
    if [ "${_STATUS}" -eq "0" ]; then
        # Send it SIGUSR1
        PID1=$(cat /opt/intel/eil/clientagent/home/client-agent.pid)
        kill -10 ${PID1}
        echo "eil_steward has been sent SIGUSR1 to refresh asset info"
    else
        # it's not running
        echo "eil_steward not running"
    fi

    exit 0
    ;;
*)
    # Display usage options
    echo "Usage: /etc/init.d/eil_steward.sh {start|stop|status|restart|asset}"

    exit 0
    ;;
esac

exit 0

# vim:set ai et sts=4 sw=4 tw=80: