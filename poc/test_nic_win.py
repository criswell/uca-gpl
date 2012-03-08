#!/usr/bin/env python

import win32api
import win32security
from ntsecuritycon import *
from netbios import *
from socket import gethostname

def getInfo(ifnum, wireless=False):
    ncb = NCB()
    ncb.Command = NCBENUM
    la_enum = LANA_ENUM()
    ncb.Buffer = la_enum
    rc = Netbios(ncb)
    if rc != 0: raise RuntimeError, "Unexpected result %d" % (rc,)
    # Grab the first one
    ncb.Reset()
    ncb.Command = NCBRESET
    ncb.Lana_num = ord(la_enum.lana[ifnum])
    rc = Netbios(ncb)
    if rc != 0: raise RuntimeError, "Unexpected result %d" % (rc,)
    ncb.Reset()
    ncb.Command = NCBASTAT
    ncb.Lana_num = ord(la_enum.lana[ifnum])
    ncb.Callname = "*               "
    adapter = ADAPTER_STATUS()
    ncb.Buffer = adapter
    Netbios(ncb)
    hwaddr = ''.join(['%02x:' % ord(char) for char in adapter.adapter_address])[:-1]


    return (hwaddr, ipaddr)

print "Wired\n---------------"

for i in range(0, 9):
    try:
        (a, b) = getInfo(i)
        print "\teth%s : %s - %s" % (i, a, b)
    except:
        break

print "Wireless\n---------------"

for i in range(0, 9):
    try:
        (a, b) = getInfo(i, True)
        print "\twlan%s : %s - %s" % (i, a, b)
    except:
        break