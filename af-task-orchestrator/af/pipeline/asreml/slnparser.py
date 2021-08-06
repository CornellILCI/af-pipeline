import pandas as pd

SLN_FILE_COLUMNS_TO_DB_COLUMNS = {"Model_Term":"model_term",
     "Level":"level",
     "Effect":"effect",
     "seEffect":"se_effect"}

static = ["model_term", "level", "effect", "se_effect"]

def parse_sln_file(slnfile) -> pd.DataFrame:
    try:
        df = pd.read_csv(slnfile, delimiter="\s+" )
        df.rename(columns=SLN_FILE_COLUMNS_TO_DB_COLUMNS, inplace=True)
        agg_cols = [x for x in df.columns if x not in set(static)]
        df = df.join(df[agg_cols].agg(dict,axis=1).to_frame('additional_info')).drop(agg_cols,1)
        df = df.astype(str)
        print(df)
        return df
    except KeyError:
        raise ColumnNotAvailableError(slnfile)



f67 = "/home/vince/dev/work/wfiles/resPedro/templatesB/67ac5d6f-5cdc-45fd-a2fa-2bc17a2c58bg_SA_0000/results/67ac5d6f-5cdc-45fd-a2fa-2bc17a2c58bg_SA_1001.sln"
f69 = "/home/vince/dev/work/wfiles/resPedro/templatesB/69ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ac_SA_0000/results/69ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ac_SA_1001_sln.txt"

parse_sln_file(f69)

testDfb = pd.DataFrame(columns=['model_term','level','effect','se_effect','additional_info'])
testDfb.loc[0] = pd.Series({'model_term': 'rep',
                          'level': '1',
                          'effect': '0.0',
                          'se_effect': '0.0',
                          'additional_info': str({'GiEffect': -0.245804, 'AOMstat': -0.268525})})
string = 'Model_Term\tLevel\tEffect\tseEffect\nrep\t1\t0.0\t0.0'




str2  = 'Model_Term\tLevel\tEffect\tseEffect\tGiEffect\tAOMstat\nmv_estimates\t2\t6.53511\t1.54492\t0.627188\t0.685164'
print(str2)
