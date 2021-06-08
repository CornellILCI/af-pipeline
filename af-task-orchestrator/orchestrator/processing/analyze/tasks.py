from orchestrator.app import app
from orchestrator.base import StatusReportingTask
from orchestrator import asremlutil





@app.task(name="run_asreml")  #, base=StatusReportingTask)
def run_asreml(params: dict):
    """
    TODO: write down params
    """
    processId = params.get("requestId")

    asreml_job_file = f"{processId}.as"
    asreml_data_file = f"{processId}.csv"

    output = asremlutil.run_asreml(asreml_job_file, asreml_data_file)
    params['asreml_result'] = output

    print(output)
    return params



    
    
