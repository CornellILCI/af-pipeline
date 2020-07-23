# simbaUtils.py -- package utilities for simba
# Ported from simba
# 2019.10.21, vjmulat

# Sprint 2020.06 Todo's
# * confPath should use EBSAF_ROOT

import os
import re
import sys
import json
from datetime import datetime

cfg={}
param={}
strSha=''
date=''
errMsg='NULL'
msg=''
jsonMsg=''
folderName='';
tmplContents='';
jobStat=3;

def readConfig():
  confPath=os.environ['EBSAF_ROOT'] + "/aeo/conf/simba.conf"
  
  simbaConf=open(confPath, 'r')
 
  line=simbaConf.readline()

  while line:
    if not line.startswith("#"):
       line=line.strip()
       key,value = line.split("=")
       cfg[key]=value
    line=simbaConf.readline()

  simbaConf.close()

def getParams (str):
  tmp=str.splitlines()
  for x in tmp:
    x=x.lstrip()
    if x.startswith("'"):
      x.rstrip(',')
      key,value = x.split(" => ")
      key=re.sub("'",'', key.rstrip())
      value=re.sub("'",'', value.rstrip())
      if 'key' in param:
        # LOG THIS
        dupMsg="Error: Duplicate parameter name!"
        writeLog(dupMsg)
        sys.exit()
      else:
        param[key]=value

def genSha (str):
  global strSha
  cmd = "echo -n {0} | sha1sum".format(str)
  strSha = os.popen(cmd).read()
  strSha = re.sub(" .+",'', strSha.rstrip())

def genShaFile (filePath):
  global strSha
  cmd = "sha1sum {}".format(filePath)
  strSha = os.popen(cmd).read()
  strSha = re.sub(" .+",'', strSha.rstrip())

def getDate():
  global date
  cmd = "date"
  date = os.popen(cmd).read()
  date=date.strip()

def getTemplate(tmplName):
  global tmplContents

  readConfig()

  fileTmpl=cfg['tpl'] + "/" + tmplName
  tmpl=open(fileTmpl, 'r')
  tmplContents=tmpl.read()

def writeLog(str):
  str=str.strip()
  getDate()
  
  readConfig()

  if not os.path.isfile(cfg['slg']):
    cmd="touch {}".format(cfg['slg'])  
    os.system(cmd) 
  
  line=date + "\t" + str + "\n" 
 
  log=open(cfg['slg'],"a+")
  log.write(line)
  log.close()  
  
def getErrMsg(str, errCode):
  global errMsg
  
  readConfig()
  errFile=str + ".err"
  errFile=cfg['lgd'] + "/" + errFile

  outFile=str + ".out"
  outFile=cfg['lgd'] + "/" + outFile
  
  # errCode:
  # 101 - get err msg
  # 110 - get out msg
  # 111 - get out and err msg
  
  if errCode != 111:
    msgSLURM=''
    if errCode == 101:
      msgSLURM = errFile
    if errCode == 110:
      msgSLURM = outFile

    with open(msgSLURM, 'r') as tmp:
      errMsg = tmp.read()
      errMsg = errMsg.strip()

  elif errCode == 111:
    with open(errFile, 'r') as tmp:
      errFileMsg = tmp.read()
      errFileMsg = errFileMsg.strip()
    with open(outFile, 'r') as tmp:
      outFileMsg = tmp.read()
      outFileMsg = outFileMsg.strip()

    errMsg = "Out: " + outFileMsg + "\nErr: " + errFileMsg

def queue(str):
  global msg
  cmd = "sbatch {}".format(str) 
  os.system(cmd)
  sbatchFile=re.sub(".+\/",'',str.rstrip())
  msg=sbatchFile + " sent to queue!"
  

def getJobStat(str):
  readConfig()
  global jobStat 

  # generate .out and .err paths
  errFile=str + ".err"
  errFile=cfg['lgd'] + "/" + errFile

  outFile=str + ".out"
  outFile=cfg['lgd'] + "/" + outFile
  
  # check if both files exists
  if os.path.exists(outFile) and os.path.exists(errFile):
     #get file sizes
     errFsize=os.path.getsize(errFile)
     outFsize=os.path.getsize(outFile)
     if (errFsize==0) and (outFsize==0):
       # both files zero size
       # (100: complete)
       jobStat=100
     elif (errFsize > 0) and (outFsize==0):
       # runtime error
       # (101: complete, with error)
       jobStat=101
     elif (errFsize==0) and (outFsize > 0):
       # (110: complete with msg)
       jobStat=110
     elif (errFsize > 0) and (outFsize > 0):
       # both files not empty
       # error and stdout msg
       jobStat=111
  else:
    # one or both files missing
    # (0: fail)
    jobStat=0

def genFolderName():
   global folderName
   folderName=datetime.now()
   folderName=folderName.strftime("%Y%m%d%H%M%S%f")

def genApiMsg(status, str):
   global jsonMsg
   msgCode=200

   if status=='failed':
     msgCode=400

   data={'status':[{'message': str,
                    'messageType': 'INFO',
                    'messageCode': msgCode,
                    'requestStatus': status
        }]}
   jsonMsg=json.dumps(data,indent=4)


