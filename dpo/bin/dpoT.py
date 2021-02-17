from dpo import  Dpo
import  sys, os, argparse
import  pytest
aeoPython = os.environ["EBSAF_ROOT"] + "/aeo/python"
sys.path.append(aeoPython)

import simbaUtils

simbaUtils.readConfig()
tmp = "/models/analysis/cimmyt/phenotypic/asreml"
parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Input folder")
args = parser.parse_args()
request = os.environ["EBSAF_ROOT"] + tmp + "/templates/" \
          + sys.argv[1] + "/" + sys.argv[1] + ".req"

i = Dpo(request)

print(i.request)
