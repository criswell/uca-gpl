#!/bin/bash -x

# the main logging function, used to output errors to the logfile
# should not be used for debugging, use dbecho instead
# currently n argument, and prints them in the following order
# $1, $2, $3,... $n
logerr() {
 echo -n "`date +%d/%m/%y-%H:%M,`" >> $LOG_FILE
 until [ -z "$1" ]; do
  echo -n ",$1 " >> $LOG_FILE
  shift
 done
 echo " " >> $LOG_FILE
}

#best way to call this is to do something like
# dbecho "some string"
# there is no need to call this function with the name of the 
# calling funciton or the line number because this is done for
# us by using the caller function
dbecho () {
 if [ ! $DEBUG -eq 1 ]; then
  return 0
 fi
 echo -n "`date +%d/%m/%y-%H:%M`> " >> $DEBUG_LOG_FILE
 str="`caller 0`"
 echo -n "$str" >> $DEBUG_LOG_FILE
 until [ -z "$1" ]; do
  echo -n ",$1 " >> $DEBUG_LOG_FILE
  shift
 done
 echo " " >> $DEBUG_LOG_FILE
}

# this is the function to start up everything
# this includes starting the log file and calling
# get_args (which calls get_clients and get_cmds)
# if you need to do any initilization places calls 
# to your function in this script
_init () {
 if [ -e $LOCKFILE ]; then
  logerr 4
  exit 4
 fi
 touch $LOCKFILE
 logerr "** ref initializing ***"
}

gen_outfile() {
 while read line; do
  if [ -z "$line" ]                         # skip the blank lines
  then
   continue
  fi
  LINES=("${LINES[@]}" "$line")
 done < $LOG_FILE
 for l in "${LINES[@]}"; do
  echo -n $l | sed -e 's/ /+/g' >> $OUTFILE
 done
 echo "" >> $OUTFILE
}


# we use this instead of exit so that we make sure to output
# the address of the log file so that what ever is calling this
# script can know were to go to look for errors
# this function takes 1 arg, $exit-code, which is the code the
# script should exit with
_exit() {
 logerr "** ref exiting **"
 echo -n "exit:$1|" >> $OUTFILE
# gen_outfile
 rm $LOCKFILE
 exit $1
}

#this is the function to parse our command file
#it takes 1 argument, $file, which is the location
#of the command file.  Later when we want to use the
#array, we can do the following
#  for t in "${CMD_ARRAY[@]}"
# do
#  `$t`  # run the command
# done
get_cmds() {
 if [ ! -e $1 ]
 then
  logerr 4 "$1"
  _exit 1
 fi
 while read line
 do
  if [ -z "$line" ]                         # skip the blank lines
  then
   continue
  fi
  char=${line:0:1}
  if [ ! "$char" == "#" ]; then
   CMD_ARRAY=("${CMD_ARRAY[@]}" "$line")
  fi
 done < $1
}

# this function is used to verify that the client has
# the command we want to run before we run it
# takes 1 arguments $cmd
has_cmd() {
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
 rm $tmp_f
 if [ ! -n "$str" ]
 then
  return 1
 fi
 return 0
}


check_err() {
 cmd_output_f=$1
 ret=0
 return $(( ret ))
}


# this is the function to actually run the command
# on the client, it currently takes one arguments
# $command 
_run_cmd() {
 tmp_cmd=$1
 char=${tmp_cmd:0:1}
 report_bck=0
 dbecho "checking ~> $tmp_cmd for !, found $char"
 if [ "$char" == "!" ]; then
  report_bck=1 
  full_cmd=${tmp_cmd:1}; 
  dbecho "found it"
 else 
  full_cmd=$tmp_cmd; 
 fi

 command="${full_cmd/_*/}"
 comment="${full_cmd/*_/}"
 cmd_output_f=/tmp/cmd_output_f
 dbecho "client[$client] command[$command] tmp_f[$tmp_f]"
 #echo "running $command"
 tmp_proxy=$http_proxy  # we do this so any local proxy settings don't
 http_proxy=""          # screw up the wget
 wget -O /tmp/laf-testing2 "10.4.1.6/laf_update.php?sid=$SID&type=1&data=`echo $full_cmd |sed -e 's/ /+/g'`" &> /tmp/laf-testing
 http_proxy=$tmp_proxy
 $command > $cmd_output_f
 if [ $report_bck -eq 1 ]; then
  tmp_proxy=$http_proxy
  http_proxy=""
  wget -O /tmp/laf-testing3 "10.4.1.6/laf_update.php?sid=$SID&type=2&data=`cat $cmd_output_f|sed -e 's/ /+/g'`" &> /tmp/laf-testing4
  http_proxy=$tmp_proxy
 fi 
 check_err $cmd_output_f
 ret=$?
 return $ret
}

# this program takes no arguments
# when called it uses the following logic
# for x in cmd_arry
#  for y in client_arry
#   run y x
#todo:
# add error checking to commands
run_cmds() {
 for cmd in "${CMD_ARRAY[@]}"
 do
  full_cmd=$cmd
  base_cmd=`echo $cmd | awk '{print $1}'`
  #echo "full[$full_cmd] base[$base_cmd]"
  dbecho "in cmd for loop [$cmd]"
  #echo "checking command-> $cmd"
  has_cmd $base_cmd
  if [ $? -eq 1 ]; then
   logerr 3 "`echo $cmd | awk '{print $1}'`"
   continue
  fi
  #echo "running-> $full_cmd"
  _run_cmd "$full_cmd"  
  if [ $? -eq 1 ]; then
   logerr 8 "`echo $cmd | awk '{print $1}'`"
   continue
  fi
 done
}

#this is the function to grab the workload file from
#nmsa, it takes one argument, the complete URI to the workload
get_workload() {
 in_file=$1
 out_file=$2
 ret=0
 tmp_proxy=$http_proxy  # we do this so any local proxy settings don't
 http_proxy=""          # screw up the wget
 wget $in_file -O $out_file &> /dev/null
 if [ ! $? -eq 0 ]; then
  logerr 2 $1
  ret=1;
 fi
 http_proxy=$tmp_proxy
 return $ret;
}
