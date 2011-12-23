#!/usr/bin/env sh

# Linux Client Agent Update Checker
#----------------------------------
# This tool periodically checks against the upstream source for updates, and
# upgrades the system if they exist.

PROGNAME=${0##*/}

# Set up the installation directories

# We use /opt for our installation location to adhere to LSB Linux
# Filesystem Hierarchy Standards (this gives us maximum compatibility
# across the various distros we aim to support).
BASE_DIR=/opt

# Intel has a registered provider name with the LSB
LANANA=$BASE_DIR/intel

# We want to have our own sub-directory under that specific to the
# EIL namespace, additionally, we want our client agent to live there.
if [ "$BOOTSTRAP_DIR" = "" ]; then
    INSTALL_DIR=$LANANA/eil/clientagent
else
    INSTALL_DIR=$BOOTSTRAP_DIR
fi

BIN_DIR=$INSTALL_DIR/bin
LIB_DIR=$INSTALL_DIR/lib
DOC_DIR=$INSTALL_DIR/doc
TOOL_DIR=$INSTALL_DIR/tools
HOME_DIR=$INSTALL_DIR/home
SCRIPTS_DIR=$INSTALL_DIR/scripts

. ${LIB_DIR}/globals.sh
. ${LIB_DIR}/helper.sh

EIL_VERSION=$(cat ${LIB_DIR}/VERSION)

TMP_WORKSPACE=`mktemp -d /tmp/eil-XXXXXX`

cd $TMP_WORKSPACE

wget -q "${URL_RELEASE}/VERSION.txt"

EIL_UPDATE_VERSION=$(cat ${TMP_WORKSPACE}/VERSION.txt)

if [ "$EIL_UPDATE_VERSION" != "$EIL_VERSION" ]; then
    trace "Update available - Old version '${EIL_VERSION}', New version '${EIL_UPDATE_VERSION}'"
    trace "Attempting to fetch update..."
    # Update available
    wget -q "${URL_RELEASE}/clientagent-bootstrap.sh"
    chmod a+x clientagent-bootstrap.sh
    ./clientagent-bootstrap.sh
    rm -fr ${TMP_WORKSPACE}
fi

exit 0

# vim:set ai et sts=4 sw=4 tw=80:
