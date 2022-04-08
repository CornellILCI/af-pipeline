from af.pipeline import calculation_engine


def test_get_h2_cullis():
    assert calculation_engine.get_h2_cullis(2, 2) is not None


def test_get_h2_cullis_return_correct_output():

    expected_output = 0.5

    variance = 2
    average_standard_error = 2

    assert calculation_engine.get_h2_cullis(variance, average_standard_error) == expected_output
