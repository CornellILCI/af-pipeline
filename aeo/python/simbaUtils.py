# simbaUtils.py -- package utilities for simba
# Ported from simba
# 2019.10.21, vjmulat

import os
import re
import sys
from datetime import datetime

cfg={}
param={}
strSha=''
date=''
errMsg='NULL'
msg=''
folderName='';
tmplContents='';
jobStat=3;

def readConfig():
  confPath=os.environ['PYSIMBA_ROOT'] + "/conf/simba.conf"
  
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
  
def getErrMsg(str):
  errFile=str + ".err"
  global errMsg
  
  readConfig()
  errPath = cfg['lgd'] + "/" + errFile
  
  if not os.path.isfile(errPath):
    errMsg='NULL'
  else:
    with open(errPath, 'r') as tmp:
      errMsg = tmp.read()
      errMsg=errMsg.strip()

def queue(str):
  global msg
  cmd = "sbatch {}".format(str) 
  os.system(cmd)
  sbatchFile=re.sub(".+\/",'',str.rstrip())
  msg=sbatchFile + " sent to queue!"
  

def getJobStat(str):
  # 1 fail, no msg 
  # 2 fail, with msg 
  # 3 success, no msg
  # 4 success, with msg 
  
  readConfig()

  global jobStat 
  x=0

  errFile=str + ".err"
  errFile=cfg['lgd'] + "/" + errFile

  outFile=str + ".out"
  outFile=cfg['lgd'] + "/" + outFile
  
  # check if both files exists

  if not os.path.isfile(errFile):
    x=x+0
  else:
    x=x+1

  if not os.path.isfile(outFile):
    x=x+0
  else:
    x=x+1
  
  # check file sizes
  if (x==2):
    errFsize=os.path.getsize(errFile)
    outFsize=os.path.getsize(outFile)
    fsize=errFsize+outFsize 
    if (fsize==0):
      # for stat design both files == 0 means success. 
      jobStat=3
    elif (errFsize==0) and (outFsize != 0):
      # have to check this -- perhaps read contents of
      # outFile to determine actual status i.e. getErrMsg 
      jobStat=4
    elif (errFsize != 0) and (outFsize==0):
      # have to check this -- perhaps read contents of
      # orrFile to determine actual status i.e. getErrMsg 
      jobStat=2
    elif (errFsize != 0) and (outFsize != 0):
      # have to check this -- perhaps read contents of
      # orrFile to determine actual status i.e. getErrMsg 
      jobStat=1
  else:
    # unknown error
    jobStat=0

def genFolderName():
   global folderName
   folderName=datetime.now()
   folderName=folderName.strftime("%Y%m%d%H%M%S%f")

