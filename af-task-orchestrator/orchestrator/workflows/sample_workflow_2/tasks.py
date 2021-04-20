from celery import chain
from gevent import time
from orchestrator.app import LOGGER, app
from orchestrator.base import FailureReportingTask, ResultReportingTask
from orchestrator.common.tasks import common_task
from orchestrator.services.sample_service import api_service


@app.task(name="sample_workflow_2")
def sample_workflow_2(params):
    """
    Sample workflow functions that call the tasks
    """
    chain(sample_analyze_task.s(params), common_task.s(), sample_post_analysis_task.s())()


# -- tasks section


@app.task(name="sample_analyze_task", base=FailureReportingTask)
def sample_analyze_task(params):
    LOGGER.info("In analyze task")
    result = api_service.some_api_call()
    params["api_call_result"] = result
    return params  # return this for next task


@app.task(name="sample_post_analysis_task", base=ResultReportingTask)
def sample_post_analysis_task(params):
    LOGGER.info("In post analysis task")
    time.sleep(1)  # simulate another long task
    return params  # return for next task
