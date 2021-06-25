import json
from unittest import TestCase
from unittest.mock import Mock, patch

import pandas as pd
from pandas._testing import assert_frame_equal
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.phenotype_data_ebs import PhenotypeDataEbs

from conftest import get_json_resource, get_test_plot_measurements, get_test_plots


def get_plots_response():
    """ returns a plots response json object to be used as mock """
    return get_json_resource(__file__, "plots_mock_response.json")


def get_plot_data_response():
    """ returns a plots response json object to be used as mock """
    return get_json_resource(__file__, "plot_data_mock_response.json")


def get_occurrence_response():
    """ returns a occurrence response json object to be used as mock """
    return get_json_resource(__file__, "occurrence_mock_response.json")


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
        "plot_count": 2,
    }
    return Occurrence(**test_occurrence)


class TestPhenotypeDataEbs(TestCase):
    @patch("af.pipeline.data_reader.data_reader.requests.post")
    def test_get_plots(self, mock_post):

        mock_post.return_value.status_code = 200

        PhenotypeDataEbs.list_api_page_size = 100

        mock_post.return_value.json = Mock(side_effect=[get_plots_response(), get_occurrence_response()])

        plots_test_df = get_test_plots().astype(str)

        plots_result_df = PhenotypeDataEbs(api_base_url="http://test").get_plots("testid")

        # assert dataframe is returned
        assert isinstance(plots_result_df, pd.DataFrame)

        plots_result_df = plots_result_df[plots_test_df.columns]

        assert_frame_equal(plots_result_df, plots_test_df)

    @patch("af.pipeline.data_reader.data_reader.requests.post")
    def test_get_plots_raise_exception_for_401(self, mock_post):

        from requests.exceptions import HTTPError

        mock_post.return_value.status_code = 401
        mock_post.return_value.json = Mock(side_effect=get_ebs_unauthorized_error_response)
        mock_post.return_value.raise_for_status = Mock(side_effect=HTTPError)

        with self.assertRaises(DataReaderException):
            PhenotypeDataEbs(api_base_url="http://test").get_plots(occurrence_id="testid")

    @patch("af.pipeline.data_reader.data_reader.requests.post")
    def test_get_plots_paging(self, mock_post):

        PhenotypeDataEbs.list_api_page_size = 2

        mock_post.return_value.status_code = 200

        _pagination = """{
            "pageSize": 2,
            "totalPages": 2,
            "currentPage": 0,
            "totalCount": 3
        }"""

        page_1_response = get_plots_response()
        pagination_1 = json.loads(_pagination)
        page_1_response["metadata"]["pagination"] = pagination_1

        page_2_response = get_plots_response()
        pagination_2 = json.loads(_pagination)
        pagination_2["currentPage"] = 1
        page_2_response["metadata"]["pagination"] = pagination_2
        page_2_response["result"]["data"].pop()
        page_2_item = page_2_response["result"]["data"][0]
        page_2_item["plotDbId"] = 2911

        mock_post.return_value.json = Mock(side_effect=[page_1_response, page_2_response, get_occurrence_response()])

        plots_expected = get_test_plots()
        plots_expected_page_2 = plots_expected.iloc[0].copy()
        plots_expected_page_2["plot_id"] = 2911
        plots_expected = plots_expected.append(plots_expected_page_2)

        plots_result_df = PhenotypeDataEbs(api_base_url="http://test").get_plots("testid")

        # assert dataframe is returned
        assert isinstance(plots_result_df, pd.DataFrame)

        plots_result_df = plots_result_df[plots_expected.columns]

        assert_frame_equal(plots_result_df, plots_expected.astype(str))

    def test_get_plots_raise_exception_for_invalid_url(self):
        with self.assertRaises(DataReaderException):
            PhenotypeDataEbs(api_base_url="htp").get_plots("testid")

    @patch("af.pipeline.data_reader.data_reader.requests.post")
    def test_get_plot_measurements(self, mock_post):

        PhenotypeDataEbs.list_api_page_size = 2

        mock_post.return_value.status_code = 200

        _pagination = """{
            "pageSize": 2,
            "totalPages": 2,
            "currentPage": 0,
            "totalCount": 3
        }"""

        page_1_response = get_plot_data_response()
        pagination_1 = json.loads(_pagination)
        page_1_response["metadata"]["pagination"] = pagination_1

        page_2_response = get_plot_data_response()
        pagination_2 = json.loads(_pagination)
        pagination_2["currentPage"] = 1
        page_2_response["metadata"]["pagination"] = pagination_2
        page_2_response["result"]["data"].pop()
        page_2_item = page_2_response["result"]["data"][0]
        page_2_item["plotDbId"] = 2911

        mock_post.return_value.json = Mock(side_effect=[page_1_response, page_2_response])

        plot_measurements_expected = get_test_plot_measurements()
        plot_measurements_expected_page_2 = plot_measurements_expected.iloc[0].copy()
        plot_measurements_expected_page_2["plot_id"] = 2911
        plot_measurements_expected = plot_measurements_expected.append(plot_measurements_expected_page_2)

        plot_measurements_result = PhenotypeDataEbs(api_base_url="http://test").get_plot_measurements("testid")

        # assert dataframe is returned
        assert isinstance(plot_measurements_result, pd.DataFrame)

        plot_measurements_result = plot_measurements_result[plot_measurements_expected.columns]

        assert_frame_equal(plot_measurements_result, plot_measurements_expected.astype(str))

    @patch("af.pipeline.data_reader.data_reader.requests.post")
    def test_get_occurrence(self, mock_post):
        from af.pipeline.data_reader.phenotype_data_ebs import PhenotypeDataEbs

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = get_occurrence_response()
        test_occurrence = get_test_occurrence()

        occurrence_result = (PhenotypeDataEbs(api_base_url="http://test")).get_occurrence(
            occurrence_id=test_occurrence.occurrence_id
        )

        for field, value in test_occurrence:
            assert value == occurrence_result.dict()[field]
