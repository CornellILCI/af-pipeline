import json
from unittest import TestCase
from unittest.mock import Mock, patch

import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.genotype_data_brapi import GenotypeDataBrapi
from pandas._testing import assert_frame_equal

from conftest import get_json_resource, get_test_plot_measurements, get_test_plots


def get_brapi_variantsets_units_response():
    """returns a mock brapi response for observation units."""
    return get_json_resource(__file__, "brapi_variantsets_mock_response.json")

def post_brapi_search_callsets_200_response():
    """returns a mock brapi response for observation units."""
    return get_json_resource(__file__, "brapi_search_callsets_200_response.json")

def post_brapi_search_callsets_202_response():
    """returns a mock brapi response for observation units."""
    return get_json_resource(__file__, "brapi_search_callsets_202_response.json")

def post_brapi_search_callsets_responses_202():
    """returns a mock brapi response for observation units."""
    return 202

def post_brapi_search_callsets_responses_200():
    """returns a mock brapi response for observation units."""
    return 200


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
    def test_get_variantsets(self, mock_get):

        mock_get.return_value.status_code = 200

        mock_get.return_value.json = Mock(side_effect=[get_brapi_variantsets_units_response()])

        plots_test_df = get_test_plots()

        plots_result_df = GenotypeDataBrapi(api_base_url="http://test").get_variantsets(["testid"])

        # assert dataframe is returned
        assert isinstance(plots_result_df, pd.DataFrame)

        # arrange columns
        plots_result_df = plots_result_df[plots_test_df.columns]

        assert_frame_equal(plots_result_df, plots_test_df.astype(str))
    

    @patch("af.pipeline.data_reader.data_reader.requests.post")
    def test_post_search_callsets(self, mock_post):
        mock_post.return_value.status_code = 200

        mock_post.return_value.json = Mock(side_effect=[post_brapi_search_callsets_200_response()])

        plots_result_df = GenotypeDataBrapi(api_base_url="http://test").post_search_callsets(["testid"])

        # return False

    
    @patch("af.pipeline.data_reader.data_reader.requests.post")
    @patch("af.pipeline.data_reader.data_reader.requests.get")
    def test_post_search_callsets_with_202(self, mock_get, mock_post):
        response = self.mock202Response()
        betterResponse = self.mock200Response()
        betterResponse.status_code = 200
        betterResponse.json
        mock_post.return_value = response
        mock_get.side_effect = [response,betterResponse]

        callsets_result = GenotypeDataBrapi(api_base_url="http://test").post_search_callsets(["testid"])

        assert len(callsets_result) == 1


    class mock202Response:
        status_code = 202
        def json(self):
            return post_brapi_search_callsets_202_response()
        def raise_for_status(self):
            return True
    
    class mock200Response:
        status_code = 200
        def json(self):
            return post_brapi_search_callsets_200_response()
        def raise_for_status(self):
            return True