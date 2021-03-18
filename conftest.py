import sys
import os

import pandas as pd

from models import Occurrence

import json

os.environ["B4R_API_BASE_URL"] = ""


def __read_mock_json_file(file_path):
    mock_response_file_path = os.path.join(sys.path[0], file_path)
    with open(mock_response_file_path) as mock_response_file:
        test_response = json.load(mock_response_file)
    return test_response


def get_ebs_plots_response():
    """ returns a plots response json object to be used as mock """

    return __read_mock_json_file("tests/data_reader/plots_mock_response.json")


def get_ebs_occurrence_response():
    """ returns a occurrence response json object to be used as mock """

    return __read_mock_json_file(
        "tests/data_reader/occurrence_mock_response.json")


def get_brapi_observation_units_response():
    """ returns a mock brapi response for observation units """

    return __read_mock_json_file(
        "tests/data_reader/brapi_observationunits_mock_response.json")


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
