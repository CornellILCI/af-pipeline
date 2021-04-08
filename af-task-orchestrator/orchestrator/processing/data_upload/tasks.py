from gevent import time
from orchestrator.app import LOGGER, app
from orchestrator.base import FailureReportingTask


@app.task(base=FailureReportingTask)
def sample_data_upload_task(params):
    LOGGER.info("DATA UPLOAD TASK")
    time.sleep(4)
    return params  # return for next task
