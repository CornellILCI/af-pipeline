import jsonpickle
from orchestrator.app import LOGGER, app
from orchestrator.base import FailureReportingTask


@app.task(name="debug", base=FailureReportingTask)
def debug(params):
    pretty_printed = jsonpickle.dumps(params, indent=4)
    LOGGER.info(pretty_printed)
    return params
