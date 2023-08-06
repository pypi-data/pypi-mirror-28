# -*- coding: utf-8 -*-
""" Full name: External SHEAR
------------------------------------------------------------
                           SHEAR                            
------------------------------------------------------------
Description
-----------
The shear models the external perturbations caused by a 
distribution of mass located nearby the main lens galaxy or 
along the line of sight.

When sufficiently weak, we expand the corresponding 
deflection potential as a Taylor series. Because of the 0th 
and 1st terms are unobservable and can be dropped, the first 
significant term is the 3rd order one, given by

phi(x) = |x|^2/2 * (kappa_0 + g * cos[2*(theta-theta_g)])

where kappa_0 = Sigma/Sigma_cr represents the convergence 
from the perturbing mass, theta the angular coordinate of 
x, and (g,theta_g) the magnitude and orientation of the 
shear. 

Model parameters
----------------
g      : the shear magnitude
theta_g: the shear orientation

Notes
-----
No additional comments.

References
----------
C.S.Kochanek, `Systematic effects in lens inversions: 
    N1 exact models for 0957+561.`, ApJ, 382:58, 1991.
C.R.Keeton, `A Catalog of Mass Models for Gravitational
    lensing.`, 2002.
    
"""

from numpy import cos, sin, arctan2, empty, pi, array, vstack
from numpy.random import uniform

__author__ = 'O. Wertz @ Bonn'
__all__ = ['deflection_angle',
           'deflection_potential',
           'derivative1_da',
           'random_parameters_shear',
           'surface_mass_density'
           ]

def deflection_potential((theta1, theta2), p):
    """ Deflection potential associated with an external shear.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection potential is 
        evaluated.
        
    p : array_like
        Parameters of the lens model.
    
    Notes
    -----
    This expression of the deflection potential as a function of 
    (theta1,theta2) is equivalent to the expression
    
        psi = 1/2 * r**2 * g * cos[2*(theta - theta_g)] ,
        
    with theta1 = r * cos(theta) and theta2 = r * sin(theta),
    as we can find in 
    C. Keeton, *gravlens documentation*, Eq. 3.23, 2004 
    or in
    C. Kochanek, Saas Fee, Eq. B.26, 2006.
    
    """
    g, theta_g = p
    
    res0 = 0.5 * g * cos(2*theta_g) * (theta1**2 - theta2**2)
    res1 = g * theta1 * theta2 * sin(2*theta_g)
    return res0 + res1    

def deflection_angle((theta1, theta2), p):
    """ Deflection angle associated with an external shear.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection angle is evaluated.
        
    p : array_like
        Parameters of the lens model.

    """
    if p[0] == 0.:
        return [0.,0.]
    
    if p[1] == 0.:
        return [p[0]*theta1, -p[0]*theta2]
    else:   
        r = (theta1**2 + theta2**2)**(0.5)
        theta = arctan2(theta2, theta1)    
        a1 = p[0] * r * cos(theta - 2*p[1])
        a2 = -p[0] * r * sin(theta - 2*p[1])
        return [a1,a2]
   
def surface_mass_density((theta1, theta2), p):
    """ Surface mass density associated with an external shear.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the surface mass density is 
        evaluated.
        
    p : array_like
        Parameters of the lens model.
        
    """
    return 0. 
    
def derivative1_da((theta1, theta2), p):
    """ Jacobi matrix of the deflection mapping associated with an external 
    shear.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the Jacobi matrix is evaluated.
        
    p : array_like
        Parameters of the lens model.
        
    """
    res = empty([2,2])    
    res[0,0] = p[0] * cos(2*p[1])
    res[1,1] = -res[0,0]
    res[0,1] = p[0] * sin(2*p[1])
    res[1,0] = res[0,1]    
    return res 

def random_parameters_shear(n=1, bounds=None):
    """ Randomly define `n' sets of model parameters.
    
    Parameters
    ----------
    n : int
        Number of parameter sets.
    bounds : [(a1,a2),(b1,b2)] array_like
        The parameter bounds. By default:
        + shear intensity   --> 0.0 and 0.2
        + shear orientation --> 0.0 and 2pi

    """
    if bounds is None:
        bounds = array([[0.0,0.2],[0.0,2.0]])
    
    rand0 = uniform(bounds[0,0],bounds[0,1],n)    
    rand1 = uniform(bounds[1,0],bounds[1,1],n) * pi

    if n == 1:
        return array([rand0[0],rand1[0]])
    elif n > 1:
        return vstack((rand0,rand1)).T
    
    
# TODO: vectorialiser les functions de sorte qu'elles acceptent (theta1, theta2)
#       avec thetai une matrice NxN.    