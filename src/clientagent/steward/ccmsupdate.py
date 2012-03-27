'''
ccmsupdate.py
-------------
Main atomic operator class for the CCMS updates.
'''

import logging, time, random
import sys, traceback, urllib2

from clientagent.steward.atom import Atom
from clientagent.common.utility import mkdir_p
from clientagent.common.utility import getIfInfo
from clientagent import get_config
from clientagent.dispatcher import Dispatcher
from clientagent.steward.commandhandler import handleReboot
from clientagent.steward.commandhandler import handleJoin
from clientagent.steward.commandhandler import handleUnJoin

# SUDs
from suds.client import Client
from suds.sax.element import Element
from suds.sax.attribute import Attribute
from suds import WebFault

from clientagent.common.platform_id import PlatformID
platformId = PlatformID()
if platformId.IS_WINDOWS:
    from clientagent.steward.win32_asset import Win32_Asset as EILAsset
else:
    # Linux
    from clientagent.steward.linux_asset import Linux_Asset as EILAsset

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
        self.SUDS_ONLINE = False
        self.RETRY = 0
        self.MAX_RETRIES = 10
        self.MIN_DELAY = 5
        self.MAX_DELAY = 30
        self.TARGET_TIMEDELTA = 30
        self.ASSET_TIMEDELTA = 60 * 60 # 60 seconds X 60 minutes
        self.assetTimer = self.ASSET_TIMEDELTA + 1 # Force a first time update
        self.MAX_JOIN_RETRIES = 2

        # Our various CCMS command interactions
        self.CCMS_COMMANDS = {
            "UPDATE_ASSET" :'http://tempuri.org/IEILClientOperations/UpdateAssetInformation',
            "GET_COMMAND" : 'http://tempuri.org/IEILClientOperations/GetCommandToExecute',
            }

        self.logger = logging.getLogger('clientagent.steward.ccmsupdate')
        self.logger.info("CCMS Update atom startup");
        self.CCMS_IP = self.config.C.get('main', 'CCMS')
        self.CCMS_WSDL = 'http://%s/CCMS/EILClientOperationsService.svc?wsdl' % self.CCMS_IP

        (self.MY_HWADDR, self.MY_HOST) = (None, None)
        try:
            self.logger.info('Obtaining HWADDR and HOSTNAME')
            (self.MY_HWADDR, self.MY_HOST) = getIfInfo()
            self.logger.info('HWADDR: %s' % self.MY_HWADDR)
            self.logger.info('HOSTNAME: %s' % self.MY_HOST)
        except RuntimeError:
            # Well, this is unfortunate, we cannot run. Log an error and bail
            self.logger.critical('RuntimeError during attempt to find network interface hardware address!')
            self.logger.critical('Bailing on CCMS operations!')
        except:
            self.logger.critical('Could not obtain network interface hardware address for some unknown reason')
            self.logger.critical('Bailing on CCMS operations!')

        if not self.MY_HOST and not self.MY_HWADDR:
            self.ACTIVE = False
            self.logger.critical('Error obtaining HWADDR and HOSTNAME!')
            self.logger.critical('Setting CCMS_Update atom inactive..')
        else:
            self.getSuds()

    def getSuds(self):
        '''
        Attempts to get a new suds client
        '''
        self.ACTIVE = True
        self.logger.info('Creating SUDS SOAP client...')
        # FIXME - We're still not caching the WSDL, before production, we
        # really need to address this!
        headers = {'Content-Type': 'application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/GetCommandToExecute"'}
        ACKheaders = {'Content-Type': 'application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/UpdateCommandStatus"'}
        assetHeaders = {'Content-Type': 'application/soap+xml; charset=utf-8; action="http://tempuri.org/IEILClientOperations/UpdateAssetInformation"'}
        try:
            self.client = Client(self.CCMS_WSDL, headers=headers)
            self.ACKclient = Client(self.CCMS_WSDL, headers=ACKheaders)
            self.assetClient = Client(self.CCMS_WSDL, headers=assetHeaders)
            self.SUDS_ONLINE = True
        except:
            traceback_lines = traceback.format_exc().splitlines()
            for line in traceback_lines:
                self.logger.critical(line)
                # FIXME we will need better error checking here, but for now,
                # we use a catch-all
            self.SUDS_ONLINE = False
            self.RETRY += 1
            if self.RETRY > self.MAX_RETRIES:
                self.logger.critical('Unknown error trying to contact CCMS!')
                self.logger.critical('Bailing on CCMS operations!')
                self.ACTIVE = False
            else:
                self.logger.critical('Error connecting CCMS, assuming we have a concurrency problem')
                self.logger.critical('Current retry attempts: %s/%s' % (self.RETRY, self.MAX_RETRIES))
                delay = random.randint(self.MIN_DELAY, self.MAX_DELAY)
                self.logger.critical('Waiting for "%s" seconds to solve for potential concurrency problem...')
                time.sleep(delay)

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

    def setHeaders(self, client, messageID, action=None):
        '''
        Sets the headers for the next exchange. Should be called every time we start
        a new exchange

        @param client: The client instance to use
        @param messageID: The UUID to use in this interaction
        @param action: One of self.CCMS_COMMANDS keys defining the type of
            interaction. If action is None, it will default to GET_COMMAND.

        @returns: The updated client
        '''
        CCMSaction = None
        if not action or action not in self.CCMS_COMMANDS.keys():
            CCMSaction = self.CCMS_COMMANDS['GET_COMMAND']
        else:
            CCMSaction = self.CCMS_COMMANDS[action]
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
        action_header = Element('Action', ns=wsa_ns).setText(CCMSaction)
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

    def generateCommand(self, client, commandName, commandStatus, commandSuccess, commandResult, errorCode, operationID, machineType):
        '''
        Generates an EILCommand according to parameters.

        @param client The SUDs client in use
        @param commandName The command name which we are acknowledging
        @param commandStatus The status of the command
        @param commandSuccess Whether the command was successful or not
        @param commandResult The result of the command
        @param errorCode Any error code associated
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
        if self.SUDS_ONLINE:
            self.assetTimer += timeDelta
            self.logger.debug('asset Timer: %s - timeDelta %s' % (self.assetTimer, self.ASSET_TIMEDELTA))
            if self.assetTimer >= self.ASSET_TIMEDELTA:
                self.assetTimer = 0
                txID = self.newMessageID()
                self.assetClient = self.setHeaders(self.assetClient, txID, 'UPDATE_ASSET')
                ctx = self.generateContext(self.assetClient, self.MY_HOST, self.MY_HWADDR)

                try:
                    self.logger.info('Sending updated asset information to CCMS')
                    asset = EILAsset()
                    assetXML = asset.getAssetXML(self.MY_HOST)
                    self.logger.debug('Asset XML was:')
                    self.logger.debug(assetXML)
                    result = self.assetClient.service.UpdateAssetInformation(self.MY_HOST, self.MY_HWADDR, assetXML)
                    if result or result == None:
                        # Yeah, this is confusing due to how SUDS interprets
                        # results from CCMS
                        self.logger.info('CCMS updated with asset information')
                    else:
                        self.logger.info('CCMS reported error when asset information was sent')
                except WebFault as e:
                    traceback_lines = traceback.format_exc().splitlines()
                    for line in traceback_lines:
                        self.logger.critical(line)
                    self.logger.critical(str(e))
                except:
                    # TODO this will be the catch-all once we've identified the ones
                    # we want to handle
                    #exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback_lines = traceback.format_exc().splitlines()
                    for line in traceback_lines:
                        self.logger.critical(line)

            if timeDelta >= self.TARGET_TIMEDELTA:
                txID = self.newMessageID()
                self.client = self.setHeaders(self.client, txID)
                ctx = self.generateContext(self.client, self.MY_HOST, self.MY_HWADDR)

                try:
                    self.logger.info('Checking for command from CCMS')
                    # FIXME - How do we handle situations where there is no
                    # hostname set? See TODO
                    result = self.client.service.GetCommandToExecute(ctx)
                    self.logger.debug('CCMS Result:')
                    self.logger.debug(result)

                    commandName = None
                    if result == None:
                        self.logger.info('No CCMS command found to execute')
                    else:
                        if 'lower' in dir(result.CommandName):
                            commandName = result.CommandName.lower()

                        if commandName == None:
                            self.logger.info('CCMS Command was "None"')
                        elif commandName == 'reboot':
                            self.logger.info('CCMS Command "reboot"')
                            handleReboot(self, ctx, result, txID)
                        elif commandName == 'join domain':
                            self.logger.info('CCMS Command "join domain"')
                            handleJoin(self, ctx, result, txID)
                        elif commandName == 'unjoin domain':
                            self.logger.info('CCMS Command "unjoin domain"')
                            handleUnJoin(self, ctx, result, txID)
                        else:
                            # FIXME TODO
                            self.logger.critical('CCMS Command unhandled! "%s"', commandName)
                            pass
                except urllib2.URLError as e:
                    traceback_lines = traceback.format_exc().splitlines()
                    for line in traceback_lines:
                        self.logger.critical(line)
                    self.logger.info('VLAN switch, running TCP diagnostics to pump interface')
                    self.dispatcher.tcpDiag()
                except:
                    # TODO this will be the catch-all once we've identified the ones
                    # we want to handle
                    #exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback_lines = traceback.format_exc().splitlines()
                    for line in traceback_lines:
                        self.logger.critical(line)
        else:
            self.getSuds()

# vim:set ai et sts=4 sw=4 tw=80:
