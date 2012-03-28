'''
commandhandler.py
-----------------
Contains the command hanlding routines which previously were cluttering up
the CCMS Update loop.
'''

import time

def handleReboot(ccmsUpdate, ctx, result, txID):
    '''
    Handles the reboot requests and acknowledgements.

    @param ccmsUpdate The CCMS Update atom caller.
    @param dispatcher The dispatcher instanct.
    @param result The result from the CCMS update call
    '''
    commandName = result.CommandName
    ccmsUpdate.ACKclient = ccmsUpdate.setStatusUpdateHeaders(ccmsUpdate.ACKclient, txID)
    #rebcode = ccmsUpdate.dispatcher.reboot('CCMS Reboot', 10)
    '''
    if rebcode:
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr,  rOID, rmt)
    else:
        rstat = 'COMMAND_FAILED'
        rsuc = False
        rresult = None
        rerr = 'reboot failed'
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr,  rOID, rmt)
    '''
    rstat = 'COMMAND_EXECUTION_COMPLETE'
    rsuc = True
    rresult = 0
    rerr = result.ErrorCode
    rtime = result.ExpectedTimeOut
    rOID = result.OperationID
    rmt= result.SetMachineType
    cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr,  rOID, rmt)
    ACKresult = ccmsUpdate.ACKclient.service.UpdateCommandStatus(ctx, cACK)
    rebcode = ccmsUpdate.dispatcher.reboot('CCMS Reboot', 10)

def handleJoin(ccmsUpdate, ctx, result, txID):
    domain = 'd1.inteleil.com'
    retry = 1

    commandName = result.CommandName
    ccmsUpdate.ACKclient = ccmsUpdate.setStatusUpdateHeaders(ccmsUpdate.ACKclient, txID)

    if result.CommandParameters != None:
        nbrparms = len(result.CommandParameters.KeyValueOfstringstring)
        parmidx = 0
        while parmidx < nbrparms:
            pkey = result.CommandParameters.KeyValueOfstringstring[parmidx].Key
            pval = result.CommandParameters.KeyValueOfstringstring[parmidx].Value
            if pkey == "Domain Name":
                domain = pval
                parmidx = nbrparms + 1
            else:
                parmidx += 1

    ccmsUpdate.logger.info('Domain name requested "%s", attempting to join...' % domain)

    joinExitCode = ccmsUpdate.dispatcher.join(domain)
    ##      ******  in CCMS they are:     *******
    ##  COMMAND_ISSUED,             == 0
    ##  COMMAND_RECEIVED,           == 1
    ##  COMMAND_EXECUTION_STARTED,  == 2
    ##  COMMAND_EXECUTION_COMPLETE, == 3
    ##  COMMAND_FAILED,             == 4
    ##  WAIT_FOR_MANUAL_STEP,       == 5
    ##  COMMAND_TIMED_OUT,          == 6
    ##  COMMAND_DELAYED_RESPONSE,   == 7
    ##  COMMAND_RETRY               == 8

    ## Note: return codes of 0, 2691 (already joined), and AD
    ## acct create are handled by a bitwise setting on an input
    ## parm - for join only - with UNjoin you do not have the
    ## bitwise setting and must check each return
    ##                                        RC - ver.Nov 2011

    if joinExitCode == 0:
        ccmsUpdate.logger.info('Command execution complete, no errors reported')
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr, rOID, rmt)
    elif joinExitCode == 1355:
        # do nothing
        ccmsUpdate.logger.critical('Command execution failed, but marked complete anyway due to 1355 error...')
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr, rOID, rmt)
    elif joinExitCode == 1219:
        # Multiple sessions to a server- disconnect all previous
        # sessions and try again?? will need to add the RETRY
        # logic from Mahdu TAF client agent
        ccmsUpdate.logger.info('Error code 1219, multiple sessions to a server, retry...')
        rstat = 'COMMAND_RETRY'
        rsuc = False
        rresult = 1219
        rerr = 1219
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr, rOID, rmt)

        # Retry logic from win Client Agent version -
        # for Join Domain only
        if retry <= ccmsUpdate.MAX_JOIN_RETRIES:
            retry =+ 1

            # release renew IP first
            ccmsUpdate.dispatcher.tcpDiag()
            time.sleep(15)

            joinExitCode = ccmsUpdate.dispatcher.join(commandName, domain)
            RetryReturn(joinExitCode, rerr, rtime, rOID, rmt)
    else:
        ccmsUpdate.logger.critical('Domain join command failed!')
        rstat = 'COMMAND_FAILED'
        rsuc = False
        rresult = None
        rerr = 'domain join failed'
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)

    # All return codes will now reply back to CCMS via function
    # below using their own web request - not the original
    # getcommand request  RC - NOV 2011
    ACKresult = ccmsUpdate.ACKclient.service.UpdateCommandStatus(ctx, cACK)

    ccmsUpdate.logger.debug('domain join> CCMS return Comand Status Update Result: %s' % ACKresult)

def handleUnJoin(ccmsUpdate, ctx, result, txID):
    ccmsUpdate.logger.info('domain unjoin requested')
    cmdName = result.CommandName
    ccmsUpdate.ACKclient = ccmsUpdate.setStatusUpdateHeaders(ccmsUpdate.ACKclient, txID)
    urtncode = ccmsUpdate.dispatcher.unJoin()

    if urtncode == 0:
        ccmsUpdate.logger.info('Commanmd execution complete')
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, cmdName, rstat, rsuc, rresult, rerr, rOID, rmt)
    elif urtncode == 2692:
        # already unjoined from a domain
        ccmsUpdate.logger.info('Already unjoined from domain, reporting command execution complete')
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, cmdName, rstat, rsuc, rresult, rerr, rOID, rmt)
    else:
        ccmsUpdate.logger.critical('Command execution failed!')
        rstat = 'COMMAND_FAILED'
        rsuc = False
        rresult = None
        rerr = 'domain unjoin failed'
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, cmdName, rstat, rsuc, rresult, rerr, rOID, rmt)

    ACKresult = ccmsUpdate.ACKclient.service.UpdateCommandStatus(ctx, cACK)

# vim:set ai et sts=4 sw=4 tw=80:
