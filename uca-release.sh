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
Usage: $PROGNAME /path/to/release [branch]

Parameters:
    - /path/to/release should be an absolute path to where the release goes.

    - [branch] is an optional named branch for the Mercurial repository.

This release tool should be ran from within a current, working, Mercurial
repository of the UCA. It will clone the current directory to a temp directory,
and build the release there.

If your release needs to be built from a specific named branch from the
repository, then you can give that branch name with the optional parameter
[branch].

EOF
}

type hg &> /dev/null || {
    cat <<EOF
Mercurial must be installed correctly in order to use this release tool!

Please download an install it from http://mercurial.selenic.com/ if it is not
available inside your distribution of choice.
EOF
}



# vim:set ai et sts=4 sw=4 tw=80:
