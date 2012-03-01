#!/usr/bin/env python

'''
uca-installer.py
----------------
Basic installer for the UCA. Should be platform agnostic, and run by the
bootstrapper during installation.
'''

import os, logging, dircache, shutil, traceback, sys, tempfile, subprocess

# Platform determination
if os.name == 'nt':
    IS_WINDOWS = True
    IS_LINUX = False
    import win32service
else:
    IS_WINDOWS = False
    IS_LINUX = True

''' The host file definitions '''
HOSTS = {
        '172.16.3.10' : ['eilportal.eil-infra.com', 'eilportal'],
        '172.16.3.10' : ['rmssrvr01.eil-infra.com', 'rmssvr01'],
        '172.16.3.10' : ['eilauto01.eil-infra.com', 'eilauto01'],
        '10.4.0.123' : [' nmsa01.eil-infra.com', 'nmsa01']
    }

'''  The directories to create in the root tree '''
DIRS = [ 'bin', 'lib', 'doc', 'tools', 'home', 'scripts', 'postinst' ]

''' A list of any Python scripts we should not pre-compile '''
PRECOMPILE_EXCEPTIONS = [ 'eil_steward.py', 'uca-installer.py' ]

logger = logging.getLogger('uca-installer')
logger.setLevel(logging.DEBUG)
if IS_WINDOWS:
    logging.basicConfig(filename='C:\\uca-install.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig('/uca-install.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(logging.StreamHandler())

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

def win32_installTools(rootDir):
    '''
    Given the rootDir, will install the Windows-specific tools.
    '''
    logger.info('Installing tools...')
    # FIXME - Add items here
    pass

# Linux specific functions
def linux_stopPreviousDaemons():
    '''
    Stop previous Linux agent daemons. Will not remove them or uninstall them
    from the system.
    '''
    if os.path.isfile('/etc/init.d/eil_steward.sh'):
        exec_command('/etc/init.d/eil_steward.sh stop')
    if os.path.isfile('/etc/init.d/nmsa_handler.sh'):
        exec_command('/etc/init.d/nmsa_handler.sh stop')

def linux_uninstallPreviousAgent(srcDir):
    '''
    Uninstall any previous Linux agent daemons.
    '''
    # We use system's unlink because we don't want to fail on errors
    exec_command('unlink /usr/bin/eil_steward')
    exec_command('unlink /bin/eil_steward')
    exec_command('chmod a+x %s/uca/linux/dispatcher/install.sh' % srcDir)
    exec_command('cd %s/uca/linux/dispatcher; ./install.sh -p' % srcDir)

def linux_setupHosts():
    '''
    Set up the hosts file under Linux.
    '''
    logger.info('Attempting to set up the hosts file in Linux...')
    if setupHosts('/etc/hosts'):
        return
    logger.critical('Could not modify hosts file, install might not work.')

def linux_installDispatcher(dst, src):
    '''
    Install the dispatcher items to the dst directory. The archive from which
    the dispatcher is installed from is in src.
    '''
    logger.info('Attempting to install the Linux dispatcher...')
    exec_command('chmod a+x %s/uca/linux/dispatcher/install.sh' % src)
    exec_command('cd %s/uca/linux/dispatcher; ./install.sh' % src)

def linux_installTools(dst, src):
    '''
    Install any other tools specific to Linux. The archive is from src, and
    the root install directory is dst.
    '''
    logger.info('Installing tools...')
    # FIXME - Add items here
    pass

# Generic functions
def recursive_delete(dirname):
    '''
    Given a directory, will attempt to recursively delete all entries. Will
    return True on success, False on failure.
    '''
    retval = True
    files = dircache.listdir(dirname)
    for file in files:
        path = os.path.join (dirname, file)
        if os.path.isdir(path):
            retval = recursive_delete(path)
        else:
            try:
                os.unlink(path)
            except:
                logger.critical('Unable to remove %s! Is file still in use?' % path)
                retval = False

    try:
        shutil.rmtree(dirname, True)
    except:
        logger.critical('Unable to remove directory %s! Contents may still be in use...' %path)
        retval = False

    return retval

def cleanUpPreviousTree(rootDir):
    '''
    Attempts to clean up previous install tree if it is present.
    '''
    logger.info('Attempting to clean-up previous EIL install tree (if present)...')
    # The previous bootstrapper was a bit indelicate with regard to this. So
    # we will be taking a more nuanced aproach.
    recursive_delete(rootDir)

def createTreeAt(rootDir):
    '''
    Attempts to create a standard, cross-platform, install tree at the root
    directory 'rootDir'
    '''
    logger.info('Attempting to create EIL install tree...')
    for dir in DIRS:
        try:
            mkdir_p(os.path.join(rootDir, dir))
        except:
            logger.critical('Could not create "%s/%s"! Traceback follows...' % (rootDir, dir))
            traceback_lines = traceback.format_exc().splitlines()
            for line in traceback_lines:
                logger.critical(line)

def installAt(rootDir, srcDir):
    '''
    Installs to a root directory structure.
    '''
    binDir = os.path.join(rootDir, 'bin')
    srcBinDir = os.path.join(srcDir, 'uca', 'bin') 
    logger.info('Attempting to install...')
    logger.info('Copying the bin directory')
    logger.info('%s -> %s' % (srcBinDir, binDir)
    shutil.copytree(srcBinDir, binDir)

def exec_command(cmd):
    '''
    given a command, will execute it in the parent environment
    '''
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.readlines()
    p.stdin.close()
    p.stdout.close()
    for line in output:
        logger.info(line)

def mkdir_p(path):
    '''
    Does the equivalent of a 'mkdir -p' (Linux) on both platforms.
    '''
    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

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
            hosts = open(hostsFile, 'a')

            hostAliases = []
            for ip in HOSTS.keys():
                aliases = ' '.join(HOSTS[ip])
                hostAliases.append('%s    %s' % (ip, aliases)

            hosts.writelines(hostAliases)
            hosts.close()

def copyHome(srcDir, dstDir):
    '''
    Copy the home directory (log and config files)
    '''
    try:
        logger.info('Attempting to copy the home directory...')
        src = os.path.join(srcDir, 'home')
        dst = os.path.join(dstDir, 'home')
        shutil.copytree(src, dst)
    except:
        logger.critical('Error copying the home directory!')
        traceback_lines = traceback.format_exc().splitlines()
        for line in traceback_lines:
            logger.critical(line)

 def precompilePy(srcDir):
    '''
    Will run through the source archive directory and pre-compile all the Python
    objects other than those exceptions defined. It will also remove the source
    python files.
    '''
    for root, dirs, files in os.walk(srcDir):
        for file in files:
            if file not in PRECOMPILE_EXCEPTIONS:
                try:
                    py_compile.compile(os.path.join(root, file))
                    os.unlink(os.path.join(root, file))
                except:
                    logger.critical('Error precompiline a file!')
                    traceback_lines = traceback.format_exc().splitlines()
                    for line in traceback_lines:
                        logger.critical(line)

'''Main installation sequence'''
if len(sys.argv) == 2:
    srcDir = sys.argv[1]
    # PRECOMPILE ALL THE THINGS!
    precompilePy(srcDir)
    if IS_LINUX:
        logger.info('Attempting to stop any previous EIL agents...')
        linux_stopPreviousDaemons()
        # Back-up home
        tempdir = tempfile.mkdtemp()
        copyHome('/opt/intel/eil/clientagent', tempdir)
        # Uninstall the previous agent
        linux_uninstallPreviousAgent(srcDir)
        # Clean up previous install tree, then re-create proper format
        cleanUpPreviousTree('/opt/intel/eil/clientagent')
        createTreeAt('/opt/intel/eil/clientagent')
        # Set up our hosts file (or try to)
        linux_setupHosts()
        # Now install
        installAt('/opt/intel/eil/clientagent', srcDir)
        # Install the rest of the Linux-specific items
        linux_installDispatcher('/opt/intel/eil/clientagent', srcDir)
        linux_installTools('/opt/intel/eil/clientagent', srcDir)
        # Restore home
        copyHome(tempdir, '/opt/intel/eil/clientagent')
        recursive_delete(tempdir)
    else:
        logger.info('Attempting to stop and remove any previous EIL services...')
        win32_stopPreviousServices()
        # Back-up home
        tempdir = tempfile.mkdtemp()
        copyHome('C:\\eil', tempdir)
        # Clean up previous install tree, then re-create proper format
        cleanUpPreviousTree('C:\\eil')
        createTreeAt('C:\\eil')
        # Set up our hosts file (or try to)
        win32_setupHosts()
        # Now install
        installAt('C:\\eil', srcDir)
        # Any Windows-specific install items
        win32_installTools('C:\\eil')
        # Restore home
        copyHome(tempdir, 'C:\\eil')
        recursive_delete(tempdir)
else:
    print "Not enough parameters given to installer!\n"
    print "The UCA installer requires the path to the extracted UCA archive:"
    print "\tuca-installer.py path_to_uca_archive\n"
    print "This installer is intended to be ran by the UCA bootstrapper."

# vim:set ai et sts=4 sw=4 tw=80:
