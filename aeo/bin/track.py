#!/usr/bin/python3
# track.py -- tracks submission to AF;
#             code from tracker.py
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2020.07.16

import os
import sys
import re
import argparse

pyPath=os.environ['EBSAF_ROOT'] + "/aeo/python"
sys.path.append(pyPath)

import simbaUtils
import dbUtils

parser=argparse.ArgumentParser()

parser.add_argument("reqID", 
                    type=str,
                    help="request to track")
parser.add_argument("-m",
                    "--mode",
                    choices=['new','update', 'addJob', 
                             'updateJob'],
                    help="new (new reqID), \
                          update (update status of reqID), \
                          addJob (add job to reqID), \
                          updateJob (update status of job)")
parser.add_argument("-s",
                    "--status",
                    choices=['queued', 'failed'],
                    help="status of reqID: queued or failed")
parser.add_argument("-j",
                    "--jobID",
                    type=str,
                    help="id of job to add/update")
parser.add_argument("-p",
                    "--parent",
                    type=str,
                    help="parent jobID; \
                          required for -m addJob")

args=parser.parse_args()

# read config
simbaUtils.readConfig()

if args.reqID:
  if args.mode == 'new':
    if args.status:
      # get request type
      reqType=re.sub("_0000",'',args.reqID)
      reqType=re.sub(".+?\_",'',reqType)

      # no need to check if it exists
      # generate sha for the request
      # get req path
      reqPath=simbaUtils.cfg['int'] + "/" + args.reqID \
              + "/" + args.reqID + ".req"
      if os.path.exists(reqPath):
        simbaUtils.genShaFile(reqPath)
        sha=simbaUtils.strSha
        dbUtils.addAnalysis(args.reqID, sha,
                            reqType, args.status)
      else:
        print("File does not exists:", reqPath)
    else:
      print("Please supply status: queued or failed!")

  elif args.mode == 'update':

    # get status of all jobs from the request, if all
    # are successful, update status to success!

    dbUtils.getAnalysisId(args.reqID, 0)
    analysisId=dbUtils.analysisId
    
    dbUtils.updateAnalysis(analysisId)
    
  elif args.mode == 'addJob':

    if args.jobID and args.parent:

      # get requestID
      dbUtils.getAnalysisId(args.reqID, 0)
      reqID_exists=dbUtils.analysisId

      # generate parentID
      if args.jobID == args.parent:
        parentID=0
      else:
        dbUtils.getJobId(args.parent)
        parentID=dbUtils.jobId
      
      if reqID_exists:
        dbUtils.addJob(reqID_exists,args.jobID,parentID)
      else:
        msg="Cannot find request: {}".format(args.reqID)
        simbaUtils.writeLog(msg)
  
    else:
      print("Please supply jobID and parent!")

  elif args.mode == 'updateJob':

    if args.jobID:

      # get job status:
      # 0: fail
      # 100: complete
      # 101: complete with err msg
      # 110: complete with out msg
      # 111: complete with err and out msg
      
      msg=''
      
      simbaUtils.getJobStat(args.jobID)
      status=simbaUtils.jobStat
      
      # get err/out msg 
      if (status != 0) and (status != 100):
          # get message
          simbaUtils.getErrMsg(args.jobID,status)
          msg=simbaUtils.errMsg

      # update job
      dbUtils.updateJob(args.jobID,status,msg) 

    else:
      print("Please supply jobID to update!")
  else:
    print("Needs more argument!")
