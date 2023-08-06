# -*- coding: utf-8 -*-

import time
from functools import partial

from scipy.misc import derivative
from scipy.spatial import Delaunay
from scipy.optimize import minimize
from scipy.integrate import nquad
from matplotlib.pylab import subplots, xlabel, ylabel, xlim, ylim, show
from matplotlib.pylab import savefig
import matplotlib.path as mplPath
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from numpy import array, sign, identity, argmin, cos, sin, pi, inf, linspace
from numpy import max, maximum, sqrt, sum, prod, nonzero, concatenate, mod
from numpy import gradient, sort, argsort, arctan2, empty, zeros, zeros_like
from numpy import trace, vstack, meshgrid, floor, argwhere, column_stack
from numpy import median, where, ceil, append, ndarray, mean, std, ones, min
from numpy.linalg import det, eig
from numpy.random import uniform, choice

from .. import catalog
from ..multiproc.multiproc import Multiprocessing, available_cpu
from ..grid.grid import Meshgrid
from ..decorators.others import Deprecated, Decenter
from ..decorators.profile import timeit
from ..tools.vector import norm_fast
from ..tools.container import HandlingDict, isiterable
from ..tools.toolbox import remove_duplicate, combine 
from ..tools.geometry import curve_extent, centroid_polygon, separation
from ..tools.geometry import closest_node, random_points_inside_triangle
from ..tools.geometry import points_on_triangle_edge, triangles_filtering
from ..tools.geometry import separate_closed_curves, get_random_point_in_circle 
from ..tools.geometry import Triangle, Ellipse
from ..tools.colors import Colors
from ..tools.caustics import GLCaustics
from ..tools.operators import grad, laplacian, hessian
from ..tools.graphics import Graphics, Colorbar
from . import examples

__author__ = 'O. Wertz @ Bonn'
__all__ = ['CriticalCurves',
           'Model',
           'ModelInitialization',
           'Which'
           ]


class Which(object):
    """ Give useful informations related to a lens model."""
    
    def __init__(self, which=None):
        """
        Parameters
        ----------
        which : string
            Id of the lens model.
            
        """
        self.which = which
        
    def list_of_models_ids(self):
        """ Give a list of the implemented lens models with their id.
        """
        return Which.static_model_implemented

    def is_model_implemented(self, which=None):
        """ Check wether the model is implemented.
        
        Parameters
        ----------
        which : string
            Id of the lens model.
            
        Returns
        -------
        isimplemented : bool
            True is the model is implemented, False otherwise.
            
        """
        if which is None: 
            which = self.which
        
        msg = 'The model id None is not recognized.'
        assert which is not None, msg
            
        if which.upper() in catalog.documentation.ModelImplemented().ids:
            return True
        else:
            return False     
       
    def model_help(self):
        """ Print the docstring related to the model."""
        catalog.documentation.ModelInfo(self.which).full_documentation()


class ModelInitialization(object):
    """ Extract the basic lensing quantities from the lens model catalog."""
    
    def __init__(self, which):
        """ 
        Parameters
        ----------
        which : string
            Id of the lens model.
            
        """
        self.which = which
        
        msg_ex_valid =("Example id `{}` does not match the class id {}.")
        msg_not_recognized = ("The model `{}` is not recognized.")
        
        if self.which is 'example_0': # If the user ask for an example ...
            assert self.which is examples.Example0.get_id(), \
                   msg_ex_valid.format(self.which,examples.Example0.get_id())
                   
        else: # ... otherwise
            assert Which(self.which).is_model_implemented(), \
                   msg_not_recognized.format(self.which)
                   
    def parameters(self):
        """ When defined, it returns the default model parameters."""
        if self.which is 'example_0':
            return examples.Example0().get_parameters()
        else:
            return None                   

    def basics(self):
        """ Extract the deflection potential, angle, surface mass density and
        the jacobian of the deflection mapping from the lens model catalog.
        """
        if self.which is 'example_0':
            _basics = examples.Example0().get_basics()
        
        else:
            _lens_model = getattr(catalog, self.which.lower())
            _basics = {'psi':_lens_model.deflection_potential,
                           'alpha':_lens_model.deflection_angle,
                           'kappa':_lens_model.surface_mass_density,
                           'jm_alpha':_lens_model.derivative1_da}        
        return _basics

 
class Model(object):
    """ Implements a wide range of basic lensing calculations.
    
    A Model object shares a lot of methods with other lensing-dedicated 
    softwares such as gravlens (Keeton 2001b). Strictly speaking, this part 
    of the code is not related to the SPT and it can be used independently 
    of any SPT analysis.
    
    """
    # TODO: implements a __getitem__    
    def __init__(self, which=None, psi=None, alpha=None, kappa=None, 
                 jacobi_matrix_alpha_mapping=None, p0=None, is_axisym=False,
                 center=[0.,0.], cc_guess=None, *args, **kwargs):
        """
        Parameters
        ----------
        which : string
            Lens model ID.
        psi, alpha, kappa, jacobi_matrix_alpha_mapping : callable
            When the user want to use its own lens model implementation, he 
            can pass callable functions to define the deflection potential,
            angle, surface mass density and the jacobian matrix of the 
            deflection mapping. The same convention as the built-in 
            methods must be respected.
        p0 : array_like
            List of the model parameters. 
        is_axisym : bool
            Define whether the model is axisymmetric or not.
        center : array_like
            Position of the gravity center of the lens.
        cc_guess : list of array_like
            Disjointed critical curves defined as Nx2 array_like, wrapped
            into a list. For instance, cc_guess defined as a list of two
            100x2 arrays corresponds to two disjointed critical curves, both 
            composed of 100 points defined by their cartesian coordinates 
            (x,y).
            
        """  
        self.center = center
        self.is_axisym = is_axisym # TODO: should be considered separatly
        self.cc_guess = cc_guess
        self.analytic = {'psi':None, 'alpha':None, 'kappa':None, 
                         'jm_alpha':None}        
        
        self.which = which
        if self.which is not None:
            mi = ModelInitialization(self.which)
            self.basics = mi.basics()
        else:
            self.basics = {'psi':psi, 
                           'alpha':alpha, 
                           'kappa':kappa, 
                           'jm_alpha':jacobi_matrix_alpha_mapping}
           
        if kwargs.has_key('ID'):
            self.ID = kwargs.pop('ID', None)
        else:
            if which == 'SHEAR':
                self.ID = 'G'
            else:
                self.ID = which
        #
        if self.ID == 'GNFWG': 
            self.ID = 'NFWG'
        #
            
        if p0 is 'random' and self.which is not None:
            self.p0= getattr(catalog,'random_parameters_'+self.which.lower())()
        elif p0 is not None and self.which is None:
            self.p0 = p0
        elif self.which is not None and self.which.startswith('example_'):
            self.p0 = mi.parameters()
        else:
            self.p0 = p0        
                          
        msg_lens_not_defined = ("Neither psi, kappa, alpha, nor its "
                                "derivatives are defined.") 
        assert self.basics.values().count(None) < 4, msg_lens_not_defined
        
        msg_psi_not_defined = 'The deflection potential must be defined.'
        assert self.basics['psi'] is not None, msg_psi_not_defined
           
        if self.p0 is None:
            self._none_function = lambda (theta1, theta2), p : (0.,0.)
        else:
            self._none_function = lambda (theta1, theta2): (0.,0.)   

        # Deflection potential must be defined analyticaly
        @Decenter(self.center)
        def _psi((theta1, theta2), p=None):
            """
            """
            if p is None: p = self.p0
            return self.basics['psi']((theta1,theta2), p)  
        self.psi = _psi
        self.analytic['psi'] = True

        # Deflection angle
        if self.basics['alpha'] is not None:
            self.analytic['alpha'] = True            
            @Decenter(self.center)            
            def _alpha((theta1, theta2), p=None):
                """
                """
                if p is None: p = self.p0
                return self.basics['alpha']((theta1,theta2), p)
        else:
            self.analytic['alpha'] = False
            @Decenter(self.center)            
            def _alpha((theta1, theta2), p=None):
                """
                """
                if p is None: p = self.p0
                return grad((theta1,theta2), 
                            partial(self.basics['psi'], p=p))
        self.alpha = _alpha            
            
        # Surface mass density
        if self.basics['kappa'] is not None:
            self.analytic['kappa'] = True
            @Decenter(self.center)            
            def _kappa((theta1, theta2), p=None):
                """
                """
                if p is None: p = self.p0
                return self.basics['kappa']((theta1, theta2), p)
        else:
            self.analytic['kappa'] = False            
            @Decenter(self.center)            
            def _kappa((theta1, theta2), p=None):
                """
                """
                if p is None: p = self.p0
                return 0.5*laplacian((theta1,theta2), 
                                     partial(self.basics['psi'], p=p))
        self.kappa = _kappa
            
        # Deflection Jacobi matrix
        if self.basics['jm_alpha'] is not None:
            self.analytic['jm_alpha'] = True
            @Decenter(self.center)
            def _jm_alpha_mapping((theta1, theta2), p=None):
                """
                """
                if p is None: p = self.p0
                return self.basics['jm_alpha']((theta1,theta2), p)
        else:
            self.analytic['jm_alpha'] = False            
            @Decenter(self.center)            
            def _jm_alpha_mapping((theta1, theta2), p=None):
                """
                """
                if p is None: p = self.p0
                return hessian((theta1,theta2), 
                               partial(self.basics['psi'], p=p))          
        self.jm_alpha_mapping = _jm_alpha_mapping

    def __add__(self, m):                           
        def new_alpha((t1,t2), p):
            a0, a1 = self.alpha((t1,t2),p[0])
            b0, b1 = m.alpha((t1,t2), p[1])
            return array([a0+b0, a1+b1])
               
        def new_kappa((t1,t2), p=None):
            return self.kappa((t1,t2),p[0]) + m.kappa((t1,t2), p[1])
        
        def new_psi((t1,t2), p=None):
            return self.psi((t1,t2),p[0]) + m.psi((t1,t2), p[1])
            
        return Model(psi=new_psi, 
                     alpha=new_alpha,
                     kappa=new_kappa,
                     jacobi_matrix_alpha_mapping=lambda (t1,t2), p: self.jm_alpha_mapping((t1,t2),p[0]) + m.jm_alpha_mapping((t1,t2), p[1]),
                     is_axisym=self.is_axisym * m.is_axisym,
                     p0 = combine(self.p0,m.p0),
                     center = None,
                     ID = self.ID + m.ID)
 
    # TODO: implements deflection_angle, deflection_potential and jm the same 
    # way we did for surface_mass_density
    def surface_mass_density(self, pos, p=None, multi=False, **kwargs):
        """ Give the surface mass density associated to the lens model.
        
        Parameters
        ----------
        pos : array_like
            pos can be either a single position in the lens plane or an array
            of several positions.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
        multi : bool
            If True, the method is parallelized over multi-cores.
        kwargs : dict
            Options passed to the Multiprocessing.run method.
        
        Returns
        -------
        kappa : float
            Return the surface mass density evaluated at the postision `pos`.
            
        """
        if p is None: p = self.p0
        
        if ((isinstance(pos,list) or isinstance(pos,tuple) or isinstance(pos,ndarray))  
            and len(pos) == 2 and not isiterable(pos[0]) and 
            not isiterable(pos[1])):
            # pos is a list which contains the two coordinates of a 
            # single position.
            return self.kappa(pos, p)
        elif (isinstance(pos,list) and len(pos) == 2 and isiterable(pos[0]) 
              and isiterable(pos[1])):          
            # pos is a list which contains exactly two sets of positions.
            return vstack((self.kappa(pos[0],p), self.kappa(pos[1],p)))
        elif len(pos) > 2 and not isiterable(pos[0]):            
            # Axisym case: pos contains a list of radial coordinates.
            return array([self.kappa((_pos,0.0),p) for _pos in pos])
        elif len(pos) > 2 and isiterable(pos[0]):            
            # pos is a list of more than two sets of positions
            return array([self.kappa(_pos,p) for _pos in pos])        
        elif isinstance(pos,ndarray) and pos.ndim ==2  and pos.shape[0] > 2:
            if multi:
                mp = Multiprocessing(self.kappa, pos, {'p':p})
                return array(mp.run(**kwargs))
            else:
                return array([self.kappa(_pos,p) for _pos in pos])
        else:
            print 'WARNING: the format of `pos` is not valid: `None` has been returned.'
            return None
    
    def isodensity(self, position, center=[0.,0.], fun=None, N=100, 
                   options=None, p=None, multi=False, multi_opts={}):
        """ Determine the coordinates of the isodensity contour which passes
        by the given `position`.
        
        Parameters
        ----------
        
        position : array_like
            Coordinates of a position in the lens plane.
        center : array_like
            Coordinates of the lens center of mass. See notes for more 
            details.
        fun : callable
            If None, the cost function used to find the positions x which 
            composed the isodensity contour is |kappa(position) - kappa(x)|.
            Otherwise, you can define you own cost function with the 
            signature (`pos`, `kp0`, ...) where `pos` is an array_like 
            and `kp0` a float.
        N : int
            Number of points which composed the contour.
        options : dict
            Options passed to scipy.optimize.minimize().
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
        multi : bool
            If True, the method is parallelized over multi-cores.            
        
        Returns
        -------
        
        contour : Nx2 numpy array
            Coordinates of the isodensity contour line. 
        
        Notes
        -----
        One restricts to closed curve centered on `center`. This means that 
        one assumes that the isodensity contour will surround the `center`. 
        When the lens model is a combination of several `Model` instances, 
        which define components that are located at different positions in the 
        lens plane, defining `center` allows us to restrict the search in 
        the vicinity of the component located at `center`. 
        
        """
        kappa0 = self.surface_mass_density(position+array(center), p, 
                                           multi, **multi_opts)
        
        if fun is None:
            def fun(pos, kp0):
                _kp = self.surface_mass_density(pos, p, multi, **multi_opts)
                return abs(_kp - kp0)
            
        options_default = {'maxiter': 500, 'maxfev': 1000, 
                           'xatol': 1.0e-08, 'fatol':1.0e-08, 
                           'return_all':False, 'disp':False}

        if options is None:
            options = options_default 
        else:
            options = HandlingDict(options).update_dict(options_default)  
         
            
        r = norm_fast(position)
        angle = linspace(0., 2.*pi, N, endpoint=False)
        
        x = r * cos(angle) + center[0]
        y = r * sin(angle) + center[1]
        
        res = []
        for _x0, _y0 in zip(x,y):
            _res = minimize(fun, (_x0,_y0), args=(kappa0), 
                            method='Nelder-Mead', options=options)
            res.append(_res.x)
        
        return array(res)
        
    def surface_mass_density_profile(self, bounds, p=None, N=100, multi=False,
                                     norm=None, logscale=False, 
                                     xlogscale=False, ylogscale=False,
                                     elliptical=False, center=[0.,0.],
                                     plot_opts=None, axis_opts=None):
        """ Plot the surface mass density profile between given radius.
        
        Parameters
        ----------
        
        Returns
        -------
        
        """        
        xcoord = linspace(bounds[0], bounds[1], N) + center[0]
        ycoord = zeros_like(xcoord) + center[1]
        sampling = array(zip(xcoord,ycoord))
        kappa = self.surface_mass_density(pos=sampling, p=p, multi=multi)
        
        if elliptical:
