#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase, TestLoader, TextTestRunner, TestSuite
from sys import modules
from inspect import getmembers, isclass, getmodule

from numpy import identity, array
from numpy.random import uniform

from pySPT.sourcemapping import SourceMapping
from pySPT.tests import MSTsp

__author__ = 'B. Orthen @ Bonn, O. Wertz @ Bonn'
__all__ = ['TestIdentity',
           'TestSPTReducedToMST']


class TestIdentity(TestCase):
    """
    For an identity SPT, i.e. no transformation applied, one tests whether the
    quantities computed with SourceMapping are left unchanged.
    """   
    def setUp(self):
        self.n = 1000
        self.mapping = SourceMapping('identity')
        self.pos     = uniform(-5.0,5.0,(self.n,2))
    
    def test_betahat_equal_beta(self):
        """
        Check hatbeta == beta for a set of source positions beta.
        """
        test1 = [self.mapping.modified_source_position(_pos) 
                    for _pos in self.pos]   
        self.assertTrue((test1 == self.pos).all()) 
        
    def test_jm_equals_identity(self):
        """
        Check that the jacobi matrix is the identity matrix.
        """
        test1 = [self.mapping.jacobi_matrix_spt_mapping(_pos) 
                    for _pos in self.pos]
        self.assertTrue((test1 == identity(2)).all()) 
        
        
class TestSPTReducedToMST(TestCase):
    """
    For an SPT reduced to an MST, one tests whether the SPT-Transformed 
    quantities (computed with SourceMapping) are consistent with the 
    well-known analytical results. To this aim, TestSPTReducedToMST uses a 
    radial isotropic streching with (f0,f2)=(f0,0). This reduces the SPT to 
    an MST characterized by lambda = (1 + f0).
    """       
    def setUp(self):
        self.n = 30
        self.pos = uniform(0,5,(self.n,2))
        self.f2  = 0.0
        self.f0  = uniform(0.0,1.0,self.n)
        
    def test_mstbeta_equal_sptbeta(self):
        """
        Check hatbeta_spt == hatbeta_mst, for random sets of source positions 
        and deformation parameters f0.
        """
        for _f0 in self.f0:
            mapping= SourceMapping(1,_f0,self.f2)
            mst    = MSTsp(1+_f0)
            test1  = array([mapping.modified_source_position(_pos) 
                                for _pos in self.pos])
            test2  = array([mst.modified_source_position((_pos)) 
                                for _pos in self.pos])
              
        self.assertTrue((test1 == test2).all())         
             
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
    