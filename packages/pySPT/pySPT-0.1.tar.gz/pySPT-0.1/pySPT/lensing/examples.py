#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import abc

from numpy import deg2rad

from .. import catalog
from ..decorators.others import Decenter
from ..tools.toolbox import combine, DynamicFunctionMaker
from ..tools.container import HandlingContainer

__author__ = 'O. Wertz @ Bonn'
__all__ = ['Example0']


class ExampleInterface(object):
    """ Interface that defines which methods an example class must implement.
    """
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def get_parameters(self):
        pass
    
    @abc.abstractmethod
    def get_basics(self):
        pass
        

class Example0(ExampleInterface):
    """ Complex mass distribution composed of 8 NIEs + external shear.    
    """
    def __init__(self):
        self.id = 'exemple_0'
        
        self.centers = ((-0.160, -0.888),
                        (0.761, 1.235),
                        (0.791, -0.555),
                        (1.352, 1.013),
                        (-0.375, 0.148),
                        (1.135, 0.006),
                        (0.490, -1.437),
                        (0.742, -0.091),
                        (0.000, 0.000))
        
        self.p = ((0.268, 0.562, 0.052, deg2rad(64.907)),
                  (0.322, 0.791, 0.127, deg2rad(45.027)),
                  (0.333, 0.463, 0.067, deg2rad(157.361)),
                  (0.675, 0.306, 0.211, deg2rad(216.404)),
                  (0.225, 0.723, 0.071, deg2rad(233.340)),
                  (0.296, 0.482, 0.136, deg2rad(134.145)),
                  (0.486, 0.327, 0.046, deg2rad(20.439)),
                  (0.589, 0.319, 0.125, deg2rad(104.884)),
                  (0.210, deg2rad(224.189)))
        
        self.p_combined = None
        self.basics = None
        
    @staticmethod
    def get_id():
        """ Give the id of the example."""
        return 'example_0'

    def get_parameters(self):
        """ 
        Give the complete lens model parameters. As a recall, the NIE model 
        parameters are: b, q, s, theta_e. 
        
        Returns
        -------
        parameters : tuple
            The parameters wrapped as nested tuples, as required for the 
            Model class.
        """
        self.p_combined = combine(*self.p)
        return self.p_combined
    
    def get_basics(self):
        """ Provide callables for the deflection potential, deflection angle, 
        surface mass density, and the Jacobi matrix of the deflection mapping. 
        
        Returns
        -------
        basics : dict
            A dictionnary composed of the keys psi, alpha, kappa and jm_alpha. 
            The corresponding values are callable objects which give the 
            deflection potential, deflection angle, surface mass density, 
            and the Jacobi matrix of the deflection mapping, respectively.
        """   
        # Deflection potential
        def psi_generic(pos, p, center):
            @Decenter(center)
            def _psi(pos, p):
                return catalog.nie.deflection_potential(pos, p)
            return _psi(pos, p)
        
        dyn_psi = DynamicFunctionMaker(psi_generic)
        
        for i,c in enumerate(self.centers[:-1]):
            DynamicFunctionMaker.add_fun(dyn_psi, prefix='psi', label=i,
                                         partial_kwargs={'center':c})
        
        def psi(pos, p):
            p = HandlingContainer(p).flatten()
            res = 0
            for i in range(8):
                res += getattr(dyn_psi,'psi{}'.format(i))(pos,p[i*4:(i*4)+4])
            return res + catalog.shear.deflection_potential(pos,p[-2:])
            
        # Deflection angle
        def alpha_generic(pos, p, center):
            @Decenter(center)
            def _alpha(pos, p):
                return catalog.nie.deflection_angle(pos, p)
            return _alpha(pos, p)
        
        dyn_alpha = DynamicFunctionMaker(alpha_generic)
        
        for i,c in enumerate(self.centers[:-1]):
            DynamicFunctionMaker.add_fun(dyn_alpha, prefix='alpha', label=i,
                                         partial_kwargs={'center':c})
        
        def alpha(pos, p):
            p = HandlingContainer(p).flatten()
            res = 0
            for i in range(8):
                res += getattr(dyn_alpha,'alpha{}'.format(i))(pos,p[i*4:(i*4)+4])
            return res + catalog.shear.deflection_angle(pos,p[-2:])
        
        # Surface mass density
        def kappa_generic(pos, p, center):
            @Decenter(center)
            def _kappa(pos, p):
                return catalog.nie.surface_mass_density(pos, p)
            return _kappa(pos, p)
        
        dyn_kappa = DynamicFunctionMaker(kappa_generic)
        
        for i,c in enumerate(self.centers[:-1]):
            DynamicFunctionMaker.add_fun(dyn_kappa, prefix='kappa', label=i,
                                         partial_kwargs={'center':c})
        
        def kappa(pos, p):
            p = HandlingContainer(p).flatten()
            res = 0
            for i in range(8):
                res += getattr(dyn_kappa,'kappa{}'.format(i))(pos,p[i*4:(i*4)+4])
            return res + catalog.shear.surface_mass_density(pos,p[-2:]) 
        
        self.basics = {'psi':psi,
                       'alpha':alpha,
                       'kappa':kappa,
                       'jm_alpha':None}
        
        # Delfection mapping Jacobi matrix
        def jm_alpha_generic(pos, p, center):
            @Decenter(center)
            def _jm_alpha(pos, p):
                return catalog.nie.derivative1_da(pos, p)
            return _jm_alpha(pos, p)
        
        dyn_jm_alpha = DynamicFunctionMaker(jm_alpha_generic)
        
        for i,c in enumerate(self.centers[:-1]):
            DynamicFunctionMaker.add_fun(dyn_jm_alpha, prefix='jm_alpha', 
                                         label=i, partial_kwargs={'center':c})
        
        def jm_alpha(pos, p):
            p = HandlingContainer(p).flatten()
            res = 0
            for i in range(8):
                res += getattr(dyn_jm_alpha,'jm_alpha{}'.format(i))(pos,p[i*4:(i*4)+4])
            return res + catalog.shear.derivative1_da(pos,p[-2:])   
        
        self.basics = {'psi':psi,
                       'alpha':alpha,
                       'kappa':kappa,
                       'jm_alpha':jm_alpha}        
            
        return self.basics

# TODO: include the SS13 fiducial model as an example.