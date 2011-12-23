#!/usr/bin/env sh

# Client Agent Helper Script
#----------------------------
# This tool is a helper script intended to bridge the gap between the
# dispatcher and the steward. It fills in the steward with specific
# information that the dispatcher will know about.
#
# The main advantage of storing this information in the dispatcher is
# that changing it involves updating simple bash scripts and will not
# require a recompile of the steward agent.

unset DUMP_BASE DUMP_INSTALL DUMP_BIN DUMP_LIB DUMP_DOC DUMP_PID || true
unset DUMP_TOOL DUMP_HOME DUMP_SCRIPTS DUMP_COMDIR DUMP_UID DUMP_SYSID || true
unset DUMP_GID DUMP_STDLOG DUMP_CCMSLOG DUMP_ERRLOG TMPFILE DUMP_PLATFORM || true

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

usage()
{
    cat <<EOF
Usage: $PROGNAME [OPTION] TMPFILE
Where [OPTION] is one of the following

    --base          Returns the base directory used by client agent

    --install       Returns the base install directory used by client
                    agent

    --bin           Returns the binary directory used by client agent

    --lib           Returns the library directory used by client agent

    --doc           Returns the documentation directory used by client
                    agent

    --tool          Returns the tools directory used by client agent

    --home          Returns the home directory used by client agent

    --scripts       Returns the scripts directory used by client agent

    --comdir        Returns the command directory used by client agent

    --uid           Returns the UID used by client agent

    --gid           Returns the GID used by client agent

    --stdlog        Returns the path to the standard log used by client
                    agent

    --ccmslog       Returns the path to the CCMS log used by client agent

    --errlog        Returns the path to the error log used by client agent

    --pidfile       Returns the path to the process ID file used by the client
                    agent

    --sysid         Returns the system identification tag.

    --platform      Returns the platform name.

If ran without any options, this usage text will be displayed.
EOF
}

if [ "$1" = "" ]; then
    usage
    exit 0
fi

if [ -n "$IS_ESX" ] || [ -n "$IS_SLES" ]; then
    # ESXi lacks getopt, and SLES /bin/sh interacts strangely with getopt, so
    # we just do this kludge and hope for the best
    TEMP="$* --"
else
    # Parse command line.
    TEMP=$(getopt -n "$PROGNAME" --options h \
--longoptions base,\
install,\
bin,\
lib,\
doc,\
tool,\
home,\
scripts,\
comdir,\
uid,\
gid,\
stdlog,\
ccmslog,\
pidfile,\
sysid,\
platform,\
errlog -- $*)

    if [ $? -ne 0 ]; then
        echo "Error while parsing options!"
        usage
        exit 1
    fi
fi

eval set -- "$TEMP"

while [ $1 != -- ]; do
    case "$1" in
        ## Directory options
        --base)
            DUMP_BASE=yes
            shift
            ;;
        --install)
            DUMP_INSTALL=yes
            shift
            ;;
        --bin)
            DUMP_BIN=yes
            shift
            ;;
        --lib)
            DUMP_LIB=yes
            shift
            ;;
        --doc)
            DUMP_DOC=yes
            shift
            ;;
        --tool)
            DUMP_TOOL=yes
            shift
            ;;
        --home)
            DUMP_HOME=yes
            shift
            ;;
        --scripts)
            DUMP_SCRIPTS=yes
            shift
            ;;
        --comdir)
            DUMP_COMDIR=yes
            shift
            ;;
        ## UID/GID options
        --uid)
            DUMP_UID=yes
            shift
            ;;
        --gid)
            DUMP_GID=yes
            shift
            ;;
        ## Log options
        --stdlog)
            DUMP_STDLOG=yes
            shift
            ;;
        --ccmslog)
            DUMP_CCMSLOG=yes
            shift
            ;;
        --errlog)
            DUMP_ERRLOG=yes
            shift
            ;;
        --pidfile)
            DUMP_PID=yes
            shift
            ;;
        --sysid)
            DUMP_SYSID=yes
            shift
            ;;
        --platform)
            DUMP_PLATFORM=yes
            shift
            ;;
        -h)
            usage
            exit 0
            ;;
        *)
            break
            ;;
    esac
done
shift

if [ -n "$1" ]; then
    TMPFILE=$1
fi

# Define our trace function
trace () {
    if [ -n "$TMPFILE" ]; then
        echo -n "$*" >> ${TMPFILE}
    else
        echo -n "$*"
    fi
}

# This is only ugly because we want to allow for stacked options, I'm
# not 100% sold that we should allow for this, but may as well since it's
# a minimal effort- Sam
if [ -n "$DUMP_BASE" ]; then
    trace "$BASE_DIR"
fi

if [ -n "$DUMP_BIN" ]; then
    trace "$BIN_DIR"
fi

if [ -n "$DUMP_CCMSLOG" ]; then
    trace "$CCMS_LOG_FILE"
fi

if [ -n "$DUMP_COMDIR" ]; then
    trace "$COMMAND_DIR"
fi

if [ -n "$DUMP_DOC" ]; then
    trace "$DOC_DIR"
fi

if [ -n "$DUMP_ERRLOG" ]; then
    trace "$ERROR_LOG_FILE"
fi

if [ -n "$DUMP_GID" ]; then
    trace "$INSTALL_GID"
fi

if [ -n "$DUMP_HOME" ]; then
    trace "$HOME_DIR"
fi

if [ -n "$DUMP_INSTALL" ]; then
    trace "$INSTALL_DIR"
fi

if [ -n "$DUMP_LIB" ]; then
    trace "$LIB_DIR"
fi

if [ -n "$DUMP_SCRIPTS" ]; then
    trace "$SCRIPTS_DIR"
fi

if [ -n "$DUMP_STDLOG" ]; then
    trace "$STANDARD_LOG_FILE"
fi

if [ -n "$DUMP_TOOL" ]; then
    trace "$TOOL_DIR"
fi

if [ -n "$DUMP_UID" ]; then
    trace "$INSTALL_UID"
fi

if [ -n "$DUMP_PID" ]; then
    trace "$PID_FILE"
fi

if [ -n "$DUMP_SYSID" ]; then
    # Messy
    if [ -n "$IS_DEB" ]; then
        trace "DEB"
    elif [ -n "$IS_RHEL" ]; then
        trace "RHEL"
    elif [ -n "$IS_ESX" ]; then
        trace "ESX"
    elif [ -n "$IS_SLES" ]; then
        trace "SLES"
    elif [ -n "$IS_ANGSTROM" ]; then
        trace "ANGSTROM"
    fi
fi

if [ -n "$DUMP_PLATFORM" ]; then
    trace "$PLATFORM_NAME"
fi

# vim:set ai et sts=4 sw=4 tw=80:
