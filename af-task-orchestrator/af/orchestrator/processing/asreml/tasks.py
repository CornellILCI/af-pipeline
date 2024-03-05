from af.orchestrator import asremlutil
from af.orchestrator.app import app

# from af.orchestrator.base import StatusReportingTask


@app.task(name="run_asreml", queue="ASREML")  # , base=StatusReportingTask)
def run_asreml(params: dict):
    """params is a dict that should contain the following:

    requestId:  the request uuid
    """
    requestId = params.get("requestId")
    asreml_job_file = f"{requestId}.as"
    asreml_data_file = f"{requestId}.csv"

    output = asremlutil.run_asreml(asreml_job_file, asreml_data_file)
    params["asreml_result"] = output

    return params


@app.task(name="parse_asremlr")
def parse_asremlr(params: dict):
    """Params is a dict that should contain the ff:

    jobId: analaysis job_id
    resultFilePath: the filepath to the result file
    """
    job_id = int(params.get("jobId"))
    result_file = params.get("resultFilePath")
    asremlutil.parse_asremlr(job_id, result_file)
