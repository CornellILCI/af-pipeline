from unittest import TestCase
from unittest.mock import Mock, patch

import pandas as pd
from pandas._testing import assert_frame_equal

from conftest import (
    get_brapi_observation_units_response,
    get_test_plots
)

from data_reader.phenotype_data_brapi import PhenotypeDataBrapi


class TestPhenotypeDataBrapi(TestCase):

    @patch('data_reader.data_reader.requests.post')
    def test_get_plots(self, mock_post):

        mock_post.return_value.status_code = 200

        mock_post.return_value.json = Mock(side_effect=[
            get_brapi_observation_units_response()])

        plots_test_df = get_test_plots()

        plots_result_df = PhenotypeDataBrapi(
            api_base_url="http://test").get_plots("testid")

        # assert dataframe is returned
        assert isinstance(plots_result_df, pd.DataFrame)

        plots_result_df = plots_result_df[plots_test_df.columns]

        print(plots_result_df)

        print(plots_test_df)

        assert_frame_equal(plots_result_df, plots_test_df)
