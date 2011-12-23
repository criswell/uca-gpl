#!/usr/bin/env sh

# install_asset.sh
# --------------
# Install and set up the assetinfo as a postinst process

# Load our libraries
. /opt/intel/eil/clientagent/lib/helper.sh
. /opt/intel/eil/clientagent/lib/globals.sh

# THIS MUST ONLY BE RUN BY THE DISPATCHER INSTALL SCRIPT

clean_init() {
    if [ -e "/etc/init.d/assetinfo.sh" ]; then
        /etc/init.d/assetinfo.sh stop
        if [ -n "$IS_RHEL" ]; then
            chkconfig --del assetinfo.sh
        elif [ -n "$IS_DEB" ] || [ -n "$IS_ANGSTROM" ]; then
            update-rc.d -f assetinfo.sh remove
        elif [ -n "$IS_SLES" ]; then
            /usr/lib/lsb/remove_initd /etc/init.d/assetinfo.sh
        elif [ -n "$IS_ESX" ]; then
            # This is silly, just reboot the system :-P
            rm -f /etc/rc.local.d/assetinfo.sh
        elif [ -n "$IS_SLACK" ]; then
            rm -f /etc/rc.d/rc3.d/K98assetinfo.sh
            rm -f /etc/rc.d/rc3.d/S98assetinfo.sh
        fi
    fi
}

setup_init() {
    if [ -n "$IS_RHEL" ]; then
        chkconfig --add assetinfo.sh
    elif [ -n "$IS_DEB" ] || [ -n "$IS_ANGSTROM" ]; then
        update-rc.d assetinfo.sh defaults
    elif [ -n "$IS_SLES" ]; then
        /usr/lib/lsb/install_initd /etc/init.d/assetinfo.sh
    elif [ -n "$IS_ESX" ]; then
        # Yay! Manual labor!
        mkdir -p /etc/rc.local.d/
        ln -s /etc/init.d/assetinfo.sh /etc/rc.local.d/assetinfo.sh
    elif [ -n "$IS_SLACK" ]; then
        ln -s /etc/init.d/assetinfo.sh /etc/rc.d/rc3.d/S98assetinfo.sh
        ln -s /etc/init.d/assetinfo.sh /etc/rc.d/rc3.d/K98assetinfo.sh
    else
        # Undefined thing! This is very very bad!
        echo "ERROR SETTING UP RC SCRIPTS! COULD NOT IDENTIFY DISTRIBUTION!" 2>&1 | tee $ERROR_LOG_FILE
        echo "Check your installation logs and your distribution and try again!" 2>&1 | tee $ERROR_LOG_FILE
        echo "assetinfo is NOT functioning properly!" 2>&1 | tee $ERROR_LOG_FILE
    fi
}

# Clean up previous work (if any), then setup
clean_init
setup_init

# vim:set ai et sts=4 sw=4 tw=80:
