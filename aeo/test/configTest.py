#!/usr/bin/python3
# configTest.py -- Tests pysimba configuration
#                  and automatically runs tests.

# 1. Reads simba.conf and checks if the directories are 
#    accessible and have appropriate read/write permission.
# 2. Check SLURM status. 
# 2. Generates control JSON files and runs reaper.py 
# 3. Checks for output and logs.
# 4. Generates a message regarding the status of the 
#    test.

import os
import sys
import re

pyPath=''

if os.getenv('PYSIMBA_ROOT'):
  pyPath=os.environ['PYSIMBA_ROOT'] + "/python"
else:
  print("PYSIMBA_ROOT environment variable not set!")
  exit()

sys.path.append(pyPath)

import simbaUtils
import dbUtils

simbaUtils.readConfig



