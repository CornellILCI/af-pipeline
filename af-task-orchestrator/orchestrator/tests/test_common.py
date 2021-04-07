import orchestrator.urlutil as urlutil
import orchestrator.pandasutil as pandasutil
import pandas as pd
from pandas._testing import assert_frame_equal


def test_valid_str():

    assert urlutil.valid_url(None) is False

    assert urlutil.valid_url("test") is False

    assert urlutil.valid_url("  ") is False

    assert urlutil.valid_url("http://url") is True

    assert urlutil.valid_url("hTtps://url/d/d/d") is True

    assert urlutil.valid_url("sftp://test.test") is False


def test_url_join():

    base_url = "http://test.com"
    relative_url = "/v1/endpoint"

    base_url_multiple_right_slashes = "http://test.com///"
    relative_url_multiple_left_slashes = "///v1/endpoint"

    expected_result = "http://test.com/v1/endpoint"

    assert urlutil.url_join(base_url, relative_url) == expected_result

    assert urlutil.url_join(base_url_multiple_right_slashes, relative_url_multiple_left_slashes) == expected_result


def test_df_keep_columns():

    _df = pd.DataFrame([{"a": 4, "b": 5, "c": 6}])

    columns_to_keep = {"a", "b", "d"}

    expected_df = pd.DataFrame([{"a": 4, "b": 5}])

    result_df = pandasutil.df_keep_columns(_df, columns_to_keep)

    # assert dataframe is returned
    assert isinstance(result_df, pd.DataFrame)

    result_df = result_df[expected_df.columns]

    assert_frame_equal(result_df, expected_df)
