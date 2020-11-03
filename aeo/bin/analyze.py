#!/usr/bin/python3
# analyze.py -- handles stat analyses requests; calculates
#   the number of jobs, creates an sbatch script that runs 
#   the appropriate analysis engine,submits sbatch to SLURM;
#   this is called from the working directory.
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2020.11.03

# Sprint 2020.11 Todo's
# prereq:
# * should have folder as input argument:
#     analyze.py 67ac2341-5cdc-45fd-a2fa-2bc17a2c_SA_0000
# * req should have elements that follow: 
# * asreml (engine) should be speficied

import os
import sys
import re
import json
import argparse

# get value of the EBSAF_ROOT environment variable
# and append to the environment path
pyPath=os.environ['EBSAF_ROOT'] + "/aeo/python"
sys.path.append(pyPath)

import simbaUtils
import dbUtils

# read configuration file.
simbaUtils.readConfig()

# specify path for the working directory
workPath=simbaUtils.cfg['int']

# set tracking, 1 = on, 0 = off
trackOn = 1

# get the input folder from the command line
# SG will write this folder in workDir

parser=argparse.ArgumentParser()
parser.add_argument("dir",
                    type=str,
                    help="Input folder")

args=parser.parse_args()

# generate path:
reqDir=workPath + "/" + args.dir 

# generate request filename
reqFile=args.dir + ".req" 
reqFile=reqDir + "/" + reqFile

# Generate output folder name
outFolder=reqDir

# Generate ouput prefix
# analysisName=args.dir
# jobName=analysisName[:-1]
# jobName=jobName + "1"

# Read job control file
try:
  with open(reqFile, 'r') as j:
    control=j.read()
    obj=json.loads(control)

    # Get system bash
    bashDir='#!'
    bashDir=bashDir + simbaUtils.cfg['bsh']

    # Get engine
    engine=obj['metadata']['engine']
    engine=re.sub(" ", "", engine)
    engine=re.sub("\.", "", engine)
    engine=(engine.lower())

    # Get model source (organization_code)
    source=obj['metadata']['organization_code']
    source=(source.lower())

    # Parse data and parameter objects
    # Calculate number of jobs given:
    # -trait_analysis_pattern
    # -exptLoc_analysis_pattern
    # -len(experiment_id)
    # -len(occurence_id)
    # -len(trait_id)
    # -len(response_variable_id)

    for p in obj['parameters'].keys():
      if p=='entryList':
        entPath=reqDir+ "/" + obj['parameters'][p]
        params=params + \
                "--{0} {1} ".format(p,entPath)
      else:
        params=params + \
               "--{0} {1} ".format(p,obj['parameters'][p])
  
    # Generate name for logs (.err and .out)
    errLog=simbaUtils.cfg['lgd'] + "/" + jobName \
           + ".err"
    outLog=simbaUtils.cfg['lgd'] + "/" + jobName \
           + ".out"

    # add new job to track
    trackOpt=args.dir + " -m addJob -j " + \
             jobName + " -p " + jobName 
    track=simbaUtils.cfg['bin'] + "/" + "track.py " + \
          trackOpt

    # command to run 
    cmd=RScript + params + "-o \"" + analysisName + \
        "\" -p \"" + outFolder + "\""

    # command to compress
    gz=simbaUtils.cfg['arch'] + "/" + analysisName \
       + ".tar.gz"
    src=outFolder
    out=simbaUtils.cfg['out'] + "/"

    # update job
    trackUpdOpt=args.dir + " -m updateJob -j " + jobName
    trackUpd=simbaUtils.cfg['bin'] + "/" + "track.py " + \
             trackUpdOpt
 
    # NEW: update analysis
    trackReqOpt=args.dir + " -m update"
    trackReq=simbaUtils.cfg['bin'] + "/" + "track.py " + \
             trackReqOpt

    # fill template
    simbaUtils.getTemplate("SLSD.TMPL")
    sbatch=simbaUtils.tmplContents
    sbatch=re.sub("\[JOBNAME\]", jobName, sbatch)
    sbatch=re.sub("\[ERRORLOG\]", errLog, sbatch)
    sbatch=re.sub("\[OUTPUTLOG\]", outLog, sbatch)
    sbatch=re.sub("\[RUN\]", cmd, sbatch)
    sbatch=re.sub("\[GZ\]", gz, sbatch)
    sbatch=re.sub("\[INP\]", workPath, sbatch)
    sbatch=re.sub("\[REQ\]", args.dir, sbatch)
    sbatch=re.sub("\[SRC\]", src, sbatch)
    sbatch=re.sub("\[OUT\]", out, sbatch)

    if trackOn:
      sbatch=re.sub("\[TRACKNEW\]", track, sbatch)
      sbatch=re.sub("\[TRACKUPD\]", trackUpd, sbatch)
      sbatch=re.sub("\[TRACKREQ\]", trackReq, sbatch)
    else:
      sbatch=re.sub("\[TRACKNEW\]", '', sbatch)
      sbatch=re.sub("\[TRACKUPD\]", '', sbatch)
      sbatch=re.sub("\[TRACKREQ\]", '', sbatch)
  
    # print(sbatch) # comment this out

    # write sbatch
    sbatchPath=outFolder + "/" + jobName + ".sh"
    sbatchFile=open(sbatchPath, 'w')
    sbatchFile.write(sbatch)
    sbatchFile.close()

    # Track analysis: submitted to the queue 
    if trackOn:
      track=simbaUtils.cfg['bin'] + "/" + "track.py " + \
            args.dir + " -m new -s queued"
      os.system(track)

    simbaUtils.queue(sbatchPath)

    # Print this to log or track this.
    simbaUtils.writeLog(simbaUtils.msg)

except ValueError:
  # track error parsing jcf
  track=simbaUtils.cfg['bin'] + "/" + "track.py " + \
        args.dir + " -m new -s fail"
  os.system(track)

  # update
  track=simbaUtils.cfg['bin'] + "/" + "track.py " + \
        args.dir + " -m update -status fail"
  os.system(track)

  # Should return message: "Fail to read job control file."?
