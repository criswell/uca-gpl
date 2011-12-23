#!/usr/bin/env bash

# XenClient Specific post installation tool
# -----------------------------------------
# This post-install script fixes various platform specific problems that occur
# during the install for XenClient systems

# The only thing we have to do, is fix crontab (since XenClient doesn't have
# proper cron directory delineations
crontab_line="0 * * * *   /opt/intel/eil/clientagent/tools/update-checker.sh"

crontab="/etc/cron/crontabs/root"

# This function cleans the previous hosts file
clean_crontab_file() {
    local TMP_FILE=`mktemp /tmp/eil-XXXXXX`
    sed '/## EIL_BEGIN/,/## EIL_END/d' ${crontab} > ${TMP_FILE}
    cp -f ${TMP_FILE} ${crontab}
    rm -f ${TMP_FILE}
}

setup_hosts_on_boot() {
    # Okay, this is just an ugly, ugly hack, but one which we have to do
    # because XenClient nukes the hosts file on reboot
    sed '/## EIL_BEGIN/,/## EIL_END/!d' /etc/hosts > \
        /opt/intel/eil/clientagent/home/xen_hosts

    cp /opt/intel/eil/clientagent/tools/xen_host_replace.sh \
        /etc/init.d/xen_host_replace.sh

    chown root.root /etc/init.d/xen_host_replace.sh
    chmod a+x /etc/init.d/xen_host_replace.sh
    update-rc.d -f xen_host_replace.sh remove
    update-rc.d -f eil_steward.sh remove
    update-rc.d xen_host_replace.sh defaults 98 98
    # We have to move this to the end on XenClient
    update-rc.d eil_steward.sh defaults 99 99
}

clean_crontab_file

echo "## EIL_BEGIN" >> ${crontab}
echo "${crontab_line}" >> ${crontab}
echo "## EIL_END" >> ${crontab}

setup_hosts_on_boot

# vim:set ai et sts=4 sw=4 tw=80:
