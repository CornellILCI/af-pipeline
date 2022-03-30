from unittest.mock import call

import pandas as pd
import pytest
from af.pipeline.asreml_r import dpo
from af.pipeline.db.models import Property
from af.pipeline.job_data import JobData


@pytest.mark.parametrize(
    "pattern, method_to_run",
    [
        (pytest.lazy_fixture("mesl_analysis_pattern"), "af.pipeline.asreml_r.dpo.AsremlRProcessData.mesl"),
        (pytest.lazy_fixture("meml_analysis_pattern"), "af.pipeline.asreml_r.dpo.AsremlRProcessData.meml"),
    ],
)
def test_dpo_run_correct_analysis_pattern_called(mocker, analysis_request, pattern, method_to_run):

    asreml_r_dpo = dpo.AsremlRProcessData(analysis_request)

    _mock = mocker.patch(method_to_run)

    jobs = asreml_r_dpo.run()

    _mock.assert_called_once()


@pytest.mark.parametrize(
    "_analysis_request",
    [pytest.lazy_fixture("mesl_analysis_request"), pytest.lazy_fixture("meml_analysis_request")],
)
def test_dpo_returns_jobs(_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)
    jobs = asreml_r_dpo.run()
    assert len(jobs) > 0


def test_dpo_run_returns_job_list(mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)
    jobs = asreml_r_dpo.run()
    for job in jobs:
        assert type(job) is JobData


def test_dpo_run_for_mesl_num_jobs(mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.run()

    # expected_num_jobs = num_locations * num_traits
    assert len(jobs) == 4


def test_job_names(mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.run()

    expected_job_names = ["test_id_mesl_1_1", "test_id_mesl_1_2", "test_id_mesl_2_1", "test_id_mesl_2_2"]

    for i in range(len(jobs)):
        assert expected_job_names[i] == jobs[i].job_name


def test_plots_are_extracted_for_each_occurrence(mesl_plots_mock, mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    asreml_r_dpo.run()

    assert mesl_plots_mock.call_count == 4


def test_plots_are_extracted_with_right_parameters(mesl_plots_mock, mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    asreml_r_dpo.run()

    # 4 occurrences in the mesl analysis request
    mesl_plots_mock.assert_has_calls(
        calls=[
            call(occurrence_id="1"),
            call(occurrence_id="2"),
            call(occurrence_id="3"),
            call(occurrence_id="4"),
        ]
    )


def test_plot_measurements_are_extracted_for_each_trait(mesl_plot_measurements_mock, mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    asreml_r_dpo.run()

    assert mesl_plot_measurements_mock.call_count == 8


def test_plot_measurements_are_extracted_with_right_parameters(mesl_plot_measurements_mock, mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    asreml_r_dpo.run()

    # 4 occurrences in the mesl analysis request
    mesl_plot_measurements_mock.assert_has_calls(
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

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.run()
    for job in jobs:
        assert os.path.isfile(job.data_file)


def test_mesl_job_data_file(mesl_analysis_request):

    expected_job_data_files = [
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
            "loc,expt,entry,plot,col,row,rep,trait_abbrev_2\n"
            "2,1,3,2911,1,1,1,6.155850575\n"
            "2,1,4,2912,1,2,1,6.751358238\n"
            "2,2,7,2915,1,1,1,6.155850575\n"
            "2,2,8,2916,1,2,1,6.751358238\n"
        ),
    ]

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.run()

    for i in range(len(jobs)):

        with open(jobs[i].data_file) as data_f_:

            file_content = data_f_.read()

            expected_data_file_content = expected_job_data_files[i]

            assert file_content == expected_data_file_content


def test_mesl_formula_added_to_job_params(mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.run()

    expected_analysis_formuals = [
        "trait_abbrev_1 ~ mu rep !r entry !f mv",
        "trait_abbrev_2 ~ mu rep !r entry !f mv",
        "trait_abbrev_1 ~ mu rep !r entry !f mv",
        "trait_abbrev_2 ~ mu rep !r entry !f mv",
    ]

    for i in range(len(jobs)):
        assert jobs[i].job_params.formula == expected_analysis_formuals[i]


def test_mesl_residual_added_to_job_params(analysis_residual, mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.run()

    for job in jobs:
        assert job.job_params.residual == analysis_residual.statement


def test_mesl_prediction_added_to_job_params(analysis_prediction, mesl_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.run()

    for job in jobs:
        assert analysis_prediction.statement in job.job_params.predictions


def test_mesl_metadata_file_created(mesl_analysis_request):

    import os

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.run()
    for job in jobs:
        assert os.path.isfile(job.metadata_file)


def test_mesl_metadata_file(mesl_analysis_request):

    expected_metadata = [
        (
            "entry_id\tentry_name\tentry_type\texperiment_id\texperiment_name\tlocation_name\tlocation_id\ttrait_abbreviation\n"
            "1\tentry_name1\tentry_type\t1\tname1\tloc1\t1\ttrait_abbrev_1\n"
            "2\tentry_name2\tentry_type\t1\tname1\tloc1\t1\ttrait_abbrev_1\n"
            "5\tentry_name5\tentry_type\t2\tname2\tloc1\t1\ttrait_abbrev_1\n"
            "6\tentry_name6\tentry_type\t2\tname2\tloc1\t1\ttrait_abbrev_1\n"
        ),
        (
            "entry_id\tentry_name\tentry_type\texperiment_id\texperiment_name\tlocation_name\tlocation_id\ttrait_abbreviation\n"
            "1\tentry_name1\tentry_type\t1\tname1\tloc1\t1\ttrait_abbrev_2\n"
            "2\tentry_name2\tentry_type\t1\tname1\tloc1\t1\ttrait_abbrev_2\n"
            "5\tentry_name5\tentry_type\t2\tname2\tloc1\t1\ttrait_abbrev_2\n"
            "6\tentry_name6\tentry_type\t2\tname2\tloc1\t1\ttrait_abbrev_2\n"
        ),
        (
            "entry_id\tentry_name\tentry_type\texperiment_id\texperiment_name\tlocation_name\tlocation_id\ttrait_abbreviation\n"
            "3\tentry_name3\tentry_type\t1\tname1\tloc2\t2\ttrait_abbrev_1\n"
            "4\tentry_name4\tentry_type\t1\tname1\tloc2\t2\ttrait_abbrev_1\n"
            "7\tentry_name7\tentry_type\t2\tname2\tloc2\t2\ttrait_abbrev_1\n"
            "8\tentry_name8\tentry_type\t2\tname2\tloc2\t2\ttrait_abbrev_1\n"
        ),
        (
            "entry_id\tentry_name\tentry_type\texperiment_id\texperiment_name\tlocation_name\tlocation_id\ttrait_abbreviation\n"
            "3\tentry_name3\tentry_type\t1\tname1\tloc2\t2\ttrait_abbrev_2\n"
            "4\tentry_name4\tentry_type\t1\tname1\tloc2\t2\ttrait_abbrev_2\n"
            "7\tentry_name7\tentry_type\t2\tname2\tloc2\t2\ttrait_abbrev_2\n"
            "8\tentry_name8\tentry_type\t2\tname2\tloc2\t2\ttrait_abbrev_2\n"
        ),
    ]

    asreml_r_dpo = dpo.AsremlRProcessData(mesl_analysis_request)

    jobs = asreml_r_dpo.run()

    for i in range(len(jobs)):

        with open(jobs[i].metadata_file) as data_f_:

            file_content = data_f_.read()

            assert file_content == expected_metadata[i]
