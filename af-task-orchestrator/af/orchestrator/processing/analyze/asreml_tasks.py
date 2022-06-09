import logging

from af.orchestrator.app import app
from af.orchestrator.base import StatusReportingTask
from af.pipeline import analyze as pipeline_analyze
from af.pipeline.exceptions import AnalysisError
from af.orchestrator.processing.analyze import common

log = logging.getLogger(__name__)


@app.task(name="run_asreml_analyze", base=StatusReportingTask, queue="ASREML")
def run_asreml_analyze(*args):
    common.run_analyze(*args)


