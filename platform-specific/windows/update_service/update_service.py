'''
update_service.py
-----------------
This is intended to run *ONLY* on Windows environments.

Compare local VERSION file to the VERSION.txt file on the LAN,
about once per minute. If they are different, run uca-bootstrap.py
to re-install the UCA.

This is how to use this Windows service:

Installing: > python update_service.py install
Starging:   > net start UpdateService
Stopping:   > net stop UpdateService
Deleting:   > sc delete UpdateService
'''

import os
import win32service
import win32serviceutil
import win32event
import subprocess
import urllib
import time

class UpdateService(win32serviceutil.ServiceFramework):
    '''
    Windows Service class to re-install UCA when VERSION file has changed.
    '''
    _svc_name_           = 'UpdateService'
    _svc_display_name_   = 'Update Service'
    _svc_description_    = 'Re-installs UCA when VERSION changes.'

    def __init__(self, args):
        '''
        Initialize parent. Create 'stop' event. Compare VERSION files
        once per minute. Do preliminary read of local VERSION file.
        '''
        # I copied these IPs from uca-bootstrap.py (changed self.testIP),
        # but they should probably come from a common location.
        self.is_Production     = False
        self.CCMS_ADDR         = 'eilauto01'
        self.prodPath          = 'EILUCA'
        self.testPath          = 'EILUCA-testing'
        self.eilPath           = 'C:\\EIL\\'
        self.versionFileLocal  = self.eilPath + 'lib\\VERSION'
        self.bootstrapperPath  = self.eilPath + 'scripts\\uca-bootstrap.py'
        self.logFile           = 'C:\\UCA_Reinstall.log'
        self.logFile_OLD       = 'C:\\UCA_Reinstall_OLD.log'

        # Determine which path to use
        self.urlPath = self.testPath
        if self.is_Production:
            self.urlPath = self.prodPath
        self.versionFileRemote = 'http://%s/%s/VERSION.txt' % (self.CCMS_ADDR, self.urlPath)

        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.timeout = 60 * 1000  # Compare VERSION files every minute.
        # If 'c:\EIL\' doesn't already exist, then create it.
        if not os.path.isdir(self.eilPath):
            os.mkdir(self.eilPath)
        # If log file exists, rename it to '_OLD' (removing '_OLD' if exist).
        if os.path.exists(self.logFile):
            if os.path.exists(self.logFile_OLD):
                os.remove(self.logFile_OLD)
            os.rename(self.logFile, self.logFile_OLD)
        self.log = open(self.logFile, 'w')
        self.LogFileMsg('UpdateService: __init__()\n')

    def LogFileMsg(self, msg):
        '''
        Write messages to the UpdateService log file. See open() above.
        '''
        msgToWrite = time.strftime('%m/%d/%Y(%H:%M:%S): ') + msg
        self.log.write(msgToWrite)
        self.log.flush()

    def ReadVersionFile(self, remote):
        '''
        Read the VERSION file. If remote==True, read remote VERSION.txt file
        over the LAN. Otherwise, remote==False, so read local VERSION file.
        '''
        try:
            if remote:
                f = urllib.urlopen(self.versionFileRemote)
            else:
                f = open(self.versionFileLocal, 'r')
            # Get first non-blank line & remove all white space.
            versionFileContents = ''
            while versionFileContents == '':
                versionFileContents += ''.join(f.read().split())
            f.close()
        except IOError:
            if remote:
                localRemote = 'remote'
            else:
                localRemote = 'local'
            # VERSION file doesn't exist - log WARNING and ignore for now.
            LogFileMsg('WARNING: There is no ' + localRemote + ' VERSION file')
        return versionFileContents

    def SvcDoRun(self):
        '''
        Compare the previous and current contents of the VERSION.txt file.
        When they are different, run uca-bootstrap.py.
        '''
        self.LogFileMsg('UpdateService: Beginning SvcDoRun()\n')
        # Loop until self.hWaitStop has happened (stop signal is encountered).
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            # Compare local and remote VERSION files.
            localVersion  = self.ReadVersionFile(False)
            remoteVersion = self.ReadVersionFile(True)
            # Debugging message:
            #msg = 'SvcDoRun: localVersion: %s; remoteVersion: %s\n' % (localVersion, remoteVersion)
            #self.LogFileMsg(msg)
            if localVersion != remoteVersion:
                # Files are different - invoke bootstrapper.
                command = 'python.exe %s' % self.bootstrapperPath
                msg = 'UpdateService: VERSION changed from %s to %s - Re-installing UCA: %s\n' % (localVersion, remoteVersion, command)
                self.LogFileMsg(msg)
                self.ExecCommand(command)  # Block until done.
                msg = 'UCA has been re-installed (new version: %s).\n' % self.ReadVersionFile(False)
                self.LogFileMsg(msg)
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
        self.LogFileMsg('UpdateService has Stopped\n')

    def SvcStop(self):
        '''
        Stop the Update service gracefully.
        '''
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def ExecCommand(self, cmd):
        '''
        Given a command, this will execute it in the parent environment.
        '''
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.readlines()
        p.stdin.close()
        p.stdout.close()
        for line in output:
            self.log.write(line.rstrip() + '\n')
        self.log.flush()

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(UpdateService)

# vim:set ai et sts=4 sw=4 tw=80:
