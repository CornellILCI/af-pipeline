

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

    h2_cullis = 1 - (average_standard_error / (2 * genetic_variance))

    if h2_cullis < 0:
        return 0

    return h2_cullis
