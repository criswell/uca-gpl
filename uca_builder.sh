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

PROGNAME=${0##*/}

MY_CWD=`pwd`

usage()
{
    cat <<EOF
Usage: $PROGNAME
blah blah
EOF
}

TMP_REPO=`mktemp -d`


# vim:set ai et sts=4 sw=4 tw=80:
