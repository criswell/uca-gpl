#!/usr/bin/env sh

# laf_test.sh
# -----------
# Test script to determine if the system should run the laf post install
# scripts

# THIS MUST ONLY BE RUN BY THE DISPATCHER INSTALL SCRIPT

# Load our libraries
. /opt/intel/eil/clientagent/lib/helper.sh
. /opt/intel/eil/clientagent/lib/globals.sh

NMSA_TOGGLE="/opt/intel/eil/clientagent/home/.nmsa_enable"

INSTALL_DEPS=$(cat <<EOF
wget
bash
python
seq
EOF
)

# FIXME - This is pretty ugly, any paths with ':" or "," in them will wreck it
# however, it should be safe for now
CLEAN_PATH=$(echo $PATH | sed "s/:/,/g" | sed -f ${LIB_DIR}/comma_split.sed)

_check_file_in_path() {
    RET_VAL=1
    for P in $CLEAN_PATH
    do
        if [ -e "${P}/${1}" ]; then
            RET_VAL=0
            trace "laf_test: Found '${P}/${1}'...."
            break
        fi
    done
    return $RET_VAL
}

check_req_progs() {
    RET_VAL=1
    for APP_TO_CHECK in $INSTALL_DEPS
    do
        _check_file_in_path $APP_TO_CHECK
        _STATUS=$?
        if [ "${_STATUS}" -eq "0" ]; then
            RET_VAL=0
            break
        fi
    done
    return $RET_VAL
}

check_init() {
    RET_VAL=1
    if [ -n "$IS_RHEL" ] || [ -n "$IS_SLES" ]; then
        trace "laf_test: detected an RHEL or SLES derived distro..."
        if [ -e "/etc/init.d/ipmi" ]; then
            trace "laf_test: ipmi init found, starting"
            /etc/init.d/ipmi start
            RET_VAL=0
        fi
    elif [ -n "$IS_DEB" ] || [ -n "$IS_ANGSTROM" ]; then
        trace "laf_test: detected a DEB or ANGSTROM derived distro..."
        if [ -e "/etc/init.d/ipmievd" ]; then
            trace "laf_test: ipmievd init found, starting"
            /etc/init.d/ipmievd start
            RET_VAL=0
        fi
        # Since we may have both, this isn't either/or
        if [ -e "/etc/init.d/openipmi" ]; then
            trace "laf_test: openipmi init found, starting"
            /etc/init.d/openipmi start
            RET_VAL=0
        fi
    else
        # Undefined thing! This is very very bad!
        trace "laf_test: Undefined or unsupported distro... failing..."
    fi
    return $RET_VAL
}

# This test script should output a filesystem toggle that indicates to
#   the steward whether to run the NMSA process
trace "laf_test: Checking program requirements..."
check_req_progs
_STATUS=$?
if [ "${_STATUS}" -eq "0" ]; then
    trace "laf_test: Checking for proper init scripts..."
    check_init
    _STATUS=$?
    if [ "${_STATUS}" -eq "0" ]; then
        trace "laf_test: Checking for device requirements..."
        # Check for proper devices
        FOUND=1
        for I in $(seq 0 10)
        do
            if [ -c "/dev/ipmi${I}" ]; then
                FOUND=0
                trace "laf_test: Found device '/dev/ipmi${I}'..."
            fi
        done

        if [ "${FOUND}" -eq "0" ]; then
            trace "laf_test: System capable of LAF/NMSA, setting up..."
            touch $NMSA_TOGGLE
            exit 0
        else
            trace "laf_test: Missing IPMI device, LAF/NMSA not set up..."
            exit 1
        fi
    fi
else
    trace "laf_test: Missing one or more required programs, LAF/NMSA not set up..."
    exit 1
fi

# vim:set ai et sts=4 sw=4 tw=80:
