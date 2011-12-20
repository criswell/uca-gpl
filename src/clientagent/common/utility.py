'''
Basic utilities which we may need multiple times
'''

import os
from clientagent.common.platform_id import PlatformID
from clientagent import ClientAgentState

_platformId = PlatformID()
if _platformId.IS_WINDOWS:
    import win32api
    import win32security
    from ntsecuritycon import *
    from netbios import *
    from socket import gethostname
else:
    import fcntl, socket, struct

def mkdir_p(path):
    '''
    Does the equivalent of a 'mkdir -p' (Linux) on both platforms.
    '''
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def getIfInfo():
    '''
    Get Interface Info.

    Obtains the hardware address from the first network interface on the
    machine.

    Returns:
        A tuple containing the (HW_ADDRESS, HOSTNAME)
    '''
    if _platformId.IS_LINUX:
        ifnum = 0
        ifname = "eth%s" % ifnum
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hwinfo = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
        return (''.join(['%02x:' % ord(char) for char in hwinfo[18:24]])[:-1], os.uname()[1])
    else:
        ncb = NCB()
        ncb.Command = NCBENUM
        la_enum = LANA_ENUM()
        ncb.Buffer = la_enum
        rc = Netbios(ncb)
        if rc != 0: raise RuntimeError, "Unexpected result %d" % (rc,)
        # Grab the first one
        ncb.Reset()
        ncb.Command = NCBRESET
        ncb.Lana_num = ord(la_enum.lana[0])
        rc = Netbios(ncb)
        if rc != 0: raise RuntimeError, "Unexpected result %d" % (rc,)
        ncb.Reset()
        ncb.Command = NCBASTAT
        ncb.Lana_num = ord(la_enum.lana[0])
        ncb.Callname = "*               "
        adapter = ADAPTER_STATUS()
        ncb.Buffer = adapter
        Netbios(ncb)
        return (''.join(['%02x:' % ord(char) for char in adapter.adapter_address])[:-1], gethostname())


# vim:set ai et sts=4 sw=4 tw=80:
