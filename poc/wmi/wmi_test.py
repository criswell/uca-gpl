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
