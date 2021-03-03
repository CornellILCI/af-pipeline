import os
import requests

import pandas as pd

import common
import config

from models.experiment import Experiment
from models.trait import Trait

SEARCH_PLOTS_BY_OCCURRENCE_URL = "/occurrences/{occurrence_id}/plots-search"


class PhenotypeDataEbs:
    """ reads plots data from data source through API.
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

    def __init__(self, **kwargs):
        pass

    def get_plots_by_occurrence_id(self,
                                   occurrence_id: int = None) -> pd.DataFrame:

        plots_url = common.url_join(config.API_BASE_URL,
                                    SEARCH_PLOTS_BY_OCCURRENCE_URL)
        data = {}
        return pd.DataFrame(data)

    def get_plot_data_by_occurrence_id(
            self,
            occurrence_id: int = None) -> pd.DataFrame:

        raise NotImplementedError

    def get_experiment(self, experiment_id: int = None) -> Experiment:
        raise NotImplementedError

    def get_trait(self, trait_id: int = None) -> Trait:
        raise NotImplementedError
