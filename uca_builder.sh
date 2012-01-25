#!/usr/bin/env sh

# Unified Client Agent Release Builder
# ------------------------------------
# Currently, this is Linux-specific, meaning to build the unified agent you
# must build it under Linux. The reason for this is because, under Linux, the
# unified agent depends upon the script elevator, which is a binary that must
# be statically built on a Linux-machine.
#
# The goal of this release builder, however, is to generate a release file
# that will work on both Windows and Linux

# FIXME currently this is very hackish

unset LOG_FILE || true

PROGNAME=${0##*/}

MY_CWD=`pwd`

###########################################################
# Convenience defintions for the various bash color prompts
###########################################################
COLOR_RESET='\e[0m'
COLOR_TRACE='\e[0;34m' # Blue
COLOR_WARNING='\e[1;33m' # Yellow
COLOR_ALERT='\e[4;31m' # Underline red
COLOR_DIE='\e[30m\033[41m' # Red background, black text

#################
# Trace functions
#################
inner_trace () {
    if [ -n "$LOG_FILE" ]; then
        echo -e "$(date) $*" >> ${LOG_FILE}
    else
        echo -e "$*"
    fi
}

warning () {
    if [ -n "$LOG_FILE" ]; then
        inner_trace "$*"
    else
        inner_trace "${COLOR_WARNING}$*${COLOR_RESET}"
    fi
}

trace () {
    if [ -n "$LOG_FILE" ]; then
        inner_trace "$*"
    else
        inner_trace "${COLOR_TRACE}$*${COLOR_RESET}"
    fi
}

alert() {
    if [ -n "$LOG_FILE" ]; then
        inner_trace "$*"
    else
        inner_trace "${COLOR_ALERT}$*${COLOR_RESET}"
    fi
}

die() {
    if [ -n "$LOG_FILE" ]; then
        inner_trace "$*"
    else
        inner_trace "${COLOR_DIE}$*${COLOR_RESET}"
    fi
    cleanup_env
    exit 1
}

usage()
{
    cat <<EOF
Usage: $PROGNAME
blah blah
EOF
}

build()
{
    trace "!!! Building the unified client agent release"
    set -x
    TMP_REPO=`mktemp -d`
    cd ${MY_CWD}
    
}

# vim:set ai et sts=4 sw=4 tw=80:
