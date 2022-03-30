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


@pytest.mark.parametrize(
    "_analysis_request",
    [pytest.lazy_fixture("mesl_analysis_request"), pytest.lazy_fixture("meml_analysis_request")],
)
def test_dpo_run_returns_job_list(_analysis_request):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)
    jobs = asreml_r_dpo.run()
    for job in jobs:
        assert type(job) is JobData


@pytest.mark.parametrize(
    "_analysis_request, expected_num_jobs",
    [(pytest.lazy_fixture("mesl_analysis_request"), 4), (pytest.lazy_fixture("meml_analysis_request"), 2)],
)
def test_dpo_run_for_num_jobs(_analysis_request, expected_num_jobs):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)

    jobs = asreml_r_dpo.run()

    assert len(jobs) == expected_num_jobs


@pytest.mark.parametrize(
    "_analysis_request, expected_job_names",
    [
        (
            pytest.lazy_fixture("mesl_analysis_request"),
            ["test_id_mesl_1_1", "test_id_mesl_1_2", "test_id_mesl_2_1", "test_id_mesl_2_2"],
        ),
        (pytest.lazy_fixture("meml_analysis_request"), ["test_id_meml_1", "test_id_meml_2"]),
    ],
)
def test_job_names(_analysis_request, expected_job_names):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)

    jobs = asreml_r_dpo.run()

    for i in range(len(jobs)):
        assert expected_job_names[i] == jobs[i].job_name


@pytest.mark.parametrize(
    "_analysis_request, expected_num_plots_extraction",
    [(pytest.lazy_fixture("mesl_analysis_request"), 4), (pytest.lazy_fixture("meml_analysis_request"), 4)],
)
def test_plots_are_extracted_for_each_occurrence(_analysis_request, expected_num_plots_extraction, me_plots_mock):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)

    asreml_r_dpo.run()

    assert me_plots_mock.call_count == expected_num_plots_extraction


@pytest.mark.parametrize(
    "_analysis_request",
    [pytest.lazy_fixture("mesl_analysis_request"), pytest.lazy_fixture("meml_analysis_request")],
)
def test_plots_are_extracted_with_right_parameters(
    _analysis_request,
    me_plots_mock,
):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)

    asreml_r_dpo.run()

    # 4 occurrences in the mesl analysis request
    me_plots_mock.assert_has_calls(
        calls=[
            call(occurrence_id="1"),
            call(occurrence_id="2"),
            call(occurrence_id="3"),
            call(occurrence_id="4"),
        ]
    )


@pytest.mark.parametrize(
    "_analysis_request",
    [pytest.lazy_fixture("mesl_analysis_request"), pytest.lazy_fixture("meml_analysis_request")],
)
def test_plot_measurements_are_extracted_for_each_occurrence_trait(_analysis_request, me_plot_measurements_mock):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)

    asreml_r_dpo.run()

    assert me_plot_measurements_mock.call_count == 8


@pytest.mark.parametrize(
    "_analysis_request",
    [pytest.lazy_fixture("mesl_analysis_request"), pytest.lazy_fixture("meml_analysis_request")],
)
def test_plot_measurements_are_extracted_with_right_parameters(_analysis_request, me_plot_measurements_mock):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)

    asreml_r_dpo.run()

    # 4 occurrences in the mesl analysis request
    me_plot_measurements_mock.assert_has_calls(
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


@pytest.mark.parametrize(
    "_analysis_request",
    [pytest.lazy_fixture("mesl_analysis_request"), pytest.lazy_fixture("meml_analysis_request")],
)
def test_data_file_exisits(_analysis_request):

    import os

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)

    jobs = asreml_r_dpo.run()
    for job in jobs:
        assert os.path.isfile(job.data_file)


@pytest.mark.parametrize(
    "_analysis_request, expected_job_data",
    [
        (
            pytest.lazy_fixture("mesl_analysis_request"),
            [
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
            ],
        ),
        (
            pytest.lazy_fixture("meml_analysis_request"),
            [
                (
                    "loc,expt,entry,plot,col,row,rep,trait_abbrev_1\n"
                    "1,1,1,2909,1,1,1,6.155850575\n"
                    "1,1,2,2910,1,2,1,6.751358238\n"
                    "2,1,3,2911,1,1,1,6.155850575\n"
                    "2,1,4,2912,1,2,1,6.751358238\n"
                    "1,2,5,2913,1,1,1,6.155850575\n"
                    "1,2,6,2914,1,2,1,6.751358238\n"
                    "2,2,7,2915,1,1,1,6.155850575\n"
                    "2,2,8,2916,1,2,1,6.751358238\n"
                ),
                (
                    "loc,expt,entry,plot,col,row,rep,trait_abbrev_2\n"
                    "1,1,1,2909,1,1,1,6.155850575\n"
                    "1,1,2,2910,1,2,1,6.751358238\n"
                    "2,1,3,2911,1,1,1,6.155850575\n"
                    "2,1,4,2912,1,2,1,6.751358238\n"
                    "1,2,5,2913,1,1,1,6.155850575\n"
                    "1,2,6,2914,1,2,1,6.751358238\n"
                    "2,2,7,2915,1,1,1,6.155850575\n"
                    "2,2,8,2916,1,2,1,6.751358238\n"
                ),
            ],
        ),
    ],
)
def test_job_data_file(_analysis_request, expected_job_data):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)

    jobs = asreml_r_dpo.run()

    for i in range(len(jobs)):

        with open(jobs[i].data_file) as data_f_:

            file_content = data_f_.read()

            assert file_content == expected_job_data[i]


@pytest.mark.parametrize(
    "_analysis_request, expected_job_formulas",
    [
        (
            pytest.lazy_fixture("mesl_analysis_request"),
            [
                "trait_abbrev_1 ~ mu rep !r entry !f mv",
                "trait_abbrev_2 ~ mu rep !r entry !f mv",
                "trait_abbrev_1 ~ mu rep !r entry !f mv",
                "trait_abbrev_2 ~ mu rep !r entry !f mv",
            ],
        ),
        (
            pytest.lazy_fixture("meml_analysis_request"),
            [
                "trait_abbrev_1 ~ mu rep !r entry !f mv",
                "trait_abbrev_2 ~ mu rep !r entry !f mv",
            ],
        ),
    ],
)
def test_formula_added_to_job_params(_analysis_request, expected_job_formulas):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)

    jobs = asreml_r_dpo.run()

    for i in range(len(jobs)):
        assert jobs[i].job_params.formula == expected_job_formulas[i]


@pytest.mark.parametrize(
    "_analysis_request",
    [
        pytest.lazy_fixture("mesl_analysis_request"),
        pytest.lazy_fixture("meml_analysis_request"),
    ],
)
def test_residual_added_to_job_params(_analysis_request, analysis_residual):

    asreml_r_dpo = dpo.AsremlRProcessData(_analysis_request)

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
