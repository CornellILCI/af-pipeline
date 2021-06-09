from orchestrator import config
from orchestrator.app import app
from orchestrator.base import StatusReportingTask
from orchestrator.exceptions import MissingTaskParameter
from pipeline.data_reader.exceptions import AnalysisError
from pipeline.data_reader.models.enums import DataSource, DataType

from pipeline import analyze

from pipeline.analysis_request import AnalysisRequest

from orchestrator import config

@app.task(name="analyze", base=StatusReportingTask)
def analyze(request_id: str, request_params):
    """ Analyze taks run the analysis engine for given task request parameters.

    Based on the type of executor whether it is Celery or Slurm, the method submits the task 
    to respective executor.

    Args:
        request_id: Id of the request to process.
        request_params: Dict object with request parameters passed to analysis module.
    """


    output_folder = config.get_analysis_request_folder(request_id)
    
    analysis_request = analysis_request(
        requestId=request_id,
        outputFolder=output_folder,
        **request_params
    )
    
    # TODO: Condition to check executor is celery, If executor is slurm, submit analyze script as sbatch
    result = analyze.run(analysis_request)
    


def _get_api_details(datasource: DataSource, *args, **kwargs):
    if datasource == DataSource.EBS:
        return config.EBS_BASE_URL
    elif datasource == DataSource.BRAPI:
        return config.BRAPI_BASE_URL


def _get_datasource(datasource: str, *args, **kwargs) -> DataSource:
    source: DataSource = None
    try:
        source = DataSource[datasource]
        return source
    except KeyError:
        raise DataSourceNotAvailableError(datasource)

