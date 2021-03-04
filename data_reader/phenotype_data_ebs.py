import pandas as pd

from pydantic import ValidationError

from models import Experiment, Occurrence, Trait, OccurrenceEbs

from data_reader.phenotype_data import PhenotypeData

from exceptions import DataReaderException

SEARCH_PLOTS_ENDPOINT = "/plots-search"

SEARCH_OCCRRENCES_ENDPOINT = "/occurrences-search"


class PhenotypeDataEbs(PhenotypeData):
    """ reads phenotype data from a ebs data source.
    """

    PLOTS_API_FIELDS_TO_LOCAL_FIELDS = {
        "plotDbId": "plot_id",
        "entryDbId": "entry_id",
        "paX": "pa_x",
        "paY": "pa_y",
        "rep": "rep_factor",
        "blockNumber": "blk",
        "plotQcCode": "plot_qc"
    }

    def get_plots(self, occurrence_id: str = None) -> pd.DataFrame:

        search_query = {
            "occurrenceDbId": occurrence_id
        }

        api_response = self.post(endpoint=SEARCH_PLOTS_ENDPOINT,
                                 data=search_query)

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        plots_data = api_response.body["result"]["data"]

        plots_df = pd.DataFrame(plots_data)

        # keep only local field columns
        plots_df_columns_to_drop = (
            set(plots_df.columns) -
            self.PLOTS_API_FIELDS_TO_LOCAL_FIELDS.keys())
        plots_df_columns_to_keep = (
            self.PLOTS_API_FIELDS_TO_LOCAL_FIELDS.keys() -
            plots_df_columns_to_drop)
        plots_df = plots_df[plots_df_columns_to_keep]

        # rename dataframe column with local field names
        plots_df.rename(
            columns=self.PLOTS_API_FIELDS_TO_LOCAL_FIELDS,
            inplace=True
        )

        occurrence = self.get_occurrence(occurrence_id)

        columns_from_occurrence = {"experiment_id",
                                   "occurrence_id",
                                   "location_id"}

        for column in columns_from_occurrence:
            plots_df[column] = occurrence.dict()[column]

        return plots_df

    def get_plot_measurements(self, occurrence_id: str = None) -> pd.DataFrame:
        raise NotImplementedError

    def get_occurrence(self, occurrence_id: str = None) -> Occurrence:

        search_query = {
            "occurrenceDbId": occurrence_id
        }

        api_response = self.post(endpoint=SEARCH_OCCRRENCES_ENDPOINT,
                                 data=search_query)

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

        occurrence = {
            "occurrence_id": _occurrence_ebs.occurrenceDbId,
            "occurrence_name": _occurrence_ebs.occurrenceName,
            "experiment_id": _occurrence_ebs.experimentDbId,
            "experiment_name": _occurrence_ebs.experiment,
            "location_id": _occurrence_ebs.locationDbId,
            "location": _occurrence_ebs.location,
            "rep_count": _occurrence_ebs.repCount,
            "entry_count": _occurrence_ebs.entryCount,
            "plot_count": _occurrence_ebs.plotCount
        }

        return Occurrence(**occurrence)

    def get_experiment(self, experiment_id: str = None) -> Experiment:
        raise NotImplementedError

    def get_trait(self, trait_id: str = None) -> Trait:
        raise NotImplementedError
