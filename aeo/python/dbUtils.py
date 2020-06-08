# dbUtils.py -- pySimba package for database connection.
# Ported from simba.
# 2019.11.19, vjmulat

# Sprint 2020.06 Todo's
# * pyPath should use EBSAF_ROOT

import os
import re
import sys
import psycopg2

dbName=''
dbUser=''
dbPswd=''
dbPort=''
dbHost=''
dbConn=''
analysisId=''
jobId=''
statusAnalysis=''

pyPath=os.environ['PYSIMBA_ROOT'] + "/python"
sys.path.append(pyPath)

import simbaUtils

def getDBcredentials():
  global dbName
  global dbUser
  global dbPswd
  global dbPort
  global dbHost

  simbaUtils.readConfig()
  dbName=simbaUtils.cfg['dbn']
  dbUser=simbaUtils.cfg['dbu']
  dbPswd=simbaUtils.cfg['dbp']
  dbPort=simbaUtils.cfg['dpt']
  dbHost=simbaUtils.cfg['dbh']

def createConn():
  getDBcredentials()
  connStr="host="+ dbHost + " port="+ dbPort + " dbname="+ \
          dbName + " user=" + dbUser + " password=" + dbPswd

  global dbConn
  dbConn=psycopg2.connect(connStr)
  # print("Connected!")

def closeConn():
  global dbConn
  dbConn.close()
  # print("Connection closed!")

def addAnalysis (rqId, sha, rqType):
  getAnalysisId(sha, 1)
  
  if analysisId:
    # LOG THIS
    msg="Analysis: {} ".format(sha)
    msg=msg + "is already in the database!"
    simbaUtils.writeLog(msg)
    # print("Analysis:", sha, " is already in the database!")
  else:
    createConn()
    sql="INSERT INTO analysis (" + \
          "request_id, sha, request_type, " + \
          "time_submitted" + \
        ") VALUES (" + \
          "'{0}', '{1}', '{2}',".format(rqId,sha,rqType) + \
          "current_timestamp" + \
          ")"
    cursor=dbConn.cursor()
    
    try:
      cursor.execute(sql)
      dbConn.commit()
    except(Exception,psycopg2.Error) as error:
      if(dbConn):
        # LOG THIS
        msg="New analysis insert fail! {}".format(error)
        simbaUtils.writeLog(msg)
        # print("New analysis insert fail! ", error)
    finally:
      if(dbConn):
        cursor.close()
        closeConn()

def addJob (analysisId, jobName, parentId): 
  getJobId(jobName)
  
  if jobId:
    # LOG THIS
    msg="Job: {} ".format(jobname)
    msg=msg + "exists!"
    simbaUtils.writeLog(msg)
    # print("Job:", jobName, "exists!")
  else:
    createConn()
    sql="INSERT INTO job (" + \
          "analysis_id, name, time_start, parent_id" +\
        ") VALUES (" + \
          "'{0}','{1}',".format(analysisId,jobName) + \
          "current_timestamp, '{0}'".format(parentId) + \
        ")"

    cursor=dbConn.cursor()
   
    try:
      cursor.execute(sql)
      dbConn.commit()
    except(Exception,psycopg2.Error) as error:
      if(dbConn):
        # LOG THIS
        msg="New job insert fail: {}".format(error)
        simbaUtils.writeLog(msg)
        # print("New job insert fail!", error)    
    finally:
       if(dbConn):
         cursor.close()
         closeConn()
   
def updateJob (jobName, status, errMsg):
  createConn()
  sql=''
  if errMsg:
    sql="UPDATE job " + \
        "SET " + \
          "time_end = current_timestamp, " + \
          "status ='{0}', ".format(status) + \
          "err_msg = '{0}' ".format(errMsg) + \
        "WHERE " + \
          "name = '{0}'".format(jobName)
  else:
    sql="UPDATE job " + \
        "SET " + \
          "time_end = current_timestamp, " + \
          "status ='{0}' ".format(status) + \
        "WHERE " + \
          "name = '{0}'".format(jobName)

  cursor=dbConn.cursor()
  
  try:
    cursor.execute(sql)
    dbConn.commit()
  except(Exception,psycopg2.Error) as error:
    if(dbConn):
      # LOG THIS
      msg="Update failed for " 
      msg=msg + "job: {0} {1}".format(jobName, error)
      simbaUtils.writeLog(msg)
      # print("Update failed for job:", jobName, error)
  finally:
    if(dbConn):
      cursor.close()
      closeConn() 


def getAnalysisId (qry, is_sha):
  createConn()
  global analysisId
  sql=''
  
  if is_sha:
    sql="SELECT id " + \
        "FROM analysis " + \
        "WHERE sha=\'{0}\'".format(qry)
  else:  
    sql="SELECT id " + \
        "FROM analysis " + \
        "WHERE request_id=\'{0}\'".format(qry)
  
  cursor=dbConn.cursor()
  cursor.execute(sql)
  
  result=cursor.fetchall()
  result=[i[0] for i in result]
  
  if result:
    analysisId=result[0]
  else:
    analysisId=0

  closeConn()

def getJobId (qry):
  createConn()
  global jobId
  sql=''

  sql="SELECT id " + \
      "FROM job " + \
      "WHERE job.name='{0}'".format(qry)
  
  cursor=dbConn.cursor()
  cursor.execute(sql)

  result=cursor.fetchall()
  result=[i[0] for i in result]

  if result:
    jobId=result[0]
  else:
   jobId=0

  closeConn()

def getStatusAnalysis (qry, is_sha):
  getAnalysisId(q, is_sha)
  global statusAnalysis
  
  if analysisId:
    createConn()
    sql=''

    if is_sha:
      sql="SELECT count(*) " + \
          "FROM analysis a, job j " + \
          "WHERE a.sha='{0}' ".format(qry) + \
          "AND a.id=j.analysis_id " + \
          "AND j.status=0";
    else:
      sql="SELECT count(*) " + \
          "FROM analysis a, job j " + \
          "WHERE a.request_id='{0}' ".format(qry) + \
          "AND a.id=j.analysis_id " + \
          "AND j.status=0";
  
    cursor=dbConn.cursor()
    cursor.execute(sql)

    result=cursor.fetchall()
    result=[i[0] for i in result]

    count=result[0]
 
    closeConn()    

    if count:
      # Some/all jobs failed!
      statusAnalysis=0
    else:
      # All jobs finished successfuly!
      statusAnalysis=1
