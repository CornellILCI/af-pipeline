from af.orchestrator import config
from af.orchestrator.app import app
from af.orchestrator.base import ResultReportingTask, StatusReportingTask
from af.pipeline import analyze as pipeline_analyze
from af.pipeline.analysis_request import AnalysisRequest


@app.task(name="analyze", base=ResultReportingTask)
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
    analyze_object = pipeline_analyze.Analyze(analysis_request)
    input_files = analyze_object.pre_process()
    engine = analyze_object.get_engine()

    results = []  # results initially empty
    run_analyze.delay(request_id, analysis_request, input_files, results, engine)


@app.task(name="run_analyze", queue="ASREML", base=StatusReportingTask)
def run_analyze(request_id, analysis_request, input_files, results, engine):
    if not input_files:
        post_process.delay(request_id, analysis_request, results)
    else:
        # pop 1 from input_files
        input_file, input_files = input_files[0], input_files[1:]

        # run analysis on input file, TODO: call Analyze.run_job() here
        result = pipeline_analyze.Analyze(analysis_request).run_job(input_file, engine)
        results.append(result)

        # then recurse
        run_analyze.delay(request_id, analysis_request, input_files, results, engine)


@app.task(name="post_process", base=StatusReportingTask)
def post_process(request_id, analysis_request, results):
    # process the results here
    if not results:
        done_analyze.delay(request_id)
    else:
        result, results = results[0], results[1:]
        job_name = result["job_name"]

        _ = pipeline_analyze.Analyze(analysis_request).process_job_result(job_name, result)

        # then recurse
        post_process.delay(request_id, analysis_request, results)


@app.task(name="done_analyze", base=ResultReportingTask)
def done_analyze(request_id):
    # this is the terminal task to report DONE in tasks
    pass  # trigger ResultReportingTask success event handler
