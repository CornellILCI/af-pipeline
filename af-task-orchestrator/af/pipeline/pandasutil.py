import os
from typing import Iterable

import pandas as pd
from af.pipeline import exceptions


def df_keep_columns(df: pd.DataFrame, columns_to_keep: Iterable[str]) -> pd.DataFrame:
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


def save_df_to_tsv(df: pd.DataFrame, file_name: str, output_folder: str):
    """Saves daataframe as a tab delimitted file.

    Args:
        df:
            Input dataframe
        file_name:
            Name of the tab delimitted file
        output_folder:
            Folder path where the file needs to be saved.
    """

    if not os.path.isdir(output_folder):
        raise exceptions.InvalidFilePath(output_folder + " does not exist")

    file_path = os.path.join(output_folder, file_name)

    df.to_csv(file_path, sep="\t", index=False)
