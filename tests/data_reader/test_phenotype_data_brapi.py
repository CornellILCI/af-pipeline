from unittest import TestCase
from unittest.mock import Mock, patch

import pandas as pd
from pandas._testing import assert_frame_equal

from conftest import (
    get_brapi_observation_units_response,
    get_brapi_observations_response,
    get_brapi_studies_response,
    get_test_plots,
    get_test_plot_measurements,
    get_test_occurrence_brapi,
)

from data_reader.phenotype_data_brapi import PhenotypeDataBrapi


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
