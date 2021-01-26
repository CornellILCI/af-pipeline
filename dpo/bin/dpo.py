#!/usr/bin/python3
# dpo.py
# uses json input to generate .as and csv files for analysis
# 2021.1.12, vparis, vsp35@cornell.edu

import sys, os, json
import argparse
import pandas as pd
import numpy as np
from glob import glob


# import dbUtils
# print(os.environ['EBSAF_ROOT'])

aeoPython = os.environ["EBSAF_ROOT"] + "/aeo/python"
sys.path.append(aeoPython)

import simbaUtils

simbaUtils.readConfig()
tmp = "/models/analysis/cimmyt/phenotypic/asreml"
# phenomodels = simbaUtils.cfg['mdl'] + "/analysis/cimmyt/phenotypic/asreml"
# print(phenomodels)
# redo request file as workpath simbautils.cfg['int']
parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Input folder")
args = parser.parse_args()


class Dpo:

    # currently to linked to pedros,
    # now it should be connected to the input path (int)
    request = os.environ["EBSAF_ROOT"] + tmp+ "/templates/" \
              + sys.argv[1] + "/" + sys.argv[1] + ".req"
    array = request.replace("req", "arr")
    conf = glob(os.environ["EBSAF_ROOT"] + tmp + "/config/")
    output = glob(os.environ["EBSAF_ROOT"] + "/aeo/input/")

    def __init__(self):
        self.request = Dpo.request
        self.req = None
        self.id = None
        self.expLocPat = None
        self.array = Dpo.array
        self.arr = None
        self.plotDf = None
        self.measDf = None
        self.traitDf = None
        self.conf = Dpo.conf
        self.cfg = None
        self.cfgId = None
        self.defs = None
        self.sf = None
        self.occList = None
        self.mergedDf = None
        self.csv = None
        self.asr = None
        self.out = Dpo.output
        self.idx = 0
        self.idx2 = 0
        self.occ = 0

    def preDF(self):

        with open(self.request, "r") as req:
            # load req and set output id
            self.req = json.load(req)
            self.id = self.req["metadata"]["id"]
            self.out = self.out[0] + self.id
            self.id = self.id[:-4] + "1000"

            # create the output directory
            if not os.path.exists(self.out): os.makedirs(self.out)

            # set experiment location pattern, config, and config Id
            self.cfg = self.conf[0] + self.req['parameters']['configFile'] + ".cfg"
            self.cfgId = self.req['parameters']['configFile'][-1:]

    def buildDFs(self):

        # open the input array + config JSONs:
        with open(self.cfg, "r") as cfg, open(self.array, "r") as arr:

            # get the plot and measurement subarrays
            self.arr = json.load(arr)
            plotArray = self.arr["data"]["plotArray"]
            measArray = self.arr["data"]["measurementArray"]
            traitList = self.arr["data"]["traitList"]

            # transform the sub-arrays into DataFrames
            self.plotDf = pd.DataFrame(plotArray["data"], columns=plotArray["headers"])
            self.measDf = pd.DataFrame(measArray["data"], columns=measArray["headers"])
            self.traitDf = pd.DataFrame(traitList[0])

            # get fields from the config
            self.cfg = json.load(cfg)
            fields = self.cfg["Analysis_Module"]["fields"]
            self.defs = [fields[n]["definition"] for n in range(len(fields))]

    def mergeDFs(self):

        # merge dfs, filter fields, add traits
        mdf = pd.merge(self.plotDf, self.measDf)
        print(mdf.columns)

        # rename cols for the merged dataframe
        defs = [d['definition'] for d in self.cfg['Analysis_Module']["fields"]]
        self.sf = [d['stat_factor'] for d in self.cfg['Analysis_Module']["fields"]]
        mapdf = pd.DataFrame()
        mapdf['def'] = defs
        mapdf['sf'] = self.sf
        d = mapdf.set_index('def').to_dict()
        # print(d)
        # for key, value in d.items():
        #     print(key, value)
        ti = mdf['trait_id']
        tv = mdf['trait_value']
        oi = mdf['occurr_id']

        # map the stat factor columns to the dataframe
        mdf.columns = mdf.columns.to_series().map(d['sf'])

        self.mergedDf = mdf
        self.mergedDf['trait'] = tv
        self.mergedDf['trait_id'] = ti
        self.mergedDf['occid'] = oi

    def filterDF(self):
        mdf = self.mergedDf
        print(mdf)
        tdf = self.traitDf
        self.id = self.id[:-4]+"1000"
        self.idx, self.idx2 = 0, 0
        jobL = len(str(self.idx))
        self.occList = self.req["data"]["occurrence_id"]
        self.occList = [float(n) for n in self.occList]
        expLocPat = self.req['parameters']["exptloc_analysis_pattern"]

        f = self.sf
        f.append("trait")
        f.append("trait_id")
        f.append('occid')
        # print(f)

        if expLocPat == 1:
            print("SESL")

            # for each unique trait
            for trait in tdf["trait_id"]:

                # for each occ in the occList
                for self.occ in self.occList:

                    mdf = mdf[f].copy(deep=True)

                    # get the trait name, for same position as trait id in tdf
                    name = tdf.loc[tdf["trait_id"] == trait, "name"].values[0]
                    self.name = name

                    # rename merged df trait column to the selected trait name
                    mdf.rename(columns={"trait": f"{str(self.name)}"}, inplace=True)

                    # filter mdf where trait id == trait n in tdf
                    fdf = mdf.loc[mdf["trait_id"] == int(trait)]
                    fdf = fdf.drop(['trait_id'], axis=1)
                    fdf = fdf[fdf["occid"] == self.occ]


                    # replace and drop NaNs
                    df = fdf[fdf["occid"] == self.occ]
                    df = fdf.replace('NA', np.nan)
                    df = df.loc[:, df.columns.notnull()]
                    df = df.dropna(axis=1, how="all")
                    print(df)

                    # write the merged, twice-filtered dataframe to a csv file
                    l = self.idx + 1
                    df.to_csv(self.out + "/" + self.id[:-len(str(l))] +
                              str(self.idx + 1) + ".csv", index=False)

                    # reset name of the trait column in the df for next pass
                    mdf.rename(columns={f"{str(name)}": "trait"}, inplace=True)

                    # build .as
                    dpo.buildAs()

                    # for output
                    self.idx += 1

                self.idx2 += 1

        if expLocPat == 2:
            print("SEML")

            for self.idx, trait in enumerate(tdf['trait_id']):
                # get the trait name for the current pass
                name = tdf.loc[tdf["trait_id"] == trait, "name"].values[0]
                self.name = name

                # rename mdf trait column, filter mdf x trait to make fdf
                mdf.rename(columns={"trait": f"{self.name}"}, inplace=True)

                # filter mdf where trait id == trait n in tdf
                fdf = mdf.loc[mdf["trait_id"] == int(trait)]
                fdf = fdf.drop(['trait_id'], axis=1)

                # replace and drop NaNs
                df = fdf.replace('NA', np.nan)
                df = df.loc[:, df.columns.notnull()]
                df = df.dropna(axis=1, how="all")
                print(df)

                # write the filtered dataframe to the proper csv
                df.to_csv(self.out + "/" + self.id[:-jobL]
                          + str(self.idx + 1) + ".csv", index=False)

                # reset name of the trait column in the df for next pass
                mdf.rename(columns={f"{str(name)}": "trait"}, inplace=True)

                # build .as
                dpo.buildAs()

                self.idx += 1

    def buildAs(self):  # only called through filter df

        jobL = len(str(self.idx + 1))
        csv = self.id[:-jobL] + str(self.idx + 1) + ".csv"

        # set the variables, with indices to be used by filtering loop
        asr = self.out + "/" + self.id[:-jobL] + str(self.idx + 1) + ".as"
        trait = self.arr['data']['traitList'][0]['name'][self.idx2]
        module = self.cfg['Analysis_Module']
        title = str(self.id[:-jobL] + str(self.idx + 1))

        res = self.req['parameters']["residual"]
        res = [d['spatial_model'] for d in module["residual"] if d['spatial_id'] == f'{res}']

        pred = self.req['parameters']["prediction"][0]
        pred = [d['statement'] for d in module["predict"] if d['id'] == f'{pred}']

        # get the fields for the .as file from the cfg module
        options = csv + " " + module['asrmel_options'][0]['options']
        tabulate = "tabulate " + module['tabulate'][0]['statement'].replace("{trait_name}", trait)
        predictedTrait = "prediction " + str(pred[0])

        if str(res[0]) == "":
            residual = ""
        else:
            residual = "residual " + str(res[0] + "\n")

        if self.cfgId == "4":
            formula = module['formula'][0]['statement'].replace("{trait_name}", trait)
        else:
            formula = module['formula'][0]['statement'].replace("{trait_name}", trait)

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


dpo = Dpo()

if __name__ == "__main__":
    dpo.preDF()
    dpo.buildDFs()
    dpo.mergeDFs()
    dpo.filterDF()
