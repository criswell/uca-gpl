#!/usr/bin/env bash

# steward-build-verify.sh
# -----------------------
# Verifies that the current steward source builds successfully

# Set up our environment
oneTimeSetUp()
{
    # Obtain a tmp directory to install to
    TMP_DIR="/tmp/clientagent."
    TMP_DIR=${TMP_DIR}$(date +%j%H%M%S)
    mkdir -p ${TMP_DIR}

    # Copy our source tree to tmp
    cd ../../
    cp -fr steward/ ${TMP_DIR}
    cp -f Globals.mk ${TMP_DIR}
    cp -f VERSION ${TMP_DIR}
    # If we don't return to the test directory, shunit2 wont be able to
    # grep this file
    cd dispatcher/tests/
}

# Tear down our environment
oneTimeTearDown()
{
    rm -fr ${TMP_DIR}
}

#######################
# Our actual unit tests
#######################

# Test that we can do a make clean
testMakeClean()
{
    cd ${TMP_DIR}/steward
    make clean
    if [ $? -ne 0 ]; then
        fail "'make clean' failure"
    else
        assertTrue ${SHUNIT_TRUE}
    fi
}

# Test that we can do a normal make
testMake()
{
    cd ${TMP_DIR}/steward
    make clean
    make
    if [ $? -ne 0 ]; then
        fail "'make' failure"
    else
        assertTrue ${SHUNIT_TRUE}
    fi
}

# Test that we can do a static buile
testMakeStatic()
{
    cd ${TMP_DIR}/steward
    make clean
    make static
    if [ $? -ne 0 ]; then
        fail "'make static' failure"
    else
        assertTrue ${SHUNIT_TRUE}
    fi
}

. /usr/share/shunit2/shunit2

# vim:set ai et sts=4 sw=4 tw=80:
