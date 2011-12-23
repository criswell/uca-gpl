#!/bin/bash

LAST_IP_OCT=6
ERR_STR="error fetching interface information: Device not found"
ETH_N=""
LAF_FILE="src/laf-lib.sh"

for i in {0..10} ; do
 /sbin/ifconfig eth$i > tmp.f
 if ! grep "$ERR_STR" tmp.f; then
  tmp_n=$i
  ip=`ifconfig eth$tmp_n | grep "inet addr" | awk '{print $2}' | sed -e 's/addr://'`
  front_oct=${ip%.*}
  if [ ! -z "$front_oct" ]; then
   ETH_N=$i
   echo "found first valid interface: $i"
   break
  fi
 fi
done
rm tmp.f

ip=`ifconfig eth$ETH_N | grep "inet addr" | awk '{print $2}' | sed -e 's/addr://'`
front_oct=${ip%.*}
server_ip="$front_oct.$LAST_IP_OCT"
echo "setting nmsa ip as $server_ip"

cat $LAF_FILE | sed -e "s/NMSA_IP/$server_ip/" > src/tmp.sh
mv $LAF_FILE $LAF_FILE.src
mv src/tmp.sh $LAF_FILE
