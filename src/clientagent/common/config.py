try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import clientagent
from clientagent.common.platform_id import PlatformID
from clientagent.common.utility import mkdir_p
import os
import sys
import time

class Config:
    '''
    The unified client agent's configuration system.
    '''

    def __init__(self):
        self._platformID = PlatformID()
        self._root = "%s/home" % clientagent.ClientAgentState.CLIENTAGENT_ROOT
        self._configFile = "%s/clientagent.cfg" % self._root
        self._C = configparser.SafeConfigParser()
        self._load_config()

    def _load_config(self):
        if os.path.isdir(self._root):
            if os.path.isfile(self._configFile):
                # Attempt to load it
                try:
                    self._C.readfp(open(self._configFile))
                except (configparser.MissingSectionHeaderError,
                        configparser.ParsingError):
                    self._backup_config()
                    self._create_config()
            else:
                # Okay, we just create it
                self._create_config()
        else:
            # need to create directory and config
            mkdir_p(self._root)
            self._create_config()

    def _backup_config(self):
        '''
        Back up the existing config
        '''
        # Our config file is fubar, we'll nuke it after backing it up
        # FIXME - Might want to verify this will work as expected under Windows
        # where file extensions matter
        backup_config = "%s.backup-%i" % (self._configFile % int(time.time()))
        os.rename(self._configFile, backup_config)

# vim:set ai et sts=4 sw=4 tw=80:
