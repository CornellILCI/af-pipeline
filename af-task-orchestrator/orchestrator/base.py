import datetime

import celery
from orchestrator.db import db_session
from orchestrator.db.models import Request, Task


class DBLoggingTask(celery.Task):
    def apply_async(self, *args, **kwargs):
        self.time_start = datetime.datetime.now()
        
        params = args[0][0] 
        job_id = params.get("processId") or params.get("jobId")

        self.af_request = db_session.query(Request).filter_by(uuid=job_id).first()
        self.af_task = None
        if self.af_request:
            # create task entry
            self.af_task = Task(name=self.name, time_start=self.time_start, status="STARTED", processor="celery", tenant_id=0, creator_id=0)
            self.af_request.tasks.append(self.af_task)
            db_session.merge(self.af_request)
            db_session.commit()
        else:
            # log warning about af_request does not exit
            print(f"{job_id} does not exist!")

        super().apply_async(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self.af_task:
            self.af_task.time_end = datetime.datetime.now()
            self.af_task.status = status
            if einfo:
                self.af_task.err_msg = str(einfo)
            db_session.merge(self.af_task)
            db_session.commit()

        db_session.remove()


class FailureReportingTask(DBLoggingTask):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Error handler.
        This is run by the worker when the task fails.
        Arguments:
            exc (Exception): The exception raised by the task.
            task_id (str): Unique id of the failed task.
            args (Tuple): Original arguments for the task that failed.
            kwargs (Dict): Original keyword arguments for the task that failed.
            einfo (~billiard.einfo.ExceptionInfo): Exception information.
        Returns:
            None: The return value of this handler is ignored.
        """
        if self.af_task:
            self.af_task.err_msg = str(exc)


class StatusReportingTask(FailureReportingTask):
    def on_success(self, retval, task_id, args, kwargs):
        """Success reporting"""
        # submit status AND/OR retval=s  to the jobapi
        # params = args[0]
        # job_id = params.get("jobId")
        pass
