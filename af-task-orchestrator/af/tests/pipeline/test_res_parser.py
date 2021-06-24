from tempfile import NamedTemporaryFile
import af.pipeline.asreml.resparser as parser
import pandas as pd
from pandas._testing import assert_frame_equal
import os


def test_res_parser():
    """
    write a mock df string to a temp file
    """
    t = NamedTemporaryFile()
    s67 = '\t\t\t\t\t  Record     SD\n0  section 11, column 14 (of 15), row 22 (of 28)   3.70'
    t.write(bytes(s67, 'UTF-8'))
    t.seek(0)

    testDf = pd.DataFrame(columns=['Record','SD'])

    testDf.loc[0] = pd.Series({'Record': 'section 11, column 14 (of 15), row 22 (of 28)',
                              'SD': '3.70' })

    handler = parser.parse_res(parser.check_file(t.name))
    assert_frame_equal(handler,testDf)

    # [parse_res(check_file(r)) for r in li]
