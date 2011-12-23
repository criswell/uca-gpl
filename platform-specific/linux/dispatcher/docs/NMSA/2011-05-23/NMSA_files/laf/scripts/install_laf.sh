#!/bin/bash

INSTALL_DIR=/opt/intel/eil/laf
CREATE_DIR=("bin" "log" "output" "sids")
REQ_PROGS=("wget")

has_cmd() {
 ret=0;
 cmd=$1
 shift
 tmp_f=/tmp/`date +%m%d%y-%M%S`
 whereis $cmd > $tmp_f
 if [ ! $? -eq 0 ]
 then
  logerr $client 6 "+1"
  return 1
 fi
 str=`cat $tmp_f | awk '{print $2}'`
 if [ ! -n "$str" ]
 then
  ret=1
 fi
 rm $tmp_f
 return $ret
}

check_req_progs() {
 ret=0
 for prog in "${REQ_PROGS[@]}"; do
  has_cmd $prog
  if [ $? -eq 1 ]; then
   echo "Missing required program $prog.  Please install and then try again"
   ret=1
   break
  fi
 done
 return $ret
} 

create_dir() { 
 if [ ! -d $INSTALL_DIR ]; then
  if [ ! -d /opt/intel/eil ]; then
   if [ ! -d /opt/intel ]; then
    mkdir /opt/intel
   fi
   mkdir /opt/intel/eil
  fi
  mkdir $INSTALL_DIR
 fi
 
 for dir in "${CREATE_DIR[@]}"; do
  if [ ! -d $INSTALL_DIR/$dir ]; then
   mkdir $INSTALL_DIR/$dir
  fi
 done
}

LUID=$(id -u)
if [[ $LUID -ne 0 ]]; then
 echo "Please run install script as root"
 exit 1
fi


check_req_progs
if [ ! $? -eq 0 ]; then
 echo "Please install missing programs and then run installer again"
 exit 1
fi
create_dir
cp src/*.sh $INSTALL_DIR/bin
