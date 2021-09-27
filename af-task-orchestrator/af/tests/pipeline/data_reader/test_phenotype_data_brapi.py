import json
from unittest import TestCase
from unittest.mock import Mock, patch
import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.models.brapi.germplasm import Germplasm

from af.pipeline.data_reader.phenotype_data_brapi import PhenotypeDataBrapi
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

# def get_search_result_dbid 
def get_brapi_search_result_dbid_mock_response():
    """ returns a mock brapi response for studies """
    return get_json_resource(__file__, "brapi_search_result_dbid_mock_response.json")

def get_brapi_germplasm_response():
    """ returns a mock brapi response for studies """
    return get_json_resource(__file__, "brapi_germplasm_mock_response.json")


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


# def get_test_germplasm_brapi() -> Germplasm:
#     test_germplasm_1 = {
#         "commonCropName": "rice",
#         "germplasmPUI":"9",
#         "germplasmDbId": "bd76c553-3862-11eb-95eb-0242ac140004",
#         "defaultDisplayName": "TANGKAI ROTAN",
#         "accessionNumber": "IRGC 31",
#         "germplasmName": "TANGKAI ROTAN",
#         "pedigree": "TR",
#         "synonyms": { "synonym": "IRGC 31", "type": "ACCNO"},
#         "countryOfOriginCode": "IRRI-GRC",
#         "typeOfGermplasmStorageCode": [],
#         "taxonIds": [],
#         "donors": [],
#         "acquisitionDate": "1961-03-27",
#         "breedingMethodDbId": "70",
#         "additionalInfo": {
#             "TAXNO_AP_text": "2832",
#             "MLS_DATE_AP_text": "29-JUN-2004",
#             "COLL_AA_text": "IRGC 31        ;O. SATIVA;;;;;MYS",
#             "SampStat_AP_text": "T",
#             "STATUS_ACC_AP_text": "AV",
#             "ORI_COUN_AP_text": "MALAYSIA",
#             "SPP_CODE_AP_text": "S",
#             "IPSTAT_AP_text": "FAO (14/09/1994)",
#             "VGISO_AA_text": "1" }
#             }
#     test_germplasm_2 = {
#         "commonCropName": "rice",
#         "germplasmPUI":"19",
#         "germplasmDbId": "bd76c553-3862-11eb-95eb-0242ac140004",
#         "defaultDisplayName": "TANGKAI BOTAN",
#         "accessionNumber": "IRGC 31",
#         "germplasmName": "TANGKAI ROTAN",
#         "pedigree": "TR",
#         "synonyms": { "synonym": "IRGC 31", "type": "ACCNO"},
#         "countryOfOriginCode": "IRRI-GRC",
#         "typeOfGermplasmStorageCode": [],
#         "taxonIds": [],
#         "donors": [],
#         "acquisitionDate": "1961-03-27",
#         "breedingMethodDbId": "70",
#         "additionalInfo": {
#             "TAXNO_AP_text": "2832",
#             "MLS_DATE_AP_text": "29-JUN-2004",
#             "COLL_AA_text": "IRGC 31        ;O. SATIVA;;;;;MYS",
#             "SampStat_AP_text": "T",
#             "STATUS_ACC_AP_text": "AV",
#             "ORI_COUN_AP_text": "MALAYSIA",
#             "SPP_CODE_AP_text": "S",
#             "IPSTAT_AP_text": "FAO (14/09/1994)",
#             "VGISO_AA_text": "1" }
#             }
#     test_germplasms = [test_germplasm_1,test_germplasm_2]
#     li = [Germplasm(**tg) for tg in test_germplasms]
#     li = list(li)
#     return li


class TestPhenotypeDataBrapi(TestCase):
    @patch("af.pipeline.data_reader.data_reader.requests.get")
    def test_get_plots(self, mock_get):

        mock_get.return_value.status_code = 200

        mock_get.return_value.json = Mock(side_effect=[get_brapi_observation_units_response()])

        plots_test_df = get_test_plots()

        plots_result_df = PhenotypeDataBrapi(api_base_url="http://test").get_plots("testid")

        # assert dataframe is returned
        assert isinstance(plots_result_df, pd.DataFrame)

        # arrange columns
        plots_result_df = plots_result_df[plots_test_df.columns]

        assert_frame_equal(plots_result_df, plots_test_df.astype(str))

    @patch("af.pipeline.data_reader.data_reader.requests.get")
    def test_get_plots_with_pages(self, mock_get):

        PhenotypeDataBrapi.brapi_list_page_size = 2

        mock_get.return_value.status_code = 200

        _pagination = """{
            "pageSize": 2,
            "totalPages": 2,
            "currentPage": 0,
            "totalCount": 3
        }"""

        first_page = get_brapi_observation_units_response()

        pagination = json.loads(_pagination)
        first_page["metadata"]["pagination"] = pagination

        second_page = get_brapi_observation_units_response()
        pagination = json.loads(_pagination)
        pagination["currentPage"] = 1
        second_page["metadata"]["pagination"] = pagination
        second_page["result"]["data"].pop()
        second_page_item = second_page["result"]["data"][0]
        second_page_item["observationUnitDbId"] = 2911

        mock_get.return_value.json = Mock(side_effect=[first_page, second_page])

        # expected result
        plots_expected = get_test_plots()
        plots_expected_page_2 = plots_expected.iloc[0].copy()
        plots_expected_page_2["plot_id"] = 2911
        plots_expected = plots_expected.append(plots_expected_page_2)

        plots_result = PhenotypeDataBrapi(api_base_url="http://test").get_plots("testid")

        # assert dataframe is returned
        assert isinstance(plots_result, pd.DataFrame)

        # arrange columns
        plots_result = plots_result[plots_expected.columns]

        assert_frame_equal(plots_result, plots_expected.astype(str))

    @patch("af.pipeline.data_reader.data_reader.requests.get")
    def test_get_plots_empty_result(self, mock_get):
        mock_get.return_value.status_code = 200

        brapi_response = get_brapi_observation_units_response()
        brapi_response["result"]["data"] = []

        mock_get.return_value.json = Mock(side_effect=[brapi_response])

        plots_test_df = get_test_plots()

        plots_result_df = PhenotypeDataBrapi(api_base_url="http://test").get_plots("testid")

        # assert dataframe is returned
        assert isinstance(plots_result_df, pd.DataFrame)

        assert len(plots_result_df) == 0

        assert set(plots_result_df.columns) == set(plots_test_df.columns)

    @patch("af.pipeline.data_reader.data_reader.requests.get")
    def test_get_plot_measurements(self, mock_get):

        mock_get.return_value.status_code = 200

        mock_get.return_value.json = Mock(side_effect=[get_brapi_observations_response()])

        plot_measurements_test_df = get_test_plot_measurements()

        plot_measurements_result_df = PhenotypeDataBrapi(api_base_url="http://test").get_plot_measurements("testid")

        # assert dataframe is returned
        assert isinstance(plot_measurements_result_df, pd.DataFrame)

        plot_measurements_result_df = plot_measurements_result_df[plot_measurements_test_df.columns]

        assert_frame_equal(plot_measurements_result_df, plot_measurements_test_df.astype(str))

    @patch("af.pipeline.data_reader.data_reader.requests.get")
    def test_get_plots_measurements_with_pages(self, mock_get):

        PhenotypeDataBrapi.brapi_list_page_size = 2

        mock_get.return_value.status_code = 200

        _pagination = """{
            "pageSize": 2,
            "totalPages": 2,
            "currentPage": 0,
            "totalCount": 3
        }"""

        first_page = get_brapi_observations_response()

        pagination = json.loads(_pagination)
        first_page["metadata"]["pagination"] = pagination

        second_page = get_brapi_observations_response()
        pagination = json.loads(_pagination)
        pagination["currentPage"] = 1
        second_page["metadata"]["pagination"] = pagination
        second_page["result"]["data"].pop()
        second_page_item = second_page["result"]["data"][0]
        second_page_item["observationUnitDbId"] = 2911

        mock_get.return_value.json = Mock(side_effect=[first_page, second_page])

        plot_measurements_expected = get_test_plot_measurements()
        plot_measurements_expected_page_2 = plot_measurements_expected.iloc[0].copy()
        plot_measurements_expected_page_2["plot_id"] = 2911
        plot_measurements_expected = plot_measurements_expected.append(plot_measurements_expected_page_2)

        plot_measurements_result = PhenotypeDataBrapi(api_base_url="http://test").get_plot_measurements("testid")

        # assert dataframe is returned
        assert isinstance(plot_measurements_result, pd.DataFrame)

        # arrange columns
        plot_measurements_result = plot_measurements_result[plot_measurements_expected.columns]

        assert_frame_equal(plot_measurements_result, plot_measurements_expected.astype(str))

    @patch("af.pipeline.data_reader.data_reader.requests.get")
    def test_get_occurrence(self, mock_get):
        from af.pipeline.data_reader.phenotype_data_brapi import PhenotypeDataBrapi

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = get_brapi_studies_response()
        test_occurrence = get_test_occurrence_brapi()

        occurrence_result = (PhenotypeDataBrapi(api_base_url="http://test")).get_occurrence(
            occurrence_id=test_occurrence.occurrence_id
        )

        for field, value in test_occurrence:
            assert value == occurrence_result.dict()[field]

    @patch("af.pipeline.data_reader.data_reader.requests.get")
    def test_get_occurrence_none_result(self, mock_get):
        from af.pipeline.data_reader.phenotype_data_brapi import PhenotypeDataBrapi

        mock_get.return_value.status_code = 200

        brapi_response = get_brapi_studies_response()
        brapi_response["result"] = None

        mock_get.return_value.json.return_value = brapi_response

        with self.assertRaises(DataReaderException):
            PhenotypeDataBrapi(api_base_url="http://test").get_occurrence(occurrence_id="test")


    @patch("af.pipeline.data_reader.data_reader.requests.post")  
    @patch("af.pipeline.data_reader.data_reader.requests.get")
    def test_search_germplasm(self,mock_post, mock_get):        
 
        brapi_response = get_brapi_germplasm_response()
        mock_post.return_value.status_code = 202
        mock_post.return_value.json.return_value = brapi_response

        brapi_response = get_brapi_search_result_dbid_mock_response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = brapi_response

        # test_germplasm = get_test_germplasm_brapi()
        search_query = {"germplasmDbIds": ["e9c6edd7", "1b1df4a6"]}
        germplasm_result = (PhenotypeDataBrapi(api_base_url="http://test")).search_germplasm(germplasm_search_ids=search_query.values)
        print(germplasm_result)

        # for germplasm in test_germplasm:
        #     for field, value in germplasm:
        #         assert value == germplasm_result.dict()[field]
xit