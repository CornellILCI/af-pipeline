from celery import Task


class FailureReportingTask(Task):
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
        # report to jobAPI that the task failed
        # params = args[0]
        # job_id = params.get("jobId")

        # call job API store to update that the task failed


class ResultReportingTask(FailureReportingTask):
    def on_success(self, retval, task_id, args, kwargs):
        """Success reporting"""
        # submit status AND/OR retval=s  to the jobapi
        # params = args[0]
        # job_id = params.get("jobId")
