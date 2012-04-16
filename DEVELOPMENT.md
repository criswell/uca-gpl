Development Overview                                            {#devdoc}
====================

* [Design Philosophy](#phil)
* [Design Patterns}(#pattern)
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
required reworking the central loop. For the Unified agent, we tried
to avoid this problem by using entities we call "atoms".

Each atom is derived from the atom base class, @ref atoms