# -*- coding: utf-8 -*-
import numpy as np
from scipy import interpolate 
from scipy import signal
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import interp1d

################## SPECIFIC FUNCTIONS FOR TREATMENT OF SPECTRA

def spectrarray(name,sh,sf,x,interpmethod):
    """The function needs the x general axis, an array containing the name of files, and a precision concenrning the interpolation method
    Spectra are interpolated to have linear and constant x values and be able to be in a same array
    Interpoation methods proposed are the np.interp function or an interpolation using the interpolate 
    function of scipy, based on spline functions
    """
    for i in range(len(name)):
        rawspectre = np.genfromtxt(name[i],skip_header=sh, skip_footer=sf)
        rawspectre = rawspectre[~np.isnan(rawspectre).any(1)] # on verifie qu on a pas de nan
        # on echantillonne le spectre pour avoir les memes x
        if interpmethod == 'np.interp':
            y = np.interp(x,rawspectre[:,0],rawspectre[:,1]) # resampling 
        elif interpmethod == 'scipy.interp':
            tck = interpolate.splrep(rawspectre[:,0],rawspectre[:,1],s=0)
            y = interpolate.splev(x,tck,der=0)
        else:
            print('Error, choose the good interp method name: np.interp or scipy.interp')
        
        # Now we construct the output matrix
        # 1st column is the x axis
        # then others are the spectra in the order provided in the list of names input array
        if i == 0:
            out = np.zeros((len(x),len(name)+1))
            out[:,0]=x
            out[:,i+1]=y
        else:
            out[:,i+1]=y
            
    return out 

def spectrataux(x,spectres):
    """
        spectrataux(x,spectres)
    
    This function calculates the increase/decrease rate of each frequency in a spectrum
    Your data must have the same frequency axis of course...
    Initial fitting function is a second order polynomial
    Change that following your needs
    """
    # we need an organized function before calling the curve_fit algorithm
    freq = spectres[:,0]
    # output array
    taux = np.zeros((len(freq),4));
    taux[:,0] = freq[:]
    
    # We look a each frequency, we sort y data and fit them with a second order polynomial
    for i in range(len(freq)):
        y = spectres[i,1::]
        popt, pcov = curve_fit(fun2,x,y,[0.5e-3,0.5e-4,1e-6])
        taux[i,1:len(x)]=popt
        
    return taux
    
#### OFFSETTING DATA FROM THE SPECTRARRAY FUNCTION

def spectraoffset(spectre,offsets):
    """
        spectraoffset(spectre,offsets)
    
    Allows to offset your spectra with values in offsets
    
    spectre : array constructed with the spectrarray function
    
    offsets : array constructed with numpy and containing the coefficient for the offset to apply to spectre 
    
    """
    
    # we already say what is the output array
    out = np.zeros(spectre.shape)
    # and we offset the spectra
    for i in range(len(offsets)):
        out[:,i+1] = spectre[:,i+1] + offsets[i]
    
    return out
    
#
# Simple data treatment functions
#
def flipsp(sp):
    """

    	flipsp(spectra::Array{Float64})

    Flip an array along the row dimension (dim = 1) if the first column values are in decreasing order.

    """
    if sp[-1,0] < sp[0,0]:
        sp = np.flip(sp,0)
        return sp
    else:
        return sp
    
	


def resample(x,y,x_new):
    """

    	resample(x,y,x_new)

    Resample a y signal associated with x, along the x_new values.

    Uses scipy.interpolate.interp1d

    """
    f = interp1d(x,y)
    return f(x_new)