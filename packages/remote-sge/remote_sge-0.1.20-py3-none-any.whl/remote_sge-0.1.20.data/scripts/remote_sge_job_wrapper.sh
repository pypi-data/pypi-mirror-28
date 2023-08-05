#!/bin/bash

# Purpose of this script is to wait for completion of the wrapped
# script, and then make a tarfile of the results.

# Call this script with the same arguments that would be
# given to the actual command.
# 

Running it with client certificates
The problem is that
* You have to 


echo FART
SCRIPT=/home/tgannon/sleeper.sh
ARCHIVE_DIR=/home/tgannon
$SCRIPT master blaster
SCRIPT_EXIT=$?
sleep 5

if [ $SCRIPT_EXIT -le 10000 ]; then
  echo "Script exited successfully with $SCRIPT_EXIT."
  echo "Archiving to $ARCHIVE_DIR/$JOB_ID.tgz"
  tar -cvzf $ARCHIVE_DIR/$JOB_ID.tgz * 1> /dev/null
else
  echo "Script exited with $SCRIPT_EXIT.  Please have a look."
fi

exit $SCRIPT_EXIT
