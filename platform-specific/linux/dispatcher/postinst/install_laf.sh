#!/usr/bin/env sh

# install_laf.sh
# --------------
# Install and set up the LAF scripts as a postinst process

# Load our libraries
. /opt/intel/eil/clientagent/lib/helper.sh
. /opt/intel/eil/clientagent/lib/globals.sh

# THIS MUST ONLY BE RUN BY THE DISPATCHER INSTALL SCRIPT

INSTALL_CWD=$1

LAF_INSTALL_DIR=/opt/intel/eil/laf

NMSA_TOGGLE="/opt/intel/eil/clientagent/home/.nmsa_enable"

CREATE_DIR=$(cat <<EOF
bin
log
output
sids
EOF
)

INSTALL_FILES=$(cat <<EOF
laf.sh
laf-lib.sh
relay.sh
EOF
)

clean_up() {
    for DIR in $CREATE_DIR
    do
        rm -f $LAF_INSTALL_DIR/$DIR/*
        rmdir --ignore-fail-on-non-empty $LAF_INSTALL_DIR/$DIR
    done

    rmdir --ignore-fail-on-non-empty $LAF_INSTALL_DIR
}

clean_init() {
    if [ -e "/etc/init.d/nmsa_handler.sh" ]; then
        /etc/init.d/nmsa_handler.sh stop
        if [ -n "$IS_RHEL" ]; then
            chkconfig --del nmsa_handler.sh
        elif [ -n "$IS_DEB" ] || [ -n "$IS_ANGSTROM" ]; then
            update-rc.d -f nmsa_handler.sh remove
        elif [ -n "$IS_SLES" ]; then
            /usr/lib/lsb/remove_initd /etc/init.d/nmsa_handler.sh
        elif [ -n "$IS_ESX" ]; then
            # This is silly, just reboot the system :-P
            rm -f /etc/rc.local.d/nmsa_handler.sh
        elif [ -n "$IS_SLACK" ]; then
            rm -f /etc/rc.d/rc3.d/K98nmsa_handler.sh
            rm -f /etc/rc.d/rc3.d/S98nmsa_handler.sh
        fi
    fi
}

create_dir() {
    if [ ! -d $LAF_INSTALL_DIR ]; then
        mkdir -p $LAF_INSTALL_DIR
    fi

    for DIR in $CREATE_DIR
    do
        mkdir -p $LAF_INSTALL_DIR/$DIR
    done
}

install_files() {
    for FILE_TO_INSTALL in $INSTALL_FILES
    do
        cp -f ${INSTALL_CWD}/tools/${FILE_TO_INSTALL} \
                ${LAF_INSTALL_DIR}/bin/${FILE_TO_INSTALL}

        # TODO - Any permisions or ownership necessary here?
        chown root.root ${LAF_INSTALL_DIR}/bin/${FILE_TO_INSTALL}
    done
}

setup_init() {
    if [ -n "$IS_RHEL" ]; then
        chkconfig --add nmsa_handler.sh
    elif [ -n "$IS_DEB" ] || [ -n "$IS_ANGSTROM" ]; then
        update-rc.d nmsa_handler.sh defaults
    elif [ -n "$IS_SLES" ]; then
        /usr/lib/lsb/install_initd /etc/init.d/nmsa_handler.sh
    elif [ -n "$IS_ESX" ]; then
        # Yay! Manual labor!
        mkdir -p /etc/rc.local.d/
        ln -s /etc/init.d/nmsa_handler.sh /etc/rc.local.d/nmsa_handler.sh
    elif [ -n "$IS_SLACK" ]; then
        ln -s /etc/init.d/nmsa_handler.sh /etc/rc.d/rc3.d/S98nmsa_handler.sh
        ln -s /etc/init.d/nmsa_handler.sh /etc/rc.d/rc3.d/K98nmsa_handler.sh
    else
        # Undefined thing! This is very very bad!
        echo "ERROR SETTING UP RC SCRIPTS! COULD NOT IDENTIFY DISTRIBUTION!" 2>&1 | tee $ERROR_LOG_FILE
        echo "Check your installation logs and your distribution and try again!" 2>&1 | tee $ERROR_LOG_FILE
        echo "NMSA Handler is NOT functioning properly!" 2>&1 | tee $ERROR_LOG_FILE
    fi

    # Apparently, we need to make sure ipmi is added as well
    if [ -e "$NMSA_TOGGLE" ]; then
        if [ -n "$IS_RHEL" ]; then
            chkconfig --add ipmi
        elif [ -n "$IS_DEB" ] || [ -n "$IS_ANGSTROM" ]; then
            update-rc.d openipmi defaults
        elif [ -n "$IS_SLES" ]; then
            # FIXME - This needs to be verified
            /usr/lib/lsb/install_initd /etc/init.d/ipmi
        fi
    fi

    /etc/init.d/nmsa_handler.sh start
}

# Clean up any previous installation, setup for new installation and install
clean_up
clean_init

# Perform our install
create_dir
install_files
setup_init

# vim:set ai et sts=4 sw=4 tw=80:
