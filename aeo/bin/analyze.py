#!/usr/bin/python3
# analyze.py -- handles stat analyses requests using asreml
#   as the engine; calculates number of jobs from the
#   parameters given in the request. Creates an sbatch
#   script that will calls the appropriate dpo.
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2020.11.11

import os
import sys
import re
import json
import argparse

# get value of EBSAF_ROOT environment variable
# and append to the environment path
pyPath = os.environ["EBSAF_ROOT"] + "/aeo/python"
sys.path.append(pyPath)

import simbaUtils
import dbUtils

# read configuration file
simbaUtils.readConfig()

# specify path for the working directory
workPath = simbaUtils.cfg["int"]

# set tracking, 1 = on, 0 = off
trackOn = 0

# get the input folder from the command line
# SG will write this folder in workDir

parser = argparse.ArgumentParser()
parser.add_argument("dir", type=str, help="Input folder")

args = parser.parse_args()

# generate path:
reqPath = workPath + "/" + args.dir
reqFile = reqPath + "/" + args.dir + ".req"

try:
    with open(reqFile, "r") as j:
        request = j.read()
        obj = json.loads(request)

        # Get system bash
        bashDir = "#!"
        bashDir = bashDir + simbaUtils.cfg["bsh"]

        # Get engine, remove version, make all lower case
        engine = obj["metadata"]["engine"]
        engine = re.sub("-.*", "", engine)
        engine = engine.lower()

        # Get value of trait_analysis_pattern and
        # establish value of nRespVar
        nRespVar = 0

        if obj["parameters"]["trait_analysis_pattern"] != 2:

            # Get number of jobs, needs:
            #   exptloc_analysis_pattern,
            #   trait_analysis_pattern,
            #   len(experiment_id),
            #   len(occurence_id),
            #   len(trait_id),
            #   nRespVar

            expLocAnPat = obj["parameters"]["exptloc_analysis_pattern"]
            trtAnPat = obj["parameters"]["trait_analysis_pattern"]
            nExp = len(obj["data"]["experiment_id"])
            nOcc = len(obj["data"]["occurrence_id"])
            nTrt = len(obj["data"]["trait_id"])

            # Get number of jobs:
            simbaUtils.getNjobs(expLocAnPat, trtAnPat, nExp, nOcc, nTrt, nRespVar)

            nJobs = simbaUtils.nJobs
            jobID = args.dir
            jobErr = args.dir + ".err"
            jobOut = args.dir + ".out"
            dpo = simbaUtils.cfg["dpo"] + "/bin/dpo.py"

            # Generate dpo's jobID is 1
            dpoJobID = re.sub("0000", "1000", args.dir)

            # Generate path to tracker
            track = simbaUtils.cfg["bin"] + "/" + "track.py"

            # Generate track option for dpo:
            trackOptAdd = args.dir + " -m addJob -j " + dpoJobID + " -p " + dpoJobID
            trackOptUpd = args.dir + " -m updateJob -j " + dpoJobID

            logPath = simbaUtils.cfg["lgd"]
            errFile = " 2> " + logPath + "/" + dpoJobID + ".err"
            outFile = " > " + logPath + "/" + dpoJobID + ".out"

            if trackOn:
                run = track + " " + trackOptAdd + "\n" + dpo + " " + args.dir + "\n" + track + " " + trackOptUpd + "\n"
            else:
                run = dpo + " " + args.dir + "\n"

            i = 1
            while i <= nJobs:
                sfx = 1000 + i
                reqName = re.sub("0000.req", "", reqFile)

                # SLURM Related
                jobName = re.sub(".+\/", "", reqName)
                jobName = jobName + "{}".format(sfx)
                trackOptAdd = args.dir + " -m addJob -j " + jobName + " -p " + jobName
                trackOptUpd = args.dir + " -m updateJob -j " + jobName

                # stdout & stderr managements
                errFile = " 2> " + logPath + "/" + jobName + ".err"
                outFile = " > " + logPath + "/" + jobName + ".out"

                # ASREML Related
                reqAs = reqName + "{}".format(sfx) + ".as"
                reqCsv = reqName + "{}".format(sfx) + ".csv"
                if trackOn:
                    run = (
                        run
                        + track
                        + " "
                        + trackOptAdd
                        + "\n"
                        + engine
                        + " "
                        + reqAs
                        + " "
                        + reqCsv
                        + " "
                        + outFile
                        + " "
                        + errFile
                        + "\n"
                        + track
                        + " "
                        + trackOptUpd
                        + "\n"
                    )
                else:
                    run = run + engine + " " + reqAs + " " + reqCsv + " " + outFile + " " + errFile + "\n"
                i = i + 1

        else:
            print("Get number of response variable!")

        # fill template
        out = simbaUtils.cfg["out"] + "/"
        gz = simbaUtils.cfg["arch"] + "/" + args.dir + ".tar.gz"
        src = simbaUtils.cfg["int"] + "/" + args.dir
        trackReq = track + " " + args.dir + " -m update"

        simbaUtils.getTemplate("ASRL.TMPL")
        sbatch = simbaUtils.tmplContents
        sbatch = re.sub("\[JOBNAME\]", jobID, sbatch)
        sbatch = re.sub("\[ERRORLOG\]", jobErr, sbatch)
        sbatch = re.sub("\[OUTPUTLOG\]", jobOut, sbatch)
        sbatch = re.sub("\[WRKNGDIR\]", reqPath, sbatch)
        sbatch = re.sub("\[RUN\]\n", run, sbatch)
        sbatch = re.sub("\[OUTDIR\]", out, sbatch)
        sbatch = re.sub("\[INP\]", simbaUtils.cfg["int"], sbatch)
        sbatch = re.sub("\[GZ\]", gz, sbatch)
        sbatch = re.sub("\[REQ\]", args.dir, sbatch)
        sbatch = re.sub("\[SRC\]", src, sbatch)
        sbatch = re.sub("\[OUT\]", out, sbatch)

        if trackOn:
            sbatch = re.sub("\[TRACKREQ\]", trackReq, sbatch)
        else:
            sbatch = re.sub("\[TRACKREQ\]\n", "", sbatch)

        # write sbatch
        sbatchPath = src + "/" + args.dir + ".sh"
        sbatchFile = open(sbatchPath, "w")
        sbatchFile.write(sbatch)
        sbatchFile.close()

        if trackOn:
            track = simbaUtils.cfg["bin"] + "/" + "track.py " + args.dir + " -m new -s queued"
            os.system(track)

        # submit sbatch to queue
        # simbaUtils.queue(sbatchPath)

        # Write to log
        # simbaUtils.writeLog(simbaUtils.msg)

except ValueError:
    # track error parsing req file
    if trackOn:
        track = simbaUtils.cfg["bin"] + "/" + "track.py " + args.dir + " -m new -s fail"
        os.system(track)

        track = simbaUtils.cfg["bin"] + "/" + "track.py " + args.dir + " -m update -s fail"
        os.system(track)
