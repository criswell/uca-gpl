# Helper functions used by all client agent code

# Determine what we're running. This is a bit messy, but hey, we're
# running in bash, we can't *really* use anything more advanced.
unset IS_RHEL IS_DEB IS_SLES IS_ESX IS_ANGSTROM IS_SLACK PLATFORM_NAME || true

# Given that we are running a Debian-derived distribution, find the
# specific Debian variant we are running.
find_specific_debian() {
    # For now, we just assume everything is compatible with Ubuntu,
    # this *probably* isn't the best assumption long-term, but until
    # we have customers screaming for Debian-specific installs, and
    # we find discrepencies, we'll just make due
    PLATFORM_NAME="ubuntu"
}

# Given that we are running a RedHat-derived distribution, find the
# specific RedHat variant we are running.
find_specific_redhat() {
    # Check for RHEL
    egrep -i "red hat enterprise" /etc/redhat-release > /dev/null
    if [ $? -ne 0 ]; then
        # Okay, let's see if we're CentOS
        egrep -i "centos" /etc/redhat-release > /dev/null
        if [ $? -ne 0 ]; then
            egrep -i "xen" /etc/redhat-release > /dev/null
            if [ $? -ne 0 ]; then
                # Hmm, we don't know what to do here... Perhaps we should
                # exit with failure
                echo "ERROR! Unsupported Red Hat derivative!"
                echo "Check /etc/redhat-release for more information!"
                exit 1
            else
                # We're Xen
                PLATFORM_NAME="xen"
            fi
        else
            # We're CentOS
            PLATFORM_NAME="centos"
        fi
    else
        # We're RHEL
        PLATFORM_NAME="rhel"
    fi
}

# Given that we are running a SuSE-derived distribution, find the
# specific SuSE variant we are running.
find_specific_suse() {
    # TODO - Right now we don't do much of anything here
    PLATFORM_NAME="suse"
}

find_specific_esx() {
    egrep -i "esxi" /etc/issue > /dev/null
    if [ $? -ne 0 ]; then
        PLATFORM_NAME="esxi"
    else
        PLATFORM_NAME="esx"
    fi
}

find_specific_angstrom() {
    # TODO - Right now, we assume that our only angstrom-based distro is
    # XenClient. In the future, if we encounter exceptions to this, we will
    # want to add alternate checks here
    PLATFORM_NAME="xenclient"
}

# Given we're running a slackware derived distribution, determine more exactly
# what we're running.
find_specific_slack() {
    if [ -f "/etc/slax-version" ]; then
        PLATFORM_NAME="slax"
    else
        PLATFORM_NAME="slackware"
    fi
}

if [ -f "/etc/debian_version" ]; then
    find_specific_debian
    IS_DEB=yes
elif [ -f "/etc/redhat-release" ]; then
    find_specific_redhat
    IS_RHEL=yes
elif [ -f "/etc/novell-release" ] || [ -f "/etc/SuSE-release" ]; then
    find_specific_suse
    IS_SLES=yes
elif [ -f "/etc/angstrom-version" ]; then
    find_specific_angstrom
    IS_ANGSTROM=yes
elif [ -f "/.emptytgz" ]; then
    find_specific_esx
    IS_ESX=yes
elif [ -f "/etc/slackware-version" ]; then
    find_specific_slack
    IS_SLACK=yes
fi

# Helper functions
trace() {
    DATESTAMP=$(date +'%Y-%m-%d %H:%M:%S %Z')
    echo "${DATESTAMP} : ${*}" >> ${STANDARD_LOG_FILE}
}

trace_error() {
    DATESTAMP=$(date +'%Y-%m-%d %H:%M:%S %Z')
    echo "${DATESTAMP} : ${*}" >> ${ERROR_LOG_FILE}
}

date_utc_stamp() {
    date --utc --date "$1" +%s
}

date_utc_stamp_delta() {
    case $1 in
        -s)
            SEC=1
            shift
            ;;
        -m)
            SEC=60
            shift
            ;;
        -h)
            SEC=3600
            shift
            ;;
        -d)
            SEC=86400
            shift
            ;;
        *)
            SEC=86400
            ;;
    esac
    DTE1=$1
    DTE2=$2
    DELTA=$((DTE2-DTE1))
    if ((DELTA < 0)); then VEC=-1; else VEC=1; fi
    echo $((DELTA/SEC*VEC))
}

get_system_ip() {
    # FIXME - Right now, this will only work for systems with one ethernet
    # adapter!
    /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'
}

is_hosts_setup() {
    STAT=$(sed '/## EIL_BEGIN/,/## EIL_END/!d' /etc/hosts)
    if [ -n "$STAT" ]; then
        return 0
    else
        return 1
    fi
    # We'll never get here
    return 1
}

# vim:set ai et sts=4 sw=4 tw=80:
