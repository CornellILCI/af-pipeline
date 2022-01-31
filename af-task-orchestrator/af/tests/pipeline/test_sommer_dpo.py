import json
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import MagicMock, patch

from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.db.models import Property
from af.pipeline.job_data import JobData
from af.pipeline.sommer.dpo import SommeRProcessData

# import csv


def test_sommer_dpo_simple_test(mocker, dbsession, brapi_observation_table_api_response_1, sommer_analysis_request):

    mocker.patch(
        "af.pipeline.data_reader.phenotype_data_brapi.PhenotypeDataBrapi.get",
        return_value=brapi_observation_table_api_response_1,
    )

    mock_residual = Property(statement="~ units")
    mock_formula = Property(statement="~ mu rep !r entry !f mv")

    mocker.patch("af.pipeline.db.services.get_property", return_value=mock_residual)
    mocker.patch("af.pipeline.db.services.get_property", return_value=mock_formula)

    dpo = SommeRProcessData(sommer_analysis_request)

    output_list = dpo.run()

    assert isinstance(output_list, list)

    entry = output_list[0]

    assert entry is not None
    assert entry.job_name == "test-request-id"
    assert entry.job_file == "/tmp/test-request-id/settings.json"


# break this out into unit tests
def test_create_rcov_for_sommer_settings(
    mocker, dbsession, brapi_observation_table_api_response_1, sommer_analysis_request
):

    mocker.patch(
        "af.pipeline.data_reader.phenotype_data_brapi.PhenotypeDataBrapi.get",
        return_value=brapi_observation_table_api_response_1,
    )

    mock_residual = Property(statement="~ units")

    mocker.patch("af.pipeline.db.services.get_property", return_value=mock_residual)

    dpo = SommeRProcessData(sommer_analysis_request)
    output_list = dpo.run()
    entry = output_list[0]
    assert entry is not None
    assert entry.job_name == "test-request-id"
    assert entry.job_file == "/tmp/test-request-id/settings.json"


def test_create_formula_for_sommer_settings(
    mocker, dbsession, brapi_observation_table_api_response_1, sommer_analysis_request
):

    mocker.patch(
        "af.pipeline.data_reader.phenotype_data_brapi.PhenotypeDataBrapi.get",
        return_value=brapi_observation_table_api_response_1,
    )

    mock_residual = Property(statement="~ units")
    mock_formula = Property(statement="~ mu rep !r entry !f mv")
    # mock_fixed = Property(statement="<FIXED>")
    # mock_random = Property(statement="<RANDOM>")
    mocker.patch("af.pipeline.db.services.get_property", return_value=mock_formula)

    dpo = SommeRProcessData(sommer_analysis_request)
    job_objects = dpo.run()
    sf = job_objects[0].job_file

    with open(sf) as json_file:
        data = json.load(json_file)

    assert data["formula"] == "~ mu rep !r entry !f mv"
