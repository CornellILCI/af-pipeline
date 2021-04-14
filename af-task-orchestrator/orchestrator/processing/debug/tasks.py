import json

import jsonpickle
import pandas as pd
import pydantic
from orchestrator.app import LOGGER, app
from orchestrator.base import FailureReportingTask


@app.task(base=FailureReportingTask)
def debug(params):
    pretty_printed = jsonpickle.dumps(params, indent=4)
    LOGGER.info(pretty_printed)
    return params
