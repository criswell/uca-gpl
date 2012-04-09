EIL Unified Client Agent Documentation                         {#mainpage}
======================================

Introduction
============

This is the documentation for the EIL Unified Client Agent (UCA). The Unified
Client Agent is a cross-platform application which currently runs under Windows
and a variety of Linux distributions to provide interaction with the central
EIL Portal through a system known as "CCMS" or "RMS". The Unified Agent has the
following features:

 * Performs post-provisioning setup and configuration.

 * Accepts and executes commands sent from Portal through CCMS.

 * Manages platform-specific utilities and features associated with the Portal.

## Project History

Originally the EIL project  had two client agents, one for Linux and one for
Windows. The Windows client came first and was written as a monolithic C#
service which utilized a variety of external BATCH and VB scripts. The Linux
client came later and featured a modular design separating the core CCMS
interaction functionality from the platform-specific command implimentations
(here, "platform-specific" refers to isolated distribution code). The Linux
client's core was written in C/C++ and the command implimentations were in
shell, sed, awk, and Python scripts.

Having two agents made maintaining and improving them more difficult, and it
had long been a desired goal to unify them. However platform limitations
prevented each agent from being successfully ported to the other platform.

In September 2011, plans were formed to create a new Unified Agent which could
be platform agnostic. After researching options, it was decided that writing
this Unified Agent in Python and heavily reusing platform-specific code from
the previous agents made the most sense, and in November 2011 work began. The
first production release of the Unified Client Agent was on March 28, 2012.

Development Environment
=======================

The Unified Agent is not developed in any specific IDE. It is meant to be
developed in whatever editor environment a developer wishes to use. The only
requirement is that any cruft-files which an editor or IDE produces which are
not necessary for the project should not be tracked in the repository, and, in
fact, should be added to the ignore file (for example, if someone wishes to use
VisualStudio under Windows, then the project files should probably not be
tracked).

## Mercurial (Source Code Management and Version Control)

Mercurial (hg) was chosen as the distributed version control system (DVCS)
because of its cross-platform nature and ease of use. It should be available on
your development platform of choice, but can also be found online at its
homepage here:

* <http://mercurial.selenic.com/>

If you are new to hg, then you should probably familiarize yourself with
the guides and tutorials available on the following pages:

* <http://mercurial.selenic.com/guide/>

* <http://mercurial.selenic.com/wiki/Tutorial>

* <http://hgbook.red-bean.com/read/>

### Branches, tags and naming conventions

Inside of our Mercurial repository, we will adhere to the following naming
conventions:

* Tagging - Tags will be used for major releases and will be the same as the
version

* Branches - Branches will be used for experimental and/or disruptive
changes that might break the code. The general branch
"bigdev" is used for any large and disruptive changes and
can be re-used, provided no active development is currently
going on in it.

## Python considerations

The Unified Agent was developed against Python 2.x with Python 2.5 being the
minimum version required. The Unified Agent currently has not been tested
against Python 3.x, and it is safe to assume it will not run correctly there.

### virtualenv development

It's generally a good idea to isolate the development environment. One possible
tool to help isolate it is the [virtualenv][] tool. See the documentation on
the virtualenv website for setting up your Virtual Python Development
Environment.

  [virtualenv]: http://www.virtualenv.org/en/latest/index.html

virtualenv can be used under both Windows and Linux to isolate development.

### Linux development

Under Linux you can either use virtualenv to isolate your development
environment, or you can use the classic Unix chroot. If you choose to use
chroot, there are scripts and tools available inside the Unified Agent
repository to help set up and maintain your chroot development environment.
These tools are holdovers from the old Linux Client Agent, but they are still
valid and useful for the Unified Agent.

#### Using the chroot script

Included in the repository is a script which will set up a chroot build and
development environment in either a Debian/Ubuntu install, or a 

. The script's name is
"build_chroot.sh", and takes a single parameter specifying the path to the
chroot to build, e.g.:

        # ./build_chroot.sh /path/to/work/chroots/lucid-buildenv

#### Using the setup_env.sh script

Included in the source repository is the current gSOAP source tree used by
the Linux client agent as well as a script called 'setup_env.sh' which can be
used to automatically set-up a Debian-based distribution (such as Ubuntu) for
development and building of the EIL Linux client agent.

This script must be run as root, and must be run on a Debian-derived system.
Running on another system (even if that system has apt available on it) will have
undefined results.

The script is not entirely automated, and will require some user intervention
during key moments. It is recommended that you read the instructions carefully.

#### Using the chroot wrap script

Maintaining and changing into your chroot build environment can be tedious,
especially if you are working from a laptop or an otherwise isolated development
environment. Thus, the 'chroot_wrap.sh' script was created to automate some of
the tasks which can be tricky to remember when working with chroots.

This script must be run as root and takes a single argument- the path to a
previously set up chroot build environment (see section "2.a" above). Once
completed, you will be left inside the chroot environment ready to work.

        host-env ~/work/path/# ./chroot_wrap.sh /home/sam/work/intel/chroots/testing
        ... (script runs)
        chroot-env /# _
        ... (everything is now in the chroot)
