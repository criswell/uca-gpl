#!/usr/bin/env python

CCMS_IP = '172.16.3.10'
CCMS_ADDR = 'eilauto01.eil-infra.com'
CCMS_WSDL = [
    'http://%s/CCMS/EILClientOperationsService.svc?wsdl',
    'http://%s/CCMS/EILClientOperationsService.svc?xsd=xsd0',
    'http://%s/CCMS/EILClientOperationsService.svc?xsd=xsd1',
    'http://%s/CCMS/EILClientOperationsService.svc?xsd=xsd2',
    'http://%s/CCMS/EILClientOperationsService.svc?xsd=xsd1',
    ]

# Google news is a meatier page
GOOGLE = 'http://news.google.com'

import logging, time, random, traceback, sys, subprocess

logger = logging.getLogger('timeout_test_wget')
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename='timeout_test_wget-%s.log' % time.ctime(),
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(logging.StreamHandler())

logger.info('This script will run until terminated or until we have a situation where CCMS cannot be reached...')

def try_address(address):
    exit_code = subprocess.call(['wget', '-q', '-O', '-', address])
    if exit_code == 1:
        logger.info('ERROR: 1   Generic error code.')
        raise Exception()
    elif exit_code == 2:
        logger.info('ERROR: 2   Parse error---for instance, when parsing command-line options, the .wgetrc or .netrc...')
        raise Exception()
    elif exit_code == 3:
        logger.info('ERROR: 3   File I/O error.')
        raise Exception()
    elif exit_code == 4:
        logger.info('ERROR: 4   Network failure.')
        raise Exception()
    elif exit_code == 5:
        logger.info('ERROR: 5   SSL verification failure.')
        raise Exception()
    elif exit_code == 6:
        logger.info('ERROR: 6   Username/password authentication failure.')
        raise Exception()
    elif exit_code == 7:
        logger.info('ERROR: 7   Protocol errors.')
        raise Exception()
    elif exit_code == 8:
        logger.info('ERROR: 8   Server issued an error response.')
        raise Exception()
    elif exit_code != 0:
        logger.info('ERROR: Some unknown error number %s' % exit_code)
        raise Exception()
    else:
        logger.info('Success!')

while True:
    for index in range(len(CCMS_WSDL)):
        address = CCMS_WSDL[index] % CCMS_ADDR
        logger.info('Using %s, %s' % (index, address))
        try:
            try_address(address)
        except:
            logger.info('Failure on address, trying IP...')
            try:
                address = CCMS_WSDL[index] % CCMS_IP
                logger.info('Using %s, %s' % (index, address))
                try_address(address)
                logger.info('Success on IP, trying Google News!!!!!!!!!!!!!!!')
                address = GOOGLE
                logger.info('Using %s, %s' % (index, address))
                try_address(address)
            except:
                logger.info('Failure on IP, trying Google News..')
                try:
                    address = GOOGLE
                    logger.info('Using %s, %s' % (index, address))
                    try_address(address)
                    logger.info('SUCCESS ON Google News!!!!!!')
                    sys.exit(0)
                except:
                    logger.info('Failre on Google News (unless we said there was success previously')
                    sys.exit(0)
