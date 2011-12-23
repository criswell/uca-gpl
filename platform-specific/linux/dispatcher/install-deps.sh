# Install file dependencies

# The executable files to install
ALL_EXECS=$(cat <<EOF
clientagent-dispatcher.sh
nmsa_handler.py
EOF
)

# The library files to install
ALL_LIBS=$(cat <<EOF
dispatcher.sh
globals.sh
helper.sh
comma_split.sed
nmsa_daemon.py
nmsa_conf.py
nmsa_main.py
EOF
)

# The tools to install
ALL_TOOLS=$(cat <<EOF
clientagent-helper.sh
eil_steward.sh
clientagent-bootstrap.sh
update-checker.sh
xen_host_replace.sh
logger.sh
laf.sh
laf-lib.sh
nmsa_reg.sh
nmsa_handler.sh
assetinfo.sh
EOF
)

# Linked tools
# The following tools are ones which should be made available in some
# sort of system-wide fashion based upon the distribution we are using.
# This way, these tools can be accessed regardless of *where* the real
# install is.
#
# The format of this variable is as follows:
#   scriptname:/path/to/link:cp-options
#
# Where:
#    scriptname is the script name as it appears in ALL_TOOLS above
#    /path/to/link is the absolute path to where the symbolic link should be
#    cp-options are the cp options used in the linking
LINKED_TOOLS=$(cat <<EOF
clientagent-helper.sh:/usr/bin:-lf
eil_steward.sh:/etc/init.d:-f
update-checker.sh:/etc/cron.hourly:-f
nmsa_handler.sh:/etc/init.d:-f
assetinfo.sh:/etc/init.d:-f
EOF
)

# The docs to install
ALL_DOCS=$(cat <<EOF

EOF
)

# For the scripts, we have to get a bit creative...
# Our format is:
#  uid.gid:script_name
#
# The reason for this is because *some* of these scripts will have to be
# run as different users depending upon what it is they are doing (for
# example, rebooting will require 'root' permissions, modifying SAMBA
# settings may require a SAMBA user, etc.)
#
# When the script is installed, it will be setuid and setgid to the
# uid and gid detailed here to ensure that it runs with the appropriate
# permissions.
#
# If uid.gid are "*.*", then they are setuid/setguid to whatever the UID
# and GID of the client agent dispatch (as detailed in globals.sh).
#
# NOTE: IF the UID and GID DO NOT EXIST, they WILL be created! However,
# if the client agent is un-installed they WILL NOT BE REMOVED! This
# cannot be helped due to the fact we are using bash and have no way to
# handle such complicated record-keeping! What this means is that care
# must be given to make sure you get the UID/GID correct! If you are
# trying to use a UID/GID that should be present on the system, then
# you MUST make sure you have them spelled correctly!

# The SOURCE_SCRIPTS is the master list of the *real* scripts to
# install. These are the actual coded scripts that reside in the
# scripts/ directory.
SOURCE_SCRIPTS=$(cat <<EOF
root.eil:reboot
root.eil:reboot-noloop
root.eil:tcp_diag-full
root.eil:tcp_diag-light
root.eil:tcp_diag-xen
root.eil:asset_refresh
root.eil:client_update
root.eil:asset_done_reboot
EOF
)

# The LINKED_SCRIPTS is a different list from the SOURCE_SCRIPTS.
# Sometimes, a script will remain the same across multiple platforms,
# but because we do not want to duplicate our code (thus having
# multiple locations to maintain the same identical code), we will
# instead hard link our secondary platform scripts to those scripts on
# the other platforms. This gives us the true platform agnostism we
# desire, without the messiness of dealing with duplicated code.
#
# The format of this variable is as follows:
#  linked_script_name:source_script_name
#
# Where:
#  linked_script_name is the intended hard link for the secondary
#           platform.
#  source_script_name is the original script_name as detailed in
#           SOURCE_SCRIPTS above.
LINKED_SCRIPTS=$(cat <<EOF
ubuntu_reboot:reboot-noloop
rhel_reboot:reboot-noloop
suse_reboot:reboot-noloop
centos_reboot:reboot-noloop
xen_reboot:reboot-noloop
esx_reboot:reboot
esxi_reboot:reboot
slackware_reboot:reboot
slax_reboot:reboot
xenclient_reboot:reboot
ubuntu_tcp_diag:tcp_diag-full
rhel_tcp_diag:tcp_diag-full
suse_tcp_diag:tcp_diag-full
centos_tcp_diag:tcp_diag-full
slackware_tcp_diag:tcp_diag-full
slax_tcp_diag:tcp_diag-full
xen_tcp_diag:tcp_diag-xen
esx_tcp_diag:tcp_diag-light
esxi_tcp_diag:tcp_diag-light
xenclient_tcp_diag:tcp_diag-light
ubuntu_asset_refresh:asset_refresh
rhel_asset_refresh:asset_refresh
suse_asset_refresh:asset_refresh
centos_asset_refresh:asset_refresh
xen_asset_refresh:asset_refresh
esx_asset_refresh:asset_refresh
esxi_asset_refresh:asset_refresh
xenclient_asset_refresh:asset_refresh
slax_asset_refresh:asset_refresh
slackware_asset_refresh:asset_refresh
ubuntu_client_update:client_update
rhel_client_update:client_update
suse_client_update:client_update
centos_client_update:client_update
xen_client_update:client_update
esx_client_update:client_update
esxi_client_update:client_update
xenclient_client_update:client_update
slackware_client_update:client_update
slax_client_update:client_update
slax_asset_done_reboot:asset_done_reboot
EOF
)

# The POSTINST_SCRIPTS contains a list of the scripts to be installed for
# post-install requirements
POSTINST_SCRIPTS=$(cat <<EOF
xenclient.sh:xen_test.sh
install_laf.sh:laf_test.sh
install_asset.sh:asset_test.sh
noinit_setup.sh:noinit_test.sh
EOF
)

# vim:set ai et sts=4 sw=4 tw=80:
