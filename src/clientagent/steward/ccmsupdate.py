'''
ccmsupdate.py
-------------
Main atomic operator class for the CCMS updates.
'''

import logging, time

from clientagent.steward.atom import Atom
from clientagent.common.utility import mkdir_p
from clientagent.common.utility import getIfInfo
from clientagent import get_config

# SUDs
from suds.client import Client
from suds.sax.element import Element
from suds.sax.attribute import Attribute

class CCMS_Update(Atom):
    '''
    This is the main CCMS interaction interface. This manages the core
    interactions with CCMS, and interacts with the dispatcher to re-route
    commands to platform-specific implimentations.
    '''
    def __init__(self):
        self.config = get_config()

        self.logger = logging.getLogger()
        self.logger.info("CCMS Update atom startup");
        self.CCMS_WSDL = 'http://%s/CCMS/EILClientOperationsService.svc?wsdl' %
                self.stdin = self.config.C.get('main', 'CCMS')

        (self.MY_HWADDR, self.MY_HOST) = (None, None)
        try:
            (self.MY_HWADDR, self.MY_HOST) = getIfInfo()
        except RuntimeError:
            # Well, this is unfortunate, we cannot run. Log an error and bail
            self.logger.critical('RuntimeError during attempt to find network interface hardware address!')
            self.logger.critical('Bailing on CCMS operations!')
        except:
            self.logger.critical('Could not obtain network interface hardware address for some unknown reason')
            self.logger.critical('Bailing on CCMS operations!')

        if not self.MY_HOST and not self.MY_HWADDR:
            self.ACTIVE = False
        else:
            self.ACTIVE = True


    def update(self, timeDelta):
        pass

# vim:set ai et sts=4 sw=4 tw=80:
