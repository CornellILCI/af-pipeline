import pandas as pd

from models.experiment import Experiment
from models.trait import Trait

from data_reader.phenotype_data import PhenotypeData

from exceptions import DataReaderException

SEARCH_PLOTS_BY_OCCURRENCE_URL = "/occurrences/{occurrence_id}/plots-search"


class PhenotypeDataEbs(PhenotypeData):
    """ reads phenotype data from a ebs data source.
    """

    API_FIELDS_TO_LOCAL_FIELDS = {
        "plotDbId": "plot_id",
        "entryDbId": "entry_id",
        "paX": "pa_x",
        "paY": "pa_y",
        "rep": "rep_factor",
        "blockNumber": "blk",
        "plotQcCode": "plot_qc"
    }

    def get_plots_by_occurrence_id(self,
                                   occurrence_id: int = None) -> pd.DataFrame:

        plots_endpoint = SEARCH_PLOTS_BY_OCCURRENCE_URL.format(
            occurrence_id=occurrence_id)

        api_response = self.post(endpoint=plots_endpoint)

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        plots_data = api_response.body["result"]["data"]

        plots_df = pd.DataFrame(plots_data)
        plots_df.rename(
            columns=self.API_FIELDS_TO_LOCAL_FIELDS,
            inplace=True
        )

        return plots_df

    def get_plots_measurements_by_occurrence_id(
            self,
            occurrence_id: int = None) -> pd.DataFrame:
        raise NotImplementedError

    def get_experiment(self, experiment_id: int = None) -> Experiment:
        raise NotImplementedError

    def get_trait(self, trait_id: int = None) -> Trait:
        raise NotImplementedError
