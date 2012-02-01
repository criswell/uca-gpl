#!/usr/bin/env python

'''
uca-bootstrap.py
----------------
Basic bootstrap tool for the Unified Agent which runs on both Windows and Linux.
NOTE- For now, this will be fairly rough. But if we decide to keep using it, we
will want to refine it considerably.
'''

import urllib, zipfile, os, tempfile, shutil, sys

# Platform determination
if os.name == 'nt':
    IS_WINDOWS = True
    IS_LINUX = False
else:
    IS_WINDOWS = False
    IS_LINUX = True

PRODUCTION_IP = '172.16.3.10'
STAGING_IP = '10.4.0.66'

HOSTS = {
        '10.4.0.29' : ['goblinserver2'],
        '172.16.3.10' : ['rmssrvr01.eil-infra.com', 'rmssvr01'],
        '172.16.3.10' : ['eilauto01.eil-infra.com', 'eilauto01'],
        '10.4.0.123' : [' nmsa01.eil-infra.com', 'nmsa01']
    }

ROOT_DIR = 'C:\\eil'
if IS_LINUX:
    ROOT_DIR = '/opt/intel/eil/clientagent'

def mkdir_p(path):
    '''
    Does the equivalent of a 'mkdir -p' (Linux) on both platforms.
    '''
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def exec_command(cmd):
    stream = os.popen(cmd)
    output = stream.readlines()
    stream.close()
    for line in output:
        print line

def setupBin(binDir, srcBinDir):
    print 'Cleaning up the bin directory (if it exists)'
    shutil.rmtree(binDir, True)

    print 'Copying the bin directory'
    print '%s -> %s' % (srcBinDir, binDir)
    shutil.copytree(srcBinDir, binDir)

def unZip(filename, tempDir):
    if sys.version_info[0] < 3 and sys.version_info[1] < 7 and IS_LINUX:
        # Horrible that we have to do this on legacy Python installs
        exec_command('unzip %s -d %s' % (filename, tempDir))
    else:
        ucaZip = zipfile.ZipFile(filename, 'r')
        binDir = '%s/bin' % ROOT_DIR

        print 'Extracting the UCA into tempDir'
        ucaZip.extractall(tempDir)
        ucaZip.close()


# Start out by grabbing the latest UCA - NOTE we're pulling from staging here
try:
    url = 'http://%s/uca/uca.zip' % STAGING_IP
    print 'Pulling UCA zipefile: %s' % url
    (filename, headers) = urllib.urlretrieve(url)
    print 'Stored in "%s"...' % filename

    binDir = '%s/bin' % ROOT_DIR
    #print 'Making binDir "%s"...' % binDir
    #mkdir_p(binDir)
    tempDir = tempfile.mkdtemp()
    print 'Obtained a tempDir "%s"...' % tempDir

    unZip(filename, tempDir)

    srcBinDir = '%s/uca/bin' % tempDir

    if IS_LINUX:
        print 'Linux> Stopping previous client agent'
        exec_command('/etc/init.d/eil_steward.sh stop')
        setupBin(binDir, srcBinDir)
        print 'Linux> Installing dispatcher'
        exec_command('chmod a+x %s/uca/linux/dispatcher/install.sh' % tempDir)
        exec_command('cd %s/uca/linux/dispatcher; ./install.sh' % tempDir)
        # FIXME - Missing elevate scipt
        print 'Linux> Starting new client agent'
        exec_command('chmod a+x %s/eil_steward.py' % binDir)
        exec_command('chmod a+x %s/elevate_script' % binDir)
        exec_command('/etc/init.d/eil_steward.sh start')
    else:
        os.chdir('C:/EIL/bin')
        print "Windows> Stopping and removing previous services"
        exec_command('net stop EILTAFService')
        exec_command('sc delete EILTAFService')
        exec_command('sc delete EILAutoUpdateService')
        setupBin(binDir, srcBinDir)
        print "Windows> Installing new service"
        exec_command('python C:\\EIL\\bin\\eil_steward.py --username localsystem --startup auto install')
        exec_command('sc failure EILClientAgent reset= 30 actions= restart/5000')
        exec_command('sc start EILClientAgent')
        exec_command('sc queryex EILClientAgent')

    # FIXME clean-up tempDir

    # FIXME - Do we need to clean-up ucaZip?
except Exception as e:
    print "Error trying to bootstrap the unified agent\n\n"
    print e

# vim:set ai et sts=4 sw=4 tw=80:
