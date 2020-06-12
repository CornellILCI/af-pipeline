#!/usr/bin/python3
# statAnalysis.py -- handles stat analysis requests; creates
#   an sbatch script that runs the appropriate randomization
#   script; submits sbatch to SLURM; this is called from the
#   working directory.
# 
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2019.11.25

import os
import sys
import re
import json
import argparse

# get the value to the EBSAF_ROOT environment variable
# and append to the environment path

pyPath=os.environ['EBSAF_ROOT'] + "/aeo/python"
sys.path.append(pyPath)

import simbaUtils
import dbUtils

# read configuration file.
simbaUtils.readConfig()

# specify path for working directory
workPath=simbaUtils.cfg['wrd']

# get the input json from the command line
parser=argparse.ArgumentParser()
parser.add_argument("json",
                    type=str,
                    help="Path to input JSON file")

args=parser.parse_args()

# get JSON name as jobName
reqJSON=re.sub(".+\/",'',args.json)
reqName=re.sub(".JSON",'',reqJSON)
sbatchPath=re.sub(".JSON",".0.sh",args.json)
errLog=simbaUtils.cfg['lgd'] + "/" + reqName + ".err"
outLog=simbaUtils.cfg['lgd'] + "/" + reqName + ".out"
workDir=re.sub(reqJSON,'',args.json)
workDir=re.sub("\/$",'',workDir)
outDir=simbaUtils.cfg['out']

engine=''
sbatchTmpl=''
exec=''
params=''
tracker=simbaUtils.cfg['bin'] + "/" + "tracker.py "
trackOpt=''

with open(args.json, 'r') as j:
  request=j.read()

  obj=json.loads(request)

  # Get system bash
  bashDir='#!'
  bashDir=bashDir + simbaUtils.cfg['bsh']

  # Get method
  method=obj['metadata']['requestMethod']
  
  # Get parameters
  for j in obj['job'].keys():
    # Get jobNum, jobId
    jobName=obj['job'][j]['jobId']
    jobMeta=j + ": " + jobName 
    trackOpt=''
    trackOpt=reqName + ' -m new -j ' + jobName + ' -p 0' 
    track=tracker + trackOpt 
    exec=exec + '\n# ' + jobMeta + '\n' + track + '\nEXEC'
    track=tracker

    for p in obj['job'][j]['parameters'].keys():
      if 'executable' in p:
        exec=exec + obj['job'][j]['parameters'][p]
        trackOpt=reqName + ' -m update -j ' + jobName  
        track=track + trackOpt
        exec=exec + '\n' + track + '\n'
      else:
        val=obj['job'][j]['parameters'][p]
        params=params + \
          "--{0} {1} ".format(p,val)
  
  if 'asreml' in method:
    engine=simbaUtils.cfg['asm']
    sbatchTmpl='ASRL.TMPL'
    prefix=engine + " " + workDir + "/"
    exec=re.sub("EXEC", prefix, exec)
    params=''

    # Get input CSV/TXT/DAT file and check if it exists 
    # Abort if it is absent
  
  elif 'runSEA' in method:
    # TODO: "method" should be "engine"
    engine=simbaUtils.cfg['rd1'] + "/Rscript --vanilla "
    sbatchTmpl='SEA.TMPL'
    model=method + ".R"
    modelDir=simbaUtils.cfg['mdl'] + "/statAnalyses/asremlr"
    prefix=engine + modelDir + "/" + model
    exec=re.sub("EXEC", prefix, exec)
    # TODO:
    # if job==1,do not empty params
    # get the script executable
    # runSEA is too specific


  elif 'cgm' in method:
    print ("CGM")

  else:
    print("Unknown method")
    exit()
  
  cmd=exec + " " + params
  
  gz=simbaUtils.cfg['out'] + "/" + reqName + ".tar.gz"
  src=workDir 
  
  simbaUtils.getTemplate(sbatchTmpl)
  sbatch=simbaUtils.tmplContents
 
  # FILL TEMPLATE
  sbatch=re.sub("\[JOBNAME\]", reqName, sbatch)
  sbatch=re.sub("\[ERRORLOG\]", errLog, sbatch)
  sbatch=re.sub("\[OUTPUTLOG\]", outLog, sbatch)
  sbatch=re.sub("\[WRKNGDIR\]", workDir, sbatch)
  sbatch=re.sub("\[OUTDIR\]", outDir, sbatch)
  sbatch=re.sub("\[RUN\]", cmd, sbatch)
  sbatch=re.sub("\[SLTMPL\]", sbatchTmpl, sbatch)
  sbatch=re.sub("\[GZ\]", gz, sbatch)
  sbatch=re.sub("\[SRC\]", src, sbatch)

  # WRITE SBATCH
  sbatchFile=open(sbatchPath, 'w')
  sbatchFile.write(sbatch)
  sbatchFile.close()
  
  # TRACK/INITIALIZE
  track=simbaUtils.cfg['bin'] + "/" + "tracker.py" + \
    " " + args.json + " -m new -t SA"
  # print(track)
  # Comment out next line to debug.
  os.system(track)

  # SUBMIT TO QUEUE 
  # Comment out next line to debug.
  simbaUtils.queue(sbatchPath)

  # PRINT TO LOG
  simbaUtils.writeLog(simbaUtils.msg)
