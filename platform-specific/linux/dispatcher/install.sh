#!/usr/bin/env sh

# Install script for clientagent-base.sh suite

MY_CWD=`pwd`

if [ "$(id -u)" != "0" ]; then
    echo "This install script must be run as root!"
    exit 1
fi

type hg &> /dev/null || { 
    type wget &> /dev/null || {
        type curl &> /dev/null || {
            cat <<EOF
One of the following programs are required by the clientagent dispatcher
in order for its auto-update/auto-patch features to work:
    * Mercurial (http://mercurial.selenic.com/)
    * wget (http://www.gnu.org/software/wget/)
    * curl (http://curl.haxx.se/)

Each should be available in any modern Linux distribution, and it is up
to you to determine which to use.

The preferred program is "Mercurial" as it allows for *both* auto-
updating and auto-patching, however, it has the most dependencies and
may not be easy to install on some of the more thin Linux installs.

Both wget and curl can do auto-update, but cannot do auto-patching.
EOF
            exit 1
        }
    }
}

. lib/helper.sh
. lib/globals.sh

# Parse the install dependency file
. ./install-deps.sh

# Functions used by the install script
_inner_unlink() {
    if [ -n "$IS_ESX" ]; then
        rm -f ${2}/${1}
    else
        unlink ${2}/${1}
    fi
}

add_user_if_not_exist() {
    local LGID=$2
    local LUID=$1
    if [ -z "$1" ]; then
        # If called with no parameters, we use the
        # defaults
        LUID=$INSTALL_UID
        LGID=$INSTALL_GID
    fi

    egrep -i "^$LGID" /etc/group > /dev/null
    if [ $? -ne 0 ]; then
        # Group does not exist, add it
        if [ -n "$IS_SLES" ] || [ -n "$IS_ESX" ]; then
            /usr/sbin/groupadd $LGID
        elif [ -n "$IS_ANGSTROM" ]; then
            # FIXME - Again, as I've said elsewhere, we assume that XenClient
            # is the only Angstrom-based distro we're using
            /bin/addgroup $LGID
        else
            /usr/sbin/groupadd -f $LGID
        fi

    fi

    egrep -i "^$LUID" /etc/passwd > /dev/null
    if [ $? -ne 0 ]; then
        # User does not exist, add them
        if [ -n "$IS_SLES" ]; then
            /usr/sbin/useradd -d $HOME_DIR -c eil_client \
                -s /bin/false -g $LGID $LUID
        elif [ -n "$IS_ESX" ]; then
            # This would be a security problem- if we were persistent
            /usr/sbin/useradd -d $HOME_DIR -c eil_client \
                -s /bin/ash -g $LGID $LUID
        elif [ -n "$IS_ANGSTROM" ]; then
            # FIXME - Same Angstrom warning as elsewhere
            /bin/adduser -D -G $LGID -H -s /bin/false -h $HOME_DIR $LUID
        else
            /usr/sbin/useradd -d /dev/null -c eil_client \
                -s /dev/null -g $LGID -M $LUID
        fi
    fi
}

del_user_if_exist() {
    egrep -i "^$INSTALL_UID" /etc/passwd > /dev/null
    if [ $? -eq 0 ]; then
        if [ -n "$IS_ESX" ]; then
            /usr/sbin/userdel $INSTALL_UID
        elif [ -n "$IS_ANGSTROM" ]; then
            /bin/deluser $INSTALL_UID
        else
            /usr/sbin/userdel -f $INSTALL_UID
        fi
    fi

    egrep -i "^$INSTALL_GID" /etc/group > /dev/null
    if [ $? -eq 0 ]; then
        if [ -n "$IS_ANGSTROM" ]; then
            /bin/delgroup $INSTALL_GID
        else
            /usr/sbin/groupdel $INSTALL_GID
        fi
    fi
}

uninstall_everything() {
    # uninstall the libs
    rm -f $LIB_DIR/*

    # uninstall the docs
    rm -f $DOC_DIR/*

    # uninstall the rc files
    if [ -n "$IS_RHEL" ]; then
        /etc/init.d/eil_steward.sh stop
        chkconfig --del eil_steward.sh
    elif [ -n "$IS_DEB" ] || [ -n "$IS_ANGSTROM" ]; then
        /etc/init.d/eil_steward.sh stop
        update-rc.d -f eil_steward.sh remove
    elif [ -n "$IS_SLES" ]; then
        /etc/init.d/eil_steward.sh stop
        /usr/lib/lsb/remove_initd /etc/init.d/eil_steward.sh
    elif [ -n "$IS_ESX" ]; then
        # This is silly, just reboot the system :-P
        /etc/init.d/eil_steward.sh stop
        rm -f /etc/init.d/eil_steward.sh
        rm -f /etc/rc.local.d/eil_steward.sh
    elif [ -n "$IS_SLACK" ]; then
        /etc/init.d/eil_steward.sh stop
        rm -f /etc/rc.d/rc3.d/S99eil_steward.sh
        rm -f /etc/rc.d/rc3.d/K99eil_steward.sh
        rm -f /etc/init.d/eil_steward.sh
    else
        # failing all else, we just get rid of the standard location
        /etc/init.d/eil_steward.sh stop
        rm -f /etc/init.d/eil_steward.sh
    fi

    # uninstall the tools
    for TOOL_LINK in $LINKED_TOOLS
    do
        LARR=`echo "$TOOL_LINK" | sed -f dep-cleaner.sed`
        _inner_unlink ${LARR}
    done
    rm -f $TOOL_DIR/*

    # uninstall the scripts
    rm -f $SCRIPTS_DIR/*

    # purge any un-consumed commands
    rm -f $COMMAND_DIR/*

    # uninstall the bin
    rm -f $BIN_DIR/*

    # uninstall the postinst
    rm -f $POSTINST_DIR/*
}

# We use /opt for our installation location to adhere to LSB Linux
# Filesystem Hierarchy Standards (this gives us maximum compatibility
# across the various distros we aim to support).
BASE_DIR=/opt

# Intel has a registered provider name with the LSB
LANANA=$BASE_DIR/intel

# We want to have our own sub-directory under that specific to the
# EIL namespace, additionally, we want our client agent to live there.
if [ "$BOOTSTRAP_DIR" = "" ]; then
    INSTALL_DIR=$LANANA/eil/clientagent
else
    INSTALL_DIR=$BOOTSTRAP_DIR
fi

BIN_DIR=$INSTALL_DIR/bin
LIB_DIR=$INSTALL_DIR/lib
DOC_DIR=$INSTALL_DIR/doc
TOOL_DIR=$INSTALL_DIR/tools
HOME_DIR=$INSTALL_DIR/home
SCRIPTS_DIR=$INSTALL_DIR/scripts
POSTINST_DIR=$INSTALL_DIR/postinst

if [ $# != 0 ] ; then
    while true ; do
        case "$1" in
            -h)
                echo "install.sh"
                echo "----------"
                echo "Run with no arguments to install software."
                echo "Run with '-u' to uninstall old software without"
                echo "      purging log files or directory structure."
                echo "Run with '-p' to purge/remove old software."
                exit 0
                ;;
            -u)
                uninstall_everything
                echo "clientagent dispatcher uninstalled"
                exit 0
                ;;
            -p)
                uninstall_everything
                # purge the libs
                rmdir $LIB_DIR

                # purge the docs
                rmdir $DOC_DIR

                # purge the tools
                rmdir $TOOL_DIR

                # purge the scripts directory
                rmdir $SCRIPTS_DIR

                # purge the commands directory
                rmdir $COMMAND_DIR

                # purge the bin
                rmdir $BIN_DIR

                # purge the postinst
                rmdir $POSTINST_DIR

                # purge the users
                del_user_if_exist

                echo "clientagent dispatcher purged"
                exit 0
                ;;
            *)
                break
                ;;
        esac
    done
fi

# Make the entire directory tree, including bin, libs, docs, etc.
mkdir -p $INSTALL_DIR
mkdir -p $BIN_DIR
mkdir -p $LIB_DIR
mkdir -p $DOC_DIR
mkdir -p $TOOL_DIR
mkdir -p $HOME_DIR
mkdir -p $SCRIPTS_DIR
mkdir -p $COMMAND_DIR
mkdir -p $POSTINST_DIR

# Set up the users
add_user_if_not_exist

# Set ownership of the proper directories
chown ${INSTALL_UID}.${INSTALL_GID} ${HOME_DIR}
chown ${INSTALL_UID}.${INSTALL_GID} $COMMAND_DIR
chmod 1775 ${HOME_DIR}

# Install the libs
for LIB_FILE in $ALL_LIBS
do
    cp -fr lib/${LIB_FILE} $LIB_DIR/.
done

# Set up the version info
cp -f ../VERSION $LIB_DIR/.

# Install the tools
for TOOL_FILE in $ALL_TOOLS
do
    cp -fr tools/${TOOL_FILE} $TOOL_DIR/.
    chmod a+x ${TOOL_DIR}/${TOOL_FILE}
done

# Set up the linked tools
_cp_linked_tools() {
    if [ -n "$IS_ESX" ]; then
        # ESX forces us to ignore the options
        cp -f ${TOOL_DIR}/${1} ${2}/${1}
    else
        cp ${3} ${TOOL_DIR}/${1} ${2}/${1}
    fi
}
for TOOL_LINE in $LINKED_TOOLS
do
    LARR=`echo "$TOOL_LINE" | sed -f dep-cleaner.sed`

    _cp_linked_tools ${LARR}
done

# Install the docs
for DOC_FILE in $ALL_DOCS
do
    cp -fr docs/${DOC_FILE} $DOC_DIR/.
done

# Install the binaries
for EXEC_FILE in $ALL_EXECS
do
    cp -fr bin/$EXEC_FILE $BIN_DIR/.
    # Set up the binaries to SETUID as the user
    chown ${INSTALL_UID}.${INSTALL_GID} ${BIN_DIR}/${EXEC_FILE}
    chmod 754 ${BIN_DIR}/${EXEC_FILE}
    # SETUID/SETGID the binaries
    chmod u+s ${BIN_DIR}/${EXEC_FILE}
    chmod g+s ${BIN_DIR}/${EXEC_FILE}
done

# Install the scripts
# - Start with the source scripts
_setup_source_script() {
    cp -fr scripts/${2} ${SCRIPTS_DIR}/.
    if [ "${1}" = "*.*" ]; then
        # Make it owned by the same owner as client agent dispatcher
        chown ${INSTALL_UID}.${INSTALL_GID} ${SCRIPTS_DIR}/${2}
    else
        # Make it owned by the user specified
        chown ${1} ${SCRIPTS_DIR}/${2}
    fi

    # SETUID/SETGID
    chmod u+xs ${SCRIPTS_DIR}/${2}
    chmod g+xs ${SCRIPTS_DIR}/${2}
}
for SCRIPT_LINE in $SOURCE_SCRIPTS
do
    LARR=`echo "$SCRIPT_LINE" | sed -f dep-cleaner.sed`

    _setup_source_script ${LARR}
done

# - Now do the linked scripts
_setup_script_linking() {
    ln -s ${SCRIPTS_DIR}/${2} ${SCRIPTS_DIR}/${1}
}
for LINKED_SCRIPT_LINE in $LINKED_SCRIPTS
do
    LARR=`echo "$LINKED_SCRIPT_LINE" | sed -f dep-cleaner.sed`

    _setup_script_linking ${LARR}
done

# - Next do the post install scripts
_setup_postinst_script() {
    cp -fr postinst/${1} ${POSTINST_DIR}/${1}
    # For these, only root can do anything with them
    chown root.root ${POSTINST_DIR}/${1}
    chmod 700 ${POSTINST_DIR}/${1}
}
for POSTINST_LINE in $POSTINST_SCRIPTS
do
    LARR=`echo "$POSTINST_LINE" | sed -f dep-cleaner.sed`

    _setup_postinst_script ${LARR}
done

# Set up the rc files
if [ -n "$IS_RHEL" ]; then
    chkconfig --add eil_steward.sh
elif [ -n "$IS_DEB" ] || [ -n "$IS_ANGSTROM" ]; then
    update-rc.d eil_steward.sh defaults
elif [ -n "$IS_SLES" ]; then
    /usr/lib/lsb/install_initd /etc/init.d/eil_steward.sh
elif [ -n "$IS_ESX" ]; then
    # Yay! Manual labor!
    mkdir -p /etc/rc.local.d/
    ln -s /etc/init.d/eil_steward.sh /etc/rc.local.d/eil_steward.sh
elif [ -n "$IS_SLACK" ]; then
    # MOAR MANUAL LABOR! But at least we have sys-v and persistence!
    ln -s /etc/init.d/eil_steward.sh /etc/rc.d/rc3.d/S99eil_steward.sh
    ln -s /etc/init.d/eil_steward.sh /etc/rc.d/rc3.d/K99eil_steward.sh
else
    # Undefined thing! This is very very bad!
    echo "ERROR SETTING UP RC SCRIPTS! COULD NOT IDENTIFY DISTRIBUTION!" 2>&1 | tee $ERROR_LOG_FILE
    echo "Check your installation logs and your distribution and try again!" 2>&1 | tee $ERROR_LOG_FILE
    echo "EIL Linux Client Agent is NOT functioning properly!" 2>&1 | tee $ERROR_LOG_FILE
fi

# Finally, set up logrotate (or equivalent)
# FIXME TODO

# Last, but not least, we run any POSTINST scripts
_run_postinst_script() {
    TEST_SCRIPT="${2}"
    POSTINST_SCRIPT="${1}"

    # We're a bit destructive here, but we have to be. Some of the systems we
    # want to support do not have mktemp or a comparable tool, so we just have
    # to do this.
    rm -f ${POSTINST_DIR}/${TEST_SCRIPT}
    cp -f postinst/${TEST_SCRIPT} ${POSTINST_DIR}/${TEST_SCRIPT}
    chown root.root ${POSTINST_DIR}/${TEST_SCRIPT}
    chmod 700 ${POSTINST_DIR}/${TEST_SCRIPT}

    # We assume an exit status of "0" means it's okay to run the script
    ${POSTINST_DIR}/${TEST_SCRIPT}

    if [ $? -eq 0 ]; then
        echo "~~> Running post-install script: ${POSTINST_SCRIPT}"
        ${POSTINST_DIR}/${POSTINST_SCRIPT} ${MY_CWD}
    fi

    # Clean up
    rm -f ${POSTINST_DIR}/${TEST_SCRIPT}
}
for POSTINST_LINE in $POSTINST_SCRIPTS
do
    LARR=`echo "$POSTINST_LINE" | sed -f dep-cleaner.sed`

    _run_postinst_script ${LARR}
done

echo "clientagent dispatcher installed successfully"

# vim:set ai et sts=4 sw=4 tw=80:
