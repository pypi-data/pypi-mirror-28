# -*- coding: utf-8 -*-   

import ctypes
from itertools import izip
from os.path import join, abspath
from os import pardir
from sys import platform
from time import time

from numpy import array, empty, cos, sin, arctan2, pi, zeros, all, where
from numpy import identity
from scipy.integrate import quad, dblquad, nquad
from scipy.optimize import minimize

from ..decorators import timeit
from ..decorators.others import Deprecated
from ..integrals import ConformalMapping, GreenFunction, GradientGreenFunction
from ..lensing import Model
from ..multiproc import Multiprocessing
from ..tools import MSG_NO_ARGS, HandlingContainer, HandlingDict, derivative
from ..tools import norm_fast
from ..tools.container import isiterable

__author__ = 'O. Wertz @ Bonn'
__all__ = ['_CheckBounds',
           'GetCLibraries',
           'SPT'
           ]

# TODO: fix the inconsistency between the way we call methods:
#       method(t1,t2, ...) or method((t1,t2), ...)
            
class SPT(object):
    """ Implements methods to compute a wide range of SPT-modified quantities.
    """
    def __init__(self, SourceMapping_object=None, Model_object=None,
                 root_to_C_libraries=None, debug=False):
        """
        
        Parameters
        ----------
        SourceMapping_object : SourceMapping instance
            Pass an instance of the class `SourceMapping`.
        Model_object : Model instance
            Pass an instance of the class `Model`.        
        root_to_C_libraries : str
            Path to the user's own C libraries required to compute the 
            physically meaningful SPT-modified deflection potential 
            $\tilde{\psi}$ and deflection angle $\tilde{\alpha}$.
        debug : bool
            If True, create a debug-mode SPT object to test the loading of 
            the C libraries.
            
        """ 
        self.debug = debug
        if not self.debug:                    
            self._source_mapping = SourceMapping_object
            self.model = Model_object    
            
            self._args_0 = Model_object.p0    
            assert self._args_0 is not None, MSG_NO_ARGS
        
            # Count the number of original model parameters and stp parameters
            self._model_args = HandlingContainer(self._args_0).flatten()
            self._n0 = len(self._model_args) # or --> Handling_Container(self._args_0).count()        
            self._spt_args = HandlingContainer(self._source_mapping._f_args).flatten()
            self._n1 = len(self._spt_args) # or --> Handling_Container(self._source_mapping._f_args).count() 
            self._all_args = tuple(self._model_args) + tuple(self._spt_args)
        
            # Define the basics
            self.alpha_0 = self.model.alpha
            self.kappa_0 = self.model.kappa
            self.psi_0 = self.model.psi                    
            self.jm_alpha_0 = self.model.jm_alpha_mapping
            
        # Determine the system on which runs python
        platf = platform.lower()
        if ('darwin' in platf or 'mac' in platf):
            # MacOS X
            self.platform = 'osx'
        elif 'linux' in platf:
            # Linux
            self.platform = 'linux'
        elif 'win' in platf:
            # Windows
            self.platform = 'win'
        else:
            print 'The system {} is not yet supported.'.format(platf)
            self.platform = None
            
        # C libraries for fast tile_alpha and tilde_psi calculation
        self._root_to_C_libraries = root_to_C_libraries
        self._getCL = GetCLibraries(root=self._root_to_C_libraries, 
                                    platform=self.platform)
    
        # Autoload: C libraries
        if not self.debug:
            self.model_ID = self.model.ID
            self.sm_ID = self._source_mapping.ID
        else:
            self.model_ID = 'none'
            self.sm_ID = 'none'
        
        try:
            alpha_C = self._getCL._integrand_alphatilde(None, self.model_ID, 
                                                        self.sm_ID)
            self._C_tildealpha_I1_comp_0 = alpha_C[0] 
            self._C_tildealpha_I1_comp_1 = alpha_C[1] 
            self._C_tildealpha_I3_comp_0 = alpha_C[2] 
            self._C_tildealpha_I3_comp_1 = alpha_C[3] 
            self._C_tildealpha_J1_comp_0 = alpha_C[4] 
            self._C_tildealpha_J1_comp_1 = alpha_C[5]   
            
            self._tildealpha_C_libraries_loaded = True
            
        except ValueError:
            self._tildealpha_C_libraries_loaded = False  
            
        try:
            psi_C = self._getCL._integrand_psitilde(None, self.model_ID, 
                                                      self.sm_ID)
            self._C_tildepsi_I1 = psi_C[0] 
            self._C_tildepsi_I2 = psi_C[1] 
            self._C_tildepsi_I3 = psi_C[2] 
            self._C_tildepsi_J1 = psi_C[3] 
            self._C_tildepsi_J2 = psi_C[4]
            
            self._tildepsi_C_libraries_loaded = True
            
        except ValueError:
            self._tildepsi_C_libraries_loaded = False

        #self._tildealpha_C_libraries_loaded = False
        #self._tildepsi_C_libraries_loaded = False

                    
    @property
    def args_0(self):
        return self._args_0                
        
    @args_0.setter
    def args_0(self, value):
        self._args_0 = value  

    @property
    def root_to_C_libraries(self):
        return self._root_to_C_libraries                
        
    @root_to_C_libraries.setter
    def root_to_C_libraries(self, value):
        self._root_to_C_libraries = value
        self._getCL = GetCLibraries(root=self._root_to_C_libraries)  

    @property
    def source_mapping(self):
        return self._source_mapping                
        
    @source_mapping.setter
    def source_mapping(self, value):
        self._source_mapping = value
        self._spt_args = HandlingContainer(self._source_mapping._f_args).flatten() 
        self._n1 = len(self._spt_args)
        self._all_args = tuple(self._model_args) + tuple(self._spt_args)
        
       
    @staticmethod   # Deprecated method  
    def norm(x): return (x[0]**2 + x[1]**2)**(0.5)
        
    def load_tilde_alpha_C_libraries(self, model_ID=None, 
                                     source_mapping_ID=None, filename=None, 
                                     verbose=False):
        """ 
        Load the C shared libraries used to compute the physically meaningful
        SPT-modified deflection angle $\tilde{\alpha}$.
        
        Parameters
        ----------
        filename : str
            Override the absolute path to a C shared library.
        model_ID : str
            The `Model`-ID corresponding to the lens model.
        source_mapping_ID : str
            The `SourceMapping`-ID corresponding to the source mapping.
        verbose: bool
            Display informations in the shell.        
        
        Returns
        -------
        None
        
        """        
#        model_ID:
#            NISG
#            NIEG
#            HERNgNFWG (Hernquist + generalized NFW + external shear)
#            
#        source_mapping_ID:
#            IS1
            
        # Check that the model_ID corresponds to the lens.ID
        if model_ID is None:
            model_ID = self.model_ID
        elif not self.debug:
            msg1 = 'The `model_ID` ({}) must correspond to the Model instance ID ({})'.format(model_ID,self.model_ID)
            assert model_ID == self.model_ID, msg1
        else:
            pass
        
        if source_mapping_ID is None:
            source_mapping_ID = self.sm_ID
        elif not self.debug:
            msg2 = 'The `source_mapping_ID` ({}) must correspond to the SourceMapping instance ID ({})'.format(source_mapping_ID,self.sm_ID)                        
            assert source_mapping_ID == self.sm_ID, msg2            
        else:
            pass
            
        # Load the C libraries
        library_C = self._getCL._integrand_alphatilde(filename, model_ID, source_mapping_ID)  

        if verbose: 
            print 'SUCCESSFULLY loaded the `IntegrandAlphaTilde_*_*.so` C libraries'          
        
        self._tildealpha_C_libraries_loaded = True  
        
        self._C_tildealpha_I1_comp_0 = library_C[0] 
        self._C_tildealpha_I1_comp_1 = library_C[1] 
        self._C_tildealpha_I3_comp_0 = library_C[2] 
        self._C_tildealpha_I3_comp_1 = library_C[3] 
        self._C_tildealpha_J1_comp_0 = library_C[4] 
        self._C_tildealpha_J1_comp_1 = library_C[5] 
       
        return None

    def load_tilde_psi_C_libraries(self, model_ID, source_mapping_ID, 
                                   filename=None, verbose=False):
        """
        Load the C shared libraries used to compute the physically meaningful
        SPT-modified deflection potnetial $\tilde{\psi}$.
        
        Parameters
        ----------
        model_ID : str
            The `Model`-ID corresponding to the lens model.
        source_mapping_ID : str
            The `SourceMapping`-ID corresponding to the source mapping.
        filename : str, optional
            Override the absolute path to a C shared library.            
        verbose: bool, optional
            If True, print some information.        
        
        Returns
        -------
        None        

        """ 
#        model_ID:
#            NISG
#            NIEG
#            HERNgNFWG (Hernquist + generalized NFW + external shear)            
#            
#        source_mapping_ID:
#            IS1    

        # Check that the model_ID corresponds to the lens.ID
        if model_ID is None:
            model_ID = self.model_ID
            source_mapping_ID = self.sm_ID
        elif not self.debug:
            msg1 = 'The `model_ID` ({}) must correspond to the Model instance ID ({})'.format(model_ID,self.model_ID)
            assert model_ID == self.model_ID, msg1
            
            msg2 = 'The `source_mapping_ID` ({}) must correspond to the SourceMapping instance ID ({})'.format(source_mapping_ID,self.sm_ID)                        
            assert source_mapping_ID == self.sm_ID, msg2
        else:
            pass
    
        library_C = self._getCL._integrand_psitilde(filename, model_ID, source_mapping_ID) 

        if verbose: 
            print 'SUCCESSFULLY loaded the `IntegrandPsiTilde_*_*.so` C libraries'           
        
        self._tildepsi_C_libraries_loaded = True  
        
        self._C_tildepsi_I1 = library_C[0] 
        self._C_tildepsi_I2 = library_C[1] 
        self._C_tildepsi_I3 = library_C[2] 
        self._C_tildepsi_J1 = library_C[3] 
        self._C_tildepsi_J2 = library_C[4]  
       
        return None        
    
    def load_C_libraries(self, model_ID=None, sm_ID=None, verbose=False):
        """
        Load the C shared libraries used to compute the physically meaningful
        SPT-modified deflection potnetial $\tilde{\psi}$ and SPT-modified 
        deflection angle $\tilde{\alpha}$.
        
        Parameters
        ----------
        model_ID : str
            The `Model`-ID corresponding to the lens model.
        sm_ID : str
            The `SourceMapping`-ID corresponding to the source mapping.
        verbose: bool
            Display informations in the shell.        
        
        Returns
        -------
        None   
        
        """
        # TODO: add a debug mode where no model_ID or sm_ID is required
        
        self.load_tilde_alpha_C_libraries(model_ID=model_ID,
                                          source_mapping_ID=sm_ID,
                                          verbose=verbose)
        
        self.load_tilde_psi_C_libraries(model_ID=model_ID,
                                          source_mapping_ID=sm_ID,
                                          verbose=verbose)
        
        return None
        
    def original_source_position(self, (theta1, theta2)):
        """ 
        Give the unmodified source position corresponding to a passed position 
        in the lens plane.
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
        
        Returns
        -------
        beta : ndarray
            The two components of the source position.
            
        """
        a = self.alpha_0((theta1, theta2), self._args_0)
        return array([theta1 - a[0], theta2 - a[1]])

    def modified_source_position(self, (theta1, theta2)):
        """
        Give the SPT-modified source position corresponding to a passed 
        position in the lens plane.
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
        
        Returns
        -------
        hatbeta : ndarray
            The two components of the SPT-modified source position.
            
        """
        beta12 = self.original_source_position((theta1, theta2))
        return self._source_mapping.modified_source_position(beta12)            
        
    def modified_source_position_generator(self, theta1, theta2):
        """
        Generator that yields the SPT-modified source position corresponding 
        to a set of positions in the lens plane.
        
        Parameters
        ----------
        theta1: array_like
            First component of the image positions.
        theta2: array_like
            Second component of the image positions.            
        
        Returns
        -------
        res : generator
            Generator that yields the SPT-modified source positions.
            
        """
        for k in izip(theta1, theta2):
            beta12 = self.original_source_position(k)
            yield self._source_mapping.modified_source_position(beta12)        
            
    def modified_alpha(self, *args):
        """ Give the SPT-modified deflection angle.
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
            
        Returns
        -------
        hatalpha : 1x2 ndarray
            The SPT-modified deflection angle $\hat{\alpha}$.
            
        """
        if len(args) == 2:
            return self._modified_alpha(args[0], args[1])
        elif len(args) == 1 and isiterable(args):        
            return self._modified_alpha(args[0][0], args[0][1])    
        else:
            raise TypeError('modified_alpha() takes exactly 2 arguments ({} given)'.format(len(args)))
        
    def _modified_alpha(self, theta1, theta2):
        res = empty(2)
        hat_beta_12 = self.modified_source_position((theta1, theta2))                       
        res[0] = theta1 - hat_beta_12[0]
        res[1] = theta2 - hat_beta_12[1]
        return res 

    def modified_jacobi_matrix_diag(self, (theta1, theta2)):
        """ 
        Give the diagonal elements of the SPT-modified Jacobi matrix of the 
        lens mapping.
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
            
        Returns
        -------
        hatjm : 2x2 ndarray
            The diagonal of the SPT-modified Jacobi matrix $\hat{\mathcal{A}}$. 
            
        """
        res = empty([2,2])
        beta1, beta2 = self.original_source_position((theta1, theta2))
        B = self._source_mapping.jacobi_matrix_spt_mapping((beta1, beta2))
        A = self.jm_alpha_0((theta1, theta2), self._args_0)
        res[0,0] = B[0][0]*(1-A[0,0]) + B[0][1]*(-A[1,0])
        res[1,1] = B[1][0]*(-A[0,1]) + B[1][1]*(1-A[1,1])
        res[0,1] = 0.
        res[1,0] = 0.
        return res 

    def modified_jacobi_matrix_antidiag(self, (theta1, theta2)):
        """
        Give the antidiagonal elements of the SPT-modified Jacobi matrix of 
        the lens mapping.
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
            
        Returns
        -------
        hatjm : 2x2 ndarray
            The antidiagonal of the SPT-modified Jacobi matrix 
            $\hat{\mathcal{A}}$. 
            
        """
        condition_1 = self._source_mapping.jacobi_matrix_spt_mapping is not None
        condition_2 = self.jm_alpha_0 is not None
        
        if condition_1 and condition_2:
            beta1, beta2 = self.original_source_position((theta1, theta2))
            B = self._source_mapping.jacobi_matrix_spt_mapping((beta1, beta2))
            A = self.jm_alpha_0((theta1, theta2), self._args_0)
            temp0 = B[0][0]*(-A[0,1]) + B[0][1]*(1-A[1,1])
            temp1 = B[1][0]*(1-A[0,0]) + B[1][1]*(-A[1,0])
            return array([[0.,temp0],[temp1,0.]])
        else:
            print 'UNDER CONSTRUCTION'
            print 'Require numerical derivation'
            return  0.              

    def modified_jacobi_matrix(self, (theta1, theta2)):
        """
        Give the SPT-modified Jacobi matrix of the lens mapping.
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
            
        Returns
        -------
        hatjm : 2x2 ndarray
            The SPT-modified Jacobi matrix $\hat{\mathcal{A}}$.  
            
        """
        condition_1 = self._source_mapping.jacobi_matrix_spt_mapping is not None
        condition_2 = self.jm_alpha_0 is not None
        
        if condition_1 and condition_2: 
            res = empty([2,2])
            beta1, beta2 = self.original_source_position((theta1, theta2))
            B = self._source_mapping.jacobi_matrix_spt_mapping((beta1, beta2))
            A = self.jm_alpha_0((theta1, theta2), self._args_0)
            res[0,0] = B[0][0]*(1-A[0,0]) + B[0][1]*(-A[1,0])
            res[1,1] = B[1][0]*(-A[0,1]) + B[1][1]*(1-A[1,1])            
            res[0,1] = B[0][0]*(-A[0,1]) + B[0][1]*(1-A[1,1])
            res[1,0] = B[1][0]*(1-A[0,0]) + B[1][1]*(-A[1,0])                        
            return res
            #return dot(B,identity(2)-A)
            
    def is_matrix_symmetric(self, M):
        """ THIS METHOD WILL BE MOVE IN THE SUBPACKAGE pySPT.tools
        
        Verify whether the matrix M is symmetric or not.
        
        Parameters
        ----------
        M : ndarray
            Matrix to check.
            
        Returns
        -------
        issym : bool
            True if M is symmetric
            
        """
        return (M.transpose(1,0) == M).all()          
            
    def eigen(self, (theta1, theta2)):
        """
        Return the eigenvalues and associated eigenvectors of both the Jacobi 
        matrix of the source mapping and the original lens mapping.
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
            
        Returns
        -------
        res : tuple
            res[0] --> eigenvalues/vectors of the source mapping
            res[1] --> eigenvalues/vectors of the lens mapping
            
        """
        eig_lens = self.model.eigen((theta1, theta2), self._args_0)
        
        beta1, beta2 = self.original_source_position((theta1, theta2))
        eig_SPT = self._source_mapping.eigen((beta1, beta2))
        
        return (eig_SPT, eig_lens)            

    def modified_kappa_axisym(self, (theta1,theta2)):
        """
        Give the SPT-modified surface mass density for the particular case of
        an axisymmetric lens and an isotropic stretching characterized by 
        the deformation function f.
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
            
        Returns
        -------
        hatkappa : float
            The SPT-modified surface mass density.
            
        Notes
        -----
        This method is valid only axisymmetric lens models modified by a 
        radial stretching. For other type of SPT, one should use 
        `modified_kappa()`, even for axisymmetric lens models.
        
        """            
        theta = norm_fast((theta1, theta2))
        alpha = norm_fast(self.alpha_0((theta1, theta2), self._args_0))
        kappa = self.kappa_0((theta1, theta2), self._args_0)
        D_alpha = 2*kappa - alpha/theta
        
        T1 = kappa - (1-kappa) * self._source_mapping.f((theta-alpha,0.), self._source_mapping._f_args) #f((theta-alpha,0.), p_spt)
        T2 = theta*0.5 * (1 - alpha/theta) * (1-D_alpha) * self._source_mapping.derivative_f((theta-alpha,0.), self._source_mapping._f_args)[0]
        return T1-T2


    def modified_kappa(self, theta1, theta2, axi_sym=False):
        """ Give the SPT-modified surface mass density.
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
            
        Returns
        -------
        hatkappa : float
            The SPT-modified surface mass density.  
        axi_sym : bool, optional
            If True, call `modified_kappa_axisym()`.
              
        Notes
        -----
        Implement the Eq.(30) in Schneider & Sluse (2014), which is the most 
        general expression for $\hat{\kappa}$.
        
        """ 
        if isiterable(theta1):
            theta1, theta2 = theta1                      
            
        diag_JM = self.modified_jacobi_matrix_diag((theta1, theta2))                   
        return 1 - 0.5 * (diag_JM[0,0]+diag_JM[1,1]) #trace(diag_JM) #
    
    def modified_surface_mass_density(self, pos, axisym=False):
        """ Give the SPT-modified surface mass density.
        
        Parameters
        ----------
        pos : array_like
            Components of a position in the lens plane. `pos` can also be a 
            Nx2 ndarray defining N image positions.
            
        Returns
        -------
        hatkappa : float
            The SPT-modified surface mass density.  
        axi_sym : bool, optional
            If True, call `modified_kappa_axisym()`.
              
        Notes
        -----
        Implement the Eq.(30) in Schneider & Sluse (2014), which is the most 
        general expression for $\hat{\kappa}$.
        
        """
        if not isiterable(pos):
            # Axi-sym case:
            # One position where only the radial coordinate is given.
            return self.modified_kappa(theta1=pos, theta2=0.0)
        elif (isiterable(pos) and all([not isiterable(_pos) for _pos in pos])
                and axisym):
            # Axi-sym case:
            # List of positions where only the radial coordinates are given.
            return array([self.modified_kappa(theta1=_pos, theta2=0.0) 
                              for _pos in pos])
        elif (isiterable(pos) and all([not isiterable(_pos) for _pos in pos])
                and len(pos)>2):   
            # Axi-sym case:
            # List of positions where only the radial coordinates are given
            # but for which the use forgot to pass axisym=True.
            return array([self.modified_kappa(theta1=_pos, theta2=0.0) 
                              for _pos in pos])            
        elif isiterable(pos) and all([isiterable(_pos) for _pos in pos]):
            # List of positions.
            return array([self.modified_kappa(*_pos) for _pos in pos])

        else:
            # One position
            return self.modified_kappa(*pos)
            
    def modified_psi_axisym(self, (theta1,theta2), lowerBound=0.):
        """ 
        Compute hatpsi by solving the equation grad(hatpsi) = hatalpha.
        
        If the unmodified deflection angle alpha is axisymmetric or if alpha
        is modified under a pure MST, the SPT-modified hatalpha is a curl-free 
        field. Hence the quantity hatpsi which satisfies the equation 
        grad(hatpsi) = hatalpha corresponds to the SPT-modified deflection
        potential. Otherwise, hatpsi is not related to the deflection 
        potential produced by the mass distribution characterized by hatkappa.
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
            
        Returns
        -------
        hatpsi : float
            The SPT-modified deflection potential which satisfies the equation
            grad(hatpsi) = hatalpha.
        
        Notes
        -----
        hatpsi is given up to a constant.
        
        """
        theta = norm_fast((theta1, theta2))
        def wrapper(x): 
            return norm_fast(self.modified_alpha(x,0.))
        I = quad(wrapper, lowerBound, theta)
        return I[0]           
            
    def _modified_alpha_dot_n(self, (theta1, theta2)):
        """
        Dot product between the modified deflection angle at the position 
        (theta1, theta2) and the normal vector to the circle passing by 
        (theta1, theta2). 
        
        """
        a = self.modified_alpha(theta1, theta2)
        theta = (theta1**2 + theta2**2)**(0.5)
        return a[0]*(theta1/theta) + a[1]*(theta2/theta)
        
    def _integrand_J(self, varphi, func, R):
        dotprod = self._modified_alpha_dot_n((R*cos(varphi), R*sin(varphi))) 
        return dotprod * func(R, varphi)
        
    def _integrand_I(self, r, varphi, func):        
        hat_kappa = self.modified_kappa(r*cos(varphi), r*sin(varphi))
        return r * func(r, varphi) * hat_kappa 

    def _integrand_I_cm(self, x, delta, cm_object, func):
        jacobian_radial = x
        jacobian_cm = cm_object._jacobian(x, delta)        
        hat_kappa_cm = cm_object._cm_func(x, delta, self.modified_kappa, input_format='cartesian')
        func_cm = cm_object._cm_func(x, delta, func)        
        return jacobian_radial * jacobian_cm * hat_kappa_cm * func_cm        

    @timeit
    def tilde_alpha(self, (theta1, theta2), R=None, debug=False, *args, **kwargs):
        """ 
        Give tildealpha, the closest curl-free approximation to the 
        SPT-modified deflection angle hatalpha
        
        The vectorial quantity tildealpha satisfies the criterion
        |tildealpha - hatalpha| < epsilon_acc ,
        over a region of the lens plane, and where epsilon_acc corresponds to 
        the current astrometric accuracy. The explicit expression for 
        tildealpha is given at Eq.(22) in Unruh, Schneider & Sluse (2017).
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
        R : float
            The radius of the circular finite region $\mathcal{U}$ of 
            integration (see Eq.(22) in Unruh, Schneider & Sluse, 2017).
        debug : bool, optional
            If True, print some intermediate result.            
        
        Returns
        -------
        tildealpha : ndarray, 1d
            The closest curl-free approximation to the SPT-modified 
            deflection angle hatalpha.
        
        Notes
        -----
        This method is a pure python implementation of Eq.(22) in 
        Unruh, Schneider & Sluse (2017), and is rather slow. An optimized 
        version of this method, using C shared libraries, is given by
        `tilde_alpha_fast()`.

        """
#        UNDER CONSTRUCTION (but it works already)
#        
#        + (theta1, theta2) corresponds to (ctheta1, ctheta2) defined in the
#          previous version. It's the position at which tilde_alpha is evaluated
#          but NOT the integration variables.
#        
#        We should account for:
#        (1) J1 = J3
#        (2) If axi-symmetric, tilde_alpha = hat_alpha ==> just call the method
#            self.modified_alpha()
#        (3) If (theta1, theta2) is very close to R, one might use a conformal
#            mapping for I3 as well ...
#        (4) I2 = J2 
       
        t_start = time()
        theta = norm_fast((theta1, theta2))
        
        if R is None:
            R = 1.45*theta
            
        assert (theta < R), 'The circular area of integration should include '\
                             '(theta1, theta2). Consider increasing the ' \
                             'radius R > {:.3f}'.format(theta)
        
        ct, phi = (theta1**2 + theta2**2)**(0.5), arctan2(theta2, theta1)
        ggf = GradientGreenFunction(ct, phi, R)
        #cm_object = ConformalMapping(theta1, theta2, R)
        
        ########################## I integration
        bound_lower = lambda x: 0.
        bound_upper = lambda x: R
        bound_upper_cm = lambda x: 1.
        
        if debug:
            print 'pre-', time() - t_start                    
            print 'kwargs', kwargs
        
        #t_start = time.time()
        #i1_0 = dblquad(self._integrand_I_cm, 0., 2.*pi, bound_lower, bound_upper_cm,
        #               args=(cm_object,ggf.grad_gf_1_comp_0,), *args, **kwargs)#epsrel=kwargs.get('eps', 1.49e-8), epsabs=kwargs.get('eps', 1.49e-8)) 
        #print 'Duration i1_0', time.time() - t_start                           
        #print i1_0
        # ---------------------------------------------------------------------
          
        def _integrand_alt_0(x, delta):
            x1 = x*cos(delta)
            x2 = x*sin(delta)            
            theta_sq = theta1**2 + theta2**2  
            dot_theta_x = (theta1*x1 + theta2*x2)
            
            p1 = R**2 * (theta_sq - R**2)
            p2 = R*cos(delta)/x + theta1
            p3 = (R**2 + 2*R*dot_theta_x + theta_sq * x**2)**2            
            k1 = p1*p2/p3
            
            denomi = 1 + 2*dot_theta_x/R + theta_sq*x**2/R**2
            xt1 = (R*x1 + theta1*(1+x**2) + (x1*(theta1**2-theta2**2) + 2*theta1*theta2*x2)/R) / denomi
            xt2 = (R*x2 + theta2*(1+x**2) + (-x2*(theta1**2-theta2**2) + 2*theta1*theta2*x1)/R) / denomi
            hat_kappa_cm = self.modified_kappa(xt1, xt2)
            
            return x * k1 * hat_kappa_cm
        t_start = time() 
        i1_0 = dblquad(_integrand_alt_0, 0., 2.*pi, bound_lower, bound_upper_cm,
                       args=(), *args, **kwargs)
        if debug: 
            print 'test: ', _integrand_alt_0((0.05**2 + 0.02**2)**(0.5), arctan2(0.02,0.05))
            print 'Duration i1_0 (new)', time() - t_start,  'Value: ', i1_0[0]/pi
        # ---------------------------------------------------------------------
        
        t_start = time()                       
        i3_0 = dblquad(self._integrand_I, 0., 2.*pi, bound_lower, bound_upper,
                       args=(ggf.grad_gf_3_comp_0,), *args, **kwargs)#epsrel=kwargs.get('eps', 1.49e-8), epsabs=kwargs.get('eps', 1.49e-8))  
        if debug:        
            print 'Duration i3_0', time() - t_start, 'Value: ', i3_0[0]/pi                            
   
        i_0_components = (1./pi) * array([i1_0[0], i3_0[0]])
        
#        t_start = time.time()
#        i1_1 = dblquad(self._integrand_I_cm, 0., 2.*pi, bound_lower, bound_upper_cm,
#                       args=(cm_object,ggf.grad_gf_1_comp_1,), *args, **kwargs)#epsrel=kwargs.get('eps', 1.49e-8), epsabs=kwargs.get('eps', 1.49e-8))  
#        print 'Duration i1_1', time.time() - t_start  
#        print i1_1  
        # ---------------------------------------------------------------------        
        t_start = time()        
        def _integrand_alt_1(x, delta):
            x1 = x*cos(delta)
            x2 = x*sin(delta)            
            theta_sq = theta1**2 + theta2**2  
            dot_theta_x = (theta1*x1 + theta2*x2)
            
            p1 = R**2 * (theta_sq - R**2)
            p2 = R*sin(delta)/x + theta2
            p3 = (R**2 + 2*R*dot_theta_x + theta_sq * x**2)**2            
            k1 = p1*p2/p3
            
            denomi = 1 + 2*dot_theta_x/R + theta_sq*x**2/R**2
            xt1 = (R*x1 + theta1*(1+x**2) + (x1*(theta1**2-theta2**2) + 2*theta1*theta2*x2)/R) / denomi
            xt2 = (R*x2 + theta2*(1+x**2) + (-x2*(theta1**2-theta2**2) + 2*theta1*theta2*x1)/R) / denomi
            hat_kappa_cm = self.modified_kappa(xt1, xt2)            
            
            return x * k1 * hat_kappa_cm   

        i1_1 = dblquad(_integrand_alt_1, 0., 2.*pi, bound_lower, bound_upper_cm,
                       args=(), *args, **kwargs) 
        if debug:        
            print 'Duration i1_1 (new)', time() - t_start, 'Value: ', i1_1[0]/pi                       
        #print i1_1_alt
        # ---------------------------------------------------------------------                   

        t_start = time()                       
        i3_1 = dblquad(self._integrand_I, 0., 2.*pi, bound_lower, bound_upper,
                       args=(ggf.grad_gf_3_comp_1,), *args, **kwargs)#epsrel=kwargs.get('eps', 1.49e-8), epsabs=kwargs.get('eps', 1.49e-8))
        if debug:
            print 'Duration i3_1', time() - t_start, 'Value: ', i3_1[0]/pi                     
    
        i_1_components = (1./pi) * array([i1_1[0], i3_1[0]]) 

        ####################### J integration         
        t_start = time()                
        j1_0 = quad(self._integrand_J, 0., 2.*pi, args=(ggf.grad_gf_1_comp_0,R,))
        if debug:
            print 'Duration j1_0', time() - t_start, 'Value: ', j1_0[0]*R/(2.*pi)
        
        #print '_integrand_J = ', self._integrand_J(0.49, ggf.grad_gf_1_comp_0, R)*R
        
        j_0_components = R/(2.*pi) * array([j1_0[0], j1_0[0]])
        
        t_start = time()
        j1_1 = quad(self._integrand_J, 0., 2.*pi, args=(ggf.grad_gf_1_comp_1,R,))
        if debug:
            print 'Duration j1_1', time() - t_start, 'Value: ', j1_1[0]*R/(2.*pi)           
        
        j_1_components = R/(2.*pi) * array([j1_1[0], j1_1[0]])

        # Results        
        tilde_alpha_0 = i_0_components.sum() - j_0_components.sum()           
        tilde_alpha_1 = i_1_components.sum() - j_1_components.sum()

        if debug:        
            print 'i_0', i_0_components
            print 'i_1', i_1_components
            print 'j_0', j_0_components
            print 'j_1', j_1_components
        
        
        return array([tilde_alpha_0, tilde_alpha_1])

    
    def tilde_alpha_generator(self, theta1, theta2, R):  
        """
        Exemple
        -------
        t1 = np.random.uniform(-0.2,0.2,1)
        t2 = np.random.uniform(-0.2,0.2,1)
        Radius = [1.3*(_1**2+_2**2)**(0.5) for _1,_2 in zip(t1,t2)]
        w = spt.tilde_alpha_generator(t1,t2,Radius)
        """
        for t1, t2, radius in izip(theta1, theta2, R):
            yield self.tilde_alpha((t1, t2), radius)
            
    def _nquad_C_integral(self, _C_func, theta1, theta2, R, epsrel,
                          (phkr_0, phkr_1), (phkp_0, phkp_1), _C_func_args,
                          opts=None, debug=False):
        """
        """
        opts_ref = [{'epsrel':epsrel, 'limit':500, 'points':[]},
                    {'epsrel':epsrel, 'limit':500, 'points':[]}]        
        
        if opts is None:
            opts = opts_ref
        else:
            opts = [HandlingDict(_opt).updateDict(_opt_ref) for _opt, _opt_ref in zip(opts,opts_ref)]
            print opts

        
        I = nquad(_C_func, [[phkr_0, phkr_1], [phkp_0, phkp_1]], args=_C_func_args,
                     opts = opts, full_output=True)   
        
        if debug:
            print '    + error       = {}'.format(I[1])
            print '    + N func eval = {}'.format(I[2])            
            
        return I
    

        
    @timeit    
    def tilde_alpha_fast(self, theta1, theta2, R, epsrel= 1.0e-05, 
                         peak_position=None, debug=False, subIntegral=None):
        """
        Give tildealpha, the closest curl-free approximation to the 
        SPT-modified deflection angle hatalpha
        
        The vectorial quantity tildealpha satisfies the criterion
        |tildealpha - hatalpha| < epsilon_acc ,
        over a region of the lens plane, and where epsilon_acc corresponds to 
        the current astrometric accuracy. The explicit expression for 
        tildealpha is given at Eq.(22) in Unruh, Schneider & Sluse (2017).
        
        Parameters
        ----------
        theta1, theta2 : float
            Components of a position in the lens plane.
        R : float
            The radius of the circular finite region $\mathcal{U}$ of 
            integration (see Eq.(22) in Unruh, Schneider & Sluse, 2017).
        epsrel : float
            The absolute precision on tildealpha.
        peak_position : tuple
            Position, in the CM-plane, of the peak corresponding to the central
            part of the modified mass distribution hat_kappa. In the lens 
            plane, this peak is located at (0,0). In complex notation, the peak
            position is then located at x = - (theta1 + 1j * theta2) / R.            
        debug : bool, optional
            If True, print some intermediate result.   
        subIntegral : list of 6 bool, optional
            The main integral is composed of 3 subintegrals per component. 
            If subIntegral[j] is False, the j-th subintegrals is ignored, 
            where j \in (0,1,2,3,4,5).
        
        Returns
        -------
        tildealpha : ndarray, 1d
            The closest curl-free approximation to the SPT-modified 
            deflection angle hatalpha.
        
        Notes
        -----
        This method makes use of C shared libraries and has been optimized.
        A pure Python implemented version if given by `tilde_alpha()`.

        """   
        if subIntegral is None:
            subIntegral = [True for _ in range(6)]
        else:
            assert isinstance(subIntegral,list), '`subIntegral` must be a list'
            assert len(subIntegral) == 6, '`subIntegral` must be of length 6'
            
        if not self._tildealpha_C_libraries_loaded:
            print 'No C libraries found.'
            print 'Load the C libraries first by calling the method ``load_tilde_alpha_C_libraries(**kwargs)``'
            return None
 
        if peak_position is None:
            peak_position = ConformalMapping(theta1, theta2, R)._original_to_cm(0.,0., coord='polar')

        if debug:
            print '-- Conformal mapping --'
            print '    peak position = ({:.4f},{:.4f})'.format(peak_position[0],
                                                               peak_position[1])
            print ''
            
        #check_bounds = _CheckBounds(peak_position)      
        r_bounds, phi_bounds = _CheckBounds(peak_position)() #check_bounds()
        
        if debug:
            print '-- Bounds --'
            print '    r bounds'
            for k,_rbds in enumerate(r_bounds):
                print '    {}: ({:.4f},{:.4f})'.format(k, _rbds[0], _rbds[1])
            print '    phi bounds'
            for k,_pbds in enumerate(phi_bounds):
                print '    {}: ({:.4f},{:.4f})'.format(k, _pbds[0], _pbds[1])            
            print ''
                            
        func_args = (theta1, theta2, R, self._n0, self._n1) + self._all_args

        #_opts = [None, [{'points':[peak_position[0]]},{'points':[peak_position[1]]}], 
        #         None, None]
        _opts = [None for _ in range(len(r_bounds))]
        
        # I1 component 0
        if debug: print '-- I1 --'
        
        I1_comp_0 = 0.
        if subIntegral[0]:     
            for k, (br, bp, opts) in enumerate(izip(r_bounds, phi_bounds, _opts)):
                I = self._nquad_C_integral(self._C_tildealpha_I1_comp_0, 
                                           theta1, theta2, R, epsrel, br, bp,
                                           func_args, debug=debug, opts=opts)
                if debug:
                    print '   I1 comp 0 sub = {:.12f}'.format(I[0])
                I1_comp_0 += I[0]
            if debug:
                print 'I1 comp 0 = {:.12f}'.format(I1_comp_0)
                print ''
                
        # I1 component 1
        I1_comp_1 = 0.        
        if subIntegral[1]:
            for k, (br, bp) in enumerate(izip(r_bounds, phi_bounds)):
                I = self._nquad_C_integral(self._C_tildealpha_I1_comp_1, 
                                          theta1, theta2, R, epsrel, br, bp,
                                          func_args, debug=debug)
                if debug:
                    print '   I1 comp 1 sub = {:.12f}'.format(I[0])            
                I1_comp_1 += I[0]    
            if debug:
                print 'I1 comp 1 = {:.12f}'.format(I1_comp_1)
                print '\n'
                    
        # I3 component 0
        if debug: print '-- I3 --'   
        
        I3_comp_0 = 0.        
        if subIntegral[2]:
            I = self._nquad_C_integral(self._C_tildealpha_I3_comp_0, 
                                       theta1, theta2, R, epsrel, 
                                       (0.,R), (0., 2.*pi),
                                       func_args, debug=debug)
            I3_comp_0 += I[0]
            if debug:
                print 'I3 comp 0 = {:.12f}'.format(I3_comp_0) 
                print ''
            
        # I3 component 1
        I3_comp_1 = 0.
        if subIntegral[3]:
            I = self._nquad_C_integral(self._C_tildealpha_I3_comp_1, 
                                       theta1, theta2, R, epsrel, 
                                       (0.,R), (0., 2.*pi),
                                       func_args, debug=debug)
            I3_comp_1 += I[0] 
            if debug:
                print 'I3 comp 1 = {:.12f}'.format(I3_comp_1)
                print '\n'
            
        # J1 component 0
        if debug: print '-- J1 --' 
        
        if subIntegral[4]:
            J1_0 = nquad(self._C_tildealpha_J1_comp_0, [[0., 2.*pi]], 
                        args= func_args,
                        opts = {'epsrel':epsrel}, full_output=True)  
                 
            if debug:
                print '    + error       = {}'.format(J1_0[1])
                print '    + N func eval = {}'.format(J1_0[2])              
                print 'J1 comp 0 = {:.12f}'.format(J1_0[0])
                print ''
        else:
            J1_0 = [0.0]
            
        # J1 component 1
        if subIntegral[5]:
            J1_1 = nquad(self._C_tildealpha_J1_comp_1, [[0., 2.*pi]], 
                         args=func_args,
                         opts = {'epsrel':epsrel}, full_output=True)                                                        
            if debug:
                print '    + error       = {}'.format(J1_1[1])
                print '    + N func eval = {}'.format(J1_1[2])              
                print 'J1 comp 1 = {:.12f}'.format(J1_1[0])        
                print ''
        else:
            J1_1 = [0.0]
            
            
        return array([I1_comp_0+I3_comp_0-2.*J1_0[0], I1_comp_1+I3_comp_1-2.*J1_1[0]])   

    def test(self, x, R=1):
        return x[0]*x[1]+R

    def _wrapper_tilde_alpha(self, x, **kwargs):
        return self.tilde_alpha_fast(x[0], x[1], **kwargs)
    
    def modified_cf_alpha(self, pos, R, *args, **kwargs):
        """
        """
        return self.tilde_alpha_fast(pos[0], pos[1], R, *args,**kwargs)
    
    @timeit            
    def tilde_alpha_fast_sequence(self, sequence, R, epsrel= 1.49e-06, 
                                  peak_position=None, ncpu=1, chunks=False,
                                  size_chunks=None, profile=False, debug=False, 
                                  **kwargs):
        """
        TODO: sequence should be either a list or an iterator.
        TODO: the Multiprocessing and run have been updated with more features. 
              One should able to pass new args and kwargs.
        """
        if not self._tildealpha_C_libraries_loaded:
            print 'No C libraries found.'
            print 'Load the C libraries first by calling the method ``load_tilde_alpha_C_libraries(**kwargs)``'
            return None                        
        
        kwargs = {'R':R, 'epsrel':epsrel, 'peak_position':peak_position}

        #res = self.parmap(partial(self._wrapper_tilde_alpha, **kwargs), sequence, nprocs=ncpu)
        
        #z = Multiprocessing(partial(self._wrapper_tilde_alpha, **kwargs), sequence)
        z = Multiprocessing(self._wrapper_tilde_alpha, sequence, kwargs)
        res = z.run(nprocs=ncpu, profile=profile, chunks=chunks, 
                    size_chunks=size_chunks, debug=debug)
                     
        return array(res)
    
    @timeit
    def tilde_psi(self, (theta1, theta2), R, debug=False, **kwargs):
        """
        Give tildepsi that satisfies grad(tildepsi) = tildealpha, where 
        tildealpha is the closest curl-free approximation to the SPT-modified 
        deflection angle hatalpha
        
        The explicit expression for tildepsi is given at Eq.(18) in 
        Unruh, Schneider & Sluse (2017).
        
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of a position in the lens plane.
        R : float
            The radius of the circular finite region $\mathcal{U}$ of 
            integration (see Eq.(22) in Unruh, Schneider & Sluse, 2017).
        debug : bool, optional
            If True, print some intermediate result.            
        
        Returns
        -------
        tildealpha : ndarray, 1d
            The closest curl-free approximation to the SPT-modified 
            deflection angle hatalpha.
        
        Notes
        -----
        This method is a pure python implementation of Eq.(18) in 
        Unruh, Schneider & Sluse (2017), and is rather slow. An optimized 
        version of this method, using C shared libraries, is given by
        `tilde_psi_fast()`.        
        """
        ct, phi = (theta1**2 + theta2**2)**(0.5), arctan2(theta2, theta1)        
        gf = GreenFunction(ct, phi, R)
        
        bound_lower = lambda x: 0.
        bound_upper = lambda x: R
        bound_upper_cm = lambda x: 1.  
        
        cm_object = ConformalMapping(theta1, theta2, R)
        
        # I integration
        I1 = dblquad(self._integrand_I_cm, 0., 2.*pi, bound_lower, bound_upper_cm,
                       args=(cm_object,gf.gf_1,))                           
        if debug:
            print 'I1 = {:.12f}'.format(2.*I1[0])        
                     
        I2 = dblquad(self._integrand_I, 0., 2.*pi, bound_lower, bound_upper,
                       args=(gf.gf_2,), **kwargs) 
        if debug:
            print 'I2 = {:.12f}'.format(2.*I2[0])            
               
        I3 = dblquad(self._integrand_I, 0., 2.*pi, bound_lower, bound_upper,
                       args=(gf.gf_3,), **kwargs)                           
        if debug:
            print 'I3 = {:.12f}'.format(2.*I3[0])        
           
        # J integration                       
        J1 = quad(self._integrand_J, 0., 2.*pi, args=(gf.gf_1,R,))
        if debug:
            print 'J1 = {:.12f}'.format(R*J1[0])        

        J2 = quad(self._integrand_J, 0., 2.*pi, args=(gf.gf_2,R,))
        if debug:
            print 'J2 = {:.12f}'.format(R*J2[0])        
           
        J3 = quad(self._integrand_J, 0., 2.*pi, args=(gf.gf_3,R,))
        if debug:
            print 'J3 = {:.12f}'.format(R*J3[0])        
                
        return 2. * (I1[0] + I2[0] + I3[0]) - R * (J1[0] + J2[0] + J3[0])
        
    @timeit    
    def tilde_psi_fast(self, theta1, theta2, R, epsrel= 1.49e-04, debug=False):
        """
        Give tildepsi that satisfies grad(tildepsi) = tildealpha, where 
        tildealpha is the closest curl-free approximation to the SPT-modified 
        deflection angle hatalpha
        
        The explicit expression for tildepsi is given at Eq.(18) in 
        Unruh, Schneider & Sluse (2017).
        
        Parameters
        ----------
        theta1, theta2 : float
            Components of a position in the lens plane.
        R : float
            The radius of the circular finite region $\mathcal{U}$ of 
            integration (see Eq.(18) in Unruh, Schneider & Sluse, 2017).
        epsrel : float
            The absolute precision on tildepsi.           
        debug : bool, optional
            If True, print some intermediate result.
        
        Returns
        -------
        tildepsi : float
            The physically meaningful SPT-modified deflection potential.
        
        Notes
        -----
        This method makes use of C shared libraries and has been optimized.
        A pure Python implemented version if given by `tilde_psi()`.  
        
        """   
        if not self._tildepsi_C_libraries_loaded:
            print 'No C libraries found.'
            print 'Load the C libraries first by calling the method ``load_tilde_psi_C_libraries(**kwargs)``'
            return None
        
        func_args = (theta1, theta2, R, self._n0, self._n1) + self._all_args 

        # I        
        I1 = self._nquad_C_integral(self._C_tildepsi_I1, 
                                    theta1, theta2, R, epsrel, 
                                    (0., 1.), (0., 2.*pi), 
                                    func_args)
        if debug:
            print 'I1 = {:.12f}'.format(2.*I1[0])
        
        I2 = self._nquad_C_integral(self._C_tildepsi_I2, 
                                    theta1, theta2, R, epsrel, 
                                    (0., R), (0., 2.*pi), 
                                    func_args)
        if debug:
            print 'I2 = {:.12f}'.format(2.*I2[0])

        
        I3 = self._nquad_C_integral(self._C_tildepsi_I3, 
                                    theta1, theta2, R, epsrel, 
                                    (0., R), (0., 2.*pi), 
                                    func_args)

        if debug:
            print 'I3 = {:.12f}'.format(2.*I3[0])

        J1 = nquad(self._C_tildepsi_J1, [[0., 2.*pi]], 
                    args= func_args,
                    opts = {'epsrel':epsrel}, full_output=False) 
        if debug:
            print 'J1 = {:.12f}'.format(J1[0])

        J2 = nquad(self._C_tildepsi_J2, [[0., 2.*pi]], 
                    args= func_args,
                    opts = {'epsrel':epsrel}, full_output=False) 
        if debug:
            print 'J2 = {:.12f}'.format(J2[0])
        
        return 2. * (I1[0] + I2[0] + I3[0]) - (2.0*J1[0] + J2[0])
        
        
    def SDF(self, (theta1,theta2), (hatbeta1,hatbeta2), R, epsrel=1.49e-04):
        """ Compute the SPT-modified Squared Deviation Function (SDF)
        
        The SDF has been introduced by Schramm, T. & Kayser, R, 1987, A&A 174, 
        361-364. The SPT-modified SDF computed here corresponds to
        
        SDF1 = hatbeta1 - theta1 + tildealpha(theta1,theta2)[1] ,
        SDF2 = hatbeta2 - theta2 + tildealpha(theta1,theta2)[2] ,
        
        and finally
        
        SDF = (SDF1**2 + SDF2**2)**0.5
            
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of an image position.
        (hatbeta1, hatbeta2) : array_like
            Components of the source position at the origin of the image.
        R : float
            The radius of the circular finite region $\mathcal{U}$ of 
            integration.
        epsrel : float
            The absolute precision on tildealpha.

        Returns
        -------
        sdf : float
            The SPT-modified SDF function.             
            
        """
        tilde_alpha = self.tilde_alpha_fast(theta1, theta2, R, epsrel=epsrel)
        SDF0 = hatbeta1 + tilde_alpha[0] - theta1
        SDF1 = hatbeta2 + tilde_alpha[1] - theta2
        return (SDF0**2 + SDF1**2)**(0.5)
    
    def modified_SDF(self, (theta1,theta2), (hatbeta1,hatbeta2), R=None, 
                     epsrel=1.49e-04):
        """ Compute the SPT-modified Squared Deviation Function (SDF)
        
        The SDF has been introduced by Schramm, T. & Kayser, R, 1987, A&A 174, 
        361-364. The SPT-modified SDF computed here corresponds to
        
        If R is given:
        SDF1 = hatbeta1 - theta1 + tildealpha(theta1,theta2)[1] ,
        SDF2 = hatbeta2 - theta2 + tildealpha(theta1,theta2)[2] ,
    
        If R is not given:
        SDF1 = hatbeta1 - theta1 + hatalpha(theta1,theta2)[1] ,
        SDF2 = hatbeta2 - theta2 + hatalpha(theta1,theta2)[2] ,            
        
        and finally
        
        SDF = (SDF1**2 + SDF2**2)**0.5
            
        Parameters
        ----------
        (theta1, theta2) : array_like
            Components of an image position.
        (hatbeta1, hatbeta2) : array_like
            Components of the source position at the origin of the image.
        R : float, optional
            The radius of the circular finite region $\mathcal{U}$ of 
            integration. If not passed, the SDF is based on hatalpha instead
            of tildealpha.
        epsrel : float
            The absolute precision on tildealpha.

        Returns
        -------
        sdf : float
            The SPT-modified SDF function. 
        """
        if R is None:
            modified_alpha = self.modified_alpha((theta1,theta2))
        else:
            modified_alpha = self.tilde_alpha_fast(theta1, theta2, R, 
                                                   epsrel=epsrel)
        SDF0 = hatbeta1 + modified_alpha[0] - theta1
        SDF1 = hatbeta2 + modified_alpha[1] - theta2
        return (SDF0**2 + SDF1**2)**(0.5)    
        

    def tilde_images(self, images, hatsource, R, options=None, 
                          full_output=True):
        """
        Find the lensed images `tilde_theta` of a unique source `hatsource`,
        i.e. the solutions of the vectorial equation: 
        hatsource = tilde_theta - tilde_alpha(tilde_theta) .
        
        As initial positions, we use the original lensed images theta, i.e. 
        the solutions of the vectorial equation:
            source = theta - alpha(theta) ,
        as well as
            hatsource = theta - hat_alpha(theta) .
        
        """
        TILDE_IMAGES = []
        MINIMIZE_INFOS = []

        options_ref = {'maxiter': 500, 'maxfev': 1000, 
                       'xatol': 1.0e-08, 'fatol':1.0e-08, 
                       'return_all':True, 'disp':False}
        if options is None:
            options = options_ref
        else:
            _dic = HandlingDict(options)
            options = _dic.update_dict(options_ref)

        for im in images:
            sol = minimize(self.SDF, im, args=(hatsource, R), 
                           method='Nelder-Mead', options=options)
            TILDE_IMAGES.append(sol.x) 
            MINIMIZE_INFOS.append({'success':sol.success, 'nfev': sol.nfev, 
                                   'fun': sol.fun})
            
        if full_output:
            return TILDE_IMAGES, MINIMIZE_INFOS        
        else:
            return TILDE_IMAGES
            
    def tilde_images_sequence(self, sequence, R, options=None, ncpu=8, 
                              profile=True, full_output=True):
        """
        """
        options_ref = {'maxiter': 500, 'maxfev': 1000, 
                       'xatol': 1.0e-08, 'fatol':1.0e-08, 
                       'return_all':True, 'disp':False}
        if options is None:
            options = options_ref
        else:
            _dic = HandlingDict(options)
            options = _dic.update_dict(options_ref)
            
        def _tim(input_data, R, options=None):
            TILDE_IMAGES = []
            MINIMIZE_INFOS = []
            for im in input_data[0]:
                sol = minimize(self.SDF, im, args=(input_data[1], R), 
                               method='Nelder-Mead', options=options)
                TILDE_IMAGES.append(sol.x) 
                MINIMIZE_INFOS.append({'success':sol.success, 'nfev': sol.nfev, 'fun': sol.fun})
            return array(TILDE_IMAGES), MINIMIZE_INFOS 
        
        MP_tildeimages = Multiprocessing(_tim, sequence, 
                                         {'R':R, 'options':options})
        
        RESULTS_TILDE_MINIMIZATION = MP_tildeimages.run(nprocs=ncpu, profile=profile) 
        TILDE_IMAGES = [res[0] for res in RESULTS_TILDE_MINIMIZATION]
        MINIMIZATION_INFOS = [res[1] for res in RESULTS_TILDE_MINIMIZATION]        
        
        if full_output:    
            return TILDE_IMAGES, MINIMIZATION_INFOS
        else:
            return TILDE_IMAGES  
            
    def hat_tau(self, image):
        """
        Valid only for axi-symmetric case.
        """
        hat_alpha = self.modified_alpha(image[0], image[1])
        hat_psi = self.modified_psi_axisym(image, lowerBound=0.)
        
        return 0.5 * (hat_alpha[0]**2 + hat_alpha[1]**2) - hat_psi       
        
    def hat_tau_sequence(self, sequence, ncpu=8, profile=True):
        """
        Valid only for axi-symmetric case.        
        """
        def _hat_tau_images(images):
            return array([self.hat_tau(img) for img in images])
            
        MP_hattau = Multiprocessing(_hat_tau_images, sequence, {})  
        hat_tau = MP_hattau.run(nprocs=ncpu, profile=profile)          
            
        return hat_tau
            
    def tilde_tau(self, image, R=None, epsrel=1.49e-08, axisym=None, **kwargs):
        """
        """
#        if axisym is None:
#            axisym = self.model.is_axisym
#            
#        if axisym:
#            tilde_alpha = self.modified_alpha(image[0], image[1])
#            tilde_psi = self.modified_psi_axisym(image, lowerBound=0.)
#        else:
#            tilde_alpha = self.tilde_alpha_fast(image[0], image[1], R=R, epsrel=epsrel)
#            tilde_psi = self.tilde_psi_fast(image[0], image[1], R=R, epsrel=epsrel)
#        
#        return 0.5 * (tilde_alpha[0]**2 + tilde_alpha[1]**2) - tilde_psi 
        return self.modified_extra_light_travel_time(image, R, epsrel, 
                                                     **kwargs)
    
    def modified_extra_light_travel_time(self, image, R=None, epsrel=1.49e-06,
                                         debug=False, **kwargs):
        """
        """
        # FIXME: why tilde_psi_fast is so slow when run inside this method 
        #        whereas it's not when run outside??? Is it related to local
        #        and global variables?
        
#        if axisym is None:
#            axisym = self.model.is_axisym
            
        if R is None:
            tilde_alpha = self.modified_alpha(image[0], image[1])
            tilde_psi = self.modified_psi_axisym(image, lowerBound=0.)
        else:
            tilde_alpha = self.tilde_alpha_fast(image[0], image[1], R=R, 
                                                epsrel=epsrel, profile=debug)
            tilde_psi = self.tilde_psi_fast(image[0], image[1], R=R, 
                                            epsrel=epsrel, profile=debug)
        
        return 0.5 * (tilde_alpha[0]**2 + tilde_alpha[1]**2) - tilde_psi    
        
    def tilde_tau_sequence(self, sequence, R, epsrel=1.49e-08, ncpu=8, 
                           axisym=None, profile=True):
        """
        """
        if axisym is None:
            axisym = self.model.is_axisym
            
        def _tilde_tau_images(images, R, epsrel=1.49e-08, axisym=None):
            return array([self.tilde_tau(img, R, epsrel, axisym) for img in images])
        
        MP_tildetau = Multiprocessing(_tilde_tau_images, sequence,
                                      {'R':R, 'epsrel':epsrel, 'axisym':axisym})
        tilde_tau = MP_tildetau.run(nprocs=ncpu, profile=profile)            
        return tilde_tau     
        
    @Deprecated('modified_time_delays','Reason: `tilde_TD` has been renamed.')
    def tilde_TD(self, images, R=None, epsrel=1.49e-08, threshold=1.0e-06, 
                 ncpu=8, axisym=None, profile=True):
        """
        """
#        assert images.shape[0] > 1, "At least 2 images should be passed."
#        
#        if axisym is None:
#            axisym = self.model.is_axisym
#        
#        tilde_tau = array([self.tilde_tau(img, R, epsrel, axisym) for img in images])
#        tilde_tau_min = tilde_tau.min(axis=0)
#        
#        tilde_TD = [(ttaus-tilde_tau_min) if (ttaus-tilde_tau_min)>threshold 
#                    else 0.0
#                    for ttaus in tilde_tau]
#
#        return tilde_TD
        return self.modified_time_delays(images, R, epsrel, threshold)

    def modified_time_delays(self, images, R=None, epsrel=1.49e-08, 
                             threshold=1.0e-06):
        """
        """
        assert images.shape[0] > 1, "At least 2 images should be passed."
        
        #if axisym is None:
        #    axisym = self.model.is_axisym
        foo = self.modified_extra_light_travel_time
        
        tilde_tau = array([foo(img, R, epsrel) for img in images])
        tilde_tau_min = tilde_tau.min(axis=0)
        
        tilde_TD = [(ttaus-tilde_tau_min) if (ttaus-tilde_tau_min)>threshold 
                    else 0.0
                    for ttaus in tilde_tau]
        tilde_TD = array(tilde_TD)

        if len(tilde_TD) == 2 and abs(tilde_TD).min() == 0.0:
            # TD has only 1 non-zero value, which indicates that 
            # `image_positions` was composed of only 2 lensed image positions
            # leading to only 1 time delay.
            return float(tilde_TD[where(tilde_TD != 0.0)])
        else:        
            return tilde_TD
        
    def tilde_TD_sequence(self, sequence, R, epsrel=1.49e-08, threshold=1.0e-06, 
                          ncpu=8, axisym=None, profile=True):
        """      
        """
        if axisym is None:
            axisym = self.model.is_axisym
            
        tilde_tau = self.tilde_tau_sequence(sequence, R, epsrel, ncpu, axisym, 
                                            profile)
        shape = [t.shape[0] for t in tilde_tau]        
        tilde_TD = [(ttaus-ttaus.min(axis=0)) if s > 1  else array([0]) 
                    for ttaus,s in zip(tilde_tau,shape)]

        tilde_TD = [array([td if abs(td)>threshold else 0.0 for td in tds]) 
                    for tds in tilde_TD]

        return tilde_TD    
    
    def basics(self, R=None, extra=None):
        """
        """
        if R is not None:
            txt = ("Load the C shared libraries first. "
                   "To do so, run the `load_C_libraries`")
            assert self._tildealpha_C_libraries_loaded, txt
            assert self._tildepsi_C_libraries_loaded, txt    
        else:
            # If R is not passed, one uses the `hat` lensing quantities
            pass

        if extra is not None:
            _Xalpha = extra['alpha']
            _Xpsi = extra['psi']
            _Xkappa = extra['kappa'] 
            _Xjm = extra['jm']
        else:
            _Xalpha = lambda x,y: zeros(2)  
            _Xpsi = lambda x,y: 0.0
            _Xkappa = lambda x,y: 0.0
            _Xjm = lambda x,y: zeros([2,2])
            
            
        def wrap_kappa((x,y), p=None):
            return self.modified_kappa(x,y) + _Xkappa(x,y)


        if R is None:
            def wrap_alpha((x,y), p=None):
                return self.modified_alpha((x,y))
        else:
            def wrap_alpha((x,y), p=None):
                R = p[0]
                return self.tilde_alpha_fast(x,y,R) + _Xalpha(x,y)
        
        if R is None:
            def wrap_psi((x,y), p=None):
                return self.modified_psi_axisym((x,y))            
        else:
            def wrap_psi((x,y), p=None):
                R = p[0]
                return self.tilde_psi_fast(x,y,R, debug=False) + _Xpsi(x,y)
            
        if R is None:
            def wrap_jm((x,y), p=None):
                return identity(2) - self.modified_jacobi_matrix((x,y))
        else:
            def comp00(x1,x2,R):
                return self.tilde_alpha_fast(x1,x2,R,subIntegral=[True,False,True,False,True,False])[0]
            
            def comp01(x2,x1,R):
                return self.tilde_alpha_fast(x1,x2,R,subIntegral=[True,False,True,False,True,False])[0]
            
            def comp11(x2,x1,R):
                return self.tilde_alpha_fast(x1,x2,R,subIntegral=[False,True,False,True,False,True])[1]
            
            def comp10(x1,x2,R):
                return self.tilde_alpha_fast(x1,x2,R,subIntegral=[False,True,False,True,False,True])[1]
            
            def wrap_jm((x,y), p):
                R = p[0]
                temp = zeros([2,2])
                temp[0,0] = derivative(x, comp00, x2=y,R=R)
                temp[1,1] = derivative(y, comp11, x1=x,R=R)    
                temp[0,1] = derivative(x, comp10, x2=y,R=R)
                temp[1,0] = temp[0,1]
                return temp + _Xjm(x,y)      
            
        return [None, wrap_psi, wrap_alpha, wrap_kappa, wrap_jm]  
    
    def sptModel(self, R=None, center=[0.,0.], cc_guess=None, extra=None):
        """
        extra:  adds an external contribution to the model, independant to the
                SPT.
        """
        basics = self.basics(R=R, extra=extra) 
        model = Model(*basics, p0=[R], center=center, cc_guess=cc_guess)
        
        return model

# -----------------------------------------------------------------------------
class _CheckBounds(object):
    """
    """
    def __init__(self, peak):
        self.peak = peak
        
    def __call__(self, radius_interval=0.1, angle_interval=0.4):
        """
        """
        r_bounds = list()
        phi_bounds = list()
        
        N_r_subdivision = 0
        
        r_condition = self.peak[0] > radius_interval
        phi_condition_0 = self.peak[1] - angle_interval < 0.
        phi_condition_1 = self.peak[1] + angle_interval > 2.*pi
        
        N_r_subdivision = 3 if r_condition else 2
        N_phi_subdivision = 2 if not phi_condition_0 and not phi_condition_1 else 1
        
        r_trailing = [(0., 1.) for k in xrange(N_phi_subdivision)]
        phi_leading = [(self.peak[1]-angle_interval, self.peak[1]+angle_interval) for k in xrange(N_r_subdivision)]
                                                     
        if r_condition: #self.peak[0] > radius_interval:
            r_bounds = [(0., self.peak[0]-radius_interval),
                        (self.peak[0]-radius_interval, self.peak[0]+radius_interval),
                        (self.peak[0]+radius_interval, 1.0)]
            r_bounds += r_trailing                        
        else:
            r_bounds = [(0., self.peak[0]+radius_interval),
                        (self.peak[0]+radius_interval, 1.0)]
            r_bounds += r_trailing                        

        phi_bounds += phi_leading        
        if not phi_condition_0 and not phi_condition_1:
            phi_bounds += [(0., self.peak[1]-angle_interval), (self.peak[1]+angle_interval, 2.*pi)]                
        elif phi_condition_0:
            phi_bounds += [(self.peak[1]+angle_interval, self.peak[1]-angle_interval+2.*pi)]                           
        elif phi_condition_1:
            phi_bounds += [(self.peak[1]+angle_interval-2.*pi, self.peak[1]-angle_interval)]
        else:
            # On should never come here.
            pass
        
        return r_bounds, phi_bounds


# ----------------------------------------------------------------------------- 
class GetCLibraries(object):
    """
    UNDER CONSTRUCTION
    
    UP TO NOW, THE ONLY MASS MODELS AND SOURCE MAPPING TO HAVE BEEN IMPLEMENTED
    ARE RESPECTIVELY:
        
    MODEL -->   (a) NIS + SHEAR
                (b) NIE + SHEAR
                (c) HERN + GNFW + SHEAR
                ...
    
    SPT -->     (a) ISOTROPIC STRETCHING 1: hat_beta = (1+f0 + f2/2*|beta|**2) * beta
                ...
    """
    # FIXME: HERNgNFWG raises sometimes an error: missing libgsl.23.dylib
    def __init__(self, root=None, platform='osx'):
        """
        """
        try:
            if platform == 'osx':
                subpath = 'sources_C/osx'
            elif platform == 'linux':
                subpath = 'sources_C/linux'
            elif platform == 'win':
                subpath = 'sources_C/win'
            else:
                subpath = 'sources_C/osx'

            self.root_builtin = join(abspath(join(__file__, pardir, pardir)),subpath)
                
        except NameError:
            self.root_builtin = None
        
        if root is not None:
            self.root = root
        else:
            self.root = self.root_builtin
        
    def _get(self, filename):
        """
        """
        return ctypes.CDLL(join(self.root, filename)) 
        
        
    def _integrand_alphatilde(self, filename=None, model_ID=None, source_mapping_ID=None):
        """
        """
        non_sheared = ['NIS', 'NIE', 'NFW', 'HERN']
        if model_ID in non_sheared:
            model_ID += 'G' # It will be considered as a zero-intensity sheared model. 
        elif model_ID == 'GNFW':
            model_ID = model_ID[1:] + 'G'
        else:
            pass            
        
        lib = None
        if filename is None:
            self.root = self.root_builtin
            if model_ID == 'NISG' and source_mapping_ID=='IS1':
                lib = self._get('IntegrandAlphaTilde_NISG_IS1.so')
            elif model_ID == 'NIEG' and source_mapping_ID=='IS1':
                lib = self._get('IntegrandAlphaTilde_NIEG_IS1.so')
            elif model_ID == 'HERNG' and source_mapping_ID=='IS1':
                lib = self._get('IntegrandAlphaTilde_HERNG_IS1.so')                
            elif model_ID == 'HERNGNFWG' and source_mapping_ID=='IS1':
                lib = self._get('IntegrandAlphaTilde_HERNgNFWG_IS1.so') 
            elif model_ID == 'NFWG' and source_mapping_ID=='IS1':
                lib = self._get('IntegrandAlphaTilde_NFWG_IS1.so')                
            else:                
                raise ValueError('``model_ID`` ({}) or ``source_mapping_ID`` ({}) keywords not recognized.'.format(model_ID,source_mapping_ID))
        else:
            lib = self._get(filename)              
        
        if lib is not None:
            integrand_I1_0 = lib.integrand_I1_0
            integrand_I1_0.restype = ctypes.c_double
            integrand_I1_0.argtypes = (ctypes.c_int, ctypes.c_double)
            
            integrand_I1_1 = lib.integrand_I1_1
            integrand_I1_1.restype = ctypes.c_double
            integrand_I1_1.argtypes = (ctypes.c_int, ctypes.c_double)
            
            integrand_I3_0 = lib.integrand_I3_0
            integrand_I3_0.restype = ctypes.c_double
            integrand_I3_0.argtypes = (ctypes.c_int, ctypes.c_double) 
            
            integrand_I3_1 = lib.integrand_I3_1
            integrand_I3_1.restype = ctypes.c_double
            integrand_I3_1.argtypes = (ctypes.c_int, ctypes.c_double)
    
            integrand_J1_0 = lib.integrand_J1_0
            integrand_J1_0.restype = ctypes.c_double
            integrand_J1_0.argtypes = (ctypes.c_int, ctypes.c_double) 
            
            integrand_J1_1 = lib.integrand_J1_1
            integrand_J1_1.restype = ctypes.c_double
            integrand_J1_1.argtypes = (ctypes.c_int, ctypes.c_double)
        else:
            # Nothing is given: no path towards the user C library, no model_ID 
            # and/or source_mapping_ID for using the buitlin implemenation.
            raise ValueError('Either ``filename`` or (``model_ID``, ``source_mapping_ID``) must be passed.')

        return [integrand_I1_0, integrand_I1_1,
                integrand_I3_0, integrand_I3_1,
                integrand_J1_0, integrand_J1_1]
                
    def _integrand_psitilde(self, filename=None, model_ID=None, source_mapping_ID=None):
        """
        """
        non_sheared = ['NIS', 'NIE', 'HERN']
        if model_ID in non_sheared:
            model_ID += 'G' # It will be considered as a zero-intensity sheared model. 
        elif model_ID == 'GNFW':
            model_ID = model_ID[1:] + 'G'
        else:
            pass
        
            
        lib = None
        if filename is None:
            self.root = self.root_builtin
            if model_ID == 'NISG' and source_mapping_ID=='IS1':
                lib = self._get('IntegrandPsiTilde_NISG_IS1.so')
            elif model_ID == 'NIEG' and source_mapping_ID=='IS1':
                lib = self._get('IntegrandPsiTilde_NIEG_IS1.so') 
            elif model_ID == 'HERNG' and source_mapping_ID=='IS1':
                lib = self._get('IntegrandPsiTilde_HERNG_IS1.so')                  
            elif model_ID == 'HERNGNFWG' and source_mapping_ID=='IS1':
                lib = self._get('IntegrandPsiTilde_HERNgNFWG_IS1.so')
            elif model_ID == 'NFWG' and source_mapping_ID=='IS1':
                lib = self._get('IntegrandPsiTilde_NFWG_IS1.so')                 
            else:                
                raise ValueError('``model_ID`` or ``source_mapping_ID`` keywords not recognized.')
        else:
            lib = self._get(filename)               
        
        if lib is not None:
            integrand_I1 = lib.integrand_I1
            integrand_I1.restype = ctypes.c_double
            integrand_I1.argtypes = (ctypes.c_int, ctypes.c_double)
            
            integrand_I2 = lib.integrand_I2
            integrand_I2.restype = ctypes.c_double
            integrand_I2.argtypes = (ctypes.c_int, ctypes.c_double)
            
            integrand_I3 = lib.integrand_I3
            integrand_I3.restype = ctypes.c_double
            integrand_I3.argtypes = (ctypes.c_int, ctypes.c_double) 
            
            integrand_J1 = lib.integrand_J1
            integrand_J1.restype = ctypes.c_double
            integrand_J1.argtypes = (ctypes.c_int, ctypes.c_double)
    
            integrand_J2 = lib.integrand_J2
            integrand_J2.restype = ctypes.c_double
            integrand_J2.argtypes = (ctypes.c_int, ctypes.c_double) 

        else:
            # Nothing is given: no path towards the user C library, no model_ID 
            # and/or source_mapping_ID for using the buitlin implemenation.
            raise ValueError('Either ``filename`` or (``model_ID``, ``source_mapping_ID``) must be passed.')

        return [integrand_I1, integrand_I2, integrand_I3,
                integrand_J1, integrand_J2]                
