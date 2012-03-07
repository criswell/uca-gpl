'''
win32_asset.py
--------------
Derived asset collection class specific to Windows.
'''

import exceptions
from clientagent.steward.asset import EILAsset

class Win32_Asset(EILAsset):
    '''
    The Windows-specific asset collection sub-class.
    '''

    def initialize(self):
        '''
        This will be called once, when the module is initialized. Put any
        code here that should be called at program start.
        '''
        raise exceptions.NotImplementedError()

    def updateAsset(self):
        '''
        This will be called whenever we need to update the asset information.
        Do your SCS Discovery scraping (and anything else that is needed) and
        populate the self.asset dictionary.

        E.g., let's say I was updating the "AMTState" sub-element in "AMT", I
        would do it thusly:
            self.asset['AMT']['AMTState'] = foo
        '''
        raise exceptions.NotImplementedError()

# vim:set ai et sts=4 sw=4 tw=80:
