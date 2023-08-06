#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from numpy import array
from numpy import cos, sin, arctan2, cosh, sinh, zeros
from numpy.linalg import eig
from numpy.random import uniform

__author__ = 'O. Wertz @ Bonn'
__all__ = ['SourceMapping']

class SourceMapping(object):
    """
    """
#   TODO: do we need a class docstring?
    def __init__(self, which=None, *args, **kwargs):
        """
        Parameters
        ----------
        which : string
            Source mapping id.
            
        """
        self.which = which
        self._args = args
        self._kwargs = kwargs
        self.ID = None

        if self.which == 'general isotropic stretching' or self.which == 0:
            if not self._kwargs and self._args:
                self.f = self._args[0]
                self._f_args = self._args[1]
                self.derivative_f = self._args[2]
            elif self._kwargs:
                self.f = self._kwargs.get('f')
                self._f_args = self._kwargs.get('f_args')
                self.derivative_f = self._kwargs.get('derivative_f')
            self.ID = 'IS0'
            
        elif self.which == 'isotropic stretching 1' or self.which == 1:
            #
            # f(beta) = f0 + 0.5 * f2 * beta**2
            #                       
            if self._args: # True if args is not empty
                self._f_args = self._args[:2]
            elif not self._args and self._kwargs:
                if len(self._kwargs) == 1:
                    self._f_args = self._kwargs.get('f_args',
                                                    self._kwargs.values())
                elif len(self._kwargs) > 1:
                    self._f_args = self._kwargs.values()

            self.f = lambda (beta1, beta2), f_args: f_args[0] + f_args[1]*0.5*(beta1**2 + beta2**2)
            
            def _derivative_f((beta1,beta2), f_args):
                return [f_args[1]*beta1, f_args[1]*beta2]                             
            
            self.derivative_f = _derivative_f
            self.which = 0
            self.ID = 'IS1'
        
        elif self.which == 'isotropic stretching 2' or self.which == 2:
            #
            # f(beta) = f0 + f2 * b0**2 * beta**2 / [2 * (beta**2 + b0**2)]
            #
            if self._args: # True if args is not empty
                self._f_args = self._args[:3]
            elif not self._args and self._kwargs:
                if len(self._kwargs) == 1:
                    self._f_args = self._kwargs.get('f_args',
                                                    self._kwargs.values())
                elif len(self._kwargs) > 1:
                    self._f_args = self._kwargs.values()    

            self.f = lambda (beta1, beta2), f_args: f_args[0] + f_args[2]**2 * f_args[1]*(beta1**2 + beta2**2) / (2.0 * (beta1**2 + beta2**2 + f_args[2]**2))                      
            
            def _derivative_f((beta1,beta2), f_args):                
                temp = f_args[1]*f_args[2]**4/(beta1**2 + beta2**2 + f_args[2]**2)**2
                return [beta1*temp, beta2*temp]            
                        
            self.derivative_f = _derivative_f
            self.which = 0  
            self.ID = 'IS2'            

        elif self.which == 'isotropic stretching 3' or self.which == 3:
            #
            # f(beta) = 2 * f0 / cosh(beta / b0) - f0
            # where b0 = sqrt(3 * (1 - f0)/(1 + f0))
            #
            if self._args: # True if args is not empty
                self._f_args = self._args[:1]
            elif not self._args and self._kwargs:
                if len(self._kwargs) == 1:
                    self._f_args = self._kwargs.get('f_args',
                                                    self._kwargs.values())
                elif len(self._kwargs) > 1:
                    self._f_args = self._kwargs.values()   

            self.f = lambda (beta1, beta2), f_args: 2.0 * f_args[0] / cosh((beta1**2 + beta2**2)**(0.5) / (3.0*(1.0-f_args[0])/(1.0+f_args[0]))**(0.5)) - f_args[0]
            
            def _derivative_f((beta1,beta2), f_args):
                beta = (beta1**2 + beta2**2)**(0.5)
                b0 = (3.0*(1.0-f_args[0])/(1.0+f_args[0]))**(0.5)
                temp = -2.0*f_args[0]/b0 * sinh(beta/b0) / (cosh(beta/b0))**2.0
                return [beta1*temp, beta2*temp]            
                        
            self.derivative_f = _derivative_f
            self.which = 0 
            self.ID = 'IS3'            

        elif self.which == 'identity':
            self._args = zeros(1) 
            self._f_args = zeros(1)
            self.f = lambda (beta1,beta2), f_args: 0.0                             
            self.derivative_f = lambda (beta1,beta2), f_args: zeros(2)
            self.which = -1
            self.ID = 'IDENTITY'            
        
        else:
            print 'Source mapping "{}" not recognized or not yet implemented.'.format(self.which)
            print 'Source mapping implemented so far: '
            print '\t 0: general isotropic stretching'
            print '\t 1: isotropic stretching 1'
            print '\t 1: isotropic stretching 2'

    def _shortcut(self):
#       TODO:docstring there is no parameters i do not know whether we even 
#       need a docstring for this "help method".
        shortcuts_string = {'general isotropic stretching': 'gis'}
        shortcuts_int = {'0': 'gis', '-1': 'gis'}
        shortcut = shortcuts_string.get(self.which)
        if shortcut is not None:
            return shortcut
        else:
            return shortcuts_int.get(str(self.which), 'None')
        
    def _Null(self, *args, **kwargs): return 0.       
    
    def _hatbeta_gis(self, (beta1,beta2)):
        """ For radial streching, give the transformed source position.
        
        Parameters
        ----------
        beta : array_like
            Two dimentional source position.
            
        Returns
        -------
        hatbeta : 2x1 ndarray
            The SPT-modified source position.
            
        """
        return array([(1 + self.f((beta1, beta2), self._f_args)) * beta1,
                      (1 + self.f((beta1, beta2), self._f_args)) * beta2])
        
    def _jm_spt_gis(self, (beta1,beta2), type_output=None):
        """
        For a general isotropic streching, give the jacobi matrix of the 
        source mapping.
        
        Parameters
        ----------
        beta : array_like
            Two dimentional source position where the Jacobi matrix is 
            computed.
        type_output : string
            Define whether the output is a list or an ndarray.
            
        Returns
        -------
        jm : 2x2 ndarray
            The Jacobi matrix of the source mapping.
            
        """
#       TODO: rewrite this method without "type_output".
        temp_0 = (1. + self.f((beta1,beta2),self._f_args))
        der_1, der_2 = self.derivative_f((beta1,beta2),self._f_args)
        res =   [[temp_0 + beta1 * der_1, beta1 * der_2],
                [beta2 * der_1, temp_0 + beta2 * der_2]]
        if type_output is None or type_output is 'list':
            return res
        elif type_output is 'ndarray':
            return array(res)

    def modified_source_position(self, *args, **kwargs):
        """ 
        """
#       TODO: Write the docstring for this method i do not know what i sould
#       write here for parameters ...
        method_name = '_hatbeta_{}'.format(self._shortcut())
        method = getattr(self, method_name, self._Null)
        return method(*args, **kwargs)
        
    def jacobi_matrix_spt_mapping(self, *args, **kwargs):
        """ Give the Jacobi matrix of the source mapping.
        
        Parameters
        ----------
        beta : array_like
            Two dimentional source position where the Jacobi matrix is 
            computed.
            
        Returns
        -------
        jm : 2x2 ndarray
            The Jacobi matrix of the source mapping.
        
        """
#       TODO: Write the docstring for this method i do not know what i sould
#       write here for parameters ...
        method_name = '_jm_spt_{}'.format(self._shortcut())
        method = getattr(self, method_name, self._Null)
        return method(*args, **kwargs)  
        
    def is_MST(self, N=100):
        """ 
        Check whether the source mapping is a pure mass-sheet transformation.
        
        Parameters
        ----------
        N : int
            Number of points which defines the circle where the surface mass 
            density is evaluated.
            
        Returns
        -------
        is_mst : bool
            Return True is the source mapping is a pure MST.
            
        """
        # FIXME: not the smartest way to implement that.
        sources = uniform(-2,2,[N,2])
        spt_jm = [self.jacobi_matrix_spt_mapping(s,type_output='ndarray') for s in sources]
        propt_identity = [all((abs(q[0,0]-q[1,1]) < 1.0e-12, abs(q[0,1]) < 1.0e-12, abs(q[1,0]) < 1.0e-12)) for q in spt_jm]
        return all(propt_identity)
        
    def eigen(self, (beta1, beta2)):
        """ 
        Return the eigenvalues and associated eigenvectors of the Jacobi 
        matrix of the source mapping.
        
        Parameters
        ----------
        beta : array_like
            Two dimentional source position.
            
        Returns
        -------
        eigen : array_like
            returns a tuple of ndarrays containing the eigenvectors and the 
            eigenvalues of the Jacobi matrix of the source mapping.
            
        """
        return eig(self.jacobi_matrix_spt_mapping((beta1,beta2)))        
               
    def B(self, (beta1,beta2)):
        """ 
        Extract the quantities B1 and B2 (see Eq.28, SS14) from the Jacobi 
        matrix of the source mapping.
        
        Parameters
        ----------
        beta : array_like
            Two dimentional source position.
            
        Returns
        -------
        B : ndarray
            Array containing the values for B1 and B2.
            
        """
#       TODO: due to the fact that B1 and B2 is expained at the beginning of
#       the docstirng i would not mention it again in the return part.
        jm_spt = self.jacobi_matrix_spt_mapping((beta1,beta2))
        b1 = 0.5 * (jm_spt[0][0] + jm_spt[1][1])
        b2 = (0.25*(jm_spt[0][0]-jm_spt[1][1])**2 + (jm_spt[0][1])**2)**(0.5)
        return array([b1, b2])
        
    def phase_shear(self, (beta1, beta2)):
        """ Extract the phase_shear (see  "pySPT.sourcemapping - Tutorial"
        available on Github) from the Jacobi matrix of the source mapping.
        
        Parameters
        ----------
        beta : array_like
            Two dimentional source position.
        
        Returns
        -------
        eta : float
            eta is the phase shear of the spt mapping at the position beta.
            
        """
        jm_spt = self.jacobi_matrix_spt_mapping((beta1,beta2))
        b2cos2eta = 0.5*(jm_spt[0][0]-jm_spt[1][1])
        b2sin2eta = jm_spt[0][1]
        return 0.5 * arctan2(b2sin2eta, b2cos2eta)

    def shear_matrix(self, (beta1, beta2)):
        """ Compute the shear matrix from the phase_shear.
        
        Parameters
        ----------
        beta : array_like
            Two dimentional source position.
        
        Returns
        -------
        Gamma : ndarray
            Array containing the sin and cos of twice the phase shear:
            Gamma = martix(  cos(2*eta)   sin(2*eta)
                             sin(2*eta)   -cos(2*eta))
            
        """
        eta = self.phase_shear((beta1, beta2))  
        ceta = cos(2*eta)
        seta = sin(2*eta)
        return array([[ceta, seta],[seta, -ceta]])
 
        
    def det_jm_spt_mapping(self, (beta1, beta2)):
        """ Compute the determinent of the Jacobi matrix of the source mapping.
        
        Parameters
        ----------
        beta : array_like
            Two dimentional source position.
            
        Returns
        -------
        Detjm : float
            Determinant of the jacobi matrix of the source mapping.
            
        """
        jm = self.jacobi_matrix_spt_mapping((beta1, beta2))        
        return jm[0][0]*jm[1][1] - jm[1][0]*jm[0][1]
