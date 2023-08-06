#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase, TestLoader, TextTestRunner, TestSuite
from sys import modules
from inspect import getmembers, isclass, getmodule

from numpy import identity, array
from numpy.random import uniform

from pySPT.sourcemapping import SourceMapping
from pySPT.tests import MSTlp
from pySPT.lensing import Model
from pySPT.spt import SPT
from pySPT.tools import norm_fast, cutoff

__author__ = 'B. Orthen @ Bonn, O. Wertz @ Bonn'
__all__ = ['TestIdentity',
           'TestSPTReducedToMST']


class TestIdentity(TestCase):
    """
    For an identity SPT, i.e. no transformation applied, one tests whether the
    quantities computed with SourceMapping are left unchanged.
    """   
    def setUp(self):
        self.mapping = SourceMapping('identity')
        self.pos     = uniform(-5.0,5.0,(3,2)) ## 40
    
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
        test1 = [self.mapping.jacobi_matrix_spt_mapping(_pos) for _pos in self.pos]
        self.assertTrue((test1 == identity(2)).all()) 

    
class TestSPTReducedToMST(TestCase):
    """
    For an SPT reduced to an MST, one tests whether the SPT-Transformed 
    quantities (computed with SourceMapping) are consistent with the 
    well-known analytical results. To this aim, TestSPTReducedToMST uses a 
    radial isotropic streching with (f0,f2)=(f0,0). This reduces the SPT to 
    an MST characterized by $lambda = (1 + f0)$.
    """       
    def setUp(self):
        self.pos = uniform(0,5,(3,2)) ## 15 -> 3
        self.f2  = 0.0
        self.f0  = uniform(0.0,1.0,3) ## 15 -> 3
        self.R   = array([norm_fast(_pos) * 1.5 for _pos in self.pos])
        self.lens = Model('NIS', p0='random')+Model('SHEAR',p0='random')
        self.sptobj = SPT(SourceMapping('identity'),self.lens)
        self.sptobj.load_C_libraries('NISG','IS1') 
    
    def test_mstjm_equal_sptjm(self):
        """
        Check that the jacobi matrix is equal to $diag(1+f0,1+f0)$.
        """
        for _f0 in self.f0:
            mapping=SourceMapping(1,_f0,self.f2)
            test1 = array([mapping.jacobi_matrix_spt_mapping(_pos) for _pos in self.pos])
            test2 = array([[1+_f0,0],[0,1+_f0]])
        
        self.assertTrue((test1 == test2).all())
        
    def test_mstkappa_equal_sptkappa(self):
        """
        Check that hatkappa_spt == hatkappa_mst, for random sets of source 
        positions and deformation parameters f0.
        """
        for _f0 in self.f0:
            mst = MSTlp(1+_f0)
            self.sptobj.source_mapping = SourceMapping(1,_f0,self.f2)
            test1 = array([array(self.sptobj.modified_kappa(*_pos)) for _pos in self.pos])
            test2 = array([mst.modified_kappa(self.lens.kappa, _pos) for _pos in self.pos])
            
        self.assertTrue((cutoff(test1,10) == cutoff(test2,10)).all())
        
    def test_mstalpha_equal_sptalpha(self):
        """
        Check that hatalpha_spt == hatalpha_mst, for random sets of source 
        positions and deformation parameters f0.
        """
        for _f0 in self.f0:
            mst = MSTlp(1+ _f0)
            self.sptobj.source_mapping = SourceMapping(1,_f0,self.f2)
            test1 = array([array(self.sptobj.tilde_alpha_fast(*_pos, R= _R)) for _pos, _R in zip(self.pos,self.R)])
            test2 = array([mst.modified_deflection(self.lens.alpha, _pos) for _pos in self.pos])

        self.assertTrue((cutoff(test1,6) == cutoff(test2,6)).all())
       
    def test_mstpsi_equal_sptpsi(self):
        """
        Check that hatpsi_spt == hatpsi_mst, for random sets of source 
        positions and deformation parameters f0.
        """
        for _f0 in self.f0:
            mst = MSTlp(1 + _f0)
            self.sptobj.source_mapping = SourceMapping(1,_f0,self.f2)
            test1 = array([self.sptobj.tilde_psi_fast(*_pos, R = _R) - self.sptobj.tilde_psi_fast(*_pos + 0.01, R = _R) for _pos, _R in zip(self.pos,self.R)])
            test2 = array([mst.modified_potential(self.lens.psi, _pos) - mst.modified_potential(self.lens.psi, _pos + 0.01) for _pos in self.pos])
            
        self.assertTrue((cutoff(test1,5) == cutoff(test2,5)).all())
        
    def test_msttau_equal_spttau(self):   
        """
        Check that hattau_spt == hattau_mst, for random sets of source 
        positions and deformation parameters f0.
        """
        for _f0 in self.f0:
            mst = MSTlp(1 + _f0)
            self.sptobj.source_mapping = SourceMapping(1,_f0,self.f2)
            test1 = array([self.sptobj.tilde_tau(_pos, R = _R) - self.sptobj.tilde_tau(_pos + 0.01, R = _R) for _pos, _R in zip(self.pos,self.R)])
            test2 = array([mst.modified_tau(self.lens.alpha, self.lens.psi, _pos) - mst.modified_tau(self.lens.alpha, self.lens.psi, _pos+0.01) for _pos in self.pos])
        
        self.assertTrue((cutoff(test1,5) == cutoff(test2,5)).all())
             
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
    