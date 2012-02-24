'''
assetupdate.py
--------------
Main atomic operator class for the Asset Update (cross-platform interface).
'''

from clientagent.steward.atom import Atom
from clientagent import get_config

class AssetUpdate(Atom):
    '''
    This is the main atom class for the asset update functionalities. This will
    manage the core asset collection routines under Windows and Linux, and it
    will interact with either the CCMS_Update atom or directly with CCMS itself
    (this is TBD) to communicate a local system's physical and software assets.
    '''

    def __init__(self):
        self.config = get_config()
        self._timer = 0
        self.TARGET_TIMEDELTA = 60 * 60 # 60 seconds X 60 minutes
        self.ACTIVE = True
        # TODO

    def shutdown(self):
        '''
        Called when the UCA is shutting down.
        '''
        # TODO - Any cleanup?
        pass

    def update(self, timeDelta):
        '''
        Called each loop with the current timeDelta since the last time the
        update was called.
        '''

        self._timer += timeDelta
        if self._timer >= self.TARGET_TIMEDELTA:
            self._timer = 0
            # Here's where our asset collection and update logic goes
            # but for now, it's just stubbed
            # TODO
            pass

# vim:set ai et sts=4 sw=4 tw=80:
