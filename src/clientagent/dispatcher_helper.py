'''
dispatcher_helper.py
--------------------
Any helper functions for the dispatcher that do not fit in the main module.
'''

import os
import logging
from clientagent import ClientAgentState

# Linux specific methods

def linux_ExecuteCommand(command):
    '''
    Takes a command and executes the external dispatcher script with it. It
    does not sanity check this command- it relies upon either the caller or the
    dispatcher script to filter out incorrect commands.

    Will return the result.

    @param command A string containing the command needed by the dispatcher
    @returns True on success. False on failure.
    '''
    logger = logging.getLogger('linux_ExecuteCommand')
    command_file = "%s/%s" % (ClientAgentState.COMDIR, command)

    logger.debug('Placing command file %s' % command_file)

    try:
        f = open(command_file, 'w')
        f.truncate()
        # The current dispatcher specification under Linux is that the content
        # of this file is meaningless. However, we do reserve the right to
        # modify that spec in the future so we can pass command values.
        f.write('foo')
        f.close()

        dispatcherPath = '%s/clientagent-dispatcher.sh' % ClientAgentState.BINDIR

        logger.debug('Executing dispatcher %s' % dispatcherPath)

        try:
            # FIXME, do we need to use the script elevator here?
            stream = os.popen(dispatcherPath)
            output = stream.readlines()
            stream.close()

            # FIXME - Once we start parsing output from dispatcher, we should
            # do something with output
            return True
        except:
            logger.critical('Error executing dispatcher script')
            return False
        finally:
            stream.close()
    except:
        logger.critical('Error touching command file')
        return False
    finally:
        f.close()

# vim:set ai et sts=4 sw=4 tw=80:
