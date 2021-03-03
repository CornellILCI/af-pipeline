import sys
import os

from unittest.mock import patch
import pandas as pd
from pandas._testing import assert_frame_equal

import json


@patch('data_reader.phenotype_data_ebs.requests.get')
def test_get_plots_by_occurrence_id(mock_get_request):

    from data_reader.phenotype_data_ebs import PhenotypeDataEbs

    mock_get_request.return_value.ok = True

    mock_response_file_path = (
        os.path.join(sys.path[0], "plots_mock_response.json"))

    with open(mock_response_file_path) as mock_response_file:
        test_plot_data = json.load(mock_response_file)

    mock_get_request.return_value.json.return_value = test_plot_data

    plots_test_df = pd.DataFrame(test_plot_data["result"]["data"])
    plots_test_df.rename(
        columns=PhenotypeDataEbs.API_FIELDS_TO_LOCAL_FIELDS,
        inplace=True
    )

    plots_result_df = PhenotypeDataEbs().get_plots_by_occurrence_id(4)

    # assert dataframe is returned
    assert isinstance(plots_result_df, pd.DataFrame)

    assert_frame_equal(plots_result_df, plots_test_df)
