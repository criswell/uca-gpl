#!/usr/bin/env sh

# dummy_postinst.sh
# -----------------
# A dummy post-installation script that simply tests the features and
# functionality of the system

cat <<EOF

*************************************
******>>> dummy_postinst.sh <<<******

This is a simple test post installation script. It does nothing other than
print this message. Enable it in the POSTINST_SCRIPTS section of install-deps.sh
along with whatever tester you wish to test and then utilze it to test your
conditional logic.

During the install process, if you do not see this text, then your conditional
logic failed.

If you do see this text, then "yay, you!"

******>>> dummy_postinst.sh <<<******
*************************************

EOF

# vim:set ai et sts=4 sw=4 tw=80:
