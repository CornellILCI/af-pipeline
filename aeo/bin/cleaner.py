#!/usr/bin/python3
# cleaner.py -- deletes old empty  *.err and *.out files in 
#               the log directory 
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2019.10.21

# This is not yet fully implemented yet

import os
import sys
import re
from datetime import datetime, timedelta

pyPath=os.environ['EBSAF_ROOT'] + "/aeo/python"

sys.path.append(pyPath)

import simbaUtils

simbaUtils.readConfig()
logPath=simbaUtils.cfg['lgd']
outPath=simbaUtils.cfg['out']

# print(logPath)
# print(outPath)

n=1
files=[]
folders=[]
monthAgo=datetime.now() - timedelta(days=1)

# delete slurm log files that are a month old
for r, d, f in os.walk(logPath):
  for file in f:
    # Ignore simba.LOG and README
    if not '.LOG' in file and not 'README' in file:
      files.append(os.path.join(r,file))

for f in files:
  ftime=datetime.fromtimestamp(os.stat(f).st_mtime)
  
  # print (f, "\t", ftime, "\t", monthAgo)

  if ftime < monthAgo:
    # delete files older than a month
    cmd="rm -fr " + f
    os.system(cmd)
    print(f, "\t", ftime)

# delete folders that are a month old.
for r, d, f in os.walk(outPath):
  for dir in d:
    if '_SD_0000' in dir:
      folders.append(os.path.join(r,dir))

for d in folders:
  dtime=datetime.fromtimestamp(os.stat(d).st_mtime)
 
  # print(d,"\t", dtime)

  if dtime < monthAgo:
    # delete folders older than a month
    cmd="rm -fr " + d
    os.system(cmd)
    print(d, "\t", dtime)
