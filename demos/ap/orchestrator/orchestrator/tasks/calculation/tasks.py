from orchestrator.registry import register
from orchestrator.base import FailureReportingTask, ResultReportingTask
from orchestrator.app import app, LOGGER
from gevent import time


@app.task(base=FailureReportingTask)
def sample_calculation_task(params):
    LOGGER.info("CALCULATION TASK")
    time.sleep(4)
    return params  # return for next task

