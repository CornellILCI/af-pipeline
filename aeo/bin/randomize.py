#!/usr/bin/python3
# randomize.py -- handles stat design requests; creates an
#   sbatch script that runs the appropriate randomization
#   script; submits sbatch to SLURM; this is called from the
#   working directory.
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2019.10.01

# Sprint 2020.06 Todo's
# prereq:
# * should have folder as input argument:
#     randomize.py 202341-2342-21231_SD_0000
# * req/jcf should have elements that follow
#     repository structure for identifying path to models,
#     for irri:
#        EBSAF_ROOT/models/design/irri/randomization
#     for cimmyt:
#        EBSAF_ROOT/models/design/cimmyt/randomization
# * r-version (engine) should be speficied
#     add rversion in conf: r344=<path> r400=<path

import os
import sys
import re
import json
import argparse

# get value of the EBSAF_ROOT environment variable
# and append to the environment path
pyPath = os.environ["EBSAF_ROOT"] + "/aeo/python"
sys.path.append(pyPath)

import simbaUtils
import dbUtils

# read configuration file.
simbaUtils.readConfig()

# specify path for the working directory
workPath = simbaUtils.cfg["int"]

# set tracking, 1 = on, 0 = off
trackOn = 1

# get the input folder from the command line
# SG will write this folder in workDir

parser = argparse.ArgumentParser()
parser.add_argument("dir", type=str, help="Input folder")

args = parser.parse_args()

# generate path:
reqDir = workPath + "/" + args.dir

# generate job control file
reqJcf = args.dir[:-1]
reqJcf = reqJcf + "1" + ".jcf"
reqJcf = reqDir + "/" + reqJcf

# Generate output folder name
outFolder = reqDir

# Generate ouput prefix
analysisName = args.dir
jobName = analysisName[:-1]
jobName = jobName + "1"

# Read job control file
try:
    with open(reqJcf, "r") as j:
        control = j.read()
        obj = json.loads(control)

        # Get system bash
        bashDir = "#!"
        bashDir = bashDir + simbaUtils.cfg["bsh"]

        # Get engine
        engine = obj["metadata"]["engine"]
        engine = re.sub(" ", "", engine)
        engine = re.sub("\.", "", engine)
        engine = engine.lower()

        # Get model source (organization_code)
        source = obj["metadata"]["organization_code"]
        source = source.lower()

        # Generate path to randomization script
        # should check if "model" exists
        RScript = simbaUtils.cfg[engine] + "/Rscript --vanilla "
        RScript = RScript + simbaUtils.cfg["mdl"] + "/design/" + source + "/randomization/" + obj["metadata"]["method"]
        RScript = RScript + ".R "

        # Get parameters
        params = ""

        for p in obj["parameters"].keys():
            if p == "entryList":
                entPath = reqDir + "/" + obj["parameters"][p]
                params = params + "--{0} {1} ".format(p, entPath)
            else:
                params = params + "--{0} {1} ".format(p, obj["parameters"][p])

        # Generate name for logs (.err and .out)
        errLog = simbaUtils.cfg["lgd"] + "/" + jobName + ".err"
        outLog = simbaUtils.cfg["lgd"] + "/" + jobName + ".out"

        # add new job to track
        trackOpt = args.dir + " -m addJob -j " + jobName + " -p " + jobName
        track = simbaUtils.cfg["bin"] + "/" + "track.py " + trackOpt

        # command to run
        cmd = RScript + params + '-o "' + analysisName + '" -p "' + outFolder + '"'

        # command to compress
        gz = simbaUtils.cfg["arch"] + "/" + analysisName + ".tar.gz"
        src = outFolder
        out = simbaUtils.cfg["out"] + "/"

        # update job
        trackUpdOpt = args.dir + " -m updateJob -j " + jobName
        trackUpd = simbaUtils.cfg["bin"] + "/" + "track.py " + trackUpdOpt

        # NEW: update analysis
        trackReqOpt = args.dir + " -m update"
        trackReq = simbaUtils.cfg["bin"] + "/" + "track.py " + trackReqOpt

        # fill template
        simbaUtils.getTemplate("SLSD.TMPL")
        sbatch = simbaUtils.tmplContents
        sbatch = re.sub("\[JOBNAME\]", jobName, sbatch)
        sbatch = re.sub("\[ERRORLOG\]", errLog, sbatch)
        sbatch = re.sub("\[OUTPUTLOG\]", outLog, sbatch)
        sbatch = re.sub("\[RUN\]", cmd, sbatch)
        sbatch = re.sub("\[GZ\]", gz, sbatch)
        sbatch = re.sub("\[INP\]", workPath, sbatch)
        sbatch = re.sub("\[REQ\]", args.dir, sbatch)
        sbatch = re.sub("\[SRC\]", src, sbatch)
        sbatch = re.sub("\[OUT\]", out, sbatch)

        if trackOn:
            sbatch = re.sub("\[TRACKNEW\]", track, sbatch)
            sbatch = re.sub("\[TRACKUPD\]", trackUpd, sbatch)
            sbatch = re.sub("\[TRACKREQ\]", trackReq, sbatch)
        else:
            sbatch = re.sub("\[TRACKNEW\]", "", sbatch)
            sbatch = re.sub("\[TRACKUPD\]", "", sbatch)
            sbatch = re.sub("\[TRACKREQ\]", "", sbatch)

        # print(sbatch) # comment this out

        # write sbatch
        sbatchPath = outFolder + "/" + jobName + ".sh"
        sbatchFile = open(sbatchPath, "w")
        sbatchFile.write(sbatch)
        sbatchFile.close()

        # Track analysis: submitted to the queue
        if trackOn:
            track = simbaUtils.cfg["bin"] + "/" + "track.py " + args.dir + " -m new -s queued"
            os.system(track)

        simbaUtils.queue(sbatchPath)

        # Print this to log or track this.
        simbaUtils.writeLog(simbaUtils.msg)

except ValueError:
    # track error parsing jcf
    if trackOn:
        track = simbaUtils.cfg["bin"] + "/" + "track.py " + args.dir + " -m new -s fail"
        os.system(track)

        # update
        track = simbaUtils.cfg["bin"] + "/" + "track.py " + args.dir + " -m update -status fail"
        os.system(track)

        # Should return message: "Fail to read job control file."?
