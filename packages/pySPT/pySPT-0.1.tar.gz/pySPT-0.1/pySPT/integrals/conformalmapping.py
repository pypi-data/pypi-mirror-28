#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:12:04 2016

@author: Sciences
"""
from numpy import real, imag, absolute, angle, exp, cos, sin, arctan2, mod, pi
from numpy import ndarray, array, ones, ones_like, empty, arange, meshgrid 
from numpy import linspace

from ..tools.colors import Colors

__author__ = 'O. Wertz @ Bonn'
__all__ = ['ConformalMapping']

class ConformalMapping (object):
    """
    A function of given original coordinates is manipulated wrt conformal 
    mapping coordinates which are defined in Eq.(A.1) in Unruh et al. (2016):
    
    x = (original - ctheta) / [R - (cthetaC * original / R)]           [1]
    
    where:
    (1) original, the complex version of the 2d-original coordinates,
    (2) x, chteta and cthetaC are complex quantities, 
    (3) cthetaC is the complex conjugate of ctheta
    (4) R is a real number.
    
    All the methods accept either (|x|, delta) or (x1, x2) where:
    + |x| and delta are resp. the norm  and the phase of the complex x
      such as x = |x| exp(1j * delta)
    + x1 and x2 are resp. the real and imaginary parts of x,    
    and return the results as evaluated with the original coordinate. 
    """
    def __init__(self, ctheta1, ctheta2, R):#, func, *args, **kwargs):
        """
        """
        self._ct1 = ctheta1
        self._ct2 = ctheta2
        self._R = R

    @property
    def R(self):
        return self._R
        
    @R.setter
    def R(self, value):
        self._R = value

    @property
    def ctheta1(self):
        return self._ct1
        
    @ctheta1.setter
    def ctheta1(self, value):
        self._ct1 = value    

    @property
    def ctheta2(self):
        return self._ct2
        
    @ctheta2.setter
    def ctheta2(self, value):
        self._ct2 = value        
        
    @property
    def ctheta12(self):
        return self._ct1, self._ct2                
        
    @ctheta12.setter
    def ctheta12(self, value): 
        self._ct1 = value[0]
        self._ct2 = value[1]        
        
    def _original_to_cm(self, theta1, theta2, coord='cartesian'):
        """
        """
        t = theta1 + 1j*theta2
        ct = self._ct1 + 1j*self._ct2
        ctc = self._ct1 - 1j*self._ct2
        x = (t - ct)/(self._R - ctc*t/self._R)
        if coord == 'cartesian':
            return real(x), imag(x)
        elif coord == 'polar':
            return absolute(x), angle(x)
        
    def _cm_cartesian_to_original_cartesian(self, x1, x2):
        """
        """
        x_complex = (x1 + 1j*x2)
        T1 = self._R*x_complex + (self._ct1 + 1j*self._ct2)
        T2 = 1 +  (self._ct1 - 1j*self._ct2)*x_complex/self._R
        theta = T1/T2
        return real(theta), imag(theta)
        
    def _cm_polar_to_cm_complex(self, x, delta):
        """
        """        
        return x * exp(1j * delta)
        
    def _cm_polar_to_original_complex(self, x, delta):
        """
        """
        x_complex = self._cm_polar_to_cm_complex(x, delta)
        ct_complex = self._ct1 + 1j*self._ct2
        ct_complex_conj = self._ct1 - 1j*self._ct2
        return (self._R*x_complex + ct_complex) / (1. + (ct_complex_conj*x_complex /self._R))
        
    def _cm_polar_to_original_polar(self, x, delta):
        """
        """
        #res = empty(2)
        theta_complex = self._cm_polar_to_original_complex(x, delta)
        theta = absolute(theta_complex)
        varphi = mod(angle(theta_complex), 2.*pi)
        return theta, varphi
        #return array([c0, c1])
        
    def _cm_polar_to_original_cartesian(self, x, delta):
        """
        """
        #res = empty(2)
        theta_complex = self._cm_polar_to_original_complex(x, delta)
        theta_1 = real(theta_complex)
        theta_2 = imag(theta_complex)
        return theta_1, theta_2
        #return array([c0, c1])   
        
    def _cm_cartesian_to_cm_polar(self, x1, x2):
        """
        """
        x = (x1**2 + x2**2)**(0.5)
        delta = mod(arctan2(x2,x1),2.*pi)
        return x, delta
                  
    def _cm_func(self, x, delta, func, *args, **kwargs):
        """
        """  
        input_format = kwargs.pop('input_format', 'polar')
        if input_format is 'polar':
            coord = self._cm_polar_to_original_polar(x, delta)
            return func(coord[0], coord[1], *args, **kwargs)            
        elif input_format is 'cartesian':
            coord = self._cm_polar_to_original_cartesian(x, delta)
            return func(coord[0], coord[1], *args, **kwargs)               
        else:
            print '{} is not recognized as a valid input_format'.format(self._input_format)
            return None         

    def _jacobian(self, x, delta):
        """
        """
        ctsq = self._ct1**2 + self._ct2**2
        dotprod = x*cos(delta)*self._ct1 + x*sin(delta)*self._ct2
        
        num = self._R**2 * (self._R**2 - ctsq)**2        
        denom = (self._R**2 + 2.*self._R*dotprod + ctsq*x**2)**2
        return num/denom 

    def cm_illustration(self, image=None, border=None, image_path=None, 
                        oversampling=1.0, add_points=[], 
                        add_curves=[], options_curves=None,
                        display=True, grid=False, grid_options=None,
                        highlight_peak=True,
                        highlight_center=True,
                        save=False, output_filename=''):
        """
        Comments
        --------
        A higher value of 'oversampling' will increase the resolution of the
        CM-modified image. However, since the resolution of the CM-modified 
        image depends on the resolution of the original image, a too high 
        value of 'oversampling' will not improve anymore the CM-modified image.
        In other word, for a middle-resolution original image, 'oversampling'
        set to 1.0 (default) will result in a poor quality CM-modified image.
        Increasing 'oversampling' to 4.0 will significantly improve the quality
        of the CM-modified image. Increasing 'oversampling' to 10.0 will not 
        affect the CM-modified image quality better than with 
        'oversampling' = 4.0 since, now, it is limited by the resolution of 
        the original image. For example:
        
        >> cm = cm = ConformalMapping(0.65, -0.1, 1.0)
        
        and compare it with the different results obtained with 'oversampling' 
        successively equal to [0.1, 0.5, 2.0, 4.0, 8.0]
        
        >> cm.cm_illustration(oversampling=0.1)
        >> cm.cm_illustration(oversampling=0.5)
        ...
        >> cm.cm_illustration(oversampling=8.0)
        
        While the poor quality of the image 'oversampling' = 0.1 is logically 
        limited by the adopted sampling, the much better quality of the image 
        'oversampling' = 8.0 is now limited by the resolution of the original 
        image. The image quality between 'oversampling' = 4.0 and 
        'oversampling' = 8.0 is almost identical, while the latter use a larger 
        amount of information from the original image, as shown by comparing 
        the third pictures. 
        """   
                     
        if image is not None:
            assert isinstance(image, ndarray), 'if passed, image must be a NxNx3 numpy array.'
            _shape = image.shape
            assert (len(_shape) == 3), 'image must be a NxNx3 numpy array: len(shape(image)) = {}'.format(len(_shape))            
            assert (_shape[0] == _shape[1]), 'image must be a NxNx3 numpy array: image.shape = {}'.format(_shape)            
            assert (_shape[2] == 3), 'image must be a NxNx3 numpy array: image.shape[2] = {}'.format(_shape[2]) 
        else:
            if image_path is None:
                from os.path import join, dirname, realpath
                image_path = join(dirname(realpath(__file__)),"fig/annulus.png")  
                
            try:
                from cv2 import imread
                print image_path
                image = imread(image_path, 1)
                image = image[:,:,[2,1,0]]
            except ImportError:
                raise ImportError('OpenCV is not installed: http://opencv.org/downloads.html')
            finally:
                pass

            _shape = image.shape
            assert (_shape[0] == _shape[1]), 'image must be squared: {}x{} passed'.format(_shape[0],_shape[1])             

        if border is None:
            border = 1.0
            
        theta = (1/border) * (self._ct1**2 + self._ct2**2)**(0.5)
        phi = arctan2(self._ct2, self._ct1)
        theta1, theta2 = array([theta/(self._R/border)*cos(phi+0.5*pi), 
                                theta/(self._R/border)*sin(phi+0.5*pi)]) # Add pi/2 to phi because numpy.array x and y axis are rotated by pi/2 in comparison with what is displayed with plt.imshow().
        theta_scaled = (theta1**2 + theta2**2)**(0.5)
        ct12_temp = self.ctheta12
        self.ctheta12 = (theta1, theta2)            

   
        _center = array([(_shape[0]-1)/2., (_shape[1]-1)/2.])       
        
        # IF RR != 1.0, one have to rescale the original image
        # It works well if RR > 1.0 since the new one is larger than the orginal and no information can be obtained from the new region.
        # However, when RR < 1.0, we crop the original to create the new one.
        # TODO: when RR<1.0, one should be able to extract the information outside the cropped region.
        if self._R/border != 1.0:
            image_rescaled = ones([int(_shape[0]*(self._R/border)), int(_shape[1]*(self._R/border)), 3], dtype=float) * 255.
        
            _shape_ = image_rescaled.shape
            _center_ = array([(_shape_[0]-1)/2., (_shape_[1]-1)/2.])
            Xs, Ys = meshgrid(arange(0,int(_shape_[0]),1), arange(0,int(_shape_[1]),1))
            
            if _center_[0] > _center[0]:
                offset = (_center_ - _center)[0]
                K = image_rescaled[int(offset):-int(offset), 0, 0].shape[0] -  _shape[0] 
                image_rescaled[int(offset):-int(offset)-K,int(offset):-int(offset)-K, :] = image
            else:
                offset = (_center - _center_)[0]
                image_rescaled = image[int(offset):-int(offset),int(offset):-int(offset),:]
            
            image = image_rescaled
            _shape = _shape_
            R_temp = self._R
            self._R = 1.0
        else:
            R_temp = border
            self._R = 1.0                              

        shape = array([int(_shape[0]*oversampling), int(_shape[1]*oversampling)])
        center = [(shape[0]-1)/2., (shape[1]-1)/2.]
        radius = min(shape/2.)   
        
        # Sampling
        X = linspace(0., shape[0]-1, shape[0])
        Y = linspace(0., shape[1]-1, shape[1])
        
        x = (X - radius)/radius
        y = (Y - radius)/radius
        
        x_mesh, y_mesh = meshgrid(x,y)   
        
        # For each scanned pixel in the cm-plane, find the corresponding 
        # pixel's indices in the original-plane. This is done in one operation
        # for all pixels thanks to matrix operation.
        T_real, T_imag = self._cm_cartesian_to_original_cartesian(x_mesh, y_mesh)        
        self.ctheta12 = ct12_temp
        self._R = R_temp
                
        index_all_0_alte_float = abs(T_real.flatten()[:] * radius + radius)
        index_all_1_alte_float = abs(T_imag.flatten()[:] * radius + radius)                
        index_all_0_alte = (index_all_0_alte_float/oversampling).astype(int)        
        index_all_1_alte = (index_all_1_alte_float/oversampling).astype(int)
        index_all_0_alte[index_all_0_alte >= _shape[0]] = 0
        index_all_1_alte[index_all_1_alte >= _shape[0]] = 0        

        # The cm-transformed image        
        RES = empty([shape[0], shape[1], 3], dtype=float)
        RES[:,:,0] = image[:,:,0][index_all_0_alte, index_all_1_alte].reshape(shape)/255.
        RES[:,:,1] = image[:,:,1][index_all_0_alte, index_all_1_alte].reshape(shape)/255.
        RES[:,:,2] = image[:,:,2][index_all_0_alte, index_all_1_alte].reshape(shape)/255.
        
        filter_ouside_unity_circle = (x_mesh**2 + y_mesh**2)**2 > 1.0
        
        RES[:,:,0][filter_ouside_unity_circle] = 1.
        RES[:,:,1][filter_ouside_unity_circle] = 1.
        RES[:,:,2][filter_ouside_unity_circle] = 1.        
   
        from scipy.ndimage.interpolation import rotate
        RES = rotate(RES, -90.)
        # Display ?             
        if not display:
            #self._R = R_temp
            #self.ctheta12 = ct12_temp
            return RES
        else:
            import matplotlib.pylab as plt
            sam_ank = linspace(0.,2.*pi, 1000)
            
            if grid and grid_options is None:
                grid_options = {'color':'g', 'alpha':0.5}
            
            #### Original ####
            plt.figure(figsize=(6,6))
            plt.hold(True)
            plt.imshow(image/255., origin='upper', interpolation='none')
            
            if highlight_peak:
                plt.plot((theta_scaled*cos(phi))*radius/oversampling+radius/oversampling, 
                         -(theta_scaled*sin(phi))*radius/oversampling+radius/oversampling, 'or')   # Add a minus sign at 2nd component because of plt.gca().invert_yaxis() which is used to obtain the image in the same orientiation as the original one.      
            if highlight_center:
                plt.plot(center[0]/oversampling,center[1]/oversampling, 'xm')            
            
            plt.xlim([-0.5,shape[0]/oversampling])
            plt.ylim([-0.5,shape[1]/oversampling])
            plt.plot(((_shape[0]-1)/2.) + 0.0 + (radius)/oversampling*cos(sam_ank), 
                     ((_shape[0]-1)/2.) + 0.0 + (radius)/oversampling*sin(sam_ank), 
                     '-', color=Colors().strawberry,
                     linewidth=2.0)         
            
            if add_points:
                if not isinstance(add_points[0], list):
                    add_points = [add_points]
                for ap in add_points:
                    plt.plot(ap[0]/self._R*radius/oversampling+radius/oversampling, 
                             -ap[1]/self._R*radius/oversampling+radius/oversampling, 'og')
                    
            if grid:                    
                _grid_comp_sampling = 500
                
                _radius = [0.2,0.4,0.6,0.8] 
                _delta  = linspace(0.,2.*pi, 12, endpoint=False)
                
                _err    = linspace(0.2,_radius[-1]*10.0, _grid_comp_sampling)
                _angles = linspace(0.,2.*pi, _grid_comp_sampling, endpoint=True)
                
                CM_CIRCLES = []
                CM_LINES = []  
                
                for r in _radius:
                    _circle = [r*cos(_angles), r*sin(_angles)]
                    plt.plot(-_circle[0]*radius/oversampling+radius/oversampling,
                             -_circle[1]*radius/oversampling+radius/oversampling, 
                             **grid_options)
                    CM_CIRCLES.append(array([self._original_to_cm(*coord) for coord 
                                             in zip(*_circle)])) 
    
                for d in _delta:
                    _line = [_err*cos(d), _err*sin(d)]
                    plt.plot(-_line[0]*radius/oversampling+radius/oversampling,
                             -_line[1]*radius/oversampling+radius/oversampling, 
                             **grid_options)
                    CM_LINES.append(array([self._original_to_cm(*coord) for coord 
                                           in zip(*_line)]))                     

            _cof_ = 1.0
            plt.xlim([-_cof_*radius/oversampling+radius/oversampling, 
                      _cof_*radius/oversampling+radius/oversampling])
            plt.ylim([-_cof_*radius/oversampling+radius/oversampling, 
                      _cof_*radius/oversampling+radius/oversampling])
                    
            plt.xticks([],[])
            plt.yticks([],[])
            plt.gca().invert_yaxis()
            if save:
                plt.savefig('CM_original_'+output_filename+'.pdf', dpi=900,
                            bbox_inches='tight', pad_inches=0.1)
            plt.show()   
            
            #### CM-modified ####
            plt.figure(figsize=(6,6))
            plt.hold(True)
            plt.imshow(RES, origin='upper', interpolation='none')  
            
            if highlight_peak:
                plt.plot(center[0], center[1],'or')
                
            
            plt.plot(center[0] + 0*0.25 + (radius)*cos(sam_ank), 
                     center[1] + 0*0.25 + (radius)*sin(sam_ank), 
                     '-', color=Colors().electricblue,
                     linewidth=2.0)
                
            _cof_ = 1.1
            plt.xlim([-_cof_*radius+center[0], _cof_*radius+center[0]])
            plt.ylim([-_cof_*radius+center[1], _cof_*radius+center[0]])
            temp = self._original_to_cm(0.,0.)

            if highlight_center:
                plt.plot(-temp[0]*radius+center[0], 
                         -temp[1]*radius+center[1], 'xm')
          
            if add_points:
                for ap in add_points:
                    temp_add_points = self._original_to_cm(ap[0],ap[1])
                    plt.plot(-temp_add_points[0]*radius+center[0], 
                             -temp_add_points[1]*radius+center[1], 'og')
                    
            if add_curves:
                if options_curves is None:
                    options_curves = {}
                    
                for cu in add_curves:
                    plt.plot(cu[:,0]*radius+center[0], 
                             cu[:,1]*radius+center[1], 
                             **options_curves)
                    
            if grid:
                for cmc in CM_CIRCLES:
                    plt.plot(-cmc[:,0]*radius+center[0], 
                             -cmc[:,1]*radius+center[0],
                             **grid_options)
                    
                for cml in CM_LINES:
                    plt.plot(-cml[:,0]*radius+center[0], 
                             -cml[:,1]*radius+center[0],
                             **grid_options)                    

            plt.xticks([],[])
            plt.yticks([],[])
            plt.gca().invert_yaxis()
            plt.gca().invert_xaxis()
            if save:
                plt.savefig('CM_cm_'+output_filename+'.pdf', dpi=900,
                            bbox_inches='tight', pad_inches=0.1)
            plt.show()  
            
            # Show which part of the original image is used to construct the 
            # CM-modified one. The sampling is regular in the CM-plane (namely
            # we are scanning all the pixel of the CM-plane) which implies that 
            # it is no more regular in the original plane. 
            image_scanned = ones_like(image)*255. #*0.
            image_scanned[index_all_0_alte, index_all_1_alte, :] = image[index_all_0_alte, index_all_1_alte, :]
            
            plt.figure(figsize=(6,6))
            plt.imshow(image_scanned/255., origin='upper', interpolation='none') 
            plt.xlim([-0.5,shape[0]/oversampling])
            plt.ylim([-0.5,shape[1]/oversampling]) 
            plt.xticks([],[])
            plt.yticks([],[])  
            plt.gca().invert_yaxis()
            if save:
                plt.savefig('CM_scan_'+output_filename+'.pdf', dpi=900,
                            bbox_inches='tight', pad_inches=0.1)
            plt.show()           
