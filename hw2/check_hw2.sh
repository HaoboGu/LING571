#!/bin/bash
GRADER_SCRIPT="/mnt/dropbox/17-18/571/grader/src/check_hw.py"
LANGUGAGE_FILE="/dropbox/17-18/571/languages"
SUBMIT_FILE_LIST="/dropbox/17-18/571/hw2/submit-file-list"
# HW_FILE_NAME="hw1.tar.gz"
if [ -z "$1" ]; then
	echo "Usage: check_hw1.sh \$HW_FILE_PATH"
else
	/usr/bin/env python2.7 $GRADER_SCRIPT $LANGUGAGE_FILE $SUBMIT_FILE_LIST "$1"
fi
