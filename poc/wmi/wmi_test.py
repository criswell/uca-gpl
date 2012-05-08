#!/usr/bin/env python

import wmi

c = wmi.WMI()

# General common stuff
NTDomain = c.Win32_NTDomain()[-1]
hostname = NTDomain.Caption
domain = NTDomain.DomainName

