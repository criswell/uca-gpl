Installation Overview                                            {#installdoc}
=====================

* [Understanding the install process](#overview)
    * [High level overview](#hilevel)
    * [Manual installation](#maninstall)
* [The installation process in more detail](#instdet)
    * [uca-bootstrap.py](#bootstrap)
        * [uca.zip](#zipfile)
    * [uca-installer.py](#installer)

Documentation authors: *Sam Hart*

------------------------------------------------------------------------------

Understanding the install process                                {#overview}
=================================

The unified client agent needed to have a common way to install on a variety of
platforms. The install process needed to not only operate under a variety of
Windows flavors, but also under a very wide range of Linux distrubutions. It
also needed to install the agent and its utilities in very specific locations.
Under Windows, the previous convention of "C:\EIL" as the install root was
necessary for compatibility with other EIL tools. Under Linux, we wanted to
conform to [LFHS](http://www.pathname.com/fhs/),
[LSB](http://www.linuxfoundation.org/collaborate/workgroups/lsb/group) and
[LANANA](http://stewbenedict.org/lsb/lanana/) conventions whenever possible
(and whenever it doesn't conflict with previously stated goals). Further, under
Linux we previously had LFHS and LSB defined paths which we wanted to keep for
compatibility. Additionally, we needed a clear and reliable way not only to
uninstall the client agent cross-platform, but also paths for upgrades and
re-installs.

Because of these reasons, we could not utilize other standard installation
methods for Python applications nor could we utilize platform-specific install
solutions such as Py2EXE installers under Windows or package files under Linux.
Instead, we had to come up with our own cross-platform installer and upgrader
for the unified client agent.

## High level overview                                          {#hilevel}

From a very high level, here's the general install process for the unified
agent.

* A bootstrapper tool first checks for compatibility, then attempts to set up
  the installation environment. It then downloads a cross-platform package
  (zip file) from a known location.
* Inside the cross-platform package is the unified agent and an installer. The
  bootstrapper extracts the package and executes the installer.
* The installer does the following:
    * It performs additional sanity checks on the system and the package.
    * It shuts down and disables any previous version of the unified agent, or
      platform-specific agents (Linux client agent or Windows client agent).
    * It backs up any configuration files from previous installs.
    * It does a best effort to un-install any previous agents.
    * It ensures that the correct install tree is set up.
    * It ensures that the system's hosts file is properly set for the CCMS and
      NMSA IPs.
    * It installs the unified agent from the archive.
    * Any additional platform-specific tools are installed.
    * The previous configuration files are restored.
    * The unified agent is started, and the installer cleans up after itself.

The bootstrapper/installer combination are intended to be used on supported
systems for fresh installs, re-installs, and upgrades.

## Manual installation                                          {#maninstall}

To install the unified agent by hand, simply execute the bootstrap tool
as an administrator ("Administrator" under Windows, or "root" under Linux).
Download the latest bootstrap from the production IP address, and execute
it:

    # python uca-bootstrap.py

Refer to the more detailed installation instructions found inside the unified
agent's repository in the document:

    docs/tests/test-document.odt

The installation process in more detail                         {#instdet}
=======================================

## "uca-bootstrap.py"                                           {#bootstrap}

The bootstrapper, defined in @ref uca-bootstrap, performs basic bootstrapping
of the installation environment for the unified agent. It is intended to be a
very simple script with the bulk of the installation logic contained in a
separate installer. The reason for this is that by keeping the bootstrapper
simple it will not need to be updated often, which means it can be used to
upgrade arbitrary client agent installs to the latest version regardless of
how old the install is.

Production and staging IPs are defined for where the unified agent installer
can be found in the [PRODUCTION_IP](@ref uca-bootstrap.PRODUCTION_IP) and
[STAGING_IP](@ref uca-bootstrap.STAGING_IP) variables set in the bootstrapper.
The bootstrapper can be told which to use by toggling the
[IS_PRODUCTION](@ref uca-bootstrap.IS_PRODUCTION) boolean.

The bootstrapper uses Python's logging framework to log all of its actions to
a log file. This log file is stored in the root directory of the filesystem
("C:\" if Windows, or "/" if Linux). It also outputs the log to STDOUT so that
anyone manually running it can see the actions. The log file will be moved into
the unified agent's root directory after installation is successful.

The bootstrapper goes to the IP address defined above and attempts to download
the file "uca.zip" from there. This is a specially formatted zip archive meant
to only be consumed by the bootstrap tool.

> NOTE: The bootstrap tool can be pointed to a local copy of the "uca.zip" file
> by passing the local path to the file as an optional parameter to the script:

    # python uca-bootstrap.py /path/to/local/uca.zip

Once the bootstrapper has downloaded the zip file, it will extract it to a
tempoary directory and execute the [installer](#installer) contained inside.

### "uca.zip"                                                   {#zipfile}

The format of the uca zip file is very specific. It must adhere to the standard
set here. The best way to ensure that is to use the "uca-builder" script
described below.

        .
        |-- bin
        |   |-- TODO
        |   |-- clientagent
        |   |   |-- ....
        |   |   `-- steward
        |   |       |-- ....
        |   |-- eil_steward.py
        |   |-- elevate_script
        |   |-- suds
        |   |   `-- ....
        |   `-- tests
        |       `-- ....
        |-- lib
        |   `-- VERSION
        |-- linux
        |   `-- dispatcher
        |       `-- ...
        |-- tools
        |   |-- uca-bootstrap.py
        |   `-- uca-installer.py
        |-- uca-bootstrap.py
        |-- uca-installer.py
        `-- windows
            `-- ....

Inside the zip file, at the top level there must be the bootstrap tool as well
as the install tool. Undernath the top level you will find the following:

* bin
    * Contains the unified agent Python scripts and all necessary support
      tools, libraries, and files.
* lib
    * Currently only contains the VERSION file, however is reserved for
      additional library tools not directly included with the Python scripts
      above (e.g., library objects that are not required to be in the Python
      path).
* linux
    * Contains the dispatcher and other Linux-specific tools necessary for the
      unified agent to run under Linux.
* windows
    * Contains any Windows-specific tools necessary for the unified agent to
      run under Windows. Currently is empty, but reserved for future use.
* tools
    * Contains the installer, bootstrapper, and any other tools necessary for
      the installation and setup of the unified agent.

## "uca-installer.py"                                           {#installer}

The installer should be called with exactly one command-line argument, the full
path to the extracted zip file. The installer is not intended to be used by
hand, instead it should be executed by the bootstrap tool. The installer is
defined in the [uca-installer](@ref uca-installer) package.

Inside the installer are four very specific sections:

* Windows specific code
    * Inside this section are any and all Windows specific functions to be
      used during the installation. These functions are all named with the
      prefix "win32_".
* Linux specific code
    * Inside this section are any and all Linux specific functions to be used
      during the installation. These functions are all named with the prefix
      "linux_".
* Generic code
    * Inside this section are functions which are platform agnostic and can
      be used on either Linux or Windows. There is no special naming convention
      here.
    * Some noteworthy functions include:
        * [uca-installer.precompilePy](@ref uca-installer.precompilePy)
            * This is used to precompile the Python modules for installation.
              Those modules defined in
              [uca-installer.PRECOMPILE_EXCEPTIONS](@ref uca-installer.PRECOMPILE_EXCEPTIONS)
              will be excluded from this process.
        * [uca-installer.copyHome](@ref uca-installer.copyHome)
            * This attempts to backup the previous installation's configuration
              and log directory. It is also used to restore the backup (by
              swapping the parameters).
* Main installation logic
    * Finally, at the end of the file, you will find the main installation
      logic.
