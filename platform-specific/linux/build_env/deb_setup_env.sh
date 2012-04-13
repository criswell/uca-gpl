#!/usr/bin/env bash

# deb_setup_env.sh
# ----------------
# A tool to setup the build environment (Ubuntu/Debian specific)

# Make sure that (if in Ubuntu) the 'Universe' and 'Multiverse' are enabled in
# your sources list!

ALL_DEBS=$(cat <<EOF
dpkg-dev
build-essential
checkinstall
flex
automake
autoconf
autotools-dev
byacc
bison
libcurl4-openssl-dev
libssl-dev
shunit2
mercurial
m4
zip
EOF
)

MY_CWD=`pwd`

# Must be run as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root!"
    exit 1
fi

# Check we're running debian/ubuntu
if [ ! -f "/etc/debian_version" ]; then
    cat <<EOF

 This script must be run in a Debian-derived distribution (such as Ubuntu)!

 If you wish to build the EIL Linux client agent in another distribution, please
 see the BUILD_ENV text file and the source for this script to find the proper
 dependencies necessary to set up your build environment!

EOF

exit 1
fi

# Show interactive text explaining what we're about to do
cat <<EOF

 This script will set up a stock Debian or Ubuntu install for development and
 building of the EIL Linux client agent.

 If you are not using Debian or Ubuntu, then take a look at this script (and the
 BUILD_ENV text file) for more information about the EIL Linux client agent's
 requirements. If you are building or developing on a distribution other than
 Debian or Ubuntu, it is left up to you to figure out what is needed for a proper
 development environment.

 This script will have a number of interactive sections, please read everything
 carefully and answer the questions with caution.

EOF

read -p "Press [Enter] to continue : "

# Install the dependencies

cat <<EOF

 Updating aptitude....

EOF
aptitude update

cat <<EOF

 Installing dependencies...

 Select "Yes" if prompted...

EOF

aptitude install ${ALL_DEBS}

# Set up gsoap sources in a tmp directory

#cat <<EOF
#
# Setting up gSOAP sources in a tmp build directory...
#
#EOF
#
#TMP_BASE=`mktemp -d`
#cp -frv gsoap-2.8 ${TMP_BASE}/.
#cd ${TMP_BASE}/gsoap-2.8/

# configure and checkinstall

#cat <<EOF

# Performing configure and package build for gsoap...
#
# Answer any questions asked...

#EOF

#read -p "Press [Enter] to continue : "

# This is an ugly hack, but there's a strange heisenbug where sometimes the
# aclocal is recognized, and sometimes it is not. I've spent a few days trying
# to trace the exact cause of this bug, and have now given up because I need to
# move on to other things. So, to side-step it entirely, we do the following
# symlink. - Sam
#ln -s /usr/bin/aclocal-1.11 /usr/bin/aclocal-1.10
#ln -s /usr/bin/aclocal-1.11 /bin/alocal-1.10
#ln -s /usr/bin/automake-1.11 /usr/bin/automake-1.10
#ln -s /usr/bin/automake-1.11 /bin/automake-1.10

#chmod a+x configure

#./configure
#make
#checkinstall

#unlink /usr/bin/aclocal-1.10
#unlink /bin/aclocal-1.10
#unlink /usr/bin/automake-1.10
#unlink /bin/automake-1.10

# Package install

#cat <<EOF

# Installing gSOAP deb package...

#EOF

#dpkg -i *.deb

# Cleanup

cat <<EOF

 Done... cleaning up...

EOF

cd $MY_CWD
#rm -fr ${TMP_BASE}

# vim:set ai et sts=4 sw=4 tw=80:
