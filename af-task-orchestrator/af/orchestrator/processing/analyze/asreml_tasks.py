import logging

from af.orchestrator.app import app
from af.orchestrator.base import StatusReportingTask
from af.pipeline import analyze as pipeline_analyze
from af.pipeline.exceptions import AnalysisError
from af.orchestrator.processing.analyze import common

log = logging.getLogger(__name__)


@app.task(name="run_asreml_analyze", base=StatusReportingTask, queue="ASREML")
def run_asreml_analyze(request_id, analysis_request, input_files, results):
    input_files = common.run_analyze(request_id, analysis_request, input_files, results)
    if not input_files:
        args = request_id, analysis_request, results
        app.send_task("post_process", args=args)
    else:
        args = request_id, analysis_request, input_files, results
        app.send_task("run_asreml_analyze", args=args, queue="ASREML")
