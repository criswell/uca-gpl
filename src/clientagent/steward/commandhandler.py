'''
commandhandler.py
-----------------
Contains the command hanlding routines which previously were cluttering up
the CCMS Update loop.
'''

def handleReboot(ccmsUpdate, dispatcher, result):
    '''
    Handles the reboot requests and acknowledgements.

    @param ccmsUpdate The CCMS Update atom caller.
    @param dispatcher The dispatcher instanct.
    @param result The result from the CCMS update call
    '''
    rebcode = dispatcher.reboot('CCMS Reboot', 10)
    ccmsUpdate.ACKclient = ccmsUpdate.setStatusUpdateHeaders(ccmsUpdate.ACKclient, txID)
    if rebcode:
        rstat = 'COMMAND_EXECUTION_COMPLETE'
        rsuc = True
        rresult = 0
        rerr = result.ErrorCode
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateAckCommand(ccmsUpdate.ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
    else:
        rstat = 'COMMAND_FAILED'
        rsuc = False
        rresult = None
        rerr = 'reboot failed'
        rtime = result.ExpectedTimeOut
        rOID = result.OperationID
        rmt= result.SetMachineType
        cACK = ccmsUpdate.generateAckCommand(ccmsUpdate.ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)

    ACKresult = ccmsUpdate.ACKclient.service.UpdateCommandStatus(ctx, cACK)

# vim:set ai et sts=4 sw=4 tw=80:
