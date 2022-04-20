import logging

from af.orchestrator import config
from af.orchestrator.app import app
from af.orchestrator.base import ResultReportingTask, StatusReportingTask
from af.pipeline import analyze as pipeline_analyze
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.exceptions import AnalysisError

log = logging.getLogger(__name__)


@app.task(name="analyze", base=StatusReportingTask)
def analyze(request_id: str, request_params):
    """Analyze taks run the analysis engine for given task request parameters.

    Based on the type of executor whether it is Celery or Slurm, the method submits the task
    to respective executor.

    Args:
        request_id: Id of the request to process.
        request_params: Dict object with request parameters passed to analysis module.
    """

    output_folder = config.get_analysis_request_folder(request_id)

    analysis_request = AnalysisRequest(requestId=request_id, outputFolder=output_folder, **request_params)

    # TODO: Condition to check executor is celery, If executor is slurm, submit analyze script as sbatch
    # pipeline_analyze.Analyze(analysis_request).run()
    # let's call init_analyze with the analysis_request object

    pre_process.delay(request_id, analysis_request)


@app.task(name="pre_process", base=StatusReportingTask)
def pre_process(request_id, analysis_request):
    analyze_object = pipeline_analyze.get_analyze_object(analysis_request)
    input_files = analyze_object.pre_process()
    # engine = analyze_object.get_engine_script()

    results = []  # results initially empty
    args = request_id, analysis_request, input_files, results
    app.send_task("run_analyze", args=args, queue="ASREML")


@app.task(name="post_process", base=StatusReportingTask)
def post_process(request_id, analysis_request, results, gathered_objects=None):
    if not results:
        done_analyze.delay(request_id, analysis_request, gathered_objects)

    result, results = results[0], results[1:]

    if gathered_objects is None:
        gathered_objects = {}
    try:
        analyze_object = pipeline_analyze.get_analyze_object(analysis_request)
        gathered_objects = analyze_object.process_job_result(result, gathered_objects)
    except AnalysisError as ae:
        log.error("Encountered error: %s", str(ae))
    finally:
        post_process.delay(request_id, analysis_request, results, gathered_objects)


@app.task(name="done_analyze", base=ResultReportingTask)
def done_analyze(request_id, analysis_request, gathered_objects):
    # this is the terminal task to report DONE in tasks
    _ = pipeline_analyze.get_analyze_object(analysis_request).finalize(gathered_objects)
