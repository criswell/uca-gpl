'''
win32_asset.py
--------------
Derived asset collection class specific to Windows.
'''

import exceptions
from clientagent.steward.asset import EILAsset
from clientagent.common.ordereddict import OrderedDict as OD
import os, platform

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
            self.__wim = WMI()

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
        self.asset['Common']['HostName'] = os.uname()[1]
        self.asset['Common']['UUID'] = self._getUUID()
        self.asset['Common']['DomainName'] = socket.getfqdn()

        self.asset['Common']['OS'] = platform.system()
        self.asset['Common']['OSVersion'] = ' '.join(platform.linux_distribution())
        self.asset['Common']['OSArchitecture'] = ' '.join(platform.architecture())
        self.asset['Common']['OSKernel'] = platform.release()


# vim:set ai et sts=4 sw=4 tw=80: