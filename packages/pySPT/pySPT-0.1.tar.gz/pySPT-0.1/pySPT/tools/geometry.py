#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 15:42:18 2017

@author: Sciences
"""

from numpy import array, empty, ones, zeros, copy, pi, inf
from numpy import newaxis, ones_like, dot, argmax, abs
from numpy import mean, linspace, arccos, sin, cos, arctan
from numpy import vstack, hstack, sum, where, append, argsort
from numpy import any, argmin, min, max, sqrt, rad2deg, isinf
from numpy.random import uniform, choice
from numpy.linalg import eig, inv
from random import random

__author__ = 'O. Wertz @ Bonn'
__all__ = ['centroid_polygon',
           'closest_node',
           'curve_extent',
           'Ellipse',
           'get_random_point_in_circle',
           'points_on_triangle_edge',
           'random_points_inside_triangle',
           'separate_closed_curves',
           'separation',
           'sort_curve',
           'Triangle',
           'triangle_angles',
           'triangles_filtering'
           ]

class Triangle(object):
    """Create a triangle object. Part of this code comes from L. Delchambre"""
    def __init__(self,v1,v2,v3):
      """
      Initialize a triangle based on its 3 vertices (v1,v2 and v3).
      Each vertex must be a list of the form [x y].
      """
      self.v1 = v1
      self.v2 = v2
      self.v3 = v3
      self.v = v1,v2,v3

    def __str__(self):
      return "({0},{1}) -> ({2},{3}) -> ({4},{5})".format(self.v1[0], self.v1[1],\
                                                          self.v2[0], self.v2[1],\
                                                          self.v3[0], self.v3[1])

    def __iter__(self):
      return iter([self.v1, self.v2, self.v3])

    @staticmethod
    def _point_pos(v1,v2,p):
      """
      Return the position of a point compared to an oriented line

      According to the returned value, ret, we have:
        ret > 0  : p stands to the right of the line joining v1 to v2
        ret < 0  : p stands to the left of the line joining v1 to v2
        ret == 0 : p stands on the line joining v1 to v2
      """
      return (p[0]-v1[0])*(v2[1]-v1[1])-(p[1]-v1[1])*(v2[0]-v1[0])

    def contains(self,v,eps=0):
      """
      Return true if this triangle contains the given point

      Input parameter:
      ----------------
        v The point to be tested
        eps : Tolerance to round-off errors
      """
      # Compute the position of the point according to the 2 first line segments
      d1 = Triangle._point_pos(self.v1, self.v2, v)
      d2 = Triangle._point_pos(self.v2, self.v3, v)
      # note: d3 would be Triangle._point_pos(self.v3, self.v1, v)

      if d1 < -eps:
        # If d1 is negative, then d2 and d3 should be negative or null
        if eps < d2 or eps < Triangle._point_pos(self.v3, self.v1, v):
          return False
      elif eps < d1:
        # If d1 is positive, then d2 and d3 should be positive or null
        if d2 < -eps or Triangle._point_pos(self.v3, self.v1, v) < -eps:
          return False
      else:
        # If d1 is null, then d2 and d3 should be of the same sign
        if d2 < -eps:
          if eps < Triangle._point_pos(self.v3, self.v1, v):
            return False
        elif eps < d2:
          if Triangle._point_pos(self.v3, self.v1, v) < -eps:
            return False
        # else d2 is null as well such that v == v2

      return True

    def barycenter(self):
      v1, v2, v3 = self.v1, self.v2, self.v3
      return [(v1[0]+v2[0]+v3[0])/3., (v1[1]+v2[1]+v3[1])/3.]


def curve_extent(curve, center=[0.0,0.0]):
    """
    Compute the min and max radial extents of a given curve wrt to its 
    center (default=[0,0]).
    
    If max >> min, thus there must exist points on the curve for which the 
    curvature radius R is small in comparison to the mean curve extent. 
    The condition (max >> min) is sufficient but not necessary for having 
    R <<. Indeed, consider the curve that locates the projection of the 
    Earth axis rotation during its precession and nutation mouvements on 
    the celestial sphere. Even though max >~ min, the curvature radius is 
    everywhere small in comparison to the mean curve extent.
    
    """
    assert curve.ndim == 2, 'The input data must be a Nx2 array'
    
    extents = sqrt(sum((curve - array([center,]*len(curve)))**2, axis=1))
    return extents.min(), extents.max()

def separation(points, reference=[0.0,0.0]):
    """
    Compute the separation of a bunch of positions wrt to a reference 
    point (default=[0,0]).
    """
    assert points.ndim == 2, 'The input data must be a Nx2 array'    
    return sqrt(sum((points - array([reference,]*len(points)))**2, axis=1))

def centroid_polygon(arr):
    """
    Compute (a simple formulation of) the centroid of a closed polygon.
    """
    length = arr.shape[0]
    sum_x = sum(arr[:, 0])
    sum_y = sum(arr[:, 1])
    return sum_x/length, sum_y/length

def random_points_inside_triangle(triangle, N=100):
    """
    plt.figure()
    plt.hold(True)
    plt.plot(y[:,0], y[:,1], ',m')
    plt.plot(np.append(triangle[:,0], triangle[0,0]), np.append(triangle[:,1], triangle[0,1]), 'r')
    plt.xlim([-2,2])
    plt.ylim([-2,2])
    plt.show()    
    """
    obj_tr = Triangle(*triangle)
    tr_center = mean(triangle[1:,:], axis=0)
    
    v1 = triangle[1,:] - triangle[0,:]
    v2 = triangle[2,:] - triangle[0,:]

    a1, a2 = uniform(0,1,(2,N))
    
    x = array([_a1*v1+_a2*v2 for _a1,_a2 in zip(a1,a2)]) + vstack(tuple([triangle[0,:] for _ in range(N)]))
    y = array([pos if obj_tr.contains(pos) else [-(pos[0]-tr_center[0])+tr_center[0],-(pos[1]-tr_center[1])+tr_center[1]] for pos in x])    
    return y

def points_on_triangle_edge(triangle, N=10, vertex=False):
    """
    """
    K = N#floor(N/3.0)
    
    slope = [(_[1][1]-_[0][1])/(_[1][0]-_[0][0]) 
             if (_[1][0]-_[0][0])!=0.0 
             else inf 
             for _ in zip(triangle, triangle[(1,2,0),:])]
    
    P = empty([0,2])
    for m, Z in zip(slope, zip(triangle, triangle[(1,2,0),:])):
        if vertex:
            x = linspace(Z[0][0],Z[1][0],K+2)[:]
        else:
            x = linspace(Z[0][0],Z[1][0],K+2)[1:-1]
            
        if isinf(m):
            if vertex:
                y = linspace(Z[0][1], Z[1][1],K+2) 
            else:
                y = linspace(Z[0][1], Z[1][1],K+2)[1:-1]            
        else:
            y = [m*(_x-Z[0][0])+Z[0][1] for _x in x]
        P = vstack((P, array(zip(x,y))))   
    return P

def triangles_filtering(triangles, threshold=1.0):
    """
    """
    
    triangles_ok = []
    indices_ok = []
    
    for k,tr in enumerate(triangles):
        angle_min = triangle_angles(tr).min()
        if angle_min > threshold:
            triangles_ok.append(tr)
            indices_ok.append(k)
             
    return array(triangles_ok), array(indices_ok)

def triangle_angles(triangle):
    """
    """
    def dotproduct(v1, v2):
        return sum((a*b) for a, b in zip(v1, v2))
    
    def length(v):
        return sqrt(dotproduct(v, v))
    
    def angle(v1, v2):
        temp = dotproduct(v1, v2) / (length(v1) * length(v2))
        if temp == 1.0:
            return 0.0
        elif temp == -1.0:
            return pi
        else:
            return arccos((min((1.0,max((temp,-1.0))))))
    
    v1 = triangle[1,:]-triangle[0,:]
    v2 = triangle[2,:]-triangle[0,:]
    v3 = triangle[0,:]-triangle[1,:]
    v4 = triangle[2,:]-triangle[1,:]
    
    if (array([length(v1),length(v2),length(v3),length(v4)])==0).any():
        return zeros(3)
    else:
        alpha1 = rad2deg(angle(v1, v2))
        alpha2 = rad2deg(angle(v3, v4))    
        return array([alpha1, alpha2, 180.0-alpha1-alpha2])

def get_random_point_in_circle(radius, center=(0,0)):
    """
    """
    t = 2 * pi * random()
    u = random() + random()
    r = None

    if u > 1:
        r = 2 - u
    else:
        r = u

    result = radius * r * cos(t) + center[0], radius * r * sin(t) + center[1]
    return result

def separate_closed_curves(points, closed=True, treshold=10):
    """
    TODO: en option, on pourrait checker si le nombre de Ncurves demandé est 
    consistent avec les données. Par exemple, si on ferme la curve, on s'attend
    à ce que le dernier et premier point soit proche au sens que leur distance
    est comparable à la distance médiane entre tous les points de la courbe. Si
    cette distance est anormalement élevée (critère à définir), on peut supposer
    que la courbe est ouverte, et donc que Ncurves est trop élevé. On pourrait
    envisager un processus itératif où l'on réduit le Ncurves à chaque étape 
    jusqu'à ce que toutes les courbes fermées soient bien fermées.
    """
    #assert isinstance(Ncurves, int), 'Ncurves must be an integer > 0'
    #assert Ncurves > 0, '{:.0f} is not an acceptable number of curves'.format(Ncurves)
    
    if isinstance(points,list) and not isinstance(points[0],float):
        assert len(points) == 1, 'When `points` is a list, it must contain only one array.'
        points = points[0]
    
    pointsSorted, _, D = sort_curve(points, full_output=True)
    
    _J = 0
    i = 0
    
    assert i >= _J, 'We test only the points at larger position in the sortCurve list than the reference: i >= _J'
    
    _i_arg0 = 0
    count = 0
    indices = [0]
    
    while i < len(D)-2 and count < 2*len(D): 
        while _i_arg0 == 0 and i < len(D)-2:
            _i_arg0 = separation(pointsSorted[i:,:], 
                                 pointsSorted[_J,:]).argsort()[0]
            i += 1
        else:
            _i_arg0 += (i-1)
            indices.append(_i_arg0)
            _J = _i_arg0+1
            i = _i_arg0+1
            _i_arg0 = 0
        count += 1
    else:
        indices.append(len(pointsSorted)-1)
        
    indices = [(indices[h]+1, indices[h+1]) if k !=0 else (0, indices[1]) for k,h in enumerate(range(len(indices)-1))]       
    
    CURVES = []
    
    for iii in indices:
        temp = pointsSorted[iii[0]:iii[1],:]
        if len(temp) > treshold and closed:
            CURVES.append(vstack((temp,temp[0,:])))
        elif len(temp) > treshold and not closed:
            CURVES.append(temp)
        else:
            pass
        
    ind = argsort([len(_) for _ in CURVES])[::-1]

    return [CURVES[j] for j in ind]

def closest_node(node, nodes):
    """
    """
    deltas = nodes - node
    dist_2 = sum(deltas**2, axis=1)
    return argmin(dist_2), min(dist_2)**(0.5)

def sort_curve(points, full_output=False):
    """
    """
    J = len(points)
    index = array([choice(range(J))])
    separations = zeros(J)    
    mask = ones(J, dtype=bool)

    cl = copy(points)
    
    count = 0
    mask[index[-1]] = False   

    while sum(mask) > 0 and count <= 2*J: # while there are points not yet sorted (with a security cut)
        #print count, 
        
        # Find the index of the closest vertex wrt the last one, as well as 
        # the corresponding separation.
        _j, sep = closest_node(cl[index[-1]], cl[mask]) 
        separations[count] = sep

        # Find the index of the closest vertex in the original matrix of points.
        # This can't be done on cl[mask] because the latter decreases at each 
        # step, which bias the index.
        _jj_all = where((cl == cl[mask][_j]).all(axis=1)) #where(cl==cl[mask][_j])[0]

        if len(_jj_all) > 2:
            multiplicity = array([_ in index for _ in _jj_all])
            if not any(multiplicity):
                _jj = _jj_all[closest_node(cl[index[-1]], cl[_jj_all])[0]]
            else:
                _jj = _jj_all[where(multiplicity==False)[0][0]]
        else:
            _jj = _jj_all[0]

        index = append(index, _jj)        

        mask[index[-1]] = False
        count += 1  
    
    # Extra Filtering
    VALID = [len(points)]
#    Nmax = 20
#    hMax = 0.0
#    down_count = 0
#    while_counter = 0
#    VALID = [0]
#    i = 0
#    
#    while VALID[-1]+i <= len(points[index]) and while_counter < 100 :
#        _sep = separation(points[index][VALID[-1]+1:],points[index][VALID[-1]+1])
#        for i,_s in enumerate(_sep):
#            if _s > hMax:
#                hMax = _s
#                down_count = 0
#            else:
#                down_count += 1
#    
#            if down_count > Nmax:
#                amin = separation(points[index][(i-Nmax+VALID[-1]):],
#                                  points[index][VALID[-1]]).argmin()
#                VALID.append(i-Nmax + amin + VALID[-1])
#                down_count = 0
#                hMax = 0
#                break
#        while_counter += 1    
    
        
    if full_output:
        return points[index][:VALID[-1]], index[:VALID[-1]], separations[:VALID[-1]]
    else:
        return points[index][:VALID[-1]]
    
    
class Ellipse(object):
    """
    """
    def __init__(self, x, y):
        """
        """
        self.x = x
        self.y = y
        
        self.parameters = None
        
        self.center = None
        self.rotangle = None
        self.axis = None
        
    def fitEllipse(self):
        """
        """
        if self.parameters is not None:
            return self.parameters
        else:
            x = self.x[:,newaxis]
            y = self.y[:,newaxis]
            D =  hstack((x*x, x*y, y*y, x, y, ones_like(x)))
            S = dot(D.T,D)
            C = zeros([6,6])
            C[0,2] = C[2,0] = 2; C[1,1] = -1
            E, V =  eig(dot(inv(S), C))
            n = argmax(abs(E))
            self.parameters = V[:,n]
            return self.parameters
    
    def ellipse_center(self):
        """
        """
        if self.center is not None:
            return self.center
        else:
            if self.parameters is None:
                a = self.fitEllipse()
            else:
                a = self.parameters
            b,c,d,f,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[0]
            num = b*b-a*c
            x0=(c*d-b*f)/num
            y0=(a*f-b*d)/num
            self.center = array([x0,y0])
            return self.center
    
    def ellipse_angle_of_rotation2(self):
        """
        """
        if self.rotangle is not None:
            return self.rotangle
        else:
            if self.parameters is None:
                a = self.fitEllipse()
            else:
                a = self.parameters            
            b,c,a = a[1]/2, a[2], a[0]
            if b == 0:
                if a > c:
                    return 0
                else:
                    return pi/2
            else:
                if a > c:
                    return arctan(2*b/(a-c))/2
                else:
                    return pi/2 + arctan(2*b/(a-c))/2
    
    
    def ellipse_axis_length(self):
        """
        """
        if self.axis is not None:
            return self.axis
        else:
            if self.parameters is None:
                a = self.fitEllipse()
            else:
                a = self.parameters          
            b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
            up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
            down1=(b*b-a*c)*( (c-a)*sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
            down2=(b*b-a*c)*( (a-c)*sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
            res1=sqrt(up/down1)
            res2=sqrt(up/down2)
            self.axis = array([res1, res2])        
            return self.axis