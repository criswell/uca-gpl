#!/bin/sh

# The XenClient host replacer init script
# ---------------------------------------
# This script restores the hosts file on XenClient on reboot

# LSB install information
### BEGIN INIT INFO
# Provides:             xen_host_replace
# Required-Start:
# Required-Stop:
# Default-Start:        1 2 3 4 5 6
# Default-Stop:
# Short-Description:    The XenClient host replacer init script
### END INIT INFO

# Make sure we have an appropriate path
PATH="${PATH}:/usr/bin"

clean_hosts_file() {
    local TMP_FILE=`mktemp /tmp/eil-XXXXXX`
    sed '/## EIL_BEGIN/,/## EIL_END/d' /etc/hosts > ${TMP_FILE}
    cp -f ${TMP_FILE} /etc/hosts
    rm -f ${TMP_FILE}
}

# Append to the hosts
append_hosts() {
    cat /opt/intel/eil/clientagent/home/xen_hosts >> /etc/hosts
}

case "$1" in
start|restart|try-restart|reload|force-reload)
    # Just in case
    clean_hosts_file
    append_hosts

    exit 0
    ;;
stop)
    # We do nothing

    exit 0
    ;;
status)
    STAT=$(sed '/## EIL_BEGIN/,/## EIL_END/!d' /etc/hosts)
    if [ -n "$STAT" ]; then
        echo "Hosts file is ready for client agent"
    else
        echo "Hosts file is not ready for client agent!"
        echo "Client agent is broken! Please run this init script with 'start'"
        echo "option!"
    fi
    exit 0
    ;;
*)
    # Display usage options
    echo "Usage: /etc/init.d/eil_steward.sh {start|stop|status}"

    exit 0
    ;;
esac

exit 0

# vim:set ai et sts=4 sw=4 tw=80:
