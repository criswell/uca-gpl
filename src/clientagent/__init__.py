import logging
import os
from clientagent.common.platform_id import PlatformID
from clientagent.common.config import Config

class ClientAgentState:
    '''
    Very basic state machine used by various client agent modules.
    '''
    INIT_SETUP = False
    CLIENTAGENT_ROOT = ""
    CONFIG = None

if not ClientAgentState.INIT_SETUP:
    platformID = PlatformID()

    # Set up the logging filename
    # FIXME - What do we want for a debug mode? Would be nice if we could run
    # from command-line and have the logging go to stdout
    if platformID.IS_WINDOWS:
        # FIXME - Will want this to be the same log we have used previously
        CLIENTAGENT_ROOT = 'C:\\eil'
        logging.basicConfig(filename='%s\\clienagent.log' % CLIENTAGENT_ROOT)
    else:
        # Our root will be defined by previously issued LANANA/LSB requirements
        CLIENTAGENT_ROOT = '/opt/intel/eil/clientagent/'
        fn = '%s/home/client-agent-base.log' % CLIENTAGENT_ROOT
        try:
            stream = os.popen('/opt/intel/eil/clientagent/tools/clientagent-helper.sh --stdlog')
            output = stream.readlines()
            stream.close()

            if len(output) == 1:
                fn = output[0]
        finally:
            stream.close()

        logging.basicConfig(filename=fn)

    ClientAgentState.CONFIG = Config()

    ClientAgentState.INIT_SETUP = True

def get_config():
    '''
    Returns the config instance
    '''
    return ClientAgentState.CONFIG.C

# vim:set ai et sts=4 sw=4 tw=80:
