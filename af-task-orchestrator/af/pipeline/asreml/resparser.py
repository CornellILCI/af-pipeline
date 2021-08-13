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

# t = NamedTemporaryFile()
# f67row = 'Residual [section 11, column 14 (of 15), row 22 (of 28)] is  3.70 SD\nResidual [section 11, column 15 (of 15), row 2 (of 28)] is  3.61 SD '
# t.write(bytes(f67row, 'UTF-8'))
# t.seek(0)
# testDf = pd.DataFrame({'Record': ['section 11, column 14 (of 15), row 22 (of 28)', 'section 11, column 15 (of 15), row 2 (of 28)'],
#                            'SD': [' 3.70', ' 3.61'] })
# # print(testDf)
# handler = parse_res(check_file(t.name))
# assert_frame_equal(handler,testDf)
