#!/usr/bin/env sh

# noinit_setup.sh
# ---------------
# On systems where the noinit toggle has been set, we disable the init scripts
# which previously had been enabled for the client agent.

# Load our libraries
. /opt/intel/eil/clientagent/lib/helper.sh
. /opt/intel/eil/clientagent/lib/globals.sh

# THIS MUST ONLY BE RUN BY THE DISPATCHER INSTALL SCRIPT

disable_init() {
    trace "noinit_setup- Disabling the init scripts"

    # uninstall the rc files
    if [ -n "$IS_RHEL" ]; then
        /etc/init.d/eil_steward.sh stop
        chkconfig --del eil_steward.sh
    elif [ -n "$IS_DEB" ] || [ -n "$IS_ANGSTROM" ]; then
        /etc/init.d/eil_steward.sh stop
        update-rc.d -f eil_steward.sh remove
    elif [ -n "$IS_SLES" ]; then
        /etc/init.d/eil_steward.sh stop
        /usr/lib/lsb/remove_initd /etc/init.d/eil_steward.sh
    elif [ -n "$IS_ESX" ]; then
        /etc/init.d/eil_steward.sh stop
        rm -f /etc/rc.local.d/eil_steward.sh
    elif [ -n "$IS_SLACK" ]; then
        /etc/init.d/eil_steward.sh stop
        rm -f /etc/rc.d/rc3.d/S99eil_steward.sh
        rm -f /etc/rc.d/rc3.d/K99eil_steward.sh
    else
        trace_error "noinit_setup- Could not identify distribution! Nothing done!"
    fi
}

disable_init

# vim:set ai et sts=4 sw=4 tw=80:
