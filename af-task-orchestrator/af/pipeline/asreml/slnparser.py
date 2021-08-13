import pandas as pd

SLN_FILE_COLUMNS_TO_DB_COLUMNS = {"Model_Term":"model_term",
     "Level":"level",
     "Effect":"effect",
     "seEffect":"se_effect"}

static = ["model_term", "level", "effect", "se_effect"]

def parse_sln_file(slnfile) -> pd.DataFrame:
    
    """
    write a mock df string to a temporary file
    pass temp file to the handler for transform
    compare transform to manually constructed df"""

    try:
        df = pd.read_csv(slnfile, delimiter="\s+" )
        df.rename(columns=SLN_FILE_COLUMNS_TO_DB_COLUMNS, inplace=True)
        agg_cols = [x for x in df.columns if x not in set(static)]
        df = df.join(df[agg_cols].agg(dict,axis=1).to_frame('additional_info')).drop(agg_cols,1)
        df = df.astype(str)
        return df
    except KeyError:
        raise ColumnNotAvailableError(slnfile)

testDfb = pd.DataFrame(columns=['model_term','level','effect','se_effect','additional_info'])
testDfb.loc[0] = pd.Series({'model_term': 'rep',
                          'level': '1',
                          'effect': '0.0',
                          'se_effect': '0.0',
                          'additional_info': str({'GiEffect': -0.245804, 'AOMstat': -0.268525})})
string = 'Model_Term\tLevel\tEffect\tseEffect\nrep\t1\t0.0\t0.0'

str2  = 'Model_Term\tLevel\tEffect\tseEffect\tGiEffect\tAOMstat\nmv_estimates\t2\t6.53511\t1.54492\t0.627188\t0.685164'
