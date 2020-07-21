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

pyPath=os.environ['EBSAF_ROOT'] + "/aeo/python"
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

def addAnalysis (rqId, sha, rqType, status):
  getAnalysisId(sha, 1)
  
  if analysisId:
    # LOG THIS
    msg="Request: {0}; sha: {1}".format(rqId,sha)
    msg=msg + " is already in the database!"
    simbaUtils.writeLog(msg)
    # print("Analysis:", sha, "is already in the database!")
  else:
    createConn()
    sql="INSERT INTO analysis (" + \
          "request_id, sha, request_type, " + \
          "time_submitted, status" + \
        ") VALUES (" + \
          "'{0}', '{1}', '{2}',".format(rqId,sha,rqType) + \
          "current_timestamp," + \
          "'{0}'".format(status) + \
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

def updateAnalysis(analysisId):
  createConn()
  # get all jobs for the analysis
  # job.analysisId = analysisId 
  ## print("Update this:", analysisId)
  sql="SELECT time_end, status " + \
      "FROM job " + \
      "WHERE analysis_id=\'{0}\'".format(analysisId)

  cursor=dbConn.cursor()
  cursor.execute(sql)

  result=cursor.fetchall()

  i=0
  c=0 # complete/has time end
  m=0 # has msg
  f=0 # fail
  s=0 # success
  e=0 # error

  if result:
    for r in result:
      i=i+1
      if r[0]:
        c=c+1
      if r[1] == 0:
        f=f+1
      if r[1] == 100:
        s=s+1
      if r[1] == 101:
        e=e+1 
      if r[1] == 110:
        m=m+1
      if r[1] == 111:
        e=e+1
        m=m+1

    if i == c:
      # all jobs complete
      # complete: n000 (n = no. of jobs)
      # fail: nnnn (n = no. of jobs and 
      #                 no. of err and out msgs
      #                 no. of failed jobs)
      code="{0}{1}{2}{3}: ".format(c,m,e,f)
      if m != 0 and e !=0 and f !=0:
        annStatus="failed"
      else:
        annStatus="complete"
      annMsg=code + \
             "{0} of {1}".format(c,i) + \
             " jobs complete with " + \
             "{0} message(s) ".format(m) + \
             "{0} error(s) ".format(e) + \
             "{0} failed job(s).".format(f)

      ##print(code, c, "of", i, "jobs complete with", \
      ##      m, "message(s),", \
      ##      e, "error(s),", \
      ##      f, "failed job(s).")

    else:
      # Job(s) seemed stuck, completion signal sent but
      # no ending timestamp given.
      annStatus="stuck"
      if c:
        # some jobs are stuck.
        annMsg="{0} of {0} job(s) stuck.".format(c,i)
        ## print(c,"of",i,"job(s) stuck.")
      else:
        # all jobs stuck.
        annMsg="{0} of {0} job(s) stuck.".format(i)
        ## print(i,"of",i,"job(s) stuck.")

  else:
    annMsg="Failed to read job control file."
    annStatus="failed"

  sql="UPDATE analysis " + \
      "SET status= \'{0}\', ".format(annStatus) + \
          "msg=\'{0}\' ".format(annMsg) + \
      "WHERE id=\'{0}\'".format(analysisId)
  ## print(sql)

  try:
    cursor.execute(sql)
    dbConn.commit()
  except(Exception,psycopg2.Error) as error:
    if(dbConn):
      msg="Update failed for "
      msg=msg + "analysis: {0} {1}".format(analysisId, error)
      simbaUtils.writeLog(msg)
  finally:
    if (dbConn):
      cursor.close()
      closeConn()

def addJob (analysisId, jobName, parentId): 
  getJobId(jobName)
  
  if jobId:
    # LOG THIS
    msg="Job: {} ".format(jobName)
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

