#!/usr/bin/env sh

# noinit_test.sh
# --------------
# Very simple test to determine if we're installing on a system that should not
# have the init scripts added to boot.

# THIS MUST ONLY BE RUN BY THE DISPATCHER INSTALL SCRIPT

# Load our libraries
. /opt/intel/eil/clientagent/lib/helper.sh
. /opt/intel/eil/clientagent/lib/globals.sh

if [ -f "/etc/ca_toggles/no_init" ]; then
    exit 0
else
    exit 1
fi

# vim:set ai et sts=4 sw=4 tw=80:
