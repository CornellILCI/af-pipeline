import pandas as pd

YHAT_FILE_COLUMNS_TO_DB_COLUMNS = {"Record":"record",
     "Yhat":"yhat",
     "Residual":"residual",
     "Hat":"hat"}

static = ["record", "yhat", "residual", "hat"]

def parse_yhat_file(yhatfile) -> pd.DataFrame:

    df = pd.read_csv(yhatfile, delimiter="\s+" )
    df.rename(columns=YHAT_FILE_COLUMNS_TO_DB_COLUMNS, inplace=True)
    agg_cols = [x for x in df.columns if x not in set(static)]
    df = df.join(df[agg_cols].agg(dict,axis=1).to_frame('additional_info')).drop(agg_cols,1)
    df = df.astype(str)
    return df


parse_yhat_file('/home/vince/dev/work/ebsaf/af-core/af-task-orchestrator/af/pipeline/yhat/templates/71ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ad_SA_1001_yht (1).txt')
