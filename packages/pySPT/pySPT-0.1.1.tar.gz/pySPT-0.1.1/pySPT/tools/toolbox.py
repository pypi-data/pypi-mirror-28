#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
"""

from functools import partial

from numpy import empty, array, vstack, floor, shape, inf, sum
from numpy.linalg import norm
from itertools import permutations

__author__ = ['O. Wertz @ Bonn','B. Orthen @ Bonn']
__all__ = ['combine',
           'cutoff',
           'DynamicFunctionMaker',
           'rejig',
           'remove_duplicate'
           ]

class DynamicFunctionMaker(object):
    """
    Other solution:
        
    class Dynamo(object):
        def __init__(self):
            pass
        
        @Decenter([0.1,0.0])
        def inner(self, (x,y), p):
            return nis.deflection_potential((x,y), p)
        
    def add_fun(cls, i):
        def generic(self, *args):
            return cls.inner(self,*args)
        generic.__name__ = 'psi{}'.format(i)
        setattr(cls,generic.__name__,generic)
        
    d = Dynamo()
    print d.inner(pos,p)    
    
    add_fun(Dynamo, 1)
    print d.psi1(pos,p)        
    """
    def __init__(self, fun=None):
        self._fun = fun
    
    def _inner(self, *args, **kwargs):
        return self._fun(*args, **kwargs)

    @classmethod
    def add_fun(cls, self, prefix, label, partial_kwargs={}):
        if partial_kwargs:
            _inner = partial(cls._inner, **partial_kwargs)
            def generic(self, *args, **kwargs):
                return _inner(self, *args, **kwargs)
        else:
            def generic(self, *args, **kwargs):
                return cls._inner(self, *args, **kwargs)            
        generic.__name__ = '{}{}'.format(prefix,label)
        setattr(cls,generic.__name__,generic)
        
def remove_duplicate(images, threshold=1.0e-06):
    """
    Remove duplicated positions in `images`. We consider two positions as the
    `same` when their angular separation are smaller than the threshold.    
    """    
    if images.size == 0: return images
    
    res = empty(2)
    size = images.shape[0] + 1    
    k = 0
    
    while k < size:
        flush = array([norm(images[k,:]-vec) for vec in images[k+1:,:]]) > threshold
        res = vstack((images[:k+1,:],images[k+1:,:][flush,:]))
        images = res
        size = images.shape[0]
        k += 1
    
    return images         

def combine(*args):
    """
    """
    temp = args[0]
    
    for _ in args[1:]:
        temp = (temp,_)

    return tuple(temp)

def cutoff(value,order=6):
    """
    """
    return floor(array(value) * 10**(order-1))

def rejig(m, template):
    """
    Rearrange the NxM matrix `m` along the first axis to match the `template` 
    NxM matrix. By "matching", we means that we minimize the separation btw
    the two matrix. 
    """
    n_m = shape(m)
    n_template = shape(template)
    assert n_m == n_template, '`m` and `template` must have the same shape.'
    
    perms = list(permutations(range(n_m[0]), n_m[0]))
    mini = [array([inf for _ in template]), -1, None]
    
    for j,p in enumerate(perms):
        w = (sum((template - m[p,:])**2, axis=1))**(0.5)
        if (w <= mini[0]).all():
            mini = [w,j,p]
            
    return m[mini[2],:], mini

