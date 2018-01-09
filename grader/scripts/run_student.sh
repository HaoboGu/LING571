#!/bin/sh
SCRIPTDIR=$(dirname $(readlink -f $0))
if [ "$#" -ne 2 ]; then
  echo "Expected 2 command line arguments: (1) the full path to the particular student's directory; (2) the script file to run student submissions with."
  exit 1
fi
rm -f 2>/dev/null $1/condor.out
rm -f 2>/dev/null $1/condor.log
rm -f 2>/dev/null $1/condor.err
condor_submit -append "student=$1" -append "script=$2" $SCRIPTDIR/hw.cmd
