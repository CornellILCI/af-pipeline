import pytest
import io


@pytest.fixture
def sample_res_data_1():
    data = """Residual [section 11, column 14 (of 15), row 22 (of 28)] is  3.70 SD\nResidual [section 11, column 15 (of 15), row 2 (of 28)] is  3.61 SD
"""
    return io.StringIO(data)