#!/bin/bash

### BEGIN INIT INFO
# Provides:             assetinfo
# Required-Start:       $local_fs $syslog ipmidrv
# Required-Stop:        $local_fs $syslog ipmidrv
# Default-Start:        2 3 4 5
# Default-Stop:
# Short-Description:    asset collection script
# Description:          asset collection script
### END INIT INFO

# RHEL information
# chkconfig: 2345 80 20
# description: asset collection script

# this check is slaxPxe specific, should
# fail on any other time
if [ -e /etc/rc.d/rc.myipmisetup ]; then 
  /etc/rc.d/rc.myipmisetup &> /dev/null
fi

IPMITOOL=/usr/local/bin/ipmitool
DCMITOOL=/usr/local/bin/ipmitool
DMIDECODE=/usr/sbin/dmidecode

DOIPMI=0

FUNCT_ARRAY=("turbo" "hyperthreading" "vt" "vtd" "Xd" "UUID" "c6state" "c2c4state"
             "nmver" "dcmiver" "eist" "dimmslots" "dimmspop" "ramtotal" "dimm"
             "sriov" "niccount" "nicspeed" "fibercount" "fiberspeed" "sol"
             "remote" "hdcount" "raid" "oem")

checkIpmi() { 
 ipmitool mc info > /tmp/ipmitest;
 if grep "Device ID" /tmp/ipmitest &> /dev/null; then
  DOIPMI=1;
 fi
}

printstart() {
 echo "<Attributes>"
}
printend() {
 echo "</Attributes>"
}

turbo() { #<Turbo>Enabled/Disabled</Turbo>
 echo "<Key>Turbo</Key><Value>N/A</Value>" 
}

hyperthreading() { #<HyperThreading>Enabled/Disabled</HyperThreading>
 echo -n "<Key>HyperThreading</Key><Value>"
 if grep ht /proc/cpuinfo &> /dev/null; then 
  echo -n "Enabled"
 else
  echo -n "Disabled"
 fi
 echo "</Value>"
}

vt() { #<Vt>Enabled/Disabled</Vt>
 echo "<Key>Vt</Key><Value>N/A</Value>"
}

vtd() { #<Vt-d>Enabled/Disabled</Vt-d>
 echo "<Key>Vt-d</Key><Value>N/A</Value>"
}

Xd() { #<Xd>Enabled/Disabled</Xd>
 echo "<Key>Xd</Key><Value>N/A</Value>"
}

UUID() { #<UUID>Urbanna</UUID>                
 echo -n "<Key>UUID</Key><Value>"
 uuid=`$DMIDECODE| grep UUID | awk '{print $2}'`
 echo -n "$uuid"
 echo "</Value>"
}

c6state() { #<C6State>Enabled/Disabled</C6State>
 echo "<Key>C6State</Key><Value>N/A</Value>"
}

c2c4state() { #<C2C3>Enabled/Disabled</C2C3>
 echo "<Key>C2C3</Key><Value>N/A</Value>"
}

nmver() { #<NMVersion>1.5</NMVersion>
 if [ $DOIPMI -eq 0 ]; then
  echo "<Key>NMVersion</Key><Value>Disabled</Value>"
 else
  echo -n "<Key>NMVersion</Key><Value>"
  bmc_v=`$IPMITOOL mc info | grep IPMI | awk '{print $4}' 2>/dev/null`
  BMC_VER="Disabled"
  if [ "$bmc_v" == "2.0" ]; then
   BMC_VER="1.5"
  fi
  if [ "$bmc_v" == "2" ]; then
   BMC_VER="1.5"
  fi
  if [ "$bmc_v" == "3.0" ]; then
   BMC_VER="2.0"
  fi
  echo  -n "$BMC_VER"
  echo "</Value>"
 fi
}

dcmiver() { #<DCMIVersion>1.5</DCMIVersion>
 if [ $DOIPMI -eq 0 ];then 
  echo "<Key>DCMIVersion</Key><Value>Disabled</Value>"
 else
  echo -n "<Key>DCMIVersion</Key><Value>"
  v=`$DCMITOOL  raw 0x2c 0x01 0xdc 0x01 | awk '{print $2"."$3}'`
  echo -n "$v"
  echo "</Value>"
 fi
}

eist() { #<EIST>Enabled/Disabled</EIST>
 echo "<Key>EIST</Key><Value>N/A</Value>"
}

dimmslots() { #<DimmSlots>4</DimmSlots>
 echo -n "<Key>DimmSlots</Key><Value>"
 cnt=`$DMIDECODE | grep "Memory Device" | wc -l`
 echo -n "$cnt"
 echo "</Value>"
}

dimmspop() { #<DimmPopulated>4</DimmPopulated>
 echo -n "<Key>DimmPopulated</Key><Value>"
 cnt=`$DMIDECODE | grep "Memory Device" -A 17 | grep "Size" | grep -v "No Module Installed" | wc -l`
 echo -n "$cnt"
 echo "</Value>"
}

ramtotal() { #<RamTotal>12</RamTotal>
 echo -n "<Key>RamTotal</Key><Value>"
 result=`$DMIDECODE | grep "Memory Array" -A 6 | grep Range | awk '{print $3$4}'`
 echo -n "$result"
 echo "</Value>"
}

dimm() { #<Dimm><DimmSpeed>1066</DimmSpeed><DimmSize>2</DimmSize></Dimm>
 echo -en "<Key>Dimm</Key>\n<Value>\n"
 for dimm in `$DMIDECODE | grep "Memory Device" -A 17 | grep "Size" | grep -v "No Module" | grep -v "Range" | awk '{print $2$3}'`; do
  echo -en "\t<Key>DimmSize</Key><Value>"
  echo -en "$dimm"
  echo    "</Value>"  
 done
 echo "</Value>"
}

sriov() { #<SR-IOV>Enabled/Disabled</SR-IOV>
 echo "<Key>SR-IOV</Key><Value>N/A</Value>"
}

niccount() { #<NicCount>2</NicCount>
 echo -n "<Key>NicCount</Key><Value>"
 cnt=`ifconfig -a| grep eth | wc -l`
 echo -n "$cnt"
 echo "</Value>"
}

nicspeed() { #<NicSpeed>1Gb</NicSpeed>
 for i in "`dmesg | grep eth | grep Mbps`"; do
  speed=`echo $i | awk '{print $7 " " $8}'` 
  echo "<Key>NicSpeed</Key><Value>$speed</Value>"
 done
}

FC_DIR=/sys/class/fc_host

fibercount() { #<FiberCount>2</FiberCount>
 echo -n "<Key>FiberCount</Key><Value>"
 if [ ! -d $FC_DIR ]; then
  echo -n "0"
 else
  PORT_CNT=`ls -1 $FC_DIR| wc -l`
  echo -n "$PORT_CNT"
 fi
 echo "</Value>"
}

fiberspeed() { #<FiberSpeed>1Gb</FiberSpeed>
 if [ -d $FC_DIR ]; then 
  for i in `ls -1 $FC_DIR`; do
   echo -n "<Key>FiberSpeed</Key><Value>"
   SPEEDS=`cat $FC_DIR/$i/supported_speeds`
   echo -n "$SPEEDS"
   echo "</Value>"
  done
 else
  echo "<Key>FiberSpeed</Key><Value>Disabled</Value>"
 fi
}

sol() { #<SerialOverLan>Enabled/Disabled</SerialOverLan>
 if [ $DOIPMI -eq 0 ]; then 
  echo "<Key>SerialOverLan</Key><Value>Disabled</Value>"
 else
  echo -n "<Key>SerialOverLan</Key><Value>"
  test=` $IPMITOOL sol info 1 | grep Enabled | awk '{print $3}'`
  if [ "$test" == "true" ]; then
   echo -n "Enabled"
  else
   echo -n "Disabled"
  fi
  echo "</Value>"
 fi
}

remote() { #<RemoteCapability><IPaddress>10.19.253.1</IPaddress><Weblink>http://10.19.253.1</Weblink><iLO></iLO></RemoteCapability> 
 echo -en "<Key>RemoteCapability</Key>\n<Value>\n"
  echo -en "\t<Key>IPaddress</Key><Value>"
  ip=""
  if [ $DOIPMI -eq 0 ]; then
   ip="N/A"
  else
   ip=`$IPMITOOL lan print | grep "IP Addr" | grep -v Source | awk '{print $4}'`
  fi
  echo -en "$ip"
  echo "</Value>"
  echo -e "\t<Key>Weblink</Key><Value>http://$ip</Value>"
  echo -e "\t<Key>iLO</Key><Value>N/A</Value>"
 echo "</Value>"
}

hdcount() { #<HardDriveCount>3</HardDriveCount>
 echo -n "<Key>HardDriveCount</Key><Value>"
 cnt=` fdisk -l | grep "^Disk" | cut -f 1 -d ',' | cut -f 3- -d '/' | wc -l`
 echo -n "$cnt"
 echo "</Value>"
}

raid() { #<Raid>Enabled/Disabled</Raid>
 echo  "<Key>Raid</Key><Value>Disabled</Value>"
# if dmesg | grep raid| grep PCI &> /dev/null; then 
#33333  echo -n "Enabled"
# else
#  echo -n "Disabled"
#33 fi
# echo "</Value>"
}

oem() { #<OEMInventory><Bios>1.5</Bios><BMC>2.11</BMC></OEMInventory>
 echo -en "<Key>OEMInventory</Key>\n<Value>\n\t"
 echo -n "<Key>Bios</Key><Value>"
 bv=`$DMIDECODE -s bios-version`
 echo  "$bv</Value>"
 echo -en "\t<Key>BMC</Key><Value>"
 ver=""
 if [ $DOIPMI -eq 0 ]; then
  ver="N/A"
 else
  ver=` $IPMITOOL mc info | grep Firmware | grep -v Aux | awk '{print $4}'`
 fi
 echo -n "$ver"
 echo "</Value>"
 
 echo "</Value>"
}

collectInfo() {
 checkIpmi
 if [ ! -d /opt/intel ]; then
  mkdir -p /opt/intel
 fi
 ASSET_FILE=/opt/intel/assetinfo
 printstart > $ASSET_FILE
 for funct in "${FUNCT_ARRAY[@]}"; do
  ${funct} >> $ASSET_FILE
 done
 printend >> $ASSET_FILE
}

if [ -f /lib/lsb/init-functions ]; then
 . /lib/lsb/init-functions 
fi

case "$1" in
start|restart)
    collectInfo
    exit 0
    ;;
esac
exit 0