#!/usr/bin/env bash

# logger,sh
# ---------
# External interface to the dispatcher's logger interface

unset OPT_ERR OPT_STD OPT_ECHO || true

PROGNAME=${0##*/}

# Load our libraries
. /opt/intel/eil/clientagent/lib/helper.sh
. /opt/intel/eil/clientagent/lib/globals.sh

usage()
{
    cat <<EOF
Usage: $PROGNAME [OPTION] <log message>
Where:
    <log message>   - is your log message
    [OPTION]        - is one of the following

    --std           Log the message to the standard client agent dispatcher log
                    (default when called with no options).

    --err           Log the message to the client agent dispatcher error log.

    --echo          Echo the message back to STDOUT in addition to whatever
                    else it may be doing.

    --nostd         Disable standard client agent dispatcher logging (use in
                    combination with '--echo' if you wish you only log to
                    STDOUT)
EOF
}

if [ "$1" = "" ]; then
    usage
    exit 0
fi

# Parse command line.
TEMP=$(getopt -n "$PROGNAME" --options h \
--longoptions std,\
err,\
echo,\
nostd -- $*)

eval set -- "$TEMP"

OPT_STD=yes

while [ $1 != -- ]; do
    case "$1" in
        --std)
            OPT_STD=yes
            shift
            ;;
        --err)
            OPT_ERR=yes
            shift
            ;;
        --echo)
            OPT_ECHO=yes
            shift
            ;;
        --nostd)
            unset OPT_STD || true
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

MESSAGE="$*"

if [ -n "$OPT_STD" ]; then
    trace "${MESSAGE}"
fi

if [ -n "$OPT_ERR" ]; then
    trace_error "${MESSAGE}"
fi

if [ -n "$OPT_ECHO" ]; then
    echo -E "${MESSAGE}"
fi

# vim:set ai et sts=4 sw=4 tw=80:
