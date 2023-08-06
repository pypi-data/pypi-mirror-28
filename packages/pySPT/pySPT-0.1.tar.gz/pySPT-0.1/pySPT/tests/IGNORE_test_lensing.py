#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 20:13:35 2017

@author: Sciences
"""
#from __future__ import (absolute_import)

from unittest import TestCase, TestLoader, TextTestRunner, TestSuite
from sys import modules
from inspect import getmembers, isclass, getmodule
from numpy import array
from numpy.random import uniform

from pySPT.lensing import Model

class TestModelOperatorOverriding(TestCase):
    """
    """
    def setUp(self):
        self.lens0 = Model('NIS', p0='random')
        self.lens1 = Model('SHEAR', p0='random')
    
    def test_add_alpha(self):
        """
        TODO: should test for more than 1 set of parameter
        """
        pos = uniform(-self.lens0.p0[1],self.lens0.p0[1],2)
        alpha_sep = array(self.lens0.alpha(pos)) + array(self.lens1.alpha(pos))
        alpha_add = array((self.lens0 + self.lens1).alpha(pos))
        self.assertTrue((alpha_sep == alpha_add).all())
           
               
def suite():
    """
    """
    moduleName = modules[suite.__module__].__name__

    classes = getmembers(modules[__name__], isclass)
    mainClasses = [_t for _t 
                   in classes 
                   if getmodule(_t[1]).__name__ == moduleName
                       and _t[0].startswith('Test')]
    
    testSuiteAll = []
    
    for _mc in mainClasses:
        testSuiteAll += TestLoader().loadTestsFromTestCase(_mc[1])
        
    return testSuiteAll       
            
if __name__ == '__main__':
    print TextTestRunner(verbosity=2).run(TestSuite(suite())) 