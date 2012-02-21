"""
fserie
======

Fourier series utilities. If a signal is periodic, one way to represent it is to calculate
the Fourier series coefficients. Since we are dealing with discrete time signals, usually 
this involves performing the DFT - Discrete Fourier Transform using the FFT algorithm
(Fast Fourier Transform). Now this usually is a mess for beginners since the algorithm usually
returns complex coefficients which are usually not desired.
"""

import numpy as np
from numpy.fft import rfft, irfft, fft, ifft

def fseries(x, Fs=1.):
    """
    Calculates the Fourier series coefficients in real form.

    *x*
      Samples.
    *Fs*
      Sampling frequency.
    **Returns**
      The cos coefficients, the sine coefficients and corresponding frequencies.
      
    """
    N = len(x)
    X = rfft(x) / N

    a = 2.0 * X.real
    b = -2.0 * X.imag
    n = len(a)
    period = N / Fs
    df = 1.0 / period
    freqs = np.arange(n) * df

    return a, b, freqs

    
def integral(x, p=1, Fs=1.):
    """
    Calculates the integral of a signal using Fourier transform.

    *x*
      Data to be integrated.
    *p*
      How many times the signal should be integrated. Negative values denote derivatives.
    *Fs*
      Sampling frequency of the data.
    
    """
    
    N = len(x)
    X = fft(x)

    period = N/float(Fs)
    n = len(x)
    nd2 = N / 2 + 1
    rest = N-nd2
    
    coefs1 = (np.arange(1, nd2, dtype=float) * (2*np.pi*1j / period)) ** (-p)
    coefs = np.hstack([0., coefs1, coefs1[:rest].conj()[::-1]])


    return ifft(X*coefs).real


