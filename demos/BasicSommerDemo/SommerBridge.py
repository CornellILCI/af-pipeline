#this tests if we can build a json file in python and point the script to it.
import os
import json
import uuid

unique_filename = str(uuid.uuid4())+".json"
here = os.getcwd()+"/demos/BasicSommerDemo"

data = {}

data['rep'] = 1
data['grm'] = here+"/Input/GRM.txt"
data['phenofounders'] = here+"/Input/Phenofounders2.csv"

data['Phenotype'] = "~rep"
data['random'] = "~vs(ID, Gu=A)"
data['rcov'] = "~ units"


#outputs
data['output_var'] = here+"/Output/var.csv"
data['output_statmodel'] = here+"/Output/statmodel.csv"
data['output_BV'] = here+"/Output/BVs.csv"
data['output_pred'] = here+"/Output/pvs.csv"
data['output_yhat'] = here+"/Output/Yhat.csv"
data['output_outliers'] = here+"/Output/outliers.csv"

os.system("echo "+here)
#creates a json file
with open(unique_filename, 'w') as outfile:
    json.dump(data, outfile)

os.system("echo PYTHON CONSOLE TEST 1")
ret = os.system("rscript "+here+"/SommerCalculationFull.R "+unique_filename)

os.system("echo R script ended with code: "+str(ret))

os.system("echo Removing created file "+unique_filename)

os.system("rm "+os.getcwd()+"/"+unique_filename)
