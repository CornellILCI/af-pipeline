from orchestrator import config
from orchestrator.app import app
from orchestrator.base import StatusReportingTask
from orchestrator.exceptions import MissingTaskParameter
from pipeline.data_reader.exceptions import DataSourceNotAvailableError, DataTypeNotAvailableError
from pipeline.data_reader.models.enums import DataSource, DataType

from pipeline import analyze

from orchestrator import config

@app.task(name="analyze", base=StatusReportingTask)
def analyze(request_id: str, request_params):
    """ Analyze taks run the analysis engine for given task request parameters.

    Based on the type of executor whether it is Celery or Slurm, the method submits the task 
    to respective executor.

    Args:
        request_id: Id of the request to process.
        request_params: Dict object with request parameters passed to analysis module.
    Throws:
        DpoException: Except when failed to read data from the datasource or process it. 
        MissingTaskParameter: Errors when teh required task parameters are not found.
    """


    data_source = request_params.get("dataSource")  # this is either EBS or BRAPI
    if not data_source:
        raise MissingTaskParameter("dataSource")

    api_token = params.get("dataSourceAccessToken")
    if not api_token:
        raise MissingTaskParameter("apiBearerToken")

    datasource = _get_datasource(source)
    api_base_url = _get_api_details(datasource)

    output_folder = config.get_analysis_request_folder(request_id)

    analyze.run(datasource, api_base_url, api_token, request_params, output_folder)
    


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

