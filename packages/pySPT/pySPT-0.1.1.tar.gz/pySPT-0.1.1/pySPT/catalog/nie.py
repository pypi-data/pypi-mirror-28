# -*- coding: utf-8 -*-
""" Full name: Non-singular Isothermal Ellipsoid
------------------------------------------------------------
                           NIE                            
------------------------------------------------------------
Description
-----------
As the non-singular isothermal sphere (NIS), the NIE yields a flat 
rotation curve, such as observed for spiral galaxies. However, this
model is intrinsically elliptic, contrary to the NIS which is 
axisymmetric.

The analytical expressions for the surface mass density, deflection
angle and deflection potential are given in [1].

Model parameters
----------------
The model parameters p are p = (b, q, s, theta_e).

b : mass normalization
q : related to the ellipticity 
s : related to the core radius
theta_e: orientation of the ellipticity

Notes
-----
The model parameters (b,q,s) are related to the parameters (b',e,s') 
used in gravlens and defined at Eq.(3.25), p23, in [2].

The parameter order in the gravlens code is:
[p[1], p[4], p[5], p[8]] = [b', e, theta_e, s']

The link to the previous parameters b, q, s and theta_e is given by:

b' = b * q * sqrt(2 / (1+q**2))
e = 1 - q
theta_e is unchanged
s' = s * q * sqrt(2 / (1+q**2))

One can relate these parameters to tE and tC by defining:
    tE = bp / (1-ep**2)**0.5 
    tC = sp / (1-ep**2)**0.5 
where ep (for epsilon in Eq. 3.25) is related to e and q by:
    ep = (1-q**2)/(1+q**2)  ==> q**2 = (1-ep)/(1+ep), and
    ep = (1-(1-e)**2)/(1+(1-e)**2)
  
References
----------    
[1] Keeton, C. R., 2009, *A Catalog of Mass Models for Gravitational Lensing*
URL=https://arxiv.org/abs/astro-ph/0102341
[2] C. Keeton, *gravlens 1.06: Software for Gravitational Lensing*
URL: http://www.physics.rutgers.edu/~keeton/gravlens/manual.pdf  
    
"""

from numpy import array, empty, arctan2, arctan, arctanh, cos, sin, log
from numpy.linalg import norm

__author__ = 'O. Wertz @ Bonn'
__all__ = ['alpha_x',
           'alpha_x_rot_x',
           'alpha_y',
           'alpha_y_rot_x',
           'b2bp',
           'bp2b',
           'deflection_angle',
           'deflection_potential',
           'derivative1_da',
           'e2ep',
           'ep2e',
           'ksi',
           'orig2prime',
           'prime2orig',
           'qprime',
           's2sp',
           'sp2s',
           'standard2orig',
           'standard2prime',
           'surface_mass_density'
           ]

# Conversion between model parameters
def b2bp(b, q):
    return b * q * (2./(1+q**2))**(0.5)
    
def bp2b(bp, q):
    return bp/q * ((1+q**2)/2)**(0.5)
    
def s2sp(s, q):
    return s * q * (2./(1+q**2))**(0.5)
    
def sp2s(sp, q):
    return sp/q * ((1+q**2)/2)**(0.5)

def ep2e(ep):
    return 1 - ((1-ep)/(1+ep))**0.5

def e2ep(e):
    return (1-(1-e)**2)/(1+(1-e)**2)
    
def prime2orig(bp, e, sp, theta_e):
    return bp2b(bp, 1-e), 1-e, sp2s(sp, 1-e), theta_e
    
def orig2prime(b, q, s, theta_e):
    return b2bp(b, q), 1-q, s2sp(s, q), theta_e

def qprime(q):
    return (1-q**2)**(0.5)

def ksi(x,y,q,s):
    return (q**2*(s**2+y**2) + x**2)**(0.5)

def standard2prime(tE, ep, tC, theta_e):
    """ Convert (tE, ep, tC, theta_e) into (bp, e, sp, theta_e)."""
    return tE*(1-ep**2)**0.5, ep2e(ep), tC*(1-ep**2)**0.5, theta_e

def standard2orig(tE, ep, tC, theta_e):
    """ Convert (tE, ep, tC, theta_e) into (b, q, s, theta_e)."""
    return prime2orig(*standard2prime(tE, tC, ep, theta_e))  

def alpha_x(x, y, b, q, s):
    """ First component of the NIE deflection angle without rotation.
    
    Parameters
    ----------
    x,y : double
        Position in the lens plane where the deflection angle is evaluated.
    b, q, s : double
        Model parameters.

    Notes
    -----
    No rotation means theta_e = 0.
    
    """
    if q == 1:
        return b*x/(s+(s**2+x**2+y**2)**(0.5))
    else:
        return b*q/qprime(q)*arctanh((qprime(q)*x)/(ksi(x,y,q,s)+q**2*s))
        
def alpha_y(x, y, b, q, s):
    """ Second component of the NIE deflection angle without rotation.
    
    Parameters
    ----------
    x,y : double
        Position in the lens plane where the deflection angle is evaluated. 
    b, q, s : double
        Model parameters.

    Notes
    -----
    No rotation means theta_e = 0. 
    
    """
    if q == 1:
        return b*y/(s+(s**2+x**2+y**2)**(0.5))
    else:
        return b*q/qprime(q)*arctan((qprime(q)*y)/(ksi(x,y,q,s)+s))        

def alpha_x_rot_x(x, y, b, q, s, theta_e):
    """ First component of the NIE deflection angle with rotation.
    
    Parameters
    ----------
    x,y : double
        Position in the lens plane where the deflection angle is evaluated.    
    b, q, s : double
        Model parameters.  
    theta_e : double
        Orientation of the lens.

    """        
    r = (x**2+y**2)**(0.5)
    theta = arctan2(y,x)
        
    xnew = r*cos(theta-theta_e)
    ynew = r*sin(theta-theta_e)
        
    return alpha_x(xnew,ynew,b,q,s)*cos(theta_e) - \
    alpha_y(xnew,ynew,b,q,s)*sin(theta_e)
    
def alpha_y_rot_x(x, y, b, q, s, theta_e):
    """ Second component of the NIE deflection angle with rotation.
    
    Parameters
    ----------
    x,y : double
        Position in the lens plane where the deflection angle is evaluated.    
    b, q, s : double
        Model parameters.  
    theta_e : double
        Orientation of the lens.
        
    Notes
    -----
    alpha_y_rot_x(x, y, ...) is equivalent to alpha_y_rot_y(y, x, ...).
    
    """    
    r = (x**2+y**2)**(0.5)
    theta = arctan2(y,x)
        
    xnew = r*cos(theta-theta_e)
    ynew = r*sin(theta-theta_e)
        
    return alpha_x(xnew,ynew,b,q,s)*sin(theta_e) + \
    alpha_y(xnew,ynew,b,q,s)*cos(theta_e)    

def deflection_potential((theta1, theta2), p):
    """ Deflection potential associated with an NIE.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection potential is 
        evaluated.
    p : array_like
        Parameters of the lens model.
        
    """ 
    b, q, s, theta_e = p
    
    r = norm((theta1,theta2))#sqrt(x**2+y**2)
    theta = arctan2(theta2,theta1)
    
    x_new = r*cos(theta-theta_e)
    y_new = r*sin(theta-theta_e)
    
    alpha_x_ = alpha_x(x_new, y_new, b, q, s)
    alpha_y_ = alpha_y(x_new, y_new, b, q, s)
    
    if s == 0:
        psi = y_new * alpha_y_ + x_new * alpha_x_
    else:
        psi = y_new * alpha_y_ + \
              x_new * alpha_x_ - \
              b*q*s*log((((q**2*(s**2+y_new**2)+x_new**2)**(0.5) + s)**2 + \
              (1-q**2)*y_new**2)**(0.5)) + b*q*s*log((1+q)*s)
 
    return psi

def deflection_angle((theta1, theta2), p):
    """ Deflection angle associated with an NIE.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the deflection angle is evaluated.
    p : array_like
        Parameters of the lens model.   
        
    """
    b, q, s, theta_e = p
    
    ax_lens = alpha_x_rot_x(theta1, theta2, b, q, s, theta_e)
    ay_lens = alpha_y_rot_x(theta1, theta2, b, q, s, theta_e)
    
    return array([ax_lens, ay_lens])
      
def surface_mass_density((theta1, theta2), p):
    """ Surface mass density associated with an NIE.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the surface mass density is 
        evaluated. 
    p : array_like
        Parameters of the lens model.
        
    """
    b, q, s, theta_e = p
    
    r = norm((theta1,theta2))#(theta1**2+theta2**2)**(0.5)
    theta = arctan2(theta2,theta1)
    
    x_new = r*cos(theta-theta_e)
    y_new = r*sin(theta-theta_e)
    
    return b/(2*((x_new)**2/q**2 + (y_new)**2 + s**2)**(0.5))  

def derivative1_da((theta1, theta2), p):
    """ Jacobi matrix of the deflection mapping associated with an NIE.
    
    Parameters
    ----------
    theta1,theta2 : double
        Position in the lens plane where the Jacobi matrix is evaluated.   
    p : array_like
        Parameters of the lens model.
        
    Notes
    -----
    The order of the parameters within p must be the same as for the C 
    library, that is p = (b, q, s, theta_e). 
    """
    b, q, s, theta_e = p
    
    qpow2 = q**2
    spow2 = s**2
    
    theta1_new = theta1*cos(theta_e) + theta2*sin(theta_e);
    theta2_new = theta2*cos(theta_e) - theta1*sin(theta_e);    
    
    split1 = (qpow2 * spow2
              + (theta1**2 + qpow2 * theta2**2) * cos(theta_e)**2
              + (qpow2 * theta1**2 + theta2**2) * sin(theta_e)**2
              - (-1 + qpow2) * theta1 * theta2 * sin(2*theta_e))**(0.5);
              
    denominator = 2 * (theta1_new**2 + qpow2 * (spow2 + theta2_new**2))**(0.5)\
                    * ((1 + qpow2)*spow2 + theta1**2 + theta2**2 \
                       + 2*s *(theta1_new**2 \
                               + qpow2*(spow2+theta2_new**2))**(0.5))**2; 

    num1 = b*q*((1 + 6 * qpow2 + q**4) * s**4 \
                  + 2 * theta2**2 * (theta1**2 + theta2**2) \
                  + (1 + qpow2) * spow2 * (3*theta1**2 + 5*theta2**2) \
                  + s*(-4*(-1 + qpow2) * s * theta1*theta2 * sin(2*theta_e) \
                       + 2*(2*(1+qpow2)*spow2+theta1**2+3*theta2**2)*split1 \
                       - (-1 + qpow2) * s * cos(2*theta_e) \
                         * (3*theta1**2-theta2**2 + s*(s+qpow2*s+2*split1)))); 

    num2 = b*q*((1 + 6 * qpow2 + q**4) * s**4 \
                  + 2 * theta1**2 * (theta1**2 + theta2**2) \
                  + (1 + qpow2) * spow2 * (5*theta1**2 + 3*theta2**2) \
                  + s*(-4*(-1 + qpow2) * s * theta1*theta2 * sin(2*theta_e) \
                       + 2*(2*(1+qpow2)*spow2+theta2**2+3*theta1**2)*split1 \
                       + (-1 + qpow2) * s * cos(2*theta_e) \
                         * (3*theta2**2-theta1**2 + s*(s+qpow2*s+2*split1))));
                
    j01 = -((b*q*(theta1*theta2 + (-1+qpow2)*spow2*cos(theta_e)*sin(theta_e)))/
                ((theta1_new**2 + qpow2 * (spow2 + theta2_new**2))**(0.5)*
                 ((1 + qpow2)*spow2 + theta1**2 + theta2**2 +
                 2 *s*(theta1_new**2 + qpow2 *(spow2+theta2_new**2))**(0.5))));
    j10 = j01                
                
    j00 = num1/denominator
    j11 = num2/denominator

    res = empty([2,2])
    res[0,0] = j00
    res[1,1] = j11
    res[0,1] = j01
    res[1,0] = j10
                      
    return res 
      

# FIXME: gravlens: it seems that sp=0.0 is automatically modified to sp=0.0001