from typing import Iterable

from pandas import DataFrame


def df_keep_columns(df: DataFrame, columns_to_keep: Iterable[str]) -> DataFrame:
    """Keeps only columns in given set.

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
