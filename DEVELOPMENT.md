Development Overview                                            {#devdoc}
====================

* [Design Philosophy](#phil)
* [Design Patterns](#pattern)
    * [Atoms](#atoms)

Documentation authors: *Sam Hart*

--------------------------------------------------------------------------

Design Philosophy                                               {#phil}
=================

The major cross-platform design philosophy utilized in the Unified client
agent is separation of platform-specific code from platform-agnostic code.
When it's at all possible, code that is specific to a given platform
should be isolated from more general code that runs on multiple platforms.

Design Patterns                                                 {#pattern}
===============

This section describes various design patterns we've used in the Unified
agent codebase.

## Atoms                                                        {#atoms}

In the previous Linux client agent we had a tight, central loop which
managed the processing of the agent's commands. The downside to this
design was that expanding it or adding new features was difficult and
required reworking the central loop. In the Windows client, we had multiple
processes for handling basic interactions with CCMS. For the Unified agent,
we tried to avoid these problems by using entities we call "atoms".

An "atom" is an object which defines some activity in the client agent which
we desire to execute atomically.

> It should be noted that the client agent does not ensure atomicity in the
> atoms defined in its queue. Instead, it assumes the atom's developer is
> properly executing and setting atomic flags as necessary. The client agent
> will simply treat each atom as if it is atomic. The actual atomicity is
> an implimentation detail.

Each atom is derived from the atom base class,
@ref clientagent.steward.atom.Atom . This base class defines a specific way to
interface with atoms in the system.