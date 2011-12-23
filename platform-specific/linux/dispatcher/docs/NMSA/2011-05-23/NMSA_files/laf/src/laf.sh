#!/bin/bash 

LOG_FILE=/opt/intel/eil/laf/log/laf-`date +%m_%d_%y-%M_%S`.log                # HARDCODED VALUE

# variables for debugging, set DEBUG=1 to enable
# dbecho function which logs to a special debug file
DEBUG=1
DEBUG_LOG_FILE=/opt/intel/eil/laf/log/laf_debug-`date +%m_%d_%y-%M_%S`.log

SID=$1
#echo "sid[$SID]"
R_WORKLOAD_FULL=$2
#echo "r_workload_full[$R_WORKLOAD_FULL]"
WORKLOAD=`basename $R_WORKLOAD_FULL`
#echo "workload[$WORKLOAD]"
L_WORKLOAD_DIR=/tmp
#echo "l_workload_dir[$L_WORKLOAD_DIR]"
L_WORKLOAD_FILE=$L_WORKLOAD_DIR/$WORKLOAD
#echo "l_workload_file[$L_WORKLOAD_FILE]"
CMD_ARRAY=()

RET_VAL=0
LOCKFILE=/opt/intel/eil/laf/sids/$SID
OUTFILE=/opt/intel/eil/laf/output/$SID

. /opt/intel/eil/laf/bin/laf-lib.sh

_init

get_workload $R_WORKLOAD_FULL $L_WORKLOAD_FILE

if [ ! $? -eq 0 ]; then
 _exit
fi

get_cmds $L_WORKLOAD_FILE
run_cmds

_exit $RET_VAL