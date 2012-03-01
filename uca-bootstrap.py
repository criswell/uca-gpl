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

logger = logging.getLogger('uca-bootsrap')
logger.setLevel(logging.DEBUG)
if IS_WINDOWS:
        logging.basicConfig(filename='C:\\uca-install.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig('/uca-install.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(logging.StreamHandler())

def exec_command(cmd):
    stream = os.popen(cmd)
    output = stream.readlines()
    stream.close()
    for line in output:
        print line

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

if IS_LINUX and something:
    # Version check for python
    pass
else:
    # Start out by grabbing the latest UCA - NOTE we're pulling from staging here
    try:
        url = 'http://%s/ucaPhase1/uca.zip' % STAGING_IP
        logger.info('Pulling UCA zipefile: %s' % url)
        (filename, headers) = urllib.urlretrieve(url)
        logger.info('Stored in "%s"...' % filename)

        tempDir = tempfile.mkdtemp()
        logger.info('Obtained a tempDir "%s"...' % tempDir)

        if IS_LINUX:
            # Version check for older Python
            pass
        else:
            unZip(filename, tempDir)

            exec_command('python %s/uca-installer.py' % tempDir)

        # FIXME clean-up tempDir

        # FIXME - Do we need to clean-up ucaZip?

        # FIXME - move log file into destination
    except Exception, e:
        logger.critical("Error trying to bootstrap the unified agent")
        logger.critical(e)

# vim:set ai et sts=4 sw=4 tw=80:
