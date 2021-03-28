# For common utils methods across packages

from urllib.parse import urljoin, urlparse

import pandas as pd

from typing import Iterable


def valid_url(url):
    """ retruns True if url is a valid http url"""

    valid_schemes = {"http", "https"}

    if not isinstance(url, str) or not url.strip():
        return False
    urlparts = urlparse(url)

    return urlparts.scheme in valid_schemes


def url_join(base_url: str, relative_url: str) -> str:
    base_url = base_url.rstrip("/") + "/"
    relative_url = relative_url.lstrip("/")

    return urljoin(base_url, relative_url)


def df_keep_columns(df: pd.DataFrame,
                    columns_to_keep: Iterable[str]) -> pd.DataFrame:
    """ Keeps only columns in given set.

    Keeps only columns in input set and drops columns not in the given set.
    Unmapped column in input set is ignored.

    Args:
        df:
            Input dataframe
        columns_to_keep:
            set of columns to keep in dataframe.

    Returns:
        df with only columns to keep.
    """

    # convert to set
    columns_to_keep = set(columns_to_keep)

    columns_to_drop = set(df.columns) - columns_to_keep
    columns_to_keep = set(df.columns) - columns_to_drop
    df = df[columns_to_keep]

    return df
