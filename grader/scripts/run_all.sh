#!/bin/sh
SCRIPTDIR=$(dirname $(readlink -f $0))
if [ "$#" -ne 2 ]; then
  echo "Expected 2 command line arguments: (1) the directory with student submissions; (2) the script file to run student submissions with."
  exit 1
fi
for student in $1/*
do
  rm -f 2>/dev/null $student/condor.out
  rm -f 2>/dev/null $student/condor.log
  rm -f 2>/dev/null $student/condor.err
  condor_submit -append "student=$student" -append "script=$2" $SCRIPTDIR/hw.cmd
done
