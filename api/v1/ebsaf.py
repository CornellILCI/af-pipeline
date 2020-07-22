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
          call(["python3",randExec, folder])
          return jsonify(msg='Request submitted.')
     else:
        return jsonify(msg='Missing input files.')
   else:
     return jsonify(msg='Input folder not found.')

@app.route('/v1/status/<folder>', methods=['GET'])
def get_status(folder):
   # check if output has been created.

   dbUtils.getStatusAnalysis(folder, 0)
   reqStatus=dbUtils.statusAnalysis
   reqMsg=dbUtils.statusMsg

   if '000:' in reqMsg and reqStatus=='complete':
     output=simbaUtils.cfg['arch'] + "/" + folder + '.tar.gz'
     if os.path.exists(output):
       return jsonify(status='complete.', msg='Files ready!')
     else:
       return jsonify(msg='Results not ready!')
   else:
     # either queued, fail, stuck
     return jsonify(status=reqStatus, msg=reqMsg)

if __name__=='__main__':
   app.run(host='0.0.0.0')

