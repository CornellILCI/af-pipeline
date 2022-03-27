from af.pipeline.job_data import JobData
from af.pipeline.db.models import Property

from af.pipeline.asreml_r import dpo

import pytest
from unittest.mock import call


def test_dpo_run_for_mesl_method_called(mocker, analysis_request):

    exp_location_analysis_pattern_stub = Property(code="MESL")
    mocker.patch("af.pipeline.db.services.get_property", return_value=exp_location_analysis_pattern_stub)

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)

    mocker.patch("af.pipeline.asreml_r.dpo.AsremlRProcessData.mesl")

    jobs = asreml_r_dpo.run()

    asreml_r_dpo.mesl.assert_called_once()


def test_dpo_run_returns_job_data(mocker, analysis_request):

    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements") 
    
    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)
    assert type(asreml_r_dpo.mesl()) is list


def test_dpo_run_returns_jobs(mocker, analysis_request):

    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements") 
    
    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)
    jobs = asreml_r_dpo.mesl()
    assert len(jobs) > 0


def test_dpo_run_returns_job_list(mocker, analysis_request):

    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements") 
    
    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)
    jobs = asreml_r_dpo.mesl()
    for job in jobs:
        assert type(job) is JobData


def test_dpo_run_for_mesl_num_jobs(mocker, mesl_analysis_request):

    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements") 

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.mesl()

    # expected_num_jobs = num_locations * num_traits
    assert len(jobs) == 4


def test_job_names(mocker, mesl_analysis_request):

    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements") 

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.mesl()

    expected_job_names = {"test_id_mesl_1_1", "test_id_mesl_2_1", "test_id_mesl_1_2", "test_id_mesl_2_2"}
    actual_job_names = set()
    for job in jobs:
        actual_job_names.add(job.job_name)

    assert expected_job_names == actual_job_names
        


def test_job_name_for_second_job(mocker, mesl_analysis_request):

    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements") 

    # combination of location id and trait id
    expected_job_name_1 = f"{mesl_analysis_request.requestId}_mesl_2_1"

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.mesl()

    assert jobs[1].job_name == expected_job_name_1


def test_plots_are_extracted_for_each_occurrence(mocker, mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    mock_method = mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements") 

    asreml_r_dpo.mesl()

    assert mock_method.call_count == 4


def test_plots_are_extracted_with_right_parameters(mocker, mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    mock_method = mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements") 

    asreml_r_dpo.mesl()
    
    # 4 occurrences in the mesl analysis request
    mock_method.assert_has_calls(
        calls=[
            call(occurrence_id="1"),
            call(occurrence_id="2"),
            call(occurrence_id="3"),
            call(occurrence_id="4"),
        ]
    )

def test_plot_measurements_are_extracted_for_each_trait(mocker, mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")

    mock_method = mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements") 
    
    asreml_r_dpo.mesl()

    assert mock_method.call_count == 8


def test_plot_measurements_are_extracted_with_right_parameters(mocker, mesl_analysis_request):
    

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    mock_method = mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements") 

    asreml_r_dpo.mesl()
    
    # 4 occurrences in the mesl analysis request
    mock_method.assert_has_calls(
        calls=[
            call(occurrence_id="1", trait_id="1"),
            call(occurrence_id="2", trait_id="1"),
            call(occurrence_id="3", trait_id="1"),
            call(occurrence_id="4", trait_id="1"),
            call(occurrence_id="1", trait_id="2"),
            call(occurrence_id="2", trait_id="2"),
            call(occurrence_id="3", trait_id="2"),
            call(occurrence_id="4", trait_id="2")
        ], any_order=True
    )


def test_mesl_job_data_file(mocker, mesl_analysis_request):
    pass
