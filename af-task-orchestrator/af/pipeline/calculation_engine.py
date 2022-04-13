from af.pipeline.exceptions import InvalidVariance, InvalidAverageStandardError

def get_h2_cullis(genetic_variance: float, average_standard_error: float):
    """ Return Heritability using Cullis method.
    
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
