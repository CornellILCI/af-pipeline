from af.pipeline import asreml_r
from mock import patch
from af.pipeline import job_data

def test_run_job_returns_job_data(analysis_request, mocker):

    mocker.patch.object(asreml_r.analyze.AsremlRAnalyze, "__init__", lambda x, y: None)

    returned_job_data = asreml_r.analyze.AsremlRAnalyze(analysis_request).run_job(job_data.JobData())

    assert type(returned_job_data) == job_data.JobData

    
