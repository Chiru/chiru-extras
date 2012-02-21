"""
filter
======

This module implements low-pass and high-pass filters in the frequency domain.
Most signal processing courses emphasize real-time filters but sometimes, in data
analysis, the data is already entirely present (a posteriori analysis) and other 
methods are possible and (accurate). There is no need to study the frequency response
of the filter or phase shifting. 

"""

import numpy as np
from numpy.fft import rfft, irfft, fft, ifft

def lpfilter(x, freq, Fs=1.):
    """
    Low-pass filter.

    *x*
      Data to be filtered.
    *freq*
      Frequency above which all spectral components are filtered.
    *Fs*
      Sampling frequency.
    **Returns**
      Array containing the filtered signal.
      
    """
    N = len(x)
    X = fft(x)
    df = float(Fs)/N
    nf = int(freq//df) 
    X[(nf+1):(N-nf)] = 0.0
    return ifft(X).real


def hpfilter(x, freq, Fs=1.):
    """
    High-pass filter.

    *x*
      Data to be filtered.
    *freq*
      Frequency below which all spectral components are filtered.
    *Fs*
      Sampling frequency.
    **Returns**
      Array containing the filtered signal.
      
    """
    N = len(x)
    X = fft(x)
    df = float(Fs)/N
    nf = int(freq//df) 
    X[0:(nf+1)] = 0.0
    X[(N-nf):N] = 0.0

    return ifft(X).real

    
