'''
asset.py
-------
Base-class defining the EIL assets
'''

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
                'Common' : {
                    'ClientAgentVersion' : None,            # String
                    'HostName' : None,                      # String
                    'UUID' : None,                          # String
                    'DomainName' : None,                    # String
                    'JoinedToDomain' : None,                # Boolean

                    'OS' : None,                            # String
                    'OSVersion' : None,                     # String
                    'OSServicePack' : None,                 # String
                    'OSArchitecture' : None,                # String
                    'BiosVersion' : None,                   # String
                    'VirtualMachine' : None,                # Boolean
                    'MachineType' : None,                   # String

                    'Motherboard' : {
                        'Manufacturer' : None,              # String
                        'Model' : None,                     # String
                        'SerialNumber' : None,              # String
                    },

                    'Processor' : {
                        'CpuCount' : None,                  # Integer
                        'CpuModel' : None,                  # String
                        'CoresPerCpu' : None,               # Integer
                        'Turbo' : None,                     # Boolean
                        'HyperThreading' : None,            # Boolean
                        'Vt' : None,                        # Boolean
                        'VtD' : None,                       # Boolean
                        'EIST' : None,                      # Boolean
                        'SRIOV' : None,                     # Boolean
                    },

                    'Memory' : {
                        'RamTotal' : None,                  # String

                        'DimmSlots' : None,                 # Integer
                        'DimmPopulated' : None,             # Integer
                        'Dimm' : { None },                  # Array of dim sizes
                    },

                    'Storage' : [                      # Array of the following
                        'HardDrive' : {
                            'Name' : None,                  # String
                            'Capacity' : None,              # String
                            'FreeSpace' : None,             # String
                        },
                        # Other elements as needed
                    ],

                    'Network' : [                      # Array of the following
                        'Interface' : {
                            'Name' : None,                  # String
                            'Mac' : None,                   # String
                            'IP4Address' : None,            # String
                            'IP6Address' : None,            # String
                            'Type' : None,                  # String
                        },
                        # Other elements as needed
                    ],
                } ,

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
                    'AMTConfigurationMode' : None,
                    'AMTConfigurationState' : None,
                    'AMTControlMode': None,
                    'AMTState' : None,
                    'AMTversion' : None,
                    'CertificateHashes' : None,
                    'IsAMTConfigured' : None,               # Boolean
                    'UUID' : None,
                }
                'OtherTechnology' : {
                }
            }

        # Example showing how to set elements above
        self.asset['Common']['ClientAgentVersion'] = ClientAgentState.VERSION
        self.initialize()

    def getAssetXML(self, hostName):
        '''
        Given the hostname of the current system, will process and return an
        updated asset update XML.

        @param hostName The hostname of the system.

        @returns A string containing the XML
        '''

        self.asset['Common']['HostName'] = hostName

        # Call the local platform's implementation of the asset update
        self.updateAsset()

        # FIXME - Need to parse this stuff using xml.etree and return a string
        raise exceptions.NotImplementedError()

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
