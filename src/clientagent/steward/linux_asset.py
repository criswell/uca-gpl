'''
linux_asset.py
--------------
Derived asset collection class specific to Linux.
'''

import exceptions
from clientagent.steward.asset import EILAsset
from clientagent.common.ordereddict import OrderedDict as OD
import fcntl, socket, struct, os, platform
import ctypes
from ctypes.util import find_library
from ctypes import Structure
from clientagent.common.utility import locateExecInPath

class DBusError(Structure):
    '''
    Defines the error interface for DBUS
    '''
    _fields_ = [("name", ctypes.c_char_p),
                ("message", ctypes.c_char_p),
                ("dummy1", ctypes.c_int),
                ("dummy2", ctypes.c_int),
                ("dummy3", ctypes.c_int),
                ("dummy4", ctypes.c_int),
                ("dummy5", ctypes.c_int),
                ("padding1", ctypes.c_void_p),]

class HardwareUuid(object):
    '''
    Used to obtain the hardware UUID. This is Linux-specific code, and requires
    hal running on the system. The system should also be compliant with
    http://www.freedesktop.org/wiki/Software/hal . Note that in the future,
    this might need to be rewritten to use DeviceKit, but for now we have hal.
    '''
    def __init__(self, dbus_error=DBusError):
        self._hal = ctypes.cdll.LoadLibrary(find_library('hal'))
        self._ctx = self._hal.libhal_ctx_new()
        self._dbus_error = dbus_error()
        self._hal.dbus_error_init(ctypes.byref(self._dbus_error))
        self._conn = self._hal.dbus_bus_get(ctypes.c_int(1),
                                            ctypes.byref(self._dbus_error))
        self._hal.libhal_ctx_set_dbus_connection(self._ctx, self._conn)
        self._uuid_ = None

    def __call__(self):
        return self._uuid

    @property
    def _uuid(self):
        if not self._uuid_:
            udi = ctypes.c_char_p("/org/freedesktop/Hal/devices/computer")
            key = ctypes.c_char_p("system.hardware.uuid")
            self._hal.libhal_device_get_property_string.restype = \
                                                            ctypes.c_char_p
            self._uuid_ = self._hal.libhal_device_get_property_string(
                                self._ctx, udi, key, self._dbus_error)
        return self._uuid_

