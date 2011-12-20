#!/usr/bin/env python

'''
                            Python Cross-platform "Unified Client Agent" 
                            Interfaces with EIL CCMS Command Service

                                        Intel Architecture Systems Integration
                                          
                                  copyright 2012          all rights reserved
'''

import os
import sys
import time
import threading
##from EILFrameworkLibrary import EILClientMetaData
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import iterparse

from datetime import datetime
from datetime import timedelta

## get windows serivce utility stuff
import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket


            
# SUDs
from suds.client import Client
from suds.sax.element import Element
from suds.sax.attribute import Attribute

import logging
logging.basicConfig(
                    filename = "UClient.log",
                    pathname = "C:\EIL\Log",
                    format = "%(levelname)-10s %(asctime)s %(message)s",
                    level = logging.DEBUG
                    )

logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)
logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
logging.getLogger('suds.resolver').setLevel(logging.DEBUG)
logging.getLogger('suds.xsd.query').setLevel(logging.DEBUG)
logging.getLogger('suds.xsd.basic').setLevel(logging.DEBUG)
logging.getLogger('suds.binding.marshaller').setLevel(logging.DEBUG)
##               ## use wireshark   if this logging doesnt show you ##

##       ## switches and settings from Win Client Agent logic
performingClientOperation = False
RetryCommand = False
MaxRetries = 2
RetryCnt = 1
cmdName = "None"
EndFlag = "n"
global EndServ
EndServ = "N"

class UnifiedClientAgent(win32serviceutil.ServiceFramework):
    _svc_name_ = "UnifiedClientAgt"
    _svc_display_name_ = "UnifiedClientAgt" 
    _svc_description_ = "EIL Portal Unified Client Service (Python) - resides on client - interfaces with CCMS"

    ##logging.debug("***********---> We are inside UnifiedClientAgent - we are beginning    RC 12-5-2011  *******")
    servicemanager.LogInfoMsg("***********---> We are inside UnifiedClientAgent - we are beginning    RC 12-5-2011  *******")
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        ##socket.setdefaulttimeout(60)

    def SvcStop(self):
        global EndServ
        ##servicemanager.LogInfoMsg("******** Entering  SvcStop: " + EndServ + "    ****")
        EndServ = "Y"
        ##servicemanager.LogInfoMsg("******** Value of EndServ (should be Y): " + EndServ + "    ****")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)      

    def SvcDoRun(self):
        import servicemanager
        import win32api
        import win32event
        servicemanager.LogInfoMsg("We are inside SvcDoRun - before LOGMSG call")
        ##logging.debug("***********---> We are inside SvcDoRun - prior to LOGMSG call    RC 12-5-2011  *******")
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        ##logging.debug("***********---> We are inside SvcDoRun - after LOGMSG call    RC 12-5-2011  *******")
        self.timeout = 3000       ## this sets a 50 minute timeout  3000 seconds = 50 minutes
                                  ## but acts more like a 3 second timer - RC
                                  ## CHGD FROM 3000 TO 30000 rc 12/6/11 and back again 12-7
        ##while 1:
        while win32event.WaitForSingleObject(self.hWaitStop, self.timeout) == win32event.WAIT_TIMEOUT:
            ##   wait for service stop signal, if 1 timeout, loop again ##
            ##logging.debug("***********---> We are inside SvcDoRun - after LOGMSG call    RC 12-5-2011  *******")
            servicemanager.LogInfoMsg("We are inside SvcDoRun - after LOGMSG call")
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            ##  check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                ## stop signal encountered
                servicemanager.LogInfoMsg("UnifiedClientAgt - Stopped")
                ##global EndServ
                ##EndServ = "Y"
                ##logging.debug("***********---> We are inside SvcDoRun - stopped     RC 12-5-2011  *******")
                break
            else:
                servicemanager.LogInfoMsg("UnifiedClientAgt - running and healthy")
                ##logging.debug("***********---> We are inside SvcDoRun - running     RC 12-5-2011  *******")
                ##logging.info("***********---> We are inside SvcDoRun - running     RC 12-5-2011  *******")
                self.main()
                
       
    def ctrlHandler(ctrlType):
        return True

    def main(self):
                     servicemanager.LogInfoMsg("We are inside in def(main) - Here is where our python code runs inside the Service via a call to runme()  ")             
                     runMe()

if __name__ == '__main__':
             #win32api.SetConsoleCtrlHandler(ctrlHandler, True)
             servicemanager.LogInfoMsg("***********---> We are inside in pgm flow      about to do win32service RC 12-5-2011  *******")
             ##logging.debug("***********---> We are inside in pgm flow      about to do win32service RC 12-5-2011  *******")
             win32serviceutil.HandleCommandLine(UnifiedClientAgent)
             ##logging.debug("***********---> We are inside in pgm flow      after win32service RC 12-5-2011  *******")
             servicemanager.LogInfoMsg("***********---> We are inside in pgm flow      after win32service RC 12-5-2011  *******")

             ##pass

# Platform determination
if os.name == 'nt':
    IS_WINDOWS = True
    IS_LINUX = False
else:
    IS_WINDOWS = False
    IS_LINUX = True

if IS_WINDOWS:
    import win32api
    import win32security
    from ntsecuritycon import *
    from netbios import *
    from socket import gethostname
else:
    import fcntl, socket, struct

import random

class UnifiedClientSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "UnifiedClientSvc"
    _svc_display_name_ = "UnifiedClientSvc" 
    _svc_description_ = "EIL Portal Unified Client Service (Python) - resides on client - interfaces with CCMS"

    ##def __init__(self):
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        ##win32serviceutil.ServiceFramework.__init__(self)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        ##socket.setdefaulttimeout(60)

    def SvcStop(self):
        EndFlag ="y"
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        import servicemanager
        servicemanager.LogMsg(Servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        ##self.timeout = 3000

        while 1:
            ##   wait for service stop signal, if 1 timeout, loop again ##
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            ##  check to see if self.hWaitStop happened
            if rc == win32event.Wait_Object_0:
                ## stop signal encountered
                servicemanager.LogInfoMsg("UnifiedClientSvc - Stopped")
                break
            else:
                servicemanager.LogInfoMsg("UnifiedClientSvc - running and healthy")

def ctrlHandler(ctrlType):
    return True

    ##def main(self):
    ##    pass

    ##if __name__ == '__main__':
    ##    win32serviceutil.HandleCommandLine(UnifiedClientSvc)


#   Interface with Intel CCMS service
CCMS_WSDL = 'http://172.16.3.10/CCMS/EILClientOperationsService.svc?wsdl'

# envns = ('SOAP-ENV', 'http://www.w3.org/2003/05/soap-envelope')
# NOTE: for SUDS    --- Be sure to setin suds/bindings/binding.py
#                   Will be part of client environment deployment by CCMS
#                   Ensures use of Soap 1.2 instead of Soap 1.1

def getIfInfo():
    '''
    Obtains the first MAC address, cross-platform
    '''
def getIfInfo():
    '''
    Obtains the first MAC address, cross-platform
    '''
    if IS_LINUX:
        ifnum = 0
        ifname = "eth%s" % ifnum
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hwinfo = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
        return (''.join(['%02x:' % ord(char) for char in hwinfo[18:24]])[:-1], os.uname()[1])
    else:
        ncb = NCB()
        ncb.Command = NCBENUM
        la_enum = LANA_ENUM()
        ncb.Buffer = la_enum
        rc = Netbios(ncb)
        if rc != 0: 
            print "Unexpected result %d" % (rc,)
            ##raise RuntimeError, "Unexpected result %d" % (rc,)
        # Grab the first one
        ncb.Reset()
        ncb.Command = NCBRESET
        ncb.Lana_num = ord(la_enum.lana[0])
        rc = Netbios(ncb)
        if rc != 0: 
            print "Unexpected result %d" % (rc,)
            ##raise RuntimeError, "Unexpected result %d" % (rc,)
        ncb.Reset()
        ncb.Command = NCBASTAT
        ncb.Lana_num = ord(la_enum.lana[0])
        ncb.Callname = "*               "
        adapter = ADAPTER_STATUS()
        ncb.Buffer = adapter
        Netbios(ncb)
        return (''.join(['%02x:' % ord(char) for char in adapter.adapter_address])[:-1], gethostname())

def AdjustPrivilege(priv, enable=True):
    '''
    Adjusts the privileges on Windows systems
    '''
    # Get the process token
    flags = TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY
    htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    # Get the ID for the system shutdown privilege.
    idd = win32security.LookupPrivilegeValue(None, priv)
    # Now obtain the privilege for this process.
    # Create a list of the privileges to be added.
    if enable:
        newPrivileges = [(idd, SE_PRIVILEGE_ENABLED)]
    else:
        newPrivileges = [(idd, 0)]
    # and make the adjustment
    win32security.AdjustTokenPrivileges(htoken, 0, newPrivileges)


   


def Win32Reboot(message='Rebooting', timeout=5, bForce=True, bReboot=True):
    '''
    Reboots a Windows system
    '''
    AdjustPrivilege(SE_SHUTDOWN_NAME)
    try:
        wrbcode = 0
        win32api.InitiateSystemShutdown(None, message, timeout, bForce, bReboot)
    finally:
        # Now we remove the privilege we just added.
        AdjustPrivilege(SE_SHUTDOWN_NAME, 0)

    return wrbcode

def LinuxReboot(message='Rebooting', timeout=5):
    '''
    Reboots a Linux system
    '''
    timeout = (1.0/60) * timeout
    os.system("shutdown -r %i '%s'" % (timeout, message))

def Reboot(message='Rebooting', timeout=5):
    '''
    Generic reboot wrapper
    '''
    if IS_WINDOWS:
        rbrtncode = Win32Reboot(message, timeout, True, True)
    elif IS_LINUX:
        LinuxReboot(message, timeout)

    return rbrtncode

def Join(message, jDomain):
    '''
    Generic Join Domain  wrapper
    '''
    if IS_WINDOWS:
       rtncode =  Win32Join(message, jDomain)
    elif IS_LINUX:
        linuxJoin(message, jDomain)    ###NOTE: no Linux join code yet 
    return rtncode


def Win32Join(message, cmdDomain):
    '''
    Joins a Windows system  to the sepcified Windows Domain
    '''
    jresult = 0
    jcmd = "wmic.exe /interactive:off ComputerSystem Where \"name = \'%computername%\'\" call JoinDomainOrWorkgroup FJoinOptions=35 Name=\"" + cmdDomain + "\" Password=\"P@ssw0rd\" UserName=\"administrator@inteleil.com\" "

    AdjustPrivilege(SE_SHUTDOWN_NAME)
    try:
        
        jresult = os.system(jcmd)

    finally:
        # Now we remove the privilege we just added.
        AdjustPrivilege(SE_SHUTDOWN_NAME, 0)

    return jresult
 
       

def LinuxJoin(message='Rebooting', timeout=5):
    '''
    Joins a Linux system
    '''
    timeout = (1.0/60) * timeout
    # os.system("shutdown -r %i '%s'" % (timeout, message))  #### No Linux Code for now

def UnJoin(message, timeout):
    '''
    Generic Join Domain  wrapper
    '''
    if IS_WINDOWS:
        ujreturn = Win32UnJoin(message)
    elif IS_LINUX:
        linuxUnJoin(message, timeout)                          ##NOTE: no Linux join code yet 
    return ujreturn

def Win32UnJoin(message):
    '''
    Unjoins a Windows system from the Windows Domain
    '''
    ujresult = 0
    ujcmd = "wmic.exe /interactive:off ComputerSystem Where \"name = \'%computername%\'\" call UnJoinDomainOrWorkgroup FUnJoinOptions=0 Password=\"P@ssw0rd\" UserName=\"administrator@inteleil.com\" "
    AdjustPrivilege(SE_SHUTDOWN_NAME)
    try:
        ujresult = os.system(ujcmd)
    finally:
        # Now we remove the privilege we just added.
        AdjustPrivilege(SE_SHUTDOWN_NAME, 0)
    return ujresult

def LinuxUnJoin(message='Rebooting', timeout=5):
    '''
    UnJoins a Linux system
    '''
    timeout = (1.0/60) * timeout
    ##os.system("shutdown -r %i '%s'" % (timeout, message))        ####  Linux Code for now

def tcpDiag():
    '''
    Performs basic, platform specific tcp diagnostics and pumping for when we
    switch to PXE or GHOST vlans
    '''
    if IS_WINDOWS:
        ##print os.system('ipconfig /release')
        ##print os.system('ipconfig /renew')
        os.system('ipconfig /release')
        os.system('ipconfig /renew')
    else:
        print os.system('/opt/intel/eil/clientagent/scripts/tcp_diag-full')

   # NASTY XML/SOAP STUFF (if we wind up using this, all of this must be revised.
def newMessageID():
    '''
    Obtains a new message ID from random sources
    '''
    source_string = '0123456789ABCDEFGHIJKLMNOPQRSTWXYZ'
    message_id = 'urn:uuid:'
    # Divide into seven stanzas
    for s in range(7):
        # and have five chars per stanza
        for c in range(5):
            message_id += source_string[random.randint(0,len(source_string)-1)]
        if s < 6:
            # Append a dash if not at end
            message_id += "-"
    return message_id

def setHeaders(client):
    '''
    Sets the headers for the next exchange. Should be called every time we start
    a new exchange
    '''
    wsa_ns = ('wsa', 'http://www.w3.org/2005/08/addressing')
    mustAttribute = Attribute('SOAP-ENV:mustUnderstand', 'true')
    messageID_header = Element('MessageID', ns=wsa_ns).setText(newMessageID())
    replyTo_address = Element('Address',
        ns=wsa_ns).setText('http://www.w3.org/2005/08/addressing/anonymous')
    replyTo_header = Element('ReplyTo', ns=wsa_ns).insert(replyTo_address)
    replyTo_header.append(mustAttribute)
    to_header = Element('To',
        ns=wsa_ns).setText('http://172.16.3.10/CCMS/EILClientOperationsService.svc')
    to_header.append(mustAttribute)
    action_header = Element('Action',
        ns=wsa_ns).setText('http://tempuri.org/IEILClientOperations/GetCommandToExecute')
    action_header.append(mustAttribute)
    master_header_list = [
        messageID_header,
        replyTo_header,
        to_header,
        action_header
    ]
    client.set_options(soapheaders=master_header_list)
    return client
def setAssetHeaders(client):
    '''
    Sets the headers for the next exchange. Should be called every time we start
    a new exchange
    '''
    wsa_ns = ('wsa', 'http://www.w3.org/2005/08/addressing')
    mustAttribute = Attribute('SOAP-ENV:mustUnderstand', 'true')
    messageID_header = Element('MessageID', ns=wsa_ns).setText(newMessageID())
    replyTo_address = Element('Address',
        ns=wsa_ns).setText('http://www.w3.org/2005/08/addressing/anonymous')
    replyTo_header = Element('ReplyTo', ns=wsa_ns).insert(replyTo_address)
    replyTo_header.append(mustAttribute)
    ##to_header = Element('To',
    ##    ns=wsa_ns).setText('http://172.16.3.10/CCMS/EILClientOperationsService.svc')
    ##to_header.append(mustAttribute)
    to_header = Element('To',
        ns=wsa_ns).setText('http://172.16.3.10/CCMS/EILClientOperationsService.svc')
    to_header.append(mustAttribute)
    action_header = Element('Action',
        ns=wsa_ns).setText('http://tempuri.org/IEILClientOperations/UpdateAssetInformation')
    action_header.append(mustAttribute)
    master_header_list = [
        messageID_header,
        replyTo_header,
        to_header,
        action_header
    ]
    client.set_options(soapheaders=master_header_list)
    return client


def setStatusUpdateHeaders(ACKclient):
    '''
    Sets the headers for the handshake ACK exchange. Should be called every time we finish
    an exchange
    '''
    wsa_ns = ('wsa', 'http://www.w3.org/2005/08/addressing')
    mustAttribute = Attribute('SOAP-ENV:mustUnderstand', 'true')
    messageID_header = Element('MessageID', ns=wsa_ns).setText(newMessageID())
    replyTo_address = Element('Address',
        ns=wsa_ns).setText('http://www.w3.org/2005/08/addressing/anonymous')
    replyTo_header = Element('ReplyTo', ns=wsa_ns).insert(replyTo_address)
    replyTo_header.append(mustAttribute)
    to_header = Element('To',
        ns=wsa_ns).setText('http://172.16.3.10/CCMS/EILClientOperationsService.svc')
    to_header.append(mustAttribute)
    action_header = Element('Action',
        ns=wsa_ns).setText('http://tempuri.org/IEILClientOperations/UpdateCommandStatus')
    action_header.append(mustAttribute)
    master_header_list = [
        messageID_header,
        replyTo_header,
        to_header,
        action_header
    ]
    ACKclient.set_options(soapheaders=master_header_list)
    return ACKclient

def generateContext(client, MY_HOST, MY_HWADDR):
    '''
    Generate our command request, this is rather hackish, and lifted almost
    verbatim from the Linux client agent code. If this becomes the norm, we
    should rewrite this more pythonically.
    '''
    ctx = client.factory.create('ns0:MachineContext')
    mParams = client.factory.create('ns2:ArrayOfKeyValueOfstringstring')
    order_num = client.factory.create('ns2:KeyValueOfstringstring')
    order_num.Key = 'ORDER_NUM'
    order_num.Value = '1'
    hwaddr = client.factory.create('ns2:KeyValueOfstringstring')
    hwaddr.Key = 'MAC_ADDR'
    hwaddr.Value = MY_HWADDR
    host = client.factory.create('ns2:KeyValueOfstringstring')
    host.Key = 'HOST_NAME'
    host.Value = MY_HOST
    mParams.KeyValueOfstringstring.append(order_num)
    mParams.KeyValueOfstringstring.append(hwaddr)
    mParams.KeyValueOfstringstring.append(host)
    ctx.mParams = mParams
    mType = client.factory.create('ns0:MachineType')
    ctx.mType = mType.HOST
    return ctx

def generateCommand(client, cNam, CStat, cSucc, cResult, cErr, cExTime, cOID, cMT):
    
    ##logging.debug('******** Beginning of ack ClientFactoryCreate  - RC ver.Nov 2011  *********')

    ack = client.factory.create('ns0:EILCommand')
    ack.CommandName = cNam
    ack.CommandStatus = CStat
    ack.CommandResult = cResult
    ack.CommandSuccessful = cSucc
    ack.ErrorCode = cErr
    ack.OperationID = cOID
    ack.SetMachineType = cMT

    ##logging.debug(ack)
  
    return ack

def RetryReturn(rtncode, cEC, cETO, cOpID, CMtyp):

    ##                  ## this function is used only for Join Domain retry to check status of Retry
                        
                    if rtncode == 0:
                       
                       rstat = 'COMMAND_EXECUTION_COMPLETE'
                       rsuc = True
                       rresult = 0
                       rerr = cEC
                       rtime = cETO
                       rOID = cOpID
                       rmt = CMtyp
                       cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
                       
                    elif rtncode == 1355:
                            ##  do nothing                     
                       rstat = 'COMMAND_EXECUTION_COMPLETE'
                       rsuc = True
                       rresult = 0
                       rerr = cEC
                       rtime = cETO
                       rOID = cOpID
                       rmt = CMtyp

                       cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)

                    else:
                       rstat = 'COMMAND_FAILED'
                       rsuc = False
                       rresult = None
                       rerr = cEC
                       rtime = cETO
                       rOID = cOpID
                       rmt = CMtyp

                       cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)

                    ACKresult = ACKclient.service.UpdateCommandStatus(ctx, cACK)
                    
                    return ACKresult

def AutoUpdate(forceupt="N"):
    '''
    Verifies Client Agent version is latest - if not: stops, deletes,unloads old version  - then - gets, loads, installs, starts, verifies new version - if restart fails: reboots it
    Verifies Client Agent is running - if not: restarts it - if restart fails: reboots it
    '''
    c1Rtn = 0
    forceupdate = forceupt
    cmd1 = "C:\EIL\EILFramework\Setup\ClientRunning.bat "
    cmd2 = "C:\EIL\EILFramework\Setup\ClientRunning.bat "
    cmd3 = "C:\EIL\EILFramework\Setup\ClientRunning.bat "
    cmd4 = "C:\EIL\EILFramework\Setup\ClientRunning.bat "
    cmd5 = "C:\EIL\EILFramework\Setup\ClientRunning.bat "
    rmvcmd1 = "C:\EIL\EILFramework\Setup\ClientRunning.bat "
    rmvcmd2 = "C:\EIL\EILFramework\Setup\ClientRunning.bat "
    rmvcmd3 = "C:\EIL\EILFramework\Setup\ClientRunning.bat "
    c1Rtn = 0
    c2Rtn = 0
    c3Rtn = 0
    c4Rtn = 0
    c5Rtn = 0
    rmvc1Rtn = 0
    rmvc2Rtn = 0
    rmvc3Rtn = 0
    try:
        c1Rtn = 0                        
        c1Rtn = os.system(cmd1)         
        if forceupdate == "Y":
            pass
        else:
            if c1Rtn == 0:
                ##      the Service is running - no need to restart it
                servicemanager.LogInfoMsg('************---> AutoUpdate - Unified Client Agent running and OK  *********')
            else:
                pass
    finally:
        c1Rtn = 0
    return c1Rtn 

def UpdateClientStatus():
    ##               ##      Update Asset Info                   ##
    ##               ##   This should be done every 60 minutes   via runMe's AUhour difference ##

    (MY_HWADDR, MY_HOST) = getIfInfo()
    CA_VERSION = "4.1.1.10 Ver 16.75"
    
    ##MY_HOST = "DELL960-DESK14"           # test only code to see what Prod CCMS
    ##MY_HWADDR = "00-24-E8-3D-50-07"

    ##MY_HOST = "DELL960-DESK14"           # test only code to see what Prod CCMS
    ##MY_HWADDR = "00-24-E8-3D-50-07"


    ujresult = 0
    ujcmd = "c:\EIL\scripts\ScsDisco.bat "
    try:
        ujresult = 0                        ## this is test only
        ujresult = os.system(ujcmd)         ## this is real and should be uncommented
    finally:
        ujresult = 0

    ##                 ##       get the IP number   ##
        ipresult = 0
    ipcmd = "ipconfig > c:\EIL\Log\IPaddr.txt"
    try:
           ipresult = os.system(ipcmd)
    finally:
           ipresult = 0

    ##IPstr = iterparse("c:\EIL\Log\IPaddr.txt", ['start','end'])
    f = open("c:\EIL\Log\IPaddr.txt")
    gotIP = False
    IPstr = f.readline()
    MyIPnbr = " "
    tip = IPstr[1:70]
    ipit = "IP Address. . . . . . . . . "
    while gotIP == False:
        if ipit in tip :
            gotIP = True
            tip = IPstr[38:50]
            tip = tip.strip(' ') 
            tip = tip.rstrip('\r\n')
            tip = tip.strip(' ') 
            MyIPnbr = tip
        else:
            gotIP = False
            IPstr = f.readline()
            tip = IPstr[1:70]

    ##                  ##       parse thru the SCS Discovery XML     ##
    ##                  ##       get fields to Update Asset Info      ##
    
    ##                   ******   This  what Client Agent used to update for Asset Info
    thisJoinedToDomain = False
    thisAMTVer = ""
    thisClientOSRunning =  " "
    thisUUID =  " "
    thisClientAgentVer =  " "
    thisAMTProvisionState =  ""
    thisBIOSVer =  0.00
    thisProvisionServer =  " "
    thisOSDomainName = " "
    thisISAMTSupported = "false"

      
    sb = "  "
    if thisJoinedToDomain == True:
        thisJoined = "True"
    else:
        thisJoined = "False"
    


     ## Build the XML to pass to the CCMS UpdateAssetInformation method
    sb = "  "
    sb = "<Attributes>"
    iparse = iterparse("C:\EIL\LOG\ScsXML.txt", ['start','end'])
    ##sb = sb + "<Key>" + 'IPAddress' + "</Key>"
    ##sb = sb + "<Value>" + MyIPnbr + "</Value>"
    ##sb = sb + "<Key>" + 'ClientAgentVer' + "</Key>"
    ##sb = sb + "<Value>" + '4.1.1.10 Ver 16.75' + "</Value>"

    sb = sb + "<IPAddress>" + MyIPnbr + "</IPAddress>"
    sb = sb + "<ClientAgentVer>" + '4.1.1.10 Ver 16.75' + "</ClientAgentVer>"  

    for event, elem in iparse:
            
        if event == 'start':    
            if elem.tag == "AMTVer":
                thisAMTVer = elem.text
            if elem.tag == "OSDomainName":
                 thisOSDomainName = elem.text
            if thisOSDomainName.find(".com") == -1:
                   thisJoinedToDomain = False
            else:
                   thisJoinedToDomain = True         
            if elem.tag == "OperatingSystem":
                thisClientOSRunning = elem.text
            if elem.tag == "UUID":
                thisUUID = elem.text
            if elem.tag == "IsAMTSupported":
                if elem.text != None:
                    thisIsAMTSupported = elem.text
            ##if elem.tag == "IsAMTSupported":
            ##    thisAMTProvisionState = " "
            ##    if elem.text != None:
            ##        thisIsAMTSupported = elem.text

            # thisAMTProvisionState = elem.text
            if elem.tag == "BIOSVersion":
                thisBIOSVer = elem.text
            if elem.tag == "IPAddress":
                thisIPAddress = elem.text
            if elem.tag == "SerialNumber":
                thisProvisionServer = elem.text
            

    

        ## Build the XML to pass to the CCMS UpdateAssetInformation method
        ##if event == "end": 
        ## and if elem.tag == "System_Discovery":
        ##    next
            ##if elem == tuple:
            ##    tuples = elem.split('),')
            ##    out = []
            ##    for x in tuples:
            ##     a,b = x.strip('()').split(', ')
             ##    out.append (str (a), str(b)) 
            ##     sb = sb + "<Key>" + out + "</Key>"
        ##else:
            if elem.text == None:
                    nothind = 0
            else:     
                if len(sb) > 2000:   ## Until Stored Proc is fixed limit key/value XML to less 2500 varchar
                    nothind = 0
                else:  
                    sb = sb + "<Key>" + elem.tag + "</Key>"
                    sb = sb + "<Value>" + elem.text + "</Value>"
                      
                    ##sb = sb + "<" + elem.tag +  ">"  
                    ##sb = sb + elem.text                 
                    ##sb = sb + "</" + elem.tag +  ">"    
                         
      
    sb = sb + "<JoinedToDomain>" + thisJoined + "</JoinedToDomain>"
    sb = sb + "<HostName>" + MY_HOST + "</HostName>"
    sb = sb + "<AMTVer>" + thisAMTVer + "</AMTVer>"
    sb = sb + "<BIOSVer>" + thisBIOSVer + "</BIOSVer>"
    sb = sb + "<DomainName>" + thisOSDomainName + "</DomainName>"
    sb = sb + "<OSVer>" + thisClientOSRunning + "</OSVer>"
    sb = sb + "<ProvisionServer>" + thisProvisionServer + "</ProvisionServer>"
    sb = sb + "<AMTProvisionState>" + thisAMTProvisionState + "</AMTProvisionState>"
    sb = sb + "<UUID>" + thisUUID + "</UUID>"
    sb = sb + "<IPAddress>" + MyIPnbr + "</IPAddress>"
    ##sb = sb + "<ClientAgentVer>" + CA_VERSION + "</ClientAgentVer>"
    sb = sb + "<ClientAgentVer>" + '4.1.1.10 Ver 16.75' + "</ClientAgentVer>"
  
    sb = sb + "</Attributes>"
          
    headers = {'Content-Type': 'application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/UpdateAssetInformation"'}
    client = Client(CCMS_WSDL, headers=headers)
     
    ## Our poll loop.
    client = setAssetHeaders(client)
    ctx = generateContext(client, MY_HOST, MY_HWADDR)
           
    try:
            ##print "---> About to run dev Update Asset command from CCMS"
            ##logging.debug('******** Beginning of this CCMS Update Asset command SUDS request  - RC ver.Nov 2011   *********')
            servicemanager.LogInfoMsg("******** Beginning of this CCMS Update Asset command SUDS request  - RC ver.Nov 2011   *********")
            servicemanager.LogInfoMsg("Host: " + MY_HOST + "mac: " + MY_HWADDR + "sb: " + sb)
            result = client.service.UpdateAssetInformation(MY_HOST, MY_HWADDR, sb)
            if result == True:
                        ##   note: There is no Command ACK for UpdateAssetInformantion  - RC ver.Nov 2011
                        ##logging.debug('******** Successful Update Asset Information  - RC ver.Nov 2011  *********')    
                        servicemanager.LogInfoMsg("******** dev Successful Update Asset Information  - RC ver.Nov 2011  *********")
            else:
                        servicemanager.LogInfoMsg("******** Failed Update Asset Information  - RC ver.Nov 2011  *********")    
                        ##Logging.debug('******** Failed Update Asset Information  - RC ver.Nov 2011  *********')   
    except Exception as e:
            ##logging.debug('******** below is the Update Asset generic Error  - RC ver.Nov 2011  *********')
            ##logging.debug(e) 
            servicemanager.LogInfoMsg("******** below is the Update Asset generic Error  - RC ver.Nov 2011  *********")     
            servicemanager.LogInfoMsg(e)
            ## logging.debug(client.last_sent())
           ## logging.debug('******** below is the Update Asset SUDS last received  - RC ver.Nov 2011  *********')
           ## logging.debug(client.last_received())
           ## logging.debug('******** End of this  Update Asset SUDS request  - RC ver.Nov 2011  *********')

def runMe():
    # Content-Type: application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/GetCommandToExecute"\r\n
    
    (MY_HWADDR, MY_HOST) = getIfInfo()

    from datetime import datetime
    from datetime import timedelta 

    ForceVersionReload = "N"
    AutoUpdate(ForceVersionReload)
    prevAUhour = datetime.now()       ##  set our own timer 
    prevAUhour.ctime()
    OneHour = timedelta(hours=1)
    Min3 = timedelta(minutes=3)
 

    ##MY_HOST = "EILDEVVM04"                   ## test only code   set your own mac and desktop
    ##MY_HWADDR = "00-50-56-28-05-27"          

    ##MY_HOST = "DELL960-DESK14"               ## test only code to see what PRod CCMS is retunring for join domain
    ##MY_HWADDR = "00-24-E8-3D-50-07"


    ##MY_HOST = "DELL755S-DESK01"               ## test only code to see what PRod CCMS is retunring for join domain
    ##MY_HWADDR = "00-1A-A0-7C-F6-46"

    ##print ">>> Hostname: %s" % MY_HOST
    ##print ">>> HW_ADDR: %s" % MY_HWADDR

    headers = {'Content-Type': 'application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/GetCommandToExecute"'}
    client = Client(CCMS_WSDL, headers=headers)
    
    ###  prepare for the Acknowlegment ACK back to CCMS with the command result
    ACKheaders = {'Content-Type': 'application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/UpdateCommandStatus"'}
    ACKclient = Client(CCMS_WSDL, headers=ACKheaders)
    ACKclient = setStatusUpdateHeaders(ACKclient)

    ##            Note:  Join seems to work fine without this authorization
    ##                   This is Mahdu code from previous Windows Client Agent
    ##                   Equivilent Python code - not yet established - to enure this impersonation
    ##
    ##                                                  RC ver.Nov 2011
    ##
    ##ACKclient.ClientCredentials.Windows.ClientCredential.UserName = "administrator";
    ##ACKclient.ClientCredentials.Windows.ClientCredential.Password = "1mnDollars";       ## "prodPass@eil3";
    ##cmd.ClientCredentials.Windows.ClientCredential.Password = "1mnDollars"; 
    
    ##while True:
    while EndServ == "N":
        # Our poll loop.
        client = setHeaders(client)
        ctx = generateContext(client, MY_HOST, MY_HWADDR)
        RetryCnt = 1
        AUhour = datetime.now()
        AUhour.ctime()
            
        try:
            ##print "---> Looking for command from CCMS"
            
            servicemanager.LogInfoMsg("******** Beginning of this CCMS get command SUDS request")
            ##logging.debug('******** Beginning of this CCMS get command SUDS request  - RC 11/7/11  *********')
            result = client.service.GetCommandToExecute(ctx)
            
            if result == None:
               ##print "!!!!No CCMS Command found to execute" 
               servicemanager.LogInfoMsg("******** !!!!  No CCMS Command found to execute")
               ##logging.debug("!!!!No CCMS Command found to execute")
               performingClientOperation = False
            else:
                
                if result != None:
                     ##print "!!!!   CCMS Command found to execute: " + result.CommandName
                     ##logging.debug('!!!!   CCMS Command found to execute: '  + result.CommandName)
                     servicemanager.LogInfoMsg('******** !!!!   CCMS Command found to execute: '  + result.CommandName)
             
                if result.CommandName == "reboot":
                   ## print "!!!!!!!!!!! REBOOT"
                    ##logging.debug('!!!! ReBoot')
                    servicemanager.LogInfoMsg("******** !!!!  CCMS ReBoot Command found to execute")
                    rebcode = Reboot("CCMS Rebooot", 10)

                    if rebcode == 0:                     
                        rstat = 'COMMAND_EXECUTION_COMPLETE'
                        rsuc = True
                        rresult = 0
                        rerr = result.ErrorCode
                        rtime = result.ExpectedTimeOut
                        rOID = result.OperationID
                        rmt= result.SetMachineType
                        cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
                       
                    else:
                       rstat = 'COMMAND_FAILED'
                       rsuc = False
                       rresult = None
                       rerr = 'reboot failed'
                       rtime = result.ExpectedTimeOut
                       rOID = result.OperationID
                       rmt= result.SetMachineType
                       cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)

                    ACKresult = ACKclient.service.UpdateCommandStatus(ctx, cACK)

                if result.CommandName == "join domain":
                    ##print "!!!!!!!!!!! JOIN DOMAIN"
                    ##logging.debug('!!!! JOIN DOMAIN')
                    servicemanager.LogInfoMsg('!!!! JOIN DOMAIN')
                    ##logging.debug('******** CommandParameters are present/returned  - RC ver.Nov 2011  *********')
                    ##logging.debug(result.CommandParameters)

                    ## release renew IP first       per Mahdu login in old Win client agent
                    ##tcpDiag()
                    ##time.sleep(15)        ##        per Mahdu loigc - slepp 15 seconds for release renew to work

                    cmdDomain = "d1.inteleil.com"      ## set default domain just like Win Agent (per Mahdu)
                    cmdName = result.CommandName
                    if result.CommandParameters != None:
                        nbrparms = len(result.CommandParameters.KeyValueOfstringstring) 
                        parmidx = 0
                        while parmidx < nbrparms:
                            pkey = result.CommandParameters.KeyValueOfstringstring[parmidx].Key
                            pval = result.CommandParameters.KeyValueOfstringstring[parmidx].Value
                            if pkey == "Domain Name":
                                cmdDomain = pval
                                parmidx = nbrparms + 1
                            else:
                                parmidx += 1
                        cmdName = result.CommandName
                   
                    rtncode = Join(cmdName, cmdDomain)
                            
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
       
                        ## Note: return codes of 0, 2691 (already joined), and AD acct create 
                        ## are handled by a bitwise setting on an input parm - for join only - 
                        ## with UNjoin you do not have the bitwise setting and must check each return
                        ##                                             RC - ver.Nov 2011            
                    
                    if rtncode == 0:
                       
                       rstat = 'COMMAND_EXECUTION_COMPLETE'
                       rsuc = True
                       rresult = 0
                       rerr = result.ErrorCode
                       rtime = result.ExpectedTimeOut
                       rOID = result.OperationID
                       rmt= result.SetMachineType
                       cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
                       
                    elif rtncode == 1355:
                            ##  do nothing                     
                       rstat = 'COMMAND_EXECUTION_COMPLETE'
                       rsuc = True
                       rresult = 0
                       rerr = result.ErrorCode
                       rtime = result.ExpectedTimeOut
                       rOID = result.OperationID
                       rmt= result.SetMachineType
                       cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)

                    elif rtncode == 1219:
                            ##Multiple sessions to a server- disconnect all previous sessions and try again??
                            ##  will need to add the RETRY logic from Mahdu TAF client agent
                       rstat = 'COMMAND_RETRY'
                       rsuc = False
                       rresult = 1219
                       rerr = 1219
                       rtime = result.ExpectedTimeOut
                       rOID = result.OperationID
                       rmt= result.SetMachineType
                       cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
                       
                       ## Retry logic from win Client Agent version - for Join Domain only
                       if RetryCnt <= MaxRetries:
                           RetryCommand = True
                           RetryCnt =+ 1
                                               
                           tcpDiag()          ## release renew IP first
                           time.sleep(15)        
                   
                           rtncode = Join(cmdName, cmdDomain)

                           RetryReturn(rtncode, rerr, rtime, rOID, rmt)

                           RetryCommand = False

                    else:
                       rstat = 'COMMAND_FAILED'
                       rsuc = False
                       rresult = None
                       rerr = 'domain join failed'
                       rtime = result.ExpectedTimeOut
                       rOID = result.OperationID
                       rmt= result.SetMachineType
                       cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)

                    ##  All return codes will now reply back to CCMS via function below
                    ##   using their own web request - not the original getcommand request  RC - NOV 2011
                    ACKresult = ACKclient.service.UpdateCommandStatus(ctx, cACK)
                    
                    servicemanager.LogInfoMsg('---> CCMS return Comand Status Update Result: ' + ACKresult)
                    ##logging.debug("---> CCMS return Comand Status Update Result: ")
                    ##print "---> CCMS return Comand Status Update Result:"
                    ##print ACKresult
                    ##logging.debug(ACKresult)
                    ##logging.debug('******** below is the Status SUDS last sent  - RC ver.Nov 2011  *********')
                    ##logging.debug(ACKclient.last_sent())
                    ##logging.debug('******** below is the Status SUDS last received  - RC ver.Nov 2011  *********')
                    ##logging.debug(ACKclient.last_received())
                    ##logging.debug('******** End of this  Status SUDS request  - RC ver.Nov 2011  *********')

                if result.CommandName == "unjoin domain":
                    ##print "!!!!!!!!!!! UNJOIN DOMAIN"
                    ##logging.debug("!!!!!!!!!!! UNJOIN DOMAIN")
                    servicemanager.LogInfoMsg("!!!!!!!!!!! UNJOIN DOMAIN")
                    cmdName = result.CommandName
                    utrncode = UnJoin(cmdName, 10)
                    
                    if urtncode == 0:                     
                        rstat = 'COMMAND_EXECUTION_COMPLETE'
                        rsuc = True
                        rresult = 0
                        rerr = result.ErrorCode
                        rtime = result.ExpectedTimeOut
                        rOID = result.OperationID
                        rmt= result.SetMachineType
                        cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
                       
                    if urtncode == 2692:               ## already unjoined from a domain         
                        rstat = 'COMMAND_EXECUTION_COMPLETE'
                        rsuc = True
                        rresult = 0
                        rerr = result.ErrorCode
                        rtime = result.ExpectedTimeOut
                        rOID = result.OperationID
                        rmt= result.SetMachineType
                        cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
                       
                    else:
                       rstat = 'COMMAND_FAILED'
                       rsuc = False
                       rresult = None
                       rerr = 'domain unjoin failed'
                       rtime = result.ExpectedTimeOut
                       rOID = result.OperationID
                       rmt= result.SetMachineType
                       cACK = generateCommand(ACKclient, cmdName, rstat, rsuc, rresult, rerr, rtime, rOID, rmt)
                 
                    ACKresult = ACKclient.service.UpdateCommandStatus(ctx, cACK)
                    
        except Exception as e:
            ##logging.debug('******** below is the Python generic Error  - RC ver.Nov 2011  *********')
            ##logging.debug(e)
            servicemanager.LogInfoMsg('***Ver A** below is the Python generic Error  - RC ver.Nov 2011  *********')
            servicemanager.LogInfoMsg(e.message) 
            ### strArg = " "
            ### for arg in e.args:
            ###     strArg  = strArg + arg.tostring      
            ### servicemanager.LogInfoMsg(strArg)
            #print "---> Manual help required, restart the network on PXE move"
            #sys.exit('Would you kindly restart the network?')

            ##logging.debug('******** below is the Status SUDS` last sent  - RC ver.Nov 2011  ********')
            ##logging.debug(ACKclient.last_sent())
            ##logging.debug('******** below is the Status SUDS last received  - RC ver.Nov 2011  *********')
            ##logging.debug(ACKclient.last_received())
            ##logging.debug('******** End of this  Status SUDS request  - RC ver.Nov 2011  *********')

            ##logging.debug("**** VLAN switch, running TCP diagnostics to pump interface ***")
            servicemanager.LogInfoMsg('**** VLAN switch, running TCP diagnostics to pump interface ***')
            ##logging.debug("---> We do TCP diagnostics every 30 seconds if we have no other CCMS command to do")
            ##print "---> VLAN switch, running TCP diagnostics to pump interface"
            ##print "---> We do TCP diagnostics every 30 seconds if we have no other CCMS command to do"
            tcpDiag()

        ##if (AUhour - prevAUhour) > Min3:
        if (AUhour - prevAUhour) > OneHour:
            UpdateClientStatus()
            prevAUhour = AUhour

        ##logging.debug("Sleeping for 30 seconds")
        servicemanager.LogInfoMsg('Sleeping for 30 seconds')
        performingClientOperation = False
        time.sleep(30)

if __name__ == "__main__":
    ##logging.debug("***********---> We are inside in pgm flow      about to do win32service RC 12-5-2011  *******")
    servicemanager.LogInfoMsg('**********---> We are inside in pgm flow      about to do win32service RC 12-5-2011  *******')
    
    win32serviceutil.HandleCommandLine(UnifiedClientAgent)

    servicemanager.LogInfoMsg('************---> We are inside in pgm flow      after win32service RC 12-5-2011  *******')  
    ##logging.debug("***********---> We are inside in pgm flow      after win32service RC 12-5-2011  *******")

