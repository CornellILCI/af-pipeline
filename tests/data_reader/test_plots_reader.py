import sys
import os

from unittest.mock import patch
import pandas as pd
from pandas._testing import assert_frame_equal

import json


def test_get_plots_by_occurrence():
    os.environ["B4R_API_BASE_URL"] = ""

    from data_reader.plots_reader import PlotsReader
    with patch('data_reader.plots_reader.requests.get') as mock_api_get:
        mock_api_get.return_value.ok = True

        mock_response_file_path = (
            os.path.join(sys.path[0], "plots_mock_response.json"))

        with open(mock_response_file_path) as mock_response_file:
            test_plot_data = json.load(mock_response_file)

        mock_api_get.return_value.json.return_value = test_plot_data

        plots_test_df = pd.DataFrame(test_plot_data["result"]["data"])

        plots_reader_df = PlotsReader().plots_get_by_occurrence_id(4)

        assert_frame_equal(plots_reader_df, plots_test_df)
