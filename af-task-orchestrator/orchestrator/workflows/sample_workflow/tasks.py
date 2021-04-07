from gevent import time
from orchestrator.app import LOGGER, app
from orchestrator.base import FailureReportingTask, ResultReportingTask
from orchestrator.registry import register


def sample_workflow(params):
    """
    Sample workflow functions that call the tasks
    """
    (
        sample_worfklow_extract_task.s(params) | sample_worflow_transform_task.s() | sample_workflow_load_task.s()
    ).apply_async()


# -- tasks section


@app.task(base=FailureReportingTask)
def sample_worfklow_extract_task(params):
    LOGGER.info("In Extract task")
    time.sleep(5)  # simulate a long task
    params["extract_result"] = "Sample extract result"
    return params  # return this for next task


@app.task(base=FailureReportingTask)
def sample_worflow_transform_task(params):
    LOGGER.info("In Transform task")
    time.sleep(4)  # simulate another long task
    params["transform_result"] = params["extract_result"] + " Sample transform result"
    # let's remove extract_result
    del params["extract_result"]
    return params  # return for next task


@app.task(base=ResultReportingTask)
def sample_workflow_load_task(params):
    LOGGER.info("In Load task")
    time.sleep(3)  # simulate long task
    params["load_result"] = params["transform_result"] + " Load Result"

    return params


# this should be called on import
register("sample_workflow", sample_workflow)
