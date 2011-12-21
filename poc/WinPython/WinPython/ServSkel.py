## get windows serivce utility stuff
import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

import win32api
print "***********---> We are inside ServSkel - in front of class def    RC 12-5-2011 ********"
import logging
logging.basicConfig(
                    filename = "UClient.log",
                    pathname = "C:\EIL\Log",
                    format = "%(levelname)-10s %(asctime)s %(message)s",
                    level = logging.DEBUG
                    )

logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)
logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
logging.getLogger('suds.resolver').setLevel(logging.DEBUG)
logging.getLogger('suds.xsd.query').setLevel(logging.DEBUG)
logging.getLogger('suds.xsd.basic').setLevel(logging.DEBUG)
logging.getLogger('suds.binding.marshaller').setLevel(logging.DEBUG)


class UnifiedClientTest(win32serviceutil.ServiceFramework):
    _svc_name_ = "UnifiedClientTst"
    _svc_display_name_ = "UnifiedClientTst" 
    _svc_description_ = "EIL Portal Unified Client Service (Python) - resides on client - interfaces with CCMS"

    logging.debug("***********---> We are inside ServSkel - we are beginning    RC 12-5-2011  *******")
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        ##socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        import servicemanager
        import win32api
        import win32event
        logging.debug("***********---> We are inside SvcDoRun - prior to LOGMSG call    RC 12-5-2011  *******")
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        logging.debug("***********---> We are inside SvcDoRun - after LOGMSG call    RC 12-5-2011  *******")
        self.timeout = 3000      ## this sets a 50 minute timeout  3000 seconds = 50 minutes
                                 ## but acts more like a 3 second timer - RC

        while 1:
            ##   wait for service stop signal, if 1 timeout, loop again ##
            logging.debug("***********---> We are inside SvcDoRun - after LOGMSG call    RC 12-5-2011  *******")
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            ##  check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                ## stop signal encountered
                servicemanager.LogInfoMsg("UnifiedClientSvc - Stopped")
                logging.debug("***********---> We are inside SvcDoRun - stopped     RC 12-5-2011  *******")
                break
            else:
                servicemanager.LogInfoMsg("UnifiedClientSvc - running and healthy")
                logging.debug("***********---> We are inside SvcDoRun - running     RC 12-5-2011  *******")
                self.main()
       
    def ctrlHandler(ctrlType):
        return True

    def main(self):
                     logging.debug("***********---> We are inside in def(main) RC 12-5-2011  *******")
                     logging.debug("***********---> Here is where our python code would run -- Right Here: X   ******")
        ##pass
if __name__ == '__main__':
             #win32api.SetConsoleCtrlHandler(ctrlHandler, True)
             logging.debug("***********---> We are inside in pgm flow      about to do win32service RC 12-5-2011  *******")
             win32serviceutil.HandleCommandLine(UnifiedClientTest)
             logging.debug("***********---> We are inside in pgm flow      after win32service RC 12-5-2011  *******")
             ##pass
