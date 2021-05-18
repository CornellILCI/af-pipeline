import os
os.environ["AFDB_URL"] = "sqlite://"

import pytest
from orchestrator.exceptions import MissingTaskParameter
from orchestrator.processing.data_gathering.tasks import gather_data


def test_data_gather_phenotype_ok(mocker, phenotype_request, mock_brapi_phenotype_data):
    mocker.patch(
        "pipeline.data_reader.DataReaderFactory.get_phenotype_data", return_value=mock_brapi_phenotype_data
    )

    data = gather_data(phenotype_request)

    assert data.get("experiment") is not None
    assert data.get("occurrence") is not None
    assert data.get("plots") is not None
    assert data.get("plotMeasurements") is not None
    assert data.get("trait") is not None


def test_data_gather_phenotype_missing_data_source(phenotype_request_missing_datasource):
    with pytest.raises(MissingTaskParameter):
        gather_data(phenotype_request_missing_datasource)
