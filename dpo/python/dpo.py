# 2021.1.11, vparis
# Sprint 2020.06

import sys, os, json
import argparse
import pandas as pd
import numpy as np
from glob import glob

tmp = "/models/analysis/cimmyt/phenotypic/asreml"


# replace with argparse
try:
    arg = sys.argv[1]
except IndexError:
    print("Expected 1 argument, got None")
    raise SystemExit


class Dpo:

    request = os.environ["EBSAF_ROOT"] + tmp + "/templates/" \
              + sys.argv[1] + "/" + sys.argv[1] + ".req"
    print(len([sys.argv[1]]))
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
        self.fields = None
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

            # load req and set id
            self.req = json.load(req)
            self.id = self.req["metadata"]["id"]

            # set and create the output directory
            self.out = self.out[0] + "/" + self.id
            if not os.path.exists(self.out): os.makedirs(self.out)

            # set experiment location pattern + config based on request
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

            # transform the subarrays into DataFrames
            self.plotDf = pd.DataFrame(plotArray["data"], columns=plotArray["headers"])
            self.measDf = pd.DataFrame(measArray["data"], columns=measArray["headers"])
            self.traitDf = pd.DataFrame(traitList[0])

            # get fields from the config
            self.cfg = json.load(cfg)
            fields = self.cfg["Analysis_Module"]["fields"]
            self.fields = [fields[n]["definition"] for n in range(len(fields))]

    def mergeDFs(self):

        # get trait id + trait value columns
        traitId = self.measDf["trait_id"]
        traitVal = self.measDf["trait_value"]
        occurrence = self.plotDf["occurr_id"]

        # merge dfs, filter fields, add traits
        mdf = pd.merge(self.plotDf, self.measDf)
        mdf = mdf[self.fields].join(traitId).join(traitVal).join(occurrence)

        # rename cols for the merged dataframe
        self.mergedDf = mdf.rename(
            columns={"loc_id": "loc",
                     "expt_id": "expt",
                     "entry_id": "entry",
                     "plot_id": "plot",
                     "pa_x": "col",
                     "pa_y": "row",
                     "rep_factor": "rep",
                     "trait_value": "trait"})
        # rename definition as stat factor!

    def buildAs(self):  # only called through filter df

        jobL = len(str(self.idx + 1))

        # set the variables, with indices to be used by filtering loop
        asr = self.out + "/" + self.id[:-4] + "100" + str(self.idx + 1) + ".as"
        csv = str(self.id[:-jobL] + str(self.idx + 1)) + ".csv"
        trait = self.arr['data']['traitList'][0]['name'][self.idx2]
        module = self.cfg['Analysis_Module']
        title = str(self.id[:-jobL] + str(self.idx + 1))

        # get the fields for the .as file from the cfg module
        options = csv + " " + module['asrmel_options'][0]['options']
        tabulate = "tabulate " + module['tabulate'][0]['statement'].replace("{trait_name}", trait)

        if self.cfgId == "4":
            formula = module['formula'][0]['statement'].replace("{trait_name}", trait)
        else:
            formula = module['formula'][0]['statement'].replace("{trait_name}", trait)

        predictedTrait = "prediction " + module['predict'][0]['statement']
        residual = "residual " + module['residual'][0]['spatial_model']

        # get the sf, dt, and c fields from the cfg module
        asr = open(asr, "w")
        fs = module['fields']
        sf, dt, c = 'stat_factor', 'data_type', 'condition'
        fields = [f"\n \t{fs[x][sf]} {fs[x][dt]} {fs[x][c]}" for x in range(len(fs))]

        # write the .as file
        asr.writelines(title)
        asr.writelines(fields)
        asr.writelines("\n" + trait + "\n" + options + "\n" + tabulate +
                       "\n" + formula + "\n" + residual + "\n" + predictedTrait)

    def filterDF(self):

        mdf = self.mergedDf
        tdf = self.traitDf
        self.idx, self.idx2 = 0, 0
        self.occList = self.req["data"]["occurrence_id"]
        self.occList = [float(n) for n in self.occList]
        expLocPat = self.req['parameters']["exptloc_analysis_pattern"]

        if expLocPat == 1:

            # for each unique trait
            for trait in tdf["trait_id"]:

                # for each occ in the occList
                for self.occ in self.occList:
                    # get the trait name, for same position as trait id in tdf
                    name = tdf.loc[tdf["trait_id"] == trait, "name"].values[0]

                    # rename merged df trait column to the selected trait name
                    mdf.rename(columns={"trait": f"{str(name)}"}, inplace=True)

                    # filter mdf where trait id == trait n in tdf
                    fdf = mdf.loc[mdf["trait_id"] == int(trait)]

                    # filter filtered df where occurrence id == requested occ
                    df = fdf[fdf["occurr_id"] == self.occ]
                    df = df.drop(['trait_id', "occurr_id"], axis=1)  # drop 'occurr_id'!

                    # replace and drop NaNs
                    df = df.replace('NA', np.nan)
                    df = df.dropna(axis=1, how='all')

                    # write the merged, twice-filtered dataframe to a csv file
                    df.to_csv(self.out + "/" + self.id[:-4] + "100" +
                              str(self.idx + 1) + ".csv", index=False)

                    # reset name of the trait column in the df for next pass
                    mdf.rename(columns={f"{str(name)}": "trait"}, inplace=True)

                    # build .as
                    dpo.buildAs()

                    # for output
                    self.idx += 1

                self.idx2 += 1

        if expLocPat == 2:

            for self.idx, trait in enumerate(tdf['trait_id']):
                # get the trait name for the current pass
                name = tdf.loc[tdf["trait_id"] == trait, "name"].values[0]

                # rename mdf trait column, filter mdf x trait to make fdf
                mdf.rename(columns={"trait": f"{str(name)}"}, inplace=True)

                # filter mdf trait id column == tdf trait n
                fdf = mdf.loc[mdf["trait_id"] == int(trait)]

                # filter mdf where trait id == trait n in tdf
                df = fdf[fdf["occurr_id"].isin(self.occList)]
                df = df.drop(["trait_id", "occurr_id"], axis=1)  # drop 'occurr_id'

                # replace and drop NaNs
                df = df.replace('NA', np.nan)
                df = df.dropna(axis=1, how='all')
                # print(df)

                # write the filtered dataframe to the proper csv
                df.to_csv(self.out + "/" + self.id[:-4] + "100" + str(self.idx + 1) + ".csv", index=False)

                # reset name of the trait column in the df for next pass
                mdf.rename(columns={f"{str(name)}": "trait"}, inplace=True)

                # build .as
                dpo.buildAs()

                self.idx += 1


dpo = Dpo()

if __name__ == "__main__":
    dpo.preDF()
    dpo.buildDFs()
    dpo.mergeDFs()
    dpo.filterDF()
