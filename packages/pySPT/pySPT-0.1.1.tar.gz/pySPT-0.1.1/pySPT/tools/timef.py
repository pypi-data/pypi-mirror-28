#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 18:02:19 2017

@author: Sciences
"""
from time import localtime as _localtime

__author__ = 'O. Wertz @ Bonn'
__all__ = ['TimeFormatter']

class TimeFormatter(object):
    """
    """
    def __init__(self):
        """
        """
        pass
    
    @staticmethod
    def localtime():
        """
        """
        return _localtime()
        
    @classmethod
    def now(cls, lt=None):
        """
        """
        if lt is None:
            lt = cls.localtime()
        
        year = str(lt.tm_year)
        _month = lt.tm_mon
        _day = lt.tm_mday
        _hour = lt.tm_hour
        _minute = lt.tm_min
        _sec = lt.tm_sec

        if _month < 10:
            month = '0' + str(_month)
        else:
            month = str(_month)
        
        if _day < 10:
            day = '0' + str(_day)
        else:
            day = str(_day)

        if _hour < 10:
            hour = '0' + str(_hour)
        else:
            hour = str(_hour)

        if _minute < 10:
            minute = '0' + str(_minute)
        else:
            minute = str(_minute)    
            
        if _sec < 10:
            sec = '0' + str(_sec)
        else:
            sec = str(_sec)            
    
        return [year, month, day, hour, minute, sec]    
