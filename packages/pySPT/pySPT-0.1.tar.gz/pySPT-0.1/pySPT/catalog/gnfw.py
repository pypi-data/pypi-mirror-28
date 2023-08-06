#!/usr/bin/env python2
# -*- coding: utf-8 -*-
""" Full name: Generalized Navarro-Frenk-White
------------------------------------------------------------
                          gNFW                            
------------------------------------------------------------
Description
-----------
To obtain a general cuspy model that is more amenable to lensing,
[1] introduce a model with a profile of the form

rho(r) = rho_s / [(r/r_s)**gamma * (1 + (r/r_s)***2)**((n-gamma)/2)], 

where r_s is a scale length, and gamma and n are the logarithmic slopes 
at small and large radii, respectively. The gNFW model corresponds to a 
cuspy halo model with n=3. 

More details can be found in [2]. Furthermore, an analytical expression 
for the deflection potential is given in [3].

Model parameters
----------------
rs = r_s, a scale length
ks = rho_s * rs / Sigma_cr, where Sigma_cr is the critical surface density 
     for lensing.
ga = logarithmic slope at small radius.

Notes
-----
No additional comments.

References
----------
[1] Munoz, J. A., Kochanek, C. S., & Keeton, C. R. 2001, ApJ, 558, 657
[2] Keeton, C. R., 2009, *A Catalog of Mass Models for Gravitational Lensing*
URL=https://arxiv.org/abs/astro-ph/0102341
[3] Wertz, O., Orthen, B., 2017, *pySPT: a package dedicated to the source 
position transformation*

"""

from numpy import pi, inf, isnan, isinf, log, array, zeros
from scipy.special import hyp2f1, gamma, beta, polygamma
from sympy import N as numerical
from sympy import polylog

from ..tools.vector import norm_fast

__author__ = 'O. Wertz @ Bonn'
__all__ = ['alpha_gnfw_polar',
           'deflection_angle',
           'deflection_potential',
           'derivative1_da',
           'dilog',
           'g_function',
           'kappa_gnfw_polar',
           'psi_gnfw_polar',
           'series_main',
           'series_sum',
           'surface_mass_density'
           ]

def dilog(z, prec=16):
    """ Give the so-called dilog function with a given precision.
    
    Parameters
    ----------
    z : double
        Argument at which the dilog is evaluated.
    prec : int
        The desired precision. For example, prec=16 measns a precision 
        of 10**(-16).
        
    Note
    ----
    There is an issue in sympy with the polylog function.
    sympy.polylog(2,-1) returns pi**2/12 instead of -pi**2/12. 
    This issue has been opened here: 
        https://github.com/sympy/sympy/issues/11593
        
    """
    if z == -1:
        return -pi**2/12.
    else:
        return float(numerical(polylog(2,z), prec))
    
def g_function(b, c, z, Nmin=1, Nmax=10, prec=16, full_output=False):
    """ Evaluate the so-called G(b,c;z) function as defined by Eq.(70) in [2].
    
    Parameters
    ----------
    b, c, z : double
        Arguments of the function. We note that abs(z) must be < 1.
    Nmin, Nmax : int
        Number min and max of iterations for the series.
    prec : int
        The desired precision. For example, prec=16 means a precision 
        of 10**(-16). Nmax overrides prec.        
    
    Notes
    -----
    The case Im(z) != 0 is not implemented because not physical.
    
    """
    assert abs(z) < 1, 'abs(z) must be < 1 ({} given)'.format(z)
    assert isinstance(Nmin, int), 'Nmin must be an integer ({} given)'.format(type(Nmin))
    assert isinstance(Nmax, int), 'Nmax must be an integer ({} given)'.format(type(Nmax))
    assert Nmax >= Nmin, 'Nmax must be >= Nmin.'
    
    Niter = 1
    step = inf
    
    result = 0.0
    
    while any([Niter < Nmin, step > 10**(-prec) and Niter < Nmax]):
        iteration = (gamma(b+Niter)/gamma(b))/(gamma(c+Niter)/gamma(c)) * (z**Niter)/Niter
        if isnan(iteration) or isinf(iteration): break
        if abs(iteration) < abs(step): step = iteration
        result += iteration
        Niter += 1
    
    if full_output:
        return result, Niter, iteration
    else:
        return result    
    
def series_main(r, p, k=0, m=0.0):
    """ Main term of the serie which defines the deflection potential.
    
    Parameters
    ----------
    r : double
        Radial position in the lens plane where the deflection potential is 
        evaluated.
    p : array_like
        Parameters of the lens model.
    k : int
        k-th term of the serie.
    m : double
        Parameter used in the gamma function evaluation.
        
    """
    assert isinstance(k, int), 'k must be an integer ({} given)'.format(type(k))
    
    rs, ks, ga = p
    
    K1 = gamma(k + 0.5*ga + m) / gamma(k + 0.5*(ga-1.) + m)
    K2 = (r/rs)**(2*(k+m)) / (k+m)**2

    return K1 * K2 * hyp2f1(k+m, k+m, 1+k+m, -(r/rs)**2)
    
def series_sum(r, p, m=0.0, k0=0, Nmin=1, Nmax=10, prec=16, full_output=False):
    """ Compute the serie K(k0,l;m;z) as defined by Eq.(A.3) in [3].
    
    Parameters
    ----------
    r : double
        Radial position in the lens plane where the deflection potential is 
        evaluated.
    p : array_like
        Parameters of the lens model.
    m : double
        Parameter used in the gamma function evaluation.
    k0 : int
        Define the index of the first term of the serie, typically 0 or 1.
        
    """
    assert isinstance(Nmax, int), 'Nmax must be an integer ({} given)'.format(type(Nmax))
    assert isinstance(Nmin, int), 'Nmin must be an integer ({} given)'.format(type(Nmin))
    assert isinstance(k0, int), 'k0 must be an integer ({} given)'.format(type(k0))
    assert Nmax >= Nmin, 'Nmax must be >= Nmin.'
    
    Niter = 0
    step = inf
    
    result = 0.0
    
    while any([Niter < Nmin, step > 10**(-prec) and Niter < Nmax]):
        iteration = series_main(r, p, k=k0+Niter, m=m)
        if isnan(iteration) or isinf(iteration): break
        if abs(iteration) < abs(step): step = iteration
        result += iteration
        Niter += 1
    
    if full_output:
        return result, Niter, iteration
    else:
        return result

def psi_gnfw_polar(r, p, debug=False, **kwargs):
    """ Deflection potential associated with an gNFW, in polar coordinates.
    
    Parameters
    ----------
    r : double
        Radial position in the lens plane where the deflection potential is 
        evaluated.
    p : array_like
        Parameters of the lens model.
    debug : bool
        Print useful informations.
         
    Note
    ----
    The analytical expression of the deflection potential can be found 
    at Eq.(A.2) in [3].
    
    """    
    rs, ks, ga = p
    
    t1 = - rs * ks * dilog(-r**2/rs**2, **kwargs.get('dilog_kwargs',{}))
    
    series1, Niter1, iter1 = series_sum(r, p, m=0.0, k0=1, Nmin=1, 
                         Nmax=kwargs.get('series_kwargs',{}).get('Nmax',200), 
                         prec=kwargs.get('series_kwargs',{}).get('prec',16),
                         full_output=True)
    t2 = rs * ks * gamma(0.5*(ga-1.))/gamma(0.5*ga) * series1
    
    series2, Niter2, iter2 = series_sum(r, p, m=0.5*(3.-ga), k0=0, Nmin=1, 
                         Nmax=kwargs.get('series_kwargs',{}).get('Nmax',200), 
                         prec=kwargs.get('series_kwargs',{}).get('prec',16),
                         full_output=True)
    t3 = (3-ga)/pi**(0.5) * ks * rs * beta(0.5*(ga-3), 1.5) * series2
    
    if debug:
        print '(t1, t2, t3) = ({:.8f}, {:.8f}, {:.8f})'.format(t1,t2,t3)
        print 'N_iter_1: {}'.format(Niter1)
        print 'iter_1: {}'.format(iter1)
        print 'N_iter_2: {}'.format(Niter2)
        print 'iter_2: {}'.format(iter2)        

    return t1 - t2 - t3
    
def deflection_potential((theta1, theta2), p, **kwargs):
    """ Deflection angle associated with an gNFW.
    
    Parameters
    ----------
    theta1, theta2 : double
        Position in the lens plane where the deflection potential is evaluated.
    p : array_like
        Parameters of the lens model.
        
    """
    r = norm_fast([theta1, theta2])
    return psi_gnfw_polar(r, p, **kwargs)
    
def alpha_gnfw_polar(r, p, zero=1.49e-12):
    """
    Note
    ----
    See Eqs.(66) and (67) in 'A Catalog of Mass Models for Gravitational 
    Lensing' by Keeton (2002). Note that:
        (1) There is a typo in Eq.(66): the G function term should be 
            multiplied by (1/x), like the log-term.
        (2) To match the result returned by `GravLens` (Keeton, 2001), one 
            should divide Eqs.(66) and (67) by r_s.
    """
    assert r >= 0.0, 'r must be positive ({} given)'.format(r)    
    if r < zero: return 0.0 
    
    rs, ks, ga = p
    
    x = r/rs
    xsq = (r/rs)**2
    
    if x <= 1.:
        K1 = 2. * ks        
        t1 = log(1.+xsq)
        t2 = g_function(0.5*ga, 0.5*(ga-1.), xsq/(1.+xsq), Nmax=200, prec=16)
        t3 = (xsq/(1.+xsq))**(0.5*(3.-ga)) * beta(0.5*(ga-3),1.5) * hyp2f1(1.5, 0.5*(3.-ga), 0.5*(5.-ga), xsq/(1.+xsq))
        
        return K1 / x * (t1 - t2 - t3)
    elif x > 1:
        K1 = 2. * ks
        t1 = log(1.+xsq)
        t2 = g_function(0.5*ga, 1.5, 1./(1.+xsq), Nmax=200, prec=16)
        t3 = polygamma(0, 1.5) - polygamma(0, 0.5*(3.-ga))
        
        return K1 / x * (t1 - t2 + t3)
    
def deflection_angle((theta1, theta2), p, zero=1.49e-12):
    """ Deflection angle associated with an gNFW.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection angle is evaluated.
    p : array_like
        Parameters of the lens model.
    zero : double
        Limit under which r is considered to be equal to 0.   
        
    Notes
    -----
    See Eqs.(66) and (67) in [2]. Note that:
        a) There is a typo in Eq.(66): the G function term should be 
           multiplied by (1/x), like the log-term.
        b) To match the result returned by `GravLens` (Keeton, 2001), one 
           should divide Eqs.(66) and (67) by r_s.
           
    """
    r = norm_fast([theta1, theta2])
    
    if r < zero: return array([0.0, 0.0])
    
    alpha = alpha_gnfw_polar(r, p)
    return alpha/r * array([theta1, theta2])
    
def kappa_gnfw_polar(r, p, zero=1.49e-12):
    """ Surface mass density associated with an gNFW, in polar coordinates.
    
    Parameters
    ----------
    r : double
        Radial position in the lens plane where the surface mass density is 
        evaluated.
    p : array_like
        Parameters of the lens model.
    zero : double
        Limit under which r is considered to be equal to 0.    

    """
    if r < zero: return 0.0
    
    rs, ks, ga = p
    
    xsq = (r/rs)**2

    return 2.0 * (ks/rs) / (1.+xsq) * hyp2f1(1., 0.5*ga, 1.5, 1./(1.+xsq)) 
    
def surface_mass_density((theta1, theta2), p):
    """ Surface mass density associated with an gNFW.
    
    Parameters
    ----------
    theta1, theta2 : double
        Position in the lens plane where the surface mass density is 
        evaluated. 
    p : array_like
        Parameters of the lens model.
        
    """
    r = norm_fast([theta1, theta2])
    
    return kappa_gnfw_polar(r, p)   

# n-th derivative of psi
def derivative1_da((theta1,theta2), p, zero=1.49e-12):
    """ Jacobi matrix of the deflection mapping associated with an gNFW.
    
    Parameters
    ----------
    theta1, theta2 : double
        Position in the lens plane where the Jacobi matrix is evaluated.   
    p : array_like
        Parameters of the lens model.
        
    """
    rs, ks, ga = p    
    r = norm_fast([theta1, theta2])
    
    if r < zero: return zeros([2,2])
    
    alpha = alpha_gnfw_polar(r,p) #alpha_gNFW((theta1, theta2), p)
    
    K1 = 4. * rs * ks / (r**2 * (rs**2 + r**2))
    H2F1 = hyp2f1(1., 0.5*ga, 1.5, 1./(1.+(r/rs)**2))
    
    # use alpha_gNFW_polar to simplify theta1 both at numerator and denominator
    # which avoids divergence when we evaluate D1_alpha_gNFW at the position
    # (0.0, y)
    alpha_xx = (theta2**2-theta1**2) / (r**2) * alpha/r \
                + theta1**2 * K1 * H2F1
    
    # use alpha_gNFW_polar to simplify theta2 both at numerator and denominator
    # which avoids divergence when we evaluate D1_alpha_gNFW at the position
    # (x, 0.0)                
    alpha_yy = (theta1**2-theta2**2) / (r**2) * alpha/r \
               + theta2**2 * K1 * H2F1

    alpha_xy = -2. * theta2 * theta1 * (alpha/r) / r**2 + theta1*theta2 * K1 * H2F1
    #--> alpha_yx = alpha_xy
    
    return array([[alpha_xx, alpha_xy],[alpha_xy, alpha_yy]])
