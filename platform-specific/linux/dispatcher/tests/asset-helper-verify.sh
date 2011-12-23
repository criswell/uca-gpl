#!/usr/bin/env bash

# asset-helper-verify.sh
# ----------------------
# Verifies the asset helper section of the code is in working condition

# Set up our environment
oneTimeSetUp()
{
    # Obtain a tmp directory
    TMP_DIR="/tmp/clientagent."
    TMP_DIR=${TMP_DIR}$(date +%j%H%M%S)
    mkdir -p ${TMP_DIR}

    # Set up our various temp file variables

    # Set up the asset source xml
    TMP_ASSET_SOURCE="${TMP_DIR}/asset_source.xml"
    cat > $TMP_ASSET_SOURCE << EOF
<Attributes>
<Turbo>N/A</Turbo>
<HyperThreading>Enabled</HyperThreading>
<Vt>N/A</Vt>
<Vt-d>N/A</Vt-d>
<Xd>N/A</Xd>
<UUID></UUID>
<C6State>N/A</C6State>
<C2C3>N/A</C2C3>
<NMVersion>Disabled</NMVersion>
<DCMIVersion></DCMIVersion>
<EIST>N/A</EIST>
<DimmSlots>0</DimmSlots>
<DimmPopulated>0</DimmPopulated>
<RamTotal></RamTotal>
<Dimm>
</Dimm>
<SR-IOV>N/A</SR-IOV>
<NicCount>1</NicCount>
<NicSpeed>is Up</NicSpeed>
<FiberCount>0</FiberCount>
<FiberSpeed>Disabled</FiberSpeed>
<SerialOverLan>Disabled</SerialOverLan>
<RemoteCapability>
<IPaddress></IPaddress>
<Weblink>http://</Weblink>
<iLO></iLO>
</RemoteCapability>
<HardDriveCount>0</HardDriveCount>
<Raid>Disabled</Raid>
<OEMInventory>
<Bios>N/A</Bios>
<BMC><BMC>
</OEMInventory>
</Attributes>
EOF

    TMP_ASSET_TEST="${TMP_DIR}/asset_test.xml"

    TMP_LOG="${TMP_DIR}/test.log"

    ASSET_FILE="/opt/intel/assetinfo"

    TMP_CURRENT_ASSET_STORAGE="${TMP_DIR}/asset_store"
    unset WAS_ORIG_ASSET || true
    if [ -e "$ASSET_FILE" ]; then
        WAS_ORIG_ASSET=yes
        cp -f ${ASSET_FILE} ${TMP_CURRENT_ASSET_STORAGE}
    else
        mkdir -p /opt/intel
    fi

    TMP_ASSET_TEST_BIN="${TMP_BIN}/assetTest"
    cd ../../steward/
    touch VERSION
    cd tests/
    make assetHelper_test
    cp -f assetHelper_test ${TMP_ASSET_TEST_BIN}
    chmod a+x ${TMP_ASSET_TEST_BIN}
    make clean
    cd ../
    rm VERSION
    cd ../dispatcher/tests
}

# Tear down our environment
oneTimeTearDown()
{
    rm -f ${ASSET_FILE}
    if [ -n "$WAS_ORIG_ASSET" ]; then
        cp -f ${TMP_CURRENT_ASSET_STORAGE} ${ASSET_FILE}
    fi
    rm -fr ${TMP_DIR}
}

#######################
# Our actual unit tests
#######################

testVerifyErrorOnNoAssetFile()
{
    rm -f ${TMP_ASSET_TEST}
    if [ -e "$ASSET_FILE" ]; then
        rm -f ${ASSET_FILE}
    fi
    ${TMP_ASSET_TEST_BIN} ${TMP_ASSET_TEST} ${TMP_LOG}
    if [ $? -ne 0 ]; then
        rm ${TMP_LOG}
        assertTrue ${SHUNIT_TRUE}
    else
        cat ${TMP_LOG}
        rm ${TMP_LOG}
        fail "We expected a failure, but we got success?"
    fi
}

testVerifyAssetFileRead()
{
    rm -f ${TMP_ASSET_TEST}
    cp -f ${TMP_ASSET_SOURCE} ${ASSET_FILE}
    ${TMP_ASSET_TEST_BIN} ${TMP_ASSET_TEST} ${TMP_LOG}
    if [ $? -ne 0 ]; then
        cat ${TMP_LOG}
        rm ${TMP_LOG}
        fail "Failure running asset test"
    else
        # Compare the two
        cat ${TMP_LOG}
        diff ${ASSET_FILE} ${TMP_ASSET_TEST}
        if [ $? -ne 0 ]; then
            rm ${TMP_LOG}
            fail "Failure, the output does not match the input!"
        else
            rm ${TMP_LOG}
            assertTrue ${SHUNIT_TRUE}
        fi
    fi
}

. /usr/share/shunit2/shunit2

# vim:set ai et sts=4 sw=4 tw=80:
