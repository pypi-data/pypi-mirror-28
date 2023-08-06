# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 09:03:53 2016

@author: Olivier Wertz, Ludovic Delchambre

FIXME: THE NAME `caustics` DOES NOT CORRESPOND TO WHAT THIS CLASS DOES. 
THIS CODE SHOULD BE MOVED INTO THE `lensing` SUBPACKAGE.
"""

from itertools import product
from random import uniform

from numpy import meshgrid, linspace, array, ceil
from numpy.random import rand, choice
from scipy.spatial import Delaunay

from ..tools.geometry import Triangle

__author__ = 'O. Wertz @ Bonn'
__all__ = ['GLCaustics']

class GLCaustics(object):
    """
    Object designed to represent the (rough) caustics curves of a lens model based
    on the mapping existing from the image positions to the source position.
    """
    def __init__(self, model_backwards_source_function, model_args, \
                 xmin=0., xmax= 1., nx= 100, \
                 ymin=0., ymax= 1., ny= 100, 
                 critical_lines=None, caustic_lines=None, triangle=None):
        """
        Construct an instance of the GL_caustics object based on the GL model
        methods or function allowing to pass from the GL image position to the
        source positions.
    
        In more details, this constuctor build a tesselation of the image plane
        through the use of a patch of triangles and map the latter to the source
        plane in order to have an approximation of the caustic curves associated
        with the provided model and model parameters.
    
        Input parameter:
        ----------------
        model_backwards_source_function : callable object 
            Must have the signature
            vs = model_backwards_source_function(model_args, vi) 
            where:
            vi is a list of the image plane coordinates in the form [x y]
            vs is the source plane coordinates corresponding to v (form [x y])
        
        model_args : The argument to pass to model_backwards_source_function
        xmin : The minimal x sampling point of the grid in the image plane
        xmax : The maximal x sampling point of the grid in the image plane
        nx   : The number of sampling point of the grid in the image plane in the x direction
        ymin : The minimal y sampling point of the grid in the image plane
        ymax : The maximal y sampling point of the grid in the image plane
        ny   : The number of sampling point of the grid in the image plane in the y direction
        """
    
        self.xrange = (xmin, xmax, nx)
        self.yrange = (ymin, ymax, ny) 
        
        self.cl = critical_lines
        self.cc = caustic_lines
        
        self.triangle = triangle
        
        self.model_backwards_source_function = model_backwards_source_function
        self.model_args = model_args
        
        self._source_tr = []
        self._image_tr = []
        
        X, Y = meshgrid(linspace(xmin,xmax,nx), linspace(ymin,ymax,ny))   
        l0, c0 = X.shape
        
        
        IMup   = array([[[(ax,ay),(bx,by),(cx,cy)] for ax,bx,cx,ay,by,cy in zip(X[:-1,i],X[:-1,i+1],X[1:,i],Y[:-1,i],Y[:-1,i+1],Y[1:,i])] for i in range(c0-1)])
        IMdown = array([[[(ax,ay),(bx,by),(cx,cy)] for ax,bx,cx,ay,by,cy in zip(X[:-1,i+1],X[1:,i],X[1:,i+1],Y[:-1,i+1],Y[1:,i],Y[1:,i+1])] for i in range(c0-1)])     
        
        IMshape = IMup.shape
        
        for i0, i1 in product(*map(xrange, (IMshape[0], IMshape[1]))):
            self._image_tr.append(Triangle(*IMup[i0,i1,:,:]))
            self._image_tr.append(Triangle(*IMdown[i0,i1,:,:]))     
            
        S = array([self.model_backwards_source_function(model_args, (x,y)) for x,y in zip(X.flatten(), Y.flatten())])
        SX = S[:,0].reshape(X.shape)
        SY = S[:,1].reshape(Y.shape) 
        
        Tup   = array([[[[ax,ay],[bx,by],[cx,cy]] for ax,bx,cx,ay,by,cy in zip(SX[:-1,i],SX[:-1,i+1],SX[1:,i],SY[:-1,i],SY[:-1,i+1],SY[1:,i])] for i in range(c0-1)])
        Tdown = array([[[[ax,ay],[bx,by],[cx,cy]] for ax,bx,cx,ay,by,cy in zip(SX[:-1,i+1],SX[1:,i],SX[1:,i+1],SY[:-1,i+1],SY[1:,i],SY[1:,i+1])] for i in range(c0-1)])    
        
        Tshape = Tup.shape
        
        for i0, i1 in product(*map(xrange, (Tshape[0], Tshape[1]))):
            self._source_tr.append(Triangle(*Tup[i0,i1,:,:]))
            self._source_tr.append(Triangle(*Tdown[i0,i1,:,:])) 
        
    def subtiling(self, triangle, N=10):
        """
        """
        coord = array(triangle.v)
        xmin = coord[:,0].min()
        xmax = coord[:,0].max()
        ymin = coord[:,1].min()
        ymax = coord[:,1].max()
        
        points = [triangle.v1, triangle.v2, triangle.v3] 
        
        while len(points) <= N:
            candidate = (uniform(xmin,xmax), uniform(ymin,ymax))
            if triangle.contains(candidate): points.append(candidate)
          
        delaunay = Delaunay(points)
        sub_img_vertex = array(points)[delaunay.simplices]
        
        sub_img_triangles = [Triangle(_[0,:],_[1,:],_[2,:]) for _ in sub_img_vertex]
        sub_src_triangles = [Triangle(self.model_backwards_source_function(self.model_args, _[0,:]),
                                      self.model_backwards_source_function(self.model_args, _[1,:]),
                                      self.model_backwards_source_function(self.model_args, _[2,:])) for _ in sub_img_vertex]
          
        return sub_img_triangles, sub_src_triangles, sub_img_vertex
      
    def images(self, src_pos, eps = 0, src_trs=None, img_trs=None, full_output=False):
        """
        """
        if src_trs is None: src_trs = self._source_tr
        if img_trs is None: img_trs = self._image_tr
    
        res = []
        index = []
        for k, (src_tr, img_tr) in enumerate(zip(src_trs, img_trs)):
            if src_tr.contains(src_pos,eps):
                res.append(img_tr.barycenter())
                index.append(k)
            k += 1
            
        if full_output:
            return res, index # res should always be non-empty
        else:
            return res
    
    def sources_tr(self, img_pos, eps = 0):
        """
        """
        for src_tr, img_tr in zip(self._source_tr, self._image_tr):
            if img_tr.contains(img_pos,eps):
                return src_tr.barycenter()
            return [] # We should never get here
    
    def plotTiling(self, src_pos=None, imgs=None):
        """
        """
        import matplotlib.pylab as plt      
        from matplotlib.patches import Polygon
        from matplotlib.collections import PatchCollection      
      
        if src_pos is not None:
            img, index = self.images(src_pos, full_output=True)
            patches = []
            patchesS = []
        else:
            index = []
      
        fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10,10))
        plt.hold(True)
      
        for k, tri in enumerate(self._image_tr):
            if k in index and src_pos is not None:
                polygon = Polygon(self._image_tr[k].v, True)
                patches.append(polygon)
                p = PatchCollection(patches, cmap=plt.cm.gray, alpha=0.7)
                ax1.add_collection(p)
    
                polygonS = Polygon(self._source_tr[k].v, True)
                patchesS.append(polygonS)
                pS = PatchCollection(patchesS, cmap=plt.cm.jet, alpha=0.1)
                colors = 100*rand(len(patchesS))
                pS.set_array(array(colors))              
                ax2.add_collection(pS)
              
            ax1.plot([tri.v1[0], tri.v2[0], tri.v3[0], tri.v1[0]], 
                     [tri.v1[1], tri.v2[1], tri.v3[1], tri.v1[1]], 
                     '.-k')
          
        for k, tri in enumerate(self._source_tr):        
            ax2.plot([tri.v1[0], tri.v2[0], tri.v3[0], tri.v1[0]], 
                     [tri.v1[1], tri.v2[1], tri.v3[1], tri.v1[1]], 
                     '.-k')          
          
            ax2.plot(src_pos[0], src_pos[1], 'or')                  
              
        c0 = array([255,181,94])/255. ##orange   
    
        if self.cl is not None:      
            for _cl in self.cl:
                ax1.plot(_cl[:,0], _cl[:,1], color=c0)
              
                spec = choice(range(len(_cl)), ceil(len(_cl)/10))
                ax1.plot(_cl[spec,0], _cl[spec,1], '.r')
              
              
        if self.cc is not None:      
            for _cc in self.cc:
                ax2.plot(_cc[:,0], _cc[:,1], color=c0) 
      
        if imgs is not None:
            ax1.plot(imgs[:,0], imgs[:,1], 'oy')
          
        ax1.set_xlim(self.xrange[0]-0.1, self.xrange[1]+0.1)
        ax1.set_ylim(self.yrange[0]-0.1, self.yrange[1]+0.1)
      
        if src_pos is not None:
            lim = 0.2
            ax2.set_xlim(src_pos[0]-lim, src_pos[0]+lim)
            ax2.set_ylim(src_pos[1]-lim, src_pos[1]+lim)      
      
        ax1.set(adjustable='box-forced', aspect='equal')
        ax2.set(adjustable='box-forced', aspect='equal')
      
        plt.show()
        return None
  