import common


def test_valid_str():

    assert common.valid_url(None) is False

    assert common.valid_url("test") is False

    assert common.valid_url("  ") is False

    assert common.valid_url("http://url") is True

    assert common.valid_url("hTtps://url/d/d/d") is True

    assert common.valid_url("sftp://test.test") is False


def test_url_join():

    base_url = "http://test.com"
    relative_url = "/v1/endpoint"

    base_url_multiple_right_slashes = "http://test.com///"
    relative_url_multiple_left_slashes = "///v1/endpoint"

    expected_result = "http://test.com/v1/endpoint"

    assert common.url_join(base_url, relative_url) == expected_result

    assert (
        common.url_join(base_url_multiple_right_slashes,
                        relative_url_multiple_left_slashes) == expected_result)
