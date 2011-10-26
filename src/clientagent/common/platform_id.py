'''
platform_id.py
--------------

Identifies the platform we are on. Provides a unified, and precise way to
determine the platform as well as any platform variants that matter.
'''

import os
import sys

class PlatformID:
    '''
    The platform ID class.
    '''

    # We use the borg state class organization for all of our static items
    __borg_state = {}

    # General platform determination
    __IS_WINDOWS = False
    __IS_LINUX = True
    if os.name === 'nt':
        __IS_LINUX = False
        __IS_WINDOWS = True

    class __PlatformVariant:
        '''
        The platform variant class helps zero in on what, specific, platform
        variation we're running on.
        '''
        def __init__(self, parentPlatformID):
            self.parentID = parentPlatformID

            if self.parentID.IS_WINDOWS:
                # FIXME - Any code variation for Windows? We should specify here
                pass
            else:
                # Linux variation can be a nightmare, for now we just call on
                # the external and existing client agent helper script

    def __init__(self):
        self.__dict__ = self.__borg_state

        self.IS_WINDOWS = self.__IS_WINDOWS
        self.IS_LINUX = self.__IS_LINUX

# vim:set ai et sts=4 sw=4 tw=80: