from gevent import time
from orchestrator.app import LOGGER, app


@app.task(base=FailureReportingTask)
def sample_aggregator_task(params):
    LOGGER.info("AGGREGATOR TASK")
    time.sleep(4)
    return params  # return for next task