#            if flattening is not None:
#                if orientation is None: 
#                    orientation = 0.0
#                else:
#                    orientation = mod(orientation, 2.*pi)
#
#                def _ellipse_axis((_z_x,_z_y), (_z_h,_z_k), _z_A, _z_q):
#                    _z_Gamma_a = (_z_x-_z_h)*cos(_z_A) + (_z_y-_z_k)*sin(_z_A)
#                    _z_Gamma_b = - (_z_x-_z_h)*sin(_z_A) + (_z_y-_z_k)*cos(_z_A)
#                    _z_a = (((1.-_z_q)**2 * _z_Gamma_a**2 + _z_Gamma_b**2) / (1.-_z_q)**2)**0.5  
#                    _z_b = _z_a*(1-_z_q)
#                    return array([_z_a, _z_b])
#                
#                _ell = [_ellipse_axis(_s, center, orientation, flattening) for _s in sampling]
#                
#            else:
    
            _sampling = array(zip(xcoord-center[0],ycoord-center[1]))
            mp = Multiprocessing(self.isodensity, _sampling, {'center':center, 'N':11})
            _iso = mp.run(nprocs=available_cpu())
            _ell = [Ellipse(_i[:,0],_i[:,1]).ellipse_axis_length() 
                    for _i in _iso]
            
            xcoord = array([(_x.prod())**0.5 for _x in _ell])
        
        if axis_opts is None: axis_opts = {}
        if plot_opts is None: plot_opts = {}
        
        # Norm and labels
        if norm is not None: xcoord = xcoord / norm

        if not elliptical: xcoord = xcoord-center[0]
            
        if norm is None and not axis_opts.has_key('set_xlabel'):
            if elliptical:
                set_xlabel = {'set_xlabel':{'xlabel':r'$\sqrt{\theta_a \theta_b}$','fontsize':20}}
            else:
                set_xlabel = {'set_xlabel':{'xlabel':r'$|\boldsymbol{\theta}|$','fontsize':20}}
        elif norm is not None and not axis_opts.has_key('set_xlabel'):
            if elliptical:
                set_xlabel = {'set_xlabel':{'xlabel':r'$\sqrt{\theta_a \theta_b} / \theta_{\text{\small E}}$','fontsize':20}}                
            else:
                xlabel = r'$|\boldsymbol{\theta}| / \theta_{\text{\small E}}$'
            set_xlabel = {'set_xlabel':{'xlabel':xlabel,'fontsize':20}}
        else:
            set_xlabel = {}
        
        if not axis_opts.has_key('set_ylabel'):
            if elliptical:
                set_ylabel = {'set_ylabel':{'ylabel':r'$\kappa(\boldsymbol{\theta})$',
                                            'fontsize':20}} 
            else:
                set_ylabel = {'set_ylabel':{'ylabel':r'$\kappa(|\boldsymbol{\theta}|)$',
                                            'fontsize':20}} 
        else:
            set_ylabel = {}

        # x- and y-scale
        if logscale: xlogscale, ylogscale = (True,True)
        
        if xlogscale: 
            xscale = 'log'
        else:
            xscale = 'linear'
            
        if ylogscale: 
            yscale = 'log'
        else:
            yscale = 'linear'            
                    
        set_xscale = {'set_xscale':xscale}
        set_yscale = {'set_yscale':yscale}            
                                    
        # x- and y-limits
        set_lim = {'set_xlim':[xcoord.min(),xcoord.max()],
                   'set_ylim':[kappa.min(),kappa.max()]}       
      
        # Update axis_opts
        axis_opts = HandlingDict.merge_dicts(axis_opts, set_xlabel, set_ylabel, 
                                             set_xscale, set_yscale, set_lim)
              
        return Graphics().plot(x=xcoord, y=kappa, axis_options=axis_opts,
                               plot_options=plot_opts) 
        
    def surface_mass_density_2dmap(self, bounds, p=None, N=100, multi=False,
                                   norm=None, clmap='gray_r', threshold=None,
                                   subplots_opts=None, plot_opts=None, 
                                   axis_opts=None, plot=True, **kwargs):
        """ Plot a 2d map of the surface mass density.
        
        Parameters
        ----------
        
        Returns
        -------
        
        """     
        if not isiterable(bounds):
            bounds = (-abs(bounds),abs(bounds))
            
        if not isiterable(bounds[0]):
            spanx = linspace(bounds[0], bounds[1], N)
            spany = spanx
        else:
            spanx = linspace(bounds[0][0], bounds[0][1], N)
            spany = linspace(bounds[1][0], bounds[1][1], N)
        
        mesh_1, mesh_2 = meshgrid(spanx, spany)
        sampling = array(zip(mesh_1.flatten(),mesh_2.flatten()))
       
        kappa = self.surface_mass_density(sampling, multi=multi, **kwargs)
        
        if threshold is not None:
            if isinstance(threshold,str) and threshold.endswith('-sigma'):
                _factor = int(threshold[0])
                _median = median(kappa)
                _std = std(kappa)
                _threshold = _median + _factor*_std
                kappa[where(kappa >= _median + _factor*_std)] = _threshold
            else:
                kappa[where(kappa >= threshold)] = threshold

        if subplots_opts is None: subplots_opts = {}
        if axis_opts is None: axis_opts = {}
        if plot_opts is None: plot_opts = {}
        
        # Norm and labels                        
        if norm is None and not axis_opts.has_key('set_xlabel'):
            set_xlabel = {'set_xlabel':{'xlabel':r'$\theta_x$','fontsize':20}}
        elif norm is not None and not axis_opts.has_key('set_xlabel'):          
            xlabel = r'$\theta_x / \theta_{\text{\small E}}$'
            set_xlabel = {'set_xlabel':{'xlabel':xlabel,'fontsize':20}}
            mesh_1 = mesh_1 / norm
        elif norm is not None:
            set_xlabel = {}
            mesh_1 = mesh_1 / norm
            
            
        if norm is None and not axis_opts.has_key('set_ylabel'):
            set_ylabel = {'set_ylabel':{'ylabel':r'$\theta_y$','fontsize':20}}
        elif norm is not None and not axis_opts.has_key('set_ylabel'):          
            ylabel = r'$\theta_y / \theta_{\text{\small E}}$'
            set_ylabel = {'set_ylabel':{'ylabel':ylabel,'fontsize':20}}
            mesh_2 = mesh_2 / norm
        else:
            set_ylabel = {}
            mesh_2 = mesh_2 / norm
      
        # Update axis_opts
        axis_opts = HandlingDict.merge_dicts(axis_opts, set_xlabel, set_ylabel) 

#        if (not axis_opts.has_key('set_xlabel') and 
#            not axis_opts.has_key('set_ylabel')):
#            labels = {'set_xlabel':{'xlabel':r'$\theta_x$', 'fontsize':20},
#                      'set_ylabel':{'ylabel':r'$\theta_y$', 'fontsize':20}}            
#            axis_opts = HandlingDict(axis_opts).update_dict(labels)                                              

        canvas,fig,ax1 = Graphics().build_figure((1,1),subplots_opts,axis_opts) 
        
        _ = ax1.contourf(mesh_1, mesh_2, kappa.reshape(mesh_1.shape), N, 
                         cmap=clmap)
        Colorbar(kappa).add_colorbar(fig, ax1, label=r'$\kappa$', 
                                               clmap=clmap)                                             
#              
#        return Graphics().plot(x=xcoord, y=kappa, axis_options=axis_opts,
#                               plot_options=plot_opts) 
        if plot: 
            return canvas.figure
        else:
            return canvas, fig, ax1
        
    def eigen(self, (theta1, theta2), p=None):
        """ Eigenvalues of the lens mapping. 
        
        Parameters
        ----------
        theta1, theta2 : double
            Position in the lens plane where the method is evaluated.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
            
        Returns
        -------
        eigen : array_like
            A tuple of ndarrays containing the eigenvectors and the 
            eigenvalues of the Jacobi matrix of the lens mapping.   
            
        """
        if p is None: p = self.p0
        
        eigv =  eig(self.jm_lens_mapping((theta1,theta2), p))
        
        return eigv
            
#    @Deprecated('kappa_average')
#    def kappa_azimuthally_averaged(self, norm_theta12, p):
#        """
#        """
#        return 0
        
    def kappa_average(self, rmax, rmin=0.0, p=None):
        """ Compute the average surface mass density in an annulus.

        Parameters
        ----------
        rmax, rmin : double
            Outer and inner radius of the annulus.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.

        Returns
        -------
        kappa_average : float
            The average of kappa within the annulus of rmin and rmax.            
            
        Notes
        -----
        When the surface mass density is axisymmetric, we have
        <kappa>(r1,r2) = 2/(r1**2 - r2**2) Integral_r1^r2[x * kappa(x) dx]
                       = 2/(r1**2 - r2**2) (Integral_0^r1[x * kappa(x) dx] 
                                            - Integral_0^r2[x * kappa(x) dx])
                       = (alpha(r1)*r1 - alpha(r2)*r2) / (r1**2 - r2**2)
                       
        For an SIS, <kappa>(r1,r2) = 1/2 if r1 and r2 are the radial 
        coordinates of two lensed images of the same source.
        
        In general, we have
        <kappa>(r1,r2) = 1/(pi*(r1**2-r2**2))
                            * dbquad[r kappa(r,phi),(r1,r2),(0, 2pi)]
        """
#        TODO: 
#            + One should separate the case where rmin=0.0 (disk) and rmin>0.0
#              (annulus).
#            + One should implement the more general `aperture mass` quantity.        
        assert rmax > 0.0, 'rmax must be positive ({} given)'.format(rmax)
        assert rmax >= abs(rmin), 'rmax must be >= |rmin|'
        assert rmin >=0.0,'rmin must be positive ({} given)'.format(rmin)
        
        if p is None: p = self.p0
        
        if self.is_axisym:
            if rmin == 0.0:
                return self.alpha((rmax, 0.0), p)[0]/rmax
            elif rmin > 0.0:
                _numerator = self.alpha((rmax, 0.0), p)[0]*rmax \
                             - self.alpha((rmin, 0.0), p)[0]*rmin
                return _numerator/(rmax**2 - rmin**2)
        elif not self.is_axisym:
            def wrapper(r, phi, p):
                return r * self.kappa((r*cos(phi), r*sin(phi)), p)    
            integral = nquad(wrapper, [[rmin, rmax],[0., 2.*pi]], args=(p,), opts={'epsrel':1.49e-05})
            return (1./(pi*(rmax**2-rmin**2))) * integral[0]

    def mass(self, r, p=None):
        """ Compute the projected mass inside a circular aperture.
        
        Parameters
        ----------
        r : double
            Radius of the circular aperture.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.

        Returns
        -------
        mass : float
            The projected mass inside a circualar aperture of radius r.             
        
        """
        if p is None: p = self.p0
        
        if self.is_axisym:
            k = self.kappa_average(r, 0.0, p)
            return k * r**2
        else:
            # Not yet implemented
            return None

    def einsteinRadius(self, p=None, options=None, full_output=False):
        """ Return a numerical estimation for tE, the angular radius of the 
        Einstein ring. 
        
        The calculation is based on an minimization process using the
        scipy.optimize.minimize module.
        
        Parameters
        ----------
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
        options : dict
            Options passed to scipy.optimize.minimize.
        full_output : bool
            If True, the method also returns intermediate results.

        Returns
        -------
        tE : float
            The numerical estimation for the angular radius of the Einstein
            ring.
            
        Notes
        -----
        For an axisymmetric lens, tE corresponds to the radius of the Einstein
        ring obtained when the source, lens and observer are perfectly aligned,
        that is when beta = 0 ==> theta - alpha(theta) = 0. In the previous 
        equation, theta is the radial component of the polar coordinates and 
        thus is > 0. In literature, one can also find another notation where
        theta represents the x-component of the cartesian coordinates after 
        rotating the colinear source-images direction to match the x-axis. In 
        that case, theta can be < 0. The adopted implementation is based on 
        the second case, which justify the `abs` in the implementation. 
        
        Non axi-symmetric lens: not yet implemented.
        
        """
        if p is None: p = self.p0
        
        if self.is_axisym:
            def wrapper(x, p):
                return abs(x - self.alpha((x,0.0), p)[0])
            
            options_default = {'maxiter': 1000, 'maxfev': 1000, 
                               'xatol': 1.49e-10, 'fatol':1.49e-10, 
                               'return_all':True, 'disp':False}            
            
            res = minimize(wrapper, 1.0, args=(p,), method='Nelder-Mead', 
                           options=HandlingDict(options).update_dict(options_default))

            if full_output:
                return res.x[0], res
            else:
                return res.x[0]
        else:
            # Not yet implemented
            return None

    def is_axi_symmetric(self, p=None, N=100, tol=1e-12, full_output= False, 
                         debug=False):
        """ Define numerically whether a model is axisymmetric or not.
        
        Parameters
        ----------
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
        N : int
            Sampling size of the circle on which the surface mass density is 
            computed.
        tol : double
            Define the numerical tolerance.
        full_output : bool
            If True, the method also returns intermediate results.
        debug : bool
            Print useful informations.            
        
        """   
        if p is None: p = self.p0
        
        if debug:
            debug_loc = locals()
            print ''
            print '####################'
            print '###  DEBUG MODE  ###'
            print '####################'
            print 'is_axi_symmetric()'
            print 'input parameters:'
            for debug_loc_label, debug_loc_value in debug_loc.items():
                if debug_loc_label != 'self' and debug_loc_label != 'debug':
                    print '\t {}: {}'.format(debug_loc_label, debug_loc_value)
            print ''

        r_range = linspace(0.001, 2.0, N)
        kappa_avg = array([self.kappa_azimuthally_averaged(r_range_k, p) for r_range_k in r_range])
        
        rand_phi = uniform(0.0,2.*pi)
        kappa_rand_angle = array([self.kappa((r_range_k*cos(rand_phi), r_range_k*sin(rand_phi)), 
                                              *p) for r_range_k in r_range])
        
        diff = abs(kappa_avg - kappa_rand_angle)
        res0 = min(diff)
        res1 = max(diff)    
        
        if full_output:
            if res1 < tol:            
                return True, (res0, res1)
            else:
                return False, (res0, res1)
        else:
            if res1 < tol:            
                return True
            else:
                return False                

    def backwards_source(self, (theta1, theta2), p=None, alpha=None):
        """ Give the source position at the origin of an image position.
        
        Parameters
        ----------
        theta1, theta2 : double
            Position in the lens plane where the method is evaluated.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
        alpha : callable (optional)
            Override the deflection angle method.
            
        """
        if p is None: p = self.p0
        
        if alpha is None: alpha = self.alpha
        
        if alpha is not None:
            if p is not None:
                a = alpha((theta1, theta2), p)
            elif p is None:
                a = alpha((theta1, theta2))
                
            beta1 = theta1 - a[0]
            beta2 = theta2 - a[1]
            return array([float(beta1), float(beta2)])
        else:
            return None
            
    def SDF(self, (theta1, theta2), (beta1, beta2), p=None):
        """ Compute the so-called Squared Deviation Function (SDF) 
        
        The SDF has been introduced by 
        Schramm, T. & Kayser, R, 1987, A&A 174, 361-364.
        
        Parameters
        ----------
        theta1, theta2 : double
            Image position in the lens plane.
        beta1,beta2 : double
            Source position in the source plane at the origin of the image 
            position.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.            
 
        """
        # WARNING: self.alpha might not accept (theta1, theta2) with theta1 
        # (resp. theta2) a NxN matrix.  
        if p is None: p = self.p0
        
        a = self.alpha((theta1, theta2), p) 
        sk1 = beta1 - theta1 + a[0]  
        sk2 = beta2 - theta2 + a[1]        
                       
        return (sk1**2 + sk2**2)**(0.5)

    def SDF_figure(self, (beta1, beta2), p=None, bounds=2.0, norm=None, 
                   mgrid=None, N=100, colorbar=False, clmap='magma_r', 
                   subplots_opts={}, axis_opts={}, plot_opts={}, plot=True, 
                   **kwargs):
        """ Illustrate the SDF in the lens plane with a nice figure. 
        
        Parameters
        ----------
        beta1, beta2 : double
            Source position in the source plane.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.  
        mesh_1, mesh_2 : array_like
            The x- and y-axis meshgrid. For instance:
            >>> sample = numpy.linspace(1,2,10)
            >>> mesh_1, mesh_2 = numpy.meshgrid(sample,sample)
        N : int
            Number of coutours for the contour-plot.
        images : [(x1,y1),(x2,y2),...] array_like
            Images positions in cartesian coordinates.
        critical_lines : list of array_like
            List of disjointed critical lines defined as Nx2 array_like
        caustics : list of array_like
            List of disjointed caustics defined as Nx2 array_like            
        figsize : 2-tuple
            Define the size of the figure. It uses Matplotlib convention.
        kwargs : dict
            Additional options passed to Matplotlib.pylab.contourf
            
        """
        if p is None: p = self.p0
        
        if mgrid is not None:
            mesh_1, mesh_2 = mgrid
        else:
            if not isiterable(bounds):
                xlim = (-abs(bounds),abs(bounds))
                ylim = (-abs(bounds),abs(bounds))  
            elif isiterable(bounds) and isiterable(bounds[0]):
                xlim = bounds[0]
                ylim = bounds[1]
            else:
                xlim = bounds
                ylim = xlim
            
            mesh_1, mesh_2 = meshgrid(linspace(xlim[0],xlim[1],N),
                                      linspace(ylim[0],ylim[1],N))
            
        sdf = self.SDF((mesh_1, mesh_2), (beta1, beta2), p) 
        
        # Norm and labels                        
        if norm is None and not axis_opts.has_key('set_xlabel'):
            set_xlabel = {'set_xlabel':{'xlabel':r'$\theta_x$','fontsize':20}}
        elif norm is not None and not axis_opts.has_key('set_xlabel'):          
            xlabel = r'$\theta_x / \theta_{\text{\small E}}$'
            set_xlabel = {'set_xlabel':{'xlabel':xlabel,'fontsize':20}}
            mesh_1 = mesh_1 / norm
        elif norm is not None:
            set_xlabel = {}
            mesh_1 = mesh_1 / norm 

        if norm is None and not axis_opts.has_key('set_ylabel'):
            set_ylabel = {'set_ylabel':{'ylabel':r'$\theta_y$','fontsize':20}}
        elif norm is not None and not axis_opts.has_key('set_ylabel'):          
            ylabel = r'$\theta_y / \theta_{\text{\small E}}$'
            set_ylabel = {'set_ylabel':{'ylabel':ylabel,'fontsize':20}}
            mesh_2 = mesh_2 / norm
        else:
            set_ylabel = {}
            mesh_2 = mesh_2 / norm            
            
        axis_opts = HandlingDict.merge_dicts(axis_opts, set_xlabel, set_ylabel)            
        
#        if (not axis_opts.has_key('set_xlabel') and 
#            not axis_opts.has_key('set_ylabel')):
#            labels = {'set_xlabel':{'xlabel':r'$\theta_x$', 'fontsize':20},
#                      'set_ylabel':{'ylabel':r'$\theta_y$', 'fontsize':20}}            
#            axis_opts = HandlingDict(axis_opts).update_dict(labels)        
            
        canvas,fig,ax1 = Graphics().build_figure((1,1),subplots_opts,axis_opts)

        ax1.hold(True)            
        _ = ax1.contourf(mesh_1, mesh_2, sdf, N, cmap=clmap, **plot_opts)
        
        # Colorbar
        if colorbar:
            cbar = Colorbar(sdf.flatten())
            _, fig, ax1 = cbar.add_colorbar(fig, ax1, n=11, clmap=clmap, 
                                            label=r'$\text{SDF}$', 
                                            level_min=0., full_output=True)
               
        if plot:
            return canvas.figure
        else:
            return canvas, fig, ax1
        
#        from matplotlib.pylab import figure, contourf, hold, show, plot, xlabel, ylabel
#        figure(figsize=figsize)
#        hold(True)
#        contourf(mesh_1, mesh_2, sdf, N, **kwargs)
#            
#            
#        plot(beta1,beta2, 'xr')
#        xlabel(r'$\theta_1$', fontsize=20)
#        ylabel(r'$\theta_2$', fontsize=20)        
#        show()
#
#        if images is not None:
#            for i in images:
#                ax1.plot(i[0],i[1], 'or')        
#        
#        if critical_lines:
#            for _cl in critical_lines:     
#                _cl = array(_cl)
#                ax1.plot(_cl[:,0], _cl[:,1], 'k')    
#                
#        if caustics:
#            for _ca in caustics:     
#                _ca = array(_ca)
#                ax1.plot(_ca[:,0], _ca[:,1], 'k')          

    def localMinimum1(self, (x0, y0), b12, p=None, options=None, 
                     full_output=False):
        """ Compute the position in lens plane which minimizes the SDF. 
        
        Parameters
        ----------
        x0, y0 : double
            Initial guess for the position.
        b12 : tuple
            Source position (b1,b2).
        p : array_like
            Model parameters. p overrides any p0 defined within the class.            
        options : dict
            Options passed to scipy.optimize.minimize.
        full_output : bool
            If True, the method also returns intermediate results.            
        
        """
        if p is None: p = self.p0
        
        options_default = {'maxiter': 500, 'maxfev': 1000, 
                           'xatol': 1.0e-08, 'fatol':1.0e-08, 
                           'return_all':False, 'disp':False}        
        if options is None:
            opts = options_default
        else: # complete the `options` dict with recommended default values
              # TODO: use the tools dedicated to handle dict.
            opts = {key:options.get(key, value) 
                    for key, value in options_default.items()}
                   
        res = minimize(self.SDF, (x0,y0), args=(b12, p), 
                       method='Nelder-Mead', options=opts)
        
        if full_output:
            return res.x, res
        else:
            return res.x
    
    @timeit    
    def images(self, src, p=None, 
               radius=2.0, density=15, tiling=None, center=[0.,0.],
               critical_curves_properties=None, 
               guess=None, forceTiling=False, 
               critical_curves=None, L=50, N_xtraPoints=3, subradius=None,
               caustics=None, proximity=False, subradius_crit=None,
               multi=False, options=None, 
               omitcore=None, checkNimgs=False,
               verbose=False, debug=False, full_output=False, **kwargs):
        """ Compute the lensed image positions of a given source position.
        
        The algorithm involves tiling the image and source planes, using 
        these tiles to determine both the number and approximate position of
        all lensed images. A numerical refinement is then perform to increase
        the precision on the posision. This algorithm follows the 
        recommendation of [1] and will be referred to as the `tiling 
        algorithm`.
        
        Parameters
        ----------
        src : array_like
            A source position. 
        tiling : 2-tuple
            Tiling parameters: size and density.
        guess : array_like
            Initial guesses for the image positions. If passed and 
            `forceTiling' is False, only a numerical refinement is performed.
        forceTiling : bool
            Force the apply of the tiling algorithm.
        critical_curves : list of array_like
            List of disjointed critical lines defined as Nx2 array_like 
        critical_curves_properties : dict
            Critical curves properties as returned by 
            CriticalCurves.properties().
        L : int
            Number max of vertices one draws out of the critical curves.
        N_xtraPoints : int
            Number of extra vertices per point on the critical curve.
        multi : bool
            If True, the method is parallelized over multi-cores.
        options : dict
            Options passed to scipy.optimize.minimize. 
        omitcore : double
            All images found in a disk or radius `omitcore' are discarded. 
        caustics : list of array_like
            List of disjointed caustics defined as Nx2 array_like  
        checkNimgs : bool
            If True, one performs several tests:
                a) check that the number of lensed images is consistent
                b) check  that the odd number theorem is verified
                c) check that the magnification theorem is verified
        proximity : bool
            If True adds a grid of vertices around the images of 
            the closest positions of the caustics w.r.t. the source.
        verbose : {True, False}, bool optional
            If True prints to stdout intermediate info.
            
        References
        ----------
        [1] Keeton, C. R., 2001, *Computational methods for gravitational 
        lensing*, URL: https://arxiv.org/abs/astro-ph/0102340

        """
        # gravlens p29: maximum level of subgrid recursion
        
#        TODO: create a class Image that aims to collect all the image 
#        properties and data. An instance of this class should be returned when
#        `full_output` is flagged True. Otherwise, we return only the numpy
#        array that contains the image coordinates.
#        
#        TODO: should check that all the method used rely on analytical 
#        implementation of psi, alpha, .... When it's not the case, one should
#        raise a warning, telling to the user the he needs to force the image
#        search to continue. This can be done with an argument called `crazy` 
#        or `live_dangerously`, for instance. 
#        
#        TODO: one should have a `quiet` mode which display no message when True
#        
#        TODO: when `guess` is not None and `forceTiling` is true, we should use
#        the tiling with `guess` as extra center of sub-grids with a dense 
#        sampling
        if debug: verbose = True
        if debug: print "Search the lensed image positions of the source {}".format(src)
        
        if p is None: p = self.p0
        
        center = array(center)
        
        default_radius = 2.0
        
        if tiling is None:
            tiling = (radius, density)
        
        if debug: print "   (1) Compute the guessed values (tiling) ...",

        if guess is not None and not forceTiling:
            img_pos = guess
            if debug: print "XXX"
        else:
            if critical_curves_properties is None:
#                if center is None:
#                    main_centroid = (0.,0.)
#                else:
#                    main_centroid = center
                main_centroid = center
                main_extent = tiling[0]
            else:
#                if center is None:
#                    main_centroid = critical_curves_properties.get('main_centroid')
#                else:
#                    main_centroid = center
                main_centroid = critical_curves_properties.get('main_centroid')                    
                    
                _extent = 1.5 * (array(critical_curves_properties.get('main_extent'))).max()
                
                if tiling[0] == default_radius:
                    main_extent = _extent
                else:
                    main_extent = tiling[0]

                  
            # TILING: first estimate of the image positions
            xmin, xmax, nx = (main_centroid[0]-main_extent, 
                              main_centroid[0]+main_extent, 
                              tiling[1])
            
            ymin, ymax, ny = (main_centroid[1]-main_extent, 
                              main_centroid[1]+main_extent, 
                              tiling[1])   
    
            _mesh = meshgrid(linspace(xmin,xmax,nx), linspace(ymin,ymax,ny))
            frame = column_stack((_mesh[0].flatten(), _mesh[1].flatten()))
    
            #L = 50 #number max of vertex we draw out of the critical lines.
            #N_xtraPoints = 3 #number of extra vertex 
    
            if critical_curves is not None:
                
                if critical_curves_properties is not None:
                    cl_size = critical_curves_properties.get('size')
                    if subradius is None:
                        cl_median_sep = critical_curves_properties.get('median_separation')
                    else:
                        cl_median_sep = [subradius for _ in critical_curves]
                else:
                    cl_size = [len(_) for _ in critical_curves]
                    cl_median_sep = [subradius for _ in critical_curves]
                
                angles_bounds = [(k*2.0*pi/N_xtraPoints,(k+1)*2.0*pi/N_xtraPoints) for k,h in enumerate(range(N_xtraPoints))]        
                vertex = empty([0,2])
                
                for k, (cl,s,sep) in enumerate(zip(critical_curves, cl_size, cl_median_sep)):
                    if s <= L:
                        vertex = vstack((vertex,cl[:,:]))
                        for bounds in angles_bounds:
                            angle = uniform(bounds[0],bounds[1],s)
                            radius = sep/3.0
                            vertex = vstack((vertex, cl + radius*column_stack((cos(angle),sin(angle)))))        
                    else:
                        _size = int(floor(s/L))
                        subcl = cl[::_size,:]
                        vertex = vstack((vertex,subcl))
                        
                        for bounds in angles_bounds:
                            angle = uniform(bounds[0],bounds[1],len(subcl))
                            radius = sep/3.0
                            vertex = vstack((vertex, subcl + radius*column_stack((cos(angle),sin(angle)))))
                points = vstack((frame, vertex))
            else:
                points = frame
            
#            if (proximity and critical_curves is not None and 
#                caustics is not None):
            if caustics is not None and critical_curves is not None:
                # we add a grid of vertices around the images of the closest 
                # positions of the caustics wrt to the source
                if subradius_crit is None:
                    subradius_crit = cl_median_sep
                else:
                    subradius_crit = [subradius_crit for _ in caustics]
                J = ceil(101**0.5)
                cc_index_closest_to_src  = array([closest_node(src, _ca) for _ca in caustics])
                #cc_points_closest_to_src = array([cc[_[0]] for _,cc in zip(cc_index_closest_to_src,caustics)])            
                cl_points_closest_to_src = array([cl[int(_[0])] for _,cl in zip(cc_index_closest_to_src,critical_curves)])
                for k, (posi,sep) in enumerate(zip(cl_points_closest_to_src,subradius_crit)):
                    grid_cl_closest = array(Meshgrid.get_circular(sep/3.0, center=posi, num=J)) 
                    points = vstack((points, grid_cl_closest))
                    
            if omitcore is not None and omitcore > 0.0:
                # Remove all points inside a disk of radius `omitcore`
                # Add the disk contour
#                if center is None:
#                    _center = zeros(2)
#                else:
#                    _center = array(center)
                    
                mask = ones(len(points), dtype=bool)
                mask[where(norm_fast(points-center) <= omitcore)] = False
                points = points[mask]                    
                    
                _angle_omit = linspace(0.,2.*pi,5*ceil(tiling[1]**0.5))
                _x_omit = omitcore * cos(_angle_omit) + center[0]
                _y_omit = omitcore * sin(_angle_omit) + center[1]
                
                points = vstack((points, array(zip(_x_omit,_y_omit))))
            
            delaunay = Delaunay(points)
            delaunay_index = delaunay.simplices
            delaunay_vertex = points[delaunay_index]
            
            triangles_imgs = [Triangle(*d) for d in delaunay_vertex]
            
            ###
            if omitcore is not None and omitcore > 0.0:
                _barry = array([norm_fast(array(_tr.barycenter())-center) for _tr in triangles_imgs])
                mask = ones(len(triangles_imgs), dtype=bool)
                mask[_barry < omitcore] = False
                
                delaunay_index = delaunay_index[mask]
                delaunay_vertex = delaunay_vertex[mask]
                triangles_imgs = [_t for _t,_m in zip(triangles_imgs,mask) if _m]
            
            sources = array([self.backwards_source(_,p) for _ in points])
            triangles_src = [Triangle(*d) for d in sources[delaunay_index]]
            inside_src = array([tr_src.contains(src, 0.0) for tr_src in triangles_src])
            triangle_with_images_index = where(inside_src)[0]  
            
            img_pos = array([triangles_imgs[_].barycenter() for _ in triangle_with_images_index])
            
            if debug: print "DONE."            
        
        # REFINEMENT
        if debug: print "   (2) Refinement ..."        
        if multi:
            if debug: print "         {} candidates are refined simultaneously".format(len(img_pos))
            MP = Multiprocessing(self.localMinimum1, img_pos, 
                                 func_extra_kwargs={'b12':src,'p':p, 
                                                    'options':options})
            # TODO: the second parameters for *.run(..., n, ...) should be restricted to the number maximumof available core
            img_pos_opt = MP.run(nprocs=min((available_cpu(),len(img_pos))), profile=False)
        else:
            img_pos_opt = []
            for j,im in enumerate(img_pos):
                if debug: print "         candidate {} on {}".format(j+1,len(img_pos))            
                image = self.localMinimum1(im, src, p, options=options)
                img_pos_opt.append(image) 
                
        # REMOVE DUPLICATE IF REQUIRED
        # FIXME: when they are very close, it cannot distinguish between the
        # images and remove a valid one.
        img_pos_opt = remove_duplicate(array(img_pos_opt))
        
        #print img_pos_opt.shape
        if debug: print "      DONE."        
        
        # OMITCORE
        if debug: print "   (3) Deal with omitcore ...",
        if omitcore:
            N_imgs_before_omitcore = img_pos_opt.shape[0]       
            img_pos_opt = array([img for img in img_pos_opt if norm_fast(img-center)>= omitcore])
            omit = max((1.0, N_imgs_before_omitcore - img_pos_opt.shape[0]))
            if debug: print "DONE."
        else:
            omit = 0 
            if debug: print "XXX"
           
         
        # CHECK IMAGES
        # THIS PART OF THE CODE IS TEMPORARILY IGNORED.
        # REASON: the self.check_images_number is not stable
        # For example, it cannot manage smooth and singular 
        if debug: print "   (4) Check the lensed image properties ...",
#        if checkNimgs and caustics is not None:
#            if len(img_pos_opt) == 0:
#                print 'No image found. None is returned.'
#                return None
#            
#            checkN = self.check_images_number(img_pos_opt, p, source=src, 
#                                              omit=omit, caustics=caustics, 
#                                              critics=critical_curves)
#            img_N_mismatch_due_to_tiling = checkN[1]  
#            
#            if verbose:
#                print ''
#                if checkN[0]:
#                    print 'The number of images ({}) of the source ({},{}) matches the theoretical expectation.'.format(img_pos_opt.shape[0], src[0], src[1])
#                else:
#                    msg = 'The number of images ({}) of the source ({},{}) does not match the theoretical expectation ({}) (`omitcore` is taken into account): `img_N_mismatch_due_to_tiling` = {}. Check the range or the density of `tiling_x` and/or `tiling_y`.'
#                    print(msg.format(img_pos_opt.shape[0], src[0], src[1], checkN[2], img_N_mismatch_due_to_tiling))           
#                
#            prop = self.image_properties(img_pos_opt, p=p) #, caustics=caustics, critics=critical_curves)
#            
#            if verbose:
#                if prop.get('oddNumberTheorem').get('oddNumberTheoremVerified'):
#                    print 'The odd Number Theorem is verified.'
#                else:
#                    print 'The odd Number Theorem is NOT verified. There might be missing images.' 
#                    
#                if prop.get('magnificationTheorem').get('magnificationTheoremVerified'):
#                    print 'The magnification Theorem is verified.'
#                else:
#                    print 'The magnification Theorem is NOT verified.'
#                    
#            if debug: print "DONE."
#        else:
#            checkN = None
#            img_N_mismatch_due_to_tiling = None 
#            prop = None
#            if debug: print "XXX"
        if debug: print "XXX"
        
                
            
        # FIG OUTPUT
        if debug: print "   (5) Full outputs are generated ...",
        if full_output:            
            tiling_output = {}
            
            _p_imgs = []
            #_patches_imgs = []
            #patches_imgs = []
            
            _p_src = []            
            #_patches_src = []            
            #patches_src = []  

            for k,i in enumerate(triangle_with_images_index):
                polygon_imgs = Polygon(triangles_imgs[i].v, True) 
                _p_imgs.append(polygon_imgs)
                #_patches_imgs = PatchCollection(_p_imgs, alpha=1.0)
                #_patches_imgs.set_facecolors(Colors().blue)
                #patches_imgs.append(_patches_imgs)
                
                polygon_src = Polygon(triangles_src[i].v, True)
                _p_src.append(polygon_src)
                #_patches_src = PatchCollection(_p_src, alpha=0.7)                
                #_patches_src.set_facecolors(Colors().blue)
                #patches_src.append(_patches_src)

            polygons = []
            for _delau in delaunay_vertex:
                polygons.append(Polygon(_delau, True))
                
            tiling_output['polygons'] = polygons
            tiling_output['polygon_imgs'] = _p_imgs #patches_imgs
            tiling_output['polygon_src'] = _p_src #patches_src 
            tiling_output['delaunay_vertices'] = delaunay_vertex
            tiling_output['triangles_src'] = [triangles_src[i] for i in triangle_with_images_index]
            tiling_output['triangles_img'] = [triangles_imgs[i] for i in triangle_with_images_index ]
            if debug: print "DONE."
        else:
            if debug: print "XXX"  

        # OUTPUT
        if debug: print "   (6) Returns the results ... DONE."        
        if full_output:
#            return img_pos_opt, {'omit':omit, 
#                                 'img_N_mismatch_due_to_tiling':img_N_mismatch_due_to_tiling, 
#                                 'checkN':checkN,
#                                 'image_properties':prop}, fig_output
            return img_pos_opt, tiling_output
        else:
            return img_pos_opt        
        
        
    def images_old(self, (beta1, beta2), p=None, 
               tiling_x=(-2.,2.,15), tiling_y=(-2.,2.,15), omitcore=None, 
               iterative=False, multi=False, options=None, checkNimgs=False, 
               checkNimgs_opts={}, caustics=None, critics=None, 
               verbose=False, full_output=False):
        """
        When an image tile crosses a critical line, one should
        use a sub-tiling to see wether there are multiple images. 
             
        """
#       TODO: image devrait pouvoir accepter le tiling comme argument. Cela permettrait
#       de ne pas le recalculer à pour chaque configurations d'images calculées, i.e. pour 
#       chaque source d'une séquence.
#
#       FIXME: when there is only one image, removeDuplicate() raise an error 
#       about indexing.
#
#       FIXME: when iterative is set to True but checkNimgs are False and 
#       caustics are None, then `checkN' is set to None at line 698 and 
#      `checkN[0]` when defining while_stop_condition raises an 'NoneType' 
#       exception. 

        if p is None: p = self.p0
        
        (xmin,xmax,xN) = tiling_x
        (ymin,ymax,yN) = tiling_y
        
        tiling_x_radius_max = (sum([xmin**2, xmax**2]))**(0.5)
        tiling_y_radius_max = (sum([ymin**2, ymax**2]))**(0.5)
        
        if omitcore > maximum(tiling_x_radius_max,tiling_y_radius_max):
            # No images can be found due to omitcore
            if full_output:
                return array([]), 0, 0, True
            else:
                return array([])

        if iterative:
            assert maximum(xN,yN) < 32, 'When `iterative` is True, it does not make sense to adopt a very dense tiling to start. xN and yN should be < 32, 15 is a good guess.'
            
        
        def backwards_source_wrapper(p,vi):
            theta1, theta2 = vi            
            return self.backwards_source((theta1, theta2), p)
            
        def SDF_wrapper(x, b, p):
            theta1, theta2 = x
            return self.SDF((theta1, theta2), b, p)
        
        xmin = float(xmin); xmax = float(xmax); 
        ymin = float(ymin); ymax = float(ymax);
        
        threshold = True
        count = 0
        factor = 1.5
        if iterative: checkNimgs = True
        
        while threshold: 
            if count != 0:
                xN *= factor; xN = int(xN) if int(xN)%2!=0 else int(xN)+1;
                yN *= factor; yN = int(yN) if int(yN)%2!=0 else int(yN)+1;
                      
            tiling = GLCaustics.GLCaustics(backwards_source_wrapper, p, \
                                            xmin = xmin, xmax = xmax, nx = xN, \
                                            ymin = ymin, ymax = ymax, ny = yN)
            
            img_pos, tile_index = tiling.images([beta1,beta2],0., full_output=True) 
            
#            ## Sub-tiling-->
#            clINtiles = array([self._tile_covers_CL(tiling._image_tr[ti], p) for ti in tile_index])
#            
#            img_pos_TOkeep = [img_pos_keep for refine,img_pos_keep in zip(clINtiles,img_pos) if not refine]
#            tilesTOrefine = [tiling._image_tr[ti] for refine,ti in zip(clINtiles,tile_index) if refine]
#
#            print 'Number of tile to refine:', len(tilesTOrefine)
#            if len(tilesTOrefine) > 0:
#                subtiles = [tiling.subtiling(_tri, N=20) for _tri in tilesTOrefine]
#                new_img = []
#                new_index = []
#                for _sub in subtiles:
#                    _ = tiling.images([beta1,beta2], 0., src_trs=_sub[1], img_trs=_sub[0], full_output=True)
#                    new_img.append(_[0][0])
#                    new_index.append(_[1][0])
#                
#                img_pos = vstack((array(img_pos_TOkeep), array(new_img)))
#            else:
#
#                print 'no refinement required'
#            ## <--

            
            if multi:
                MP = Multiprocessing(self.localMinimum1, img_pos, 
                                     func_extra_kwargs={'b12':(beta1, beta2),'p':p})
                img_pos_opt = MP.run(nprocs=min((available_cpu(),len(img_pos))), profile=False)
            else:
                img_pos_opt = []
                for im in img_pos:               
                    image = self.localMinimum1(im, (beta1,beta2), p, options=options)
                    img_pos_opt.append(image) 
                    
            img_pos_opt = remove_duplicate(array(img_pos_opt))    
                                           
            if omitcore:
                N_imgs_before_omitcore = img_pos_opt.shape[0]
                img_pos_opt = array([img for img in img_pos_opt if norm_fast(img)>= omitcore])
                omit = N_imgs_before_omitcore - img_pos_opt.shape[0]
            else:
                omit = 0
            
            if checkNimgs and caustics is not None:
                # FIXME: warning!! there is a case which is not taken into account.
                # Consider that the range of `tiling_#` is smaller than one or several
                # images, or consider the `tiling_#` is not dense enough and miss
                # image(s) which are very close to each other (close to a critics).            
                # Let's say that k images cannot be found due to the tiling. 
                #
                # In addition, consider that omitcore is larger than all the N 
                # theoretical images but not larger than at least one point of the 
                # tiling. It results that no images will be found thanks to the 
                # omitcore, as expected. 
                #
                # However, the checkNimgs, which takes into account the
                # omitcore size, will return a (False, -k) instead of a (True, 0).
                # Indeed, omitcore >> implies that none of the N theoretical images 
                # should be found and the correct answer for checkN is (True, 0). 
                # However, the result of the parameter `omit` in the `if omitcore:` 
                # here above is N-k and not N since the img_pos_opt contains only 
                # N-k images due to the fact that the too small or not dense enough
                # tiling ignore k images. 
                #
                # Even it's easy to know if image(s) has been ignored due to the 
                # tiling thanks to the parameter `img_ignored_due_to_tiling`, how 
                # to know whether the missing image(s) is radially larger than the
                # omitcore or not . If it does, than the image would not have been 
                # discarded due to omitcore and checkN should correctly return 
                # (False, j) with j <= k the number of the related images. 
                # Conversely, (True, 0) becomes the expected result for checkN.
                #
                # The method `image_properties` would be really helpful since one
                # could compare the properties of the images found and deduce part
                # of the properties of the j missing j images without computing 
                # their exact position. Thus, one might be able to decide whether 
                # the j missing images are radially larger than the omitcore or 
                # not. It would also be helpful if the missing images are inner
                # images (than missing to too small density of the tiling):
                # for ex. when xN and/or yN are very small implying that the central
                # image is not found. If omitcore > angular distance of this central
                # image, than even the image would have been found, it would have 
                # been discared --> checkN should be (True, 0). Conversely, if 
                # omitcore < angular distance of this central image, than (False,-1)
                # is the expected result for checkN since this image would NOT have
                # been discarded due to omitcore.
                #
                checkN = self.check_images_number(img_pos_opt, p, 
                                                  source=(beta1,beta2),
                                                  omit=omit,
                                                  caustics=caustics, 
                                                  critics=critics)

                img_N_mismatch_due_to_tiling = checkN[1]    
                
#                if checkN[0]:
#                    # The number of images found matches the theoretical expectation
#                    img_N_mismatch_due_to_tiling = checkN[1]
#                elif not checkN[0]:
#                    # Mismatch between the number of images found and the theoretical expectation
#                    img_N_mismatch_due_to_tiling = checkN[1]
#                    #msg = 'The number of images ({}) of the source ({},{}) does not match the theoretical expectation ({}) (`omitcore` is taken into account): `img_N_mismatch_due_to_tiling` = {}. Check the range or the density of `tiling_x` and/or `tiling_y`.'
#                    #print(msg.format(img_pos_opt.shape[0], beta1, beta2, checkN[2],
#                    #                 img_N_mismatch_due_to_tiling))
#                    pass
            else:
                checkN = None
                img_N_mismatch_due_to_tiling = None
            
            
            if not iterative:
                threshold = False
            else:
                #print 'count {} --> (xN, yN)'.format(count), xN, yN
                count += 1
                # condition to stop the while-loop
                while_stop_condition = (maximum(xN,yN)>checkNimgs_opts.get('density_max',101)) | (checkN[0]) #| checkN[1]>0 #| count > 0
                
                if while_stop_condition: 
                    threshold = False
        
        if checkNimgs and not checkN[0] and verbose:
            msg = 'The number of images ({}) of the source ({},{}) does not match the theoretical expectation ({}) (`omitcore` is taken into account): `img_N_mismatch_due_to_tiling` = {}. Check the range or the density of `tiling_x` and/or `tiling_y`.'
            print(msg.format(img_pos_opt.shape[0], beta1, beta2, checkN[2], img_N_mismatch_due_to_tiling))
            print(count-1, maximum(xN,yN))
            
        if full_output:
            return img_pos_opt, omit, img_N_mismatch_due_to_tiling, checkN
        else:
            return img_pos_opt
        
    def image_properties(self, images, p=None, omitcore=False):   
        """
        UNDER CONSTRUCTION
        
        Method which should return all the properties related to the images:
            + type (I, II or III): DONE
            + parity: DONE
            + position wrt critics (inside-or-outside the tangential/radial CL)
            + amplification: DONE
            + ... ?
        """
        if p is None: p = self.p0
        
        results = {}
        
        N = len(images)
        
        imageType = []
        nI = 0
        nII = 0
        nIII = 0
        
        if omitcore:
            N += 1
            nIII += 1        
        
        parity = zeros(N)
        mu = zeros_like(parity)        
        tau = zeros_like(parity)
   
        # Image types, parity, tau, ...  
        for k, img in enumerate(images):
            A = self.jm_lens_mapping(img, p)
            detA = det(A)
            traceA = trace(A)
            
            mu[k], parity[k] = self.amplification(img, p, parity=True)
            tau[k] = self.tau(img, p)
            
            if detA > 0 and traceA > 0:
                imageType.append('I')
                nI += 1
            elif detA > 0 and traceA < 0:
                imageType.append('III')
                nIII += 1
            elif detA < 0:
                imageType.append('II')
                nII += 1
            else:
                imageType.append(None)
                
        if omitcore:
            imageType.append('III') 
            mu[-1] = 0.0
            parity[-1] = 1.0
            tau[-1] = 1000.               
        
        results['imageType'] = imageType
        results['parity'] = parity
        results['amplification'] = mu        
        
        # Odd-number theorem check
        n = nI + nII + nIII
        oddNumberTheorem = {'nI >= 1':False, 'n < inf': False, 
                            'nI + nIII = 1 + nII': False, 
                            'n = 1 + 2nII': False, 'nII >= nIII': False, 
                            'even = odd + 1':False}
        
        if nI >= 1: oddNumberTheorem['nI >= 1'] = True
        if n < inf: oddNumberTheorem['n < inf'] = True 
        if nI + nIII == 1 + nII: oddNumberTheorem['nI + nIII = 1 + nII'] = True   
        if n == 1 + 2*nII: oddNumberTheorem['n = 1 + 2nII'] = True
        if nII >= nIII: oddNumberTheorem['nII >= nIII'] = True 
        if parity.sum() == 1: oddNumberTheorem['even = odd + 1'] = True         
        
        if all(oddNumberTheorem.values()): 
            oddNumberTheorem['oddNumberTheoremVerified'] = True
        else:
            oddNumberTheorem['oddNumberTheoremVerified'] = False
        
        results['oddNumberTheorem'] = oddNumberTheorem
        
        # Magnification theorem
        magnificationTheorem = {}
        magnificationTheorem['theorem'] = ("Image which arrives first is of "
                                           "type I and appears brither " 
                                           "(or equally bright) than the " 
                                           "source.")
        
        firstImageIndex = argwhere(tau == tau.min())[0][0]
        magnificationTheorem['firstImageIndex'] = firstImageIndex
        magnificationTheorem['firstImageAmplification'] = mu[firstImageIndex]
        magnificationTheorem['firstImageType'] = imageType[firstImageIndex]
        if imageType[firstImageIndex] is 'I' and mu[firstImageIndex] >= 1.0:
            magnificationTheorem['magnificationTheoremVerified'] = True
        else:
            magnificationTheorem['magnificationTheoremVerified'] = False
            
        results['magnificationTheorem'] = magnificationTheorem
        
        return results
    
    def print_image_properties(self, image_properties=None, images=None, 
                               p=None, omitcore=False):
        """
        """
        if image_properties is None and images is not None:
            image_properties = self.image_properties(images, p, omitcore)

        print '######################'
        print '## Image properties ##'
        print '######################'            
        for key,val in image_properties.items():
            if isinstance(val,dict):
                print key
                for _k,_v in val.items():
                    print '\t {} --> {}'.format(_k,_v)
            else:
                print '{} --> {}'.format(key,val)   
                
        return None
    

    def check_images_number(self, images, p=None, source=None, omit=0, 
                            caustics=None, critics=None):
        """
        We check that we have found all the images for the source.
        
        omit : if the parameter `omitcore` has been used in the method 
        `images()`, than we have to take account of the fact that the number of 
        images is delibarately smaller than the theoretical one. Thus, the 
        parameter `omit` allows to compare the theoretical number of images
        minus the number of delibarately omitted ones with the number of images
        in the matrix `images`. 
        
        """
#       TODO: from the matrix images, if the number does not correspond to the 
#       theoretical expectation, one could determine which image(s) is missing
#       and/or is duplicated thanks to the image type and their positions with
#       respect to the critical curves.
        
        if p is None: p = self.p0
        
        N_imgs = images.shape[0]
        
        if source is None:
            if images.size == 2: #then there is only 1 image with 2 components
                source = self.backwards_source(images, p)
            else:
                source = array([self.backwards_source(img, p) for img in images]).mean(axis=0)
        else:
            # One should check that the type and size of source is valid. 
            pass
                
        if caustics is not None:
            N = self.N_lensed_images(tuple(source), caustics)   
            print N                     
        elif caustics is None and critics is not None:
            print '`caustics` is None'
            return -inf
        elif caustics is None and critics is None:
#                self.critical_lines(p, radius=2.0, density=21, n_iterations=7, 
#                                    refinement=True, nprocesses=8, separate=True)
#                self.caustic_curves
            print 'Both `caustics` and `critics` are None'
            return -inf        
        
        if (N-omit) == images.shape[0]:
            return (True, 0, N-omit)
        elif (N-omit) != N_imgs:
            # > 0 ==> there are too much images
            # < 0 ==> there are missing images
            return (False, N_imgs - max([N-omit,0]), N-omit)

    @Deprecated(None,'Dead function which has been removed: return None.')    
    def psi_second_derivative(self, (theta1, theta2), p=None):
        """
        k0 = mpmath.diff(lambda x,y: func_test(x,y,p), (t1, t2), (2,0))
        """
        if p is None: p = self.p0
        
        if self.analytic.get('alpha'):
            
            #w = lambda x: self.alpha_1_1_wrapper(x, theta2, p)
            #print type(w)
            #print w(theta1)
            #print self.analytic
            #psi_11 = mpmath.diff(w, theta1)
            #print psi_11
            psi_11 = derivative(self.alpha_1_1_wrapper, theta1, n=1, args=(theta2, p), dx=1e-8)
                                   
            psi_22 = derivative(self.alpha_2_2_wrapper, theta2, n=1, args=(theta1, p), dx=1e-8) 
            psi_12 = derivative(self.alpha_1_2_wrapper, theta2, n=1, args=(theta1, p), dx=1e-8) 
            psi_21 = derivative(self.alpha_2_1_wrapper, theta1, n=1, args=(theta2, p), dx=1e-8)
            return array([[float(psi_11),float(psi_12)],[float(psi_21),float(psi_22)]]) 
        else:
            return None

    @Deprecated('jm_lens_mapping')  
    def magnificationTensor(self, (theta1, theta2), p=None):
        """
        """
        if p is None: p = self.p0
        
        if self.analytic.get('alpha'):
            psi_ij = self.psi_second_derivative((theta1, theta2), p)
            return identity(2)-psi_ij
        else:
            return None     

    def jm_lens_mapping(self, (theta1, theta2), p=None):
        """ The Jacobi matrix of the lens mapping.
        
        Parameters
        ----------
        theta1, theta2 : double
            Position in the lens plane where the method is evaluated.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
        
        Returns
        -------
        jm_lens_mapping : ndarray
            The Jacobi matrix of the lens mapping.
            
        Notes
        -----
        Must return a numpy array (to keep consistency with __add__).
        
        """
        if p is None: p = self.p0
        
        if self.jm_alpha_mapping is not None and p is not None:
            return identity(2) - self.jm_alpha_mapping((theta1,theta2), p)
        elif self.jm_alpha_mapping is not None and p is None:
            return identity(2) - self.jm_alpha_mapping((theta1,theta2))        
        else:
            return None            

        
    def amplification(self, (theta1, theta2), p=None, parity=False):
        """The magnification is quantified by the inverse of the Jacobian
        matrix.
        
        Parameters
        ----------
        theta1, theta2 : double
            Position in the lens plane where the method is evaluated.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
        parity : bool
            Parity of the image. The parity is by default 'False'.
        
        Returns
        -------
        mu : float
            The magnification at a given position in the lensplane.

        """
        if p is None: p = self.p0
        
        A = self.jm_lens_mapping((theta1,theta2), p)
        #A = self.magnificationTensor((theta1, theta2), p)
        mu_signed = 1./det(A)
        if parity:
            return (abs(mu_signed), sign(mu_signed))
        else:
            return abs(mu_signed)

    def amplification_imgconfig(self, images, p=None, parity=False):
        """ The magnification is computed for a give image configuration.
        
        Parameters
        ----------
        images : array_like
            Image position cumputed for a given lens model for a given source
            position.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
        parity : bool
            Parity of the image. The parity is by default 'False'.
        
        Returns
        -------
        mu : ndarray
            The magnification for the given image configuration.
            
        """
        if p is None: p = self.p0
        
        mu = [self.amplification((img[0], img[1]), p, parity=parity) for img in images]
        
        if parity:
            return array([prod(sa) for sa in mu])
        else:
            return array(mu)

        
    def tau(self, (theta1,theta2), p=None):
        """
        tau = extra_light_travel_time in units of time scale t0.
        """
        if p is None: p = self.p0
        
        psi_i = self.psi((theta1, theta2), p)
        alpha_i = self.alpha((theta1, theta2), p)
        return 0.5*(alpha_i[0]**2 + alpha_i[1]**2) - psi_i  
    
    def fermat_potential(self, (theta1,theta2), (beta1,beta2), p=None):
        """Computes the fermat potential for a given source at the lens
        position theta.
        
        Parameters
        ----------
        theta1, theta2 : double
            Position in the lens plane where the method is evaluated.
        beta1, beta2 : double
            Source position in the source plane.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
        
        Returns
        -------
        fermat_potential : float
            The fermat potential at a given source position, at the position
            theta in the lens plane.

        """
        if p is None: p = self.p0
        
        psi_i = self.psi((theta1, theta2), p)

        return 0.5*((theta1-beta1)**2 + (theta2-beta2)**2) - psi_i    
    
    def fermat_potential_2dmap(self, src, bounds, p=None, N=50, norm=None, 
                               clmap='jet', subplots_opts=None, plot_opts=None, 
                               axis_opts=None, plot=True, **kwargs):
        """ Plot a 2d map of the Fermat potential.
        """      
        if not isiterable(bounds):
            xlim = (-abs(bounds),abs(bounds))
            ylim = (-abs(bounds),abs(bounds))  
        elif isiterable(bounds) and isiterable(bounds[0]):
            xlim = bounds[0]
            ylim = bounds[1]
        else:
            xlim = bounds
            ylim = xlim        
#        if not isiterable(bounds):
#            bounds = (-abs(bounds),abs(bounds)) 
            
        spanx = linspace(xlim[0], xlim[1], N)
        spany = linspace(ylim[0], ylim[1], N)        
        mesh_1, mesh_2 = meshgrid(spanx, spany)
        sampling = array(zip(mesh_1.flatten(),mesh_2.flatten()))
       
        fermat = array([self.fermat_potential(_pos, src) for _pos in sampling])
        fermat = fermat + abs(fermat.min())

        if subplots_opts is None: subplots_opts = {}
        if axis_opts is None: axis_opts = {}
        if plot_opts is None: plot_opts = {}

        # Norm and labels                        
        if norm is None and not axis_opts.has_key('set_xlabel'):
            set_xlabel = {'set_xlabel':{'xlabel':r'$\theta_x$','fontsize':20}}
        elif norm is not None and not axis_opts.has_key('set_xlabel'):          
            xlabel = r'$\theta_x / \theta_{\text{\small E}}$'
            set_xlabel = {'set_xlabel':{'xlabel':xlabel,'fontsize':20}}
            mesh_1 = mesh_1 / norm
        elif norm is not None:
            set_xlabel = {}
            mesh_1 = mesh_1 / norm
            
            
        if norm is None and not axis_opts.has_key('set_ylabel'):
            set_ylabel = {'set_ylabel':{'ylabel':r'$\theta_y$','fontsize':20}}
        elif norm is not None and not axis_opts.has_key('set_ylabel'):          
            ylabel = r'$\theta_y / \theta_{\text{\small E}}$'
            set_ylabel = {'set_ylabel':{'ylabel':ylabel,'fontsize':20}}
            mesh_2 = mesh_2 / norm
        else:
            set_ylabel = {}
            mesh_2 = mesh_2 / norm
      
        # Update axis_opts
        axis_opts = HandlingDict.merge_dicts(axis_opts, set_xlabel, set_ylabel)                                             

        canvas,fig,ax1 = Graphics().build_figure((1,1),subplots_opts,axis_opts) 
        
        _ = ax1.contour(mesh_1, mesh_2, fermat.reshape(mesh_1.shape), N, 
                         cmap=clmap)
        Colorbar(fermat).add_colorbar(fig, ax1, label=r'$\tau(\boldsymbol{\theta},\boldsymbol{\beta})$', clmap=clmap)                                             

        if plot: 
            return canvas.figure
        else:
            return canvas, fig, ax1    

    @Deprecated('time_delays','Dead function which has been removed: return None.')
    def time_delays_old(self, image_positions, p=None):
        """
        """       
        if p is None: p = self.p0
        
        tau = []
        for i in image_positions:
            tau.append(self.tau(i, p))
        tau = array(tau)    

        argmin_tau = argmin(tau)

        TD = []
        for t in tau:
            TD.append(t - tau[argmin_tau])
      
        return array(TD)
        
    def time_delays(self, image_positions, p=None, threshold=None):
        """
        """
        if p is None: p = self.p0
        
        if threshold is None or threshold:
            threshold = 1.0e-06
        elif not threshold:
            threshold = 0.0    
            
        if not isinstance(image_positions, list):
            image_positions = [image_positions]
            
        res = []
        for imgs in image_positions:    
            tau = array([self.tau(i, p) for i in imgs])
            min_tau = tau.min(axis=0)
            TD = array([(t - min_tau) if (t - min_tau)>threshold else 0.0 for t in tau]) 
            
            if len(TD) == 2 and abs(TD).min() == 0.0:
                # TD has only 1 non-zero value, which indicates that 
                # `image_positions` was composed of only 2 lensed image positions
                # leading to only 1 time delay.
                TD = float(TD[where(TD != 0.0)])
                
            res.append(TD)
        
        if len(res) == 1:
            return res[0]
        else:
            return res
        
    def time_delay_ratios(self, td1, td2):
        """
        """
        temp = [[htd/td for htd,td in zip(htds,tds) if td!=0] 
                if isiterable(htds) else htds/tds 
                for htds,tds in zip(td1,td2)]
        
        res = [(mean(_td), std(_td)) 
               if isiterable(_td) else _td 
               for _td in temp]
        
        return res        
        

    def _mu_vertex(self, tr, p=None):
        """
        Return the (inverse of?) amplification at the 3 vertex positions of the given 
        triangle `tr`.
        """
        if p is None: p = self.p0
        
        w = [self.jm_lens_mapping(pos, p) for pos in tr]
        return [w[0][0,0]*w[0][1,1] - w[0][0,1]*w[0][1,0], 
                w[1][0,0]*w[1][1,1] - w[1][0,1]*w[1][1,0],
                w[2][0,0]*w[2][1,1] - w[2][0,1]*w[2][1,0]]        

    def _tile_covers_CL(self, tr, p=None):
        """
        Determine if the triangle `tr` covers a critical line or not.
        """
        if p is None: p = self.p0
        
        res = sign(self._mu_vertex(tr, p)).sum()
        if res == 3. or res == -3:
            return False
        else:
            return True

        
    def _tile_covers_CL_new(self, points, vertex, p=None):
        """
        """
        if p is None: p = self.p0
        
        A = [self.jm_lens_mapping(pos, p) for pos in points]
        detA = array([a[0,0]*a[1,1] - a[0,1]*a[1,0] for a in A])
        
        return abs(sum(sign(detA[vertex]),axis=1)) != 3
    
    def _cl_crosses_tile(self, detA):
        """
        detA = 1x3 numpy array or Nx2 numpy array
        """
        if detA.ndim == 1:
            return abs(sum(sign(detA), axis=0)) != 3
        elif detA.ndim == 2:
            return abs(sum(sign(detA), axis=1)) != 3
    
    def _detA(self, points, p=None):
        """
        """
        if p is None: p = self.p0
        
        A = [self.jm_lens_mapping(pos, p) for pos in points]
        detA = array([a[0,0]*a[1,1] - a[0,1]*a[1,0] for a in A])
        
        return detA
        
            
    @staticmethod
    def _barycenter(tr):
        return sum(tr, axis=0)/3. 
    
    def _sub_tiling(self,(tr, detaf), N, K, angle_threshold, p=None):
        """        
        Contruct a grid inside the triangle tr, compute the det(A) at each
        grid's node and return the barycenter of each sub triangle that 
        contains a CL, all the sub triangles with the index locating those used
        for the barycenter and the det(A) of the sub triangles vertex.
        
        tr: triangles vertex coordinates
        detaf: det(A) at the 3 vertex
        
        N: number of extra vertex inside the triangle
        K: number of extra vertex on the triangle's edge
        
        angle_threshold: a sub triangle with min(angle) < angle_threshold is 
                         discarded. It avoids slivered triangles
        p: model parameters        
        """
        if p is None: p = self.p0
        
        vertex = vstack((tr, random_points_inside_triangle(tr, N), 
                         points_on_triangle_edge(tr, K, vertex=False)))
        sub_detA = append(detaf, self._detA(vertex[3:], p))
        
        try:
            sub_d = Delaunay(vertex)
        except:
            print 'Delaunay? nope !!!'
            return None
        
        _sub_triangles = vertex[sub_d.simplices]                    
        _sub_detA = sub_detA[sub_d.simplices]  
        
        if angle_threshold is not None:
            not_slivered_tr = triangles_filtering(_sub_triangles, angle_threshold)
            _sub_triangles = not_slivered_tr[0]
            _sub_detA = _sub_detA[not_slivered_tr[1]]   
        
        # Indices of tiles crossed by the CL
        _sub_cl = self._cl_crosses_tile(_sub_detA) 
        temp = array([Model._barycenter(_tr_) for _tr_ in _sub_triangles[nonzero(_sub_cl)]])
        
        return temp, _sub_triangles, _sub_cl, _sub_detA    
    
    #@timeit
    def tiling_new(self, points, p=None, N=10, K=3, iteration=1, 
                   angle_threshold=None, multi=False, nprocs=1,
                   full_output=False, debug=False):
        """       
        """        
        if p is None: p = self.p0
        
        # First filtering
        _d = Delaunay(points)
        _triangles = points[_d.simplices]
        A = [self.jm_lens_mapping(pos, p) for pos in points]
        detA = array([a[0,0]*a[1,1] - a[0,1]*a[1,0] for a in A])
        _cl = self._cl_crosses_tile(detA[_d.simplices])  #index_cl_crossed
        
        # Refinement
        triangles_filtered = _triangles[nonzero(_cl)]
        detA_filtered      = detA[_d.simplices][nonzero(_cl)]
                
        triangles_total = _triangles.copy()
        cl_covered_total = zeros(triangles_total.shape[0], dtype=bool)
        
        BC_total = empty([0,2])
        temp_triangles_filtered = empty([0,3,2])
        temp_sub_detA = empty([0,3])
        
        if not isinstance(N,list):
            N = [N] * iteration
        else:
            assert len(N) == iteration, 'if N is a list of integer, its length must be equal to `iteration`'
            
        if not isinstance(K,list):
            K = [K] * iteration
        else:
            assert len(K) == iteration, 'if K is a list of integer, its length must be equal to `iteration`'            
            
        # Iterations
        for i,_N,_K in zip(range(iteration), N, K):
            if debug: print 'iteration: {}/{}'.format(i+1,iteration)
            
            MP = Multiprocessing(self._sub_tiling,zip(triangles_filtered, detA_filtered), 
                                 {'N':_N, 'K':_K, 'angle_threshold':angle_threshold,
                                  'p':p})
            res = MP.run(nprocs=nprocs, debug=debug) 
            
            for part in res:
                triangles_total = concatenate((triangles_total,part[1]))
                  
                if i < iteration-1:
                    cl_covered_total = append(cl_covered_total, zeros(part[2].shape[0], dtype=bool))
                else:
                    cl_covered_total = append(cl_covered_total, part[2])
                    if part[0].shape[0] != 0:
                        BC_total = vstack((BC_total, part[0]))
                        
                if iteration > 1:
                    temp_triangles_filtered = concatenate((temp_triangles_filtered,
                                                           part[1][nonzero(part[2])]))
                    temp_sub_detA = vstack((temp_sub_detA, part[3][nonzero(part[2])]))                        

            triangles_filtered = temp_triangles_filtered
            detA_filtered = temp_sub_detA
            
            temp_triangles_filtered = empty([0,3,2])
            temp_sub_detA = empty([0,3])            

        if full_output:
            return BC_total, triangles_total, cl_covered_total
        else:
            return BC_total
    
    @timeit
    def tiling(self, points, p=None, N=0, processes=8, full_output=False, debug=False):
        """
        sampling: number of points we want for the curve. (not yet implemented)
        """
        if p is None: p = self.p0
        
        _d = Delaunay(points)
        _triangles = points[_d.simplices]
        
        ###
        #_t0 = time.time()
        
        #_cl = self._tile_covers_CL_new(points, _d.simplices, p)
        
        A = [self.jm_lens_mapping(pos, p) for pos in points]
        detA = array([a[0,0]*a[1,1] - a[0,1]*a[1,0] for a in A])
        #detA_struct = detA[_d.simplices]
        _cl = self._cl_crosses_tile(detA[_d.simplices])

        if N == 0:
            BC0 = array([Model._barycenter(tr) for tr in _triangles])
            return BC0, _triangles, _cl
        
        triangles0 = _triangles.copy()
        #cl0 = _cl.copy()        
        
        if full_output:
            triangles_total = triangles0.copy()
               
        #vertex_already_evaluated = vstack((empty([0,2]), points))
        
        for i in xrange(N): 
            # TODO: one could go a step further in the optimization. 
            # For a given iteration, we filter the triangles that cover a CL from the previous iteration, 
            # then compute their centroid and use them as additional vertex, 
            # construct the new Delaunay triangles, and compute the mu at the 
            # vertex (using the index to rebuild the Delaunay triangles).
            # However, even if mu is computed at the vertex (and not for every triangles, implying redundancy evaluations)
            # part of the vertex have already been considered during the previous iteration.
            # If we keep a trace between the iteration, one could reduce again the 
            # number of self.jm_lens_mapping evaluations.
            


            if debug:
                start = time.time()
                now = time.localtime()
                now_str = '{}h{}m{}s'.format(now.tm_hour, now.tm_min, now.tm_sec)
                print '{}: iteration {} --> '.format(now_str, i),            
            
            _triangles_filtered = _triangles[nonzero(_cl)]
            _BC = array([Model._barycenter(tr) for tr in _triangles_filtered])
            
            ###
#            _detA_filtered = detA_struct[nonzero(_cl)]
#            
#            A_bc = [self.jm_lens_mapping(pos, p) for pos in _BC]
#            detA_bc = array([a[0,0]*a[1,1] - a[0,1]*a[1,0] for a in A_bc])
#            
#            _test_vertex = [[vstack((_tfil[(0,1),:],_bc)), 
#                             vstack((_tfil[(0,2),:],_bc)),
#                             vstack((_tfil[(1,2),:],_bc))] for _tfil,_bc in zip(_triangles_filtered, _BC)]
#            _triangles = array(_test_vertex).reshape((3*len(_test_vertex),3,2))
#            
#
#            _test_detA = [array([[_fil[0],_fil[1],_bc],
#                                 [_fil[0],_fil[2],_bc],
#                                 [_fil[1],_fil[2],_bc]]) for _fil,_bc in zip(_detA_filtered, detA_bc)]
#            detA_struct = array(_test_detA).reshape((3*len(_test_vertex),3))
#            
#            _cl = array([self._cl_crosses_tile(_deta_) for _deta_ in _test_detA]).flatten()
            
            ###
            
            if len(_triangles_filtered) == 0: 
                print 'Warning: none of the tiles covers a critical line'
                print '(1) If the tile size is relatively small --> the critical line might be even smaller than a single tile'
                print '(2) If the tile size is large --> decrease the size of the original tile.'
                break
            
            _vertex = concatenate((_triangles_filtered.reshape((_triangles_filtered.shape[0]*3,2)), _BC))
            _vertex = vstack({tuple(row) for row in _vertex}) # like np.unique() but for row in matrix
            
            _d = Delaunay(_vertex)
            _triangles = _vertex[_d.simplices] 
            
            if full_output:
                triangles_total = concatenate((triangles_total, _triangles))        

            _cl = self._tile_covers_CL_new(_vertex, _d.simplices, p)
            if debug:
                print '{:.0f}   ({:.3f}s)'.format(len(_cl), time.time()-start)            

        BC_total = array([Model._barycenter(tr) for tr in _triangles[nonzero(_cl)]])                
        
        if full_output: 
            # TODO: one should avoid the multiprocessing here and use the alternative method _tile_covers_CL_new :
            # compute the mu for all the points and after only build the triangles.
            
            #cl_total = array([self._tile_covers_CL(tr, p) for tr in triangles_total])
            try:
                #if debug: print 'multiprocess total ...'
                if debug: 
                    start = time.time()
                    now = time.localtime()
                    now_str = '{}h{}m{}s'.format(now.tm_hour, now.tm_min, now.tm_sec)
                    print '{}: multiprocess total ...'.format(now_str)                 
                MP = Multiprocessing(self._tile_covers_CL, triangles_total, 
                                     func_extra_kwargs={'p':p})
                cl_total = MP.run(nprocs=processes, profile=False)
                cl_total = array(cl_total)  
                
                if debug: 
                    
                    print '... {} done (duration: {:.3f}sec)'.format(i, time.time()-start)
            except:
                _cl = array([self._tile_covers_CL(tr, p) for tr in _triangles])        
        
            return triangles_total, cl_total, BC_total 
        else:
            return BC_total
        
    def _separate_critical_lines(self, critical_line):
        """
        """
        RADIUS = (sum(critical_line**2, axis=1))**(0.5)
        ANGLE = mod(arctan2(critical_line[:,1], critical_line[:,0]), 2.*pi)
        
        RADIUS_SORTED = sort(RADIUS)
        _index_radius = gradient(RADIUS_SORTED).argmax()
        RADIUS_INTERFACE = RADIUS_SORTED[_index_radius]
                
        A1 = ANGLE[RADIUS<RADIUS_INTERFACE]
        ANGLE_CL_1 = sort(A1)
        RADIUS_CL_1 = (RADIUS[RADIUS<RADIUS_INTERFACE])[argsort(A1)]
        CL1 = empty([A1.shape[0]+1,2])
        CL1[:-1,0] = RADIUS_CL_1*cos(ANGLE_CL_1)
        CL1[-1,0] = CL1[0,0]
        CL1[:-1,1] = RADIUS_CL_1*sin(ANGLE_CL_1)
        CL1[-1,1] = CL1[0,1]                
        
        A2 = ANGLE[RADIUS>RADIUS_INTERFACE]
        ANGLE_CL_2 = sort(A2)
        RADIUS_CL_2 = (RADIUS[RADIUS>RADIUS_INTERFACE])[argsort(A2)]
        CL2 = empty([A2.shape[0]+1,2])
        CL2[:-1,0] = RADIUS_CL_2*cos(ANGLE_CL_2)
        CL2[-1,0] = CL2[0,0]
        CL2[:-1,1] = RADIUS_CL_2*sin(ANGLE_CL_2)
        CL2[-1,1] = CL2[0,1]        

        return CL1, CL2     
    
    def _check_critical_lines_extent(self, cl, radius, 
                                     center=[0.0,0.0]):
        """
        Check the size of the critical lines wrt the radius. If the radius is >>, raise a warning.  
        
        """
        
#       TODO: implement the case where the cl is small and not centered, i.e., 
#       centroid(cl) is very different to the center of the grid search.

        _, extent_max = curve_extent(cl, center)
    
        if 2.0*extent_max < radius:
            _text = ['Warning: the radius {:.1f} '.format(radius),
                    'of the search area centered on ',
                    '({:.2f},{:.2f}) '.format(center[0], center[1]),
                    'is {:.1f}x '.format(radius/extent_max), 
                    'larger than the critical lines extent. ',
                    '\nIf combined with a too small grid sampling, ',
                    'some critical line features might be undetected. ',
                    '\nIf the grid rightly encompasses an isolated ', 
                    'inner critical lines or the whole critical lines, '
                    'we suggest you decrease the ',
                    'radius down to {:.1f}. '.format(extent_max*1.75), 
                    'Otherwise, we suggest you increase the ',
                    'radius up to {:.1f}.'.format(radius*1.75)]  
            text = ''.join(_text)
            return True, text
        else:
            return False, ''
        
    def _check_gridcentering(self, cl, center=[0.0,0.0], factor=0.5):
        """
        Check that the center of the grid search is not too far from the 
        critical_lines centroid.
        
        factor = 0.5 --> we trigger the warning when the distance btw the 
        grid center and the cl centroid is larger than 0.5x the maximum
        cl extent.
        """
        centroid = centroid_polygon(cl)
        _, extent_max = curve_extent(cl, center=centroid)
        
        distance = sqrt(sum((centroid - array(center))**2))
        
        if distance > extent_max*factor:
            _text = ['Warning: the offset between the grid center and the \n', 
                     'critical line centroid is {:.1f}x '.format(distance/extent_max),
                     'larger than the critical \nline maximum extent. ',
                     'We suggest you recenter the search grid. \n',
                     'center: ({:.2f},{:.2f}) --> '.format(center[0], center[1]),
                     '({:.2f},{:.2f})'.format(centroid[0], centroid[1])]
            
            text = ''.join(_text) 
            return True, text
        else:
            return False, ''
     
    @timeit    
    def critical_curves(self, p=None, radius=2.0, density=51, center=[0.0,0.0], 
                        gridtype='square', tiling=None, guess=None, 
                        extra=None, extra_kwargs=None,
                        N_vertex_per_tile=5, N_vertex_per_edge=3,
                        n_iterations=1, angle_threshold=5.0,
                        refinement=True, options=None, multi=True,
                        nprocs=None, separate=True, full_output=False, 
                        debug=False):
        """
        Generate the critical curves.
        
        Parameters
        ----------
        p : array_like (default:None)
            If not None, `p` is the lens model parameters. It overrides the 
            attribute self.p0.
        radius : float
            Maximum extension of the grid.
        density : int
            Number of vertices per 2*radius. The larger, the more dense is 
            the grid.
        center : array_like
            Cartesian coordinate of the grid center.
        gridtype : str
            When `square`, the vertices are located on a square grid.
            When `random`, the vertices are randomly chosen.
            In both cases, the radial component r of the vertices satisfy
            r <= radius.
        tiling : 2-tuple (float,int)
            A shortcut to define simultaneously `radius` and `density`.
        guess : array_like
            Good guesses used to generate the critical curves.
        extra : list of array_like
            Center(s) of the extra subgrids added to the main grid.
        extra_kwargs : dict
            Options to characterized the radius and density of the subgrids
            defined with `extra`.
        N_vertex_per_tile : int
            Number of vertices per tile used at each iteration to define 
            the subtiling.
        N_vertex_per_edge : int
            Number of vertices per tile side used at each iteration to define 
            the subtiling.  
        n_iterations : int
            Number of iteration of the tiling algorithm.
        angle_threshold : float
            To avoids slivered triangles in the tiling, any of them which has
            the minimum inner angle smaller than angle_threshold are 
            discarded. 
        refinement : bool
            If True, perform a numerical optimization of the individual 
            critical curve positions.
        options : dict
            Options passed to scipy.optimize.minimize.
        multi : bool
            If True, perform parallel computing when possible.
        nprocs : int
            The Number of cpu cores you want to dedicate to this method.
        separate : bool (Default:True)
            If True, (try) to separate all the critical curves into a list
            of well-separated closed curves. The process is not yet perfectly
            stable, but is doing fine in most of the cases.
        full_output : bool
            If True, return an instance of the class `CriticalCurves` which 
            encompasses several subproduct used during the process and 
            provides methods to plot the tiling.
        
        Returns
        -------
        cc : Nx2 array_like, list or CriticalCurves instance
            The critical curves. If `separate` is false the result is a 
            Nx2 numpy array, otherwise the result is a list of the 
            well-separated critical curves. If `full_output` is True, 
            the result is an instance of the class `CriticalCurves`.
        
        """ 
#        FIXME: seperating the CLs is not yet perfectly stable! 
#            
#        TODO: on pourrait envisager d'
#        ajouter plusieurs attributs à l'instance de Model, comme 
#        self.critical_lines, self.caustics, self.cl_triangles de sorte que ces 
#        données soient accessibles directement. Il faudrait alors implémenter
#        un - restore to default value - dès lors que les paramètres self.p0
#        sont modifié, sans quoi on pourrait avoir des critical lines stockées
#        qui ne correspondent pas aux model parameters.
#        
#        TODO: on pourrait envisager que critical_lines puisse accepter une librairie
#        C qui implémente la méthode backwards_source et fasse l'alogorithme de
#        tiling dessus. Ainsi, le user pourrait utiliser critical_lines pour générer
#        les lignes critiques pour un modèle tout à fait indépendant. Cette 
#        update n'a de sens que si on a une classe dédiée à critical line, totalement
#        dissociée de la classe Model.
#        
#        TODO: like for `images`, when `guess` is not None, one should just run
#        an optimization from the guesses, using a L.-M. algorithm. This should 
#        override the use of the tiling algorithm.
#
#        index_starting_point : int
#            Index of the point at which the `separate_closed_curves` starts to
#            sort the points. The argument is passed to `sort_curve`.
        
        if p is None: p = self.p0
        assert p is not None, 'No model parameters have been provided'
        
        if tiling is not None:
            radius, density = tiling
        
        if multi and nprocs is None:
            nprocs = available_cpu()
            
        if guess is None and self.cc_guess is not None:
        #and not discard_internal_guess:
            guess = self.cc_guess
        
        if guess is not None:
            separate = False
            reconsider_radius = False
            reconsider_centering = False
            triangles = None
            cl_covered = None
            critical_line = guess
        else:
            if not density % 2: density += 1
            if n_iterations < 1: '`n_iterations` must be at least 1'

                
            # Grid
            if gridtype is 'square':
                points = array(Meshgrid.get_circular(radius, center=center, 
                                                     num=density))
            elif gridtype is 'random':
                points = array([get_random_point_in_circle(radius, center) for _ in range(density**2)])
    
            if extra is not None:
                extra_kwargs_ref = {'radius':0.3, 'num':floor(density/2)}
                if extra_kwargs is None: 
                    extra_kwargs = extra_kwargs_ref
                else:
                    extra_kwargs = HandlingDict(extra_kwargs).update_dict(extra_kwargs_ref)
    
                for pos in extra:
                    points = vstack((points, Meshgrid.get_circular(center=pos, **extra_kwargs)))            
                
            res_tiling = self.tiling_new(points, p, N_vertex_per_tile, 
                                         N_vertex_per_edge, n_iterations, 
                                         angle_threshold, multi, nprocs, 
                                         full_output, debug)
            
            if isinstance(res_tiling, tuple):
                critical_line = res_tiling[0]
                triangles = res_tiling[1]
                cl_covered = res_tiling[2]
            else:
                critical_line = res_tiling
    
            if len(critical_line) == 0:
                print 'No critical lines found. None is returned.'
                return None
            
            # Posterior check
            reconsider_centering, text_center = self._check_gridcentering(critical_line, center, factor=0.5)
            if reconsider_centering: print text_center
                
            reconsider_radius, text_radius = self._check_critical_lines_extent(critical_line, radius, center)
            if reconsider_radius and not reconsider_centering: print text_radius
        
        if (not refinement 
            or (refinement and reconsider_radius) 
            or (refinement and reconsider_centering)):
            #if separate:
            #    critical_line = self._separate_critical_lines(critical_line)
            
            if refinement and reconsider_centering:
                print ''.join(['Warning: No refinement has been performed ', 
                               'because of the not well centered grid.'])  
                
            if refinement and reconsider_radius and not reconsider_centering:
                print ''.join(['Warning: No refinement has been performed ', 
                               'because of the too large radius.'])
                
            if separate:
                critical_line = separate_closed_curves(critical_line)
              
            if full_output:
                return CriticalCurves(cc=critical_line,
                                      triangles=triangles,
                                      coveredtiles=cl_covered,
                                      refine={},
                                      p = self.p0)
            else:
                return critical_line
        else:
            options_ref = {'maxfev': 20, 'fatol': 1.0e-06, 
                           'nrefine':1.0} 
            if options is None:
                options = options_ref
            else:
                options = HandlingDict(options).update_dict(options_ref)
                
            if guess is not None and isinstance(critical_line,list):
                critical_line_optimized = [zeros([len(_cc),2]) for _cc 
                                           in critical_line]
            else:
                length = int(ceil(min((options.pop('nrefine', 1.0),1.0)) * len(critical_line)))
                sampling = choice(range(len(critical_line)), size=length, 
                                  replace=False)                
                
                critical_line_optimized = [zeros([length,2])]
                critical_line = [critical_line]
                
            success = [[] for _ in range(length)]
            fun = [[] for _ in range(length)]
            nfev = [[] for _ in range(length)]
            res_refine = []
            refine = []                
                
            for j,_cc in enumerate(critical_line):
                if debug: 
                    start = time.time()
                    now = time.localtime()
                    now_str = '{}h{}m{}s'.format(now.tm_hour, now.tm_min, now.tm_sec)
                    print 'Step {}/{}'.format(j+1,len(critical_line))
                    print '{}: Refinement of {} points ...'.format(now_str, len(_cc[sampling]))
                    
                res_refine.append(self._cl_refinement(_cc[sampling], p, nprocs, options, 
                                                      debug, full_output))
    
                if debug: print '... refinement done (duration: {:.3f}sec)'.format(time.time()-start)            
            
            if full_output:
                for i in range(len(critical_line_optimized)):
                    for k,res in enumerate(res_refine[i]):
                        critical_line_optimized[i][k,:] = res.x
                        success[i].append(res.success)
                        fun[i].append(res.fun)
                        nfev[i].append(res.nfev)
                    refine.append({'success':success, 'fun':fun, 'nfev':nfev})
                    
                    if separate:
                        critical_line_optimized = separate_closed_curves(critical_line_optimized)
                    
                return CriticalCurves(cc=critical_line_optimized,
                                      triangles=triangles,
                                      coveredtiles=cl_covered,
                                      refine=refine,
                                      p = self.p0)
            else:
                if separate:
                    return separate_closed_curves(res_refine)  
                else:
                    return res_refine
        
        return 42 # One should never reach this return.  
    
    
    def _cl_refinement(self, sequence, p=None, nprocesses=1, options=None, 
                       debug=False, full_output=False):
        """
        """
        if p is None: p = self.p0
        
        if options is None:
            options = {'maxfev': 10, 'fatol': 1.0e-06}        
            
        def M((t1,t2), p):
            w = self.jm_lens_mapping((t1,t2), p)
            return abs(w[0,0]*w[1,1] - w[0,1]*w[1,0])  
        
        def critical_points(bc, p, full_output=False):   
            sol = minimize(M, bc, args=(p,), method='Nelder-Mead', 
                           options=options)
            if full_output:
                return sol
            else:
                return sol.x  

        MP = Multiprocessing(critical_points, 
                             sequence, 
                             {'p':p, 'full_output':full_output})
        
        optimized = MP.run(nprocs=nprocesses, debug=debug)
        
        if full_output:
            return optimized
        else:
            return array(optimized)
    
    def critical_curve_properties(self, critics):
        """
        """
        main_centroid = centroid_polygon(vstack(tuple(critics)))
        main_extent = curve_extent(vstack(tuple(critics)), center=main_centroid)        
        
        cl_size = [len(cl) for cl in critics]
        cl_centroids = [centroid_polygon(cl) for cl in critics]
        cl_extents = [curve_extent(cl, center=cent) for cl,cent in zip(critics, cl_centroids)]        
        cl_median_sep = [median(separation(cl,cl_centroid)) for cl,cl_centroid in zip(critics, cl_centroids)]        
        
        res = {'size':cl_size, 'centroids':cl_centroids, 'extents':cl_extents,
               'median_separation':cl_median_sep, 'main_centroid':main_centroid,
               'main_extent':main_extent}
        return res

    def plot_tiling_critical_curves(self, cl=None, triangles=None, tiles=None, 
                                    extra=None, lim=None, save=False, **kwargs):
        """        
        kwargs:
            tile_colors
            Polygon_kwargs
            PatchCollection_kwargs
            figsize
            subplots_kwargs
            set_xlabel
            set_ylabel
            set_xlabel_fontsize
            set_ylabel_fontsize
            set_tick_params_labelsize
            
        """
#       TODO: if cl is not None but (triangles or tiles) are, plot cl only.
        
        if kwargs.pop('tile_colors', None) is None:
            tile_colors = ('w','k')
            
        Polygon_kwargs = kwargs.pop('Polygon_kwargs', None)
        if Polygon_kwargs is None:
            Polygon_kwargs = dict()

        if Polygon_kwargs.get('linewidth') is None:
            Polygon_kwargs['linewidth'] = 0.1 
        if Polygon_kwargs.get('edgecolor') is None:
            Polygon_kwargs['edgecolor'] = 'k'          
          
        colors = [Colors().get_random_colors(output='rgb') 
                    if k else tile_colors[0] for k in tiles]
        patches = [Polygon(array(tr), True, facecolor=color, **Polygon_kwargs) 
                    for tr,color in zip(triangles,colors)]                   
        p = PatchCollection(patches, match_original=True, 
                            **kwargs.pop('PatchCollection_kwargs', dict()))

        # Creat the figure
        fig, ax = subplots(figsize=kwargs.get('figsize',(8,8)), 
                           **kwargs.pop('subplots_kwargs', dict()))

        # Add the polygones        
        ax.add_collection(p)
        
        # true critical line
        if cl is not None:
            for _cl in cl:
                ax.plot(_cl[:,0], _cl[:,1], color='g')
                
        # extra
        if extra is not None:
            ax.plot(extra[:,0], extra[:,1], '.r')
        
        # axes
        xlabel(kwargs.get('set_xlabel',r'$\theta_1$'), 
               fontsize=kwargs.get('set_xlabel_fontsize',20))
        ylabel(kwargs.get('set_ylabel',r'$\theta_2$'), 
               fontsize=kwargs.get('set_ylabel_fontsize',20))
        
        if lim is None:
            xlim([triangles[:,:,0].min(),triangles[:,:,0].max()])
            ylim([triangles[:,:,1].min(),triangles[:,:,1].max()])
        else:
            xlim([lim[0],lim[1]])
            ylim([lim[2],lim[3]])        
        
        ax.tick_params(labelsize=kwargs.get('set_tick_params_labelsize',12))
        
        if save:
            savefig('critical_lines.pdf',dpi=900, bbox_inches='tight', 
                    pad_inches=0.1)
            show()
        else:
            show()
        return fig, ax       

    def caustics(self, critical_lines, p=None):
        """ Compute the caustics from the corresponding critical curves.
        
        Parameters
        ----------
        critical_lines : ndarray or list of ndarray
            One critical curve as a Nx2 ndarray or a list of separated
            critical curves as a list of Nx2 ndarray.
        p : array_like
            Model parameters. p overrides any p0 defined within the class.
        
        Returns
        -------
        cv : ndarray or list of ndarray
            Sampling of the caustic(s) in the source plane.

        """
#       TODO: implement a multiprocessing verions of this method.

        if p is None: p = self.p0
        
        if isinstance(critical_lines,tuple) or isinstance(critical_lines,list):
            cv = [array([[self.backwards_source(im, p) for im in cl]]) 
                  for cl in critical_lines]
            cv = [_cv.reshape((_cv.shape[1:])) for _cv in cv]
        else:
            cv = array([self.backwards_source(im, p) for im in critical_lines])
            
        return cv
            
    def _source_inside_caustic(self, beta, caustic):
        """
        """
        # TODO: Ne prend pas en compte une caustic qui possède des swallowtails
        #       internes. Dans ces cas là, il se peut qu'on cross la caustic 
        #       tout en restant à l'intérieur de cette dernière, avec formation
        #       d'images qui ne sont pas comptabilisées.
        polygon = mplPath.Path(caustic)
        
        if isinstance(beta,tuple):
            return polygon.contains_point(beta)
        else:
            return polygon.contains_points(beta)
    
    def N_lensed_images(self, beta, caustics, full_output=False):
        """
        """
#        TODO: It seems that `beta` must be a tuple and raise an error when it's
#        a list or a numpy array. One should investigate such a behavior.        
        Nimgs = 1
        
        beta_inside_caustic = zeros(len(caustics))        
        for k,cc in enumerate(caustics):
            beta_inside_caustic[k] = self._source_inside_caustic(beta, cc)
            if beta_inside_caustic[k]: Nimgs += 2
        
        if full_output:
            return Nimgs, beta_inside_caustic
        else:
            return Nimgs

#    def R_kappa(self, norm_theta12, p):
#        """
#        """
#        def wrapper(norm_theta12, p):
#            #return self.kappa_azimuthally_averaged(norm_theta12, p)
#            return self.kappa_average(norm_theta12, p=p)
#            
#        #kappa_avg = self.kappa_azimuthally_averaged(norm_theta12, p)
#        kappa_avg = self.kappa_average(norm_theta12, p=p)
#        D_kappa_avg = derivative(func=wrapper, x0=norm_theta12, args=([p]), 
#                                 dx=1e-06)
#        return (1 - kappa_avg)/D_kappa_avg 


class CriticalCurves(object):
    """
    TODO: we should add `plot_tiling_critical_lines` here.  
    
    TODO: implements a __getitem__
    """

    def __init__(self, cc, triangles=None, coveredtiles=None, refine=None, 
                 p=None, alpha=None):
        """
        """
        self.cc = cc
        self.triangles = triangles
        self.coveredtiles = coveredtiles
        self.refine = refine
        self.p = p
        self._alpha = alpha


        self.main_centroid = centroid_polygon(vstack(tuple(self.cc)))
        self.main_extent = curve_extent(vstack(tuple(self.cc)), 
                                        center=self.main_centroid)        
        
        self.sizes = [len(_cl) for _cl in self.cc]
        
        self.centroids = [centroid_polygon(_cl) for _cl in self.cc]
        
        self.extents = [curve_extent(_cl, center=cent) for _cl,cent 
                        in zip(self.cc, self.centroids)]        
        
        self.median_sep = [median(separation(_cl,cl_centroid)) 
                           for _cl,cl_centroid 
                           in zip(self.cc, self.centroids)]        
         
        self.properties = {'size':self.sizes, 
                           'centroids':self.centroids, 
                           'extents':self.extents,
                           'median_separation':self.median_sep, 
                           'main_centroid':self.main_centroid,
                           'main_extent':self.main_extent} 
        
    def plot_tiling(self, lines=False, extra=None, lim=None, save=False, 
                    **kwargs):
        """
        TODO: if cl is not None but (triangles or tiles) are, plot cl only.
        kwargs:
            tile_colors
            Polygon_kwargs
            PatchCollection_kwargs
            figsize
            subplots_kwargs
            set_xlabel
            set_ylabel
            set_xlabel_fontsize
            set_ylabel_fontsize
            set_tick_params_labelsize
        """
        
        if kwargs.pop('tile_colors', None) is None:
            tile_colors = ('w','k')
            
        Polygon_kwargs = kwargs.pop('Polygon_kwargs', None)
        if Polygon_kwargs is None:
            Polygon_kwargs = dict()

        if Polygon_kwargs.get('linewidth') is None:
            Polygon_kwargs['linewidth'] = 0.1 
        if Polygon_kwargs.get('edgecolor') is None:
            Polygon_kwargs['edgecolor'] = 'k'          
          
        colors = [Colors().get_random_colors(output='rgb') 
                    if k else tile_colors[0] for k in self.coveredtiles]
        patches = [Polygon(array(tr), True, facecolor=color, **Polygon_kwargs) 
                    for tr,color in zip(self.triangles,colors)]                   
        p = PatchCollection(patches, match_original=True, 
                            **kwargs.pop('PatchCollection_kwargs', dict()))

        # Creat the figure
        fig, ax = subplots(figsize=kwargs.get('figsize',(6,6)), 
                           **kwargs.pop('subplots_kwargs', dict()))

        # Add the polygones        
        ax.add_collection(p)
        
        # true critical line
        if lines and self.cc is not None:
            for _cl in self.cc:
                ax.plot(_cl[:,0], _cl[:,1], color='g')
                
        # extra
        if extra is not None:
            ax.plot(extra[:,0], extra[:,1], '.r')
        
        # axes
        xlabel(kwargs.get('set_xlabel',r'$\theta_1$'), 
               fontsize=kwargs.get('set_xlabel_fontsize',20))
        ylabel(kwargs.get('set_ylabel',r'$\theta_2$'), 
               fontsize=kwargs.get('set_ylabel_fontsize',20))
        
        if lim is None:
            xlim([self.triangles[:,:,0].min(),self.triangles[:,:,0].max()])
            ylim([self.triangles[:,:,1].min(),self.triangles[:,:,1].max()])
        else:
            xlim([lim[0],lim[1]])
            ylim([lim[2],lim[3]])        
        
        ax.tick_params(labelsize=kwargs.get('set_tick_params_labelsize',12))
        
        if save:
            savefig('critical_lines.pdf',dpi=900, bbox_inches='tight', 
                    pad_inches=0.1)
            show()
        else:
            show()
        return fig, ax       
     
    
    