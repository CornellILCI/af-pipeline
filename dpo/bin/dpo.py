import sys, os, json
import argparse
import pandas as pd
from glob import glob
import numpy as np

aeoPython = os.environ["EBSAF_ROOT"] + "/aeo/python"
sys.path.append(aeoPython)
import simbaUtils

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Input folder")
args = parser.parse_args()

# Initialize paths
simbaUtils.readConfig()
tmp = simbaUtils.cfg["mdl"] + "/analysis/cimmyt/phenotypic/asreml"
phenomodels = simbaUtils.cfg["mdl"] + "/analysis/cimmyt/phenotypic/asreml"
req = simbaUtils.cfg["int"] + "/" + args.input + "/" + args.input + ".req"


class Dpo(object):

    array = req.replace("req", "arr")
    conf = simbaUtils.cfg["mdl"] + "/analysis/cimmyt/phenotypic/asreml/config/"

    output = glob(os.environ["EBSAF_ROOT"] + "/aeo/input/")

    def __init__(self, request):
        self.request = request
        self.req = None
        self.id = None
        self.pat = None
        self.cfg = None
        self.fields = None
        self.traitList = None
        self.array = Dpo.array
        self.arr = None
        self.conf = Dpo.conf
        self.sf = None
        self.map = None
        self.occList = None
        self.mdf = None
        self.csv = None
        self.outdir = Dpo.output
        self.idx = 0
        self.idx2 = 0
        self.occ = 0

    def loadReq(self):
        try:
            with open(self.request, "r") as req:
                self.req = json.load(req)
        except ValueError:
            pass
        self.id = self.req["metadata"]["id"][:-4] + "1000"
        self.outdir = self.outdir[0] + self.req["metadata"]["id"]
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        self.pat = self.req["parameters"]["exptloc_analysis_pattern"]

    #  gather the fields which will
    def loadConfig(self):

        self.cfg = self.conf + self.req["parameters"]["configFile"] + ".cfg"

        # print("sel ", self.cfg)
        try:
            with open(self.cfg, "r") as cfg:
                self.cfg = json.load(cfg)
        except ValueError:
            pass
        self.fields = self.cfg["Analysis_Module"]["fields"]

    #  single dataframe from the multiple arrays in the .array
    def mergeArrays(self):
        try:
            with open(self.array, "r") as arr:
                self.arr = json.load(arr)
        except ValueError:
            pass
        p = self.arr["data"]["plotArray"]
        m = self.arr["data"]["measurementArray"]
        p = pd.DataFrame(p["data"], columns=p["headers"])
        m = pd.DataFrame(m["data"], columns=m["headers"])
        self.mdf = pd.merge(p, m)

    # map definition to the ,stat factor by creating a map object,
    # and map  stat factor to the definition named columns in the df
    def mapColumns(self):
        map = pd.DataFrame()
        map["def"] = [d["definition"] for d in self.fields]
        map["sf"] = [f["stat_factor"] for f in self.fields]
        self.map = map.set_index("def").to_dict()
        ti = self.mdf["trait_id"]
        tv = self.mdf["trait_value"]
        oi = self.mdf["occurr_id"]
        self.mdf.columns = self.mdf.columns.to_series().map(self.map["sf"])
        self.mdf["trait"] = tv
        self.mdf["trait_id"] = ti
        self.mdf["occid"] = oi

    # set the occurrence list for
    def preFilter(self):
        occList = self.req["data"]["occurrence_id"]
        self.occList = [float(n) for n in occList]
        sf = [d["stat_factor"] for d in self.fields]
        sf.append("trait")
        sf.append("trait_id")
        sf.append("occid")
        self.sf = sf

    def selectFilter(self):
        if self.pat == 1:
            dpo.seslFilter()
        if self.pat == 2:
            dpo.semlFilter()

    def seslFilter(self):
        idx, idx2 = 0, 0
        traits = pd.DataFrame(self.arr["data"]["traitList"][0])
        for trait in traits["trait_id"]:
            for self.occ in self.occList:
                self.mdf = self.mdf[self.sf].copy(deep=True)  #
                self.name = traits.loc[traits["trait_id"] == trait, "name"].values[0]  #
                fdf = self.mdf.loc[self.mdf["trait_id"] == int(trait)]
                fdf = fdf.drop(["trait_id"], axis=1)
                fdf = fdf[fdf["occid"] == self.occ]
                fdf = fdf.drop(["occid"], axis=1)
                fdf = fdf.rename(columns={"trait": f"{self.name}"})
                dpo.buildCSV(fdf, idx)
                idx += 1
            idx2 += 1

    def semlFilter(self):
        traits = pd.DataFrame(self.arr["data"]["traitList"][0])
        for idx, trait in enumerate(traits["trait_id"]):
            self.mdf = self.mdf[self.sf].copy(deep=True)
            self.name = traits.loc[traits["trait_id"] == trait, "name"].values[0]
            fdf = self.mdf.loc[self.mdf["trait_id"] == int(trait)]
            fdf = fdf.drop(["trait_id"], axis=1)
            fdf = fdf.drop(["occid"], axis=1)
            fdf = fdf.rename(columns={"trait": f"{self.name}"})
            fdf = fdf.loc[:, fdf.columns.notnull()]
            dpo.buildCSV(fdf, idx)
            idx += 1

    def buildCSV(self, fdf, idx):
        fdf.to_csv(self.outdir + "/" + self.id[: -len(str(idx + 1))] + str(idx + 1) + ".csv", index=False)
        self.mdf.rename(columns={f"{str(self.name)}": "trait"}, inplace=True)
        dpo.buildAs(idx)

    def buildAs(self, idx):  # only called through filter df
        jobL = len(str(idx + 1))
        csv = self.id[:-jobL] + str(idx + 1) + ".csv"
        asr = self.outdir + "/" + self.id[:-jobL] + str(idx + 1) + ".as"
        module = self.cfg["Analysis_Module"]
        title = str(self.id[:-jobL] + str(idx + 1))
        res = self.req["parameters"]["residual"]
        res = [d["spatial_model"] for d in module["residual"] if d["spatial_id"] == f"{res}"]
        pred = self.req["parameters"]["prediction"][0]
        pred = [d["statement"] for d in module["predict"] if d["id"] == f"{pred}"]
        form = self.req["parameters"]["formula"]
        form = [d["statement"] for d in module["formula"] if d["id"] == f"{form}"]
        formula = form[0].replace("{trait_name}", self.name)
        options = csv + " " + module["asrmel_options"][0]["options"]
        tabulate = "tabulate " + module["tabulate"][0]["statement"].replace("{trait_name}", self.name)
        predictedTrait = "prediction " + str(pred[0])
        if str(res[0]) == "":
            residual = ""
        else:
            residual = "residual " + str(res[0] + "\n")
        asr = open(asr, "w")
        fs = module["fields"]
        sf, dt, c = "stat_factor", "data_type", "condition"
        fields = [f"\n \t{fs[x][sf]} {fs[x][dt]} {fs[x][c]}" for x in range(len(fs))]
        # write the .as file
        asr.writelines(title)
        asr.writelines(fields)
        asr.writelines(
            "\n" + self.name + "\n" + options + "\n" + tabulate + "\n" + formula + "\n" + residual + predictedTrait
        )


dpo = Dpo(req)

if __name__ == "__main__":
    dpo.loadReq()
    dpo.loadConfig()
    dpo.mergeArrays()
    dpo.mapColumns()
    dpo.preFilter()

    dpo.selectFilter()
