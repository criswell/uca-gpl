#!/usr/bin/env sh

# Unified Client Agent Doc Generator
# ----------------------------------
# Very simple tool for regenerating the documentation for the Unified Client
# Agent.

cat <<EOF

This script will regenerate the documentation for the unified agent. It will
overwrite the current docs/html contents with updated documentation. Use
caution when running it as cleaning it up if something goes wrong will require
an 'hg revert'.

EOF

read -p "Press [ENTER] to continue, or break to cancel : "

doxygen

cp -fr docs/build/html docs/html

# vim:set ai et sts=4 sw=4 tw=80:
