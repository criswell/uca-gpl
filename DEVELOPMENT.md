Development Overview                                            {#devdoc}
====================

* [Design Philosophy](#phil)
* [Design Patterns](#pattern)
    * [Client agent state machine](#statemachine)
    * [Atoms](#atoms)
    * [CCMS Update Steward and Dispatcher](#stewdisp)

Documentation authors: *Sam Hart*

--------------------------------------------------------------------------

Design Philosophy                                               {#phil}
=================

The major cross-platform design philosophy utilized in the Unified client
agent is separation of platform-specific code from platform-agnostic code.
When it's at all possible, code that is specific to a given platform
should be isolated from more general code that runs on multiple platforms.
A great example of where this philosophy can be seen is in the
[EILAsset](@ref clientagent.steward.asset.EILAsset) class and the two, platform-
specific classes derived from it.

The [EILAsset](@ref clientagent.steward.asset.EILAsset) class defines base,
platform agnostic code which describes the asset data structure and methods
for interfacing with CCMS. However, it does not define any logic for collecting
asset information and populating the asset data structure as that logic would
be highly platform-specific. Instead, it defines two abstract methods,
[EILAsset.initialize](@ref clientagent.steward.asset.EILAsset.initialize) and
[EILAsset.updateAsset](@ref clientagent.steward.asset.EILAsset.updateAsset),
which should be overridden with the platform-specific logic for asset
collection.

Meanwhile, the derived classes
[Linux_Asset](@ref clientagent.steward.linux_asset.Linux_Asset) and
[Win32_Asset](@ref clientagent.steward.win32_asset.Win32_Asset) derive from
[EILAsset](@ref clientagent.steward.asset.EILAsset) and override the initialize
and updateAsset methods with logic specific to Linux and Windows respectively.

By abstracting out the agnostic logic from platform-specific logic, we hope
that we will both produce cleaner code as well as reduce code duplication.

Design Patterns                                                 {#pattern}
===============

This section describes various design patterns we've used in the Unified
agent codebase.

## Client agent state machine                                   {#statemachine}

The client agent state machine,
[ClientAgentState](@ref clientagent.ClientAgentState), is where anything that
must be available for random sub-systems of the client agent should go. In
many regards, it can be thought of as a global state machine for the client
agent. It is intended to be a static class and treated as if it were singleton,
however it is not a real singleton.

ClientAgentState should be treated as read-only. Those properties defined which
will be of most use are as follows:

* CLIENTAGENT_ROOT
    * The root directory for the client agent's installation.
* CONFIG
    * The configuration instance for the client agent. If you are expanding
      the client agent's features through the use of an [atom](#atoms}, please
      do not use your own configuration system. Instead, add a sub-section to
      the client agent's configuration instance and use it. This way all of
      the client agent's settings can be found in the same place.
* SRV_NAME, SRV_DISPLAY_NAME, SRV_DESCRIPTION
    * These are strings used primarily in the Windows Service definitions.
      However, since they may be used elsewhere in the future, they are defined
      in the ClientAgentState.
* VERSION
    * The current unified client agent version string.
* COMDIR, BINDIR
    * These are largely used for compatibility under Linux for the dispatcher
      scripts. They define the commands directory as well as the binary
      directory for the client agent. They currently have no meaning under
      Windows, however they are kept in the ClientAgentState for future use.

## Atoms                                                        {#atoms}

In the previous Linux client agent we had a tight, central loop which
managed the processing of the agent's commands. The downside to this
design was that expanding it or adding new features was difficult and
required reworking the central loop. In the Windows client, we had multiple
processes for handling basic interactions with CCMS. For the Unified agent,
we tried to avoid these problems by using entities we call "atoms".

An "atom" is an object which defines some activity in the client agent which
we desire to execute atomically. Example activities include interacting with
CCMS to obtain commands, submitting asset information, and communicating with
the NMSA. The client agent holds the atoms in a queue and every loop executes
those atoms which are still active/alive. Using this atom model, we can define
an arbitrary number of activities for the client agent to manage.

> It should be noted that the client agent does not ensure atomicity in the
> atoms defined in its queue. Instead, it assumes the atom's developer is
> properly executing and setting atomic flags as necessary. The client agent
> will simply treat each atom as if it is atomic. The actual atomicity is
> an implimentation detail.

Each atom is derived from the atom base class,
[Atom](@ref clientagent.steward.atom.Atom). This base class defines a specific
way to interface with atoms in the system. These interfaces are as follows:

* [Atom.ACTIVE](@ref clientagent.steward.atom.Atom.ACTIVE)
    * The ACTIVE flag determines whether or not the atom is active. As the
      client agent runs, it is constantly checking the ACTIVE flag for each atom
      in its queue. If no atoms are active, that tells the client agent it is
      time to exit.
* [Atom.__init__()](@ref clientagent.steward.atom.Atom.__init__)
    * The constructor for the atom. This is, obviously, called at process start
      up. It is safe to assume that the various client agent properties have
      been set in [ClientAgentState](@ref clientagent.ClientAgentState).
* [Atom.shutdown()](@ref clientagent.steward.atom.Atom.shutdown)
    * This method is called when the client agent is shutting down. It will not
      be called when the atom is set inactive. Note that you cannot assume your
      shutdown method will always be called due to the various ways in which
      the system running the client agent can be restarted or halted. The
      shutdown method should be considered a "best case scenario" type of
      operation.
* [Atom.update(timeDelta)](@ref clientagent.steward.atom.Atom.update)
    * This method is called every loop and should be the entry point for your
      atom's activities. It is here where the majority of your atom's logic
      should go. The update method will try to be called once every 30 seconds,
      although this is not guaranteed. The timeDelta parameter gives the true
      time elapsed since last update was called.

## CCMS Update Steward and Dispatcher                          {#stewdisp}

The CCMS update operation, which is arguably the most significant feature of
the client agent, is split between two major code-blocks:

* Steward:
    * The steward defines the basic interactions with CCMS. Its logic can be
      found in the [CCMS_Update](@ref clientagent.steward.ccmsupdate.CCMS_Update)
      class. The steward should be as platform-agnostic as possible.
* Dispatcher:
    * The dispatcher handles the platform-specific command executions when the
      steward receives commands from CCMS. The abstract dispatcher interfaces
      can be found in the [Dispatcher](@ref clientagent.dispatcher.Dispatcher)
      class, but some additional, platform-specific code can be found in
      [dispatcher_helper](@ref clientagent.dispatcher_helper) and in
      [commandhandler](@ref clientagent.steward.commandhandler).

> The steward/dispatcher distinction is partially legacy from the Linux client
> agent and partially required for full Linux support.

> Linux is an inhomogeneous platform, and we aim to support a very wide-range of
> Linux distributions. Thus, operations that might be simple under a more
> homogeneous platform like Windows can become much more bifurcated under Linux.

> To accomodate this, the Linux-agnostic operations were split out into the
> steward and the Linux-specific operations were handled by a series of shell
> scripts known as the dispatcher. This is how the previous Linux client agent
> worked.

> Today, the unified agent re-uses all of the Linux client agent dispatcher
> shell scripts for handling commands passed down from CCMS in much the same
> way they were used previously, however since the agent is unified some
> dispatcher logic can be found inside the above files for both Windows and
> Linux.

> Basically, anything that can be easily handled in the unifed agent's Python
> code-base should, but anything that reflects the bifurcated nature detailed
> previously will be offloaded to the Linux dispatcher scripts.
