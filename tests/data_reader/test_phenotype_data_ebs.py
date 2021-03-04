from unittest import TestCase
from unittest.mock import Mock, patch

import pandas as pd
from pandas._testing import assert_frame_equal

from conftest import (
    get_ebs_plots_response,
    get_ebs_occurrence_response,
    get_test_plots,
    get_test_occurrence,
    get_ebs_unauthorized_error_response)

from exceptions import DataReaderException

from data_reader.phenotype_data_ebs import PhenotypeDataEbs

class TestPhenotypeDataEbs(TestCase):

    @patch('data_reader.data_reader.requests.post')
    def test_get_plots(self, mock_post):


        mock_post.return_value.status_code = 200

        mock_post.return_value.json = Mock(side_effect=[
            get_ebs_plots_response(),
            get_ebs_occurrence_response()])

        plots_test_df = get_test_plots()

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
            plots_result_df = PhenotypeDataEbs(
                api_base_url="http://test"
            ).get_plots(occurrence_id="testid")


    def test_get_plots_raise_exception_for_invalid_url(self):
        with self.assertRaises(DataReaderException):
            plots_result_df = PhenotypeDataEbs(
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
