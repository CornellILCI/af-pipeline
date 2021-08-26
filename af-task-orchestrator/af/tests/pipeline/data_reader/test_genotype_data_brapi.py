import json
from unittest import TestCase
from unittest.mock import Mock, patch

import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.genotype_data_brapi import GenotypeDataBrapi
from pandas._testing import assert_frame_equal

from conftest import get_json_resource, get_test_plot_measurements, get_test_plots


def get_brapi_observation_units_response():
    """returns a mock brapi response for observation units."""
    return get_json_resource(__file__, "brapi_observationunits_mock_response.json")


def get_brapi_observations_response():
    """ returns a mock brapi response for observation units """
    return get_json_resource(__file__, "brapi_observations_mock_response.json")


def get_brapi_studies_response():
    """ returns a mock brapi response for studies """
    return get_json_resource(__file__, "brapi_studies_mock_response.json")


def get_test_occurrence_brapi() -> Occurrence:
    test_occurrence = {
        "occurrence_id": 7,
        "occurrence_name": "test_occurrence",
        "experiment_id": 4,
        "experiment_name": "test_experiment",
        "location_id": 6,
        "location": "test_location",
    }
    return Occurrence(**test_occurrence)


class TestGenotypeDataBrapi(TestCase):
    @patch("af.pipeline.data_reader.data_reader.requests.get")
    def test_get_(self, mock_get):

        mock_get.return_value.status_code = 200

        mock_get.return_value.json = Mock(side_effect=[get_brapi_observation_units_response()])

        plots_test_df = get_test_plots()

        plots_result_df = GenotypeDataBrapi(api_base_url="http://test").get_plots("testid")

        # assert dataframe is returned
        assert isinstance(plots_result_df, pd.DataFrame)

        # arrange columns
        plots_result_df = plots_result_df[plots_test_df.columns]

        assert_frame_equal(plots_result_df, plots_test_df.astype(str))
