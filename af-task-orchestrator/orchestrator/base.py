import celery
from orchestrator.services.afdbservice import AFDBService


class StatusReportingTask(celery.Task):
    def apply_async(self, *args, **kwargs):
        self.afdb_service = AFDBService()
        params = args[0][0]  # args should be a tuple and the first element of that
        # tuple should be our standard 'params' dict
        request_id = params.get("processId") or params.get("jobId")

        self.af_request = self.afdb_service.get_af_request(request_id)
        self.af_task = None
        if self.af_request:
            # create task entry
            self.af_task = self.afdb_service.create_request_task_entry(self.af_request, self.name)
        else:
            # log warning about af_request does not exit
            print(f"{request_id} does not exist!")
        self.af_task_updated = False

        super().apply_async(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):

        if self.af_task:
            self.afdb_service.update_task_status(self.af_task, status)

        # return/cleanup connection
        self.afdb_service.remove_session()

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

        if self.af_request:
            self.afdb_service.update_request_status(self.af_request, "FAILURE")

        if self.af_task:
            self.af_task.err_msg = str(exc)


class ResultReportingTask(StatusReportingTask):
    def on_success(self, retval, task_id, args, kwargs):
        """Success reporting"""
        # TODO:  determine if this task is a terminal task
        # if yes, then set the af_request status to DONE
        if self.af_request:
            self.afdb_service.update_request_status(self.af_request, "DONE")
