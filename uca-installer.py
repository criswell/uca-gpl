#!/usr/bin/env python

'''
uca-installer.py
----------------
Basic installer for the UCA. Should be platform agnostic, and run by the
bootstrapper during installation.
'''

import os, logging

# Platform determination
if os.name == 'nt':
    IS_WINDOWS = True
    IS_LINUX = False
    import win32service
else:
    IS_WINDOWS = False
    IS_LINUX = True

logger = logging.getLogger('uca-installer')
logger.setLevel(logging.DEBUG)
if IS_WINDOWS:
        logging.basicConfig(filename='%s\\home\install.log' % ROOT_DIR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        fn = '%s/home/install.log' % ROOT_DIR
        logging.basicConfig(filename=fn,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(logging.StreamHandler())

def exec_command(cmd):
    '''
    given a command, will execute it in the parent environment
    '''
    stream = os.popen(cmd)
    output = stream.readlines()
    stream.close()
    for line in output:
        print line

# Windows specific functions
def win32_checkServiceRunning(name):
    '''
    Given the name of a Windows service, will query for it to determine if it is
    running. Returns 'True' if the service is running.
    '''
    returnCode = False
    try:
        scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
        svc = win32service.OpenService(scm, name, win32service.SC_MANAGER_ALL_ACCESS)
        status = win32service.QueryServiceStatus(svc)
        win32service.CloseService(svc)
        if status[1] == 4:
            returnCode = True
    except:
        pass
    finally:
        win32service.CloseService(svc)

    return returnCode

def win32_stopService(name):
    '''
    Given the name of a Windows service, will query for it and attempt to stop
    it (if running) and delete it.
    '''
    try:
        if win32_checkServiceRunning(name):
            # Service is running, stop it
            exec_command('net stop %s' % name)
        exec_command('sc delete %s' % name)
    except:
        logger.info("Service %s not found or some other error on access." % name)
    finally:
        win32service.CloseService(svc)

def win32_stopPreviousServices():
    '''
    Attempts to stop and clean up any previous services under Windows.
    '''
    for service in ['EILTAFService', 'EILAutoUpdateService', 'EILClientAgent']:
        win32_stopService(service)
        if win32_checkServiceRunning(service):
            logger.critical('Unable to clean up %s! It is still running!' % service)

# Linux specific functions

# Generic functions
def cleanUpPreviousTree(rootDir):
    '''
    Attempts to clean up previous install tree if it is present.
    '''
    logger.info('Attempting to clean-up previous EIL install tree (if present)...')
    pass

def createTreeAt(rootDir):
    '''
    Attempts to create a standard, cross-platform, install tree at the root
    directory 'rootDir'
    '''
    logger.info('Attempting to create EIL install tree...')
    pass

'''Main installation sequence'''

if IS_LINUX:
    pass
else:
    logger.info('Attempting to stop and remove any previous EIL services...')
    win32_stopPreviousServices()
    # Clean up previous install tree, then re-create proper format
    cleanUpPreviousTree('C:\\eil')
    createTreeAt('C:\\eil')

# vim:set ai et sts=4 sw=4 tw=80:
