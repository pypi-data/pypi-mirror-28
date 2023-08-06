#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 15:32:53 2017

@author: Sciences
"""

from colorsys import rgb_to_hsv, hsv_to_rgb
from operator import itemgetter

from numpy import array, floor
from numpy.random import choice
from matplotlib.pylab import subplots, savefig, show
from matplotlib.patches import Rectangle

__author__ = 'O. Wertz @ Bonn'
__all__ = ['Colors']

class Colors(object):
    """
    """
    def __init__(self):
        """
        """
        # BLUE
        self.blue = '#62B2FF'
        self.darkblue = '#6664B5'
        self.middleblue = '#6560FF'
        self.cyan = '#00CFFA'
        self.mist = '#90AFC5'
        self.stone = '#336B87'
        self.waterfall = '#68829E'
        self.wave = '#66A5AD'
        self.blueblack = '#021C1E'
        self.rain = '#2C7873'
        self.sky = '#375E97'
        self.bluesky = '#4CB5F5'
        self.lagoon = '#6AB187'
        self.sea = '#20948B'
        self.ice = '#A1D6E2'
        self.glacierblue = '#1995AD'
        self.indigo = '#2D4262'
        self.navy = '#00293C'
        self.peacockblue = '#1E656D'
        self.electricblue = '#4897D8'
        self.grecianblue = '#2988BC'
        
        # RED
        self.red = '#F96A62'  
        self.petal = '#F98866'   
        self.redclay = '#A43820'  
        self.berry = '#EC96A4'  
        self.hotpink = '#F52549'
        self.bubblegum = '#FA6775'  
        self.strawberry = '#CB0000'
        self.candyapple = '#F62A00' 
        self.raspberry = '#ED5752'
        self.rubyred = '#FA4032'
        self.redpepper = '#C60000'
        self.phoneboothred = '#D70026'
        self.fuschia = '#E1315B'

        # ORANGE 
        self.orange = '#FFB55E'  
        self.sunset = '#FB6542'
        self.tangerine = '#F0810F'
        self.marmalade = '#F25C00'
        
        # YELLOW
        self.sunflower = '#FFBB00'    
        self.yellow = '#F7FF5D' 
        self.sandstone = '#F4CC70'
        self.yellowpaper = '#F5BE41'
        self.lemon = '#EDAE01'
        self.lemontea = '#E1B80D'
        self.golden = '#EFB509'
        
        # GREEN
        self.green = '#B5FFA5'        
        self.springgreen = '#89DA59'
        self.avocado = '#258039'
        self.lettuce = '#B8D20B'
        self.emerald = '#265C00'
        self.greenbean = '#68A225'
        self.lightgreen = '#B3DE81'
        self.deepaqua = '#128277'
        
        # OTHERs
        self.thundercloud = '#505160'
        self.granite = '#B7B8B6'
        self.forest = '#1E434C'
        self.overcast = '#BCBABE'
        self.ivory = '#F1F3CE'
        self.slate = '#626D71'
        self.latte = '#DDBC95'
        self.fig = '#4C3F54'
        self.blackseaweed = '#231B12'
        self.smoke = '#C0B2B5'
        self.pearl = '#F8F5F2'
        self.craftpaper = '#CDAB81'
        
    def get_rgb(self, hexrgb, norm=True):
        """
        """
        hexrgb = hexrgb.lstrip('#')
        rgb = array([int(hexrgb[i:i+2], 16) for i in (0, 2 ,4)])
        if norm:
            return tuple(rgb/255.)
        else:
            return tuple(rgb)
    
    def get_all_colors_name(self):
        """
        """
        names = [_ for _ in dir(self) if (not _.startswith('__') and 
                                          not _.startswith('palette') and
                                          not _.startswith('get_'))]
        return names
    
    def get_all_colors_hex(self):
        """
        """
        return [getattr(self, name) for name in self.get_all_colors_name()] 
    
    def get_all_colors_item(self):
        """
        """
        return zip(self.get_all_colors_name(), self.get_all_colors_hex())
    
    def get_random_colors(self, N=1, output='hex'):
        """
        """
        colors = self.get_all_colors_hex()
        
        if N > len(colors):
            rep = True
        else:
            rep = False
        
        c = choice(colors, size=N, replace=rep)
        
        if output is 'hex':
            return c
        elif output is 'rgb':
            if N > 1:
                return [self.get_rgb(_) for _ in c]
            else:
                return self.get_rgb(c[0])
    
    def get_hsv(self, hexrgb):
        """
        """
        hexrgb = hexrgb.lstrip("#")
        r, g, b = (int(hexrgb[i:i+2], 16) / 255.0 for i in xrange(0,5,2))
        return rgb_to_hsv(r, g, b) 
    
    def get_sorted_colors(self):
        """
        """
        chex = self.get_all_colors_hex()
        names = self.get_all_colors_name()
        
        items = [(n,self.get_hsv(_hex)) for n,_hex in zip(names,chex)]
        items_sorted = sorted(items, key=itemgetter(1))
        
        return items_sorted
    
    def palette(self, sort='name', save=False):
        """
        """
        if sort is 'name':
            color_names = self.get_all_colors_name()
            color_hex = self.get_all_colors_hex()
        elif sort is 'hsv':
            items = self.get_sorted_colors()
            color_names, color_hsv = zip(*items) 
            color_hex = [hsv_to_rgb(*hsv) for hsv in color_hsv]
        
        # FIGURE
        # ------
        fig, ax = subplots(1, 1, sharex=False, sharey=False, figsize=(10,10))
        
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        
        ### Main --------------------
        ax.text(5, 28, r'Colors available in the class `colors`', 
                size=16, rotation=0., ha="left", va="center")
        
        mid = int(floor(len(color_hex)/2))
        for k in range(mid):
            pos1 = (0, -k*15)
            rect1 = Rectangle(pos1, 20, 10, color=color_hex[k])
            ax.add_patch(rect1)
            ax.text(30, 4-k*15, '{}'.format(color_names[k]), 
                    size=12, rotation=0., ha="left", va="center")
            
            pos2 = (160, -k*15)
            rect2 = Rectangle(pos2, 20, 10, color=color_hex[k+mid])
            ax.add_patch(rect2)
            ax.text(190, 4-k*15, '{}'.format(color_names[k+mid]), 
                    size=12, rotation=0., ha="left", va="center")    
            
        ax.set_xlim([-5, 300])
        ax.set_ylim([-500, 50])   
        
        ax.set(adjustable='box-forced', aspect='equal')
        
        ### Save and show -----------
        if save:
            savefig('palette.pdf', dpi=900, bbox_inches='tight', 
                    pad_inches=0.1)
            show()        
        else:
            show()
            
            
if __name__ == '__main__':
    Colors().palette('hsv')