#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

from . import gnfw, hern, nie, nis, shear, sple

__author__ = 'O. Wertz @ Bonn'
__all__ = ['ModelImplemented',
           'ModelInfo'
           ]


class ModelImplemented(object):
    """ Keep track of the lens models implemented in the catalog."""
    def __init__(self):
        self.ids = ['GNFW',
                    'HERN',
                    'NIE',
                    'NIS',
                    'SHEAR',
                    'SPLE'
                    ]
    
    @staticmethod
    def _substring_position(string, substring):
        """ Find the index of a substring within a larger string."""
        try:
            return string.index(substring)
        except ValueError:
            return float('Inf')
        
    def _get_fullnames_from_doc(self):
        """ Extract the full name of the lens model from the docstring of 
        the corresponding *.py file. 

        This method extract automatically all the full names from all the
        lens model *.py files and zip them with their id. 
        For example, the main docstring of the nis.py file defines the 
        corresponding full name, that is `Non-singular Isothermal Sphere'.
        The list returned thus contains:
        [('NIS','Non-singular Isothermal Sphere'), ...]
        
        """
        fullnames = []
        for _id in self.ids:
            first_line = (globals()[_id.lower()]).__doc__.split('\n')[0]
            s = ':'
            index_fullname = ModelImplemented._substring_position(first_line,s)
            
            if index_fullname < float('Inf'):
                fullnames.append((_id,first_line[index_fullname+2:]))
        return fullnames
            
    def list_of_models(self):
        """ Print a table containing the ids and full names of the 
        implemented lens model.
        
        """
        print("-------------------------------------------------------")
        print("     List of models available with `lensing.Model`     ")
        print("-------------------------------------------------------")
        print("----     -----------                                   ")        
        print(" id       full name                                    ")
        print("----     -----------                                   ")
        for model in self._get_fullnames_from_doc():
            print("{} \t {}".format(model[0],model[1]))
        print("no yet complete                                        ")
        print("-------------------------------------------------------")     
        

class ModelInfo(object):
    """ Extract the documentation related to a lens model.
    
    Examples
    --------
    >>> import pySPT
    >>> doc = pySPT.catalog.ModelInfo(which='SHEAR')
    >>> doc.full_documentation()
    ------------------------------------------------------------
                               SHEAR                            
    ------------------------------------------------------------
    Description
    -----------
    The shear models the external perturbations caused by a 
    distribution of mass located nearby the main lens galaxy or 
    along the line of sight.  
    .
    .
    .    
    References
    ----------
    C.S.Kochanek, `Systematic effects in lens inversions: 
        N1 exact models for 0957+561.`, ApJ, 382:58, 1991.
    C.R.Keeton, `A Catalog of Mass Models for Gravitational
        lensing.`, 2002. 
        
    """            
    def __init__(self, which=None):
        """
        Parameters
        ----------
        which : string
            Lens model id. For instance: 'SHEAR'.
            
        """
        self.which = which
        
        if self.which in ModelImplemented().ids:
            self.doc = (globals()[self.which.lower()]).__doc__.split('\n')
        else:
            self.doc = None
                    
    def full_documentation(self):
        """ Print the documention related to a lens model `which'."""
        for line in self.doc[1:]:
            print(line)
