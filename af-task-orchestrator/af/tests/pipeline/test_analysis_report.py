import os

import pandas as pd
import pytest
from af.pipeline import analysis_report
from pandas._testing import assert_frame_equal


@pytest.fixture
def report_file(temp_dir):
    report_file = os.path.join(temp_dir.name, "report.xlsx")
    return report_file


@pytest.fixture
def predictions_df():

    return pd.DataFrame(
        columns=["job_id", "entry", "loc", "value", "std_error", "e_code", "num_factors"],
        data=[
            [1, 1, None, 1, 1.4, "E", 1],
            [1, 2, None, 1, 1.5, "E", 1],
            [1, None, 1, 1, 1.4, "E", 1],
            [1, 1, 1, 1, 1.5, "E", 2],
            [1, 2, 1, 1, 1.5, "E", 2],
        ],
    )


@pytest.fixture
def entry_only_predictions_df():

    return pd.DataFrame(
        columns=["job_id", "entry", "value", "std_error", "e_code", "num_factors"],
        data=[
            [1, 1, 1, 1.4, "E", 1],
            [1, 2, 1, 1.5, "E", 1],
        ],
    )


@pytest.fixture
def location_only_predictions_df():

    return pd.DataFrame(
        columns=["job_id", "loc", "value", "std_error", "e_code", "num_factors"],
        data=[
            [1, 1, 1, 1.4, "E", 1],
        ],
    )


@pytest.fixture
def model_stat():

    return {
        "job_id": 1,
        "LogL": "x",
        "aic": "x",
        "bic": "x",
        "components": "x",
        "conclusion": "y",
        "is_converged": False,
    }


@pytest.fixture
def metadata_df():

    return pd.DataFrame(
        columns=[
            "entry_id",
            "entry_name",
            "entry_type",
            "experiment_id",
            "experiment_name",
            "location_name",
            "location_id",
            "trait_abbreviation",
        ],
        data=[
            [1, "entry1", "test", 1, "experiment1", "loc1", 1, "testtrait"],
            [2, "entry2", "check", 1, "experiment1", "loc1", 1, "testtrait"],
        ],
    )


def test_write_predictions_all_sheets(report_file, predictions_df, metadata_df):

    analysis_report.write_predictions(report_file, location_only_predictions_df, metadata_df)

    assert os.path.isfile(report_file)

    # assert entry report
    output_entry_report = pd.read_excel(report_file, sheet_name=analysis_report.ENTRY_SHEET_NAME)
    expected_entry_report = pd.DataFrame(
        columns=[
            "job_id",
            "experiment_id",
            "experiment_name",
            "trait_abbreviation",
            "entry_id",
            "entry_name",
            "entry_type",
            "value",
            "std_error",
            "location_id"
        ],
        data=[
            [1, 1, "experiment1", "testtrait", 1, "entry1", "test", 1, 1.4, 1],
            [1, 1, "experiment1", "testtrait", 2, "entry2", "check", 1, 1.5, 1],
        ],
    )
    assert_frame_equal(output_entry_report, expected_entry_report, check_dtype=False)

    # assert location report
    output_location_report = pd.read_excel(report_file, sheet_name=analysis_report.LOCATION_SHEET_NAME)
    expected_location_report = pd.DataFrame(
        columns=["job_id", "trait_abbreviation", "location_id", "location_name", "value", "std_error"],
        data=[
            [1, "testtrait", 1, "loc1", 1, 1.4],
        ],
    )

    assert_frame_equal(output_location_report, expected_location_report, check_dtype=False)

    # assert entry x location report
    output_entry_location_report = pd.read_excel(report_file, sheet_name=analysis_report.ENTRY_LOCATION_SHEET_NAME)
    expected_entry_location_report = pd.DataFrame(
        columns=[
            "job_id",
            "trait_abbreviation",
            "entry_id",
            "entry_name",
            "location_id",
            "location_name",
            "value",
            "std_error",
        ],
        data=[
            [1, "testtrait", 1, "entry1", 1, "loc1", 1, 1.5],
            [1, "testtrait", 2, "entry2", 1, "loc1", 1, 1.5],
        ],
    )
    assert_frame_equal(output_entry_location_report, expected_entry_location_report, check_dtype=False)


def test_write_predictions_entry_only(report_file, entry_only_predictions_df, metadata_df):

    analysis_report.write_predictions(report_file, location_only_predictions_df, metadata_df)

    assert os.path.isfile(report_file)

    # assert entry report
    output_entry_report = pd.read_excel(report_file, sheet_name=analysis_report.ENTRY_SHEET_NAME)
    expected_entry_report = pd.DataFrame(
        columns=[
            "job_id",
            "experiment_id",
            "experiment_name",
            "trait_abbreviation",
            "entry_id",
            "entry_name",
            "entry_type",
            "value",
            "std_error",
            "location_id"
        ],
        data=[
            [1, 1, "experiment1", "testtrait", 1, "entry1", "test", 1, 1.4, 1],
            [1, 1, "experiment1", "testtrait", 2, "entry2", "check", 1, 1.5, 1],
        ],
    )

    assert_frame_equal(output_entry_report, expected_entry_report, check_dtype=False)

    # test append to entry report
    analysis_report.write_predictions(report_file, entry_only_predictions_df, metadata_df)
    output_entry_report = pd.read_excel(report_file, sheet_name=analysis_report.ENTRY_SHEET_NAME)
    expected_entry_report = pd.concat([expected_entry_report, expected_entry_report], ignore_index=True)

    assert_frame_equal(output_entry_report, expected_entry_report, check_dtype=False)


def test_write_predictions_location_only(report_file, location_only_predictions_df, metadata_df):

    analysis_report.write_predictions(report_file, location_only_predictions_df, metadata_df)

    assert os.path.isfile(report_file)

    # assert entry report
    output_entry_report = pd.read_excel(report_file, sheet_name=analysis_report.LOCATION_SHEET_NAME)
    expected_entry_report = pd.DataFrame(
        columns=[
            "job_id",
            "trait_abbreviation",
            "location_id",
            "location_name",
            "value",
            "std_error",
        ],
        data=[
            [1, "testtrait", 1, "loc1", 1, 1.4],
        ],
    )

    assert_frame_equal(output_entry_report, expected_entry_report, check_dtype=False)


def test_write_predictions_location_only(report_file, model_stat, metadata_df):

    analysis_report.write_model_stat(report_file, model_stat, metadata_df, {"log_lik": "LogL"})

    assert os.path.isfile(report_file)

    # assert entry report
    output_modelstat_report = pd.read_excel(report_file, sheet_name=analysis_report.MODEL_STAT_SHEET_NAME)
    expected_modelstat_report = pd.DataFrame(
        columns=[
            "job_id",
            "experiment_name",
            "trait_abbreviation",
            "location_name",
            "LogL",
            "aic",
            "bic",
            "components",
            "conclusion",
            "is_converged",
        ],
        data=[
            [1, "experiment1", "testtrait", "loc1", "x", "x", "x", "x", "y", False],
        ],
    )

    assert_frame_equal(output_modelstat_report, expected_modelstat_report, check_dtype=False)
