#!/usr/bin/python3
# cleaner.py -- deletes old empty  *.err and *.out files in 
#               the log directory 
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2019.10.21

import os
import sys
import re
from datetime import datetime, timedelta

pyPath=os.environ['PYSIMBA_ROOT'] + "/python"

sys.path.append(pyPath)

import simbaUtils

simbaUtils.readConfig()
logPath=simbaUtils.cfg['lgd']

print(logPath)

files=[]

for r, d, f in os.walk(logPath):
  for file in f:
    if not '.LOG' in file and not 'README' in file:
      files.append(os.path.join(r,file))

for f in files:
  fsize=os.stat(f).st_size
  monthAgo=datetime.now() - timedelta(days=30)
  ftime=datetime.fromtimestamp(os.stat(f).st_mtime)
  
  if ftime < monthAgo:
    # delete files older than a month
    print(f, fsize, monthAgo)
