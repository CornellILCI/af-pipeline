#!/usr/bin/python3
# tracker.py -- tracks submission to AF
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2019.11.26

import os
import sys
import re
import argparse

pyPath=os.environ['EBSAF_ROOT'] + "/aeo/python"
sys.path.append(pyPath)

import simbaUtils
import dbUtils

parser=argparse.ArgumentParser()

parser.add_argument("name", 
                    type=str,
                    help="analysis to track")
parser.add_argument("-t",
                    "--type",
                    choices=['SD','SA'],
                    help="request type (stat design, 'SD' \
                    or stat analysis, 'SA'")
parser.add_argument("-j",
                    "--job",
                    help="job name to track")
parser.add_argument("-m",
                    "--mode",
                    choices=['n','new','u','update'],
                    default=['new'],
                    help="track mode: new, n or \
                    update, u; default: new")
parser.add_argument("-p","--parent_id",
                    default='',
                    help="parent job ID; \
                    required for -m new option")

args=parser.parse_args()

if args.mode == 'new' or args.mode == 'n':
  if args.job:
    if args.parent_id != '':
      dbUtils.getAnalysisId(args.name, 0)
      analysisId=dbUtils.analysisId
      if analysisId:
        dbUtils.addJob(analysisId, args.job, args.parent_id)
      else:
        # LOG THIS
        msg="Cannot find analysis: {}".format(args.name)
        simbaUtils.writeLog(msg)
    else:
      # LOG THIS
      msg="Parent id needed for " 
      msg=msg + "new job: {}".format(args.job)
      simbaUtils.writeLog(msg)
  else:
    if args.type:
      # get sha of args.name:
      simbaUtils.genShaFile(args.name)
      sha=simbaUtils.strSha

      if re.match("JSON", args.name):
        analysisName=re.sub(".JSON",'',args.name)
      else:
        analysisName=re.sub(".req",'',args.name)

      analysisName=re.sub(".+\/",'',analysisName.rstrip())
      
      dbUtils.addAnalysis(analysisName, sha, args.type)
    else:
      # LOG THIS
      msg="Needed request type for " 
      msg=msg + "analysis: {}".format(args.name)
      simbaUtils.writeLog(msg)
elif args.mode == 'update' or args.mode == 'u':
  if args.job:

    # get the status
    simbaUtils.getJobStat(args.name)
    status=simbaUtils.jobStat 
    
    if status:
      # get error message
      simbaUtils.getErrMsg(args.job)
      message=simbaUtils.errMsg
      dbUtils.updateJob(args.job, status, message)
    else:
      # LOG THIS
      msg="Unknown error(100) for: {}".format(args.job)
      simbaUtils.writeLog(msg)
  else:
    # LOG THIS
    msg="Missing job name to update!"
    simbaUtils.writeLog(msg)
    # print("Missing job name to update!")
else:
  # LOG THIS
  msg="Unknown error(10)!"
  simbaUtils.writeLog(msg)
