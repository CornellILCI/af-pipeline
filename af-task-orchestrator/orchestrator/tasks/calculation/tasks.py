from gevent import time
from orchestrator.app import LOGGER, app
from orchestrator.base import FailureReportingTask, ResultReportingTask
from orchestrator.registry import register


@app.task(base=FailureReportingTask)
def sample_calculation_task(params):
    LOGGER.info("CALCULATION TASK")
    time.sleep(4)
    return params  # return for next task
