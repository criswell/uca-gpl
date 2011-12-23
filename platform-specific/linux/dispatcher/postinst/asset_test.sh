#!/usr/bin/env sh

# asset_test.sh
# -------------
# Test script to determine if the system is capable of supporting the assetinfo
# script.

# THIS MUST ONLY BE RUN BY THE DISPATCHER INSTALL SCRIPT

# Load our libraries
. /opt/intel/eil/clientagent/lib/helper.sh
. /opt/intel/eil/clientagent/lib/globals.sh

INSTALL_DEPS=$(cat <<EOF
bash
ipmitool
dmidecode
dcmitool
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
            trace "asset_test: Found '${P}/${1}'...."
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

trace "asset_test: Checking program requirements..."
check_req_progs
_STATUS=$?
if [ "${_STATUS}" -eq "0" ]; then
    trace "asset_test: assetinfo program requirements found..."
    exit 0
else
    trace "asset_test: Missing one or more required programs, assetinfo not set up..."
    exit 1
fi

# vim:set ai et sts=4 sw=4 tw=80:
