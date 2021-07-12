from af.orchestrator import config
from af.orchestrator.app import app
from af.orchestrator.base import ResultReportingTask
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
    result = pipeline_analyze.Analyze(analysis_request).run()
