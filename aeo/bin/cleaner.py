#!/usr/bin/python3
# cleaner.py -- deletes old empty  *.err and *.out files in
#               the log directory
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2019.10.21

# This is not yet fully implemented yet

import os
import re
import sys
import math
from datetime import date, datetime, timedelta

pyPath = os.environ["EBSAF_ROOT"] + "/aeo/python"

sys.path.append(pyPath)

import simbaUtils

simbaUtils.readConfig()
intPath = simbaUtils.cfg["int"]  # input
logPath = simbaUtils.cfg["lgd"]  # log
outPath = simbaUtils.cfg["out"]  # output
archPath = simbaUtils.cfg["arch"]  # archive

n = 0  # number of old files to delete
t = 0  # total number of files
a = int(simbaUtils.cfg["age"])  # age of file to delete
filesN = int(simbaUtils.cfg["set"])  # N of files/folder

files = []
folders = []
monthAgo = datetime.now() - timedelta(days=a)

# delete slurm log files that are a days old
for r, d, f in os.walk(logPath):
    for file in f:
        # Ignore simba.LOG and README
        if not ".LOG" in file and not "README" in file:
            files.append(os.path.join(r, file))

for f in files:
    ftime = datetime.fromtimestamp(os.stat(f).st_mtime)
    t = t + 1
    if ftime < monthAgo:
        n = n + 1
        # delete files older than a a days
        cmd = "rm -fr " + f
        os.system(cmd)

if n:
    msg = "cleaner.py: deleted {0} of ".format(n) + "{0} slurm log files older than ".format(t) + "{0} days.".format(a)
    simbaUtils.writeLog(msg)

n = 0
t = 0
folders = []

# delete folders in input that are a days old.
for r, d, f in os.walk(intPath):
    for dir in d:
        if "_0000" in dir:
            folders.append(os.path.join(r, dir))

for d in folders:
    dtime = datetime.fromtimestamp(os.stat(d).st_mtime)
    t = t + 1
    if dtime < monthAgo:
        # delete folders older than a d days
        n = n + 1
        cmd = "rm -fr " + d
        os.system(cmd)

if n:
    msg = (
        "cleaner.py: deleted {0} of ".format(n)
        + "{0} folders in input that are older ".format(t)
        + "than {0} days.".format(a)
    )
    simbaUtils.writeLog(msg)

n = 0
t = 0
folders = []

# delete folders in output  that are a days old.
for r, d, f in os.walk(outPath):
    for dir in d:
        if "_0000" in dir:
            folders.append(os.path.join(r, dir))

for d in folders:
    dtime = datetime.fromtimestamp(os.stat(d).st_mtime)
    t = t + 1
    if dtime < monthAgo:
        # delete folders older than a d days
        n = n + 1
        cmd = "rm -fr " + d
        os.system(cmd)

if n:
    msg = (
        "cleaner.py: deleted {0} of ".format(n)
        + "{0} folders in output  that are older ".format(t)
        + "than {0} days.".format(a)
    )
    simbaUtils.writeLog(msg)

n = 0
t = 0
files = []

# organize archive in folders with filesN files each.
for r, d, f in os.walk(archPath):
    for file in f:
        if "tar.gz" in file:
            files.append(os.path.join(r, file))
    break

for f in files:
    t = t + 1

if t >= filesN:
    nFolders = math.trunc(t / filesN)
    archFolders = []
    i = 0
    while i < nFolders:
        simbaUtils.genFolderName()
        fPath = archPath + "/" + simbaUtils.folderName
        # create folder
        cmd = "mkdir {0}".format(fPath)
        os.system(cmd)
        archFolders.append(fPath)
        i = i + 1
    i = 0
    c = 1
    for f in files:
        dest = archFolders[i]
        if c > filesN:
            c = 1
            i = i + 1
            if i == nFolders:
                break
            else:
                dest = archFolders[i]

        cmd = "mv {0} {1}".format(f, dest)
        os.system(cmd)
        c = c + 1

    msg = "cleaner.py: {0}".format(t) + " files moved into {0} folder(s).".format(nFolders)
    simbaUtils.writeLog(msg)
