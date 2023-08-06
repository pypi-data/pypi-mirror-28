# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 09:14:36 2016

@author: Sciences

Decorators
----------
http://www.artima.com/weblogs/viewpost.jsp?thread=240845
https://wiki.python.org/moin/PythonDecoratorLibrary

A do-nothing decorator class would look like this:
    
class NullDecl (object):        
    def __init__ (self, func):
        self.func = func
        for name in set(dir(func)) - set(dir(self)):
            setattr(self, name, getattr(func, name))

    def __call__ (self, *args, **kwargs):
        return self.func(*args, **kwargs) 

"""
from collections import Hashable
from functools import partial
from inspect import stack
from os import path
from pickle import loads, dumps
from re import sub
from unicodedata import normalize

from ..tools.container import arg_first_iterable

__author__ = 'O. Wertz @ Bonn'
__all__ = ['Decenter',
           'Deprecated', 
           'Memorize',
           'Signature'
           ]

class Decenter(object):
    """Decorator that apply a decentering of the position where a quantity
    is evaluated.
    """
    def __init__(self, delta=None):
        """Since they are decorator arguments, the function to be decorated 
        is not passed to the constructor.
        """
        self.delta = delta

    def __call__(self, func):
        """Since there are decorator arguments, __call__() is only called
        once, as part of the decoration process. You can only give
        it a single argument, which is the function object.
        """
        def wrapped_func(*args, **kwargs):
            j = arg_first_iterable(args)
            if self.delta is not None:               
                args2 = tuple([(args[k][0] - self.delta[0],args[k][1] - self.delta[1]) 
                                if k == j 
                                else _ 
                                for k,_ in enumerate(args)])
                return func(*args2, **kwargs)                
            else:
                return func(*args, **kwargs)
        
        return wrapped_func    


class Signature (object):
    """
    Decorator putting a mark on functions which should change of signature:
    Old --> func((a,b), *args[1:], **kwargs)
    New --> func(*args, **kwargs)
    where args[0] = a and args[1] = b.
    """        
    def __init__ (self, func):
        self.func = func
        for name in set(dir(func)) - set(dir(self)):
            setattr(self, name, getattr(func, name))

    def __call__ (self, *args, **kwargs):
        try:
            # Then, args[0] is iterable
            #_ = (k for k in args[0])
            print 'args[0] of func `{}` is an iterable containing {} elements.'.format(self.func.__name__, len(args[0])),
            print 'Consider changing the func signature to accept the first args[0] as {} separated arguments.'.format(len(args[0]))
            return self.func(*args, **kwargs)
        except TypeError:
            # Then, args[0] is not iterable
            #print args
            #print kwargs
            #return self.func(*args, **kwargs)
            return self.func(args[:2], *args[2:], **kwargs) 

class Deprecated(object):
    """Decorator that can be used to mark functions as deprecated. 
    It will result in a warning being emitted when the function is used.
    """
    def __init__(self, new_method_to_call=None, extra_text_to_print=None):
        """Since they are decorator arguments, the function to be decorated 
        is not passed to the constructor.
        """
        self.nmtc_txt = new_method_to_call
        self.extra = extra_text_to_print

    def __call__(self, func):
        """Since there are decorator arguments, __call__() is only called
        once, as part of the decoration process. You can only give
        it a single argument, which is the function object.
        """
        def wrapped_func(*args, **kwargs):
            print 'DeprecationWarning: call to deprecated function {}.'.format(func.__name__)            
            if self.nmtc_txt is not None:
                print 'In future, use the method {}() instead.'.format(self.nmtc_txt)
            
            if self.extra is not None:
                print '{}'.format(self.extra)                
            
            return func(*args, **kwargs)
        
        return wrapped_func   
        

class Memorize(object):
    """
    A function decorated with @Memorize caches its return
    value every time it is called. If the function is called
    later with the same arguments, the cached value is
    returned (the function is not reevaluated). The cache is
    stored as a .cache file in the current directory for reuse
    in future executions. If the Python file containing the
    decorated function has been updated since the last run,
    the current cache is deleted and a new cache is created
    (in case the behavior of the function has changed).
    """
    def __init__(self, func):
        self.func = func
        self.set_parent_file() # Sets self.parent_filepath and self.parent_filename
        self.__name__ = self.func.__name__
        self.set_cache_filename()
        if self.cache_exists():
            self.read_cache() # Sets self.timestamp and self.cache
            if not self.is_safe_cache():
                self.cache = {}
        else:
            self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, Hashable):
            return self.func(*args) 
        #print 'Memorize: args: ',args
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            self.save_cache()
            return value

    def set_parent_file(self):
        """
        Sets self.parent_file to the absolute path of the
        file containing the memoized function.
        """
        rel_parent_file = stack()[-1][1]#.filename
        self.parent_filepath = path.abspath(rel_parent_file)
        self.parent_filename = _filename_from_path(rel_parent_file)

    def set_cache_filename(self):
        """
        Sets self.cache_filename to an os-compliant
        version of "file_function.cache"
        """
        filename = _slugify(self.parent_filename.replace('.py', ''))
        funcname = _slugify(self.__name__)
        self.cache_filename = filename+'_'+funcname+'.cache'

    def get_last_update(self):
        """
        Returns the time that the parent file was last
        updated.
        """
        last_update = path.getmtime(self.parent_filepath)
        return last_update

    def is_safe_cache(self):
        """
        Returns True if the file containing the memoized
        function has not been updated since the cache was
        last saved.
        """
        if self.get_last_update() > self.timestamp:
            return False
        return True

    def read_cache(self):
        """
        Read a pickled dictionary into self.timestamp and
        self.cache. See self.save_cache.
        """
        with open(self.cache_filename, 'rb') as f:
            data = loads(f.read())
            self.timestamp = data['timestamp']
            self.cache = data['cache']
            

    def save_cache(self):
        """
        Pickle the file's timestamp and the function's cache
        in a dictionary object.
        """
        with open(self.cache_filename, 'wb+') as f:
            out = dict()
            out['timestamp'] = self.get_last_update()
            out['cache'] = self.cache
            f.write(dumps(out))

    def cache_exists(self):
        '''
        Returns True if a matching cache exists in the current directory.
        '''
        if path.isfile(self.cache_filename):
            return True
        return False

    def __repr__(self):
        """ Return the function's docstring. """
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """ Support instance methods. """
        return partial(self.__call__, obj)

def _slugify(value):
    """
    Normalizes string, converts to lowercase, removes
    non-alpha characters, and converts spaces to
    hyphens. From
    http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
    """
    value = normalize('NFKD', unicode(value,'utf-8')).encode('ascii', 'ignore')
    value = sub(r'[^\w\s-]', '', value.decode('utf-8', 'ignore'))
    value = value.strip().lower()
    value = sub(r'[-\s]+', '-', value)
    return value

def _filename_from_path(filepath):
    return filepath.split('/')[-1]      