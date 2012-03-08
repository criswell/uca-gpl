'''
asset.py
-------
Base-class defining the EIL assets
'''

import exceptions
import xml.etree.ElementTree as ET
from clientagent.common.ordereddict import OrderedDict as OD
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
        self.asset = OD([
                ('Common' , OD([
                    ('ClientAgentVersion' , None),            # String
                    ('HostName' , None),                      # String
                    ('UUID' , None),                          # String
                    ('DomainName' , None),                    # String
                    ('JoinedToDomain' , None),                # Boolean

                    ('OS' , None),                            # String
                    ('OSVersion' , None),                     # String
                    ('OSServicePack' , None),                 # String
                    ('OSArchitecture' , None),                # String
                    ('BiosVersion' , None),                   # String
                    ('VirtualMachine' , None),                # Boolean
                    ('MachineType' , None),                   # String

                    ('Motherboard' , OD([
                        ('Manufacturer' , None),              # String
                        ('Model' , None),                     # String
                        ('SerialNumber' , None),              # String
                    ])),

                    ('Processor' , OD([
                        ('CpuCount' , None),                  # Integer
                        ('CpuModel' , None),                  # String
                        ('CoresPerCpu' , None),               # Integer
                        ('Turbo' , None),                     # Boolean
                        ('HyperThreading' , None),            # Boolean
                        ('Vt' , None),                        # Boolean
                        ('VtD' , None),                       # Boolean
                        ('EIST' , None),                      # Boolean
                        ('SRIOV' , None),                     # Boolean
                    ])),

                    ('Memory' , OD([
                        ('RamTotal' , None),                  # String

                        ('DimmSlots' , None),                 # Integer
                        ('DimmPopulated' , None),             # Integer
                        ('Dimm' , [                     # Array of dim sizes
                            { 'DimSize' : None },
                            # Other elements as needed
                        ]),
                    ])),

                    ('Storage' , [                      # Array of the following
                        { 'HardDrive' : {
                            'Name' : None,                  # String
                            'Capacity' : None,              # String
                            'FreeSpace' : None,             # String
                            },
                        },
                            # Other elements as needed
                    ]),

                    ('Network' , [                      # Array of the following
                        { 'Interface' : {
                            'Name' : None,                  # String
                            'Mac' : None,                   # String
                            'IP4Address' : None,            # String
                            'IP6Address' : None,            # String
                            'Type' : None,                  # String
                            },
                        },
                        # Other elements as needed
                    ]),
                ])) ,

                ('NodeManager', OD([
                    ('Firmware' , OD([
                        ('BmcVersion' , None),
                        ('MeVersion' , None),
                        ('NmVersion' , None),
                        ('DcmiVersion' , None),
                    ])),
                    ('RemoteCapability' , OD([
                        ('BmcIpAddress' , None),
                        ('iLo' , None),
                        ('SerialOverLan' , None),
                    ])),
                ])) ,

                ('AMT' , OD([
                    ('AMTConfigurationMode' , None),
                    ('AMTConfigurationState' , None),
                    ('AMTControlMode', None),
                    ('AMTState', None),
                    ('AMTversion' , None),
                    ('CertificateHashes' , None),
                    ('IsAMTConfigured' , None),               # Boolean
                    ('UUID' , None),
                ])),
                ('OtherTechnology' , None)
            ])

        # Hackish, horrible thing... someone should be fired for what I'm about
        # to do... But since we're not doing this correctly in Portal, I need
        # to take matters into my own hands...
        #self.order = [ 'Common', 'ClientAgentVersion', 'HostName',
        #    'UUID', 'DomainName', 'JoinedToDomain', 'OS', 'OSVersion',
        #    'OSServicePack', 'OSArchitecture', 'BiosVersion', 'VirtualMachine',
        #    'MachineType', 'Motherboard', 'Manufacturer', 'Model',
        #    'SerialNumber', 'Processor', 'CpuCount', 'CpuModel', 'CoresPerCpu',
        #    'Turbo', 'HyperThreading', 'Vt', 'VtD', 'EIST', 'SRIOV', 'Memory',
        #    'RamTotal', 'DimmSlots', 'DimmPopulated', 'Dimm', 'DimSize',
        #    'Storage', 'HardDrive', 'Name', 'Capacity', 'FreeSpace', 'Network',
        #    'Interface', 'Name', 'Mac', 'IP4Address', 'IP6Address', 'Type',
        #    'NodeManager', 'Firmware', 'BmcVersion', 'MeVersion', 'NmVersion',
        #    'DcmiVersion', 'RemoteCapability', 'BmcIpAddress', 'iLo',
        #    'SerialOverLan', 'AMT', 'AMTConfigurationMode',
        #    'AMTConfigurationState', 'AMTControlMode', 'AMTState',
        #    'AMTversion', 'CertificateHashes', 'IsAMTConfigured', 'UUID',
        #    'OtherTechnology' ]

        #self.asset = self._makeOrderFromChaos(tempasset)

        # Example showing how to set elements above
        self.asset['Common']['ClientAgentVersion'] = ClientAgentState.VERSION
        self.initialize()

    #def _makeOrderFromChaos(asset):
        '''
        Given an unordered asset collection, will return an ordered one based
        upon whatever is set in self.order.

        @param asset: The unordered asset collection.
        @returns: An ordered asset collection.
        '''
        

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
        self._parseSubElement(self.asset, root)

        # I hate myself for doing this...
        #for tag in self.topLevelPriorityTags:
        #    if self.asset.has_key(tag):
        #        parent = ET.SubElement(root, tag)
        #        self._parseSubElement(self.asset[tag], parent)

        #for key in self.asset.keys():
        #    if key not in self.topLevelPriorityTags:
        #        self._parseSubElement(self.asset[key], root)

        return ET.tostring(root)

    def _parseSubElement(self, obj, parent):
        '''
        Iterative, internal method for parsing sub-elements and converting
        them to an ElementTree entity.

        @param obj: The object (a dict, list, or general data type) to parse
        @param parent: the Parent ElementTree entity.
        '''
        print type(obj)
        if type(obj) == dict:
            print str(obj)
        if type(obj) == OD or type(obj) == dict:
            for element in obj:
                sub = ET.SubElement(parent, element)
                if type(obj[element]) == OD or type(obj) == dict or type(obj[element]) == list:
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
