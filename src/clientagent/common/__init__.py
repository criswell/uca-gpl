import logging
import os

class ClientAgentState:
    '''
    Very basic state machine used by various client agent modules.
    '''
    INIT_SETUP = False

if not ClientAgentState.INIT_SETUP:
    platformID = PlatformID()

    # Set up the logging filename
    # FIXME - What do we want for a debug mode? Would be nice if we could run
    # from command-line and have the logging go to stdout
    if platformID.IS_WINDOWS:
        # FIXME - Will want this to be the same log we have used previously
        logging.basicConfig(filename='C:\\eil\\clienagent.log')
    else:
        # Something intelligent for a default
        fn = '/opt/intel/eil/clientagent/home/client-agent-base.log'
        try:
            stream = os.popen('/opt/intel/eil/clientagent/tools/clientagent-helper.sh --stdlog')
            output = stream.readlines()
            stream.close()

            if len(output) == 1:
                fn = output[0]
        finally:
            stream.close()

        logging.basicConfig(filename=fn)

# vim:set ai et sts=4 sw=4 tw=80:
