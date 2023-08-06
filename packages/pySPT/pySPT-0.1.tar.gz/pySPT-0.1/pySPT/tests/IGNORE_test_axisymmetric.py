#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase, TestLoader, TextTestRunner, TestSuite
from sys import modules
from inspect import getmembers, isclass, getmodule
from numpy import array, trace
from numpy.random import uniform
from numpy.linalg import det

from pySPT.tools import cutoff
from pySPT.lensing import Model

__author__ = 'B. Orthen @ Bonn, O. Wertz @ Bonn'
__all__ = ['TestAxiSymmetric']


class TestAxiSymmetric(TestCase):
    """  
    TestAxiSymmetric uses an NIS as a model for the lens. In the Axi-Symmetric
    care we know analytical formulars. Those are tested in this Class.
    """    
    def setUp(self):
        testnumber      = 10 #5000
        self.pos        = uniform(-2,2,testnumber)
        self.r          = array([(_pos**2)**0.5 for _pos in self.pos])
        self.lnis       = Model('NIS', p0='random', is_axisym=True)
                
    def test_kappaalpha(self):
        """
        test_kappaalpha tests that $\bar{kappa} == alpha/theta$.
        """
        test1  = array([self.lnis.kappa_average(_r) for _r in self.r])
        alpha  = array([self.lnis.alpha((_pos,0))[0] for _pos in self.pos])
        theta  = array([_pos for _pos in self.pos])
        test2  = array([_alpha/_theta for (_alpha,_theta) in zip(alpha,theta)])
        self.assertTrue((cutoff(test1,6) == cutoff(test2,6)).all())

    def test_tracekappa(self):
        """
        test_tracekappe tests that $\Tr{A} == 2*(1 - Kappa)$.
        """
        kappa    = array([self.lnis.surface_mass_density((_pos,0.0)) for _pos in self.pos])
        jac      = [self.lnis.jm_lens_mapping((_pos,0)) for _pos in self.pos]
        test1    = 2 * (1-kappa)
        test2    = array([trace(_jac) for _jac in jac])
        self.assertTrue((cutoff(test1,6) == cutoff(test2,6)).all())   

    def test_detderalpha(self):
        """
        test_deralpha tests that 
        $\det{A} == (1-alpha/theta)*(1- dalpha/ dtheta)$
        """
        alpha    = array([self.lnis.alpha((_pos,0))[0] for _pos in self.pos])
        deralpha = array([self.lnis.jm_alpha_mapping((_pos,0))[0][0] for _pos in self.pos])
        theta    = array([_pos for _pos in self.pos])
        jac      = [self.lnis.jm_lens_mapping((_pos,0)) for _pos in self.pos]
        test1    = array([(1-(_alpha/_theta))*(1-_deralpha) for (_alpha, _theta, _deralpha) in zip(alpha, theta, deralpha)])
        test2    = array([det(_jac) for _jac in jac])
        self.assertTrue((cutoff(test1,6) == cutoff(test2,6)).all())  

def suite():
    """
    """
    moduleName = modules[suite.__module__].__name__

    classes = getmembers(modules[__name__], isclass)
    mainClasses = [_t for _t 
                   in classes 
                   if getmodule(_t[1]) is not None
                       and getmodule(_t[1]).__name__ == moduleName
                       and _t[0].startswith('Test')]
    
    testSuiteAll = []
    
    for _mc in mainClasses:
        testSuiteAll += TestLoader().loadTestsFromTestCase(_mc[1])
        
    return testSuiteAll       
            
if __name__ == '__main__':
    print TextTestRunner(verbosity=0).run(TestSuite(suite())) 
