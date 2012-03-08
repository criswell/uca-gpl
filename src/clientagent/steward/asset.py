'''
asset.py
-------
Base-class defining the EIL assets
'''

import exceptions
import xml.etree.ElementTree as ET
from clientagent import ClientAgentState

class EILAsset:
    '''
    This class defines what it means to be an EIL asset. It should contain all
    relevant information concerning a system in the lab.

    This class should not be used directly. Instead, it should be sub-classed
    based upon the platform in question and then that sub-class should fill in
    the fields as necessary.

    Note that many of these fields will be a "best effort" kind of thing, as
    some of them undoubtedly will be more difficult on one platform versus
    another.
    '''

    def __init__(self):
        self.asset = {
                'NodeManager': {
                    'Firmware' : {
                        'BmcVersion' : None,
                        'MeVersion' : None,
                        'NmVersion' : None,
                        'DcmiVersion' : None,
                    },
                    'RemoteCapability' : {
                        'BmcIpAddress' : None,
                        'iLo' : None,
                        'SerialOverLan' : None,
                    },
                } ,

                'AMT' : {
                    'UUID' : None,
                    'IsAMTConfigured' : None,               # Boolean
                    'CertificateHashes' : None,
                    'AMTversion' : None,
                    'AMTState' : None,
                    'AMTControlMode': None,
                    'AMTConfigurationState' : None,
                    'AMTConfigurationMode' : None,
                },

                'OtherTechnology' : None,

                'Common' : {
                    'Network' : [                      # Array of the following
                        { 'Interface' : {
                            'Type' : None,                  # String
                            'IP6Address' : None,            # String
                            'IP4Address' : None,            # String
                            'Mac' : None,                   # String
                            'Name' : None,                  # String
                            },
                        },
                        # Other elements as needed
                    ],

                    'Storage' : [                      # Array of the following
                        { 'HardDrive' : {
                            'Name' : None,                  # String
                            'Capacity' : None,              # String
                            'FreeSpace' : None,             # String
                            },
                        },
                        # Other elements as needed
                    ],

                    'Memory' : {
                        'DimmPopulated' : None,             # Integer
                        'DimmSlots' : None,                 # Integer

                        'RamTotal' : None,                  # String
                        'Dimm' : [                     # Array of dim sizes
                            { 'DimSize' : None },
                            # Other elements as needed
                        ],
                    },

                    'Processor' : {
                        'SRIOV' : None,                     # Boolean
                        'EIST' : None,                      # Boolean
                        'VtD' : None,                       # Boolean
                        'Vt' : None,                        # Boolean
                        'HyperThreading' : None,            # Boolean
                        'Turbo' : None,                     # Boolean
                        'CoresPerCpu' : None,               # Integer
                        'CpuModel' : None,                  # String
                        'CpuCount' : None,                  # Integer
                    },

                    'Motherboard' : {
                        'SerialNumber' : None,              # String
                        'Model' : None,                     # String
                        'Manufacturer' : None,              # String
                    },

                    'MachineType' : None,                   # String
                    'VirtualMachine' : None,                # Boolean
                    'BiosVersion' : None,                   # String
                    'OSArchitecture' : None,                # String
                    'OSServicePack' : None,                 # String
                    'OSVersion' : None,                     # String
                    'OS' : None,                            # String

                    'JoinedToDomain' : None,                # Boolean
                    'DomainName' : None,                    # String
                    'UUID' : None,                          # String
                    'HostName' : None,                      # String
                    'ClientAgentVersion' : None,            # String
                } ,

            }

        # Hackish, horrible thing... someone should be fired for what I'm about
        # to do... But since we're not doing this correctly in Portal, I need
        # to take matters into my own hands...
        self.topLevelPriorityTags = [ 'Common', ]

        # Example showing how to set elements above
        self.asset['Common']['ClientAgentVersion'] = ClientAgentState.VERSION
        self.initialize()

    def getAssetXML(self, hostName):
        '''
        Given the hostname of the current system, will process and return an
        updated asset update XML.

        @param hostName: The hostname of the system.

        @returns: A string containing the XML
        '''

        self.asset['Common']['HostName'] = hostName

        # Call the local platform's implementation of the asset update
        self.updateAsset()

        # Build up our XML structure from self.asset
        root = ET.Element('AssetUpdate')

        # I hate myself for doing this...
        for tag in self.topLevelPriorityTags:
            if self.asset.has_key(tag):
                parent = ET.SubElement(root, tag)
                self._parseSubElement(self.asset[tag], parent)

        for key in self.asset.keys():
            if key not in self.topLevelPriorityTags:
                self._parseSubElement(self.asset[key], root)

        return ET.tostring(root)

    def _parseSubElement(self, obj, parent):
        '''
        Iterative, internal method for parsing sub-elements and converting
        them to an ElementTree entity.

        @param obj: The object (a dict, list, or general data type) to parse
        @param parent: the Parent ElementTree entity.
        '''
        if type(obj) == dict:
            for element in obj:
                sub = ET.SubElement(parent, element)
                if type(obj[element]) == dict or type(obj[element]) == list:
                    self._parseSubElement(obj[element], sub)
                else:
                    if obj[element] != None:
                        sub.text = str(obj[element])
        elif type(obj) == list:
            # Okay, so if this thing isn't in the appropriate format, we will
            # REALLY break down here. But hopefully we can keep the data coming
            # in sane :-)
            for element in obj:
                self._parseSubElement(element, parent)
        else:
            if obj != None:
                parent.text = str(obj)

    def initialize(self):
        '''
        This is the method you override to actually initialize your local
        sub-class.
        '''
        raise exceptions.NotImplementedError()

    def updateAsset(self):
        '''
        This is the method you override to actually generate the asset
        '''
        raise exceptions.NotImplementedError()

# vim:set ai et sts=4 sw=4 tw=80:
