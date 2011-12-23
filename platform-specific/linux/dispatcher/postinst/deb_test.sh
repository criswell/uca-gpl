#!/usr/bin/env sh

# deb_test.sh
# -----------
# Very simple test to see if we are installing on a Debian-derived distribution
# (such as Ubuntu, Linux Mint, etc, or even vanilla Debian).

# THIS MUST ONLY BE RUN BY THE DISPATCHER INSTALL SCRIPT

# Load our libraries
. /opt/intel/eil/clientagent/lib/helper.sh
. /opt/intel/eil/clientagent/lib/globals.sh

if [ -n "$IS_DEB" ]; then
    exit 0
else
    exit 1
fi

# vim:set ai et sts=4 sw=4 tw=80:
