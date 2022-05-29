import logging

from af.orchestrator.app import app
from af.orchestrator.base import StatusReportingTask
from af.pipeline import analyze as pipeline_analyze
from af.pipeline.exceptions import AnalysisError

log = logging.getLogger(__name__)


@app.task(name="run_asreml_analyze", base=StatusReportingTask, queue="ASREML")
def run_asreml_analyze(*args):
    _run_analyze(*args)


@app.task(name="run_analyze", base=StatusReportingTask)
def run_analyze(*args):
    _run_analyze(*args)


def _run_analyze(request_id, analysis_request, input_files, results):
    # pop 1 from input_files
    input_file, input_files = input_files[0], input_files[1:]

    try:
        # run analysis on input file, TODO: call Analyze.run_job() here
        result = pipeline_analyze.get_analyze_object(analysis_request).run_job(input_file)
        results.append(result)
    except AnalysisError as ae:
        log.error("Encountered error %s", str(ae))
    finally:
        if not input_files:
            args = request_id, analysis_request, results
            app.send_task("post_process", args=args)
        else:
            args = request_id, analysis_request, input_files, results
            app.send_task("run_asreml_analyze", args=args, queue="ASREML")
