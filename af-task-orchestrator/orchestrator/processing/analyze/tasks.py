from orchestrator import config
from orchestrator.app import app
from orchestrator.base import ResultReportingTask
from orchestrator.exceptions import MissingTaskParameter
from pipeline.data_reader.models.enums import DataSource, DataType

from pipeline import analyze as pipeline_analyze

from pipeline.analysis_request import AnalysisRequest

from orchestrator import config


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
    result = pipeline_analyze.run(analysis_request)