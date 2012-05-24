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

import logging, urllib2, time, random, traceback, sys

logger = logging.getLogger('timeout_test')
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename='timeout_test.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(logging.StreamHandler())

logger.info('This script will run until terminated or until we have a situation where CCMS cannot be reached...')

while True:
    for index in range(len(CCMS_WSDL)):
        address = CCMS_WSDL[index] % CCMS_ADDR
        logger.info('Using %s, %s' % (index, address))
        try:
            f = urllib2.urlopen(address)
            throwaway = f.readlines()
            f.close()
            logger.info('Success, read %s lines' % len(throwaway))
            #logger.info(throwaway)
        except:
            traceback_lines = traceback.format_exc().splitlines()
            for line in traceback_lines:
                logger.info(line)
            logger.info('GOT AN ERROR READING THAT WSDL!')
            address = CCMS_WSDL[index] % CCMS_IP
            logger.info('Trying to read by IP: %s' % address)
            try:
                f = urllib2.urlopen(address)
                throwaway = f.readlines()
                f.close()
                logger.info('Success, read %s lines' % len(throwaway))
                logger.info('Success reading by IP!!!!!!!!!!!!!!!!!!!')
            except:
                traceback_lines = traceback.format_exc().splitlines()
                for line in traceback_lines:
                    logger.info(line)
                logger.info('Failure reading by IP! Trying Google News..')
            address = GOOGLE
            try:
                f = urllib2.urlopen(address)
                throwaway = f.readlines()
                f.close()
                logger.info('Success, read %s lines' % len(throwaway))
                logger.info('Success reading Google News!!!!!!!!!!!!!!!')
                sys.exit(0)
            except:
                traceback_lines = traceback.format_exc().splitlines()
                for line in traceback_lines:
                    logger.info(line)
                logger.info('Failure reading Google News...')
                sys.exit(0)
            sys.exit(0)
    timeout = random.randint(2, 15)
    logger.info('Sleeping %s' % timeout)
    time.sleep(timeout)
