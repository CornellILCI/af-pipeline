import os
import requests
import pandas as pd
from urllib.parse import urljoin
import common
import config

SEARCH_MEAS_BY_PLOT_DATA = "/plot-data/{plot_data_id}/plots-data-search"

class MeasReader:
    """ reads measurement data from data source through API.
    """

    def __init__(self, **kwargs):
        pass

    def get_meas_by_plot(self, plot_data_id: int = None) -> pd.DataFrame:

        meas_url = common.url_join(config.API_BASE_URL,
                                    SEARCH_MEAS_BY_PLOT_DATA)
        data = {}

        return pd.DataFrame(data)
