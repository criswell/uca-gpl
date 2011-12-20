'''
ccmsupdate.py
-------------
Main atomic operator class for the CCMS updates.
'''

from clientagent.steward.atom import Atom
from clientagent.common.utility import mkdir_p
from clientagent.common.utility import getIfInfo

class CCMS_Update(Atom):
    '''
    This is the main CCMS interaction interface. This manages the core
    interactions with CCMS, and interacts with the dispatcher to re-route
    commands to platform-specific implimentations.
    '''
    def __init__(self):
        (self.MY_HWADDR, self.MY_HOST) = getIfInfo()
        

    def update(self, timeDelta):
        pass

# vim:set ai et sts=4 sw=4 tw=80:
