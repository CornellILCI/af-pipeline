from numpy import NAN
import pandas as pd
import re
import json

sd = [" SD", "STND"]

{"type": "spatial", "data": { "section": NAN, "column": [], "row": [], "SD": 3.7 }}
        

def check_file(file) :
    try:
        with open (file, "rt") as f:
            file = f.readlines()
            res = list(filter(lambda x: any(True for c in sd if c in x), file))
        return res
    except KeyError:
        raise ColumnNotAvailableError(file)

"""
parse_res checks if there is SD and then extracts appropriate data
"""

def parse_res(res)-> pd.DataFrame:
    x = 0
    if len(res) > 0:

        df = pd.DataFrame(columns=['Record','SD'])

        for row in res :

            if sd[0] in row:

                SDrow = re.search('\[(.*?)\]', res[x])
                dict = {'type':'spatial'}
                data = {}

                if SDrow is not None:
                    r = row.split('\t')
                    SDrow = SDrow.group(1)
                    sr = SDrow.split(",")
                    data['section'] = [ re.findall(r'\d+', sr[0])][0][0]
                    data['column'] = [ re.findall(r'\d+', sr[1])][0]
                    data['row'] = [ re.findall(r'\d+', sr[2])][0]
                    data['SD'] = re.findall("\d+\.\d+", r[0])[0]
                    dict['data'] = data
                    rjson = json.dumps(dict)
                    print("\n",rjson,"\n")
                    x = x+1
                    return rjson

            if sd[1] in row:
                dict = {'type':'record'}
                data = {}
                r = row.split('\t')
                # print([data[0]])
                data['record'] = r[1]
                data['value'] = r[2]
                data['scale'] = r[3]
                dict['data'] = data
                rjson = json.dumps(dict)

                print(rjson)


    if len(res) == 0 :
        print("no outliers found\n")


# hi = "/home/vince/dev/work/wfiles/resPedro/templatesB/69ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ac_SA_0000/results/69ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ac_SA_1001.res"
# aloha = check_file(hi)
# parse_res(aloha)