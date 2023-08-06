#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:29:06 2017

@author: bastianorthen, O.Wertz
"""
from numpy import array, ndarray

from pySPT.tools import norm_fast, isiterable
#from pySPT.lensing import Model

__all__ = ['MSTsp',
           'MSTlp'
           ]


class MSTsp(object):
    """
    Returns the MST transormed values in the source plane.
    """
    def __init__(self, lamdba=1.0, beta=None):
        """
        Parameters
        ----------
        beta: list/array of float values
            Source position in the source plane.
        lambda : float
                Parameter of the mass sheet transformation.
            
        Note 
        -------
        The source position beta can either be passed when instantiate the class
        `MSTsp` or when using the method `modified_source_position`. 
        """
        self.el = lamdba
        self.beta = beta
        
    def modified_source_position(self, beta=None):
        """
        Returns the MST transormed source position $\hat{beta}$ in the source plane.
    
        Parameters
        ----------
        beta: list/ndarray of float values
            Source position in the source plane.
        
        Returns
        -------
        hatbeta: ndarray
            Vector containing the MST-transformed source positions.
            
        Note 
        -------
        The source position beta can either be passed when instantiate the class
        `MSTsp` or when using the method `modified_source_position`. 
        """
        if beta is None:
            beta = self.beta
        
        assert beta is not None, 'No `beta` has been passed.'
        
        if not isinstance(beta, ndarray):
            beta = array(beta)
            
        assert beta.shape == (2,), 'The shape of `beta` {} does not match the required (2,).'.format(beta.shape)
        
        return self.el * beta


class MSTlp(object):
    """
    """
    def __init__(self, lamdba=1.0, theta=None):
        """
        """
        self.el    = lamdba
        self.theta = theta

    def conditiontest(self, x, fun):    
        """
        """
        if x is None:
            x = self.theta
         
        assert x is not None, '`theta` has not been passed.'
        
        if not isinstance(x, ndarray):
            x = array(x)

        if not isiterable(fun):
            fun = [fun]
            
        for _fun in fun:
            assert callable(_fun), 'kappa should be a callable object, {} has been passed.'.format(type(_fun))
        
        return x
        
    
    def modified_kappa(self, kappa, theta=None, **kwargs):
        """
        Todo fertig schreiben...
        Returns the MST transormed convergence $\hat{kappa}$ in the source plane.
    
        Parameters
        ----------
        beta   : list/array of float values
                Source position in the source plane.
        
        Returns
        -------
        hatbeta : ndarray
                Vector containing the `MST`-transformed source positions.
            
        Note 
        -------
        The source position beta can either been passed when instantiate the class
        `MSTsp` or when using the method `modified_source_position`. 
        """
        theta = self.conditiontest(theta, kappa)
        
        return (1-self.el) + self.el * kappa(theta, **kwargs)
    
    def modified_deflection(self, alpha, theta=None):
        """
        """
        theta = self.conditiontest(theta, alpha)
        
        return (1- self.el)* theta + self.el * array(alpha((theta)))
    
    def modified_potential(self, psi, theta=None):
        """
        """
        theta = self.conditiontest(theta, psi)
        
        return ((1.- self.el)/2.) * (theta[0]**2 + theta[1]**2) + self.el * psi(theta)
    
    def modified_tau(self, alpha, psi, theta=None):
        """
        """
        mode_def = array(self.modified_deflection(alpha, theta))
        mod_pot = self.modified_potential(psi, theta)
        return 0.5*(mode_def[0]**2 + mode_def[1]**2) - mod_pot