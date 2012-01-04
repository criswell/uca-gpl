import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from clientagent import ClientAgentState

class Service(win32serviceutil.ServiceFramework):
    """
    Generic Windows Service class with the same framework as the Linux
    daemon class.
    """

    _svc_name_ = ClientAgentState.SRV_NAME
    _svc_display_name_ = ClientAgentState.SRV_DISPLAY_NAME
    _svc_description_ = ClientAgentState.SRV_DESCRIPTION

    EndServ = False

    ##logging.debug("***********---> We are inside UnifiedClientAgent - we are beginning    RC 12-5-2011  *******")
    servicemanager.LogInfoMsg("***********---> We are inside windows_service.py - we are beginning    RC 12-5-2011  *******")
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        ##socket.setdefaulttimeout(60)

    def SvcStop(self):
        ##servicemanager.LogInfoMsg("******** Entering  SvcStop: " + EndServ + "    ****")
        self.EndServ = True
        ##servicemanager.LogInfoMsg("******** Value of EndServ (should be Y): " + EndServ + "    ****")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        import servicemanager
        import win32api
        import win32event
        servicemanager.LogInfoMsg("We are inside windows_service SvcDoRun - before LOGMSG call")
        ##logging.debug("***********---> We are inside SvcDoRun - prior to LOGMSG call    RC 12-5-2011  *******")
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        ##logging.debug("***********---> We are inside SvcDoRun - after LOGMSG call    RC 12-5-2011  *******")
        self.timeout = 3000       ## this sets a 50 minute timeout  3000 seconds = 50 minutes
                                  ## but acts more like a 3 second timer - RC
                                  ## CHGD FROM 3000 TO 30000 rc 12/6/11 and back again 12-7
        ##while 1:
        self.local_init()
        while win32event.WaitForSingleObject(self.hWaitStop, self.timeout) == win32event.WAIT_TIMEOUT:
            ##   wait for service stop signal, if 1 timeout, loop again ##
            ##logging.debug("***********---> We are inside SvcDoRun - after LOGMSG call    RC 12-5-2011  *******")
            servicemanager.LogInfoMsg("We are inside windows_service SvcDoRun - after LOGMSG call")
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            ##  check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                ## stop signal encountered
                servicemanager.LogInfoMsg("windows_service EILClientAgt - Stopped")
                ##global EndServ
                ##EndServ = "Y"
                ##logging.debug("***********---> We are inside SvcDoRun - stopped     RC 12-5-2011  *******")
                break
            else:
                servicemanager.LogInfoMsg("windows_service EILClientAgt - running and healthy")
                ##logging.debug("***********---> We are inside SvcDoRun - running     RC 12-5-2011  *******")
                ##logging.info("***********---> We are inside SvcDoRun - running     RC 12-5-2011  *******")
                self.main()

    def ctrlHandler(ctrlType):
        return True

    def main(self):
        servicemanager.LogInfoMsg("We are inside windows_service in def(main) - Here is where our python code runs inside the Service via a call to runme()  ")
        self.run()

    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been daemonized by start() or
        restart().
        """
        raise exceptions.NotImplementedError()

    def local_init(self):
        """
        Override this method for additional items to be initialized during
        daemonization, after the fork but before the main .run(..) call.
        """
        raise exceptions.NotImplementedError()

    def local_shutdown(self):
        """
        Override this method for any functionality you need executed during
        shutdown of this daemon or service.
        """
        raise exceptions.NotImplementedError()

# vim:set ai et sts=4 sw=4 tw=80:
