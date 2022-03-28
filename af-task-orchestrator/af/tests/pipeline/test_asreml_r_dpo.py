from af.pipeline.job_data import JobData
from af.pipeline.db.models import Property

from af.pipeline.asreml_r import dpo

import pytest
from unittest.mock import call

import pandas as pd


def test_dpo_run_for_mesl_method_called(mocker, analysis_request):

    exp_location_analysis_pattern_stub = Property(code="MESL")
    mocker.patch("af.pipeline.db.services.get_property", return_value=exp_location_analysis_pattern_stub)

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)

    mocker.patch("af.pipeline.asreml_r.dpo.AsremlRProcessData.mesl")

    jobs = asreml_r_dpo.run()

    asreml_r_dpo.mesl.assert_called_once()


def test_dpo_run_returns_job_data(mesl_analysis_request):

    analysis_request, _, _ = mesl_analysis_request

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)
    assert type(asreml_r_dpo.mesl()) is list


def test_dpo_run_returns_jobs(mesl_analysis_request):

    analysis_request, _, _ = mesl_analysis_request

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)
    jobs = asreml_r_dpo.mesl()
    assert len(jobs) > 0


def test_dpo_run_returns_job_list(mesl_analysis_request):

    analysis_request, _, _ = mesl_analysis_request

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)
    jobs = asreml_r_dpo.mesl()
    for job in jobs:
        assert type(job) is JobData


def test_dpo_run_for_mesl_num_jobs(mesl_analysis_request):

    analysis_request, _, _ = mesl_analysis_request

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)

    jobs = asreml_r_dpo.mesl()

    # expected_num_jobs = num_locations * num_traits
    assert len(jobs) == 4


def test_job_names(mesl_analysis_request):

    analysis_request, _, _ = mesl_analysis_request

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)

    jobs = asreml_r_dpo.mesl()

    expected_job_names = {"test_id_mesl_1_1", "test_id_mesl_2_1", "test_id_mesl_1_2", "test_id_mesl_2_2"}
    actual_job_names = set()
    for job in jobs:
        actual_job_names.add(job.job_name)

    assert expected_job_names == actual_job_names


def test_plots_are_extracted_for_each_occurrence(mesl_analysis_request):

    analysis_request, plots_mock, _ = mesl_analysis_request

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)

    asreml_r_dpo.mesl()

    assert plots_mock.call_count == 4


def test_plots_are_extracted_with_right_parameters(mesl_analysis_request):

    analysis_request, plots_mock, _ = mesl_analysis_request

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)

    asreml_r_dpo.mesl()

    # 4 occurrences in the mesl analysis request
    plots_mock.assert_has_calls(
        calls=[
            call(occurrence_id="1"),
            call(occurrence_id="2"),
            call(occurrence_id="3"),
            call(occurrence_id="4"),
        ]
    )


def test_plot_measurements_are_extracted_for_each_trait(mesl_analysis_request):

    analysis_request, _, plot_data_mock = mesl_analysis_request

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)

    asreml_r_dpo.mesl()

    assert plot_data_mock.call_count == 8


def test_plot_measurements_are_extracted_with_right_parameters(mesl_analysis_request):

    analysis_request, _, plot_data_mock = mesl_analysis_request

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)

    asreml_r_dpo.mesl()

    # 4 occurrences in the mesl analysis request
    plot_data_mock.assert_has_calls(
        calls=[
            call(occurrence_id="1", trait_id="1"),
            call(occurrence_id="2", trait_id="1"),
            call(occurrence_id="3", trait_id="1"),
            call(occurrence_id="4", trait_id="1"),
            call(occurrence_id="1", trait_id="2"),
            call(occurrence_id="2", trait_id="2"),
            call(occurrence_id="3", trait_id="2"),
            call(occurrence_id="4", trait_id="2"),
        ],
        any_order=True,
    )


def test_data_file_exisits(mesl_analysis_request):

    import os

    analysis_request, _, plot_data_mock = mesl_analysis_request

    plot_data_mock.return_value = pd.DataFrame()

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)

    jobs = asreml_r_dpo.mesl()
    for job in jobs:
        assert os.path.isfile(job.data_file)


@pytest.mark.skip(reason="need to test other stuffs before this.")
def test_mesl_job_data_file(mocker, mesl_analysis_request):

    plots_columns = [
        "plot_id",
        "expt_id",
        "loc_id",
        "occurr_id",
        "entry_id",
        "entry_name",
        "entry_type",
        "pa_x",
        "pa_y",
        "rep_factor",
        "blk",
        "plot_qc",
    ]
    plots_stub = [
        DataFrame(
            columns=plots_columns,
            data=[
                [2909, 1, 1, 1, 1, "entry_name1", "entry_type", 1, 1, 1, 1, "G"],
                [2910, 1, 1, 1, 2, "entry_name2", "entry_type", 1, 2, 1, 1, "G"],
            ],
        ),
        DataFrame(
            columns=plots_columns,
            data=[
                [2911, 1, 2, 2, 3, "entry_name3", "entry_type", 1, 1, 1, 1, "G"],
                [2912, 1, 2, 2, 4, "entry_nam4", "entry_type", 1, 2, 1, 1, "G"],
            ],
        ),
        DataFrame(
            columns=plots_columns,
            data=[
                [2913, 2, 1, 3, 5, "entry_name5", "entry_type", 1, 1, 1, 1, "G"],
                [2914, 2, 1, 3, 6, "entry_name6", "entry_type", 1, 2, 1, 1, "G"],
            ],
        ),
        DataFrame(
            columns=plots_columns,
            data=[
                [2915, 2, 2, 4, 7, "entry_name7", "entry_type", 1, 1, 1, 1, "G"],
                [2916, 2, 2, 4, 8, "entry_name8", "entry_type", 1, 2, 1, 1, "G"],
            ],
        ),
    ]

    plot_measurements_columns = ["plot_id", "trait_id", "trait_qc", "trait_value"]

    plot_measurements_stub = [
        DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2909, 1, "G", 6.155850575],
                [2910, 1, "G", 6.751358238],
            ],
        ),
        DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2909, 2, "G", 6.155850575],
                [2910, 2, "G", 6.751358238],
            ],
        ),
        DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2911, 1, "G", 6.155850575],
                [2912, 1, "G", 6.751358238],
            ],
        ),
        DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2911, 2, "G", 6.155850575],
                [2912, 2, "G", 6.751358238],
            ],
        ),
        DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2913, 1, "G", 6.155850575],
                [2914, 1, "G", 6.751358238],
            ],
        ),
        DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2913, 2, "G", 6.155850575],
                [2914, 2, "G", 6.751358238],
            ],
        ),
        DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2915, 1, "G", 6.155850575],
                [2916, 1, "G", 6.751358238],
            ],
        ),
        DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2915, 2, "G", 6.155850575],
                [2916, 2, "G", 6.751358238],
            ],
        ),
    ]

    mocker.patch("af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots", side_effect=plots_stub)
    mocker.patch(
        "af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements",
        side_effect=plot_measurements_stub,
    )

    expected_job_data_files = {
        (
            "loc,expt,entry,plot,col,row,rep,trait_abbrev_1\n"
            "1,1,1,2909,1,1,1,6.155850575\n"
            "1,1,2,2910,1,2,1,6.751358238\n"
            "1,2,5,2913,1,1,1,6.155850575\n"
            "1,2,6,2914,1,2,1,6.751358238\n"
        ),
        (
            "loc,expt,entry,plot,col,row,rep,trait_abbrev_2\n"
            "1,1,1,2909,1,1,1,6.155850575\n"
            "1,1,2,2910,1,2,1,6.751358238\n"
            "1,2,5,2913,1,1,1,6.155850575\n"
            "1,2,6,2914,1,2,1,6.751358238\n"
        ),
        (
            "loc,expt,entry,plot,col,row,rep,trait_abbrev_1\n"
            "2,1,3,2911,1,1,1,6.155850575\n"
            "2,1,4,2912,1,2,1,6.751358238\n"
            "2,2,7,2915,1,1,1,6.155850575\n"
            "2,2,8,2916,1,2,1,6.751358238\n"
        ),
        (
            "loc,expt,entry,plot,col,row,rep,trait_abbrev_1\n"
            "2,1,3,2911,1,1,1,6.155850575\n"
            "2,1,4,2912,1,2,1,6.751358238\n"
            "2,2,7,2915,1,1,1,6.155850575\n"
            "2,2,8,2916,1,2,1,6.751358238\n"
        ),
    }
