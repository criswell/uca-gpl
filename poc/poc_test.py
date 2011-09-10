#!/usr/bin/env python

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

# SUDs
from suds.client import Client

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

if __name__ == "__main__":
    client = Client(CCMS_WSDL)

# vim:set ai et sts=4 sw=4 tw=80:
