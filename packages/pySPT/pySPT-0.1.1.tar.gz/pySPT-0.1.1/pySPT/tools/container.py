#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 16:06:08 2017

@author: Sciences
"""

__author__ = 'O. Wertz @ Bonn'
__all__ = ['arg_first_iterable',
           'HandlingContainer',
           'HandlingDict',
           'isiterable'
           ]

def isiterable(x):
    """
    Check if `x` is an iterable.
    
    Note: The designed-in idiom for such behavioral checks is a 
    "membership check" with the abstract base class in the collections 
    module of the standard library:
    >>> from collections import Iterable
    >>> isinstance(x, Iterable)    
    """
    try:
        iter(x)        
    except TypeError:
        return False
    return True

def arg_first_iterable(iterable):
    """
    """
    for k,z in enumerate(iterable):
        if isiterable(z):
            return k        
    return None
    
class HandlingContainer(object):
    """
    """
    def __init__(self, sequence=None):
        self._seq = sequence
    
    def flatten(self, sequence=None, container=None):
        """
        """
        if sequence is None: sequence = self._seq            
        if container is None: container = list()

        for s in sequence:
            if hasattr(s, '__iter__'):
                self.flatten(s, container)
            else:
                container.append(s)
        return container
    
    def count(self, sequence=None):
        """
        """
        return len(self.flatten(sequence))

    def chunks(self, sequence=None, n=1, index=False):
        """
        Create a generator which yield successive `n`-sized chunks from the 
        sequence.
        
        n: size of the chunks
        """
        if sequence is None: sequence = self._seq
        
        l = len(sequence)
        for i in range(0, l, n):
            if index:
                yield (range(i,min((i+n, l))), sequence[i:i+n])
            else:
                yield sequence[i:i+n]  
                
class HandlingDict(object):
    """
    """
    def __init__(self, dic=None):
        """
        """
        self.dic = dic

    @staticmethod
    def merge_dicts(*dict_args):
        '''
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        '''
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
            
        return result

    def add_dicts(self, *dict_args):
        """
        """
        for dictionary in dict_args:
            self.dic.update(dictionary)
            
        return self.dic        
    
    def update_dict(self, dicRef=None):
        """
        Compare the dictionary `dic` to a reference dictionary `dicRef` and return
        a new dictionary containing all the keys of dicRef which are initialized 
        either to the dic value if the dic.key exists or to the default dicRef 
        value.
        
        Example:
            dic    = {'a':1, 'b':2}
            dicRef = {'a':0, 'b':0, 'c':0}
            updateDict(dic, dicRef) --> {'a':1, 'b':2, 'c':0}
        """
        if dicRef is None: 
            dicRef = {}
    
        if self.dic is None: 
            return dicRef
        elif dicRef == {}:
            return self.dic
        else:
            dic = {key:self.dic.get(key, value) for key,value in dicRef.items()} 
            self.dic.update(dic)
            return self.dic
        