'''
update_service.py
-----------------
This is intended to run only on Windows environments.

Wait for the uca 'C:\EIL\lib\VERSION' file to be created and remember its
contents. Then, once a minute, open the VERSION file again and compare its
current and previous contents. If they are different, run uca-bootstrap.py.
'''

import pythoncom
import win32serviceutil
import win32service
import win32api
import win32event
import servicemanager
import socket
from clientagent import ClientAgentState
import subprocess

class UpdateService(win32serviceutil.ServiceFramework):
    '''
    Generic Windows Service class with the same framework as the Linux
    daemon class.
    '''
    _svc_name_         = ClientAgentState.SRV_NAME
    _svc_display_name_ = ClientAgentState.SRV_DISPLAY_NAME
    _svc_description_  = ClientAgentState.SRV_DESCRIPTION
    _svc_version_file_path_ = 'C:\\EIL\\lib\\VERSION'
    _svc_bootstrapper_path_ = 'C:\\EIL\\lib\\uca-bootstrap.py'

    servicemanager.LogInfoMsg('*** Inside UpdateService - Beginning')

    def __init__(self, args):
        '''
        Wait for VERSION file to be created and remember VERSION file contents.
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.running = False  # Do we need this flag?
        self.timeout = 60  # Check VERSION file every minute.
        self.previousVersion = ''

    def ReadVersionFile():
        f = open(_svc_version_file_path_)
        versionFileContents = ''
        while f:
            versionFileContents += f.read()
        f.close()
        return versionFileContents

    def SvcDoRun(self):
        '''
        Compare the previous and current contents of the VERSION.txt file.
        When they are different, run uca-bootstrap.py.
        '''
        servicemanager.LogInfoMsg('*** Inside UpdateService - def(SvcDoRun)')
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        # Loop until self.hWaitStop has happened (stop signal is encountered).
        while win32event.WaitForSingleObject(self.hWaitStop, self.timeout) != \
                win32event.WAIT_OBJECT_0:
            # Initialize previous contents of VERSION file.
            # Loop until there IS a VERSION file.
            # Should we add a timestamp to quit looping after (say) an hour?
            while self.previousVersion == '':
                try:
                    self.previousVersion = self.ReadVersionFile()
                    break  # Break - previous version initialized.
                except IOError:
                    pass # VERSION file not found - keep looping.
            # Check current contents of VERSION file.
            try:
                tmpVersion = self.ReadVersionFile()
                if tmpVersion != self.previousVersion:
                    # Changed VERSION file encountered - invoke bootstrapper.
                    command = 'python %s' % _svc_bootstrapper_path_
                    msg = 'Executing the bootstrapper:   %s' % command
                    servicemanager.LogInfoMsg(msg)
                    self.exec_command(command)  # Block until done.
                    self.previousVersion = tmpVersion
            except IOError:
                pass # VERSION file doesn't exist - ignore for now.
        servicemanager.LogInfoMsg('UpdateService has Stopped')

    def SvcStop(self):
        '''
        Stop the Update service gracefully.
        '''
        self.running = False  # Not needed?
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
            servicemanager.LogInfoMsg(line.rstrip())

    # *BOGUS* Remaining methods are not used anywhere.

    def ctrlHandler(ctrlType):
        '''
        The signal handler for the Update service always returns True.
        '''
        return True

    def main(self):
        servicemanager.LogInfoMsg('*** Inside UpdateService - def(main)')
        self.running = True
        while self.running:
            self.run()

    def run(self):
        '''
        You should override this method when you subclass Daemon.
        It will be called after the process has been daemonized by start() or
        restart().
        '''
        raise exceptions.NotImplementedError()

    def local_init(self):
        '''
        Override this method for additional items to be initialized during
        daemonization, after the fork but before the main .run(..) call.
        '''
        raise exceptions.NotImplementedError()

    def local_shutdown(self):
        '''
        Override this method for any functionality you need executed during
        shutdown of this daemon or service.
        '''
        raise exceptions.NotImplementedError()

# vim:set ai et sts=4 sw=4 tw=80:
