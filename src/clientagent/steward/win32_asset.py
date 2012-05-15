'''
win32_asset.py
--------------
Derived asset collection class specific to Windows.
'''

import exceptions
from clientagent.steward.asset import EILAsset
from clientagent.common.ordereddict import OrderedDict as OD
import os

WMI_ENABLED = True
try:
    from clientagent.wmi import WMI
except:
    WMI_ENABLED = False

class Win32_Asset(EILAsset):
    '''
    The Windows-specific asset collection sub-class.
    '''

    def initialize(self):
        '''
        This will be called once, when the module is initialized. Put any
        code here that should be called at program start.
        '''

        if WMI_ENABLED:
            self.logger.info('WMI Enabled for Windows Asset Update')
            self.__wmi = WMI()
        else:
            self.logger.critial('WMU disabled for Windows asset update!')

    def _hasResult(self, someObject):
        '''
        When called with a WMI result will return the last entry or None if
        no entries found. This should only be used when you're expecting
        exactly one WMI result.
        '''
        if len(someObject) > 0:
            return someObject[-1]
        else:
            return None

    def updateAsset(self):
        '''
        Called when we update the asset from getAssetXML
        '''

        # Put all non WMI items up here, so we can ensure something shows up

        if WMI_ENABLED:
            # General stuff
            NTDomain = self._hasResult(self.__wmi.Win32_NTDomain())
            XPOS = self._hasResult(self.__wmi.Win32_ComputerSystem())
            if NTDomain:
                self.asset['Common']['HostName'] = NTDomain.Caption
                self.asset['Common']['DomainName'] =  NTDomain.DomainName
                joinedToDomain = False
                if NTDomain.DomainName:
                    joinedToDomain = True
                self.asset['Common']['JoinedToDomain'] = joinedToDomain
                if XPOS:
                    self.asset['Common']['JoinedToDomain'] = XPOS.PartOfDomain

            productID = self._hasResult(self.__wmi.Win32_ComputerSystemProduct())
            if productID:
                self.asset['Common']['UUID'] = productID.UUID

            OS = self._hasResult(self.__wmi.Win32_OperatingSystem())
            if OS:
                self.asset['Common']['OS'] = OS.Caption
                self.asset['Common']['OSVersion'] = OS.Version
                mjv = OS.ServicePackMajorVersion
                mjm = OS.ServicePackMinorVersion
                self.asset['Common']['OSServicePack'] = "%s.%s" % (mjv, mjm)
                try:
                    self.asset['Common']['OSArchitecture'] = OS.OSArchitecture
                except:
                    if XPOS:
                        self.asset['Common']['OSArchitecture'] = XPOS.SystemType

                biosVersion = None
                BIOS = self._hasResult(self.__wmi.Win32_BIOS())
                if BIOS:
                    biosVersion = BIOS.Version
                self.asset['Common']['BiosVersion'] = biosVersion

                # Motherboard
                mobo = self._hasResult(self.__wmi.Win32_BaseBoard())
                if mobo:
                    manufacturer = mobo.Manufacturer
                    model = mobo.Model
                    serialNum = mobo.SerialNumber

                    moboOrd = OD([
                        ('Manufacturer' , manufacturer),
                        ('Model' , model),
                        ('SerialNumber' , serialNum),
                    ])

                    self.asset['Common']['Motherboard'] = moboOrd

                # Processor
                allProcs = self.__wmi.Win32_Processor()
                if len(allProcs) > 0:
                    cpuCount = len(allProcs)
                    cpuModel = allProcs[0].Name
                    coresPerCpu = allProcs[0].NumberOfCores

                    processor = OD([
                        ('CpuCount' , cpuCount),
                        ('CpuModel' , cpuModel),
                        ('CoresPerCpu' , coresPerCpu),
                        ('Turbo' , None),
                        ('HyperThreading' , None),
                        ('Vt' , None),
                        ('VtD' , None),
                        ('EIST' , None),
                        ('SRIOV' , None),
                    ])
                    self.asset['Common']['Processor'] = processor

                # Memory
                mem = self.__wmi.Win32_PhysicalMemory()
                if len(mem) > 0:
                    # Let's put this in M
                    ramTotal = 0
                    for m in mem:
                        ramTotal += int(mem[0].Capacity) / 1048576
                    dimmSlots = len(mem)

                    memory = OD([
                        ('RamTotal' , '%sMB' % ramTotal),
                        ('DimmSlots' , dimmSlots),
                    ])
                    self.asset['Common']['Memory'] = memory

                # Storage
                discs = self.__wmi.Win32_LogicalDisk()
                if len(discs) > 0:
                    storage = []

                    for drive in discs:
                        if drive.Size:
                            d = OD([
                                ( 'HardDrive', OD([
                                    ('Name', drive.Name),
                                    ('Capacity', '%sMB' % (int(drive.Size) / 1048576)),
                                    ('FreeSpace', '%sMB' % (int(drive.FreeSpace) / 1048576)),
                                ]),
                            ), ])

                            storage.append(d)

                    if len(storage) > 0:
                        self.asset['Common']['Storage'] = storage

                # Networking
                totalNICs = []
                allNet = self.__wmi.Win32_NetworkAdapter()
                allIPs = self.__wmi.Win32_NetworkAdapterConfiguration()
                nics = []
                ips = []
                equalNics = (len(allNet) == len(allIPs))

                for n in range(len(allNet)):
                    try:
                        if allNet[n].PhysicalAdapter:
                            nics.append(allNet[n])
                            if equalNics:
                                ips.append(allIPs[n])
                    except:
                        # On XP, this is a bit wonky
                        if allNet[n].Manufacturer != 'Microsoft':
                            nics.append(allNet[n])
                            if equalNics:
                                ips.append(allIPs[n])

                if len(nics) > 0:
                    for n in range(len(nics)):

                        nicName = nics[n].Name
                        nicMac = nics[n].MACAddress
                        try:
                            nicType = nics[n].AdapterType
                        except:
                            # XP is Wonky
                            pass
                        ip = None
                        if equalNics:
                            try:
                                ip = ips[n].IPAddress[0]
                            except:
                                ip = None

                        totalNICs.append(OD([
                            ( 'Interface', OD([
                                ('Name', nicName),
                                ('Mac', nicMac),
                                ('IP4Address', ip),
                                ('IP6Address', None),
                                ]))
                        ]))

                self.asset['Common']['Network'] = totalNICs

# vim:set ai et sts=4 sw=4 tw=80:
