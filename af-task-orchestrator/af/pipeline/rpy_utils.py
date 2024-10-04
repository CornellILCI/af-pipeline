import os

import pandas as pd
import rpy2.robjects.packages as rpackages
from rpy2.robjects import vectors #DataFrame and StrVector
from af import pipeline
from rpy2 import robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr

from rpy2.robjects import Environment


r_base = importr("base")


@robjects.packages.no_warnings
def read_csv(file: str) -> vectors.DataFrame:
    """Reads the csv file to return R dataframe.

    Args:
        file: Input file to read and converted to R dataframe.

    Returns:
        R dataframe.
    """

    if not os.path.isfile(file):
        raise pipeline.exceptions.InvalidFilePath(f"File not found {file}")

    utils = importr("utils")

    r_df = utils.read_csv(file=file, sep=",", header=True) #na.strings is read.csv's way of saying what can be null, but 'na.strings' isn't recognized here

    return r_df

#Take a raw dataframe and make it a relationship matrix

#R code sample:
#calcGenomicRelationshipMatrix <- function(locusMat){
#  freq <- colMeans(locusMat) / 2
#  locusMat <- scale(locusMat, center=TRUE, scale=F)
#  return(tcrossprod(locusMat) / sum(2*freq*(1-freq)))
#}

#Just write it in R and call it
def relationship_mat_env(r_df):
    #Saw this on someone's blog, no way this works
    robjects.r['source']('scripts/GRM.R')
    funcGRM=robjects.globalenv['calcGenomicRelationshipMatrix']
    
    r_result=funcGRM(r_df)
    return r_result


def relationship_mat(pydf):
    rdf=pydf_to_rdf(pydf)
    return relationship_mat_env(rdf)


def rdf_to_pydf(rdf: robjects.DataFrame) -> pd.DataFrame:
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

def pydf_to_rdf(pydf:pd.DataFrame) -> robjects.DataFrame:
        
    with localconverter(robjects.default_converter + pandas2ri.converter):
        rdf = robjects.conversion.py2rpy(pydf)

    return rdf

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

#Converts a column in an rpy2 dataframe to a factor, as if data_frame$col_name <- as.factor(data_frame$col_name)
def factorize(data_frame:vectors.DataFrame, col_name):
    #if we contain an R 'factor' type - such as 'rep', import_csv will treat it as continuous
    #Effectively we need to do - input_data$rep <- as.factor(input_data$rep)
    column_names:vectors.StrVector=data_frame.colnames #Isn't a series, is actually a StrVector? VSCode failed typing

    #col_idx = data_frame.colnames.index(col_name) #Index calls an exception on run, so replace with most of the source so we can save a stack
    col_idx=-1
    for i, e in enumerate(column_names):
            if e == col_name:
                col_idx = i
    
    #if(col_idx < 0): raise Exception(f"Invalid column named {col_name} in request to 'factorize' {data_frame.colnames}")
    if(col_idx < 0): 
        #print(f"Warning: invalid column named {col_name} in request to 'factorize' {data_frame.colnames}") #Annoying, but catching a lot of stupid errors 
        return data_frame #disable this failure for now

    data_frame[col_idx]=robjects.r(f"as.factor({data_frame[col_idx].r_repr()})")
    return data_frame