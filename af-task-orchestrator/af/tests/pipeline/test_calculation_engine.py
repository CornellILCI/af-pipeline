import pytest
from af.pipeline import calculation_engine
from af.pipeline.exceptions import InvalidAverageStandardError, InvalidVariance


def test_get_h2_cullis():
    assert calculation_engine.get_h2_cullis(2, 2) is not None


def test_get_h2_cullis_return_correct_output():

    expected_output = 0.5

    variance = 2
    average_standard_error = 2

    assert calculation_engine.get_h2_cullis(variance, average_standard_error) == expected_output


def test_zero_genetic_variance_returns_zero():

    genetic_variance = 0
    average_standard_error = 10
    assert calculation_engine.get_h2_cullis(genetic_variance, average_standard_error) == 0


def test_negetive_h2_return_zero():

    genetic_variance = 2
    average_standard_error = 10
    assert calculation_engine.get_h2_cullis(genetic_variance, average_standard_error) == 0


def test_h2_invalid_input_variance():

    genetic_variance = -2
    average_standard_error = 10

    with pytest.raises(InvalidVariance):
        calculation_engine.get_h2_cullis(genetic_variance, average_standard_error)


def test_h2_invalid_average_standard_error():

    average_standard_error = -10
    genetic_variance = 2

    with pytest.raises(InvalidAverageStandardError):
        calculation_engine.get_h2_cullis(genetic_variance, average_standard_error)


def test_get_average_standard_error_is_not_none(predictions_df):

    assert calculation_engine.get_average_std_error(predictions_df) is not None


def test_get_average_standard_error(predictions_df):

    # from predictions_df fixture
    expected_average_std_error = 1.46

    assert calculation_engine.get_average_std_error(predictions_df) == expected_average_std_error
