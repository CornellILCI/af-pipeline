from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.data_reader.models.enums import DataSource
from af.pipeline.sommer.dpo import SommeRProcessData
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import MagicMock, patch
from af.pipeline.db.models import Property

# import csv


def test_sommer_dpo_simple_test(mocker, dbsession, brapi_observation_table_api_response_1):

    mock_analysis_request = AnalysisRequest(
        requestId="test-request-id",
        dataSource=DataSource.BRAPI,
        dataSourceUrl="http://test",
        dataSourceAccessToken="foo-token-fake",
        outputFolder="/tmp/",
        experimentIds=["foo"],
        occurrenceIds=["foo"],
        traitIds=["foo"],
        analysisObjectivePropertyId="foo",
        analysisConfigPropertyId="foo",
        expLocAnalysisPatternPropertyId="foo",
        configFormulaPropertyId="foo",
        configResidualPropertyId="foo",
    )

    mocker.patch(
        "af.pipeline.data_reader.phenotype_data_brapi.PhenotypeDataBrapi.get",
        return_value=brapi_observation_table_api_response_1,
    )

    mock_residual = Property(statement="~ units")
    mock_formula = Property(statement="~ mu rep !r entry !f mv")

    mocker.patch("af.pipeline.db.services.get_property", return_value=mock_residual)
    mocker.patch("af.pipeline.db.services.get_property", return_value=mock_formula)

    dpo = SommeRProcessData(mock_analysis_request)

    output_list = dpo.run()

    assert isinstance(output_list, list)

    entry = output_list[0]

    assert entry is not None
    assert entry["job_name"] == "test-request-id"
    assert entry["data_file"] == "/tmp/test-request-id/test-request-id.csv"


# break this out into unit tests
def test_create_rcov_for_sommer_settings(mocker, dbsession, brapi_observation_table_api_response_1):

    mock_analysis_request = AnalysisRequest(
        requestId="test-request-id",
        dataSource=DataSource.BRAPI,
        dataSourceUrl="http://test",
        dataSourceAccessToken="foo-token-fake",
        outputFolder="/tmp/",
        experimentIds=["foo"],
        occurrenceIds=["foo"],
        traitIds=["foo"],
        analysisObjectivePropertyId="foo",
        analysisConfigPropertyId="foo",
        expLocAnalysisPatternPropertyId="foo",
        configFormulaPropertyId="foo",
        configResidualPropertyId="foo",
    )

    mocker.patch(
        "af.pipeline.data_reader.phenotype_data_brapi.PhenotypeDataBrapi.get",
        return_value=brapi_observation_table_api_response_1,
    )

    mock_residual = Property(statement="~ units")

    mocker.patch("af.pipeline.db.services.get_property", return_value=mock_residual)

    dpo = SommeRProcessData(mock_analysis_request)
    output_list = dpo.run()
    entry = output_list
    assert entry[1]["rcov"] == "~ units"


def test_create_formula_for_sommer_settings(mocker, dbsession, brapi_observation_table_api_response_1):

    mock_analysis_request = AnalysisRequest(
        requestId="test-request-id",
        dataSource=DataSource.BRAPI,
        dataSourceUrl="http://test",
        dataSourceAccessToken="foo-token-fake",
        outputFolder="/tmp/",
        experimentIds=["foo"],
        occurrenceIds=["foo"],
        traitIds=["foo"],
        analysisObjectivePropertyId="foo",
        analysisConfigPropertyId="foo",
        expLocAnalysisPatternPropertyId="foo",
        configFormulaPropertyId="foo",
        configResidualPropertyId="foo",
    )

    mocker.patch(
        "af.pipeline.data_reader.phenotype_data_brapi.PhenotypeDataBrapi.get",
        return_value=brapi_observation_table_api_response_1,
    )

    mock_residual = Property(statement="~ units")
    mock_formula = Property(statement="~ mu rep !r entry !f mv")

    mocker.patch("af.pipeline.db.services.get_property", return_value=mock_formula)

    dpo = SommeRProcessData(mock_analysis_request)
    output_list = dpo.run()
    entry = output_list
    assert entry[1]["formula"] == "~ mu rep !r entry !f mv"


def test_create_csvs(mocker, dbsession, brapi_observation_table_api_response_1):

    mock_analysis_request = AnalysisRequest(
        requestId="test-request-id",
        dataSource=DataSource.BRAPI,
        dataSourceUrl="http://test",
        dataSourceAccessToken="foo-token-fake",
        outputFolder="/tmp/",
        experimentIds=["foo"],
        occurrenceIds=["foo"],
        traitIds=["foo"],
        analysisObjectivePropertyId="foo",
        analysisConfigPropertyId="foo",
        expLocAnalysisPatternPropertyId="foo",
        configFormulaPropertyId="foo",
        configResidualPropertyId="foo",
    )

    mocker.patch(
        "af.pipeline.data_reader.phenotype_data_brapi.PhenotypeDataBrapi.get",
        return_value=brapi_observation_table_api_response_1,
    )

    mock_residual = Property(statement="~ units")
    mock_formula = Property(statement="~ mu rep !r entry !f mv")

    mocker.patch("af.pipeline.db.services.get_property", return_value=mock_formula)

    dpo = SommeRProcessData(mock_analysis_request)
    output_list = dpo.run()
    entry = output_list
    assert entry[2]["var"] == "/var.csv"
    assert entry[2]["statmodel"] == "/statmodel.csv"
    assert entry[2]["BVs"] == "/BVs.csv"
    assert entry[2]["pvs"] == "/pvs.csv"
    assert entry[2]["Yhat"] == "/Yhat.csv"
    assert entry[2]["outliers"] == "/outliers.csv"
    assert entry[2]["out"] == "/out.rds"
