

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import ifft, fft

class Kernel(object):

    def __init__(self, coef, name='unknown'):
        self.coef = np.array(coef)
        self.m = len(self.coef) - 1
        self.name = name
    def apply_vector(self, x, circular=True):

        m = self.m
        coef = self.coef
        n = len(x)
        w = np.concatenate((coef, np.zeros(n-2*m-1), coef[1:][::-1]))
        y = ifft(fft(x)*fft(w)).real 
        if circular:
            return y
        else:
            return y[m:(n-m)]
    def apply_kernel(self, k):
        n = self.m
        xx = np.concatenate( (np.zeros(n), k.coef[1:][::-1], k.coef, np.zeros(n)) )
        coef = self.apply_vector(xx, circular=True)
        m = len(coef) // 2
        return Kernel(coef[m:])
    def list_coefs(self, coef=None):
        if coef is None:
            coef = self.coef
        return np.concatenate( (coef[1:][::-1], coef) )
    
    def plot(self, *args, **kw):
        x = np.arange(2*self.m + 1) - self.m
        coef = self.list_coefs()
        plt.plot(x, coef, 'o', *args, **kw)

    def __call__(self, x, circular=True, axis=0):
        if isinstance(x, Kernel):
            return self.apply_kernel(x)
        x = np.array(x)

        ndim = x.ndim
        if ndim==1:
            return self.apply_vector(x, circular)
        if ndim==2:
            s = x.shape
            out = np.empty_like(x)
            if axis==0:
                for i in xrange(s[1]):
                    out[:,i] = self.apply_vector(x[:,i], circular)
            else:
                for i in xrange(s[0]):
                    out[i,:] = self.apply_vector(x[i,:], circular)
            return out
        else:
            raise RuntimeError("Don't know to do this yet!")
        
                
        
def daniell(m):
    if m < 1: raise RuntimeError("'m' is less than 1")
    return Kernel(1./(2*m+1) * np.ones(m+1))
def modified_daniell(m):
    if m < 1: raise RuntimeError("'m' is less than 1")
    cc = np.ones(m+1) / (2.*m)
    cc[m] *= 0.5
    return Kernel(cc)

def fejer_kernel(m,r):
    if r < 1: raise RuntimeError("'r' is less than 1")
    if m < 1: raise RuntimeError("'m' is less than 1")
    n = 2*m + 1
    wn = np.zeros(m+1)
    wj = 2.0 * np.pi * np.arange(1,m+1)/n
    wn[1:] = np.sin(r*wj/2.)**2 / np.sin(wj/2.)**2 / r
    wn[0] = r
    wn = wn / (wn[0] + 2*wn[1:].sum())
    return Kernel(wn)

def dirichilet_kernel(m,r):
    if r < 1: raise RuntimeError("'r' is less than 1")
    if m < 1: raise RuntimeError("'m' is less than 1")
    n = 2*m + 1
    wn = np.zeros(m+1)
    wj = 2 * np.pi * np.arange(1,m+1)/n
    wn[1:] = np.sin( (r+0.5)*wj) / np.sin(wj/2.)
    wn[0] = 2*r + 1
    wn = wn / (wn[0] + 2.0*wn[1:].sum())
    return Kernel(wn)

def multiple_kernel(m, fun1=modified_daniell, *args):

    try:
        l = len(m)
        if l==1:
            m = m[0]
            l = None
    except:
        l = None

    if l is None:
        return fun1(m, *args)
    else:
        k = fun1(m[0], *args)
        for i in m[1:]:
            kern = fun1(i, *args)
            k = kern.apply_kernel(k)
    return k

    
def daniell_kernel(m):
    return multiple_kernel(m, daniell)
def modified_daniell_kernel(m):
    return multiple_kernel(m, modified_daniell)

    
def kernel(coef, m, *args):
    if isinstance(coef, str):
        fun_names = dict(daniell=daniell_kernel, modified_daniell=modified_daniell_kernel,
                         fejer=fejer_kernel, dirichilet=dirichilet_kernel)
        if coef not in fun_names: raise RuntimeError("%s is not an implemented kernel" % (coef))
        return fun_names[coef](m, *args)

    coef = np.array(coef)
    return Kernel(coef, *args)

    
"""
def daniell_kernel(m):
    try:
        l = len(m)
        if l == 1: m = m[0]
    except:
        l = None
        
    if l is None :
        return Kernel(1./(2*m+1) * np.ones(m+1))
    else:
        k = daniell_kernel(m[0])
        for i in m[1:]:
            kern = daniell_kernel(i)
            k = kern.apply_kernel(k)
    k.name = "Daniell"
    return k


def modified_daniell_kernel(m):
    try:
        l = len(m)
        if l == 1: m = m[0]
    except:
        l = None
    if l is None :
        cc = np.ones(m+1) / (2.*m)
        cc[m] *= 0.5
        
        return Kernel(cc)
    else:
        k = modified_daniell_kernel(m[0])
        for i in m[1:]:
            kern = modified_daniell_kernel(i)
            k = kern.apply_kernel(k)
    
"""
