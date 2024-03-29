import sys, os, time, atexit
from signal import SIGTERM
import logging
import exceptions
from clientagent import get_config

class Daemon:
    """
    Generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self):
        self.config = get_config()
        self.stdin = self.config.C.get('linux', 'daemon_stdin')
        self.stdout = self.config.C.get('linux', 'daemon_stdout')
        self.stderr = self.config.C.get('linux', 'daemon_stderr')
        self.pidfile = self.config.C.get('linux', 'pidfile')
        self.debug = False

    def daemonize(self):
        """
        Double fork to completely prevent zombie processes (this is necessary
        as we may be ran from steward).
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)

    def checkprocess(self, pid):
        '''
        Checks if a given process ID (pid) is a running process. Returns True
        if it is, False if it is not.
        '''
        return os.path.exists('/proc/%s' % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self, debug=False):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        self.debug = debug
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            if checkprocess(pid):
                message = "pidfile %s already exist. Daemon is already running.\n"
                sys.stderr.write(message % self.pidfile)
            else:
                message = "pidfile %s already exist. However, daemon is not running.\n"
                sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        if not self.debug:
            self.daemonize()
        self.local_init()
        self.main()
        self.stop()

    def stop(self, quiet=False):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            if not quiet:
                message = "pidfile %s does not exist. Daemon not running?\n"
                sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        logging.shutdown()

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def status(self):
        '''
        Query the status of the daemon
        '''
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running\n"
            sys.stdout.write(message % self.pidfile)
        else:
            if checkprocess(pid):
                message = "daemon running, proccess %s\n"
                sys.stdout.write(message % pid)
            else:
                message = "pidfile %s exists, but daemon not running as process %s\n"
                sys.stdout.write(message % (self.pidfile, pid))


    def main(self):
        running = True
        while running:
            running = self.run()

    def restart(self):
        """
        Restart the daemon
        """
        self.stop(True)
        self.start()

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
