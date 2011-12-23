#!/usr/bin/env bash

# helper-verify.sh
# ----------------
# Verifies that the output given from clientagent-helper.sh is what is
# expected from globals.sh

# Set up our environment
oneTimeSetUp()
{
    # Obtain a tmp directory to install to
    TMP_DIR="/tmp/clientagent."
    TMP_DIR=${TMP_DIR}$(date +%j%H%M%S)
    mkdir -p ${TMP_DIR}

    # Install to tmp directory
    BOOTSTRAP_DIR=$TMP_DIR
    export BOOTSTRAP_DIR
    cd ../
    bash install.sh

    cd tests/

    . ../lib/globals.sh
}

# Tear down our environment
oneTimeTearDown()
{
    # Clean up tmp directory
    BOOTSTRAP_DIR=$TMP_DIR
    export BOOTSTRAP_DIR
    cd ../
    bash install.sh -p

    cd tests/
}

#######################
# Our actual unit tests
#######################

# Test the log file and uid/gid outputs
testStdlog()
{
    export BOOTSTRAP_DIR
    local _test=`${TOOL_DIR}/clientagent-helper.sh --stdlog`

    assertEquals "Standard log file error!" \
        "${STANDARD_LOG_FILE}" "${_test}"
}

testCCMSlog()
{
    export BOOTSTRAP_DIR
    local _test=`${TOOL_DIR}/clientagent-helper.sh --ccmslog`

    assertEquals "CCMS log file error!" \
        "${CCMS_LOG_FILE}" "${_test}"
}

testErrlog()
{
    export BOOTSTRAP_DIR
    local _test=`${TOOL_DIR}/clientagent-helper.sh --errlog`

    assertEquals "Error log file error!" \
        "${ERROR_LOG_FILE}" "${_test}"
}

testUID()
{
    export BOOTSTRAP_DIR
    local _test=`${TOOL_DIR}/clientagent-helper.sh --uid`

    assertEquals "Unexpected install UID!" \
        "${INSTALL_UID}" "${_test}"
}

testGID()
{
    export BOOTSTRAP_DIR
    local _test=`${TOOL_DIR}/clientagent-helper.sh --gid`

    assertEquals "Unexpected install GID!" \
        "${INSTALL_GID}" "${_test}"
}

# Test each of the directory outputs
testBase()
{
    export BOOTSTRAP_DIR
    local base_test=`${TOOL_DIR}/clientagent-helper.sh --base`

    assertEquals "Base directory error!" \
        "${BASE_DIR}" "${base_test}"
}

testInstall()
{
    export BOOTSTRAP_DIR
    local install_test=`${TOOL_DIR}/clientagent-helper.sh --install`

    assertEquals "Install directory error!" \
        "${INSTALL_DIR}" "${install_test}"
}

testBin()
{
    export BOOTSTRAP_DIR
    local bin_test=`${TOOL_DIR}/clientagent-helper.sh --bin`

    assertEquals "Binary directory error!" \
        "${BIN_DIR}" "${bin_test}"
}

testLib()
{
    export BOOTSTRAP_DIR
    local lib_test=`${TOOL_DIR}/clientagent-helper.sh --lib`

    assertEquals "Library directory error!" \
        "${LIB_DIR}" "${lib_test}"
}

testDoc()
{
    export BOOTSTRAP_DIR
    local doc_test=`${TOOL_DIR}/clientagent-helper.sh --doc`

    assertEquals "Documentation directory error!" \
        "${DOC_DIR}" "${doc_test}"
}

testTool()
{
    export BOOTSTRAP_DIR
    local tool_test=`${TOOL_DIR}/clientagent-helper.sh --tool`

    assertEquals "Tool directory error!" \
        "${TOOL_DIR}" "${tool_test}"
}

testHome()
{
    export BOOTSTRAP_DIR
    local home_test=`${TOOL_DIR}/clientagent-helper.sh --home`

    assertEquals "Home directory error!" \
        "${HOME_DIR}" "${home_test}"
}

testScripts()
{
    export BOOTSTRAP_DIR
    local scripts_test=`${TOOL_DIR}/clientagent-helper.sh --scripts`

    assertEquals "Scripts directory error!" \
        "${SCRIPTS_DIR}" "${scripts_test}"
}

testComdir()
{
    export BOOTSTRAP_DIR
    local comdir_test=`${TOOL_DIR}/clientagent-helper.sh --comdir`

    assertEquals "Command directory error!" \
        "${COMMAND_DIR}" "${comdir_test}"
}

. /usr/share/shunit2/shunit2

# vim:set ai et sts=4 sw=4 tw=80:
