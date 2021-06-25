import os

os.environ["AFDB_URL"] = "sqlite://"

import pytest
from af.orchestrator.exceptions import MissingTaskParameter
from af.orchestrator.processing.data_gathering.tasks import gather_data


def test_data_gather_phenotype_ok(mocker, phenotype_request, mock_brapi_phenotype_data, dbsession):
    mocker.patch("af.pipeline.data_reader.DataReaderFactory.get_phenotype_data", return_value=mock_brapi_phenotype_data)
    mocker.patch("af.pipeline.db.core.get_session", return_value=dbsession)

    data = gather_data(phenotype_request)

    assert data.get("experiment") is not None
    assert data.get("occurrence") is not None
    assert data.get("plots") is not None
    assert data.get("plotMeasurements") is not None
    assert data.get("trait") is not None


def test_data_gather_phenotype_missing_data_source(mocker, phenotype_request_missing_datasource, dbsession):
    print("mocked")
    mocker.patch("af.pipeline.db.core.get_session", return_value=dbsession)
    with pytest.raises(MissingTaskParameter):
        gather_data(phenotype_request_missing_datasource)
