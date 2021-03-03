from unittest.mock import patch
import pandas as pd
from pandas._testing import assert_frame_equal

from conftest import get_ebs_plots_response, get_test_plots


@patch('data_reader.phenotype_data_ebs.requests.get')
def test_get_plots_by_occurrence_id(mock_get_request):

    from data_reader.phenotype_data_ebs import PhenotypeDataEbs

    mock_get_request.return_value.ok = True
    mock_get_request.return_value.json.return_value = get_ebs_plots_response()

    plots_test_df = get_test_plots()

    plots_result_df = PhenotypeDataEbs().get_plots_by_occurrence_id(4)

    # assert dataframe is returned
    assert isinstance(plots_result_df, pd.DataFrame)

    assert_frame_equal(plots_result_df, plots_test_df)
