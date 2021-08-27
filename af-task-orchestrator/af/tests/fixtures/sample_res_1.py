import pytest
import io
from tempfile import NamedTemporaryFile


@pytest.fixture
def sample_res_data_1():
    tmp = NamedTemporaryFile()
    data = """Residual [section 11, column 14 (of 15), row 22 (of 28)] is  3.70 SD\nResidual [section 11, column 15 (of 15), row 2 (of 28)] is  3.61 SD
"""
    tmp.write(bytes(data, 'UTF-8'))
    tmp.seek(0)

    return tmp.name