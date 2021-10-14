import json
import io
from af.pipeline.sommer.services import get_prediction
from af.pipeline.db.models import Prediction

import os
from tempfile import NamedTemporaryFile

from af.pipeline.sommer.services import parser
import pandas as pd
from pandas._testing import assert_frame_equal


def test_sommer_services():
    """
    """
    t = NamedTemporaryFile()
    string = ""
    t.write(bytes(string, "UTF-8"))
    t.seek(0)
    print("hi")

    # eg testDf = pd.DataFrame(columns=["record", "yhat", "residual", "hat", "additional_info"])

    # testDf.loc[0] = pd.Series(
    #     {
    #         "record": "1",
    #         "yhat": "6.7272",
    #         "residual": "-0.5713",
    #         "hat": "0.04985",
    #         "additional_info": json.dumps({"RinvRes": 0.009825, "AOMstat": 0.02041}),
    #     }
    # )


    # handler = parser.parse(t.name)
    # assert_frame_equal(handler.head(2), testDf)

