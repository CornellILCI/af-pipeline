from af.pipeline.job_data import JobData

from af.pipeline.asreml_r import dpo

def test_mesl_returns_job_data():
    asreml_r_dpo = dpo.AsremlRProcessData()
    assert type(asreml_r_dpo.mesl()) is JobData


