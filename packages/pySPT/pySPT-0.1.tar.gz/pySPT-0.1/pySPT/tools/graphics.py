#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from copy import deepcopy

from numpy import arange, round, logspace, log10, linspace, array, ceil, floor
from numpy import float32
from matplotlib.ticker import ScalarFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.pyplot import contourf, close, gcf
from matplotlib.cm import get_cmap
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
        
from ..tools.container import HandlingDict

__author__ = 'O. Wertz @ Bonn'
__all__ = ['Colorbar',
           'Data',
           'Graphics']

def ceil_decimal(x, decimals=2):
    return ceil(x * 10**decimals) / 10**decimals

def floor_decimal(x, decimals=2):
    return floor(x * 10**decimals) / 10**decimals

class Data(object):
    """
    """
    def __init__(self):
        """
        """
        pass
    
    def xylimits(self, x, y=None):
        """
        """
        if not isinstance(x,list) and y is None: 
            xlim = [x[:,0].min(),x[:,0].max()]
        elif not isinstance(x,list) and y is not None: 
            xlim = [x.min(),x.max()]
        elif isinstance(x,list) and y is None:
            xlim = [array([_x[:,0].min() for _x in x]).min(), 
                    array([_x[:,0].max() for _x in x]).max()]
        else:
            pass

        if not isinstance(x,list) and y is None: 
            ylim = [x[:,1].min(),x[:,1].max()]
        elif isinstance(x,list) and y is None:
            ylim = [array([_x[:,1].min() for _x in x]).min(),
                    array([_x[:,1].max() for _x in x]).max()]
        elif y is not None: 
            if not isinstance(y, list):
                ylim = [y.min(),y.max()]
            elif isinstance(y, list):
                ylim = [array([_y.min() for _y in y]).min(),
                        array([_y.max() for _y in y]).max()]
            else:
                pass
        else:
            pass
        
        return (xlim, ylim)
    
class Colorbar(object):
    """
    """
    def __init__(self, z):
        """
        """
        self.z = z
        self.zmax = z.max()
        self.zmin = z.min()
        
    def unbound_colorbar(self, clmap='magma_r', n=101, level_min=None, 
                         level_max=None):
        """
        """
        cmap = get_cmap(clmap)
        
        if level_min is None: level_min = self.zmin
        if level_max is None: level_max = self.zmax
        
        levels = linspace(level_min, level_max, n)
        
        cs = contourf([[0,0],[0,0]], levels, cmap=cmap)
        close()
        
        return cs

    def add_colorbar(self, fig, ax, n=11, clmap='magma_r', level_min=None, 
                     level_max=None, label='', aspect=20, pad_fraction=0.5,
                     tick_prec=2, tick_sample=None, fontsize=16, squared=False,
                     full_output=False):
        """
        WARNING: if `fig` already possesses a colorbar, `add_colorbar()` will
        stack a new one, whatever the presence of the old one. It's cool when
        you want several colorbars but take care to not stack multiple 
        occurences of the same colorbar.
         
        """                    
        #print len(fig.get_axes())
        
        if level_min is None: level_min = self.zmin
        if level_max is None: level_max = self.zmax            
        
        divider = make_axes_locatable(ax)
        width = axes_size.AxesY(ax, aspect=1./aspect)
        pad = axes_size.Fraction(pad_fraction, width)
        cbar_ax = divider.append_axes("right", size=width, pad=pad)        

        if tick_sample is None:
            cbar_yticks = linspace(level_min, level_max, 11, dtype=float32)
        else:
            cbar_yticks = tick_sample
            
        if tick_prec == 1:
            cbar_yticks_labels = ['{:.1f}'.format(k) for k in cbar_yticks]
        elif tick_prec == 2:
            cbar_yticks_labels = ['{:.2f}'.format(k) for k in cbar_yticks]
        elif tick_prec == 3:
            cbar_yticks_labels = ['{:.3f}'.format(k) for k in cbar_yticks]
        elif tick_prec == 4:
            cbar_yticks_labels = ['{:.4f}'.format(k) for k in cbar_yticks] 
        elif tick_prec == 12:
            cbar_yticks_labels = ['{:.12f}'.format(k) for k in cbar_yticks]             
        else:
            cbar_yticks_labels = ['{:.2f}'.format(k) for k in cbar_yticks]            

        cbar_yticks_labels[-1] = r'$\geq$' + cbar_yticks_labels[-1]
        
        cs = self.unbound_colorbar(clmap, n*15, level_min, level_max)
        cbar = fig.colorbar(cs, cax=cbar_ax, format='%.3f', ticks=cbar_yticks)
        cbar.set_label(label, rotation=90, fontsize=fontsize, labelpad=3, 
                       y=0.5)
        cbar.ax.tick_params(labelsize=10)
        cbar.ax.set_yticklabels(cbar_yticks_labels)

        if squared:
            ax.set_aspect(1.0)
        
        if full_output:
            return cbar, fig, ax
        else:
            return None


class Graphics(object):
    """
    """
    def __init__(self):
        pass
    
    def tick_logspace(self, xmin, xmax, N=4, decimals=1):
        """
        """
        res = logspace(log10(xmin),log10(xmax), 
                       num=N, endpoint=True, base=10.0)
        res[0] = ceil_decimal(res[0], decimals)
        res[-1] = floor_decimal(res[-1], decimals) 
        res[1:-1] = round(res[1:-1], decimals)
        
        return res
        
    def tick_linspace(self, xmin, xmax, N=4, decimals=1):
        """
        """
        return round(linspace(xmin,xmax, num=N, endpoint=True), decimals)    
        
    def set_ticklabels(self, xmin, xmax, axis='x', N=4, decimals=1, scale='linear'):
        """
        """
        assert axis is 'x' or axis is 'y', '`axis` must be either `x` or `y`.'
        
        if scale is 'linear':
            ticks = self.tick_linspace(xmin, xmax, N, decimals)
        elif scale is 'log':
            ticks = self.tick_logspace(xmin, xmax, N, decimals) 
        else:
            ticks = self.tick_linspace(xmin, xmax, N, decimals)  
           
        if axis is 'x':
            return {'set_xticks': ticks}
        elif axis is 'y':
            return {'set_yticks': ticks}    
    
    def custom_axis(self, axis, options=None, **kwargs):
        """ Apply changes to a matplotlib axes object according to the options 
        passed as a dictionary.
        
        Parameters
        ----------
        axis : matplotlib.axes object
            The axes object we want to modify.
        options : dict
            Set of options. A dictionary key must corresponds to a valid axes 
            method name. See Notes for more details.        
            
        Return
        ------
        matplotlib.axes object 
        
        Notes
        -----
        The argument `options' must be a dict whose keys must correspond to valid
        axes method name. For example: 
            
            options = {'set_xticks':[1.0,5.0,10.0]}.
    
        When calling a method that takes multi arguments, the corresponding
        dict value can be either a dictionary (for kwargs arguments only) 
        or a 2-tuple composed of a n-tuple (for n args) and a dictionary 
        (for the kwargs). For example: 
            
            options = {'set_xlabel':((r'$\theta$',),{'fontsize':20})} 
            
        or equivalently
        
            options = {'set_xlabel':{'xlabel':r'$\theta$', 'fontsize':20})}    
        
        """
        axis.set_xscale(options.pop('set_xscale','linear'))
        axis.set_yscale(options.pop('set_yscale','linear'))
        
        # Modify the default tick label sizes without overriding the 
        # user's choice.
        # https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller
        tickdefaultlabelsize = kwargs.pop('tickdefaultlabelsize',16)
        
        if not options.has_key('set_xticklabels'):
            for tick in axis.xaxis.get_major_ticks():
                tick.label.set_fontsize(tickdefaultlabelsize)            
            
        if not options.has_key('set_yticklabels'):            
            for tick in axis.yaxis.get_major_ticks():
                tick.label.set_fontsize(tickdefaultlabelsize)     

        # Loop through the rest of options
        for key,val in options.items():
            if isinstance(val,dict):
                getattr(axis,key)(**val)
            elif (isinstance(val,tuple) and len(val)==2 
                  and isinstance(val[0],tuple) and isinstance(val[1],dict)):
                getattr(axis,key)(*val[0], **val[1])
            else:
                getattr(axis,key)(val)
    
        if options.has_key('set_xticks'):
            axis.get_xaxis().set_major_formatter(ScalarFormatter())
            
        if options.has_key('set_yticks'):
            axis.get_yaxis().set_major_formatter(ScalarFormatter())            
            
        return axis
    
    def axes(self, fig, grid=(1,1), **kwargs):
        """
        """            
        sharex = kwargs.pop('sharex', False)
        sharey = kwargs.pop('sharey', False)

        l,c = grid
        
        if grid == (1,1):
            axs = fig.add_subplot(1,1,1, **kwargs)
        else:
            if not sharex and not sharey:
                axs = [fig.add_subplot(l, c, _n, **kwargs) 
                            for _n in arange(1,l*c + 1)]
            elif sharex and not sharey:
                axs = []
                axs.append(fig.add_subplot(l, c, 1, **kwargs))
                axs = axs + [fig.add_subplot(l, c, _n, sharex=axs[0], **kwargs) 
                                for _n in arange(2,l*c + 1)]
            elif sharey and not sharex:
                axs = []
                axs.append(fig.add_subplot(l, c, 1, **kwargs))
                axs = axs + [fig.add_subplot(l, c, _n, sharey=axs[0], **kwargs) 
                                for _n in arange(2,l*c + 1)] 
            else:
                axs = []
                axs.append(fig.add_subplot(l, c, 1, **kwargs))
                axs = axs + [fig.add_subplot(l, c, _n, sharex=axs[0], 
                                             sharey=axs[0], **kwargs) 
                                for _n in arange(2,l*c + 1)]       
        
        return fig, axs
    
    def build_figure(self, grid=(1,1), subplots_opts={}, axis_opts={}, 
                     figsize=None, **kwargs):
        """
        
        Parameters
        ----------
        subplots_opts : dict
            Options passed to self.axes() to custom the subplots with 
            fig.add_subplot(...,**subplots_opts). For example, 
            subplots_opts = {'sharex':True, 'sharey':True}.
        axis_opts : dict or list of dict
            Options passed to self.custom_axis() to deal with fancy axis 
            options. See `custom_axis` docstring for more details. A list of
            dicts can be used to costumize a list of axes.
          
        """
        # TODO: https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller
        if subplots_opts: 
            sp_opts = deepcopy(subplots_opts)
        else:
            sp_opts = {}
            
        if figsize is None:
            figsize = sp_opts.pop('figsize',(4,4))
        
        fig = Figure(figsize=figsize)
        canvas = FigureCanvas(fig) 
        
        fig, axs = self.axes(fig, grid, **sp_opts)
          
        if isinstance(axs,list):
            n_axs = len(axs)
        else:
            n_axs = 1
        
        if n_axs == 1:
            axs = self.custom_axis(axs, axis_opts)
            #axs.set_aspect(1.0)
        elif n_axs > 1:
            if isinstance(axis_opts,list):
                assert len(axis_opts) == n_axs, 'len(axis_opts) ({}) must be equal to number of axes ({})'.format(len(axis_opts), n_axs)
            elif isinstance(axis_opts, dict):
                axis_opts = [axis_opts for _ in range(n_axs)]
            else:
                pass
            
            axs = [self.custom_axis(_ax, _opts) 
                    for _ax,_opts in zip(axs,axis_opts)]

            #for _ax in axs: 
            #    _ax.set_aspect(1.0)
            #    _ax.set(adjustable='box-forced', aspect='equal')

        return canvas, fig, axs

    def plot(self, x, y=None, subplots_options=None, axis_options=None, 
             plot_options=None, plot=True, box=True, *args, **kwargs):
        """ Plot data on a single figure.
        
        Parameters
        ----------
        x : array_like or list
            When `x` is array_like and `y` is None, x must be a Nx2 numpy 
            array containing the x- and y-coordinates of the data to plot.
            ...
        plot_opts : dict
            Options passed to the method `plot` to deal with fancy plot 
            options. For example, plot_opts = {'color':'b', 'linewidth':2}. 
            
        """
        # Make copies, avoiding any modification of the original dic with the
        # method update.        
        if subplots_options is None: 
            subplots_opts = {}
        else:
            subplots_opts = deepcopy(subplots_options)
            
        if axis_options is None: 
            axis_opts = {}
        else:
            axis_opts = deepcopy(axis_options)
            
        if plot_options is None: 
            plot_opts = {}
        else:
            plot_opts = deepcopy(plot_options)    

        # Deal with multiplot options
        plot_opts_default = {'color':'k',
                             'linewidth':1}
        if plot_opts is None:
            plot_opts = plot_opts_default
            multiplotopts = False
        elif isinstance(plot_opts,list):
            plot_opts = [HandlingDict.merge_dicts(plot_opts_default,_opts) for _opts in plot_opts]
            multiplotopts = True
        else: 
            plot_opts = HandlingDict.merge_dicts(plot_opts_default, plot_opts)
            multiplotopts = False
            
           
        # Define the x- and y-limits      
        xlim, ylim = Data().xylimits(x, y)

        if axis_opts.get('set_xscale',False) is 'log' and min(xlim)<=0:
            print 'WARNING: you cannot use logarithmic xscale with negative values: `set_xscale` has been changed to `linear`.' 
            axis_opts.update({'set_xscale':'linear'})

        if axis_opts.get('set_yscale',False) is 'log' and min(ylim)<=0:
            print 'WARNING: you cannot use logarithmic yscale with negative values: `set_yscale` has been changed to `linear`.' 
            axis_opts.update({'set_yscale':'linear'})            
                   
        # Set the default axis limits if not specified in axis_opts
        if not axis_opts.has_key('set_xlim'):
            axis_opts.update({'set_xlim': xlim})

        if not axis_opts.has_key('set_ylim'):
            axis_opts.update({'set_ylim': ylim}) 
             
        
        # Modify the default tick labels for axis 'log' scales, without 
        # overriding the user's choice
        if (axis_opts.get('set_xscale',False) is 'log' and 
            not axis_opts.has_key('set_xticks')):
            xticklabels = self.set_ticklabels(xlim[0], xlim[1], axis='x',
                                              scale='log', decimals=1)
            axis_opts.update(xticklabels)
             
        if (axis_opts.get('set_yscale',False) is 'log' and 
            not axis_opts.has_key('set_yticks')):
            yticklabels = self.set_ticklabels(ylim[0], ylim[1], axis='y',
                                              scale='log', decimals=1)
            axis_opts.update(yticklabels) 
            
        # Build the figure    
        canvas, fig, ax1 = self.build_figure((1,1), subplots_opts, axis_opts)
        
        # Plot the data
        if isinstance(x,list) and y is None:
            if multiplotopts:
                assert len(plot_opts) == len(x), 'len(plot_opts) ({}) must be equal to len(x) ({})'.format(len(plot_opts), len(x))
            else:
                plot_opts = [plot_opts for _ in range(len(x))]
                
            for _x,_opts in zip(x,plot_opts): ax1.plot(_x[:,0],_x[:,1],**_opts)

        elif not isinstance(x,list) and y is None:
            ax1.plot(x[:,0], x[:,1], **plot_opts) 
            
        elif not isinstance(x,list) and y is not None:
            if isinstance(y,list):
                if multiplotopts:
                    assert len(plot_opts) == len(y), 'len(plot_opts) ({}) must be equal to len(y) ({})'.format(len(plot_opts), len(y))
                else:
                    plot_opts = [plot_opts for _ in range(len(y))]
                    
                for _y,_opts in zip(y,plot_opts): ax1.plot(x, _y, **_opts)
            else:
                ax1.plot(x, y, **plot_opts) 
        else:
            pass
        
        if plot:
            return canvas.figure
        else:
            return canvas, fig, ax1
    
#    def render(self, canvas, form='plot', **kwargs):
#        """
#        """
#        if form is 'plot':
#            return canvas.figure
#        elif form is 'save':
#            if not len(kwargs): kwargs = {'filename':'foo.png'}
#            return canvas.print_figure(**kwargs)
#        else:
#            return None
    
#    def save(self, x, filename='foo.png', subplots_opts={}, axis_opts={}, 
#             plot_opts={}, *args, **kwargs):
#        """
#        """
#        canvas, fig, ax1 = self.build_figure(x, subplots_opts, 
#                                             axis_opts, plot_opts)
#        new_kwargs = HandlingDict.merge_dicts(kwargs,{'filename':filename})
#        return self.render(canvas, form='save', **new_kwargs)
        
    
    
# https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window   


### 2 subplots with a modified aspect ratio
#zcanvas, zfig, zax = pySPT.tools.graphics.Graphics().build_figure((2,1))
#angle = np.linspace(0.,2.*np.pi, 100)
#zax[0].plot(np.cos(angle),np.sin(angle),'b')
#zax[1].plot(np.cos(angle),np.sin(angle),'r')
#zax[1].set_aspect(0.1)
#zfig.subplots_adjust(hspace = -0.2)
#zcanvas.figure 
    








