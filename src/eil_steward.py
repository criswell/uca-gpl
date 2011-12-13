#!/usr/bin/env python

'''
steward.py
----------
The steward is the main control daemon that acts as the communicator link
between the client agent and CCMS.
'''

import sys, logging, time
from clientagent.common.platform_id import PlatformID
from clientagent import ClientAgentState

platformId = PlatformID()
if platformId.IS_WINDOWS:
    import win32serviceutil
    from clientagent.steward.libdaemon.windows_service import Service as Daemon
else:
    # Linux
    from clientagent.steward.libdaemon.unix_daemon import Daemon

class StewardHandler(Daemon):
    # TODO - determine if we want this to be variable based upon config
    __sleep_timer = 30
    __min_time_resolution = 15

    def local_init(self):
        self.logger = logging.getLogger()
        self.logger.info("-----------------------------------");
        self.logger.info(ClientAgentState.SRV_DISPLAY_NAME);
        self.logger.info("Version: %s" % ClientAgentState.VERSION);
        # Setup the atom queue
        self.atoms = [] # FIXME TODO


    def local_shutdown(self):
        pass

    def run(self):
        self.logger.info("Startup daemon/service");
        timeDelta = self.__sleep_timer
        while True:
            start_time = time.time()
            self.logger.debug('Starting client agent activity')
            for a in self.atoms:
                a.update(timeDelta)

            wait_time = self.__sleep_timer - (time.time() - start_time)

            if wait_time < self.__min_time_resolution:
                wait_time = self.__min_time_resolution

            time.sleep(wait_time)
            timeDelta = time.time() - start_time
            if timeDelta < self.__sleep_timer:
                timeDelta = self.__sleep_timer

def usage_linux():
    print "Usage:\n"
    print "\teil_steward.py COMMAND"
    print "\t\twhere 'COMMAND' is one of the following:\n"
    print "\tstart\t\tStart the daemon/service"
    print "\tstop\t\tStop the daemon/service"
    print "\trestart\t\tRestart the daemon/service"

def usage_win():
    pass

if __name__ == "__main__":
    if platformId.IS_WINDOWS:
         daemon = StewardHandler(sys.argv)
         win32serviceutil.HandleCommandLine(daemon)
    else:
        # Linux
        daemon = StewardHandler()
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
            usage_linux()
            sys.exit(2)

# vim:set ai et sts=4 sw=4 tw=80:
