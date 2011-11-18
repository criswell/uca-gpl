#!/usr/bin/env Python


'''
steward.py
----------
The steward is the main control daemon that acts as the communicator link
between the client agent and CCMS.
'''

from clientagent.common.platform_id import PlatformID
from clientagent import ClientAgentState

platformId = PlatformID()
if platformId.IS_WINDOWS:
    from steward.libdaemon.windows_service import Service as Daemon
else:
    # Linux
    from steward.libdaemon.unix_daemon import Daemon


# vim:set ai et sts=4 sw=4 tw=80:
