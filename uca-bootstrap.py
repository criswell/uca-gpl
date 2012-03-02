#!/usr/bin/env python

'''
uca-bootstrap.py
----------------
Basic bootstrap tool for the Unified Agent which runs on both Windows and Linux.
NOTE- For now, this will be fairly rough. But if we decide to keep using it, we
will want to refine it considerably.
'''

import urllib, zipfile, os, tempfile, shutil, sys, logging, traceback
import subprocess

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
logFile = None
dstLogFile = os.path.join(ROOT_DIR, 'home', 'uca-install.log')
if IS_WINDOWS:
    logFile = 'C:\\uca-install.log'
    logging.basicConfig(filename=logFile,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
else:
    logFile = '/uca-install.log'
    logging.basicConfig(filename=logFile,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(logging.StreamHandler())

def exec_command(cmd, noLog=False):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.readlines()
    p.stdin.close()
    p.stdout.close()

    for line in output:
        line = line.rstrip()
        if not noLog:
            logger.info(line)
        else:
            print line

def unZip(filename, tempDir):
    if IS_LINUX and os.path.isfile('/usr/bin/unzip'):
        # Horrible that we have to do this on legacy or buggy Python installs
        exec_command('unzip %s -d %s' % (filename, tempDir))
    else:
        ucaZip = zipfile.ZipFile(filename, 'r')
        binDir = '%s/bin' % ROOT_DIR

        logger.info('Extracting the UCA into tempDir')
        ucaZip.extractall(tempDir)
        ucaZip.close()
        logger.info('Extracted...')

if sys.version_info[0] < 3 and sys.version_info[1] < 6 and IS_LINUX:
    # Default to old LCA
    url = 'http://172.16.3.10/EILLinuxAgent/latest/clientagent-bootstrap.sh'
    logger.info('Pulling LCA bootsrap: %s' % url)
    (filename, headers) = urllib.urlretrieve(url)
    logger.info('Stored in "%s"...' % filename)
    exec_command('chmod a+x %s ; sh %s' % (filename, filename))
else:
    # Start out by grabbing the latest UCA - NOTE we're pulling from staging here
    try:
        url = 'http://%s/uca/uca.zip' % STAGING_IP
        logger.info('Pulling UCA zipfile: %s' % url)
        (filename, headers) = urllib.urlretrieve(url)
        logger.info('Stored in "%s"...' % filename)

        tempDir = tempfile.mkdtemp()
        logger.info('Obtained a tempDir "%s"...' % tempDir)

        unZip(filename, tempDir)

        logger.info('Executing the installer...')

        installer = os.path.join(tempDir, 'uca', 'uca-installer.py')
        command = 'python %s %s' % (installer, tempDir)

        logger.info(command)

        exec_command(command, True)

        # Clean-up tempDir (do a best effort here, but don't bomb on failure)
        try:
            shutil.rmtree(tempDir, True)
        except:
            logger.info('Could not remove tmpDir, "%s"...' % tempDir)
            traceback_lines = traceback.format_exc().splitlines()
            for line in traceback_lines:
                logger.info(line)

        # Clean-up ucaZip (again, best effort)
        try:
            os.unlink(filename)
        except:
            logger.info('Could not remove zip file, "%s"...' % filename)
            traceback_lines = traceback.format_exc().splitlines()
            for line in traceback_lines:
                logger.info(line)
    except:
        logger.critical("Error trying to bootstrap the unified agent")
        traceback_lines = traceback.format_exc().splitlines()
        for line in traceback_lines:
            logger.critical(line)

# Move log file into destination
try:
    logging.shutdown()

    if os.path.isfile(dstLogFile):
        installLogFile = open(logFile, 'rU')
        installLog = installLogFile.readlines()
        installLogFile.close()

        installLogFile = open(dstLogFile, 'a')
        installLogFile.writelines(installLog)
        installLogFile.close()

        os.unlink(logFile)
    else:
        shutil.move(logFile, dstLogFile)
except:
    print "Error shutting down and moving the install log..."
    traceback_lines = traceback.format_exc().splitlines()
    for line in traceback_lines:
        print line

# vim:set ai et sts=4 sw=4 tw=80:
