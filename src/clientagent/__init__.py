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
    # The following are largely used in the Win32 service APIs, but provided
    # in case we find a use for them elsewhere
    SRV_NAME = "EILClientAgent"
    SRV_DISPLAY_NAME = "EIL Client Agent"
    SRV_DESCRIPTION = "EIL Portal Unified Client Service (Python) - resides on client - interfaces with CCMS"
    # Version information FIXME would be nice to generate programatically
    VERSION = "4.3.0.1.d20111011"

    # Various Linux-isms we need for compatibility with the dispatcher scripts
    COMDIR = None
    BINDIR = None

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
        ClientAgentState.CLIENTAGENT_ROOT = '/opt/intel/eil/clientagent'
        fn = '%s/home/client-agent-base.log' % ClientAgentState.CLIENTAGENT_ROOT
        try:
            stream = os.popen('/usr/bin/clientagent-helper.sh --stdlog')
            output = stream.readlines()
            stream.close()

            if len(output) == 1:
                fn = output[0]
        finally:
            stream.close()

        logging.basicConfig(filename=fn,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        comdir = '%s/home/commands' % ClientAgentState.CLIENTAGENT_ROOT
        try:
            stream = os.popen('/usr/bin/clientagent-helper.sh --comdir')
            output = stream.readlines()
            stream.close()

            if len(output) == 1:
                comdir = output[0]
        finally:
            stream.close()

        ClientAgentState.COMDIR = comdir

        bindir = '%s/bin' % ClientAgentState.CLIENTAGENT_ROOT
        try:
            stream = os.popen('/usr/bin/clientagent-helper.sh --bin')
            output = stream.readlines()
            stream.close()

            if len(output) == 1:
                bindir = output[0]
        finally:
            stream.close()

        ClientAgentState.BINDIR = bindir

    ClientAgentState.CONFIG = Config(ClientAgentState.CLIENTAGENT_ROOT)
    debug_level = 2
    if(ClientAgentState.CONFIG.C.has_option('main', 'log_level')):
        _debug_level = ClientAgentState.CONFIG.C.get('main', 'log_level')
        try:
            debug_level = int(_debug_level)
        except:
            pass

    Logger = logging.getLogger()

    if debug_level < 1:
        Logger.setLevel(logging.CRITICAL)
    elif debug_level == 1:
        Logger.setLevel(logging.ERROR)
    elif debug_level == 2:
        Logger.setLevel(logging.WARNING)
    elif debug_level == 3:
        Logger.setLevel(logging.INFO)
    else:
        # Anything higher will be debug to full
        Logger.setLevel(logging.DEBUG)

    ClientAgentState.INIT_SETUP = True

def get_config():
    '''
    Returns the config instance
    '''
    return ClientAgentState.CONFIG

# vim:set ai et sts=4 sw=4 tw=80:
