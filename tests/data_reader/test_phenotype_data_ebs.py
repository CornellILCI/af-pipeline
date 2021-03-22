from unittest import TestCase
from unittest.mock import Mock, patch

import pandas as pd
from pandas._testing import assert_frame_equal

from conftest import (
    read_mock_json_file
)

from exceptions import DataReaderException

from models import Occurrence

from data_reader.phenotype_data_ebs import PhenotypeDataEbs

import json


def get_ebs_plots_response():
    """ returns a plots response json object to be used as mock """

    return read_mock_json_file("tests/data_reader/plots_mock_response.json")


def get_ebs_occurrence_response():
    """ returns a occurrence response json object to be used as mock """

    return read_mock_json_file(
        "tests/data_reader/occurrence_mock_response.json")


def get_ebs_unauthorized_error_response():
    error_response = """{
        "metadata": {
            "pagination": {
                "pageSize": null,
                "totalCount": null,
                "currentPage": null,
                "totalPages": null
            },
            "status": [
                {
                    "message": "",
                    "messageType": "Unauthorized"
                }
            ],
            "datafiles": []
        },
        "result": {
            "data": []
        }
    }"""
    return json.loads(error_response)


def get_test_plots() -> pd.DataFrame:
    """ return a mock plots dataframe """

    columns = ["plot_id", "experiment_id", "location_id", "occurrence_id",
               "entry_id", "pa_x", "pa_y", "rep_factor",
               "blk", "plot_qc"]
    data = [
        [2909, 4, 6, 7, 180, 3, 5, 1, 1, "G"],
        [2910, 4, 6, 7, 103, 4, 5, 1, 1, "G"],
    ]
    return pd.DataFrame(data, columns=columns)


def get_test_plot_measurements() -> pd.DataFrame:
    """ return a mock plot measurement dataframe"""

    columns = ["plot_id", "trait_id", "trait_qc", "trait_value"]
    data = [
        [2909, 1, "G", 6.155850575],
        [2910, 1, "G", 6.751358238],
    ]
    return pd.DataFrame(data, columns=columns)


def get_test_occurrence() -> Occurrence:
    test_occurrence = {
        "occurrence_id": 7,
        "occurrence_name": "test_occurrence",
        "experiment_id": 4,
        "experiment_name": "test_experiment",
        "location_id": 6,
        "location": "test_location",
        "rep_count": 1,
        "entry_count": 4,
        "plot_count": 2
    }
    return Occurrence(**test_occurrence)


class TestPhenotypeDataEbs(TestCase):

    @patch('data_reader.data_reader.requests.post')
    def test_get_plots(self, mock_post):

        mock_post.return_value.status_code = 200

        mock_post.return_value.json = Mock(side_effect=[
            get_ebs_plots_response(),
            get_ebs_occurrence_response()])

        plots_test_df = get_test_plots().astype(str)

        plots_result_df = PhenotypeDataEbs(
            api_base_url="http://test").get_plots("testid")

        # assert dataframe is returned
        assert isinstance(plots_result_df, pd.DataFrame)

        plots_result_df = plots_result_df[plots_test_df.columns]

        assert_frame_equal(plots_result_df, plots_test_df)

    @patch('data_reader.data_reader.requests.post')
    def test_get_plots_raise_exception_for_401(self, mock_post):

        mock_post.return_value.status_code = 401
        mock_post.return_value.json.reset_mock(
            side_effect=get_ebs_unauthorized_error_response)

        with self.assertRaises(DataReaderException):
            PhenotypeDataEbs(
                api_base_url="http://test"
            ).get_plots(occurrence_id="testid")

    def test_get_plots_raise_exception_for_invalid_url(self):
        with self.assertRaises(DataReaderException):
            PhenotypeDataEbs(
                api_base_url="htp").get_plots("testid")

    @patch('data_reader.data_reader.requests.post')
    def test_get_occurrence(self, mock_post):
        from data_reader.phenotype_data_ebs import PhenotypeDataEbs

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = (
            get_ebs_occurrence_response())
        test_occurrence = get_test_occurrence()

        occurrence_result = (
            PhenotypeDataEbs(api_base_url="http://test")
        ).get_occurrence(occurrence_id=test_occurrence.occurrence_id)

        for field, value in test_occurrence:
            assert value == occurrence_result.dict()[field]
