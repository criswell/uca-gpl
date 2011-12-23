#!/usr/bin/env python

'''
nmsa_handler.py
---------------
The main handler daemon for the various NMSA features and functionality

- Note: While the dispatcher/steward combo proper was designed with Python as
"off the table", for the NMSA handler, we can use it because it automatically
requires platforms with a full Python stack.
'''

import sys, time, os
import logging
import ConfigParser as configparser

# NMSA specific modules
sys.path.append('/opt/intel/eil/clientagent/lib')
from nmsa_daemon import Daemon
from nmsa_conf import setup_conf
from nmsa_main import NMSA_Master

# Global settings and overrides

'''The minimum timer resolution for main run loop'''
MIN_TIMER_RES = 10

'''The file toggle that determines if we should run or not'''
NMSA_TOGGLE = '/opt/intel/eil/clientagent/home/.nmsa_enable'

'''The maximum number of times we attempt to register before giving up on failures'''
MAX_REG_ATTEMPTS = 10

'''The maximum number of times we attempt to poll NMSA before giving up on failures'''
MAX_POLL_ATTEMPTS = 20

class HandlerDaemon(Daemon):
    __log_file = '/opt/intel/eil/clientagent/home/nmsa_handler.log'
    __conf_file = '/opt/intel/eil/clientagent/home/nmsa_handler.cfg'
    __sleep_timer = 30
    __debug_level = logging.WARNING

    def local_init(self):
        logging.basicConfig(
            filename=self.__log_file,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.logger = logging.getLogger()

        self.config = setup_conf(self.__conf_file)
        if self.config.has_option('main', 'sleep_timer'):
            self.__sleep_timer = self.config.getint('main', 'sleep_timer')

        if self.__sleep_timer < MIN_TIMER_RES:
            self.__sleep_timer = MIN_TIMER_RES

        if self.config.has_option('main', 'log_level'):
            log_level = self.config.getint('main', 'log_level')
            if log_level == 0:
                self.__debug_level = logging.CRITICAL
            elif log_level == 1:
                self.__debug_level = logging.ERROR
            elif log_level == 2:
                self.__debug_level = logging.INFO
            elif log_level == 3:
                self.__debug_level = logging.WARNING
            else:
                self.__debug_level = logging.DEBUG

        max_reg = MAX_REG_ATTEMPTS
        if self.config.has_option('main', 'registration_attempts'):
            max_reg = self.config.getint('main', 'registration_attempts')

        max_poll = MAX_POLL_ATTEMPTS
        if self.config.has_option('main', 'poll_retry_attempts'):
            max_poll = self.config.getint('main', 'poll_retry_attempts')

        self.logger.setLevel(self.__debug_level)

        self.masterControl = NMSA_Master(max_reg_attempts=max_reg, max_poll_attempts=max_poll)

        self.logger.info('Handler start up...')

    def run(self):
        while True:
            self.logger.debug('Starting NMSA handler activity...')
            self.masterControl.run()
            if self.masterControl.failure:
                self.logger.critical('Failure in MasterControl! Stopping daemon!')
                self.stop()
            else:
                time.sleep(self.__sleep_timer)

def usage():
    print "Usage:\n"
    print "\tnmsa_handler.py COMMAND"
    print "\t\twhere 'COMMAND' is one of the following:\n"
    print "\tstart\t\tStart the daemon"
    print "\tstop\t\tStop the daemon"
    print "\trestart\t\tRestart the daemon"

if __name__ == "__main__":
    daemon = HandlerDaemon('/opt/intel/eil/clientagent/home/nmsa_handler.pid')
    if os.path.isfile(NMSA_TOGGLE):
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                daemon.start()
            elif 'stop' == sys.argv[1]:
                daemon.stop()
            elif 'restart' == sys.argv[1]:
                daemon.restart()
            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)
        else:
            usage()
            sys.exit(2)
    else:
        usage()
        print "\nThe file:\n\n\t'%s'\n\nmust exist before running this daemon" % NMSA_TOGGLE
        sys.exit(2)

# vim:set ai et sts=4 sw=4 tw=80:
