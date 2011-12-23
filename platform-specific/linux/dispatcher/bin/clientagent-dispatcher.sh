#!/usr/bin/env sh

# Client agent base dispatcer (Bash prototype)
# --------------------------------------------
# This base takes commands that have already been parsed by another
# application and executes them based up certain criteria. It is
# intended to be fairly lean and require a minimal amount of external
# dependencies (e.g., it should run on a wide variety of platforms with
# minimal additional dependency installation)
#
# Please see the associated INSTALL and README files for more
# information

unset DEBUG || true

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

EXEC=clientagent-base.sh

BIN_DIR=$INSTALL_DIR/bin
LIB_DIR=$INSTALL_DIR/lib
DOC_DIR=$INSTALL_DIR/doc
TOOL_DIR=$INSTALL_DIR/tools
HOME_DIR=$INSTALL_DIR/home
SCRIPTS_DIR=$INSTALL_DIR/scripts

# Load our libraries
. $LIB_DIR/helper.sh
. $LIB_DIR/globals.sh
. $LIB_DIR/dispatcher.sh

# Set up our temp files and interfaces
if [ "$TMP_DIR" = "" ]; then
    TMP_DIR="/tmp/clientagent."
    TMP_DIR=${TMP_DIR}$(date +%j%H%M%S)
fi

if [ ! -f "$STANDARD_LOG_FILE" ]; then
    touch $STANDARD_LOG_FILE
fi

if [ ! -f "$ERROR_LOG_FILE" ]; then
    touch $ERROR_LOG_FILE
fi

if [ ! -d "$COMMAND_DIR" ]; then
    mkdir -p $COMMAND_DIR
    if [ ! -d "$COMMAND_DIR" ]; then
        echo "Cannot create command directory $COMMAND_DIR!"
        echo "Check permissions and installation!"
        exit 1
    fi
fi

trace "clientagent-dispatcher called"

# Get the available commands
COMMANDS=`ls -t $COMMAND_DIR`

for COMMAND in $COMMANDS
do
    trace "Executing command '${COMMAND}' as UID:${UID} with EUID:${EUID}"
    # Get rid of the command pending processing
    rm -f ${COMMAND_DIR}/${COMMAND}

    process_command "$COMMAND"
done

# vim:set ai et sts=4 sw=4 tw=80:
