#!/usr/bin/env python2
# -*- coding: utf-8 -*-
""" Full Name: Softened Power-Law Ellipsoid
------------------------------------------------------------
                          SPLE                            
------------------------------------------------------------
Description
-----------
This model has a projected surface density

kappa(xi) = 0.5 * b**(2-a) / (s**2 + xi**2)**(1 - a/2)

which represents a flat core with scale radius s, and then a power law 
decline with exponent a defined such that the mass grows as 
M_cyl(r) \propto r asymptotically. See [1] for more details.

Model parameters
----------------
b : mass normalization
s : related to the core radius
a : exponent of the power law

Notes
-----
No additional comments.

References
----------
[1] Keeton, C. R., 2009, *A Catalog of Mass Models for Gravitational Lensing*
URL=https://arxiv.org/abs/astro-ph/0102341

"""

from numpy import array, zeros, log
from scipy.special import hyp2f1, polygamma

from ..tools.vector import norm_fast
from ..tools.const import EULEUR_MASCHERONI_CONST

__author__ = 'O. Wertz @ Bonn'
__all__ = ['alpha_sple_polar',
           'deflection_angle',
           'deflection_potential',
           'derivative1_da',
           'kappa_sple_polar',
           'psi_sple_polar'
           ]

def psi_sple_polar(r, p, zero=1.49e-12, gravlens=False):
    """ Deflection potential associated with an SPLE, in polar coordinates.
    
    Parameters
    ----------
    r : double
        Radial position in the lens plane where the deflection potential is 
        evaluated.
    p : array_like
        Parameters of the lens model.
    zero : double
        Limit under which r is considered to be equal to 0.
        
    Note
    ----
    Implementation of Eqs.(27) and (28) in [1]. 
    
    """
    b, s, a = p
    
    if r < zero or a == 0.0: return 0.0
    
    if gravlens: 
        # To match the GravLens output (see docstring for more details)        
        K0 = 1.
    else:
        # For consistency with alpha(r) and kappa(r).
        K0 = a
        
    K1 = K0 * (1./a) * b**(2.-a) 
    
    if a > 0 and s == 0:
        return K1 * (1./a) * r**a
    else:
        t1 = (1./a) * r**a * hyp2f1(-0.5*a, -0.5*a, 1.-0.5*a, -(s/r)**2)
        t2 = s**a * log(r/s)
        t3 = 0.5 * s**a * (EULEUR_MASCHERONI_CONST + polygamma(0, -0.5*a))    # + polygamma(...) (personal communication from C. Keeton)     
        return K1 * (t1 - t2 - t3)

def deflection_potential((theta1, theta2), p, **kwargs):
    """ Deflection potential associated with an SPLE.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection potential is 
        evaluated.
    p : array_like
        Parameters of the lens model.
        
    """
    r = norm_fast([theta1, theta2])
    return psi_sple_polar(r, p, **kwargs)
    
def alpha_sple_polar(r, p, zero=1.49e-12):
    """ Deflection angle associated with an SPLE, in polar coordinates.
    
    Parameters
    ----------
    r : double
        Radial position in the lens plane where the deflection angle is 
        evaluated.
    p : array_like
        Parameters of the lens model.
    zero : double
        Limit under which r is considered to be equal to 0.   

    Notes
    -----
    Warning: implementation of Eqs.(29) and (30) in [1] multiplied by the 
    parameter `a'. Thus, this implementation matches the results returned
    by `gravlens'.

    """
    b, s, a = p
    
    assert a != 0.0 or s != 0.0, 'The deflection angle is not defined for a=0 and s=0.'
    
    if r < zero or a == 0.0: return 0.0
        
    if a == 0.0 and s > 0.0:
        return b**2/r * log(1. + (r/s)**2)
    else:
        return a * b**(2.-a) / (a*r) * ((s**2 + r**2)**(0.5*a) - s**a)
    
def deflection_angle((theta1, theta2), p, zero=1.49e-12, **kwargs):
    """ Deflection angle associated with an SPLE.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection angle is evaluated.
    p : array_like
        Parameters of the lens model.
        
    """
    r = norm_fast([theta1, theta2])
    
    if r < zero: return zeros(2)    

    alpha = alpha_sple_polar(r, p, **kwargs)    
    return alpha/r * array([theta1, theta2])
    
def kappa_sple_polar(r, p, zero=1.49e-12):
    """ Surface mass density associated with an SPLE, in polar coordinates.
    
    Parameters
    ----------
    r : double
        Radial position in the lens plane where the surface mass density is 
        evaluated.
    p : array_like
        Parameters of the lens model.
    zero : double
        Limit under which r is considered to be equal to 0.    

    Notes
    -----
    Warning: implementation of Eq.(26) in [1] multiplied by the 
    parameter `a'. Thus, this implementation matches the results returned
    by `gravlens'.
   
    """
    b, s, a = p
    
    if r < zero and s == 0.0:
        return 0.0
    else:
        return a * 0.5 * b**(2.-a) / (s**2 + r**2)**(1.-0.5*a)
   
def surface_mass_density((theta1, theta2), p, **kwargs):
    """ Surface mass density associated with an SPLE.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the surface mass density is 
        evaluated. 
    p : array_like
        Parameters of the lens model.
        
    """
    r = norm_fast([theta1, theta2])
    
    return kappa_sple_polar(r, p, **kwargs)
    

# n-th derivative of psi
def derivative1_da((theta1, theta2), p, zero=1.49e-12):
    """ Jacobi matrix of the deflection mapping associated with an HERN.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the Jacobi matrix is evaluated.   
    p : array_like
        Parameters of the lens model.
        
    Notes
    -----
    Warning: the implementation is multiplied by the parameter `a' to match 
    the results returned by `gravlens'.    
  
    """
    b, s, a = p
    x, y = theta1, theta2
    
    r = norm_fast([x, y])
    
    if r < zero or a == 0.0: return zeros([2,2])    
    
    K1 = b**(2.-a) / (a * r**4)
    P1 = (s**2 + r**2)**(0.5*(a-2.))
    d = (x**2 - y**2)

    alpha_xx = a * K1 * ( d*s**a + P1 * ((a-2.) * x**2 * r**2 + r**4 - s**2*d))
    alpha_yy = a * K1 * (-d*s**a + P1 * ((a-2.) * y**2 * r**2 + r**4 + s**2*d))   
    alpha_xy = a * K1 * x*y * (2.*s**a + P1 * ((a-2.)*r**2 - 2.*s**2))
    #--> alpha_yx = alpha_xy
    
    return array([[alpha_xx, alpha_xy],[alpha_xy, alpha_yy]])    
    
"""
[This warning corresponds to an older version of gravlens. The issue pointed
here has been solved.]

WARNING: 
--------
THE EQUATIONS ON WHICH GRAVLENS IS BASED ARE DESCRIBED IN:
    + DENSITY PROFILE kappa(r): 
        1°) EQ.(3.25) IN GRAVLENS MANUAL        
        2°) EQ.(26) IN 'A Catalog of Mass Models for Gravitational Lensing' 
            (Keeton, 2002)
            
    + DEFLECTION LAW alpha(r):
        EQS.(29) and (30) IN 'A Catalog of Mass Models for Gravitational 
        Lensing' (Keeton, 2002)
        
    + DEFLECTION POTENTIAL psi(r):
        EQS.(27) and (28) IN 'A Catalog of Mass Models for Gravitational 
        Lensing' (Keeton, 2002)

WHILE THESE EQUATIONS ARE CONSISTENT, THOSE IMPLEMENTED INTO GRAVLENS ARE NOT. 
INDEED, IT APPEARS THAT THE IMPLEMENTED DENSITY PROFILE EQ.(3.25) IS MULTIPLIED
BY THE POWER-LAW INDEX PARAMETER `a`, AND THE DEFLECTION LAW IS EQS.(29)-(30)
MULTIPLIED ALSO BY `a`. HOWEVER, THE IMPLEMENTED DEFLECTION POTENTIAL SEEMS TO 
CORRECTLY CORRESPOND TO THE EQS.(27) AND (28). THIS MEANS THAT THE GRAD[PSI] 
DOES NOT LONGER EQUAL THE DEFLECTION LAW. INDEED, IT TURNS OUT THAT:
    
    Grad[psi_GravLens] = alpha_GravLens / a
    Laplacian[psi_GravLens] = 2 kappa_GravLens / a
             
WHICH NEGATIVELY AFFECTS, FOR EXAMPLE, THE FERMAT POTENTIAL AND THEREFORE THE
TIME DELAYS BETWEEN LENSED IMAGES.
    
FOR CONSISTENCY, ONE SHOULD EITHER MULTIPLIED THE EQS.(27) AND (28) FOR THE 
DEFLECTION POTENTIAL BY `a` OR DIVIDE THE EQS.(29), (30) AND (3.25) BY `a`. THE
LATTER OPTION WOULD MAKE THE IMPLEMENTATION CONSISTENT WITH THE THEORY 
PRESENTED IN 'A Catalog of Mass Models for Gravitational Lensing' 
(Keeton, 2002).

TO MATCH RESULTS RETURNED BY GRAVLENS, THE DEFLECTION LAW AND DENSITY PROFILE 
HAVE BEEN MULTIPLIED BY THE PARAMETER `a`. FOR CONSISTENCY, THE DEFLECTION 
POTENTIAL HAS ALSO BEEN MULTIPLIED BY `a`, AND THEREFORE DOES NOT MATCH THE ONE
RETURNED BY GRAVLENS.
"""