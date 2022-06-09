from af.orchestrator.app import app
from af.pipeline import analyze as pipeline_analyze
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.exceptions import AnalysisError


def run_analyze(request_id, analysis_request, input_files, results):

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

