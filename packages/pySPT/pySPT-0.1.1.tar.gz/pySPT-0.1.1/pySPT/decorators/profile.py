#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 18:05:08 2017

@author: Sciences
"""

from functools import wraps
from time import time

from numpy import ndarray

from ..tools.timef import TimeFormatter
from ..tools.container import isiterable

__author__ = 'O. Wertz @ Bonn'
__all__ = ['timed',         
           'timeit'
           ]

def timed(method, *args, **kwargs):
    """
    Function that deals with time, args, and kwargs of a decorated method.
    """
    if kwargs.pop('profile', False):
        # Before
        n = len(method.__name__)
        extra_str = ''.join(['-' for _ in xrange(n)])
        ts = time()
        now = TimeFormatter.now()
        if n <= 34:
            extra_str_2 = ''
            extra_str_3 = ''.join(['-' for _ in xrange(34-n)])
        else:
            extra_str_2 = ''.join(['-' for _ in xrange(n-34)])
            extra_str_3 = ''
        print '----------------------------------{}'.format(extra_str_2)
        print 'Start time: {}-{}-{}  {}h{}m{}s'.format(now[0], now[1], now[2], now[3], now[4], now[5])
        print '----------------------------------{}'.format(extra_str_2)
        print '+ Method name: {}'.format(method.__name__)
        print ''
        print '+ args:'
        if len(args) > 4:
            print 'Too much args to display. Just the first 4 are shown.'
            args_to_display = args[:4]
        else:
            args_to_display = args
            
        for a in args_to_display:
            if isinstance(a, tuple):
                if len(a) > 4:
                    print '({},{},{},{},...) , '.format(a[0],a[1],a[2],a[3])
                else:
                    print a
            elif isinstance(a, list) or isinstance(a, ndarray):
                if len(a) > 4:
                    print '[{},{},{},{},...] , '.format(a[0],a[1],a[2],a[3])
                else:
                    print a,', '                        
            #elif isinstance(a, numpy.array):
            #    pass
            #elif isinstance(v, dict)
            #    pass
            else:
                print a, ', '
            
        print ''        
        print '+ kwargs:'
        if len(kwargs.items()) > 4:
            print 'Too much kwargs to display. Just a few are shown.'
            kwargs_to_display = kwargs.items()[:4]
        else:
            kwargs_to_display = kwargs.items()

        for k,v in kwargs_to_display:
#            if isinstance(v, list) or isinstance(v, tuple):
#                if len(v) > 4:                         
#                    print k, v[:4], '...'
#                else:
#                    print k, v
#            #elif isinstance(a, numpy.array):
#            #    pass 
#            #elif isinstance(v, dict)
#            #    pass
#            else:
#                print '{}: {}'.format(k, v)
            if isiterable(v):
                print '{}: {}'.format(k, type(v))
            else:
                print '{}: {}'.format(k, v)                
                
        print ''
        print 'THE PROCESS IS RUNNING ...'
            
        if kwargs.get('debug', False):
            print '\n+ Debug informations:'
        
        # Method
        result = method(*args, **kwargs)
        
        # After
        te = time()
        now = TimeFormatter.now()
        if kwargs.get('debug', False): print ''
        print 'DONE!'
        print '{}{}'.format(extra_str, extra_str_3)
        print 'Total duration --> {:.4f} sec'.format(te-ts)
        print 'End time:   {}-{}-{}  {}h{}m{}s'.format(now[0], now[1], now[2], now[3], now[4], now[5])
        print '{}{}'.format(extra_str,extra_str_3)
    else:
        result = method(*args, **kwargs)              
    return result

def timeit(method):
    """
    Decorator.
    """
    @wraps(method)
    def _timeit(*args, **kwargs):
        """ Basic decorator profiler""" 
        return timed(method, *args, **kwargs)
    return _timeit