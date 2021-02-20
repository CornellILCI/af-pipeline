import os
import requests
import pandas as pd
from urllib.parse import urljoin
import common
import config

SEARCH_MEAS_BY_OCCURRENCE_URL = "/occurrences/{occurrence_id}/plots-  search"


class MeasReader:
    """ reads measurement data from data source through API.
    """

    def __init__(self, **kwargs):
        pass

    def getMeasByOccurrenceId(self, occurrence_id: int = None) -> pd.DataFrame:

        meas_url = common.url_join(config.API_BASE_URL,
                                    SEARCH_MEAS_BY_OCCURRENCE_URL)
        data = {}
        return pd.DataFrame(data)
