#!/usr/bin/python3
# ebsaf.py -- triggers randomization of a given folder 
#   containing *.jcf (job control file) and *.lst 
#   (entry list). The folder should be present in the
#   <mounted volume>/input folder.
#   
# Jack Elendil Lagare (j.lagare@irri.org)
# Victor Jun Ulat (v.ulat@cgiar.org)
# 2020.06.24

import os
import sys
import json 
import flask
from flask import request, jsonify
from subprocess import call

ebsafRoot=os.environ['EBSAF_ROOT']
pyPath=ebsafRoot + "/aeo/python"
sys.path.append(pyPath)

binPath=ebsafRoot + "/aeo/bin"
randExec=binPath + "/randomize.py"

import simbaUtils
import dbUtils

# read configuration file.
simbaUtils.readConfig()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/v1/randomize/<folder>', methods=['POST'])
def start_randomization(folder):
   # check if folder exists...
   input=simbaUtils.cfg['int'] + "/" + folder
   if os.path.isdir(input):
     # generate filenames for required files
     jobName=folder[:-1] + '1'
     reqFile=input + "/" + folder + ".req"
     reqJcf=input + "/" + jobName + ".jcf"
     entLst=input + "/" + jobName + ".lst"

     # check if all required files exists
     if (os.path.exists(reqJcf) and
        os.path.exists(reqFile) and
        os.path.exists(entLst)):
          
          # check for duplicate submission
          simbaUtils.genShaFile(reqFile)
          sha=simbaUtils.strSha
          dbUtils.getAnalysisId(sha, 1)
          reqID=dbUtils.analysisId
          
          if reqID:
            msg="Duplicate submission."
            simbaUtils.genApiMsg('failed',msg)
            jsonMsg=simbaUtils.jsonMsg 
            return (jsonMsg)
          else:
            call(["python3",randExec, folder])
            msg="Request has been submitted."
            simbaUtils.genApiMsg('submitted',msg)
            jsonMsg=simbaUtils.jsonMsg 
            return (jsonMsg)
     else:
        msg="Missing input files."
        simbaUtils.genApiMsg('failed',msg)
        jsonMsg=simbaUtils.jsonMsg
        return(jsonMsg)
   else:
     msg="Input folder not found."
     simbaUtils.genApiMsg('failed',msg)
     jsonMsg=simbaUtils.jsonMsg
     return(jsonMsg)

@app.route('/v1/status/<folder>', methods=['GET'])
def get_status(folder):
   # check if output has been created.

   dbUtils.getStatusAnalysis(folder, 0)
   reqStatus=dbUtils.statusAnalysis
   reqMsg=dbUtils.statusMsg

   if '000:' in reqMsg and reqStatus=='complete':
     # returns "Request is in queue" after results has 
     # been archived as a result of running cleaner.py
     output=simbaUtils.cfg['arch'] + "/" + folder + '.tar.gz'
     if os.path.exists(output):
       msg="Request has been successfully completed."
       simbaUtils.genApiMsg('completed',msg)
       jsonMsg=simbaUtils.jsonMsg 
       return(jsonMsg)
     else:
       msg="Request is in the queue."
       simbaUtils.genApiMsg('queued',msg)
       jsonMsg=simbaUtils.jsonMsg 
       return (jsonMsg)
   else:
     # either queued, fail, stuck
     if reqStatus=='queued':
       status='queued'
       msg="Request is in the queue."
     else:
       status='failed'
       msg=reqMsg
    
     simbaUtils.genApiMsg(status,msg)
     jsonMsg=simbaUtils.jsonMsg
     return (jsonMsg)

if __name__=='__main__':
   app.run(host='0.0.0.0')

