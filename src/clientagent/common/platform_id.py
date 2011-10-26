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

            # We undefine these and then fill as needed. The current assumption
            # is that IF they are None then no variant in external code
            # requirements

            '''
            SYSID defines the unique system ID. For example "DEB" for Debian-
            derived distributions.
            '''
            self.SYSID = None

            '''
            PLATFORM defines the platform variation (if it exists). For example,
            'ubuntu' for Ubuntu, which is derived from Debian.
            '''
            self.PLATFORM = None

            '''
            VERSION defines any additional version information for the platform.
            Currently unsupported, but included in case we need it later on
            '''
            self.VERSION = None

            if self.parentID.IS_WINDOWS:
                # FIXME - Any code variation for Windows? We should specify here
                pass
            else:
                # Linux variation can be a nightmare, for now we just call on
                # the external and existing client agent helper script
                stream = os.popen('/opt/intel/eil/clientagent/tools/clientagent-helper.sh --sysid')
                output = stream.readlines()
                stream.close()

                if len(output) == 1:
                    # in the event that the client agent helper is non-
                    # functional, we want to fail gracefully
                    self.SYSID = output[1]

                stream = os.popen('/opt/intel/eil/clientagent/tools/clientagent-helper.sh --platform')
                output = stream.readlines()
                stream.close()

                if len(output) == 1:
                    # in the event that the client agent helper is non-
                    # functional, we want to fail gracefully
                    self.PLATFORM = output[1]

    __Variant = None

    def __init__(self):
        self.__dict__ = self.__borg_state

        if self.__Variant == None:
            # This should only happen on initial creation
            self.IS_WINDOWS = self.__IS_WINDOWS
            self.IS_LINUX = self.__IS_LINUX
            self.__Variant = __PlatformVariant(self)
            self.VARIANT = self.__Variant

# vim:set ai et sts=4 sw=4 tw=80:
