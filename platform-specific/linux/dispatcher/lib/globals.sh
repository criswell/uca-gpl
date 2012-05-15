# Global variables to be used by the client agent

#######################
# PATH settings
# (if not already set)
#######################
if [ -z "$BASE_DIR" ]; then
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
    POSTINST_DIR=$INSTALL_DIR/postinst
fi

###################
# UID/GID settings
###################

INSTALL_UID="eil"
INSTALL_GID="eil"

####################################
# Basic logging and error reporting
####################################

# Note that these will be inside the home directory as defined
# elsewhere
STANDARD_LOG_FILE="${HOME_DIR}/client-agent-base.log"
CCMS_LOG_FILE="${HOME_DIR}/ccms-agent.log"
ERROR_LOG_FILE="${HOME_DIR}/client-agent-error.log"
PID_FILE="${HOME_DIR}/client-agent.pid"

###############################
# Communication layer settings
###############################

# Note that, again, these will be inside the home directory as
# defined elsewhere
COMMAND_DIR="${HOME_DIR}/commands"

# The URL for the release directory
URL_RELEASE="http://eilauto01/EILUCA/"

# vim:set ai et sts=4 sw=4 tw=80:
