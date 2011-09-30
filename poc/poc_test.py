#!/usr/bin/env python

'''
This is a simple POC of a very basic cross-platform reboot CCMS command
'''

import os
import sys
import time

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

# SUDs
from suds.client import Client
from suds.sax.element import Element
from suds.sax.attribute import Attribute

# UGLY HARDCODED POC GARBAGE
CCMS_WSDL = 'http://172.16.3.10/CCMS/EILClientOperationsService.svc?wsdl'
MY_HWADDR = '00:1B:78:C3:08:D6' # HP7700-DESK13
MY_HOST = 'HP7700-DESK14'

# Be sure to set
# envns = ('SOAP-ENV', 'http://www.w3.org/2003/05/soap-envelope')
# in suds/bindings/binding.py
# Probably better way to fix this with import doctor, but in 2 weeks I couldn't
# figure it out

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
        if rc != 0: raise RuntimeError, "Unexpected result %d" % (rc,)
        # Grab the first one
        ncb.Reset()
        ncb.Command = NCBRESET
        ncb.Lana_num = ord(la_enum.lana[0])
        rc = Netbios(ncb)
        if rc != 0: raise RuntimeError, "Unexpected result %d" % (rc,)
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
        win32api.InitiateSystemShutdown(None, message, timeout, bForce, bReboot)
    finally:
        # Now we remove the privilege we just added.
        AdjustPrivilege(SE_SHUTDOWN_NAME, 0)

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
        Win32Reboot(message, timeout, True, True)
    elif IS_LINUX:
        LinuxReboot(message, timeout)

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

def generateContext(client):
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

def runMe():
    # Content-Type: application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/GetCommandToExecute"\r\n
    (MY_HWADDR, MY_HOST) = getIfInfo()
    print ">>> Hostname: %s" % MY_HOST
    print ">>> HW_ADDR: %s" % MY_HWADDR
    headers = {'Content-Type': 'application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/GetCommandToExecute"'}
    client = Client(CCMS_WSDL, headers=headers)
    while True:
        # Our poll loop.
        client = setHeaders(client)
        ctx = generateContext(client)
        #client.service.GetCommandToExecute(ctx)
        try:
            print "---> Looking for command from CCMS"
            result = client.service.GetCommandToExecute(ctx)
            print "---> CCMS Result:"
            print result
            if result != None:
                if result.CommandName == "reboot":
                    print "!!!!!!!!!!! REBOOT"
                    Reboot("CCMS Rebooot", 10)
        except:
            print "---> Manual help required, restart the network on PXE move"
            sys.exit('Would you kindly restart the network?')

        time.sleep(30)

if __name__ == "__main__":
    runMe()

# vim:set ai et sts=4 sw=4 tw=80:
