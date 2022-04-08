

def get_h2_cullis(genetic_variance: float, average_standard_error: float):
    """ Return Heritability using Cullis method of calculation.
    
    Args:
        genetic_variance: Genetic variance.
        average_standard_error: Average standard error of the genetic BLUPs

    Returns:
        Heritability using cullis method

    """

    h2_cullis = 1 - (average_standard_error / (2 * genetic_variance))
    return h2_cullis
