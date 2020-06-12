#!/usr/bin/python3
# statDesign.py -- handles stat design requests; creates an 
#   sbatch script that runs the appropriate randomization 
#   script; submits sbatch to SLURM; this is called from the
#   working directory.
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2019.10.01

# Sprint 2020.06 Todo's
# * pyPath should use EBSAF_ROOT
# * should have folder as input argument:
#     statDesign.py 202341-2342-21231_SD_0000
# * prereq: req/jcf should have elements that follow 
#     repository structure for identifying path to models,
#     for irri:  
#        EBSAF_ROOT/models/design/irri/randomization
#     for cimmyt:
#        EBSAF_ROOT/models/design/cimmyt/randomization
# * r-version should be speficied
#     add rversion in conf: r344=<path> r400=<path

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
workPath=simbaUtils.cfg['wrd']

# get the input json from the command line
parser=argparse.ArgumentParser()
parser.add_argument("json",
                    type=str,
                    help="Input JSON file")

args=parser.parse_args()

# Generate output folder name
outFolder=re.sub(".JSON",'',args.json)

# Generate ouput prefix
analysisName=outFolder
analysisName=re.sub(".+\/",'',analysisName.rstrip())
jobName=analysisName + ".0"

with open(args.json, 'r') as j:
  request=j.read()

  obj=json.loads(request)

  # Get system bash
  bashDir='#!'
  bashDir=bashDir + simbaUtils.cfg['bsh']

  # Get the r executable and rscript
  # Should check if "model" exists
  RScript=simbaUtils.cfg['rd1'] + "/Rscript --vanilla "
  RScript=RScript + simbaUtils.cfg['mdl'] + "/statDesign/" \
          + obj['metadata']['requestMethod']
  RScript=RScript + ".R "
  
  # Get parameters
  params=''  

  for p in obj['parameters'].keys():
    params=params + \
           "--{0} {1} ".format(p,obj['parameters'][p])
  
  # Create output folder
  cmd="mkdir {}".format(outFolder)
  os.system(cmd)
  
  # Move .JSON file inside output folder
  # change "cp" to "mv" bellow
  cmd="mv {0} {1}".format(args.json, outFolder)
  os.system(cmd)

  # logs
  errLog=simbaUtils.cfg['lgd'] + "/" + analysisName + ".err"
  outLog=simbaUtils.cfg['lgd'] + "/" + analysisName + ".out"

  # add new job to track
  trackOpt=" " + analysisName + " -m new -j " + jobName + \
           " -p 0"
  track=simbaUtils.cfg['bin'] + "/" + "tracker.py" + \
        trackOpt

  # command to run 
  cmd=RScript + params + "-o \"" + analysisName + \
      "\" -p \"" + outFolder + "\""

  # command to compress
  gz=simbaUtils.cfg['out'] + "/" + analysisName + ".tar.gz"
  #src=outFolder + "/" + analysisName
  src=outFolder

  # update
  trackUpdOpt=" " + analysisName + " -m update -j " + \
              jobName
  trackUpd=simbaUtils.cfg['bin'] + "/" + "tracker.py" + \
           trackUpdOpt 

  # fill template
  simbaUtils.getTemplate("SLSD.TMPL")
  sbatch=simbaUtils.tmplContents
  sbatch=re.sub("\[JOBNAME\]", jobName, sbatch)
  sbatch=re.sub("\[ERRORLOG\]", errLog, sbatch)
  sbatch=re.sub("\[OUTPUTLOG\]", outLog, sbatch)
  sbatch=re.sub("\[TRACKNEW\]", track, sbatch)
  sbatch=re.sub("\[RUN\]", cmd, sbatch)
  sbatch=re.sub("\[GZ\]", gz, sbatch)
  sbatch=re.sub("\[SRC\]", src, sbatch)
  sbatch=re.sub("\[TRACKUPD\]", trackUpd, sbatch)
  # print(sbatch)

  # write sbatch
  sbatchPath=outFolder + "/" + jobName + ".sh"
  sbatchFile=open(sbatchPath, 'w')
  sbatchFile.write(sbatch)
  sbatchFile.close()

  # Track analysis or add this to sbatch?
  reqJSON=outFolder + "/" + analysisName + ".JSON"
  track=simbaUtils.cfg['bin'] + "/" + "tracker.py" + \
       " " +  reqJSON  + " " + "-m new -t SD"
  os.system(track)

  simbaUtils.queue(sbatchPath)

  # Print this to log or track this.
  simbaUtils.writeLog(simbaUtils.msg)
