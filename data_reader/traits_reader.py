import os
import requests
import pandas as pd
from urllib.parse import urljoin
import common
import config

SEARCH_MEAS_BY_PLOT_DATA = "/plot-data/{plot_data_id}/plots-data-search"


class TraitsReader:
    """ reads traits from data source through API.
    """

    def __init__(self, **kwargs):
        pass

    def getTraitsByOccurrenceId(self, occurrence_id: int = None) -> pd.DataFrame:

        traits_url = common.url_join(config.API_BASE_URL,
                                    SEARCH_TRAITS_BY_OCCURRENCE_URL)
        data = {}
        return pd.DataFrame(data)
