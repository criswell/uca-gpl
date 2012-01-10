'''
commandhandler.py
-----------------
Contains the command hanlding routines which previously were cluttering up
the CCMS Update loop.
'''

def handleReboot(ccmsUpdate, ctx, result):
    '''
    Handles the reboot requests and acknowledgements.

    @param ccmsUpdate The CCMS Update atom caller.
    @param dispatcher The dispatcher instanct.
    @param result The result from the CCMS update call
    '''
    commandName = result.CommandName
    rebcode = ccmsUpdate.dispatcher.reboot('CCMS Reboot', 10)
    ccmsUpdate.ACKclient = ccmsUpdate.setStatusUpdateHeaders(ccmsUpdate.ACKclient, txID)
    if rebcode:
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
    else:
        rstat = 'COMMAND_FAILED'
        rsuc = False
        rresult = None
        rerr = 'reboot failed'
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)

    ACKresult = ccmsUpdate.ACKclient.service.UpdateCommandStatus(ctx, cACK)

def handleJoin(ccmsUpdate, ctx, result):
    domain = 'dl.inteleil.com'
    retry = 1

    commandName = result.CommandName

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

    joinExitCode = ccmsUpdate.dispatcher.join(commandName, domain)
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
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
    elif joinExitCode == 1355:
        # do nothing
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
    elif joinExitCode == 1219:
        # Multiple sessions to a server- disconnect all previous
        # sessions and try again?? will need to add the RETRY
        # logic from Mahdu TAF client agent
        rstat = 'COMMAND_RETRY'
        rsuc = False
        rresult = 1219
        rerr = 1219
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, commandName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)

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

    ccmsUpdate.logger.debug('domain join> CCMS return Comand Status Update Result: ' + ACKresult)

def handleUnJoin(ccmsUpdate, ctx, result):
    ccmsUpdate.logger.info('domain unjoin requested')
    cmdName = result.CommandName
    utrncode = ccmsUpdate.dispatcher.unJoin()

    if urtncode == 0:
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
    elif urtncode == 2692:
        # already unjoined from a domain
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
    else:
        rstat = 'COMMAND_FAILED'
        rsuc = False
        rresult = None
        rerr = 'domain unjoin failed'
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateCommand(ccmsUpdate.ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)

    ACKresult = ccmsUpdate.ACKclient.service.UpdateCommandStatus(ctx, cACK)

# vim:set ai et sts=4 sw=4 tw=80:
