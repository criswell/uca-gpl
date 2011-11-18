import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import clientagent.common.ClientAgentState as ClientAgentState

class Service(win32serviceutil.ServiceFramework):
    """
    Generic Windows Service class with the same framework as the Linux
    daemon class.
    """

    _svc_name_ = ClientAgentState.SRV_NAME
    _svc_display_name_ = ClientAgentState.SRV_DISPLAY_NAME

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.local_shutdown()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.local_init()
        self.run()

    def start(self):
        """
        Starts the Windows service
        """
        self.SvcDoRun()

    def stop(self):
        """
        Stops the Windows service
        """
        self.SvcStop()

    def restart(self):
        """
        Restart the windows service
        """
        self.SvcStop()
        self.SvcDoRun()

    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been daemonized by start() or
        restart().
        """
        pass

    def local_init(self):
        """
        Override this method for additional items to be initialized during
        daemonization, after the fork but before the main .run(..) call.
        """
        pass

    def local_shutdown(self):
        """
        Override this method for any functionality you need executed during
        shutdown of this daemon or service.
        """
        pass

# vim:set ai et sts=4 sw=4 tw=80:
