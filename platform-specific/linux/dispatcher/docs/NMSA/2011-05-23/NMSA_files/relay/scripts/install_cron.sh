CRONCOMMFILE=/tmp/cron_comm_file.sh
CRONGREP=`crontab -l | grep relay.sh`

if [ "$CRONGREP" != "" ]; then
 echo "Crontab already exists"
 exit 
fi

# Create command file to create crontab file
if [ -f $CRONCOMMFILE ]; then
  rm -f $CRONCOMMFILE
fi

CRONLINE="* * * * * sh /opt/intel/eil/relay/bin/relay.sh >> /tmp/relay.log 2>/tmp/relay.bash.out"

# Added commands into the file to create the crontab entry
echo "#!/bin/sh" >> $CRONCOMMFILE
echo "EDITOR=ed" >> $CRONCOMMFILE
echo "export EDITOR" >> $CRONCOMMFILE

echo "crontab -e << EOF > /dev/null" >> $CRONCOMMFILE
echo "a" >> $CRONCOMMFILE
echo "$CRONLINE" >> $CRONCOMMFILE
echo "." >> $CRONCOMMFILE
echo "w" >> $CRONCOMMFILE
echo "q" >> $CRONCOMMFILE
echo "EOF" >> $CRONCOMMFILE

chmod 750 $CRONCOMMFILE

# Execute the the crontab command file
if [ -f $CRONCOMMFILE ]; then
  $CRONCOMMFILE
  rm $CRONCOMMFILE
else
  echo "Error: File generated to create crontab entry does not exist"
  exit 1
fi

echo "Crontab Entry Inserted Successfully"

