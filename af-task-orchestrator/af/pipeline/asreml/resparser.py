import pandas as pd
import re

sd = [" SD", "STND"]

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

                SD = re.search('\[(.*?)\]', res[x])

                if SD is not None:
                    data = row.split('\t')
                    result = re.findall("\d+\.\d+", data[0])
                    SD = SD.group(1)
                    SD = [SD, result[0]]
                    df.loc[len(df.index)] = SD
                    x = x+1

            if sd[1] in row:
                data = row.split('\t')
                SD = [data[1], data[3]]
                df.loc[len(df.index)] = SD

        print(df)
        return df

    if len(res) == 0 :
        print("no outliers found\n")
