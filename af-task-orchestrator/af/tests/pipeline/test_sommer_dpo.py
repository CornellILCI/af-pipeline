from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.sommer.dpo import SommeRProcessData


def test_sommer_dpo_simple_test(mocker, dbsession, brapi_observation_table_api_response_1, sommer_analysis_request):

    mocker.patch(
        "af.pipeline.data_reader.phenotype_data_brapi.PhenotypeDataBrapi.get",
        return_value=brapi_observation_table_api_response_1,
    )

    dpo = SommeRProcessData(sommer_analysis_request)

    output_list = dpo.run()

    assert isinstance(output_list, list)

    entry = output_list[0]

    assert entry is not None
    assert entry["job_name"] == "test-request-id"
    assert entry["data_file"] == "/tmp/test-request-id/test-request-id.csv"