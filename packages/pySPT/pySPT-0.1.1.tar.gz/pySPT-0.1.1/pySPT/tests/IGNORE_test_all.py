#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 20:10:33 2017

@author: Sciences
"""
# TODO: create a test to check the installation of the package, in particular
# check that the C libraries are compiled properly for the user operating
# system.

# FIXME: seems to fail when the test in run outside the tests/ folder. This
# is probably due to dynamic module import and other automatic stuff.

from unittest import TextTestRunner, TestSuite

from os import getcwd, listdir
from os.path import isfile, join

from itertools import chain

# Dynamic module import
tests_dir = getcwd()
names = [f.split('.')[0] for f 
         in listdir(tests_dir) 
         if isfile(join(tests_dir, f)) 
             and f.endswith('.py')
             and not f.split('.')[0].endswith('_all')
             and not f.split('.')[0].endswith('_pep8conformance')]
         
modules = map(__import__, names)  

# unittest test cases      
suites = list(chain.from_iterable([m.suite() for m in modules]))
TextTestRunner(verbosity=2).run(TestSuite(suites))
    