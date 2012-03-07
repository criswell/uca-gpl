'''
linux_asset.py
--------------
Derived asset collection class specific to Linux.
'''

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
        raise exceptions.NotImplementedError()

    def updateAsset(self):
        '''
        Called when we update the asset from getAssetXML
        '''
        raise exceptions.NotImplementedError()

# vim:set ai et sts=4 sw=4 tw=80:
