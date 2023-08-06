#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 17:09:38 2017

@author: Sciences
"""

__author__ = 'O. Wertz @ Bonn'
__all__ = ['EULEUR_MASCHERONI_CONST',
           'MSG_NO_ARGS'
           ]

# The Euler-Mascheroni constant, up to 66 digits
EULEUR_MASCHERONI_CONST = 0.577215664901532860606512090082402431042159335939923598805767234885

# Assert messages
MSG_NO_ARGS = ("No model parameters have been found. Either define the "
               "attribut `p0` of the `Model` instance (if passed) or define "
               "`args_0`.")