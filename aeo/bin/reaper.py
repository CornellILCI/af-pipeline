#!/usr/bin/python3
# reaper.py -- scans simba's input folder for analysis
#              request and input data and prepares it
#              for analysis. It calls specific "handler"
#              depending on analysis request type.
#
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2019.09.30

import os
import sys
import re

# get value of the PYSIMBA_ROOT environment variable
# and append to the environment path
pyPath = os.environ["EBSAF_ROOT"] + "/aeo/python"
sys.path.append(pyPath)

import simbaUtils
import dbUtils

# read simba configuration file.
simbaUtils.readConfig()

# specify path to input and work directories
inputPath = simbaUtils.cfg["int"]
workPath = simbaUtils.cfg["wrd"]

files = []
dirs = []
fileNum = 0
dirNum = 0
itemTot = 0

# get file list from the input folder
fList = [f for f in os.listdir(inputPath)]

for f in fList:
    if not "README" in f:
        # check if path is a directory
        fPath = inputPath + "/" + f
        isDir = os.path.isdir(fPath)
        if isDir:
            dirNum = dirNum + 1
            dirs.append(f)
        else:
            fileNum = fileNum + 1
            files.append(f)

itemTot = fileNum + dirNum

if itemTot > 0:
    # Update log
    msg = "{0}/{1} files/dirs found!".format(fileNum, dirNum)
    simbaUtils.writeLog(msg)
    # generate folder name for the current set of input
    simbaUtils.genFolderName()
    workFolder = workPath + "/" + simbaUtils.folderName

    # create folder and move input files
    cmd = "mkdir {}".format(workFolder)
    os.system(cmd)

    if fileNum > 0:
        for f in files:
            fPath = inputPath + "/" + f
            cmd = "mv {0} {1}".format(fPath, workFolder)
            os.system(cmd)

        # check if each file has been processed before
        for f in files:
            filePath = workFolder + "/" + f
            simbaUtils.genShaFile(filePath)
            dbUtils.getAnalysisId(simbaUtils.strSha, 1)

            if dbUtils.analysisId:
                # request was previously submitted
                # delete file
                msg = "Duplicate submission for: {}".format(f)
                simbaUtils.writeLog(msg)
                cmd = "rm -fr {}".format(filePath)
                os.system(cmd)
            else:
                if "_SD_" in f:
                    # call statDesign.py
                    sd = simbaUtils.cfg["bin"] + "/" + "statDesign.py"
                    cmd = "{0} {1}".format(sd, filePath)
                    os.system(cmd)
                else:
                    print("SA: ", filePath)
                    # call statAnalysis.py

    if dirNum > 0:
        for d in dirs:
            dPath = inputPath + "/" + d
            cmd = "mv {0} {1}".format(dPath, workFolder)
            os.system(cmd)

        # get the JSON
        for d in dirs:
            dirPath = workFolder + "/" + d
            jsonPath = dirPath + "/"

            for i in os.listdir(dirPath):
                if i.endswith(".JSON"):
                    jsonPath = jsonPath + i

            simbaUtils.genShaFile(jsonPath)

            # print(jsonPath)
            # cmd="cat {}".format(jsonPath)
            # os.system(cmd)

            dbUtils.getAnalysisId(simbaUtils.strSha, 1)

            if dbUtils.analysisId:
                # duplicate request/analysis
                # delete directory
                msg = "Duplicate submission for: {}".format(d)
                simbaUtils.writeLog(msg)
                cmd = "rm -fr {}".format(dirPath)
                os.system(cmd)
            else:
                if "_SD_" in d:
                    # call statDesign.py
                    print("statDesign.py ", d)
                elif "_SA_" in d:
                    # call statAnalysis.py
                    sa = simbaUtils.cfg["bin"] + "/" + "statAnalysis.py"
                    saJSON = workFolder + "/" + d + "/" + d + ".JSON"
                    cmd = "{0} {1}".format(sa, saJSON)
                    os.system(cmd)
                    # print("statAnalysis.py ", saJSON)
                elif "_CG_" in d:
                    # call cropGrowthModel.py
                    print("cropGrowthModel.py", d)
                else:
                    msg = "Unknown reference for {}".format(d)
                    simbaUtils.writeLog(msg)

else:
    simbaUtils.writeLog("No new files found!")
