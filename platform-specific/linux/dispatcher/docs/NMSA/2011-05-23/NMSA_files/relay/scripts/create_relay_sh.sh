#!/bin/bash

if [ -e src/relay.sh ]; then
 rm -f src/relay.sh
fi
mac=`ifconfig eth0 | grep HWaddr | awk '{print $5}'`
cat src/relay_no_mac | sed -e 's/CLIENT_MAC/'$mac'/g' >> src/relay_tmp

LAST_IP_OCT=3
ERR_STR="error fetching interface information: Device not found"
ETH_N=""

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
server_ip="10.4.1.6"
echo "setting nmsa ip as $server_ip"

cat src/relay_tmp | sed -e "s/NMSA_IP/$server_ip/" > src/relay.sh
chmod +x src/relay.sh

