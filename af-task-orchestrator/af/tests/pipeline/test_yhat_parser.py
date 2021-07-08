from tempfile import NamedTemporaryFile
import af.pipeline.yhat.yhatparser as parser
import pandas as pd
from pandas._testing import assert_frame_equal
import os

path = "/home/vince/dev/work/ebsaf/af-core/af-task-orchestrator/af/pipeline/yhat/tmp"



def test_simple_test_2():
    """
    write a df string to a temp file
    pass temp file to the handler for transform
    compare transform to the manually constructed valid df constructed below
    """
    t = NamedTemporaryFile()
    string = 'Record\tYhat\tResidual\tHat\tRinvRes\tAOMstat\n1\t6.7272\t-0.57130\t0.04985\t0.009825\t0.02041\n2\t6.5568\t0.19460\t0.09771\t-0.014930\t-0.03078\n'
    t.write(bytes(string, 'UTF-8'))
    t.seek(0)

    testDf = pd.DataFrame(columns=['record','yhat','residual','hat','additional_info'])
    testDf.loc[0] = pd.Series({'record': '1',
                              'yhat': '6.7272',
                              'residual': '-0.5713',
                              'hat': '0.04985',
                              'additional_info':str({'RinvRes': 0.009825, 'AOMstat': 0.02041}) })
    testDf.loc[1] = pd.Series({'record': '2' ,
                              'yhat': '6.5568',
                              'residual': '0.1946',
                              'hat':'0.09771' ,
                              'additional_info':str({'RinvRes': -0.01493, 'AOMstat': -0.03078})})

                            


    handler = parser.YHatParser()
    handler.read_yht(t.name)
    handler.rename_columns()
    handler.create_correct_df()

    assert_frame_equal(handler.df,testDf)


    # create a 2 row dataframe
