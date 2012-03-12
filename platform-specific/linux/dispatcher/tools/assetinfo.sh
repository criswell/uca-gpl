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

IPMITOOL=ipmitool
DCMITOOL=ipmitool
DMIDECODE=/usr/sbin/dmidecode
ASSET_FILE=/opt/intel/assetinfo
DOIPMI=0
DONM=0
BRIDGE=""
TRANSPORT=""
		
GROUP_ARRAY=("chassisGroup" "processorGroup" "memoryGroup" "firmwareGroup" "storageGroup" "networkGroup" "remoteGroup")

CHASSIS_GROUP=("manufacturer" "model" "serialNumber")	 
PROCESSOR_GROUP=("cpuCount" "cpuModel" "corePerCpu" "turbo" "hyperThreading" "vt" "vtd" "Xd" "UUID" "eist" "sriov")
MEMORY_GROUP=("dimmSlots" "dimmsPop" "ramTotal" "dimm")
FIRMWARE_GROUP=("biosVersion" "bmcVersion" "meVersion" "nmVersion" "dcmiVersion")
STORAGE_GROUP=("hardDriveCount" "raid")
NETWORK_GROUP=("nicCount" "macs" "fiberCount")
REMOTE_GROUP=("ipAddress" "iLo" "sol")

CHAN_ARRAY=("0" "6");
TRAN_ARRAY=("0x2c" "0x88");

brute_force() {
 control=0;
 for chan in "${CHAN_ARRAY[@]}"; do
  if [ $control -eq 1 ]; then
   break;
  fi
  for tran in "${TRAN_ARRAY[@]}"; do
   res=`$ipmitool -b $chan -t $tran mc info 2>&1`;
   if grep -q Timeout <<< $res &> /dev/null; then
    continue
   else
    CHAN=$chan
    TRAN=$tran
    control=1
    DONM=1
    break;
   fi
  done
 done
}

checkIpmi() { 
 ipmitool mc info > /tmp/ipmitest;
 if grep "Device ID" /tmp/ipmitest &> /dev/null; then
  DOIPMI=1;
  brute_force
 fi
}

printstart() {
 echo "<Attributes>"
}
printend() {
 echo "</Attributes>"
}

chassisGroup() {
 echo -e "\t<Chassis>" >> $ASSET_FILE
 for funct in "${CHASSIS_GROUP[@]}"; do
  ${funct} >> $ASSET_FILE
 done
 echo -e "\t</Chassis>" >> $ASSET_FILE
}

manufacturer() {
 manf=`$DMIDECODE -s system-manufacturer | sed 's/  */ /g'`
 echo -e "\t\t<Manufacturer>$manf</Manufacturer>"
}

model() {
 mod=`$DMIDECODE  -s system-product-name | sed 's/  */ /g'`
 echo -e "\t\t<Model>$mod</Model>"
}

serialNumber() {
 serial=`$DMIDECODE -s system-serial-number | sed 's/  */ /g'`
 echo -e "\t\t<SerialNumber>$serial</SerialNumber>"
}

processorGroup() {
 echo -e "\t<Processor>" >> $ASSET_FILE
 for funct in "${PROCESSOR_GROUP[@]}"; do
  ${funct} >> $ASSET_FILE
 done
 echo -e "\t</Processor>" >> $ASSET_FILE
} 

cpuCount() {
 ccount=`grep "physical id" /proc/cpuinfo | sort -u | wc -l`
 echo -e "\t\t<CpuCount>$ccount</CpuCount>"
}

cpuModel() {
 cmodel=`grep "model name" /proc/cpuinfo | sort -u | cut -d ":" -f 2| sed 's/  */ /g'`
 echo -e "\t\t<CpuModel>$cmodel</CpuModel>"
}

corePerCpu() {
 ccount=`grep "processor" /proc/cpuinfo | wc -l`
 pcount=`grep "physical id" /proc/cpuinfo|sort -u|wc -l`
 cpc=$((ccount / pcount))
 echo -e "\t\t<CorePerCpu>$cpc</CorePerCpu>"
}

turbo() {
 echo -en "\t\t<Turbo>"
 if grep turbo /proc/cpuinfo &> /dev/null; then
  echo -n "Enabled"
 else
  echo -n "N/A"
 fi
 echo "</Turbo>"
}

hyperThreading() {
 echo -en "\t\t<HyperThreading>"
 if grep ht /proc/cpuinfo &> /dev/null; then 
  echo -n "Enabled"
 else
  echo -n "N/A"
 fi
 echo "</HyperThreading>"
}

vt() {
 echo -en "\t\t<Vt>"
 if grep vt /proc/cpuinfo &> /dev/null; then 
  echo -n "Enabled"
 else
  echo -n "N/A"
 fi
 echo "</Vt>"
}

vtd() {
 echo -en "\t\t<VtD>"
 if grep vtd /proc/cpuinfo &> /dev/null; then 
  echo -n "Enabled"
 else
  echo -n "N/A"
 fi
 echo "</VtD>"
}

Xd() { 
 echo -en "\t\t<VtD>"
 if grep vtd /proc/cpuinfo &> /dev/null; then 
  echo -n "Enabled"
 else
  echo -n "N/A"
 fi
 echo "</VtD>"
}

UUID() {
 echo -en "\t\t<UUID>"
 uuid=`$DMIDECODE| grep UUID | awk '{print $2}'`
 echo -n "$uuid"
 echo "</UUID>"
}

eist() {
 echo -en "\t\t<EIST>"
 if grep eist /proc/cpuinfo &> /dev/null; then 
  echo -n "Enabled"
 else
  echo -n "N/A"
 fi
 echo "</EIST>"
}

sriov() {
 echo -en "\t\t<SRIOV>"
 if grep sriov /proc/cpuinfo &> /dev/null; then 
  echo -n "Enabled"
 else
  echo -n "N/A"
 fi
 echo "</SRIOV>"
}

memoryGroup() {
 echo -e "\t<Memory>" >> $ASSET_FILE
 for funct in "${MEMORY_GROUP[@]}"; do
  ${funct} >> $ASSET_FILE
 done
 echo -e "\t</Memory>" >> $ASSET_FILE
}

dimmSlots() {
 cnt=`$DMIDECODE | grep "Memory Device" | wc -l`
 echo -e "\t\t<DimmSlots>$cnt</DimmSlots>"
}

dimmsPop() {
 cnt=`$DMIDECODE | grep "Memory Device" -A 17 | grep "Size" | grep -v "No Module Installed" | wc -l`
 echo -e "\t\t<DimmPopulated>$cnt</DimmPopulated>"
}

ramTotal() {
 result=`$DMIDECODE | grep "Memory Array" -A 6 | grep Range | awk '{print $3$4}' | tail -n 1`
 echo -e "\t\t<RamTotal>$result</RamTotal>"
}

dimm() {
 echo -en "\t\t<Dimm>\n"
 for dimm in `$DMIDECODE | grep "Memory Device" -A 17 | grep "Size" | grep -v "No Module" | grep -v "Range" | awk '{print $2$3}'`; do
  echo -en "\t\t\t<DimmSize>"
  echo -en "$dimm"
  echo    "</DimmSize>"  
 done
 echo -e "\t\t</Dimm>"
}

firmwareGroup() {
 echo -e "\t<Firmware>" >> $ASSET_FILE
 for funct in "${FIRMWARE_GROUP[@]}"; do
  ${funct} >> $ASSET_FILE
 done
 echo -e "\t</Firmware>" >> $ASSET_FILE
}

biosVersion() {
 bv=`$DMIDECODE -s bios-version`
 echo -e "\t\t<BiosVersion>$bv</BiosVersion>"
}

bmcVersion() {
 bv="N/A"
 if [ $DOIPMI -gt 0 ]; then
  bv=`$IPMITOOL mc info | grep Firmware | grep -v Aux | awk '{print $4}'`
 fi
 echo -e "\t\t<BmcVersion>$bv</BmcVersion>"
}

