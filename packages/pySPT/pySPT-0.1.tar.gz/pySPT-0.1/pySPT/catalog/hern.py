#!/usr/bin/env python2
# -*- coding: utf-8 -*-
""" Full name: HERNquist
------------------------------------------------------------
                          HERNQUIST                            
------------------------------------------------------------
Description
-----------
The Hernquist [1] model is a 3-d density distribution with a projected
distribution that mimics the luminosity distribution of early-type galaxies. 
It has the form

rho(r) = rho_s / [(r/r_s)(1 + r/r_s)**3],

where r_s is a scale length and rho_s is a characteristic density. More 
details can be found in [2].

Model parameters
----------------
rs = r_s, a scale length
ks = rho_s * rs / Sigma_cr, where Sigma_cr is the critical surface density 
     for lensing.

Notes
-----
No additional comments.

References
----------
[1] Hernquist, L. 1990, ApJ, 356, 359
[2] Keeton, C. R., 2009, *A Catalog of Mass Models for Gravitational Lensing*
URL=https://arxiv.org/abs/astro-ph/0102341

"""

from numpy import arctan, arctanh, log
from numpy import array, zeros

from ..tools.vector import norm_fast

__author__ = 'O. Wertz @ Bonn'
__all__ = ['alpha_hern_polar',
           'deflection_angle',
           'deflection_potential',
           'derivative1_da',
           'F',
           'Fr',
           'kappa_hern_polar',
           'psi_hern_polar',
           'surface_mass_density'           
           ]

# We first define usefull functions.
def F(a):
    """ Piece-wise function as defined by Eq.(48) in [2].
    
    Parameters
    ----------
    a : double
        Argument of the function. 
        
    """
    if a == 1.:
        return 1.
    elif abs(a) < 1.49e-07:
        return 0.0
    elif a > 1:
        return arctan((a**2-1)**(0.5)) / (a**2-1)**(0.5)
    elif a < 1:
        return arctanh((1-a**2)**(0.5)) / (1-a**2)**(0.5)
    else:
        return 0.0
        
def Fr(a):
    """ First derivative of the piece-wise function F(a), see Eq.(49) in [2]. 
    
    Parameters
    ----------
    a : double
        Argument of the function. 
        
    """
    if a == 1.:
        return -2./3.
    else:
        return (1 - a**2 * F(a)) / (a * (a**2 - 1))        

def psi_hern_polar(r, p, zero=1.49e-12):
    """ Deflection potential associated with an HERN, in polar coordinates.
    
    Parameters
    ----------
    r : double
        Radial position in the lens plane where the deflection potential is 
        evaluated.
    p : array_like
        Parameters of the lens model.
    zero : double
        Limit under which r is considered to be equal to 0.

    """
    assert r >= 0.0, 'r must be positive ({} given)'.format(r)
    if r < zero: return 0.0  
    
    rs, ks = p
    x = r/rs 
    return 2.*rs**2*ks * (F(x) + log(x/2.))

def deflection_potential((theta1, theta2), p):
    """ Deflection potential associated with an HERN.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection potential is 
        evaluated.
    p : array_like
        Parameters of the lens model.
        
    """
    r = norm_fast([theta1, theta2])
    return psi_hern_polar(r, p)    
    
def alpha_hern_polar(r, p, zero=1.49e-12):
    """ Deflection angle associated with an HERN, in polar coordinates.
    
    Parameters
    ----------
    r : double
        Radial position in the lens plane where the deflection angle is 
        evaluated.
    p : array_like
        Parameters of the lens model.
    zero : double
        Limit under which r is considered to be equal to 0.   

    """
    assert r >= 0.0, 'r must be positive ({} given)'.format(r)
    if r < zero: return 0.0    
    
    rs, ks = p
    x = r/rs    
    
    if x == 1:
        return 2.*rs*ks/3.
    else:
        return 2.*rs*ks * (x * (1-F(x)))/(x**2 - 1)
    
def deflection_angle((theta1, theta2), p, zero=1.49e-12):
    """ Deflection angle associated with an HERN.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection angle is evaluated.
    p : array_like
        Parameters of the lens model.
        
    """
    r = norm_fast([theta1, theta2])
    
    if r < zero: return array([0.0, 0.0])
    
    alpha = alpha_hern_polar(r, p)    
    return alpha/r * array([theta1, theta2])       
        
def kappa_hern_polar(r, p, zero=1.49e-12):
    """ Surface mass density associated with an HERN, in polar coordinates.
    
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
    assert r >= 0.0, 'r must be positive ({} given)'.format(r)    
    if r < zero: return 0.0
    
    rs, ks = p
    
    x = r/rs    
        
    if x == 1:
        return 4.*ks/15.
    else:
        return ks/(x**2-1)**2 * (-3 + (2+x**2)*F(x))        

def surface_mass_density((theta1, theta2), p):
    """ Surface mass density associated with an HERN.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the surface mass density is 
        evaluated. 
    p : array_like
        Parameters of the lens model.
        
    """
    r = norm_fast([theta1, theta2])
    return kappa_hern_polar(r, p)  

# n-th derivative of psi
def derivative1_da((theta1, theta2), p, zero=1.49e-12):
    """ Jacobi matrix of the deflection mapping associated with an HERN.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the Jacobi matrix is evaluated.   
    p : array_like
        Parameters of the lens model.
        
    """
    rs, ks = p
    r = norm_fast([theta1, theta2])
    
    if r < zero: return zeros([2,2])
    
    if r == rs:
        return array([[2./15.*ks*(-1.+6.*(theta2/rs)**2), -4.*theta1*theta2*ks/(5.*rs**2)],
                      [-4.*theta1*theta2*ks/(5.*rs**2), 2./15.*ks*(5.-6.*(theta2/rs)**2)]])
        
    K = 2.*ks*rs / (r*(r**2-rs**2)**2)
    Q = 2.*ks*rs**2 / (r**2-rs**2)**2
    
    alpha_xx = K * (r*rs*(rs**2 + theta1**2 - theta2**2) * (F(r/rs)-1.) \
                    - theta1**2 * (r**2-rs**2) * Fr(r/rs))
    alpha_yy =-K * (r*rs*(rs**2 - theta1**2 + theta2**2) * (1.-F(r/rs)) \
                    + theta2**2 * (r**2-rs**2) * Fr(r/rs))
    
    alpha_xy = Q*theta1*theta2 * (2.*(F(r/rs)-1.)-rs/r*((r/rs)**2-1.)*Fr(r/rs))
    # --> alpha_yx = alpha_xy
    
    return array([[alpha_xx, alpha_xy],[alpha_xy, alpha_yy]])


# TODO: instead of a vectorized version of the functions, one should
#       create iterator's version for each of them.