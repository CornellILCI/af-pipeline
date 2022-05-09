from af.pipeline import rpy_utils
from af.pipeline import exceptions
from rpy2 import robjects

import pandas as pd

import pytest


def test_read_csv(temp_file):
    temp_file.write(b"test\n")
    temp_file.seek(0)
    assert rpy_utils.read_csv(temp_file.name) is not None


def test_read_csv_returns_r_dataframe(temp_file):

    temp_file.write(b"test\n")
    temp_file.seek(0)
    assert type(rpy_utils.read_csv(temp_file.name)) == robjects.vectors.DataFrame


def test_read_csv_raises_invalid_file_exception():

    with pytest.raises(exceptions.InvalidFilePath):
        rpy_utils.read_csv("")


def test_read_csv_output_is_correct(temp_file, r_base):

    data_ = b"h1,h2,h3\n4,d1,3.444\n2,d2,5.000\n6,6,0.0000001\n"
    temp_file.write(data_)
    temp_file.seek(0)

    expected_r_df = robjects.vectors.DataFrame(
        {
            "h1": robjects.IntVector((4, 2, 6)),
            "h2": robjects.StrVector(("d1", "d2", "6")),
            "h3": robjects.FloatVector((3.444, 5.000, 0.0000001)),
        }
    )

    output_r_df = rpy_utils.read_csv(temp_file.name)

    assert list(r_base.identical(expected_r_df, output_r_df))[0] == True
