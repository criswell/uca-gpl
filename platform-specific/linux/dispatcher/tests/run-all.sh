#!/usr/bin/env bash

# run-all.sh
# ----------
# Run all the tests

# List of all tests
ALL_TESTS=$(cat <<EOF
helper-verify.sh
install-verify.sh
elevate-build-verify.sh
steward-build-verify.sh
asset-helper-verify.sh
EOF
)

COLOR_RESET='\e[0m'
COLOR_TRACE='\e[1;33m' # Yellow

TMP_TIMESTAMP=`mktemp`

trace () {
    echo -e "${COLOR_TRACE}$*${COLOR_RESET}"
}

clock_tick() {
    date +%s.%N >> $TMP_TIMESTAMP
}

trace "!!! Run all tests"

clock_tick

for TEST_FILE in $ALL_TESTS
do
    ./${TEST_FILE}
done

clock_tick

TOTAL_TIME=`awk '{ if (!start) { start = $1 } else { print $1-start } }' < $TMP_TIMESTAMP`

rm -f $TMP_TIMESTAMP

trace "!!! Total time ran was $TOTAL_TIME seconds"

# vim:set ai et sts=4 sw=4 tw=80:
