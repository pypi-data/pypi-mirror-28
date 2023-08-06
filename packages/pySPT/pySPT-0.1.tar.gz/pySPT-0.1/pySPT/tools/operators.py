#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 12:36:55 2016

@author: Sciences
"""

from numdifftools import Gradient, Jacobian, Hessian, Hessdiag
from numpy import array

from ..decorators.profile import timeit
from ..multiproc.multiproc import Multiprocessing 
from .container import HandlingDict

__author__ = 'O. Wertz @ Bonn'
__all__ = ['curl2d',
           'curl2d_sequence',
           'derivative',
           'divergence2d',
           'divergence2d_sequence',
           'grad',
           'grad2d',
           'grad_sequence']

def grad(x, fun, **kwargs):
    """
    """
    assert callable(fun), 'fun must be callable'
    return Gradient(fun, **kwargs)(x)

def grad_sequence(seq, fun, mp_kwargs={'nprocs':4}, **kwargs):
    """
    """
    _kwargs = HandlingDict.merge_dicts({'fun':fun},kwargs)
    mp = Multiprocessing(grad, seq, _kwargs)
    res = mp.run(**mp_kwargs)
    return array(res)

def div(x, fun, **kwargs):
    """
    # FIXME: does not work properly
    """
    assert callable(fun), 'fun must be callable'
    jac = Jacobian(fun, **kwargs)(x)
    return jac[0,0] + jac[1,1] + jac[2,2]

def div_sequence(seq, fun, mp_kwargs={'nprocs':4}, **kwargs):
    """
    # FIXME: does not work properly
    """
    _kwargs = HandlingDict.merge_dicts({'fun':fun},kwargs)
    mp = Multiprocessing(div, seq, _kwargs)
    res = mp.run(**mp_kwargs)
    return array(res)

def curl(x, fun, **kwargs):
    """
    # FIXME: does not work properly    
    """
    assert callable(fun), 'fun must be callable'
    jac = Jacobian(fun, **kwargs)(x)
    return array([jac[2,1]-jac[1,2],jac[0,2]-jac[2,0],jac[1,0]-jac[0,1]])

def curl_sequence(seq, fun, mp_kwargs={'nprocs':4}, **kwargs):
    """
    # FIXME: does not work properly    
    """
    _kwargs = HandlingDict.merge_dicts({'fun':fun},kwargs)
    mp = Multiprocessing(curl, seq, _kwargs)
    res = mp.run(**mp_kwargs)
    return array(res)

def laplacian(x, fun, **kwargs):
    """
    """
    assert callable(fun), 'fun must be callable'
    hes = Hessdiag(fun, **kwargs)(x)
    return sum(hes)

def laplacian_sequence(seq, fun, mp_kwargs={'nprocs':4}, **kwargs):
    """
    """
    _kwargs = HandlingDict.merge_dicts({'fun':fun},kwargs)
    mp = Multiprocessing(laplacian, seq, _kwargs)
    res = mp.run(**mp_kwargs)
    return array(res)

def hessian(x, fun, **kwargs):
    """
    """
    assert callable(fun), 'fun must be callable'
    return Hessian(fun, **kwargs)(x)

def hessian_sequence(seq, fun, mp_kwargs={'nprocs':4}, **kwargs):
    """
    """
    _kwargs = HandlingDict.merge_dicts({'fun':fun},kwargs)
    mp = Multiprocessing(hessian, seq, _kwargs)
    res = mp.run(**mp_kwargs)
    return array(res)

@timeit
def derivative(val, func, h=1.49e-06, **kwargs):
    """
    func: callable
        func is callable and must return, for a set of arguments, a 2d vector.
    """
    assert callable(func), 'fct must be callable'
    
    # D_1 fct_component_1
    fct_D1_v1 = func(val-h, **kwargs)
    fct_D1_v2 = func(val+h, **kwargs)
    D1_fct_1 = (fct_D1_v2 - fct_D1_v1)/(2.*h)
    
    return D1_fct_1

@timeit    
def grad2d(pos, func, h=1.49e-06, **kwargs):
    """
    func: callable
        func is callable and must return, for a set of arguments, a 2d vector.
    """
    assert callable(func), 'fct must be callable'
    
    # D_1 fct_component_1
    fct_D1_v1 = func(pos[0]-h, pos[1], **kwargs)
    fct_D1_v2 = func(pos[0]+h, pos[1], **kwargs)
    D1_fct_1 = (fct_D1_v2 - fct_D1_v1)/(2.*h)

    # D_2 fct_component_2
    fct_D2_v1 = func(pos[0], pos[1]-h, **kwargs)
    fct_D2_v2 = func(pos[0], pos[1]+h, **kwargs)
    D2_fct_2 = (fct_D2_v2 - fct_D2_v1)/(2.*h)    
    
    return array([D1_fct_1, D2_fct_2])

@timeit    
def curl2d(pos, func, h=1.49e-06, **kwargs):
    """
    func: callable
        func is callable and must return, for a set of arguments, a 2d vector.
    """
    assert callable(func), 'fct must be callable'
    
    # D_1 fct_component_2
    fct_D1_v1 = func(pos[0]-h, pos[1], **kwargs)
    fct_D1_v2 = func(pos[0]+h, pos[1], **kwargs)
    D1_fct_2 = (fct_D1_v2[1] - fct_D1_v1[1])/(2.*h)

    # D_2 fct_component_1
    fct_D2_v1 = func(pos[0], pos[1]-h, **kwargs)
    fct_D2_v2 = func(pos[0], pos[1]+h, **kwargs)
    D2_fct_1 = (fct_D2_v2[0] - fct_D2_v1[0])/(2.*h)    
    
    return D1_fct_2 - D2_fct_1
    
@timeit
def curl2d_sequence(sequence, func, h=1.49e-06, nprocs=1, run_options={}, **kwargs):
    """
    func: callable
        fct is callable and must return, for a set of arguments, a sequence 
        of 2d vector.
    """
    assert callable(func), 'fct must be callable'
                                                  
    curl2d_kwargs = {'func':func, 'h':h}

    MP = Multiprocessing(curl2d, sequence, HandlingDict.merge_dicts(kwargs, curl2d_kwargs))
    res = MP.run(nprocs=nprocs, **run_options)
    return array(res)
    
@timeit   
def divergence2d(pos, func, h=1.49e-06, **kwargs):
    """
    """
    """
    func: callable
        func is callable and must return, for a set of arguments, a 2d vector. 
        The func signature should be func(x, y, **kwargs).
    """
    assert callable(func), 'func must be callable'
    
    # D_1 fct_component_2
    fct_D1_v1 = func(pos[0]-h, pos[1], **kwargs)
    fct_D1_v2 = func(pos[0]+h, pos[1], **kwargs)
    D1_fct_1 = (fct_D1_v2[0] - fct_D1_v1[0])/(2.*h)

    # D_2 fct_component_1
    fct_D2_v1 = func(pos[0], pos[1]-h, **kwargs)
    fct_D2_v2 = func(pos[0], pos[1]+h, **kwargs)
    D2_fct_2 = (fct_D2_v2[1] - fct_D2_v1[1])/(2.*h)    
    
    return D1_fct_1 + D2_fct_2
    
@timeit
def divergence2d_sequence(sequence, func, h=1.49e-06, nprocs=1, run_options={}, **kwargs):
    """
    func: callable
        fct is callable and must return, for a set of arguments, a sequence 
        of 2d vector.
    """
    assert callable(func), 'fct must be callable'
                                                  
    divergence2d_kwargs = {'func':func, 'h':h}

    MP = Multiprocessing(divergence2d, sequence, HandlingDict.merge_dicts(kwargs, divergence2d_kwargs))
    res = MP.run(nprocs=nprocs, **run_options)
    return array(res)    

#@timeit    
#def vectorLaplacian2d(pos, func, h=1.49e-06, **kwargs):
#    """
#    func: callable
#        func is callable and must return, for a set of arguments, a 2d vector.
#    """
#    assert callable(func), 'fct must be callable'
#    
#    def _grad_0(pos, func, **kwargs):
#        return grad2d(pos, func, **kwargs)
#    
#
#    divergence2d(t12, _grad_0, **kwargs)
#
#    # D_1 fct_component_1
#    fct_D1_v1 = func(pos[0]-h, pos[1], **kwargs)
#    fct_D1_v2 = func(pos[0]+h, pos[1], **kwargs)
#    D1_fct_1 = (fct_D1_v2 - fct_D1_v1)/(2.*h)
#    
#    return 0.0