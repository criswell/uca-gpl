'''
win32_asset.py
--------------
Derived asset collection class specific to Windows.
'''

import exceptions
from clientagent.steward.asset import EILAsset
from clientagent.common.ordereddict import OrderedDict as OD
import os

WMI_ENABLED = True
try:
    from clientagent.wmi import WMI
except:
    WMI_ENABLED = False

class Win32_Asset(EILAsset):
    '''
    The Windows-specific asset collection sub-class.
    '''

    def initialize(self):
        '''
        This will be called once, when the module is initialized. Put any
        code here that should be called at program start.
        '''

        if WMI_ENABLED:
            self.__wmi = WMI()

    def _hasResult(self, someObject):
        '''
        When called with a WMI result will return the last entry or None if
        no entries found. This should only be used when you're expecting
        exactly one WMI result.
        '''
        if len(someObject) > 0:
            return someObject[-1]
        else:
            return None

    def updateAsset(self):
        '''
        Called when we update the asset from getAssetXML
        '''

        # Put all non WMI items up here, so we can ensure something shows up
        self.asset['Common']['HostName'] = os.uname()[1]

        if WMI_ENABLED:
            NTDomain = self._hasResult(self.__wmi.Win32_NTDomain())
            if NTDomain:
                hostname = NTDomain.Caption
                self.asset['Common']['DomainName'] =  NTDomain.DomainName
                joinedToDomain = False
                if domain:
                    joinedToDomain = True
                self.asset['Common']['JoinedToDomain'] = joinedToDomain

            productID = hasResult(c.Win32_ComputerSystemProduct())
            if productID:
                self.asset['Common']['UUID'] = productID.UUID

            OS = hasResult(c.Win32_OperatingSystem())
            if OS:
                self.asset['Common']['OS'] = OS.Caption
                self.asset['Common']['OSVersion'] = OS.Version
                mjv = OS.ServicePackMajorVersion
                mjm = OS.ServicePackMinorVersion
                self.asset['Common']['OSServicePack'] = "%s.%s" % (mjv, mjm)
                self.asset['Common']['OSArchitecture'] = OS.OSArchitecture

                biosVersion = None
                BIOS = hasResult(c.Win32_BIOS())
                if BIOS:
                    biosVersion = BIOS.Version
                self.asset['Common']['BiosVersion'] = biosVersion


# vim:set ai et sts=4 sw=4 tw=80: