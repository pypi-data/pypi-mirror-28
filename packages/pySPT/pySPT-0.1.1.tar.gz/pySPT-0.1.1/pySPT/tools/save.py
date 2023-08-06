#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 16:15:41 2017

@author: Sciences
"""

from pickle import dump, load, HIGHEST_PROTOCOL
from time import localtime

__author__ = 'O. Wertz @ Bonn'
__all__ = ['HandlingFilename',
           'PickleObject'
           ]

class HandlingFilename(object):
    """
    """
    def __init__(self):
        """
        """
        _now = localtime()
        self._now = '{}_{}_{}_{}h{}m{}s'.format(_now.tm_year, _now.tm_mon, 
                                                _now.tm_mday, _now.tm_hour,
                                                _now.tm_min,  _now.tm_sec)
        self.__now = self._now
        
    @property
    def now(self):
        return self._now  

    @staticmethod
    def right_now():
        """
        """
        _now = localtime()
        _now_str = '{}_{}_{}_{}h{}m{}s'.format(_now.tm_year, _now.tm_mon, 
                                               _now.tm_mday, _now.tm_hour,
                                               _now.tm_min,  _now.tm_sec)
        return _now_str                      

    def update_now(self):
        """
        """
        self._now = HandlingFilename.right_now()
        return None     

    def back_to_instanced_now(self):
        """
        """
        self._now = self.__now
        return None            
        
    def filename_complete(self, main='', sub='', now=None, **kwargs):
        """
        """
        assert isinstance(now, bool) or now is None, '`now` must be a boolean'
        
        if now is None or now is False:
            now = self._now
        else:
            now = HandlingFilename.right_now()
            
        f = ''
        for key, value in kwargs.items():
            if isinstance(value,int) or isinstance(value,str):
                f += '_'+key+'_{}'.format(value)
            else:
                f += '_'+key+'_{:.2f}'.format(value)   
        f = f.replace('.','p')
        
        if main == '':
            return now + '_' + sub + f
        else:
            return main + '_' + now + '_' + sub + f
        
class PickleObject(object):
    """
    """
    @staticmethod
    def save_pickle(filename, obj):
        """
        """
        with open(filename+'.pickle', 'wb') as f: 
            dump(obj, f, HIGHEST_PROTOCOL)            
        return None

    @staticmethod
    def load_pickle(filename):
        """
        """
        with open(filename, 'rb') as f:  
            obj = load(f)
        return obj  
      