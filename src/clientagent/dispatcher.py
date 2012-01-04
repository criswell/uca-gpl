'''
dispatcher.py
-------------
Abstract interface to the system-level functions.
'''

import logging
from clientagent.common.platform_id import PlatformID

platformId = PlatformID()
if platformId.IS_WINDOWS:
    import win32api
    import win32security
    from ntsecuritycon import *
    from netbios import *
else:
    import fcntl, socket, struct
    from clientagent.dispatcher_helper import linux_ExecuteCommand

class Dispatcher:
    '''
    This class provides an abstract interface into the dispatcher itself. It is
    intended to centralize all dispatcher-related calls and interfacing into a
    single location such that any changes only affect the one location.

    Under Linux, this will wrap the dispatcher scripts and perform the same
    function as the DispatcherHelper class in the original Linux Client Agent.

    Under Windows, this will simply handle the platform-specific calls and
    scripts that are relevant.
    '''

    def __init__(self):
        self.platformID = platformId
        self.logger = logging.getLogger('dispatcher')

    # The following methods are the platform-agnostic abstractions
    def reboot(self, message='Rebooting', timeout=5):
        '''
        Generic reboot wrapper
        '''
        rbrtncode = 0
        if self.platformID.IS_WINDOWS:
            rbrtncode = self.__Win32Reboot(message, timeout, True, True)
        elif self.platformID.IS_LINUX:
            self.__LinuxReboot(message, timeout)

        return rbrtncode

    def tcpDiag(self):
        '''
        Performs basic, platform specific tcp diagnostics and pumping for when we
        switch to PXE or GHOST vlans
        '''
        if self.platformID.IS_WINDOWS:
            self.__Win32tcpDiag()
        else:
            self.__LinuxTcpDiag()

    # The following methods are all platform-specific, they are set obfuscated
    # because they are not supposed to be called externally

    # WINDOWS SECTION
    def __Win32tcpDiag(self):
        os.system('ipconfig /release')
        os.system('ipconfig /renew')

    def __AdjustPrivilege(self, priv, enable=True):
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

    def __Win32Reboot(self, message='Rebooting', timeout=5, bForce=True, bReboot=True):
        '''
        Reboots a Windows system
        '''
        self.__AdjustPrivilege(SE_SHUTDOWN_NAME)
        try:
            wrbcode = True
            win32api.InitiateSystemShutdown(None, message, timeout, bForce, bReboot)
        finally:
            # Now we remove the privilege we just added.
            self.__AdjustPrivilege(SE_SHUTDOWN_NAME, 0)

        return wrbcode

    # LINUX SECTION
    def __LinuxReboot(self, message='Rebooting', timeout=5):
        '''
        Reboots a Linux system
        '''
        return linux_ExecuteCommand('reboot')

    def __LinuxTcpDiag(self):
        throwAwayResult = linux_ExecuteCommand('tcp_diag')

# vim:set ai et sts=4 sw=4 tw=80:
