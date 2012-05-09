#!/usr/bin/env python

import wmi

c = wmi.WMI()

def hasResult(someObject):
    if len(someObject) > 0:
        return someObject[-1]
    else:
        return None

# General common stuff
NTDomain = hasResult(c.Win32_NTDomain())
if NTDomain:
    hostname = NTDomain.Caption
    domain = NTDomain.DomainName
    joinedToDomain = False
    if domain:
        joinedToDomain = True

    print "hostname : %s" % hostname
    print "domain : %s " % domain
    print "joinedToDomain: %s" % joinedToDomain

productID = hasResult(c.Win32_ComputerSystemProduct())
if productID:
    print "UUID : %s" % productID.UUID

OS = hasResult(c.Win32_OperatingSystem())
if OS:
    osName = OS.Caption
    osVersion = OS.Version
    mjv = OS.ServicePackMajorVersion
    mjm = OS.ServicePackMinorVersion
    osServicePack = "%s.%s" % (mjv, mjm)
    osArch = OS.OSArchitecture

    BIOS = hasResult(c.Win32_BIOS())
    if BIOS:
        biosVersion = BIOS.Version
    else:
        biosVersion = None

    print "OS : %s" % osName
    print "OSVersion : %s" % osVersion
    print "OSServicePack : %s" % osServicePack
    print "OSArchitecture : %s" % osArch
    print "BiosVersion : %s" % biosVersion

# Motherboard
mobo = hasResult(c.Win32_BaseBoard())
if mobo:
    manufacturer = mobo.Manufacturer
    model = mobo.Model
    serialNum = mobo.SerialNumber

    print "Motherboard"
    print "\t Manufacturer: %s" % manufacturer
    print "\t Model: %s" % model
    print "\t SerialNumber: %s" % serialNum

# Processor
allProcs = c.Win32_Processor()
if len(allProcs) > 0:
    cpuCount = len(allProcs)
    cpuModel = allProcs[0].Caption
    coresPerCpu = allProcs[0].NumberOfCores

    print "Processor"
    print "\t CpuCount : %s" % cpuCount
    print "\t CpuModel : %s" % cpuModel
    print "\t CoresPerCpu : %s" % coresPerCpu

# Memory
mem = c.Win32_PhysicalMemory()
if len(mem) > 0:
    # Let's put this in M
    ramTotal = int(mem[0].Capacity) / 1048576 # * 0.000001
    dimmSlots = len(mem)

    print "Memory"
    print "\t RamTotal: %sM" % ramTotal
    print "\t DimmSlots: %s" % dimmSlots

# Storage

# Networking
allNet = c.Win32_NetworkAdapter()
allIPs = c.Win32_NetworkAdapterConfiguration()
nics = []
ips = []
equalNics = (len(allNet) == len(allIPs))

for n in range(len(allNet)):
    if allNet[n].PhysicalAdapter:
        nics.append(allNet[n])
        if equalNics:
            ips.append(allIPs[n])

if len(nics) > 0:
    print "Network"
    for n in range(len(nics)):
        print "\t Interface-"

        nicName = nics[n].Name
        nicMac = nics[n].MACAddress
        nicType = nics[n].AdapterType
        ip = None
        if equalNics:
            ip = string(ips[n].IPAddress)

        print "\t\t Name: %s" % nicName
        print "\t\t Mac: %s" % nicMac
        print "\t\t IP4: %s" % ip
        print "\t\t Type: %s" % nicType
