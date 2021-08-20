from af.orchestrator.app import app
from af.orchestrator.base import StatusReportingTask
from af.pipeline import analyze as pipeline_analyze


@app.task(name="run_analyze", base=StatusReportingTask, queue="ASREML")
def run_analyze(request_id, analysis_request, input_files, results, engine):
    if not input_files:
        args = request_id, analysis_request, results
        app.send_task('post_process', args=args)
    else:
        # pop 1 from input_files
        input_file, input_files = input_files[0], input_files[1:]

        # run analysis on input file, TODO: call Analyze.run_job() here
        result = pipeline_analyze.Analyze(analysis_request).run_job(input_file, engine)
        results.append(result)

        # then recurse
        args = request_id, analysis_request, input_files, results, engine
        app.send_task('run_analyze', args=args, queue="ASREML")
