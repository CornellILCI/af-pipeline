from unittest import TestCase
from unittest.mock import patch

import pandas as pd
from pandas._testing import assert_frame_equal

from conftest import (
    get_ebs_plots_response,
    get_test_plots,
    get_ebs_unauthorized_error_response)

from exceptions import DataReaderException


class TestPhenotypeDataEbs(TestCase):

    @patch('data_reader.data_reader.requests.post')
    def test_get_plots_by_occurrence_id(self, mock_post):

        from data_reader.phenotype_data_ebs import PhenotypeDataEbs

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = (
            get_ebs_plots_response())

        plots_test_df = get_test_plots()

        plots_result_df = PhenotypeDataEbs(
            api_base_url="http://test").get_plots_by_occurrence_id(4)

        # assert dataframe is returned
        assert isinstance(plots_result_df, pd.DataFrame)

        assert_frame_equal(plots_result_df, plots_test_df)

        mock_post.return_value.status_code = 401
        mock_post.return_value.json.return_value = (
            get_ebs_unauthorized_error_response)

        with self.assertRaises(DataReaderException):
            plots_result_df = PhenotypeDataEbs(
                api_base_url="http://test").get_plots_by_occurrence_id(4)

        with self.assertRaises(DataReaderException):
            plots_result_df = PhenotypeDataEbs(
                api_base_url="htp://test").get_plots_by_occurrence_id(4)

    @patch('data_reader.data_reader.requests.get')
    def test_get_occurrence(self, mock_get):
        pass
