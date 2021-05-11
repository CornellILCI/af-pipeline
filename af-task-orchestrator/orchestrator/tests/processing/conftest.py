import pandas as pd
import pytest
from pipeline.data_reader.phenotype_data_brapi import PhenotypeDataBrapi
from pipeline.data_reader.models import Experiment, Occurrence, Trait


@pytest.fixture
def phenotype_request():
    return {
        "dataSource": "BRAPI",
        "dataType": "PHENOTYPE",
        "experimentId": "123",
        "occurrenceId": "456",
        "traitId": "789",
        "jobId": "sampleId",
        "processName": "some_workflow",
        "apiBearerToken": "some_bearer_token",
    }


@pytest.fixture
def phenotype_request_missing_datasource():
    return {
        "experimentId": "123",
        "occurrenceId": "456",
        "traitId": "789",
        "jobId": "sampleId",
        "processName": "some_workflow",
        "apiBearerToken": "some_bearer_token",
    }


@pytest.fixture
def mock_trait():
    trait = Trait(trait_id=789, trait_name="TestTrait", abbreviation="TRAIT_ABBREV")
    return trait


@pytest.fixture
def mock_experiment():
    experiment = Experiment(id=123, experiment_name="TestExperiment")
    return experiment


@pytest.fixture
def mock_plots():
    mock_plot_data = [{"field1": "1"}, {"field1": "2"}]
    plots = pd.DataFrame(data=mock_plot_data)
    return plots


@pytest.fixture
def mock_plot_measurements():
    mock_plot_mdata = [
        {
            "id": "1",
            "field1": "10",
            "field2": "11",
        },
        {
            "id": "2",
            "field1": "12",
            "field2": "13",
        },
    ]
    plot_ms = pd.DataFrame(data=mock_plot_mdata)
    return plot_ms


@pytest.fixture
def mock_occurrence():
    occ = Occurrence(
        occurrence_id=456,
        occurrence_name="TestOccurrence",
        experiment_id=123,
        experiment_name="Test Experiment",
        location_id=999,
        location="TestLocation",
        rep_count=1,
        entry_count=1,
        plot_count=1,
    )
    return occ


@pytest.fixture
def mock_brapi_phenotype_data(mocker, mock_plots, mock_plot_measurements, mock_experiment, mock_trait, mock_occurrence):
    mocked_data_reader = mocker.MagicMock(spec=PhenotypeDataBrapi)

    mocked_data_reader.get_plots.return_value = mock_plots
    mocked_data_reader.get_plot_measurements.return_value = mock_plot_measurements
    mocked_data_reader.get_trait.return_value = mock_trait
    mocked_data_reader.get_experiment.return_value = mock_experiment
    mocked_data_reader.get_occurrence.return_value = mock_occurrence

    return mocked_data_reader
