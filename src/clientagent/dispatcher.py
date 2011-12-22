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
        if IS_WINDOWS:
            rbrtncode = self.__Win32Reboot(message, timeout, True, True)
        elif IS_LINUX:
            self.__LinuxReboot(message, timeout)

        return rbrtncode

    # The following methods are all platform-specific, they are set obfuscated
    # because they are not supposed to be called externally

    # WINDOWS SECTION
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
            wrbcode = 0
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
        # FIXME - This needs to call the external dispatcher scripts
        #timeout = (1.0/60) * timeout
        #os.system("shutdown -r %i '%s'" % (timeout, message))
        raise exceptions.NotImplementedError()


# vim:set ai et sts=4 sw=4 tw=80:
