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

class StewardHandler(Daemon):

    def local_init(self):
        pass

    def local_shutdown(self):
        pass

    def run(self):
        pass

def usage():
    print "Usage:\n"
    print "\teil_steward.py COMMAND"
    print "\t\twhere 'COMMAND' is one of the following:\n"
    print "\tstart\t\tStart the daemon/service"
    print "\tstop\t\tStop the daemon/service"
    print "\trestart\t\tRestart the daemon/service"

if __name__ == "__main__":
    daemon = Daemon()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        usage()
        sys.exit(2)
    pass

# vim:set ai et sts=4 sw=4 tw=80:
