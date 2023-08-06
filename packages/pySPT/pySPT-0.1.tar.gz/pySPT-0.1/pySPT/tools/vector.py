#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 16:19:08 2017

@author: Sciences
"""

from numpy import arctan2, vstack, ndarray, sum
from numpy.linalg import norm

from .container import isiterable

__author__ = 'O. Wertz @ Bonn'
__all__ = ['cart2polar',
           'norm_fast'
           ]

def norm_fast(vec):
    """
    `norm_fast` runs much faster than `numpy.linalg.norm` on a tuple or a list 
    of 2 elements.
    
    >>> %time norm_fast([1.,3.])
    >>> 12.2 microseconds
    
    >>> %time numpy.linalg.norm([1.,3.])
    >>> 298 microseconds
    
    `norm_fast` runs slightly faster than `numpy.linalg.norm` on a numpy array.
    """
    if isiterable(vec) and not isinstance(vec, ndarray):
        return (vec[0]**2 + vec[1]**2)**(0.5)
    else:
        if len(vec.shape) == 1:
            return (sum(vec**2))**(0.5)
        else:
            return (sum(vec**2, axis=1))**(0.5)
        
def cart2polar(vec):
    """
    vec: array
        Matrix N x 2 containing N vectors of cartesian coordinates.
    """
    r = norm(vec, axis=1)
    phi = arctan2(vec[:,1], vec[:,0])
    return vstack((r,phi)).T        