from tempfile import NamedTemporaryFile
import af.pipeline.asreml.slnparser as parser
import pandas as pd
from pandas._testing import assert_frame_equal
import os


def test_sln_parser():
    """
    write a df string to a temp file
    pass temp file to the handler for transform
    compare transform to the manually constructed valid df constructed below
    """
    t = NamedTemporaryFile()
    string = 'Model_Term\tLevel\tEffect\tseEffect\nrep\t1\t0.0\t0.0'
    t.write(bytes(string, 'UTF-8'))
    t.seek(0)

    testDf = pd.DataFrame(columns=['model_term','level','effect','se_effect', 'additional_info'])
    testDf.loc[0] = pd.Series({'model_term': 'rep',
                              'level': '1',
                              'effect': '0.0',
                              'se_effect': '0.0',
                              'additional_info': 'nan'})
    handler = parser.parse_sln_file(t.name)
    assert_frame_equal(handler,testDf)

    t2 = NamedTemporaryFile()
    string2  = 'Model_Term\tLevel\tEffect\tseEffect\tGiEffect\tAOMstat\nmv_estimates\t2\t6.53511\t1.54492\t0.627188\t0.685164'
    t2.write(bytes(string2, 'UTF-8'))
    t2.seek(0)
    testDf2 = pd.DataFrame(columns=['model_term','level','effect','se_effect','additional_info'])
    testDf2.loc[0] = pd.Series({'model_term': 'mv_estimates',
                              'level': '2',
                              'effect': '6.53511',
                              'se_effect': '1.54492',
                              'additional_info': str({'GiEffect': 0.627188, 'AOMstat': 0.685164 })})
    handler2 = parser.parse_sln_file(t2.name)
    assert_frame_equal(handler2,testDf2)




    # create a 2 row dataframe
