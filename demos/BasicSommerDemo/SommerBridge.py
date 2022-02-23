#this tests if we can build a json file in python and point the script to it.
import os
import json
import uuid

unique_filename = str(uuid.uuid4())+".json"
here = os.getcwd()+"/demos/BasicSommerDemo"

data = {}

data['rep'] = 1
data['grm'] = here+"/Input/GRM.txt"
# data['input_phenotypic_data'] = here+"/Input/Phenofounders2.csv"
data['input_phenotypic_data'] = here+"/Input/2cd7238d-1d50-4b2b-b514-e1f2b80bcd60.csv"

# data['fixed'] = "Phenotype~rep" #"{trait_name}~rep" trait_name is the column in the 
# data['random'] = "~ID" #"~vs(ID, Gu=A)"
data['formula'] = "fixed=%trait%~Rep, random=~ID"
data['rcov'] = "~ units"

data['trait'] = "GrYld_Comp_kgha"

#outputs
data['output_var'] = here+"/Output/var.csv"
data['output_statmodel'] = here+"/Output/statmodel.csv"
data['output_BV'] = here+"/Output/BVs.csv"
data['output_pred'] = here+"/Output/pvs.csv"
data['output_yhat'] = here+"/Output/Yhat.csv"
data['output_outliers'] = here+"/Output/outliers.csv"
data['raw_analysis_out'] = here+"/Output/out.rds"

os.system("echo "+here)
#creates a json file
with open(unique_filename, 'w') as outfile:
    json.dump(data, outfile)

os.system("echo PYTHON CONSOLE TEST 1")
# ret = os.system("rscript "+here+"/SommerCalculationFull.R "+unique_filename)
ret = os.system("rscript "+here+"/SommerTest.R "+unique_filename)

os.system("echo R script ended with code: "+str(ret))

os.system("echo Removing created file "+unique_filename)

os.system("rm "+os.getcwd()+"/"+unique_filename)
