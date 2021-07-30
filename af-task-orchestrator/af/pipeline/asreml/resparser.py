from tempfile import NamedTemporaryFile

import pandas as pd
import re


sd = [" SD", "STND"]

f67 = "/home/vince/dev/work/wfiles/resPedro/templatesB/67ac5d6f-5cdc-45fd-a2fa-2bc17a2c58bg_SA_0000/results/67ac5d6f-5cdc-45fd-a2fa-2bc17a2c58bg_SA_1001.res"
# f68 = "/home/vince/dev/work/wfiles/resPedro/templatesB/68ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ab_SA_0000/results/68ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ab_SA_1001.res"
f69 = "/home/vince/dev/work/wfiles/resPedro/templatesB/69ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ac_SA_0000/results/69ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ac_SA_1001.res"
# f84 = "/home/vince/dev/work/wfiles/resPedro/templatesB/84ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ae_SA_0000/results/84ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ae_SA_1001.res"
# f85 = "/home/vince/dev/work/wfiles/resPedro/templatesB/85/results/85.res"
li = [ f69]

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

                    SD = SD.group(1)
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



# li2 = [parse_res(check_file(r)) for r in li]
# print(li2[0][0:2])
#
f69 = "STND RES\t30\t12.362\t3.81\nSTND RES\t30\t12.362\t2.38"

print(parse_res(check_file(li[0])))

testDf2 = pd.DataFrame({'Record': ['30', '30'],
                           'SD': [' 3.81', ' 2.38']})
print(testDf2)
