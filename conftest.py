import sys
import os

import pandas as pd

import json

os.environ["B4R_API_BASE_URL"] = ""


def get_ebs_plots_response():
    """ returns a plots response json object to be used as mock """

    mock_response_file_path = (
        os.path.join(sys.path[0],
                     "plots_mock_response.json"))
    with open(mock_response_file_path) as mock_response_file:
        test_plot_data = json.load(mock_response_file)

    return test_plot_data


def get_test_plots():
    """ return a mock plots dataframe """

    from data_reader.phenotype_data_ebs import PhenotypeDataEbs

    test_plot_data = get_ebs_plots_response()
    plots_test_df = pd.DataFrame(test_plot_data["result"]["data"])
    plots_test_df.rename(
        columns=PhenotypeDataEbs.API_FIELDS_TO_LOCAL_FIELDS,
        inplace=True
    )
    return plots_test_df
