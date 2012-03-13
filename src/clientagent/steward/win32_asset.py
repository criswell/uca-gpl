'''
win32_asset.py
--------------
Derived asset collection class specific to Windows.
'''

import exceptions
import logging
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import iterparse
from clientagent.steward.asset import EILAsset
from clientagent.common.utility import getIfInfo
from clientagent.common.ordereddict import OrderedDict as OD
import socket, struct, os, platform
import ctypes
from ctypes.util import find_library
from ctypes import Structure
from clientagent.common.utility import locateExecInPath


class Win32_Asset(EILAsset):
    '''
    The Windows-specific asset collection sub-class.
    '''

    def initialize(self):
        '''
        This will be called once, when the module is initialized. Put any
        code here that should be called at program start.
        '''
        ##raise exceptions.NotImplementedError()

    def updateAsset(self):
        '''
        This will be called whenever we need to update the asset information.
        Do your SCS Discovery scraping (and anything else that is needed) and
        populate the self.asset dictionary.

        E.g., let's say I was updating the "AMTState" sub-element in "AMT", I
        would do it thusly:
            self.asset['AMT']['AMTState'] = foo
        '''
        #raise exceptions.NotImplementedError()
        
        self.logger.info("WIn32_asset function updateAsset  being entered");
        '''
        This will be called whenever we need to update the asset information.
        Do your SCS Discovery scraping (and anything else that is needed) and
        populate the self.asset dictionary.

        E.g., let's say I was updating the "AMTState" sub-element in "AMT", I
        would do it thusly:
            self.asset['AMT']['AMTState'] = foo
        '''
        self.logger.info("WIn32_asset function starting getIFInfo function");
        (MY_HWADDR, MY_HOST) =   getIfInfo()
        CA_VERSION = "4.1.1.10 Ver 16.75"
        self.logger.info("WIn32_asset function done with getIFInfo function");
        
        ##MY_HOST = "DELL960-DESK14"           # test only code to see what Prod CCMS
        ##MY_HWADDR = "00-24-E8-3D-50-07"

        ##MY_HOST = "DELL960-DESK14"           # test only code to see what Prod CCMS
        ##MY_HWADDR = "00-24-E8-3D-50-07"


        ujresult = 0
        ujcmd = "c:\EIL\scripts\ScsDisco.bat "
        try:
            ujresult = 0                        ## this is test only
            ##                                  #  comment only for testing to save SCS 7 minute process time
            #ujresult = os.system(ujcmd)         ## this is real and should be uncommented
        finally:
            ujresult = 0

        self.logger.info("WIn32_asset function passed SCS gather info");
        ##                 ##       get the IP number   ##
        ipresult = 0
        ipcmd = "ipconfig > c:\EIL\Log\IPaddr.txt"
        try:
               ipresult = os.system(ipcmd)
        finally:
               ipresult = 0
        self.logger.info("WIn32_asset function starting IP parsing");
        ##IPstr = iterparse("c:\EIL\Log\IPaddr.txt", ['start','end'])
        f = open("c:\EIL\Log\IPaddr.txt")
        gotIP = False
        IPstr = f.readline()
        MyIPnbr = " "
        tip = IPstr[1:70]
        lin = 0
        ipit = "IP Address. . . . . . . . . "
        ipit4 = "IPv4 Address. . . . . . . . ."
        while gotIP == False:
            lin = lin + 1
            if (ipit in tip) or (ipit4 in tip) :
                gotIP = True
                tip = IPstr[38:50]
                tip = tip.strip(' ') 
                tip = tip.rstrip('\r\n')
                tip = tip.strip(' ') 
                MyIPnbr = tip
            else:
                gotIP = False
                IPstr = f.readline()
                tip = IPstr[1:70]
                if lin > 20:
                    gotIP = True
        self.logger.info("WIn32_asset function done with IP parsing");
        self.logger.info("WIn32_asset function starting SCS Disco info to EILAsset");
        ##                  ##       parse thru the SCS Discovery XML     ##
        ##                  ##       get fields to Update Asset Info      ##
    
        ##                   ******   This  what Client Agent used to update for Asset Info
        thisJoinedToDomain = False
        thisAMTVer = ""
        thisClientOSRunning =  " "
        thisUUID =  " "
        thisClientAgentVer =  " "
        thisAMTProvisionState =  ""
        thisBIOSVer =  0.00
        thisProvisionServer =  " "
        thisOSDomainName = " "
        thisISAMTSupported = "false"

        thisAMTConfigurationMode = " "
        thisAMTConfigurationState = " "
        thisAMTControlMode = " "
        thisAMTState = " "
        thisAMTversion = ""
        thisCertificateHashes = " "
        thisIsAMTConfigured = "false"
        #UUID

      
        sb = "  "
        if thisJoinedToDomain == True:
            thisJoined = "True"
        else:
            thisJoined = "False"
    
        ## Build the XML to pass to the CCMS UpdateAssetInformation method
        sb = "  "
        sb = "<Attributes>"
        iparse = iterparse("C:\EIL\LOG\ScsXML.txt", ['start','end'])
        ##sb = sb + "<Key>" + 'IPAddress' + "</Key>"
        ##sb = sb + "<Value>" + MyIPnbr + "</Value>"
        ##sb = sb + "<Key>" + 'ClientAgentVer' + "</Key>"
        ##sb = sb + "<Value>" + '4.1.1.10 Ver 16.75' + "</Value>"

        sb = sb + "<IPAddress>" + MyIPnbr + "</IPAddress>"
        sb = sb + "<ClientAgentVer>" + '4.1.1.10 Ver 16.75' + "</ClientAgentVer>"  

        for event, elem in iparse:
            
             if event == 'start':    
                if elem.tag == "AMTVer":
                   thisAMTVer = elem.text
                   thisAMTversion = elem.text
                if elem.tag == "AMTversion":
                   thisAMTVer = elem.text
                   thisAMTversion = elem.text
                if elem.tag == "OSDomainName":
                     thisOSDomainName = elem.text
                if thisOSDomainName.find(".com") == -1:
                       thisJoinedToDomain = False
                else:
                       thisJoinedToDomain = True         
                if elem.tag == "OperatingSystem":
                    thisClientOSRunning = elem.text
                if elem.tag == "UUID":
                    thisUUID = elem.text
                if elem.tag == "IsAMTSupported":
                    if elem.text != None:
                        thisIsAMTSupported = elem.text
                ##if elem.tag == "IsAMTSupported":
                ##    thisAMTProvisionState = " "
                ##    if elem.text != None:
                ##        thisIsAMTSupported = elem.text

                # thisAMTProvisionState = elem.text
                #   Newly added in MArch  
                if elem.tag == "AMTConfigurationMode":
                    if elem.text != None:
                        thisAMTConfigurationMode = elem.text

                if elem.tag == "AMTConfigurationState":
                    if elem.text != None:
                        thisAMTConfigurationState = elem.text

                if elem.tag == "AMTControlMode":
                    if elem.text != None:
                        thisAMTControlMode = elem.text

                if elem.tag == "AMTState":
                    if elem.text != None:
                        thisAMTState = elem.text
                        
                if elem.tag == "AMTVersion":
                    if elem.text != None:
                        thisAMTVersion = elem.text
                        
                if elem.tag == "CertificationHashes":
                    if elem.text != None:
                        thisCertificationHashes = elem.text
                    
                if elem.tag == "IsAMTConfigured":
                    if elem.text != None:
                        thisIsAMTConfigured = elem.text

                #    end of newly added AMT foe EILAsset
                if elem.tag == "BIOSVersion":
                    thisBIOSVer = elem.text
                if elem.tag == "IPAddress":
                    thisIPAddress = elem.text
                if elem.tag == "SerialNumber":
                    thisProvisionServer = elem.text


    

                ## Build the XML to pass to the CCMS UpdateAssetInformation method
                ##if event == "end": 
                ## and if elem.tag == "System_Discovery":
                ##    next
                ##if elem == tuple:
                ##    tuples = elem.split('),')
                ##    out = []
                ##    for x in tuples:
                ##     a,b = x.strip('()').split(', ')
                ##    out.append (str (a), str(b)) 
                ##     sb = sb + "<Key>" + out + "</Key>"
            ##else:
                if elem.text == None:
                     nothind = 0
                else:     
                    #if len(sb) > 2000:   ## Until Stored Proc is fixed limit key/value XML to less 2500 varchar
                    #    nothind = 0
                    #else:                ## as of 2/16/2010 SQL column type chgd from varchar to XML  - no more len limit       
                        sb = sb + "<" + elem.tag +  ">"  
                        sb = sb + elem.text                 
                        sb = sb + "</" + elem.tag +  ">"  
                    
                        #sb = sb + "<Key>" + elem.tag + "</Key>"     # 2/16/2012 this style commented about activated
                        #sb = sb + "<Value>" + elem.text + "</Value>"  
                         
      
        sb = sb + "<JoinedToDomain>" + thisJoined + "</JoinedToDomain>"
        sb = sb + "<HostName>" + MY_HOST + "</HostName>"
        sb = sb + "<AMTVer>" + thisAMTVer + "</AMTVer>"
        sb = sb + "<BIOSVer>" + thisBIOSVer + "</BIOSVer>"
        sb = sb + "<DomainName>" + thisOSDomainName + "</DomainName>"
        sb = sb + "<OSVer>" + thisClientOSRunning + "</OSVer>"
        sb = sb + "<ProvisionServer>" + thisProvisionServer + "</ProvisionServer>"
        sb = sb + "<UUID>" + thisUUID + "</UUID>"
        sb = sb + "<IPAddress>" + MyIPnbr + "</IPAddress>"
        ##sb = sb + "<ClientAgentVer>" + CA_VERSION + "</ClientAgentVer>"
        sb = sb + "<ClientAgentVer>" + '4.1.1.10 Ver 16.75' + "</ClientAgentVer>"
  
        sb = sb + "</Attributes>"

        sb = sb + "</Attributes>"


        ##self.ccmsupdate.AssetCCMS(self, sb)
        self.logger.info("Win32_asset SCS Disco info to EILAsset  parsing done ...RC-3-12");
        '''
        Called when we update the asset from getAssetXML
        '''
        self.asset['Common']['HostName'] = MY_HOST
        self.asset['Common']['UUID'] = thisUUID
        self.asset['Common']['DomainName'] = thisOSDomainName
        self.asset['Common']['JoinedToDomain'] = thisJoinedToDomain
        self.asset['Common']['ClientAgentVersionNumber'] = CA_VERSION


        #self.asset['Common']['OS'] = platform.system()
        self.asset['Common']['OSVersion'] = thisClientOSRunning
        #self.asset['Common']['OSArchitecture'] = ' '.join(platform.architecture())
        self.asset['Common']['OSKernel'] = platform.release()

        self.asset['Common']['OSKernel'] = platform.release()
        #self.asset['Common']['Network']['Interface'](int('0')[IP4Address] = MyIPnbr

        nic = ('Network' , [                     # Array of the following
               { 'Interface' : {
                 'Name' : None,                  # String
                 'Mac' : MY_HWADDR,              # String
                 'IP4Address' : MyIPnbr,         # String
                 'IP6Address' : None,            # String
                 'Type' : None,                  # String
                            },
                        },
                        # Other elements as needed
                  ])


        self.asset['Common']['Network'] = nic

        theAMT = OD([
                    ('AMTConfigurationMode' , thisAMTConfigurationMode),
                    ('AMTConfigurationState' , thisAMTConfigurationState),
                    ('AMTControlMode', thisAMTControlMode),
                    ('AMTState', thisAMTState),
                    ('AMTversion' , thisAMTversion),
                    ('CertificateHashes' , thisCertificateHashes),
                    ('IsAMTConfigured' , thisIsAMTConfigured),               # Boolean
                    ('UUID' , thisUUID),
                    ])
                    
        #print theAMT
        self.asset['Common']['AMT'] = theAMT
        self.logger.info("AMTConfigurationState :" +  thisAMTConfigurationState);
        self.logger.info("AMTConfigurationMode :" +  thisAMTConfigurationMode);
        self.logger.info("AMTversion: " + thisAMTversion);
        self.logger.info("AMTver: " + thisAMTVer);
    def endthis():
        thisen = ' '
# vim:set ai et sts=4 sw=4 tw=80: