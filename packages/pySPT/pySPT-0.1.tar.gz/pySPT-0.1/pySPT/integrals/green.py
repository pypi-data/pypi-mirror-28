#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:08:27 2016

@author: Sciences
"""
from numpy import array, cos, sin, log, pi

__author__ = 'O. Wertz @ Bonn'
__all__ = ['GradientGreenFunction',
           'GreenFunction'
           ]

class GreenFunction(object):
    """
    Green's function for a circular region of radius R and defined for the 
    Neumann boundary problem in the framework of the Source Position 
    Transformation (see Eq.(20) in Unruh et al. 2016):
    
    (1) log[(ct - t)**2]/R**2
    (2) - (|ct|**2 + |t|**2) / R**2
    (3) log[1 - (2 ct.t)/R**2 + (|ct|**2 |t|**2)/R**4]
    
    where ct and t are 2d-vectors and R a scalar. Then we have:
    
    H(ct,t) = (1/4*pi) * [(1) + (2) + (3)]
    """
    def __init__(self, ctheta, phi, radius):
        """
        """
        self._ctheta = ctheta
        self._phi = phi
        self._R = radius
        
        self._ct1 = self._ctheta * cos(self._phi)
        self._ct2 = self._ctheta * sin(self._phi)

    @property
    def R(self):
        return self._R
        
    @R.setter
    def R(self, value):
        self._R = value 
        
    @property
    def ctheta(self):
        return self._ctheta                
        
    @ctheta.setter
    def ctheta(self, value):
        self._ctheta = value 
        self._ct1 = self._ctheta * cos(self._phi)
        self._ct2 = self._ctheta * sin(self._phi)         
        
    @property
    def phi(self):
        return self._phi                
        
    @phi.setter
    def phi(self, value):
        self._phi = value 
        self._ct1 = self._ctheta * cos(self._phi)
        self._ct2 = self._ctheta * sin(self._phi)
        
    def gf_1(self, r, varphi):
        """
        Implementation of K * log[(ct - t)**2]/R**2, the first component of the 
        Green's function, where ct and t are 2d-vectors and K = 1/(4*pi).
        
        Parameters
        ----------
        r, varphi: float
            Polar coordinates of a point in the lensed plane where the 
            Green\'s function is evaluated. 
               
        """  
        t1, t2 = r * cos(varphi), r * sin(varphi)        
        norm_ct_minus_t_squared = (self._ct1-t1)**2 + (self._ct2-t2)**2        
        return (1./(4.*pi)) * log(norm_ct_minus_t_squared/self._R**2) 
        
    def gf_2(self, r, varphi):
        """
        Implementation of - K * (|ct|**2 + |t|**2)/R**2, the first component of the 
        Green's function, where ct and t are 2d-vectors and K = 1/(4*pi).
        
        Parameters
        ----------
        r, varphi: float
            Polar coordinates of a point in the lensed plane where the 
            Green\'s function is evaluated.                
        """  
        #t1, t2 = r * cos(varphi), r * sin(varphi)        
        #norm_ct_minus_t_squared = (self._ct1-t1)**2 + (self._ct2-t2)**2        
        return (-1./(4.*pi)) * (self._ctheta**2 + r**2)/self._R**2

    def gf_3(self, r, varphi):
        """
        Implementation of K * log(1 - 2*dot(ct,t)/R**2 + |ct|**2*|t|**2/R**4), 
        the first component of the 
        Green's function, where ct and t are 2d-vectors and K = 1/(4*pi).
        
        Parameters
        ----------
        r, varphi: float
            Polar coordinates of a point in the lensed plane where the 
            Green\'s function is evaluated.                
        """  
        t1, t2 = r * cos(varphi), r * sin(varphi) 
        dotprod = self._ct1*t1 + self._ct2*t2
        return (1./(4.*pi)) * log(1. - 2.*dotprod/self._R**2 + self._ctheta**2 * r**2 / self._R**4)
        
    
class GradientGreenFunction(object):
    """
    Gradient of the Green's function for a circular region of radius R and 
    defined for the Neumann boundary problem in the framework of the Source
    Position Transformation (see Eq.(21) in Unruh et al. 2016):
    
    (1) (ct - t)/|ct - t|**2
    (2) - ct / R**2
    (3) [|t|**2 ct - R**2 t] / [R**4 - 2 ct.t + |ct|**2 |t|**2]
    
    where ct and t are 2d-vectors and R a scalar. Then we have:
    
    Grad[H(ct,t)] = (1/2*pi) * [(1) + (2) + (3)]
    """
    def __init__(self, ctheta, phi, radius):
        """
        """
        self._ctheta = ctheta
        self._phi = phi
        self._R = radius
        
        self._ct1 = self._ctheta * cos(self._phi)
        self._ct2 = self._ctheta * sin(self._phi)

    @property
    def R(self):
        return self._R
        
    @R.setter
    def R(self, value):
        self._R = value
        
    @property
    def ctheta(self):
        return self._ctheta                
        
    @ctheta.setter
    def ctheta(self, value):
        self._ctheta = value 
        self._ct1 = self._ctheta * cos(self._phi)
        self._ct2 = self._ctheta * sin(self._phi)         
        
    @property
    def phi(self):
        return self._phi                
        
    @phi.setter
    def phi(self, value):
        self._phi = value 
        self._ct1 = self._ctheta * cos(self._phi)
        self._ct2 = self._ctheta * sin(self._phi)
        
    def grad_gf_1_comp_0(self, r, varphi):
        """
        First component of the vector (ct - t)/|ct - t|**2, where ct and t are 
        2d-vectors.
        
        Parameters
        ----------
        r, varphi: float
            Polar coordinates of a point in the lensed plane where the gradient
            of the Green\'s function is evaluated. 
               
        """        
        t1, t2 = r * cos(varphi), r * sin(varphi)        
        norm_ct_minus_t_squared = (self._ct1 - t1)**2 + (self._ct2 - t2)**2    
        return (self._ct1 - t1)/norm_ct_minus_t_squared 

    def grad_gf_1_comp_1(self, r, varphi):
        """
        Second component of the vector (ct - t)/|ct - t|**2, where ct and t are 
        2d-vectors.
        
        Parameters
        ----------
        r, varphi: float
            Polar coordinates of a point in the lensed plane where the gradient
            of the Green\'s function is evaluated. 
            
        """        
        t1, t2 = r * cos(varphi), r * sin(varphi)        
        norm_ct_minus_t_squared = (self._ct1 - t1)**2 + (self._ct2 - t2)**2    
        return (self._ct2 - t2)/norm_ct_minus_t_squared         

    def grad_gf_2_comp_0(self, r, varphi):
        """
        First component of the vector - ct / R**2, where ct is a 2d-vectors and 
        R a scalar.
        
        Parameters
        ----------
        r, varphi: float
            Polar coordinates of a point in the lensed plane where the gradient
            of the Green\'s function is evaluated. 
                    
        """
        return -(1./self._R**2) * self._ct1
        
    def grad_gf_2_comp_1(self, r, varphi):
        """
        Second component of the vector - ct / R**2, where ct is a 2d-vectors 
        and R a scalar.   
        
        Parameters
        ----------
        r, varphi: float
            Polar coordinates of a point in the lensed plane where the gradient
            of the Green\'s function is evaluated. 
                    
        """
        return -(1./self._R**2) * self._ct2       

    def grad_gf_3_comp_0(self, r, varphi):
        """
        First component of the vector 
        [|t|**2 ct - R**2 t] / [R**4 - 2 ct.t + |ct|**2 |t|**2], 
        where ct and t are 2d-vectors and R a scalar. 
        
        Parameters
        ----------
        r, varphi: float
            Polar coordinates of a point in the lensed plane where the gradient
            of the Green\'s function is evaluated. 
                    
        """
        t1, t2 = r * cos(varphi), r * sin(varphi)            
        num = r**2 * self._ct1 - self._R**2 * t1
        denom = self._R**4 - 2*self._R**2 * (self._ct1*t1 + self._ct2*t2) \
                + self._ctheta**2 * r**2        
        return num/denom 

    def grad_gf_3_comp_1(self, r, varphi):
        """
        Second component of the vector 
        [|t|**2 ct - R**2 t] / [R**4 - 2 ct.t + |ct|**2 |t|**2], 
        where ct and t are 2d-vectors and R a scalar.
        
        Parameters
        ----------
        r, varphi: float
            Polar coordinates of a point in the lensed plane where the gradient
            of the Green\'s function is evaluated. 
                    
        """
        t1, t2 = r * cos(varphi), r * sin(varphi)            
        num = r**2 * self._ct2 - self._R**2 * t2
        denom = self._R**4 - 2*self._R**2 * (self._ct1*t1 + self._ct2*t2) \
                + self._ctheta**2 * r**2        
        return num/denom   

    def grad_gf(self, r, varphi):
        """
        Gradient of the Green's function on a circular region of radius R and 
        defined for the Neumann boundary problem in the framework of the Source
        Position Transformation.
        
        Parameters
        ----------
        r, varphi: float
            Polar coordinates of a point in the lensed plane where the gradient
            of the Green\'s function is evaluated. 
                    
        """
        comp_0 = self.grad_gf_1_comp_0(r, varphi) \
                 + self.grad_gf_2_comp_0(r, varphi) \
                 + self.grad_gf_3_comp_0(r, varphi)
        comp_1 = self.grad_gf_1_comp_1(r, varphi) \
                 + self.grad_gf_2_comp_1(r, varphi) \
                 + self.grad_gf_3_comp_1(r, varphi)                
        return (1./(2.*pi)) * array([comp_0, comp_1])                   
        