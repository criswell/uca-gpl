#!/usr/bin/env sh

# The client agent bootstrap script
#----------------------------------
# This script is intended to bootstrap the EIL Linux Client Agent
#
# This script must be completely self-contained (unfortunately)

# EIL IP configs
EIL_AUTO_PRO="172.16.3.10"
EIL_AUTO_DEV="172.16.3.12"
EIL_RELEASE="172.16.3.10"
EIL_STAGING="10.4.0.66"
NMSA_IP="10.4.0.123"

unset IS_STAGING IS_RELEASE EIL_LATEST EIL_AUTO INSTALL_TOOL IS_DEV IS_PRO || true

# Uncomment whichever of the following is correct for this install
IS_STAGING=yes
#IS_RELEASE=yes

# Uncomment the following to determine whether we're using development or
# production servers
IS_PRO=yes
#IS_DEV=yes

if [ -n "$IS_STAGING" ]; then
    EIL_LATEST=$EIL_STAGING
else
    EIL_LATEST=$EIL_RELEASE
fi

if [ -n "$IS_DEV" ]; then
    EIL_AUTO=$EIL_AUTO_DEV
else
    EIL_AUTO=$EIL_AUTO_PRO
fi

PROGNAME=${0##*/}
MY_CWD=`pwd`
THIS_SCRIPT="${MY_CWD}/${PROGNAME}"

# The two install tool variants
INSTALL_TOOL_GENERAL="install_tool.sh"
INSTALL_TOOL_ESXi="install_tool_esxi.sh"

# This function cleans the previous hosts file
clean_hosts_file() {
    local TMP_FILE=`mktemp /tmp/eil-XXXXXX`
    sed '/## EIL_BEGIN/,/## EIL_END/d' /etc/hosts > ${TMP_FILE}
    cp -f ${TMP_FILE} /etc/hosts
    rm -f ${TMP_FILE}
}

# This function makes the hosts file, it backs up the old hosts file, and
# stores checksum signatures to check for tampering
make_hosts_file() {
    local DATE_STAMP=$(date +%j%H%M%S)
    cp -f /etc/hosts /etc/hosts.backup.${DATE_STAMP}
    md5sum /etc/hosts.backup.${DATE_STAMP} > /etc/hosts.backup.md5.${DATE_STAMP}

    clean_hosts_file

    echo "## EIL_BEGIN" >> /etc/hosts
    echo "### EIL Linux Client Agent Specific Config ###" >> /etc/hosts
    echo "# Changes to this section will be overwritten during client agent upgrades" >> /etc/hosts
    echo "${EIL_AUTO}    eilauto01   eilauto01.eil-infra.com" >> /etc/hosts
    echo "${EIL_AUTO}   hfseilauto01 hfseilauto01.eil-infra.com" >> /etc/hosts
    echo "${EIL_LATEST} eilstaging  eilstaging.eil-infra.com" >> /etc/hosts
    echo "${NMSA_IP}  nmsa01  nmsa01.eil-infra.com" >> /etc/hosts
    echo "## EIL_END" >> /etc/hosts

    md5sum /etc/hosts > /etc/hosts.md5
}

# Pre-install zaniness to ensure that things like ESXi are happy
if [ ! -e "/bin/bash" ] && [ -e "/.emptytgz" ]; then
    echo ">> Installation on ESXi"
    INSTALL_TOOL=$INSTALL_TOOL_ESXi
else
    INSTALL_TOOL=$INSTALL_TOOL_GENERAL
fi

# Start out by setting up our hosts file
make_hosts_file

# Obtain the latest release
WORKSPACE=`mktemp -d /tmp/eil-XXXXXX`
cd $WORKSPACE
wget -q "http://${EIL_LATEST}/EILLinuxAgent/latest/eil_clientagent-release.tar.gz"
tar xzf eil_clientagent-release.tar.gz

# Before we start, we should ensure the old steward is shutdown, if it is
# installed and running
if [ -e "/etc/init.d/eil_steward.sh" ]; then
    /etc/init.d/eil_steward.sh stop
fi

# Give it a bit to stop what it's doing
sleep 5

cd eil_clientagent-release/
# First, uninstall the old one
./${INSTALL_TOOL} -r --uninstall

# Begin the package install
./${INSTALL_TOOL} -r --pkginstall

# Finally, log the update
UPD_VERSION=$(cat /opt/intel/eil/clientagent/lib/VERSION)
/opt/intel/eil/clientagent/tools/logger.sh --std New client agent installed ${UPD_VERSION}

# Clean-up after ourselves
rm -fr $WORKSPACE
rm -f $THIS_SCRIPT

# vim:set ai et sts=4 sw=4 tw=80:
