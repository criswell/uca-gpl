#!/usr/bin/env sh

# Unified Client Agent Release Tool
# ---------------------------------
# Currently, this is Linux-specific, meaning to build the unified agent you
# must build it under Linux. The reason for this is because, under Linux, the
# unified agent depends upon the script elevator, which is a binary that must
# be statically built on a Linux-machine.
#
# The goal of this release tool is to generate a release for the UCA.

PROGNAME=${0##*/}

MY_CWD=`pwd`

. ./uca_helper.sh


usage()
{
    cat <<EOF
Usage: $PROGNAME /path/to/release

The /path/to/release should be an absolute path.
EOF
}

# vim:set ai et sts=4 sw=4 tw=80:
