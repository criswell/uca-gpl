#!/usr/bin/env python

'''
steward.py
----------
The steward is the main control daemon that acts as the communicator link
between the client agent and CCMS.
'''

# Before we begin, we need to properly set up paths
import os, sys
if os.name == 'nt':
    sys.path.append('C:/EIL/bin')
else:
    sys.path.append('/opt/intel/eil/clientagent/bin')

import logging, time

from clientagent.common.platform_id import PlatformID
from clientagent.common.utility import getIfInfo
from clientagent.common.utility import exec_command
from clientagent import ClientAgentState
from clientagent.steward.ccmsupdate import CCMS_Update
from clientagent.steward.configwatch import ConfigWatch
from clientagent.steward.assetupdate import AssetUpdate

platformId = PlatformID()
if platformId.IS_WINDOWS:
    import win32serviceutil
    from clientagent.steward.libdaemon.windows_service import Service as Daemon
    from clientagent.steward.win32_asset import Win32_Asset as EILAsset
else:
    # Linux
    from clientagent.steward.libdaemon.unix_daemon import Daemon
    from clientagent.steward.linux_asset import Linux_Asset as EILAsset

class StewardHandler(Daemon):
    # TODO - determine if we want this to be variable based upon config
    __sleep_timer = 30
    __min_time_resolution = 15

    def local_init(self):
        self.logger = logging.getLogger('steward')
        self.logger.info("-----------------------------------");
        self.logger.info(ClientAgentState.SRV_DISPLAY_NAME);
        self.logger.info("Version: %s" % ClientAgentState.VERSION);
        # Setup the atom queue
        self.atoms = [
            ConfigWatch(),
            CCMS_Update(),
            AssetUpdate(),
        ]

    def local_shutdown(self):
        self.logger.info("Shutting down");
        for a in self.atoms:
            if a.ACTIVE:
                a.shutdown()

    def run(self):
        self.logger.info("Startup daemon/service");
        timeDelta = self.__sleep_timer

        start_time = time.time()
        self.logger.debug('Starting client agent activity')

        aliveCount = 0
        for a in self.atoms:
            if a.ACTIVE:
                a.update(timeDelta)
                aliveCount = aliveCount + 1

        if aliveCount > 0:
            self.logger.info('Activities done, sleeping')
            wait_time = self.__sleep_timer - (time.time() - start_time)

            if wait_time < self.__min_time_resolution:
                wait_time = self.__min_time_resolution

            self.logger.debug('Sleeping "%s"' % wait_time)
            time.sleep(wait_time)
            timeDelta = time.time() - start_time
            if timeDelta < self.__sleep_timer:
                timeDelta = self.__sleep_timer
            return True
        else:
            self.logger.info('No more active process atoms. Agent exit.')
            return False

def usage_linux():
    print "Usage:\n"
    print "\teil_steward.py COMMAND"
    print "\t\twhere 'COMMAND' is one of the following:\n"
    print "\tstart\t\tStart the daemon/service"
    print "\tstop\t\tStop the daemon/service"
    print "\trestart\t\tRestart the daemon/service"
    print "\tdebug\t\tStart the daemon/service in debug mode"
    print "\tstatus\t\tReturn running status of the daemon/service"
    print "\tasset\t\tDump the system asset XML"
    print "\tupgrade\t\tForce an auto-upgrade of the agent"

def usage_win():
    pass

if __name__ == "__main__":
    if 'asset' in sys.argv:
        (mac, hostName) = getIfInfo()
        asset = EILAsset()
        print asset.getAssetXML(hostName)
    if 'upgrade' in sys.argv:
        output = exec_command('python %s' % os.path.join(ClientAgentState.CLIENTAGENT_ROOT, 'tools', 'uca-bootstrap.py'))
        for line in output:
            print line
    else:
        if platformId.IS_WINDOWS:
            win32serviceutil.HandleCommandLine(StewardHandler)
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
                elif 'debug' == sys.argv[1]:
                    daemon.start(True)
                elif 'status' == sys.argv[1]:
                    daemon.status()
                else:
                    print "Unknown command"
                    sys.exit(2)
                sys.exit(0)
            else:
                usage_linux()
                sys.exit(2)

# vim:set ai et sts=4 sw=4 tw=80:
