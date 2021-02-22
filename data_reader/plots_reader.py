import os
import requests

import pandas as pd

from urllib.parse import urljoin

import common
import config

SEARCH_PLOTS_BY_OCCURRENCE_URL = "/occurrences/{occurrence_id}/plots-search"
# we'll fill that dynamically


class PlotsReader:
    """ reads plots data from data source through API.
    """

    def __init__(self, **kwargs):
        pass

    def plots_get_by_occurrence_id(self,
                                   occurrence_id: int = None) -> pd.DataFrame:

        plots_url = common.url_join(config.API_BASE_URL,
                                    SEARCH_PLOTS_BY_OCCURRENCE_URL)
                                    # config has the environment variable
                                    # plots by occurrence
        data = {}
        return pd.DataFrame(data)
