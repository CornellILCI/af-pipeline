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
    f67row = 'Residual [section 11, column 14 (of 15), row 22 (of 28)] is  3.70 SD\nResidual [section 11, column 15 (of 15), row 2 (of 28)] is  3.61 SD '
    t.write(bytes(f67row, 'UTF-8'))
    t.seek(0)
    testDf = pd.DataFrame({'Record': ['section 11, column 14 (of 15), row 22 (of 28)', 'section 11, column 15 (of 15), row 2 (of 28)'],
                               'SD': ['3.70', '3.61'] })
    handler = parser.parse_res(parser.check_file(t.name))
    assert_frame_equal(handler,testDf)


    t2 = NamedTemporaryFile()
    f69row = "STND RES\t30\t12.362\t3.81"
    t2.write(bytes(f69row,"UTF-8"))
    t2.seek(0)
    testDf2 = pd.DataFrame({'Record': ['30'],
                               'SD': ['3.81']})
    handler2 = parser.parse_res(parser.check_file(t2.name))
    assert_frame_equal(handler2,testDf2)






















    # t2 = NamedTemporaryFile()
    # f69 = 'STND RES\t30\t12.362\t3.81\nSTND RES\t30\t12.362\t2.38'
    # t2.write(bytes(f67, 'UTF-8'))
    # t2.seek(0)
    # testDf2 = pd.DataFrame({'Record': ['30', '30'],
    #                            'SD': [' 3.81', ' 2.38']})
    #
    #
    # handler2 = parser.parse_res(parser.check_file(t2.name))
    # assert_frame_equal(handler2,testDf2)

    # [parse_res(check_file(r)) for r in li]
