import logging
import os
from types import *
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
        ClientAgentState.CLIENTAGENT_ROOT = 'C:\\eil'
        logging.basicConfig(filename='%s\\clienagent.log' % ClientAgentState.CLIENTAGENT_ROOT,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        # Our root will be defined by previously issued LANANA/LSB requirements
        CLIENTAGENT_ROOT = '/opt/intel/eil/clientagent/'
        fn = '%s/home/client-agent-base.log' % ClientAgentState.CLIENTAGENT_ROOT
        try:
            stream = os.popen('/opt/intel/eil/clientagent/tools/clientagent-helper.sh --stdlog')
            output = stream.readlines()
            stream.close()

            if len(output) == 1:
                fn = output[0]
        finally:
            stream.close()

        logging.basicConfig(filename=fn,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ClientAgentState.CONFIG = Config(ClientAgentState.CLIENTAGENT_ROOT)
    debug_level = 2
    if(ClientAgentState.CONFIG.C.has_option('main', 'debug')):
        _debug_level = ClientAgentState.CONFIG.C.get('main', 'debug')
        try:
            debug_level = int(_debug_level)
        except:
            pass

    if debug_level < 1:
        logging.setLevel(logging.CRITICAL)
    elif debug_level = 1:
        logging.setLevel(logging.ERROR)
    elif debug_level = 2:
        logging.setLevel(logging.WARN)
    elif debug_level = 3:
        logging.setLevel(logging.INFO)
    else:
        # Anything higher will be debug to full
        logging.setLevel(logging.DEBUG)

    ClientAgentState.INIT_SETUP = True

def get_config():
    '''
    Returns the config instance
    '''
    return ClientAgentState.CONFIG

# vim:set ai et sts=4 sw=4 tw=80:
