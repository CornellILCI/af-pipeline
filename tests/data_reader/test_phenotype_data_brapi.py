from unittest import TestCase
from unittest.mock import Mock, patch

import pandas as pd
from pandas._testing import assert_frame_equal

from conftest import (
    read_mock_json_file
)

from models import Occurrence

from data_reader.phenotype_data_brapi import PhenotypeDataBrapi

import json


def get_brapi_observation_units_response(page_size=None,
                                         total_pages=1,
                                         ):
    """ returns a mock brapi response for observation units.
    """
    return read_mock_json_file(
        "tests/data_reader/brapi_observationunits_mock_response.json")


def get_brapi_observations_response():
    """ returns a mock brapi response for observation units """

    return read_mock_json_file(
        "tests/data_reader/brapi_observations_mock_response.json")


def get_brapi_studies_response():
    """ returns a mock brapi response for studies """

    return read_mock_json_file(
        "tests/data_reader/brapi_studies_mock_response.json")


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


def get_test_occurrence_brapi() -> Occurrence:
    test_occurrence = {
        "occurrence_id": 7,
        "occurrence_name": "test_occurrence",
        "experiment_id": 4,
        "experiment_name": "test_experiment",
        "location_id": 6,
        "location": "test_location",
    }
    return Occurrence(**test_occurrence)


class TestPhenotypeDataBrapi(TestCase):

    @patch('data_reader.data_reader.requests.get')
    def test_get_plots(self, mock_get):

        mock_get.return_value.status_code = 200

        mock_get.return_value.json = Mock(side_effect=[
            get_brapi_observation_units_response()])

        plots_test_df = get_test_plots()

        plots_result_df = PhenotypeDataBrapi(
            api_base_url="http://test").get_plots("testid")

        # assert dataframe is returned
        assert isinstance(plots_result_df, pd.DataFrame)

        # arrange columns
        plots_result_df = plots_result_df[plots_test_df.columns]

        assert_frame_equal(plots_result_df,
                           plots_test_df.astype(str))

    @patch('data_reader.data_reader.requests.get')
    def test_get_plots_with_pages(self, mock_get):

        PhenotypeDataBrapi.brapi_list_page_size = 2

        mock_get.return_value.status_code = 200

        _pagination = """{
            "pageSize": 2,
            "totalPages": 2,
            "currentPage": 0,
            "totalCount": 3
        }"""

        first_page = get_brapi_observation_units_response()

        pagination = json.loads(_pagination)
        first_page["metadata"]["pagination"] = pagination

        second_page = get_brapi_observation_units_response()
        pagination = json.loads(_pagination)
        pagination["currentPage"] = 1
        second_page["metadata"]["pagination"] = pagination
        second_page["result"]["data"].pop()
        second_page_item = second_page["result"]["data"][0]
        second_page_item["observationUnitDbId"] = 2911

        mock_get.return_value.json = Mock(
            side_effect=[first_page, second_page])

        # expected result
        plots_expected = get_test_plots()
        plots_expected_page_2 = plots_expected.iloc[0].copy()
        plots_expected_page_2["plot_id"] = 2911
        plots_expected = plots_expected.append(plots_expected_page_2)

        plots_result = PhenotypeDataBrapi(
            api_base_url="http://test").get_plots("testid")

        # assert dataframe is returned
        assert isinstance(plots_result, pd.DataFrame)

        print(plots_result)

        # arrange columns
        plots_result = plots_result[plots_expected.columns]

        assert_frame_equal(plots_result,
                           plots_expected.astype(str))

    @patch('data_reader.data_reader.requests.get')
    def test_get_plot_measurements(self, mock_get):

        mock_get.return_value.status_code = 200

        mock_get.return_value.json = Mock(side_effect=[
            get_brapi_observations_response()])

        plot_measurements_test_df = get_test_plot_measurements()

        plot_measurements_result_df = PhenotypeDataBrapi(
            api_base_url="http://test").get_plot_measurements("testid")

        # assert dataframe is returned
        assert isinstance(plot_measurements_result_df, pd.DataFrame)

        plot_measurements_result_df = plot_measurements_result_df[
            plot_measurements_test_df.columns]

        assert_frame_equal(plot_measurements_result_df,
                           plot_measurements_test_df.astype(str))

    @patch('data_reader.data_reader.requests.get')
    def test_get_plots_measurements_with_pages(self, mock_get):

        PhenotypeDataBrapi.brapi_list_page_size = 2

        mock_get.return_value.status_code = 200

        _pagination = """{
            "pageSize": 2,
            "totalPages": 2,
            "currentPage": 0,
            "totalCount": 3
        }"""

        first_page = get_brapi_observations_response()

        pagination = json.loads(_pagination)
        first_page["metadata"]["pagination"] = pagination

        second_page = get_brapi_observations_response()
        pagination = json.loads(_pagination)
        pagination["currentPage"] = 1
        second_page["metadata"]["pagination"] = pagination
        second_page["result"]["data"].pop()
        second_page_item = second_page["result"]["data"][0]
        second_page_item["observationUnitDbId"] = 2911

        mock_get.return_value.json = Mock(
            side_effect=[first_page, second_page])

        plot_measurements_expected = get_test_plot_measurements()
        plot_measurements_expected_page_2 = (
            plot_measurements_expected.iloc[0].copy())
        plot_measurements_expected_page_2["plot_id"] = 2911
        plot_measurements_expected = plot_measurements_expected.append(
            plot_measurements_expected_page_2)

        plot_measurements_result = PhenotypeDataBrapi(
            api_base_url="http://test").get_plot_measurements("testid")

        # assert dataframe is returned
        assert isinstance(plot_measurements_result, pd.DataFrame)

        # arrange columns
        plot_measurements_result = (
            plot_measurements_result[plot_measurements_expected.columns])

        assert_frame_equal(plot_measurements_result,
                           plot_measurements_expected.astype(str))

    @patch('data_reader.data_reader.requests.get')
    def test_get_occurrence(self, mock_get):
        from data_reader.phenotype_data_brapi import PhenotypeDataBrapi

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = (
            get_brapi_studies_response())
        test_occurrence = get_test_occurrence_brapi()

        occurrence_result = (
            PhenotypeDataBrapi(api_base_url="http://test")
        ).get_occurrence(occurrence_id=test_occurrence.occurrence_id)

        for field, value in test_occurrence:
            assert value == occurrence_result.dict()[field]
