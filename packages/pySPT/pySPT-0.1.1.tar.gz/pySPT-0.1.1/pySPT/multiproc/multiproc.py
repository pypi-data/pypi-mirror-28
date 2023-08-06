#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:20:26 2016

@author: Sciences

Example
-------

object = classname(attr1=val1, attr2=val2, ...)
method_args = {'arg_name1':arg_val1, 'arg_name2':arg_val2, ...}

MP = Multiprocessing(object.method, sequence, method_args)

RES = MP.run(nprocs=8, profile=True, chunks=False, size_chunks=5000, debug=True)
"""

from functools import partial
from multiprocessing import Queue, Process, cpu_count
from re import search

from numpy import ceil
from psutil import virtual_memory

from ..decorators.profile import timeit
from ..tools.container import HandlingContainer

__author__ = 'O. Wertz @ Bonn'
__all__ = ['available_cpu',
           'Multiprocessing']

def available_cpu():
    """ 
    Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program
    """
    # cpuset may restrict the number of *available* processors
    try:
        m = search(r'(?m)^Cpus_allowed:\s*(.*)$',
                   open('/proc/self/status').read())
        if m:
            res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
            if res > 0:
                return res
    except IOError:
        # Python 2.6+
        return cpu_count()


class Multiprocessing(object):
    """
    """
    def __init__(self, func, sequence, func_extra_kwargs=dict(), 
                 processes=4):
        """
        """
        self._func = func
        self._seq = sequence
        self._kwargs = func_extra_kwargs        
        self._pfunc = partial(self._func, **self._kwargs)  

    @staticmethod            
    def _print_warning_message_1(nprocs, size_chunks):
        """
        """  
        print 'Gentle warning: you set `nprocs` to {} but `size_chunks to {}`. '.format(int(nprocs), int(size_chunks)),
        print 'Since the number of working CPU is min(size_chunks, nprocs) and `size_chunks` < `nprocs` ',
        print ' ==> {} over the {} nprocs will sleep. '.format(nprocs-size_chunks, int(nprocs)),
        print 'If you want all your nprocs to work, set size_chunks >= nprocs.' 
        print ''        
        return None         
                
    def _wrapper(self, f, q_in, q_out):
        """
        """
        while True:
            i, x = q_in.get()
            if i is None:
                break
            q_out.put((i, f(x))) 
                     
    @timeit        
    def run(self, f=None, X=None, nprocs=None, chunks=False, size_chunks=None, 
            debug=False):
        """
        chunks: boolean
            If True, the job is split in sub-jobs and the used memory is freed
            after the end of each sub-job. 
        size_chunks: int
            Size of the sub-sequence (default=None).
            If size_chunks is None, it is automatically set to nprocs.
        """
        if nprocs is None:
            nprocs = available_cpu()
            
        if chunks:
            if size_chunks is None: 
                size_chunks = nprocs
            elif size_chunks < nprocs and debug:
                Multiprocessing._print_warning_message_1(nprocs, size_chunks)                
            else:
                pass
            sequence_generator = HandlingContainer(self._seq).chunks(n=size_chunks)
            N_chunks = int(ceil(len(self._seq)/float(size_chunks)))
        else:
            sequence_generator = HandlingContainer(self._seq).chunks(n=len(self._seq))
            N_chunks = 1
            
        RESULT_COMPLETE = list()    
        for k, partial_seq in enumerate(sequence_generator): 
            if debug: 
                _memory = virtual_memory()
                txt = 'total of memory used by the system'
                print 'Chunk {}/{}'.format(k+1, N_chunks)
                print '   {}: {}% {:.3f}G'.format(txt, _memory.percent, 
                                                  _memory.used/(2.0**30))
            
            q_in = Queue(1)
            q_out = Queue()
        
            proc = [Process(target=self._wrapper, args=(self._pfunc, q_in, q_out))
                    for _ in range(nprocs)]
    
            for p in proc:
                p.daemon = True
                p.start()
        
            sent = [q_in.put((i, x)) for i, x in enumerate(partial_seq)]
            [q_in.put((None, None)) for _ in range(nprocs)]
            res = [q_out.get() for _ in range(len(sent))]
        
            [p.join() for p in proc]
            
            partial_result = [x for _, x in sorted(res)]
            RESULT_COMPLETE += partial_result  
            if debug: print '   done'                    
    
        return RESULT_COMPLETE