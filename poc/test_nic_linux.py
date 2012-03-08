#!/usr/bin/env python

import fcntl, socket, struct

SIOCGIFNAME   = 0x8910          #/* get iface name               */
SIOCSIFLINK   = 0x8911          #/* set iface channel            */
SIOCGIFCONF   = 0x8912          #/* get iface list               */
SIOCGIFFLAGS  = 0x8913          #/* get flags                    */
SIOCSIFFLAGS  = 0x8914          #/* set flags                    */
SIOCGIFADDR   = 0x8915          #/* get PA address               */
SIOCSIFADDR   = 0x8916          #/* set PA address               */
SIOCGIFDSTADDR= 0x8917          #/* get remote PA address        */
SIOCSIFDSTADDR= 0x8918          #/* set remote PA address        */
SIOCGIFBRDADDR= 0x8919          #/* get broadcast PA address     */
SIOCSIFBRDADDR= 0x891a          #/* set broadcast PA address     */
SIOCGIFNETMASK= 0x891b          #/* get network PA mask          */
SIOCSIFNETMASK= 0x891c          #/* set network PA mask          */
SIOCGIFMETRIC = 0x891d          #/* get metric                   */
SIOCSIFMETRIC = 0x891e          #/* set metric                   */
SIOCGIFMEM    = 0x891f          #/* get memory address (BSD)     */
SIOCSIFMEM    = 0x8920          #/* set memory address (BSD)     */
SIOCGIFMTU    = 0x8921          #/* get MTU size                 */
SIOCSIFMTU    = 0x8922          #/* set MTU size                 */
SIOCSIFNAME   = 0x8923          #/* set interface name */
SIOCSIFHWADDR = 0x8924          #/* set hardware address         */
SIOCGIFENCAP  = 0x8925          #/* get/set encapsulations       */
SIOCSIFENCAP  = 0x8926
SIOCGIFHWADDR = 0x8927          #/* Get hardware address         */
SIOCGIFSLAVE  = 0x8929          #/* Driver slaving support       */
SIOCSIFSLAVE  = 0x8930
SIOCADDMULTI  = 0x8931          #/* Multicast address lists      */
SIOCDELMULTI  = 0x8932
SIOCGIFINDEX  = 0x8933          #/* name -> if_index mapping     */

def getInfo(ifnum, wireless=False):
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