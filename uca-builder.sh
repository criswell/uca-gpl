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

. ./uca_helper.sh

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
    TMP_WORKSPACE=`mktemp -d`
    # FIXME depend on mercurial?
    hg clone ${MY_CWD} ${TMP_REPO}

    mkdir -p ${TMP_WORKSPACE}/uca/bin
    mkdir -p ${TMP_WORKSPACE}/uca/linux
    mkdir -p ${TMP_WORKSPACE}/uca/windows
    cp -fr ${TMP_REPO}/src/* ${TMP_WORKSPACE}/uca/bin/.
    cp -fr ${TMP_REPO}/platform-specific/linux/dispatcher ${TMP_WORKSPACE}/uca/linux/.
    cp -fr ${TMP_REPO}/uca-bootstrap.py ${TMP_WORKSPACE}/uca/.
    cp -fr ${TMP_REPO}/uca-installer.py ${TMP_WORKSPACE}/uca/.
    cd ${TMP_REPO}/platform-specific/linux/elevate_script
    make clean
    make
    cp ${TMP_REPO}/platform-specific/linux/elevate_script/elevate_script ${TMP_WORKSPACE}/uca/bin/.

    # FIXME currently no platform-specifics on Windows

    cd ${TMP_WORKSPACE}
    zip -r uca.zip uca/
    cd ${MY_CWD}
    cp -f ${TMP_WORKSPACE}/uca.zip ${MY_CWD}

    rm -fr ${TMP_REPO}
    rm -fr ${TMP_WORKSPACE}
    set +x
}

build

# vim:set ai et sts=4 sw=4 tw=80:
