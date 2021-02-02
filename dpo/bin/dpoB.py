##!/usr/bin/python3
# dpo.py
# uses json input to generate .as and csv files for analysis
# 2021.1.12, vparis, vsp35@cornell.edu

import sys, os, json
import argparse
import pandas as pd
from glob import glob
import numpy as np

aeoPython = os.environ["EBSAF_ROOT"] + "/aeo/python"
sys.path.append(aeoPython)
import simbaUtils

simbaUtils.readConfig()
tmp = "/models/analysis/cimmyt/phenotypic/asreml"
phenomodels = simbaUtils.cfg['mdl'] + "/analysis/cimmyt/phenotypic/asreml"
parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Input folder")
args = parser.parse_args()
req = os.environ["EBSAF_ROOT"] + tmp + "/templates/" \
          + sys.argv[1] + "/" + sys.argv[1] + ".req"


class Dpo(object):
    array = req.replace("req", "arr")
    conf = glob(os.environ["EBSAF_ROOT"] + tmp + "/config/")
    output = glob(os.environ["EBSAF_ROOT"] + "/aeo/input/")

    def __init__(self, request):
        self.request = request
        self.req = None
        self.dir = None
        self.id = None
        self.pat = None
        self.cfg = None
        self.fields = None
        self.plotArray = None
        self.measArray = None
        self.traitList = None
        self.expLocPat = None
        self.array = Dpo.array
        self.arr = None
        self.plotDf = None
        self.measDf = None
        self.traitDf = None
        self.conf = Dpo.conf
        self.defs = None
        self.sf = None
        self.map = None
        self.occList = None
        self.mdf = None
        self.csv = None
        self.asr = None
        self.outdir = Dpo.output
        self.idx = 0
        self.idx2 = 0
        self.occ = 0

    def loadReq(self):
        with open(self.request, "r") as req:
            self.req = json.load(req)
            self.id = self.req["metadata"]["id"][:-4] + "1000"
            self.pat = self.req['parameters']["exptloc_analysis_pattern"]
            self.outdir = self.outdir[0] + self.req["metadata"]["id"]
            if not os.path.exists(self.outdir): os.makedirs(self.outdir)

    def loadConfig(self):
        self.cfg = self.conf[0] + self.req['parameters']['configFile'] + ".cfg"
        with open(self.cfg, "r") as cfg:
            self.cfg = json.load(cfg)
            self.fields = self.cfg['Analysis_Module']["fields"]

    def loadArrays(self):
        with open(self.array, "r") as arr:
            self.arr = json.load(arr)

    def mergeArrays(self):
        plots = self.arr["data"]["plotArray"]
        meas = self.arr["data"]["measurementArray"]
        plots = pd.DataFrame(plots["data"], columns=plots["headers"])
        meas = pd.DataFrame(meas["data"], columns=meas["headers"])
        self.mdf = pd.merge(plots, meas)

    def mapColumns(self):
        map = pd.DataFrame()
        map['def'] = [d['definition'] for d in self.fields]
        map['sf'] = [f['stat_factor'] for f in self.fields]
        self.map = map.set_index('def').to_dict()
        ti = self.mdf['trait_id']
        tv = self.mdf['trait_value']
        oi = self.mdf['occurr_id']
        self.mdf.columns = self.mdf.columns.to_series().map(self.map['sf'])
        self.mdf['trait'] = tv
        self.mdf['trait_id'] = ti
        self.mdf['occid'] = oi

    def preloop(self):
        self.traitList = self.arr["data"]["traitList"]
        self.tdf = pd.DataFrame(self.traitList[0])
        self.occList = self.req["data"]["occurrence_id"]
        self.occList = [float(n) for n in self.occList]
        fields = [d['stat_factor'] for d in self.cfg['Analysis_Module']["fields"]]
        fields.append("trait")
        fields.append("trait_id")
        fields.append('occid')
        self.fields = fields

    def dataFilter(self):
        mdf = self.mdf
        jobL = len(str(self.idx))
        self.idx, self.idx2 = 0, 0
        if self.pat == 1:

            for trait in self.tdf["trait_id"]:

                for self.occ in self.occList:

                    mdf = mdf[self.fields].copy(deep=True)
                    name = self.tdf.loc[self.tdf["trait_id"] == trait, "name"].values[0]
                    self.name = name
                    mdf.rename(columns={"trait": f"{str(self.name)}"}, inplace=True)
                    fdf = mdf[mdf["occid"] == self.occ]
                    fdf = fdf.loc[mdf["trait_id"] == int(trait)]
                    fdf = fdf.drop(['trait_id'], axis=1)
                    fdf = fdf.drop(['occid'], axis=1)
                    print(fdf)
                    l = self.idx + 1
                    fdf.to_csv(self.outdir + "/" + self.id[:-len(str(l))] +
                               str(self.idx + 1) + ".csv", index=False)
                    mdf.rename(columns={f"{str(name)}": "trait"}, inplace=True)
                    dpo.buildAs()

                    self.idx += 1
                self.idx2 += 1

        if self.pat == 2:

            for self.idx, trait in enumerate(self.tdf['trait_id']):

                mdf = mdf[self.fields].copy(deep=True)
                name = self.tdf.loc[self.tdf["trait_id"] == trait, "name"].values[0]
                self.name = name
                mdf.rename(columns={"trait": f"{self.name}"}, inplace=True)
                fdf = mdf.loc[mdf["trait_id"] == int(trait)]
                fdf = fdf.drop(['trait_id'], axis=1)
                fdf = fdf.drop(['occid'], axis=1)
                fdf = fdf.loc[:, fdf.columns.notnull()]
                print(fdf)
                fdf.to_csv(self.outdir + "/" + self.id[:-jobL]
                           + str(self.idx + 1) + ".csv", index=False)
                mdf.rename(columns={f"{str(name)}": "trait"}, inplace=True)
                dpo.buildAs()

                self.idx += 1

    def buildAs(self):  # only called through filter df

        jobL = len(str(self.idx + 1))
        csv = self.id[:-jobL] + str(self.idx + 1) + ".csv"

        # set the variables, with indices to be used by filtering loop
        asr = self.outdir + "/" + self.id[:-jobL] + str(self.idx + 1) + ".as"
        trait = self.arr['data']['traitList'][0]['name'][self.idx2]
        print(self.name)
        module = self.cfg['Analysis_Module']
        title = str(self.id[:-jobL] + str(self.idx + 1))

        res = self.req['parameters']["residual"]
        res = [d['spatial_model'] for d in module["residual"] if d['spatial_id'] == f'{res}']
        pred = self.req['parameters']["prediction"][0]
        pred = [d['statement'] for d in module["predict"] if d['id'] == f'{pred}']
        form = self.req['parameters']["formula"]
        form = [d['statement'] for d in module["formula"] if d['id'] == f'{form}']
        formula = form[0].replace("{trait_name}", self.name)

        # get the fields for the .as file from the cfg module
        options = csv + " " + module['asrmel_options'][0]['options']
        tabulate = "tabulate " + module['tabulate'][0]['statement'].replace("{trait_name}", self.name)
        predictedTrait = "prediction " + str(pred[0])

        if str(res[0]) == "":
            residual = ""
        else:
            residual = "residual " + str(res[0] + "\n")

        # get the sf, dt, and c fields from the cfg module
        asr = open(asr, "w")
        fs = module['fields']
        sf, dt, c = 'stat_factor', 'data_type', 'condition'
        fields = [f"\n \t{fs[x][sf]} {fs[x][dt]} {fs[x][c]}" for x in range(len(fs))]

        # write the .as file
        asr.writelines(title)
        asr.writelines(fields)
        asr.writelines("\n" + self.name + "\n" + options + "\n" + tabulate +
                       "\n" + formula + "\n" + residual + predictedTrait)


dpo = Dpo(req)

if __name__ == "__main__":
    dpo.loadReq()
    dpo.loadConfig()
    dpo.loadArrays()
    dpo.mergeArrays()
    dpo.mapColumns()
    dpo.preloop()
    dpo.dataFilter()
