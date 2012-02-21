"""
periodogram
===========

This module implements functions that calculate the periodogram of a time series.
The periodogram is an estimate of the power density spectrum of a function.
"""

import numpy as np
from numpy.fft import rfft, irfft
import scipy.signal as signal


def ftransf(x, Fs=1.):
    """
    Fourier transform of a function.

    *x*
      Data to be transformed.
    *Fs*
      Sampling frequency.
    **returns**
      Fourier transform of x
    """
    N = len(x)
    
    X = 1. / (Fs * 2.0 * np.pi) * rfft(x)

    df = float(N) / Fs

    return X, (arange(len(X))*df)


