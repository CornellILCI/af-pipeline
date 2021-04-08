import json

from orchestrator.app import LOGGER, app
from orchestrator.base import FailureReportingTask


@app.task(base=FailureReportingTask)
def debug(params: dict) -> dict:
    pretty_printed = json.dumps(params, sort_keys=True, indent=4)
    LOGGER.info(pretty_printed)
    return params