meVersion() {
 mv="N/A"
 if [ $DOIPMI -gt 0 ]; then
  if [ $DONM -gt 0 ]; then
   mv=`$IPMITOOL -b $BRIDGE -t $TRANSPORT mc info | grep "Firmware Revision" | awk '{print $4}'`
  fi
 fi
 echo -e "\t\t<MeVersion>$mv</MeVersion>"
}

nmVersion() {
nv="N/A"
if [ $DOIPMI -gt 0 ]; then
if [ $DONM -gt 0 ]; then
nv="N/A"
tmp=`ipmitool  -b 06 -t 0x2c raw 0x2e 0xca 0x57 0x01 0x00 | awk '{print $4}'`
case $tmp in
01)
  nv="1.0"
  ;;
02)
  nv="1.5"
  ;;
03)
  nv="2.0"
  ;;
esac
fi
fi
echo -e "\t\t<NmVersion>$nv</NmVersion>"
}

dcmiVersion() {
 echo -e "\t\t<DcmiVersion>N/A</DcmiVersion>"
}

storageGroup() {
 echo -e "\t<Storage>" >> $ASSET_FILE
 for funct in "${STORAGE_GROUP[@]}"; do
  ${funct} >> $ASSET_FILE
 done
 echo -e "\t</Storage>" >> $ASSET_FILE
}

hardDriveCount() {
 cnt=` fdisk -l | grep "^Disk" | cut -f 1 -d ',' | cut -f 3- -d '/' | wc -l`
 echo -e "\t\t<HardDriveCount>$cnt</HardDriveCount>"
}

raid() {
 echo -en "\t\t<Raid>"
 if dmesg | grep raid| grep PCI &> /dev/null; then
  echo -n "Enabled"
 else
  echo -n "Disabled"
 fi
 echo "</Raid>"
}

networkGroup() {
 echo -e "\t<Network>" >> $ASSET_FILE
 for funct in "${NETWORK_GROUP[@]}"; do
  ${funct} >> $ASSET_FILE
 done
 echo -e "\t</Network>" >> $ASSET_FILE
}

nicCount() {
 cnt=`ifconfig -a | grep HWaddr | wc -l`
 echo -e "\t\t<NicCount>$cnt</NicCount>"
}

macs() {
 echo -e "\t\t<Macs>"
 for i in `ifconfig -a | grep HWaddr | awk '{print $5}'`; do
  echo -e "\t\t\t<WiredMacAddress>$i</WiredMacAddress>"
 done
 echo -e "\t\t</Macs>"
}

fiberCount() {
 FC_DIR=/sys/class/fc_host
 fc=0
 if [ -d $FC_DIR ]; then
  fc=`ls -1 $FC_DIR | wc -l`
 fi
 echo -e "\t\t<FiberCount>$fc</FiberCount>"
}

remoteGroup() {
 echo -e "\t<RemoteCapability>" >> $ASSET_FILE
 for funct in "${REMOTE_GROUP[@]}"; do
  ${funct} >> $ASSET_FILE
 done
 echo -e "\t</RemoteCapability>" >> $ASSET_FILE
}

ipAddress() {
 ip="N/A"
 if [ $DOIPMI -gt 0 ]; then
  ip=`$IPMITOOL lan print | grep "IP Addr" | grep -v Source | awk '{print $4}'`
 fi
 echo -e "\t\t<BmcIpAddress>$ip</BmcIpAddress>"
}

iLo() {
 echo -e "\t\t<iLo>N/A</iLo>"
}

sol() {
 result="N/A"
 if [ $DOIPMI -gt 0 ]; then
  test=` $IPMITOOL sol info 1 | grep Enabled | awk '{print $3}'`
  if [ "$test" == "true" ]; then
   result="Enabled"
  fi
 fi
 echo -e "\t\t<SerialOverLan>$result</SerialOverLan>"
}

collectInfo() {
 checkIpmi
 if [ ! -d /opt/intel ]; then
  mkdir -p /opt/intel
 fi
 printstart > $ASSET_FILE
 for group in "${GROUP_ARRAY[@]}"; do
  ${group}
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