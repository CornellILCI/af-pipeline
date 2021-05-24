import io
import json
import os
import random
import string
import sys

from pandas import DataFrame

os.environ["B4R_API_BASE_URL"] = ""


def get_test_resource_path(testfile, resource_name):
    """ Get resource files in the same directory as test file
    """
    currentdir = os.path.dirname(os.path.realpath(testfile))
    return os.path.join(currentdir, resource_name)


def get_json_resource(testfile, json_file_name):
    """ Reads json file from given file path.
    """
    file_path = get_test_resource_path(testfile, json_file_name)
    with open(file_path) as file_:
        json_ = json.load(file_)
    return json_


def get_test_plots() -> DataFrame:
    """ return a mock plots dataframe """

    columns = [
        "plot_id",
        "expt_id",
        "loc_id",
        "occurr_id",
        "entry_id",
        "pa_x",
        "pa_y",
        "rep_factor",
        "blk",
        "plot_qc",
    ]
    data = [
        [2909, 4, 6, 7, 180, 3, 5, 1, 1, "G"],
        [2910, 4, 6, 7, 103, 4, 5, 1, 1, "G"],
    ]
    return DataFrame(data, columns=columns)


def get_test_plot_measurements() -> DataFrame:
    """ return a mock plot measurement dataframe"""

    columns = ["plot_id", "trait_id", "trait_qc", "trait_value"]
    data = [
        [2909, 1, "G", 6.155850575],
        [2910, 1, "G", 6.751358238],
    ]
    return DataFrame(data, columns=columns)
