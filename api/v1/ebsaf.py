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
   call(["python3",randExec, folder])
   return jsonify([{'id':'200'}])
app.run()

