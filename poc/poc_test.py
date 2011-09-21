#!/usr/bin/env python

'''
This is a simple POC of a very basic cross-platform reboot CCMS command
'''

import os

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

import random

# SUDs
from suds.client import Client
from suds.sax.element import Element
from suds.sax.attribute import Attribute

# UGLY HARDCODED POC GARBAGE
CCMS_WSDL = 'http://172.16.3.10/CCMS/EILClientOperationsService.svc?wsdl'
MY_HWADDR = '00:1B:78:C3:08:D6' # HP7700-DESK13

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
    messageID_header = Element('MessageID', ns=wsa_ns).setText(newMessageID)
    master_header_list = [
        messageID_header,
    ]
    client.set_options(soapheaders=master_header_list)
    return client

if __name__ == "__main__":
    headers = {'Content-Type': 'application/soap+xml; charset=utf-8'}
    client = Client(CCMS_WSDL, headers=headers)

# vim:set ai et sts=4 sw=4 tw=80:
