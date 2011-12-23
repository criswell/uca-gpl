#!/usr/bin/env bash

# nmsa_reg.sh
# -----------
# Generates and returns a properly formed NMSA registration URL of the form:
# $NMSA_SERVER/nmsa/client_register.php?mac=m&hostname=h&bmc=b&bridge=B&trans=t

CHAN_ARRAY=("0" "6");
TRAN_ARRAY=("2c" "88");
CHAN="";
TRAN="";
MAC=""
HOSTNAME=""
BMC_IP=""
BRUTE_WORKED=0
MAC_WORKED=0

NMSA_ETH_CONF="/opt/intel/eil/clientagent/home/.nmsa_eth"

pre_clean_up() {
    if [ -e "${NMSA_ETH_CONF}" ]; then
        rm -f ${NMSA_ETH_CONF}
    fi
}

get_mac() {
    for i in {0..25} ; do
        /sbin/ifconfig eth$i > tmp.f
        if ! grep "Device not found" tmp.f; then
            MAC=`ifconfig eth$i | grep HWaddr | awk '{print $5}'`
            touch ${NMSA_ETH_CONF}
            echo $i > ${NMSA_ETH_CONF}
            chmod 644 ${NMSA_ETH_CONF}
            MAC_WORKED=1
            break
        fi
    done
    rm tmp.f
}

get_hostname() {
    HOSTNAME=`hostname`
}

get_bmc_ip() {
    BMC_IP=`ipmitool lan print | grep "IP Address" | grep -v Source | \
        awk '{print $4}'`
}

get_chan_tran() {
    control=0;
    for chan in "${CHAN_ARRAY[@]}"; do
        if [ $control -eq 1 ]; then
            break;
        fi
        for tran in "${TRAN_ARRAY[@]}"; do
            res=`ipmitool -b $chan -t 0x$tran mc info 2>&1`;
            if grep -q Timeout <<< $res &> /dev/null; then
                continue
            else
                CHAN=$chan
                TRAN=$tran
                control=1
                BRUTE_WORKED=1
                break;
            fi
        done
    done
}

pre_clean_up
get_mac
get_hostname
get_bmc_ip
get_chan_tran

if [[ $BRUTE_WORKED -eq 1 && $MAC_WORKED -eq 1 ]]; then
    echo "/nmsa/client_register.php?mac=$MAC&hostname=$HOSTNAME&bmc=$BMC_IP&bridge=$CHAN&trans=$TRAN"
else
    echo "ERROR"
fi

# vim:set ai et sts=4 sw=4 tw=80:
