from tempfile import NamedTemporaryFile

import pandas as pd
import re


sd = [" SD", "STND"]

f67 = "/home/vince/dev/work/wfiles/resPedro/templatesB/67ac5d6f-5cdc-45fd-a2fa-2bc17a2c58bg_SA_0000/results/67ac5d6f-5cdc-45fd-a2fa-2bc17a2c58bg_SA_1001.res"
f68 = "/home/vince/dev/work/wfiles/resPedro/templatesB/68ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ab_SA_0000/results/68ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ab_SA_1001.res"
f69 = "/home/vince/dev/work/wfiles/resPedro/templatesB/69ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ac_SA_0000/results/69ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ac_SA_1001.res"
f84 = "/home/vince/dev/work/wfiles/resPedro/templatesB/84ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ae_SA_0000/results/84ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ae_SA_1001.res"
f85 = "/home/vince/dev/work/wfiles/resPedro/templatesB/85/results/85.res"

li = [f67, f68, f69, f84, f85]

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

                SD = re.search('\[(.*?)\]', res[x]).group(1)
                SD = [SD, row[-9:-4]]
                df.loc[len(df.index)] = SD
                x = x+1

            if sd[1] in row:

                SD = [row[12:16], row[-6:-1]]
                df.loc[len(df.index)] = SD

        print(df)
        return df


    if len(res) == 0 :
        print("no outliers found\n")

# s67 and testdf are the same strings im using in the txt file
s67 = '\t\t\t\t\t  Record     SD\n0  section 11, column 14 (of 15), row 22 (of 28)   3.70\n1   section 11, column 15 (of 15), row 2 (of 28)   3.61'
print(s67)

testDf = pd.DataFrame({'Record': ['section 11, column 14 (of 15), row 22 (of 28)', 'section 11, column 15 (of 15), row 2 (of 28)'],
                           'SD': [' 3.70', ' 3.61'] })
print(testDf, "\n\n\n")

# runs the parser
# parse_res(check_file(f67))
[parse_res(check_file(r)) for r in li]
