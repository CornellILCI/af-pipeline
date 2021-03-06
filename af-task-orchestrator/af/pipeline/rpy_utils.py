import os

import pandas as pd
import rpy2.robjects.packages as rpackages
from af import pipeline
from rpy2 import robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr

r_base = importr("base")


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


def rdf_to_pydf(rdf: robjects.DataFrame):
    """Converts R dataframe to Python pandas dataframe.

    If rdf is not R dataframe, then it returns the same object.

    Args:
        rdf: R Dataframe object

    Returns:
        Pandas dataframe
    """

    with localconverter(robjects.default_converter + pandas2ri.converter):
        pydf = robjects.conversion.rpy2py(rdf)

    if type(pydf) == pd.DataFrame:
        return pydf
    return None


def rdf_to_csv(rdf, file_path: str, **csv_kwargs):
    """ Write r dataframe to csv file.
    """

    py_df = rdf_to_pydf(rdf)

    py_df.to_csv(file_path, **csv_kwargs)


class InvalidFormulaError(ValueError):
    pass


@robjects.packages.no_warnings
def r_formula(formula: str):
    if not formula or not formula.strip():
        return None
    try:
        return robjects.Formula(formula)
    except rpy2.rinterface_lib.embedded.RRuntimeError as e:
        raise InvalidFormulaError(f"Invalid Formula: {formula}")
