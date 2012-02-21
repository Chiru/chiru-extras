"""
taper
=====

Implements additional window functions.
"""
import numpy as np


def cos_taper(x, p=0.1):
    """
    Implement a cossine taper. Implemented following
    the function spec.taper in R.

    **Arguments**
    """
    xx = np.asarray(x)
    n = len(x)
    m = np.floor(n*p)
    if m == 0: return xx

    w = 0.5 * (1. - np.cos(np.pi*np.arange(1, 2*m, 2)/(2.*m)))
    return np.concatenate( (w, np.ones(n-2*m), w[::-1]) )*x