class Linux_Asset(EILAsset):
    '''
    The Linux-specific asset collection sub-class.
    '''

    def initialize(self):
        '''
        This will be called once, when the module is initialized. Put any
        code here that should be called at program start.
        '''

        # Pull some defines from linux/sockios.h, we may not need all of them
        # but just grab them in bulk in case.
        self.SIOCGIFNAME   = 0x8910          #/* get iface name               */
        self.SIOCSIFLINK   = 0x8911          #/* set iface channel            */
        self.SIOCGIFCONF   = 0x8912          #/* get iface list               */
        self.SIOCGIFFLAGS  = 0x8913          #/* get flags                    */
        self.SIOCSIFFLAGS  = 0x8914          #/* set flags                    */
        self.SIOCGIFADDR   = 0x8915          #/* get PA address               */
        self.SIOCSIFADDR   = 0x8916          #/* set PA address               */
        self.SIOCGIFDSTADDR= 0x8917          #/* get remote PA address        */
        self.SIOCSIFDSTADDR= 0x8918          #/* set remote PA address        */
        self.SIOCGIFBRDADDR= 0x8919          #/* get broadcast PA address     */
        self.SIOCSIFBRDADDR= 0x891a          #/* set broadcast PA address     */
        self.SIOCGIFNETMASK= 0x891b          #/* get network PA mask          */
        self.SIOCSIFNETMASK= 0x891c          #/* set network PA mask          */
        self.SIOCGIFMETRIC = 0x891d          #/* get metric                   */
        self.SIOCSIFMETRIC = 0x891e          #/* set metric                   */
        self.SIOCGIFMEM    = 0x891f          #/* get memory address (BSD)     */
        self.SIOCSIFMEM    = 0x8920          #/* set memory address (BSD)     */
        self.SIOCGIFMTU    = 0x8921          #/* get MTU size                 */
        self.SIOCSIFMTU    = 0x8922          #/* set MTU size                 */
        self.SIOCSIFNAME   = 0x8923          #/* set interface name */
        self.SIOCSIFHWADDR = 0x8924          #/* set hardware address         */
        self.SIOCGIFENCAP  = 0x8925          #/* get/set encapsulations       */
        self.SIOCSIFENCAP  = 0x8926
        self.SIOCGIFHWADDR = 0x8927          #/* Get hardware address         */
        self.SIOCGIFSLAVE  = 0x8929          #/* Driver slaving support       */
        self.SIOCSIFSLAVE  = 0x8930
        self.SIOCADDMULTI  = 0x8931          #/* Multicast address lists      */
        self.SIOCDELMULTI  = 0x8932
        self.SIOCGIFINDEX  = 0x8933          #/* name -> if_index mapping     */

    def _getInfo(self, ifnum, wireless=False):
        '''
        Get the interface information for ifnum.

        @param ifnum: The interface number
        @param wireless: If the interface is wireless or not

        @returns: A tuple containing (hardware_address, ipv4, ipv6)
        '''
        ifname = "eth%s" % ifnum
        if wireless:
            ifname = "wlan%s" % ifnum
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hwinfo = fcntl.ioctl(s.fileno(), SIOCGIFHWADDR, struct.pack('256s', ifname[:15]))
        hwaddr = ''.join(['%02x:' % ord(char) for char in hwinfo[18:24]])[:-1]

        ipaddr = None
        try:
            hwinfo = fcntl.ioctl(s.fileno(), SIOCGIFADDR, struct.pack('256s', ifname[:15]))
            ipaddr = ''.join(['%s.' % ord(char) for char in hwinfo[20:24]])[:-1]
        except:
            pass

        ivp6 = None
        s.close()
        # FIXME - For now we do nothing
        #s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        #hwinfo = fcntl.ioctl(s.fileno(), SIOCGIFHWADDR, struct.pack('256s', ifname[:15]))
        #ipv6 = ''.join(['%02x:' % ord(char) for char in hwinfo[18:24]])[:-1]

        return (hwaddr, ipaddr, ipv6)

    def _locateInPath(obj):
        '''
        Given a command or list of commands, try to locate them in path.

        @returns: True if all commands are found. False if any one is missing.
        '''
        if type(obj) == str:
            if locateExecInPath(obj):
                return True
        else:
            retval = True
            for i in obj:
                if locateExecInPath(i) == None:
                    retval = False
            return retval
        return False

    def _getCommandOutput(self, cmd, lines):
        '''
        Given a command, will get the output
        '''
        try:
            stream = os.popen(cmd)
            output = stream.readlines()
            stream.close()

            if len(output) >= lines:
                if lines == 1:
                    return output[0].strip()
                else:
                    return outpit[0:lines]
            else:
                return None
        except:
            return None


    def _getUUID(self):
        '''
        Attempts to get and return the UUID
        '''
        try:
            return HardwareUuid()
        except:
            # Silly wrong or no hal systems
            if self._locateInPath('dmidecode', 'awk', 'grep'):
                try:
                    output = self._getCommandOutput("dmidecode | grep UUID | awk '{print $2}'")

                    if len(output) > 0:
                        return output[0].strip()
                except:
                    return None

        # IF we get here, we haven't found it
        return None

    def _getBiosInfo(self):
        '''
        Will attempt to get the BIOS information.

        returns: A tuple containing
            (biosVersion,
            motherboardManufact,
            motherboardModel,
            motherboardSerial)

            Any fields not found will be None.
        '''
        if locateExecInPath('dmidecode'):
            biosVersion = self._getCommandOutput('dmidecode -s bios-version', 1)
            moboManufact = self._getCommandOutput('dmidecode -s baseboard-manufacturer', 1)
            moboModel = self._getCommandOutput('dmidecode -s baseboard-product-name', 1)
            moboSerial = self._getCommandOutput('dmidecode -s baseboard-serial-number', 1)

            return (biosVersion, moboManufact, moboModel, moboSerial)
        else:
            return (None, None, None, None)

    def updateAsset(self):
        '''
        Called when we update the asset from getAssetXML
        '''
        self.asset['Common']['HostName'] = os.uname()[1]
        self.asset['Common']['UUID'] = self._getUUID()
        self.asset['Common']['DomainName'] = socket.getfqdn()

        self.asset['Common']['OS'] = platform.system()
        self.asset['Common']['OSVersion'] = ' '.join(platform.linux_distribution())
        self.asset['Common']['OSArchitecture'] = ' '.join(platform.architecture())
        self.asset['Common']['OSKernel'] = platform.release()

        # Until we can figure out a red pill/blue pill method in Python, this is
        # commented out
        #self.asset['Common']['VirtualMachine'] = False

        (biosVersion, moboManufact, moboModel, moboSerial) = self._getBiosInfo()
        self.asset['Common']['BiosVersion'] = biosVersion

        mobo = OD([
                ('Manufacturer' , moboManufact),
                ('Model' , moboModel),
                ('SerialNumber' , moboSerial),
            ])

        self.asset['Common']['Motherboard'] = mobo

        if self._locateInPath('cat', 'grep', 'sort', 'uniq', 'wc'):
            cpuCount = self._getCommandOutput('cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l', 1)
            tmpCpuModel = self._getCommandOutput('cat /proc/cpuinfo | grep "model name" | sort | uniq', 1)
            cpuModel = ' '.join(tmpCpuModel.split()[3:])
            tmpCores = self._getCommandOutput('cat /proc/cpuinfo | grep "cpu cores" | sort | uniq', 1)
            cores = tmpCores.split(':')[-1].strip()

            # Now, we run through the CPU flags to get everything we need
            tmpFlags = self._getCommandOutput('cat /proc/cpuinfo | grep "flags" | sort | uniq', 1).lower()
            flags = tmpCpuModel.split(':')[-1].strip().split()
            hyperThreading = False
            vt = False
            vtd = False
            eist = False
            sriov = None
            trubo = None
            if ('ht' in flags) or ('htt' in flags):
                hyperThreading = True
            if ('vmx' in flags) or ('svm' in flags):
                vt = True
            if ('vnmi' in flags) or ('smx' in flags):
                # NOTE - I'm not 100% certain about this one
                vtd = True
            if ('eist' in flags) or ('est' in flags):
                eist = True
            # FIXME - I do not know how to check for SRIOV
            # FIXME - I do not know how to check for Turbo

            processor = OD([
                ('CpuCount' , cpuCount),
                ('CpuModel' , cpuModel),
                ('CoresPerCpu' , cores),
                ('Turbo' , turbo),
                ('HyperThreading' , hyperThreading),
                ('Vt' , vt),
                ('VtD' , vtd),
                ('EIST' , eist),
                ('SRIOV' , sriov),
            ])
            self.asset['Common']['Processor'] = processor

# vim:set ai et sts=4 sw=4 tw=80:
