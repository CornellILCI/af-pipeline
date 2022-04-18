from af.pipeline.exceptions import InvalidAverageStandardError, InvalidVariance

import pandas as pd


def get_h2_cullis(genetic_variance: float, average_standard_error: float) -> float:
    """Return Heritability using Cullis method.

    Args:
        genetic_variance: Genetic variance.
        average_standard_error: Average standard error of the genetic BLUPs

    Returns:
        Heritability using cullis method

    """

    if genetic_variance == 0:
        return 0

    if genetic_variance < 0:
        raise InvalidVariance

    if average_standard_error < 0:
        raise InvalidAverageStandardError

    h2_cullis = 1 - (average_standard_error / (2 * genetic_variance))

    # check for upper and lower bounds
    if h2_cullis < 0:
        return 0

    return h2_cullis


def get_average_std_error(predictions_df: pd.DataFrame) -> float:
    """Returns average standard error for predictions.

    Args:
        predictions_df: Dataframe with predictions.

        example,
            job_id, entry, loc,  value, std_error, e_code, num_factors
            1,      1,     None, 1,     1.4,       E,       1
            1,      2,     None, 1,     1.5,       E,       1
            1,      None,  1,    1,     1.4,       E,       1
            1,      1,     1,    1,     1.5,       E,       2
            1,      2,     1,    1,     1.5,       E,       2


    Returns:
        average standard error.
    """

    if predictions_df.empty:
        return 0

    predictions_df["std_error"] = predictions_df["std_error"].apply(pd.to_numeric)
    return predictions_df["std_error"].mean()
