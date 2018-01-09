#!/bin/sh
SCRIPTDIR=$(dirname $(readlink -f $0))
python $SCRIPTDIR/../src/grader57x/grader.py $@