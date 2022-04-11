from af.pipeline import calculation_engine
import pytest

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

