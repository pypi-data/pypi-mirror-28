#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 20:13:35 2017

@author: Sciences
"""

from unittest import TestCase, TestLoader, TextTestRunner, TestSuite
from sys import modules
from inspect import getmembers, isclass, getmodule

class TestStringMethods(TestCase):
    """
    """
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)   
            
class TestStringMethodsNew(TestCase):
    """
    """
    def test_upper_new(self):
        self.assertEqual('foo'.upper(), 'FOO')            
               
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