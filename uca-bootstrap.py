#!/usr/bin/env python

'''
uca-bootstrap.py
----------------
Basic bootstrap tool for the Unified Agent which runs on both Windows and Linux.
NOTE- For now, this will be fairly rough. But if we decide to keep using it, we
will want to refine it considerably.
'''

import urllib, zipfile, os, tempfile, shutil, sys, logging

# Platform determination
if os.name == 'nt':
    IS_WINDOWS = True
    IS_LINUX = False
else:
    IS_WINDOWS = False
    IS_LINUX = True

PRODUCTION_IP = '172.16.3.10'
STAGING_IP = '10.4.0.66'

ROOT_DIR = 'C:\\eil'
if IS_LINUX:
    ROOT_DIR = '/opt/intel/eil/clientagent'

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

# For logging, we need to ensure that the root directory is there
mkdir_p("%s/home/" % ROOT_DIR)

logger = logging.getLogger('uca-bootsrap')
logger.setLevel(logging.DEBUG)
if IS_WINDOWS:
        logging.basicConfig(filename='C:\\install.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig('/install.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(logging.StreamHandler())

def exec_command(cmd):
    stream = os.popen(cmd)
    output = stream.readlines()
    stream.close()
    for line in output:
        print line

def setupBin(binDir, srcBinDir):
    logger.info('Cleaning up the bin directory (if it exists)')
    shutil.rmtree(binDir, True)

    logger.info('Copying the bin directory')
    logger.info('%s -> %s' % (srcBinDir, binDir)
    shutil.copytree(srcBinDir, binDir)

def unZip(filename, tempDir):
    if sys.version_info[0] < 3 and sys.version_info[1] < 7 and IS_LINUX:
        # Horrible that we have to do this on legacy Python installs
        exec_command('unzip %s -d %s' % (filename, tempDir))
    else:
        ucaZip = zipfile.ZipFile(filename, 'r')
        binDir = '%s/bin' % ROOT_DIR

        logger.info('Extracting the UCA into tempDir')
        ucaZip.extractall(tempDir)
        ucaZip.close()


# Start out by grabbing the latest UCA - NOTE we're pulling from staging here
try:
    url = 'http://%s/ucaPhase1/uca.zip' % STAGING_IP
    logger.info('Pulling UCA zipefile: %s' % url)
    (filename, headers) = urllib.urlretrieve(url)
    logger.info('Stored in "%s"...' % filename)

    binDir = '%s/bin' % ROOT_DIR
    #logger.info('Making binDir "%s"...' % binDir
    #mkdir_p(binDir)
    tempDir = tempfile.mkdtemp()
    logger.info('Obtained a tempDir "%s"...' % tempDir)

    unZip(filename, tempDir)

    srcBinDir = '%s/uca/bin' % tempDir

    if IS_LINUX:
        logger.info('Linux> Stopping previous client agent')
        exec_command('/etc/init.d/eil_steward.sh stop')
        setupBin(binDir, srcBinDir)
        logger.info('Linux> Installing dispatcher')
        exec_command('chmod a+x %s/uca/linux/dispatcher/install.sh' % tempDir)
        exec_command('cd %s/uca/linux/dispatcher; ./install.sh' % tempDir)
        # FIXME - Missing elevate scipt
        logger.info('Linux> Starting new client agent')
        exec_command('chmod a+x %s/eil_steward.py' % binDir)
        exec_command('chmod a+x %s/elevate_script' % binDir)
        exec_command('/etc/init.d/eil_steward.sh start')
    else:
        logger.info("Windows> Stopping and removing previous services")
        exec_command('net stop EILTAFService')
        exec_command('sc delete EILTAFService')
        exec_command('sc delete EILAutoUpdateService')
        setupBin(binDir, srcBinDir)
        os.chdir('C:/EIL/bin')
        logger.info("Windows> Installing new service")
        exec_command('python C:\\EIL\\bin\\eil_steward.py --username localsystem --startup auto install')
        exec_command('sc failure EILClientAgent reset= 30 actions= restart/5000')
        exec_command('sc start EILClientAgent')
        exec_command('sc queryex EILClientAgent')

    # FIXME clean-up tempDir

    # FIXME - Do we need to clean-up ucaZip?
except Exception, e:
    logger.critical("Error trying to bootstrap the unified agent")
    logger.critical(e)

# vim:set ai et sts=4 sw=4 tw=80:
