from orchestrator.app import app
from orchestrator.base import StatusReportingTask
from orchestrator import asremlutil



@app.task(name="run_asreml", base=StatusReportingTask)
def run_asreml(params: dict):
    """params is a dict that should contain the following:
    
    requestId:  the request uuid 
    """
    requestId = params.get("requestId")
    asreml_job_file = f"{requestId}.as"
    asreml_data_file = f"{requestId}.csv"

    output = asremlutil.run_asreml(asreml_job_file, asreml_data_file)
    params['asreml_result'] = output

    return params
 
