from af.orchestrator import config
from af.orchestrator.app import app
from af.orchestrator.base import StatusReportingTask
from af.orchestrator.exceptions import MissingTaskParameter
from pandas import DataFrame
from af.pipeline.data_reader import DataReaderFactory, PhenotypeData
from af.pipeline.data_reader.exceptions import DataSourceNotAvailableError, DataTypeNotAvailableError
from af.pipeline.data_reader.models import Experiment, Occurrence, Trait
from af.pipeline.data_reader.models.enums import DataSource, DataType


@app.task(name="gather_data", base=StatusReportingTask)
def gather_data(params):
    """Gather data using data_reader

    For Phenotype data, this task will extract any related data depending on what
    parameters are contained in params.

    Required Params:
    dataSource -- EBS or BRAPI
    apiBearerToken -- API Auth token for accessing APIs

    experimentId -- task will update params with Experiment info
    occurenceId -- task will update params with Plots, PlotMeasurements and Occurence data
    traitId -- task will update params with Trait data.
    """
    source = params.get("dataSource")  # this is either EBS or BRAPI
    if not source:
        raise MissingTaskParameter("dataSource")

    api_token = params.get("dataSourceAccessToken")
    if not api_token:
        raise MissingTaskParameter("dataSourceAccessToken")

    datasource = _get_datasource(source)
    datatype = _get_datatype(params.get("dataType", "PHENOTYPE"))  # putting phenotype as default
    occurrence_ids = params.get("occurrenceIds") or []

    experiment_ids = params.get("experimentIds") or []
    trait_ids = params.get("traitIds") or []

    api_base_url = params.get("dataSourceUrl")

    factory = DataReaderFactory(datasource)

    if datatype == DataType.PHENOTYPE:
        reader: PhenotypeData = _get_phenotypedata_reader(factory, api_base_url, api_token)

        # TODO:  determine from the analysis type and/pr datasource? which of these data sets
        # are required

        plots: DataFrame = None
        plot_measurements: DataFrame = None
        experiment: Experiment = None
        occurrence: Occurrence = None
        trait: Trait = None

        experiments = []
        for experiment_id in experiment_ids:
            experiment = reader.get_experiment(experiment_id)
            experiments.append(experiment)

        occurrences = []
        plots = {}
        plot_measurements = {}
        for occurrence_id in occurrence_ids:
            occurrence = reader.get_occurrence(occurrence_id)
            occurrences.append(occurrence)

            plots[occurrence_id] = reader.get_plots(occurrence_id)
            plot_measurements[occurrence_id] = reader.get_plot_measurements(occurrence_id)

        traits = []
        for trait_id in trait_ids:
            trait = reader.get_trait(trait_id)
            traits.append(trait)

        # TODO:  determine how large these data are, they might not fit into
        # the parameter size limit for celery tasks
        results = {
            "experiment": experiments,
            "trait": traits,
            "occurrence": occurrences,
            "plots": plots,
            "plotMeasurements": plot_measurements,
        }

        params.update(results)  # include data in params for next task
        return params

    raise DataTypeNotAvailableError(datatype.name)


def _get_api_details(datasource: DataSource, *args, **kwargs):
    if datasource == DataSource.EBS:
        return config.EBS_BASE_URL
    elif datasource == DataSource.BRAPI:
        return config.BRAPI_BASE_URL


def _get_datasource(datasource: str, *args, **kwargs) -> DataSource:
    source: DataSource = None
    try:
        source = DataSource[datasource]
        return source
    except KeyError:
        raise DataSourceNotAvailableError(datasource)


def _get_datatype(datatype: str, *args, **kwargs) -> DataType:
    dtype: DataType = None
    try:
        dtype = DataType[datatype]
        return dtype
    except KeyError:
        raise DataTypeNotAvailableError(datatype)


def _get_phenotypedata_reader(factory: DataReaderFactory, base_url: str, token: str) -> PhenotypeData:
    return factory.get_phenotype_data(api_base_url=base_url, api_bearer_token=token)
