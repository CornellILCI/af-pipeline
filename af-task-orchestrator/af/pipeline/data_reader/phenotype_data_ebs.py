import pandas as pd
from af.pipeline import config
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Experiment, Occurrence, OccurrenceEbs, Trait, VariableEbs
from af.pipeline.data_reader.phenotype_data import PhenotypeData
from af.pipeline.pandasutil import df_keep_columns
from pydantic import ValidationError

SEARCH_PLOTS_ENDPOINT = "/plots-search"

SEARCH_PLOT_DATA_ENDPOINT = "/plot-data-search"

SEARCH_OCCURRENCES_ENDPOINT = "/occurrences-search"

SEARCH_VARIABLES_ENDPOINT = "/variables-search"


class PhenotypeDataEbs(PhenotypeData):
    """EBS concrete class for PhenotypeData interface."""

    # maps ebs plot resource fields to local plot fields.
    plots_api_fields_to_local_fields = {
        "plotDbId": "plot_id",
        "entryDbId": "entry_id",
        "entryName": "entry_name",
        "entryType": "entry_type",
        "paX": "pa_x",
        "paY": "pa_y",
        "rep": "rep_factor",
        "blockNumber": "blk",
        "plotQcCode": "plot_qc",
        "occurrence_id": "occurr_id",
        "location_id": "loc_id",
        "experiment_id": "expt_id",
    }

    # maps ebs plot_data resource fields to local plot measurement fields
    plot_data_api_fields_to_local_fields = {
        "plotDbId": "plot_id",
        "variableDbId": "trait_id",
        "dataValue": "trait_value",
        "dataQCCode": "trait_qc",
    }

    plots_unknown_values = {"paX": "", "paY": ""}

    list_api_page_size = 100

    def get_plots(self, experiment_id=None, occurrence_id: str = None, location_id=None) -> pd.DataFrame:

        columns_from_occurrence = {"experiment_id", "occurrence_id", "location_id"}

        page_num = 1

        plots_data = []

        plots_url = SEARCH_PLOTS_ENDPOINT.format(occurrence_id=occurrence_id)

        search_query = {"occurrenceDbId": occurrence_id}

        api_page_params = {
            "limit": self.list_api_page_size,
        }

        while len(plots_data) >= self.list_api_page_size or page_num == 1:

            api_page_params["page"] = page_num

            api_response = self.post(endpoint=plots_url, data=search_query, params=api_page_params)

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            plots_data = api_response.body["result"]["data"]

            if not len(plots_data):
                if page_num == 1:
                    columns = list(self.plots_api_fields_to_local_fields.values())
                    columns.extend(columns_from_occurrence)
                    return pd.DataFrame(columns=columns)
                break

            plots_page = pd.DataFrame(plots_data)

            # Fill the unknown values
            for field in self.plots_unknown_values:
                plots_page[field] = plots_page[field].fillna(self.plots_unknown_values[field])

            plots_page = plots_page.fillna(config.UNIVERSAL_UNKNOWN)

            # keep only local field columns
            plots_page = df_keep_columns(plots_page, self.plots_api_fields_to_local_fields.keys())

            if page_num == 1:
                plots = plots_page
            else:
                plots = plots.append(plots_page)

            page_num += 1

        # Add columns from Occurrence entity
        occurrence = self.get_occurrence(occurrence_id)
        for column in columns_from_occurrence:
            if occurrence.dict()[column]:
                plots[column] = occurrence.dict()[column]
            else:
                plots[column] = config.UNIVERSAL_UNKNOWN

        # rename dataframe column with local field names
        plots.rename(columns=self.plots_api_fields_to_local_fields, inplace=True)

        return plots.astype(str)

    def get_plot_measurements(self, occurrence_id: str = None, trait_id: str = None) -> pd.DataFrame:

        page_num = 1

        plot_measurements_data = []

        plots_url = SEARCH_PLOT_DATA_ENDPOINT.format(occurrence_id=occurrence_id)

        search_query = {"occurrenceDbId": occurrence_id, "variableDbId": trait_id}

        api_page_params = {
            "limit": self.list_api_page_size,
        }

        while len(plot_measurements_data) >= self.list_api_page_size or page_num == 1:

            api_page_params["page"] = page_num

            api_response = self.post(endpoint=plots_url, data=search_query, params=api_page_params)

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            plot_measurements_data = api_response.body["result"]["data"]

            if not len(plot_measurements_data):
                if page_num == 1:
                    columns = list(self.plot_data_api_fields_to_local_fields.values())
                    return pd.DataFrame(columns=columns)
                break
            plot_measurements_page = pd.DataFrame(plot_measurements_data)

            # keep only local field columns
            plot_measurements_page = df_keep_columns(
                plot_measurements_page, self.plot_data_api_fields_to_local_fields.keys()
            )

            if page_num == 1:
                plot_measurements = plot_measurements_page
            else:
                plot_measurements = plot_measurements.append(plot_measurements_page)

            page_num += 1

        # rename dataframe column with local field names
        plot_measurements.rename(columns=self.plot_data_api_fields_to_local_fields, inplace=True)

        return plot_measurements.astype(str)

    def get_occurrence(self, occurrence_id: str = None) -> Occurrence:

        search_query = {"occurrenceDbId": occurrence_id}

        api_response = self.post(endpoint=SEARCH_OCCURRENCES_ENDPOINT, data=search_query)

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        result_list = api_response.body["result"]["data"]

        if len(result_list) > 1:
            raise DataReaderException("More than one resource found for id")
        elif len(result_list) == 0:
            raise DataReaderException("No Occurrence found")

        # load it to model to make sure required fields are found
        try:
            _occurrence_ebs = OccurrenceEbs(**result_list[0])
        except ValidationError as e:
            raise DataReaderException(str(e))

        return Occurrence(
            occurrence_id=_occurrence_ebs.occurrenceDbId,
            occurrence_name=_occurrence_ebs.occurrenceName,
            experiment_id=_occurrence_ebs.experimentDbId,
            experiment_name=_occurrence_ebs.experiment,
            location_id=_occurrence_ebs.locationDbId,
            location=_occurrence_ebs.location,
            rep_count=_occurrence_ebs.repCount,
            entry_count=_occurrence_ebs.entryCount,
            plot_count=_occurrence_ebs.plotCount,
        )

    def get_experiment(self, experiment_id: str = None) -> Experiment:
        raise NotImplementedError

    def get_trait(self, trait_id: str = None) -> Trait:

        search_query = {"variableDbId": trait_id}

        api_response = self.post(endpoint=SEARCH_VARIABLES_ENDPOINT, data=search_query)

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        result_list = api_response.body["result"]["data"]

        if len(result_list) > 1:
            raise DataReaderException("More than one resource found for id")
        elif len(result_list) == 0:
            raise DataReaderException(f"Trait(id:{trait_id}) not found")

        # load it to model to make sure required fields are found
        try:
            _variable_ebs = VariableEbs(**result_list[0])
        except ValidationError as e:
            raise DataReaderException(str(e))

        return Trait(
            trait_id=_variable_ebs.variableDbId, trait_name=_variable_ebs.name, abbreviation=_variable_ebs.abbrev
        )
