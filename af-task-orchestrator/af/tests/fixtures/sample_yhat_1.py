import io

import pytest


@pytest.fixture
def sample_yhat_data_1():
    data = """Record\tYhat\tResidual\tHat\tRinvRes\tAOMstat
1\t6.7272\t-0.57130\t0.04985\t0.009825\t0.02041
2\t6.5568\t0.19460\t0.09771\t-0.014930\t-0.03078

"""
    return io.StringIO(data)