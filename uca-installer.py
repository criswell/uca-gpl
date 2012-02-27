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

HOSTS = {
        '172.16.3.10' : ['eilportal.eil-infra.com', 'eilportal'],
        '172.16.3.10' : ['rmssrvr01.eil-infra.com', 'rmssvr01'],
        '172.16.3.10' : ['eilauto01.eil-infra.com', 'eilauto01'],
        '10.4.0.123' : [' nmsa01.eil-infra.com', 'nmsa01']
    }

logger = logging.getLogger('uca-installer')
logger.setLevel(logging.DEBUG)
if IS_WINDOWS:
        logging.basicConfig(filename='C:\\install.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig('/install.log',
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

def setupHosts(hostsFile):
    '''
    Will attempt to set up the hosts file located at the path hostsFile for
    UCA use. Will return True on success, or False on failure.
    '''
    if os.path.isfile(hostsFile):
        hosts = open(hostsFile, 'rU')
        
        for rawline in hosts:
            line = rawline.strip()
            if '#' in line:
                line = line[:line.index('#')]
                
            if line:
                destination, aliases = re.split(r'\s', line, 1)
                
                # NOTE: This is pretty blunt- we check that the IP is there,
                # but not whether or not it is aliased correctly. May want to
                # reapproach this later on and see if this is sufficient.
                # TODO
                if HOSTS.has_key(destination):
                    # dummy is throw-away, we just want it out of the dict
                    dummy = HOSTS.pop(destination)
                    
        hosts.close()
        
        # Now, add missing entries
        if len(HOSTS) > 0:
            hosts = open(hostsFile, 'aU')
            
            hostAliases = []
            for ip in HOSTS.keys():
                hostAliases.append('%s    %s' % (ip, HOSTS[ip]))
                
            hosts.writelines(hostAliases)
            hosts.close()

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

def win32_setupHosts():
    '''
    Runs through the annoying myriad of locations that the hosts file might be
    located on Windows and attempts to set it up for UCA use.
    '''
    logger.info('Attempting to set up the hosts file in Windows- looking for environment variable defining system root...')
    possibleHostFiles = []
    try:
        systemroot = os.environ['SYSTEMROOT']
    except KeyError:
        pass
    else:
        # This is by far the most likely place for it
        possibleHostFiles.append('%s\\system32\\drivers\\etc\\hosts' % systemroot)

    try:
        systemroot = os.environ['WINDIR']
    except KeyError:
        pass
    else:
        possibleHostFiles.append('%s\\hosts' % systemroot)

    if len(possibleHostFiles) > 1:
        for filename in possibleHostFiles:
            logger.info('Trying host file "%s"' % filename)
            if setupHosts(filename):
                return
        logger.critical('Could not modify hosts file, some problem occured. Install might not work.')
    else:
        logger.critical('Could not find appropriate environment variable for where the system files are. Could not set up hosts file as a result.')

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

def installAt(rootDir, srcDir):
    '''
    Installs to a root directory structure.
    '''
    binDir = '%s/bin' % rootDir
    srcBinDir = '%s/uca/bin' % srcDir
    logger.info('Attempting to install...')
    logger.info('Copying the bin directory')
    logger.info('%s -> %s' % (srcBinDir, binDir)
    shutil.copytree(srcBinDir, binDir)
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
    # Set up our hosts file (or try to)
    win32_setupHosts()
    # Now install
    installAt('C:\\eil')

# vim:set ai et sts=4 sw=4 tw=80:
