import rpy2.robjects as ro
import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

from rpy2.robjects.conversion import localconverter

import pathlib

#Uncomment when used as a task
#@app.task(base=FailureReportingTask)
def example_sommer_task():
    ro.r("""print(getwd())""")
    ro.r("""setwd('""" + str(pathlib.Path(__file__).parent.absolute()) + """')""")

    #Load the R file
    r = ro.r
    r.source('SommerExample1.R')

    Pheno = pd.read_csv(str(pathlib.Path(__file__).parent.absolute())+"/input/Phenogenotyped.csv")
    with localconverter(ro.default_converter + pandas2ri.converter):
        Pheno_r = ro.conversion.py2rpy(Pheno)
    del Pheno

    A = pd.read_table(str(pathlib.Path(__file__).parent.absolute())+"/input/A.txt", sep=' ')
    with localconverter(ro.default_converter + pandas2ri.converter):
        A_r = ro.conversion.py2rpy(A)
    del A

    #Call the R function
    rfunction = ro.r['calculate']
    result = rfunction(Pheno_r, A_r)

#Remove when made into a task
example_sommer_task()

#Convert a R to python
#with localconverter(ro.default_converter + pandas2ri.converter):
#  pd_from_r_df = ro.conversion.rpy2py(result)

# Convert Python to R
# with localconverter(ro.default_converter + pandas2ri.converter):
#   r_from_pd_df = ro.conversion.py2rpy(pd_df)


