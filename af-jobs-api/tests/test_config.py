import os

import config


def test_get_allowable_origins():

    os.environ["AFAPI_ALLOWABLE_ORIGINS"] = "*"

    assert config.get_allowable_origins() == ["*"]

    os.environ["AFAPI_ALLOWABLE_ORIGINS"] = "http://localhost:5000;http://dev.ebsproject.org"

    assert config.get_allowable_origins() == ["http://localhost:5000", "http://dev.ebsproject.org"]
