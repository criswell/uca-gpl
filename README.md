My Main Page                         {#mainpage}
============

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
the previous agents made the most sense, and in November 2011 work began.

Development Environment
=======================

Todo
