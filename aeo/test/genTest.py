#!/usr/bin/python3
# genTest.py -- generates tests
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2020.06.30

import os
import sys
import re
import json
import time
import ntpath
import random
import argparse

pyPath=os.environ['EBSAF_ROOT'] + "/aeo/python"
sys.path.append(pyPath)

import simbaUtils
simbaUtils.readConfig()

designDir=simbaUtils.cfg['mdl'] + "/design"
path=os.walk(designDir)

parser=argparse.ArgumentParser()
parser.add_argument("N",
                    type=int,
                    help="Number of tests to generate.")
parser.add_argument("-m",
                    "--mode",
                    choices=['auto', 'manual'],
                    default=['manual'],
                    help="default is manual; \
                    if auto, service must be running.")

args=parser.parse_args()
numTests=args.N

reqTemplates=[]
inputFolders=[]

for root, directories, files in path:
  for file in files:
    if 'req' in file:
      reqTempPath = root + "/" + file 
      reqTemplates.append(reqTempPath) 

i = 0
while i < numTests:
    i += 1
    reqTemplate=random.choice(reqTemplates)
    jcfTemplate=re.sub("0.req", "1.jcf", reqTemplate)
    lstTemplate=re.sub("0.req", "1.lst", reqTemplate)

    head, tmplReqID=ntpath.split(reqTemplate)
    tmplReqID=re.sub(".req", '', tmplReqID)
    head, tmplLst=ntpath.split(lstTemplate)
    
    if (os.path.exists(jcfTemplate) and 
        os.path.exists(lstTemplate)):
        
      # generate uuid
      uuid=os.popen('uuid').read()
      uuid=uuid.rstrip()

      # generate filenames
      reqID=uuid + "_SD_" + "0000"
      jobID=uuid + "_SD_" + "0001"
      req=reqID + ".req"
      jcf=jobID + ".jcf"
      lst=jobID + ".lst"
      
      # create folder
      cmd=''
      if args.mode == 'auto':
        # create test input in input folder
        cmd = "mkdir " + simbaUtils.cfg['int'] + "/" + reqID
      else:
        # create test input in current directory
        cmd = "mkdir " +  reqID
      
      os.system(cmd)

      # copy reqTemplate to folder
      reqPath=''
      if args.mode == 'auto':
        # copy request file to input folder
        reqPath = simbaUtils.cfg['int'] + "/" + reqID + \
                  "/" + req
      else:
        reqPath = reqID + "/" + req
      cmd = "cp " + reqTemplate + " " + reqPath
      os.system(cmd)
      # replace IDs
      reqIn=open(reqPath, "rt")
      reqContent=reqIn.read()
      reqContent=reqContent.replace(tmplReqID, reqID)
      reqContent=reqContent.replace(tmplLst, lst)
      reqIn.close
      reqIn=open(reqPath, "wt")
      reqIn.write(reqContent)
      reqIn.close
      reqIn.flush()
      os.fsync(reqIn.fileno())
      
      # copy jcfTemplate to folder
      jcfPath=''
      if args.mode == 'auto':
        # copy request file to input folder
        jcfPath = simbaUtils.cfg['int'] + "/" + reqID + \
                  "/" + jcf
      else:
        jcfPath = reqID + "/" + jcf
      cmd = "cp " + jcfTemplate + " " + jcfPath
      os.system(cmd)
      # replace IDs
      jcfIn=open(jcfPath, "rt")
      jcfContent=jcfIn.read()
      jcfContent=jcfContent.replace(tmplReqID, reqID)
      jcfContent=jcfContent.replace(tmplLst, lst)
      jcfIn.close
      jcfIn=open(jcfPath, "wt")
      jcfIn.write(jcfContent)
      jcfIn.close
      jcfIn.flush()
      os.fsync(jcfIn.fileno())

      # copy lstTemplate to folder
      if args.mode == 'auto':
        # copy entry list to input folder
        lstPath = simbaUtils.cfg['int'] + "/" + reqID + \
                  "/" + lst
      else:
        lstPath = reqID + "/" + lst
      cmd = "cp " + lstTemplate + " " + lstPath
      os.system(cmd)

      # append folder created to list of input folders
      inputFolders.append(reqID)

    else:
      print("Config Error: Missing templates.")

if args.mode == 'auto':
  i=0;
  for input in inputFolders:
    input=input.rstrip()
    i=i+1
    print("\n-- Test", i, "of", args.N, "--")
    print("Submitting request:",input)
    print("Service response:")
    cmd="curl -X POST http://localhost:5000/v1/randomize/" \
         + input
    os.system(cmd)
    time.sleep(1)

  #check status
  print("\nWill check status after 10 seconds.")
  time.sleep(10)
  i=0
  for input in inputFolders:
    input=input.rstrip()
    i=i+1
    print("\n-- Result", i, "of", args.N,"--")
    print("Checking status of request:",input)
    print("Service response:")
    cmd="curl -X GET http://localhost:5000/v1/status/" \
        +input
    os.system(cmd)
    msg="\nIf response is \"queued\", manually check " + \
        "status with:"
    print(msg)
    print(cmd)
    time.sleep(1)

elif args.mode == 'manual':
  print("Generated:", numTests, "sample request(s).")
  exit()

