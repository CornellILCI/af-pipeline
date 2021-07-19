import pandas as pd

from af.pipeline.exceptions import FileParseException

YHAT_FILE_COLUMNS_TO_DB_COLUMNS = {"Record": "record", "Yhat": "yhat", "Residual": "residual", "Hat": "hat"}

static = ["record", "yhat", "residual", "hat"]


def parse(yhatfile) -> pd.DataFrame:
    try:
        df = pd.read_csv(yhatfile, delimiter="\s+")
        df.rename(columns=YHAT_FILE_COLUMNS_TO_DB_COLUMNS, inplace=True)
        agg_cols = [x for x in df.columns if x not in set(static)]
        df = df.join(df[agg_cols].agg(dict, axis=1).to_frame("additional_info")).drop(agg_cols, 1)
        df = df.astype(str)
        return df
    except Exception as exc:
        raise FileParseException(exc)
