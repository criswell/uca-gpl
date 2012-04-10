EIL Dispatcher API Documentation                            {#shellapi}
================================

* [Overview](#sh_1)
    * [Installation location, and importing the libraries](#sh_1a)
* [The Dispatcher APIs](#sh_2)
    * ["dispatcher.sh"](#sh_2a)
    * ["globals.sh"](#sh_2b)
    * ["helper.sh"](#sh_2c)
        * [Platform specification](#sh_2c1)
        * [Logging functions](#sh_2c2)
        * [Date functions](#sh_2c3)
        * [Network functions](#sh_2c4)
    * ["logger.sh"](#sh_2d)
* [System Toggles](#sh_3)
    * [Locations and meanings of the toggles](#sh_3a)
        * [Toggles in /etc/ca_toggles](#sh_3a1)
        * [Other toggles](#sh_3a2)

Documentation author: Sam Hart

------------------------------------------------------------------------------

Overview                                                    {#sh_1}
========

The Dispatcher includes shell libraries which can be utilized in external
shell scripts. These libraries provide a number of unique features including
distribution detection and abstraction,

Installation location, and importing the libraries          {#sh_1a}
==================================================

In keeping with the Filesystem Hierarchy Standard
(http://www.pathname.com/fhs/) and LANANA (http://www.lanana.org/), the
Dispatcher libraries are installed into

        * /opt/intel/eil/clientagent/lib/

The various libraries contained in this system-wide directory can be
included in your shell script in a variety of ways. However, the most platform-
agnostic way is to use the dot-execute directive:

        DSP_LIB_PATH="/opt/intel/eil/clientagent/lib"
        . ${DSP_LIB_PATH}/helper.sh

The Dispatcher APIs                                         {#sh_2}
===================

## "dispatcher.sh"                                             {#sh_2a}

The "dispatcher.sh" library abstracts the underlying platform for running
commands. It requires the "globals.sh" library to be loaded.

## "globals.sh"                                                {#sh_2b}

This library defines a number of global variables utilized by the EIL
Dispatcher. Unless you are extending the dispatcher itself, or using some of the
internal Dispatcher functionality, you probably will not need to use anything
here.

## "helper.sh"                                                 {#sh_2c}

This library contains a number of helper features which are utilized by the
Dispatcher, but which should be general enough that arbitrary scripts can use
it as well.

### Platform specification                                      {#sh_2c1}

By simply sourcing the helper.sh script, you will gain access to information
about the underlying Linux distribution. A number of environmental variables
will be defined describing the distribution.

* IS_RHEL
* IS_DEB
* IS_SLES
* IS_ESX
* IS_ANGSTROM

One of the above will be set to 'yes' (with the others remaining unset)
which will define the general distribution flavor.

Beyond the flavor of the distribution, you can additionally check the
variable

* PLATFORM_NAME

which will contain a string detailing the more specific dialect of the
distribution.

For example, CentOS would be defined as:

* IS_RHEL=yes
* PLATFORM_NAME="centos"

### Logging functions                                       {#sh_2c2}

The helper library contains two functions for logging:

* trace()
    - This function will log to the standard client agent log file,
        which defaults to ${HOME_DIR}/client-agent-base.log .

* trace_error()
    - This function will log to the client agent error log file, which
        defaults to ${HOME_DIR}/client-agent-error.log .

### Date functions                                          {#sh_2c3}

The helper library provides a number of functions which assist in high-level
date logic.

* date_utc_stamp()
    - This function takes a parameter of a date string (or "now" to
        indicate the current time) and returns a specially formatted UTC
        stamp which can be used by the other date functions.

* date_utc_stamp_delta()
    - This function takes three parameters. The first parameter is one
        of:
            -s : second
            -m : minute
            -d : day
        The next two parameters are UTC date stamps (returned from
        date_utc_stamp). It will compute and return the delta (in whatever
        format you request) between the two date stamps.

### Network functions                                       {#sh_2c4}

The helper library provides a number of functions which assist with various
network items.

* get_system_ip()
    - This function returns the system's IP information. It requires
        working grep, cut and awk commands.

* is_hosts_setup()
    - This function queries the /etc/hosts file to verify whether or
        not the EIL entries are in place. It returns 0 upon success
        (meaning the entries are there) or 1 on failure (meaning the
        entries are not there).

        The main reason this function exists (though it can easily have
        uses elsewhere) was because of a need on XenClient where the
        hosts file was being destroyed at odd times after boot causing
        TCP diagnostic script runs which resulted in Linux client agent
        hangs.

## "logger.sh"                                              {#sh_2d}

Access to the Linux client agent's logging facilities by external
applications can be found through the logger.sh script. This script is located
in the tools/ directory under the install directory (typically
/opt/intel/eil/clientagent/tools). The usage for this script is as follows:

    Usage: logger.sh [OPTION] <log message>
    Where:
        <log message>   - is your log message
        [OPTION]        - is one of the following

        --std           Log the message to the standard client agent dispatcher log
                        (default when called with no options).

        --err           Log the message to the client agent dispatcher error log.

        --echo          Echo the message back to STDOUT in addition to whatever
                        else it may be doing.

        --nostd         Disable standard client agent dispatcher logging (use in
                        combination with '--echo' if you wish you only log to
                        STDOUT)

So, if you wanted to log the message "Error during operation FOO" to the
client agent's error logs from an external application, you would call the
logger.sh script with the following parameters:

    logger.sh --err Error during operation FOO

System Toggles                                              {#sh_3}
==============

There are several system-wide toggles which affect the behavior of the
various components of the client agent. This section defines what they are and
what they mean.

## Locations and meanings of the toggles                    {#sh_3a}

### Toggles in /etc/ca_toggles                              {#sh_3a1}

Most toggles for the client agent can be found in /etc/ca_toggles. These
toggles are as follows:

* /etc/ca_toggles/no_init
    This determines that a system should not have the client agent
    components start at boot. During the installation process, a post-
    install script will check for this and disable the init scripts.

* /etc/ca_toggles/ac_image
    This determines that an install is for an asset collection image.
    When a new system is added to the cloud, the client agent needs to
    run, collect asset information on the system and then report that
    information to CCMS. Once this is done, the system should reboot
    for normal provisioning. This toggle should be set on the asset
    collection image to trigger this.

### Other toggles                                           {#sh_3a2}

* /opt/intel/eil/clientagent/home/.nmsa_enable
    This determines whether or not NMSA is to be enabled. This is
    automatically set during installation, but you can override it
    by removing or touching this file.
