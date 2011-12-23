#!/usr/bin/env sh

# xen_test.sh
# -----------
# Test script to determine if the system should run the xen post install
# scripts

# THIS MUST ONLY BE RUN BY THE DISPATCHER INSTALL SCRIPT

# Load our libraries
. /opt/intel/eil/clientagent/lib/helper.sh
. /opt/intel/eil/clientagent/lib/globals.sh

if [ -n "$IS_ANGSTROM" ]; then
    # verify we're specifically xenclient
    if [ "$PLATFORM_NAME" -eq "xenclient" ]; then
        exit 0
    else
        exit 1
    fi
else
    exit 1
fi

# vim:set ai et sts=4 sw=4 tw=80:
