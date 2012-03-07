'''
linux_asset.py
--------------
Derived asset collection class specific to Linux.
'''

import exceptions
from clientagent.steward.asset import EILAsset

class Linux_Asset(EILAsset):
    '''
    The Linux-specific asset collection sub-class.
    '''

    def initialize(self):
        '''
        This will be called once, when the module is initialized. Put any
        code here that should be called at program start.
        '''
        pass

    def updateAsset(self):
        '''
        Called when we update the asset from getAssetXML
        '''
        # Complete dummy data to test serialization
        self.asset['Common']['HostName'] = "scorpious"
        self.asset['Common']['UUID'] = 'EF38A029-300C-11DE-BA59-0015179E15E4'
        self.asset['Common']['DomainName'] = 'sh.linuxd.org'

        self.asset['Common']['OS'] = 'Linux'
        self.asset['Common']['OSVersion'] = 'Kubuntu 11.10'
        self.asset['Common']['VirtualMachine'] = False

        processor = {
            'CpuCount' : 4,
            'CpuModel' : 'Intel',
            'CoresPerCpu' : 3,
            'Vt' : True,
            'VtD' : False,
        }
        self.asset['Common']['Processor'] = processor

# vim:set ai et sts=4 sw=4 tw=80:
