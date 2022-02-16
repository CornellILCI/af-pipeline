import json
import os

# hacky importing since we need to declare these before we import Base
# since core.py directly declares the vars
import tempfile

import pytest
from pandas import DataFrame

# fixtures import area


def get_test_resource_path(testfile, resource_name):
    """Get resource files in the same directory as test file"""
    currentdir = os.path.dirname(os.path.realpath(testfile))
    return os.path.join(currentdir, resource_name)


def get_json_resource(testfile, json_file_name):
    """Reads json file from given file path."""
    file_path = get_test_resource_path(testfile, json_file_name)
    with open(file_path) as file_:
        json_ = json.load(file_)
    return json_


def get_test_analysis_request():
    from af.pipeline.analysis_request import AnalysisRequest, Experiment, Occurrence, Trait

    # output_folder = tempfile.TemporaryDirectory()
    analysis_request = AnalysisRequest(
        requestId="test_id",
        dataSource="EBS",
        dataSourceUrl="http://test.org",
        dataSourceAccessToken="",
        experiments=[
            Experiment(
                experimentId="1",
                experimentName="name1",
                occurrences=[
                    Occurrence(occurrenceId="1", occurrenceName="occur1"),
                    Occurrence(occurrenceId="2", occurrenceName="occur2"),
                ],
            )
        ],
        traits=[Trait(traitId="1", traitName="trait1")],
        analysisObjectivePropertyId="1",
        analysisConfigPropertyId="1",
        expLocAnalysisPatternPropertyId="1",
        configFormulaPropertyId="1",
        configResidualPropertyId="1",
        outputFolder="/tmp/",
        configPredictionPropertyIds=["19"],
    )
    return analysis_request


def get_test_plots() -> DataFrame:
    """return a mock plots dataframe"""

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
    """return a mock plot measurement dataframe"""

    columns = ["plot_id", "trait_id", "trait_qc", "trait_value"]
    data = [
        [2909, 1, "G", 6.155850575],
        [2910, 1, "G", 6.751358238],
    ]
    return DataFrame(data, columns=columns)


@pytest.fixture
def sommer_analysis_request():

    from af.pipeline.data_reader.models.enums import DataSource

    sommer_analysis_request = get_test_analysis_request()
    sommer_analysis_request.requestId = "test-request-id"

    sommer_analysis_request.dataSource = DataSource.BRAPI

    return sommer_analysis_request


@pytest.fixture
def analysis_request():

    analysis_request = get_test_analysis_request()
    return analysis_request
