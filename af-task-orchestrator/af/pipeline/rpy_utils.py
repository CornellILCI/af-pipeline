import os

import rpy2.robjects.packages as rpackages
from af import pipeline
from rpy2 import robjects
from rpy2.robjects.packages import importr


@robjects.packages.no_warnings
def read_csv(file: str):
    """Reads the csv file to return R dataframe.

    Args:
        file: Input file to read and converted to R dataframe.

    Returns:
        R dataframe.
    """

    if not os.path.isfile(file):
        raise pipeline.exceptions.InvalidFilePath(f"File not found {file}")

    utils = importr("utils")

    r_df = utils.read_csv(file=file, sep=",", header=True)

    return r_df
