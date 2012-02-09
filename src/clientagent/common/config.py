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

    def __init__(self, rootDir):
        self._platformID = PlatformID()
        self._root = "%s/home" % rootDir
        self._configFile = "%s/clientagent.cfg" % self._root
        self.C = configparser.SafeConfigParser()
        self._load_config()
        self._callbacks = []
        self._lastModTime = self._getConfigMod()

    def _load_config(self):
        if os.path.isdir(self._root):
            if os.path.isfile(self._configFile):
                # Attempt to load it
                try:
                    self.C.readfp(open(self._configFile))
                    if(self.C.has_option('main', 'log_level')):
                        pass
                    else:
                        self._backup_config()
                        self._create_config()
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

    def _create_config(self):
        '''
        Creates a default config file
        '''
        if not self.C.has_section('main'):
            self.C.add_section('main')

        if not self.C.has_section('linux'):
            self.C.add_section('linux')

        if not self.C.has_section('windows'):
            self.C.add_section('windows')

        # Our default is to enabled ERROR and above
        self.C.set('main', 'log_level', '3')

        # Set some reasonable defaults for the servers we have to work with
        self.C.set('main', 'RMS', 'rmssvr01')
        self.C.set('main', 'CCMS', '172.16.3.10')
        self.C.set('main', 'NMSA', 'nmsa01')

        # Default Linux settings
        self.C.set('linux', 'daemon_stdin', '/dev/null')
        self.C.set('linux', 'daemon_stdout', '/dev/null')
        self.C.set('linux', 'daemon_stderr', '/dev/null')
        self.C.set('linux', 'pidfile', "%s/clientagent.pid" % self._root)

        # Default Windows settings
        # TODO

        try:
            # It really is horrible we don't have the 'with' statement on
            # CentOS
            configfile = open(self._configFile, 'wb')
            self.C.write(configfile)
            configfile.close()
        except:
            raise

    def _getConfigMod(self):
        '''
        Obtains the mtime for the config file. Returns None on os.error
        '''
        mtime = None
        try:
            mtime = os.path.getmtime(self._configFile)
        except:
            mtime = None

        return mtime

    def recheck(self):
        '''
        Re-checks the config file for changes. If no changes, does nothing. If
        changes have been found, will reload the config file and execute the
        callbacks for other modules watching for config modifications.
        '''
        mtime = self._getConfigMod()
        if mtime != self._lastModTime:
            self._lastModTime = mtime
            self._load_config()
            for callback in self._callbacks:
                callback()

    def setCallback(self, callback):
        '''
        Sets a callback method for when the config file changes.

        @param callback The callback method. Should not accept any arguments.
        '''
        self._callbacks.append(callback)

# vim:set ai et sts=4 sw=4 tw=80:
