# -*- coding: utf-8 -*-
""" Full name: Non-singular Isothermal Sphere
------------------------------------------------------------
                           NIS                            
------------------------------------------------------------
Description
-----------
The non-singular isothermal sphere (NIS) corresponds to a distribution of 
self-gravitating particles where the velocity distribution at all radii
is Maxwellian. This model yields a flat rotation curve, such as observed 
for spiral galaxies. The NIS shares the infinite total mass with the 
singular isothermal sphere (SIS), as their density profiles agree for large 
radial distances. However, in the context of lensing, the infinite mass poses
no problem.

The mean surface mass density is defined by

.. math::
    \bar{\kappa}(\theta) = \frac{\theta_{\text{e}}}}{\sqrt{\theta^2 + \theta_{\text{c}}^2}}
    
More details can be found in [1].
    

Model parameters
----------------
tc : the core radius
te : a normalization constant


Notes
-----
When $\theta$ is much larger than the core radius, the mass distribution 
approaches that of an SIS with an Einstien angle (tE)_SIS = te. Whereas 
(tE)_SIS is the angular radius of the Einstein ring that we can observe when 
the source, lens (SIS) and observer are perfectly aligned, te is NOT the 
location of the critical curve for the NIS.

References
----------
[1] Schneider, P., 2006, Saas-Fee Advanced Course 33: Gravitational Lensing: 
    Strong, Weak and Micro, http://adsabs.harvard.edu/abs/2006glsw.conf...91K

"""

from numpy import empty, zeros, vstack, array
from numpy.random import uniform

__author__ = 'O. Wertz @ Bonn'
__all__ = ['deflection_angle',
           'deflection_potential',
           'derivative1_1_psi_nis',
           'derivative1_2_psi_nis',
           'derivative2_11_psi_nis',
           'derivative2_12_psi_nis',
           'derivative2_21_psi_nis',
           'derivative2_22_psi_nis',
           'derivative1_da',     
           'random_parameters_nis',
           'surface_mass_density',
           ]

def deflection_potential((theta1, theta2), p):
    """ Deflection potential associated with an NIS.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection potential is 
        evaluated.
    p : array_like
        Parameters of the lens model.
        
    """
    tC, tE = p
    return tE * (tC**2 + theta1**2 + theta2**2)**(0.5)

def deflection_angle((theta1, theta2), p):
    """ Deflection angle associated with an NIS.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection angle is evaluated.
    p : array_like
        Parameters of the lens model.
        
    """
    # FIXME:the following `if` raise an error when he's called to plot the SDF. 
    #       The reason is that (theta1,theta2) is, in that case, a tuple of 
    #       matrices which cannot be compared with a tuple of 2 floats.
    try:
        if (theta1,theta2) == (0.0,0.0) and p[0]==0.0:
            return [0.0,0.0]
    except ValueError:
        pass

    tC, tE = p    
    K = tE / (tC**2 + theta1**2 + theta2**2)**(0.5)    
    return [K*theta1, K*theta2] 
    
def surface_mass_density((theta1, theta2), p):
    """ Surface mass density associated with an NIS.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the surface mass density is 
        evaluated. 
    p : array_like
        Parameters of the lens model.
        
    """
    if (theta1,theta2) == (0.0,0.0) and p[0]==0.0:
        return 0.0
        
    tC, tE = p
    theta_squared = theta1**2 + theta2**2
    return tE*0.5 * (2*tC**2 + theta_squared) / (tC**2 + theta_squared)**(1.5)  

# n-th derivative of psi
# n = 1
def derivative1_1_psi_nis((theta1, theta2), p):
    """ First derivative of the deflection potential with respect to the 1st 
    component: \psi_{,1}.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the derivative is evaluated. 
    p : array_like
        Parameters of the lens model.  
        
    """
    tC, tE = p    
    K = tE / (tC**2 + theta1**2 + theta2**2)**(0.5)
    return K*theta1
    
def derivative1_2_psi_nis((theta1, theta2), p):
    """ First derivative of the deflection potential with respect to the 2nd 
    component: \psi_{,2}.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the derivative is evaluated.
    p : array_like
        Parameters of the lens model. 
        
    """
    tC, tE = p    
    K = tE / (tC**2 + theta1**2 + theta2**2)**(0.5)
    return K*theta2   

## n = 2
def derivative2_11_psi_nis((theta1, theta2), p):
    """ Second derivative of the deflection potential with respect to the 1st 
    component: \psi_{,11}.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the derivative is evaluated.
    p : array_like
        Parameters of the lens model. 
        
    """
    tC, tE = p
    theta_squared = theta1**2 + theta2**2
    K = tE / (tC**2 + theta_squared)**(1.5)
    return K*(theta2**2 + tC**2)
    
def derivative2_22_psi_nis((theta1, theta2), p):
    """ Second derivative of the deflection potential with respect to the 2nd 
    component: \psi_{,22}.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the derivative is evaluated.  
    p : array_like
        Parameters of the lens model. 
        
    """
    tC, tE = p
    theta_squared = theta1**2 + theta2**2
    K = tE / (tC**2 + theta_squared)**(1.5)
    return K*(theta1**2 + tC**2)

   
def derivative2_12_psi_nis((theta1, theta2), p):
    """ Second derivative of the deflection potential with respect to the 1st 
    and 2nd component: \psi_{,12}.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the derivative is evaluated.   
    p : array_like
        Parameters of the lens model. 
        
    """
    tC, tE = p
    theta_squared = theta1**2 + theta2**2
    K = tE / (tC**2 + theta_squared)**(1.5)
    return -K*theta1*theta2 
    

def derivative2_21_psi_nis((theta1, theta2), p):
    """ Second derivative of the deflection potential with respect to the 2nd 
    and 1st component: \psi_{,21}.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the derivative is evaluated.  
    p : array_like
        Parameters of the lens model. 
    
    """
    return derivative2_12_psi_nis((theta1, theta2), p)   
    
           
def derivative1_da((theta1, theta2), p):
    """ Jacobi matrix of the deflection mapping associated with an NIS.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the Jacobi matrix is evaluated.   
    p : array_like
        Parameters of the lens model.
        
    """
    if (theta1,theta2)==(0.0,0.0) and p[0]==0:
        return zeros([2,2])
    else:
        res = empty([2,2])  
    
    t1s = theta1**2
    t2s = theta2**2
    K = p[1] / (p[0]**2 + t1s + t2s)**(1.5)

    res[0,0] = K*(t2s + p[0]**2) #D2_11_psi_NIS((theta1, theta2), p)
    res[1,1] = K*(t1s + p[0]**2) #D2_22_psi_NIS((theta1, theta2), p)
    res[0,1] = -K*theta1*theta2 #D2_12_psi_NIS((theta1, theta2), p)
    res[1,0] = res[0,1] 
    return res
# -----------------------------------------------------------------------------

def random_parameters_nis(n=1, bounds=None):
    """ Randomly define `n' sets of model parameters.
    
    Parameters
    ----------
    n : int
        Number of parameter sets.
    bounds : [(a1,a2),(b1,b2)] array_like
        The parameter bounds. By default:
        + core radius       --> 0.0 and 0.2
        + Einstein radius   --> 0.5 and 2.0

    """
    if bounds is None:
        bounds = array([[0.0,0.2],[0.5,2.0]])
    
    rand0 = uniform(bounds[0,0],bounds[0,1],n)    
    rand1 = uniform(bounds[1,0],bounds[1,1],n)
    
    if n == 1:
        return array([rand0[0]*rand1[0], rand1[0]])
    elif n > 1:
        return vstack((rand0*rand1,rand1)).T
    
# TODO: vectorialiser les functions de sorte qu'elles acceptent (theta1, theta2)
#       avec thetai une matrice NxN.
#
# TODO: function signature should be func(theta1, theta2, ...) instead of 
#       func((theta1, theta2))    