'''
update_service.py
-----------------
This is intended to run only on Windows environments.

Compare local VERSION file to the VERSION.txt file on the LAN,
about once per minute. If they are different, run uca-bootstrap.py
to re-install the UCA.
'''

import win32service
import win32serviceutil
#import win32api
import win32event
#import servicemanager
#import socket
import subprocess
import urllib

class UpdateService(win32serviceutil.ServiceFramework):
    '''
    Windows Service class to re-install UCA when VERSION file has changed.
    '''
    _svc_name_               = 'UpdateService'
    _svc_display_name_       = 'Update Service'
    _svc_description_        = 'Re-installs UCA when VERSION changes.'
    # I copied these IPs from uca-bootstrap.py (changed _TEST_IP_),
    # but they should probably come from a common location.
    _PROD_IP_                = '172.16.3.10' # ???
    _TEST_IP_                = '10.4.8.23'   # UCA-DEV01
    _STAG_IP_                = '10.4.0.66'   # UbuntuDev
    _svc_version_file_url_   = 'http://' + _STAG_IP_ + '/EILUCA/VERSION.txt'
    _svc_version_file_local_ = 'C:\\EIL\\lib\\VERSION'
    _svc_bootstrapper_path_  = 'C:\\EIL\\scripts\\uca-bootstrap.py'

    #servicemanager.LogInfoMsg('*** Inside UpdateService - Beginning')

    def __init__(self, args):
        '''
        Initialize parent. Create 'stop' event. Compare VERSION files
        once per minute. Do preliminary read of local VERSION file.
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.timeout = 60000  # Compare VERSION files every minute.
        self.localVersion = ReadVersionFile(False)
        self.log = open('c:\\UCA-Reinstall.log', 'w')
        self.log.write('UpdateService has started\n')

    def ReadVersionFile(remote):
        '''
        Read the VERSION file. If remote==True, read remote VERSION.txt file
        over the LAN. Otherwise, remote==False, so read local VERSION file.
        '''
        versionFileContents = ''
        try:
            if remote:
                f = urllib.urlopen(_svc_version_file_url_)
            else:
                f = open(_svc_version_file_local_, 'r')
            # Get first non-blank line & remove all white space.
            while versionFileContents == '':
                versionFileContents += ''.join(f.read().split())
            f.close()
        except IOError:
            pass # VERSION file doesn't exist - ignore for now.
        return versionFileContents

    def SvcDoRun(self):
        '''
        Compare the previous and current contents of the VERSION.txt file.
        When they are different, run uca-bootstrap.py.
        '''
        #servicemanager.LogInfoMsg('*** Inside UpdateService - def(SvcDoRun)')
        #servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
        #                      servicemanager.PYS_SERVICE_STARTED,
        #                      (self._svc_name_, ''))
        self.log.write('UpdateService: Beginning SvcDoRun()\n')
        # Loop until self.hWaitStop has happened (stop signal is encountered).
        while win32event.WaitForSingleObject(self.hWaitStop, self.timeout) != \
                win32event.WAIT_OBJECT_0:
            # Compare local and network VERSION files.
            if self.localVersion != self.ReadVersionFile(True):
                self.log.write('UpdateService: VERSION changed - Re-installing UCA\n')
                # Files are different - invoke bootstrapper.
                command = 'python %s' % _svc_bootstrapper_path_
                msg = 'Executing the bootstrapper:   %s' % command
                #servicemanager.LogInfoMsg(msg)
                self.log.write(msg, '\n')
                self.exec_command(command)  # Block until done.
                # We should now have a new, local VERSION file - get it.
                self.localVersion = ReadVersionFile(False)
        #servicemanager.LogInfoMsg('UpdateService has Stopped')
        self.log.write('UpdateService has stopped\n')

    def SvcStop(self):
        '''
        Stop the Update service gracefully.
        '''
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def exec_command(cmd):
        '''
        Given a command, this will execute it in the parent environment.
        '''
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.readlines()
        p.stdin.close()
        p.stdout.close()
        for line in output:
            #servicemanager.LogInfoMsg(line.rstrip())
            self.log.write(line.rstrip(), '\n')

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(UpdateService)

# vim:set ai et sts=4 sw=4 tw=80:
