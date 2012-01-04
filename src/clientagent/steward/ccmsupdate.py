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
from clientagent.dispatcher import Dispatcher
from clientagent.steward.commandhandler import handleReboot
from clientagent.steward.commandhandler import handleJoin

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
        self.dispatcher = Dispatcher()
        self.config = get_config()
        self.FIRST_PASS = True
        self.TARGET_TIMEDELTA = 30
        self.MAX_JOIN_RETRIES = 2

        self.logger = logging.getLogger('clientagent.steward.ccmsupdate')
        self.logger.info("CCMS Update atom startup");
        self.CCMS_IP = self.config.C.get('main', 'CCMS')
        self.CCMS_WSDL = 'http://%s/CCMS/EILClientOperationsService.svc?wsdl' % self.CCMS_IP

        (self.MY_HWADDR, self.MY_HOST) = (None, None)
        try:
            self.logger.debug('Obtaining HWADDR and HOSTNAME')
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
            self.logger.debug('Creating SUDS SOAP client...')
            # FIXME - We're still not caching the WSDL, before production, we
            # really need to address this!
            headers = {'Content-Type': 'application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/GetCommandToExecute"'}
            ACKheaders = {'Content-Type': 'application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/UpdateCommandStatus"'}
            try:
                self.client = Client(self.CCMS_WSDL, headers=headers)
                self.ACKclient = Client(self.CCMS_WSDL, headers=ACKheaders)
            except:
                # FIXME we will need better error checking here, but for now,
                # we use a catch-all
                self.logger.critical('Unknown error trying to contact CCMS!')
                self.logger.critical('Bailing on CCMS operations!')
                self.ACTIVE = False

    def newMessageID(self):
        '''
        Obtains a new message ID from random sources
        '''
        source_string = '0123456789ABCDEFGHIJKLMNOPQRSTWXYZ'
        message_id = 'urn:uuid:'
        # Divide into seven stanzas
        for s in range(7):
            # and have five chars per stanza
            for c in range(5):
                message_id += source_string[random.randint(0,len(source_string)-1)]
            if s < 6:
                # Append a dash if not at end
                message_id += "-"
        return message_id

    def setHeaders(self, client, messageID):
        '''
        Sets the headers for the next exchange. Should be called every time we start
        a new exchange
        '''
        wsa_ns = ('wsa', 'http://www.w3.org/2005/08/addressing')
        mustAttribute = Attribute('SOAP-ENV:mustUnderstand', 'true')
        messageID_header = Element('MessageID', ns=wsa_ns).setText(messageID)
        replyTo_address = Element('Address',
            ns=wsa_ns).setText('http://www.w3.org/2005/08/addressing/anonymous')
        replyTo_header = Element('ReplyTo', ns=wsa_ns).insert(replyTo_address)
        replyTo_header.append(mustAttribute)
        # FIXME hard-coded
        to_header = Element('To',
            ns=wsa_ns).setText('http://%s/CCMS/EILClientOperationsService.svc' % self.CCMS_IP)
        to_header.append(mustAttribute)
        action_header = Element('Action',
            ns=wsa_ns).setText('http://tempuri.org/IEILClientOperations/GetCommandToExecute')
        action_header.append(mustAttribute)
        master_header_list = [
            messageID_header,
            replyTo_header,
            to_header,
            action_header
        ]
        client.set_options(soapheaders=master_header_list)
        return client

    def setStatusUpdateHeaders(self, ACKclient, messageID):
        '''
        Sets the headers for the handshake ACK exchange. Should be called every time we finish
        an exchange
        '''
        wsa_ns = ('wsa', 'http://www.w3.org/2005/08/addressing')
        mustAttribute = Attribute('SOAP-ENV:mustUnderstand', 'true')
        # FIXME - this shouldn't be a new ID!
        messageID_header = Element('MessageID', ns=wsa_ns).setText(messageID)
        replyTo_address = Element('Address',
            ns=wsa_ns).setText('http://www.w3.org/2005/08/addressing/anonymous')
        replyTo_header = Element('ReplyTo', ns=wsa_ns).insert(replyTo_address)
        replyTo_header.append(mustAttribute)
        # FIXME hard-coded
        to_header = Element('To',
            ns=wsa_ns).setText('http://%s/CCMS/EILClientOperationsService.svc' % self.CCMS_IP)
        to_header.append(mustAttribute)
        action_header = Element('Action',
            ns=wsa_ns).setText('http://tempuri.org/IEILClientOperations/UpdateCommandStatus')
        action_header.append(mustAttribute)
        master_header_list = [
            messageID_header,
            replyTo_header,
            to_header,
            action_header
        ]
        ACKclient.set_options(soapheaders=master_header_list)
        return ACKclient

    def generateContext(self, client, MY_HOST, MY_HWADDR):
        '''
        Generate our command request, this is rather hackish, and lifted almost
        verbatim from the Linux client agent code. If this becomes the norm, we
        should rewrite this more pythonically.
        '''
        ctx = client.factory.create('ns0:MachineContext')
        mParams = client.factory.create('ns2:ArrayOfKeyValueOfstringstring')
        order_num = client.factory.create('ns2:KeyValueOfstringstring')
        order_num.Key = 'ORDER_NUM'
        order_num.Value = '1'
        hwaddr = client.factory.create('ns2:KeyValueOfstringstring')
        hwaddr.Key = 'MAC_ADDR'
        hwaddr.Value = MY_HWADDR
        host = client.factory.create('ns2:KeyValueOfstringstring')
        host.Key = 'HOST_NAME'
        host.Value = MY_HOST
        mParams.KeyValueOfstringstring.append(order_num)
        mParams.KeyValueOfstringstring.append(hwaddr)
        mParams.KeyValueOfstringstring.append(host)
        ctx.mParams = mParams
        mType = client.factory.create('ns0:MachineType')
        ctx.mType = mType.HOST
        return ctx

    def generateAckCommand(self, client, commandName, commandStatus, commandSuccess, commandResult, errorCode, operationID, machineType):
        '''
        Generates an acknowledgement command.

        @param client The SUDs client in use
        @param commandName The command name which we are acknowledging
        @param commandStatus The status of the command
        @param commandSuccess Whether the command was successful or not
        @param commandResult The result of the command
        @param errorCode Any error code associated with this ACK
        @param operationID The Operation ID for the transaction
        @param machineType The machine type of the host machine
        '''
        ack = client.factory.create('ns0:EILCommand')
        ack.CommandName = commandName
        ack.CommandStatus = commandStatus
        ack.CommandResult = commandResult
        ack.CommandSuccessful = commandSuccess
        ack.ErrorCode = errorCode
        ack.OperationID = operationID
        ack.SetMachineType = machineType

        return ack

    def shutdown(self):
        pass

    def update(self, timeDelta):
        if timeDelta >= self.TARGET_TIMEDELTA:
            txID = self.newMessageID()
            self.client = self.setHeaders(self.client, txID)
            ctx = self.generateContext(client, self.MY_HOST, self.MY_HWADDR)

            try:
                self.logger.info('Checking for command from CCMS')
                # FIXME - How do we handle situations where there is no
                # hostname set? See TODO
                result = self.client.service.GetCommandToExecute(ctx)
                self.logger.debug('CCMS Result:')
                self.logger.debug(result)

                commandName = None

                if 'lower' in dir(result.CommandName):
                    commandName = result.CommandName.lower()

                if commandName == None:
                    self.logger.info('No CCMS command found to execute')
                elif commandName == 'reboot':
                    handleReboot(self, dispatcher, result)
                elif commandName == 'join domain':
                    handleJoin(self, result)
                else:
                    # FIXME TODO
                    pass
            except:
                self.logger.info('VLAN switch, running TCP diagnostics to pump interface')
                self.dispatcher.tcpDiag()

# vim:set ai et sts=4 sw=4 tw=80:
