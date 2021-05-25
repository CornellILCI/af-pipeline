import jsonpickle
from orchestrator.app import LOGGER, app
from orchestrator.base import ResultReportingTask, StatusReportingTask


@app.task(name="debug", base=StatusReportingTask)
def debug(params):
    pretty_printed = jsonpickle.dumps(params, indent=4)
    LOGGER.info(pretty_printed)
    return params


@app.task(name="debug_result", base=ResultReportingTask)
def debug_result(params):
    LOGGER.info("Terminal task -- reporting")
    return params
