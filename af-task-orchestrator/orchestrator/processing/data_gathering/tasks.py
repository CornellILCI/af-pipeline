from orchestrator import config
from orchestrator.app import LOGGER, app
from orchestrator.base import FailureReportingTask
from orchestrator.data_reader import DataReaderFactory, PhenotypeData
from orchestrator.exceptions import DataSourceNotAvailableError, DataTypeNotAvailableError, MissingTaskParameter
from orchestrator.models import Experiment, Occurrence, Trait
from orchestrator.models.enums import DataSource, DataType
from pandas import DataFrame


@app.task(name="gather_data", base=FailureReportingTask)
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

    api_token = params.get("apiBearerToken")
    if not api_token:
        raise MissingTaskParameter("apiBearerToken")

    datasource = _get_datasource(source)
    datatype = _get_datatype(params.get("dataType", "PHENOTYPE"))  # putting phenotype as default
    occurrence_id = params.get("occurrenceId")

    experiment_id = params.get("experimentId")
    trait_id = params.get("traitId")

    api_base_url = _get_api_details(datasource)

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

        if experiment_id:
            experiment = reader.get_experiment(experiment_id)

        if occurrence_id:
            occurrence = reader.get_occurrence(occurrence_id)
            plots = reader.get_plots(occurrence_id)
            plot_measurements = reader.get_plot_measurements(occurrence_id)

        if trait_id:
            trait = reader.get_trait(trait_id)

        # TODO:  determine how large these data are, they might not fit into
        # the parameter size limit for celery tasks
        results = {
            "experiment": experiment,
            "trait": trait,
            "occurrence": occurrence,
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
