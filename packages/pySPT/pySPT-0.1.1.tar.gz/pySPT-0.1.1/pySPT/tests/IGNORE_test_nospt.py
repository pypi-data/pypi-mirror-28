#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase, TestLoader, TextTestRunner, TestSuite
from sys import modules
from inspect import getmembers, isclass, getmodule
from numpy import array
from numpy.random import uniform

from pySPT.lensing import Model
from pySPT.sourcemapping import SourceMapping
from pySPT.spt import SPT
from pySPT.tools import norm_fast, cutoff

__author__ = 'B. Orthen @ Bonn, O. Wertz @ Bonn'
__all__ = ['TestNoSPT',
           'TestNoSPTNoMST']


class TestNoSPTNoMST(TestCase):
    """
    """
    def setUp(self):
        self.lens   = Model('NIS', p0='random')+Model('SHEAR',p0=(0.3,0.5))
        self.pos    = uniform(-self.lens.p0[0][1],self.lens.p0[0][1],(1,2))
        self.R      = array([norm_fast(_pos) * 1.5 for _pos in self.pos])
        f0,f2       = 0.0,0.0
        self.srcmap = SourceMapping(1,f0,f2)
        self.sptobj = SPT(self.srcmap,self.lens)
        self.sptobj.load_C_libraries('NISG','IS1')
    
    def test_tildehat(self):
        """
        testing for the equality of tilde alpha and hat alpha for an
        isothermal streching with f0=f2=0 .
        """
        test1   = array([array(self.sptobj.modified_alpha(*_pos)) for _pos in self.pos])
        test2   = array([array(self.sptobj.tilde_alpha_fast(*_pos, R=_R)) for _pos,_R in zip(self.pos,self.R)])
        self.assertTrue((cutoff(test1,6) == cutoff(test2,6)).all())
    
    def test_tildealpha(self):
        """
        testing for the equality of tilde alpha and alpha for an
        isothermal streching with f0=f2=0 .
        """
        test1   = array([array(self.sptobj.modified_alpha(*_pos)) for _pos in self.pos])
        test2   = array([array(self.lens.alpha((_pos[0],_pos[1]))) for _pos in self.pos])
        self.assertTrue((cutoff(test1,6) == cutoff(test2,6)).all())
  
class TestNoSPT(TestCase):
    """
    """
    def setUp(self):
        self.lens   = Model('NIS', p0='random')+Model('SHEAR',p0=(0.3,0.5))
        self.pos    = uniform(-self.lens.p0[0][1],self.lens.p0[0][1],(3,2)) ## 20 -> 3
        self.R      = array([norm_fast(_pos) * 1.5 for _pos in self.pos])
        self.f0     = uniform(0.0, 1.0, 3) ## 20 -> 3
        self.f2     = 0.0
        self.sptobj = SPT(SourceMapping('identity'),self.lens)
        self.sptobj.load_C_libraries('NISG','IS1')
        
    def test_msttildehat(self):
        """
        testing for the equality of tilde alpha and hat alpha for an
        isothermal streching with f0=uniform(0.1,1,N) f2=0.
        """       
        for _f0 in self.f0:
            self.sptobj.source_mapping = SourceMapping(1,_f0,self.f2)           
            test1 = array([array(self.sptobj.modified_alpha(*_pos)) for _pos in self.pos])
            test2 = array([array(self.sptobj.tilde_alpha_fast(*_pos, R= _R)) for _pos, _R in zip(self.pos,self.R)])

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