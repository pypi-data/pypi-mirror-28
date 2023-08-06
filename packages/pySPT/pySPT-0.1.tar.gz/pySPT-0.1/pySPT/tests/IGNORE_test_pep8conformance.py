#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 23:39:48 2017

@author: Sciences
"""

from unittest import TestCase, TestLoader, TextTestRunner, TestSuite
from sys import modules
from inspect import getmembers, isclass, getmodule
from pycodestyle import StyleGuide

from os import getcwd, listdir
from os.path import isfile, join


class TestCodeFormat(TestCase):
    """
    """
    def test_pep8_conformance(self, quiet=True):
        """Test that we conform to PEP-8."""
        style = StyleGuide(quiet=quiet)
        
        main_dir = '/'.join(getcwd().split('/')[:-1])
        py_files = [join(main_dir,f) for f 
                    in listdir(main_dir) 
                    if (isfile(join(main_dir, f)) 
                        and f.endswith('.py'))]
                    
        n_total_errors = style.check_files(py_files).total_errors
        msg = 'Found {} code style errors (and warnings).'
        self.assertEqual(n_total_errors, 0, msg.format(n_total_errors)) 
       
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