from af.pipeline.job_data import JobData
from af.pipeline.db.models import Property

from af.pipeline.asreml_r import dpo


def test_dpo_run_returns_job_data(mocker, analysis_request):
    
    exp_location_analysis_pattern_stub = Property(code="MESL")
    mocker.patch("af.pipeline.db.services.get_property", return_value=exp_location_analysis_pattern_stub)
    
    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)
    assert type(asreml_r_dpo.run()) is list


def test_dpo_run_returns_jobs(mocker, analysis_request):

    exp_location_analysis_pattern_stub = Property(code="MESL")
    mocker.patch("af.pipeline.db.services.get_property", return_value=exp_location_analysis_pattern_stub)
    
    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)
    jobs = asreml_r_dpo.run()
    assert(len(jobs) > 0)


def test_dpo_run_returns_job_list(mocker, analysis_request):
    
    exp_location_analysis_pattern_stub = Property(code="MESL")
    mocker.patch("af.pipeline.db.services.get_property", return_value=exp_location_analysis_pattern_stub)
    
    
    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)
    jobs = asreml_r_dpo.run()
    for job in jobs:
        assert type(job) is JobData


def test_dpo_run_for_mesl_method_called(mocker, analysis_request):
    
    exp_location_analysis_pattern_stub = Property(code="MESL")
    mocker.patch("af.pipeline.db.services.get_property", return_value=exp_location_analysis_pattern_stub)
    
    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)
    
    mocker.patch('af.pipeline.asreml_r.dpo.AsremlRProcessData.mesl')

    jobs = asreml_r_dpo.run()

    asreml_r_dpo.mesl.assert_called_once()
