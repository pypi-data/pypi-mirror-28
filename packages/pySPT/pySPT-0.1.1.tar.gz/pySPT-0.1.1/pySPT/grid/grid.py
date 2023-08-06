#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:26:56 2016

@author: Sciences

# TODO: at the end, this single class will be split in several classes, 
# leading to a more general implementation of this subpackage. One should even
# consider to convert the class+method into individual functions.

# TODO: one should define new method doing a specific job like inside_regions
#       and which is used in different other methods (random, elliptic, ...)
"""

from numpy import linspace, meshgrid, array, delete, ones_like, zeros_like
from numpy import ceil, inf, pi, cos, sin, arctan2, deg2rad, logical_and
from numpy import logical_or, all, where, ceil, ones
from numpy.random import uniform, choice
import matplotlib.path as mplPath

from ..tools.container import isiterable

__author__ = 'O. Wertz @ Bonn'
__all__ = ['Meshgrid']

class Meshgrid(object):
    """
    """
    def __init__(self):
        """
        """
        pass
    
    @staticmethod
    def filter_inside_region(positions_x, positions_y, regions):
        """
        """
        if len(regions) == 2 and not isinstance(regions[0],tuple):
            polygon = mplPath.Path(regions[1])
            is_inside_region = array([polygon.contains_point((_1,_2)) 
                                     for _1,_2 in zip(positions_x,positions_y)])            
        else:
            is_inside_region = zeros_like(positions_x)
            for region in regions:
                polygon = mplPath.Path(region[1])
                _conditions = array([polygon.contains_point((_1,_2)) 
                                    for _1,_2 in zip(positions_x,positions_y)])
                is_inside_region = logical_or(is_inside_region, _conditions)            

        return is_inside_region
    
    @classmethod
    def sampling(clc, x_bounds, y_bounds=None, category='random', N=50):
        """
        """
        if category is 'random':
            sampling_x = uniform(low=x_bounds[0], high=x_bounds[1], size=N**2)
            x = sampling_x.reshape(N,N)
            if y_bounds is None:
                return (x,x)
            else:
                sampling_y = uniform(low=y_bounds[0], high=y_bounds[1], size=N**2)                        
                return (x, sampling_y.reshape(N,N))
        elif category is 'linear':
            sampling_x = linspace(start=x_bounds[0], stop=x_bounds[1], num=N)
            if y_bounds is None:
                return meshgrid(sampling_x, sampling_x)
            else:
                sampling_y = linspace(start=y_bounds[0], stop=y_bounds[1], num=N)            
                return meshgrid(sampling_x, sampling_y)
        else:
            return 0.0

    @classmethod
    def get_random(clc, side_length=None, num=50, quadrant=None, R_filter=None,
                   discard_regions=False, inside_regions=False, nmax=None,
                   regions_opts=None, full_output=False):
        """
        
        Parameters
        ----------
        nmax : int
            Number max of sample.
        
        
        TODO: the discard_regions filtering process into a separated method        
        TODO: the discard_regions filtering is time consuming --> multiprocessing
        TODO: the inside_regions check is hard coded for the 1st regions given
                and should be generalized.
        """
        if side_length is None and R_filter is None:
            side_length = 1.0
        elif side_length is None and R_filter is not None:
            side_length = 2. * R_filter
        else:
            pass
            
        if nmax is not None:
            assert isinstance(nmax,int), '`nmax` must be an integer ({} passed)'.format(type(nmax))
            num = nmax
            if R_filter is not None:
                side_length = 2. * R_filter

        if quadrant is None:
            x,y = clc.sampling(x_bounds=(-side_length, side_length),
                               y_bounds=(-side_length, side_length),
                               category='random', N=num)
        elif quadrant == 1:
            x,y = clc.sampling(x_bounds=(0.0, side_length), 
                               y_bounds=(0.0, side_length),
                               category='random', N=num)
        else:
            pass
        
        x_flat = x.flatten(); y_flat = y.flatten()        
        radial = (x_flat**2 + y_flat**2)**(0.5)
        

        if R_filter and not discard_regions:
            if isiterable(R_filter):
                inside = logical_and(radial <= R_filter[0], radial >= R_filter[1])
            else:                        
                inside = radial <= R_filter
        elif R_filter and discard_regions:
            if len(regions_opts) == 2 and not isinstance(regions_opts[0],tuple):
                # One region
                D = array([((((regions_opts[1]-array(p))**2).sum(axis=1))**(0.5)).min() for p in zip(x_flat,y_flat)])
                _conditions = [D > ones_like(D)*regions_opts[0]]
            else:
                # Multiple regions
                Ds = [array([((((region[1]-array(p))**2).sum(axis=1))**(0.5)).min() for p in zip(x_flat,y_flat)]) for region in regions_opts]
                _conditions = [D > ones_like(D)*region[0] for D,region in zip(Ds,regions_opts)]
            
            if isiterable(R_filter):
                _conditions += [radial <= R_filter[0]]
                _conditions += [radial >= R_filter[1]]                
            else:
                _conditions += [radial <= R_filter] 
                
            inside = logical_and.reduce(_conditions, axis=0)
        else:
            inside = radial > -1 # always true --> construct the matrix `inside` where each element is True
        
        if inside_regions:
#            if len(regions_opts) == 2 and not isinstance(regions_opts[0],tuple):
#                polygon = mplPath.Path(regions_opts[1])
#                is_inside_region = array([polygon.contains_point((_1,_2)) for _1,_2 in zip(x_flat,y_flat)])
#                if all(is_inside_region):
#                    pass
#                else:
#                    inside = logical_and(inside,is_inside_region)
#            else:
#                is_inside_region = zeros_like(inside)
#                for region in regions_opts:
#                    polygon = mplPath.Path(region[1])
#                    _conditions = array([polygon.contains_point((_1,_2)) for _1,_2 in zip(x_flat,y_flat)])
#                    is_inside_region = logical_or(is_inside_region, _conditions)
#                if not all(is_inside_region): 
#                    inside = logical_and(inside, is_inside_region)
            is_inside_region = Meshgrid.filter_inside_region(x_flat, y_flat, regions_opts)
            if not all(is_inside_region): 
                inside = logical_and(inside, is_inside_region)
                
        if nmax is not None and inside.sum() >= nmax:
            index = choice(where(inside)[0], nmax, replace=False)
            inside = zeros_like(inside, dtype=bool)
            inside[index] = True
        
        if full_output:
            return array(zip(x.flatten()[inside], y.flatten()[inside])), (x,y), inside, int(num)
        else:
            return array(zip(x.flatten()[inside], y.flatten()[inside]))
    
    @classmethod
    def get_n_random_(clc, side_length, num=50, quadrant=None, R_filter=None,
                      discard_regions=False, inside_regions=False, nmax=None,
                      regions_opts=None):
        """
        
        Parameters
        ----------
        nmax : int
            Number max of sample.
        
        
        TODO: the discard_regions filtering process into a separated method        
        TODO: the discard_regions filtering is time consuming --> multiprocessing
        TODO: the inside_regions check is hard coded for the 1st regions given
                and should be generalized.
        """    
    
    @classmethod
    def get_square(clc, side_length, num=50, quadrant=False, R_filter=None, 
                   discard_origin=False, center=None, full_output=False):
        """
        """
        if center is not None and not quadrant:
            sampling_x = linspace(-side_length/2. + center[0], 
                                  side_length/2. + center[0], num)
            sampling_y = linspace(-side_length/2. + center[1], 
                                  side_length/2. + center[1], num)            
        elif not quadrant:
            sampling_x = linspace(-side_length/2., side_length/2., num)
            sampling_y = sampling_x
        else:
            sampling_x = linspace(0., side_length, num)
            sampling_y = sampling_x
            
        x, y = meshgrid(sampling_x, sampling_y)
        x_flat = x.flatten(); y_flat = y.flatten()        
        radial = (x_flat**2 + y_flat**2)**(0.5)
        
        if R_filter:                        
            inside = radial <= R_filter
        else:
            inside = radial > -1 # always true --> construct the matrix `inside` where each element is True
            
        grid = zip(x.flatten()[inside], y.flatten()[inside])  
        
        if discard_origin:
            grid = [_x for _x in grid if _x != (0.0,0.0)]      
            
        if full_output:
            return array(grid), (x,y), inside, int(num)
        else:
            #if R_filter is None:
            #    return zip(x.flatten(), y.flatten())
            #else:
            return array(grid)#zip(x_flat[inside], y_flat[inside])

    @classmethod
    def get_elliptic(clc, a, b=None, center=(0.0,0.0), num=50, quadrant=None, 
                     discard_regions=False, regions_opts=None, R_filter=None,
                     full_output=False, inside_regions=False):
        """
        TODO: the discard_regions filtering process into a separated method        
        TODO: the discard_regions filtering is time consuming --> multiprocessing
        TODO: the inside_regions check is hard coded for the 1st regions given
                and should be generalized.
        TODO: implement the R_filter condition.
                
        By default, we consider the circular case: b==None => b is set to a
        """  
        if b is None: b = a
        
        center = array(center)
        center_x = array([center[0],]*2)
        center_y = array([center[1],]*2)      
        
        if quadrant is None:
            x_bounds = array([-a,a])+center_x; y_bounds = array([-b,b])+center_y;
        elif quadrant == 1:
            x_bounds = array([0,a])+center_x; y_bounds = array([0,b])+center_y; #(0,a); y_bounds = (0,b);
        elif quadrant == 2:
            x_bounds = array([-a,0])+center_x; y_bounds = array([0,b])+center_y; #(-a,0); y_bounds = (0,b); 
        elif quadrant == 3:
            x_bounds = array([-a,0])+center_x; y_bounds = array([-b,0])+center_y; #(-a,0); y_bounds = (-b,0);
        elif quadrant == 4:
            x_bounds = array([0,a])+center_x; y_bounds = array([-b,0])+center_y; #(0,a); y_bounds = (-b,0);   
        else:
            print '`quadrant` argument not recognized: set to default `None`.'
            x_bounds = array([-a,a])+center_x; y_bounds = array([-b,b])+center_y;
                     
        sampling_x = linspace(x_bounds[0], x_bounds[1], num)
        sampling_y = linspace(y_bounds[0], y_bounds[1], num)
              
        #if a == b and quadrant is None:  # full pure circular case 
        #    x, y = meshgrid(sampling_x, sampling_x)            
        #else:       # elliptic case or circular w/ quadrant
            #sampling_y = linspace(y_bounds[0], y_bounds[1], num)
        x, y = meshgrid(sampling_x, sampling_y)
            
        x_flat = x.flatten(); y_flat = y.flatten()
        radial = ((x_flat-center[0])**2 + (y_flat-center[1])**2)**(0.5)
        
        if a == b:  # pure circular case
            radius_ell = a
        else:       # elliptic case
            angle = arctan2(y_flat, x_flat)
            radius_ell = a*b / ((a*sin(angle))**2 + (b*cos(angle))**2)**(0.5)
        
        if discard_regions:
            if len(regions_opts) == 2 and not isinstance(regions_opts[0],tuple):
                # One region
                D = array([((((regions_opts[1]-array(p))**2).sum(axis=1))**(0.5)).min() for p in zip(x_flat,y_flat)])
                _conditions = [D > ones_like(D)*regions_opts[0]]
            else:
                # Multiple regions
                Ds = [array([((((region[1]-array(p))**2).sum(axis=1))**(0.5)).min() for p in zip(x_flat,y_flat)]) for region in regions_opts]
                _conditions = [D > ones_like(D)*region[0] for D,region in zip(Ds,regions_opts)]
            
            inside = array(radial <= radius_ell, dtype=bool) & logical_and.reduce(_conditions, axis=0)
        else:
            inside = radial <= radius_ell
            
        #import matplotlib.pylab as plt        
        #plt.figure()
        #plt.plot(x_flat[:],y_flat[:], '.k')
        #plt.show()            
            
        if inside_regions:
#            if len(regions_opts) == 2 and not isinstance(regions_opts[0],tuple):
#                polygon = mplPath.Path(regions_opts[1])
#                is_inside_region = array([polygon.contains_point((_1,_2)) for _1,_2 in zip(x_flat,y_flat)])
#                if all(is_inside_region):
#                    pass
#                else:
#                    inside = logical_and(inside,is_inside_region)
#            else:
#                is_inside_region = zeros_like(inside)
#                for region in regions_opts:
#                    polygon = mplPath.Path(region[1])
#                    _conditions = array([polygon.contains_point((_1,_2)) for _1,_2 in zip(x_flat,y_flat)])
#                    is_inside_region = logical_or(is_inside_region, _conditions)
            is_inside_region = Meshgrid.filter_inside_region(x_flat, y_flat, regions_opts)
            if not all(is_inside_region): 
                inside = logical_and(inside, is_inside_region)           

        x_flat_filtered = x_flat[inside]
        y_flat_filtered = y_flat[inside]        
                
        if full_output:           
            return zip(x_flat_filtered, y_flat_filtered), (x, y), inside, int(num)
        else:                
            return zip(x_flat_filtered, y_flat_filtered) 
        
    @classmethod
    def get_circular(clc, radius, center=(0.0,0.0), num=50, quadrant=None, full_output=False):
        """
        """
        return Meshgrid.get_elliptic(a=radius, b=None, center=center, 
                                     num=num, quadrant=quadrant, 
                                     full_output=full_output)
#        sampling = linspace(-radius, radius, num)
#        
#        x, y = meshgrid(sampling, sampling)
#        x_flat = x.flatten(); y_flat = y.flatten()
#        radial = (x_flat**2 + y_flat**2)**(0.5)
#        
#        inside = radial <= radius
#
#        x_flat_filtered = x_flat[inside]
#        y_flat_filtered = y_flat[inside]        
#                
#        if full_output:           
#            return zip(x_flat_filtered, y_flat_filtered), (x, y), inside, int(num)
#        else:                
#            return zip(x_flat_filtered, y_flat_filtered)    
        
    @classmethod
    def get_circular_with_N_max(clc, radius, N=1000, full_output=False):
        """
        """
        num = ceil(N**(0.5))
        k = inf
        bsup = False
        binf = False
        
        while any([not bsup, not binf]):
            sampling = linspace(-radius, radius, num)
        
            x, y = meshgrid(sampling, sampling)
            x_flat = x.flatten(); y_flat = y.flatten()
            radial = (x_flat**2 + y_flat**2)**(0.5)
        
            inside = radial <= radius
        
            k = x_flat[inside].shape[0]

            if k > N:
                bsup = True
                if binf and bsup:
                    break
                else:
                    num -= 1;
            elif k < N:
                binf = True
                if binf and bsup:
                    break
                else:
                    num += 1;
            else:
                binf = True
                bsup = True            
        
        x_flat_filtered = x_flat[inside]
        y_flat_filtered = y_flat[inside]        

        if full_output:
            return zip(x_flat_filtered, y_flat_filtered), (x, y), inside, int(num)
        else:
            return zip(x_flat_filtered, y_flat_filtered)

    @classmethod
    def get_polar(clc, radius, azimuth=2.*pi, n_radius=30, n_azimuth=360, 
                  type_azimuth='rad', discard_origin=True, cartesian=False, 
                  full_output=False):
        """
        the returned phi is always in `rad`, even if azimuth if given in `deg`.
        
        discard_origin: bool
            If True, and if radius_in = 0., then all the realisations of the 
            origin (0,0) will be kept. Actually, it will appear exactly 
            n_azimuth times. 
        """
        if n_radius == 1 and discard_origin: n_radius += 1
        
        if hasattr(radius, '__iter__'): # radius is an iterable
                if len(radius) == 2:
                    radius_in = radius[0]
                    radius_out = radius[1]
                elif len(radius) == 1:
                    radius_in = 0.
                    radius_out = radius[0]
                elif len(radius) > 2:
                    print 'Warning: len(radius) > 2. Only radius[:2] is used.'
                    radius_in = radius[0]
                    radius_out = radius[1] 
                else: #len(radius) == 0
                    pass
        else:
            radius_in = 0.
            radius_out = radius
            
        if hasattr(azimuth, '__iter__'): # azimuth is an iterable
                if len(azimuth) == 2:
                    azimuth_in = azimuth[0]
                    azimuth_out = azimuth[1]
                elif len(azimuth) == 1:
                    azimuth_in = 0.
                    azimuth_out = azimuth[0]
                elif len(azimuth) > 2:
                    print 'Warning: len(azimuth) > 2. Only azimuth[:2] is used.'
                    azimuth_in = azimuth[0]
                    azimuth_out = azimuth[1] 
                else: #len(azimuth) == 0
                    pass
        else:
            azimuth_in = 0.
            azimuth_out = azimuth
        
        if type_azimuth is 'deg': 
            azimuth_in = deg2rad(azimuth_in)
            azimuth_out = deg2rad(azimuth_out)
        
        sampling_radius = linspace(radius_in, radius_out, n_radius)
        sampling_angle = linspace(azimuth_in, azimuth_out, n_azimuth, 
                                  endpoint=True)
                
        r, phi = meshgrid(sampling_radius, sampling_angle)
        if discard_origin and radius_in == 0.0:
            r = r[:,1:]
            phi = phi[:,1:]        
        r_flat = r.flatten(); phi_flat = phi.flatten()
                        
        if cartesian:
            x = r_flat * cos(phi_flat)
            y = r_flat * sin(phi_flat) 
            inside = ones(len(x), dtype=bool)
            if full_output:
                return zip(x, y), (x.reshape(r.shape), y.reshape(r.shape)), inside
            else:
                return zip(x, y)
        else:                
            if full_output:
                return zip(r_flat, phi_flat), (r, phi)
            else:
                return zip(r_flat, phi_flat)        
