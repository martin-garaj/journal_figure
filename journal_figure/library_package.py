#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 17:28:20 2021

@author: Martin Garaj
"""

#%% ---------------------------------------------------------------------------
#   ----------------------------------IMPORTS----------------------------------
#   ---------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator, FixedLocator)

import os.path

#%% ---------------------------------------------------------------------------
#   ---------------------------------FUNCTIONS---------------------------------
#   ---------------------------------------------------------------------------

# copied from: https://stackoverflow.com/questions/4187300/how-do-i-use-a-relative-path-in-a-python-module-when-the-cwd-has-changed
def package_path(*paths, package_directory=os.path.dirname(os.path.abspath(__file__))):
    return os.path.join(package_directory, *paths)


#%% general font settings
def set_style(style='pretty_style_v1', apply_to='fonts'):
    """
    Set pre-defined style to particular element.
    
    Parameters
    ----------
    style : <string>, optional
        Name of the style to be set.
    apply_to: <list<string>>, optional
        List of objects to apply the style to. Currently defined styles for 'figure', 'fonts', 'grid', 'ticks', 'legend'.
        
    Returns
    -------
    None.
    """
    _fuctionName = 'set_style'
    
    if(isinstance(apply_to,list)):
        for entry in apply_to:
            # path = './stylelib/'+entry+'/'+style+'.mplstyle'
            path = package_path('stylelib/'+entry, style+'.mplstyle')
            if( os.path.isfile(path) ):
                plt.style.use(path)
            else:
                raise RuntimeError(_fuctionName+': the file at the end of the path : '+path+', doesn''t exist.')
    else:
        raise ValueError(_fuctionName+': the "apply_to" parameter needs to be a <list> of <strings>.')

#%% detail_axes
def pretty_detail_axis(main_ax, detail_ax, main_limits, detail_limits, detail_pos, 
                       connections=[{'connector_detail':'NE', 'connector_detail_ax':'NE'}, {'connector_detail':'SW', 'connector_detail_ax':'SW'}], 
                       line_setting = {'linestyle':'-', 'color':'black', 'linewidth':0.5, 'alpha':1.0}):
    """Set the position of the detail axis "detail_ax" within the main axis "main_ax",
    create the focussed area and draw the connecting lines among edges.

    Parameters
    ----------
    main_ax: <axis handle>
        Handle of the main axis.
    detail_ax: <axis handle>
        Handle of the detail axis.
    main_limits: [[x_min, x_max], [y_min, y_max]]
        Limits of the main axis, such as required by xlim() abd ylim() functions.
    detail_limits: [[x_min, x_max], [y_min, y_max]]
        Limits of the detail axis, such as required by xlim() abd ylim() functions.
    detail_pos: [[x_left, x_right], [y_bottom, y_top]]
        Position of the detail_ax within the main_ax defined by 2 points in 
        the same manner as limits.
    connections: <list(<dict>)>
        <dict>: 'connector_detail_ax': 'NE'/'NW'/'SE'/'SW'
                'connector_detail': 'NE'/'NW'/'SE'/'SW'
                    
    Returns
    ----------
    lines: <list(<line handles>)>
        A list of handles for connector and detail lines.
    """
    # output dictionary
    lines = {}
    
    # set limits
    main_ax.set_xlim(main_limits[0])
    main_ax.set_ylim(main_limits[1])
    
    # set position of detail_ax, calculate the relative position within main_ax
    main_ax_width  = main_limits[0][1] - main_limits[0][0]
    main_ax_height = main_limits[1][1] - main_limits[1][0]
    # position of detail_ax within main_ax
    detail_ax_x0 = (detail_pos[0][0] - main_limits[0][0]) / main_ax_width
    detail_ax_y0 = (detail_pos[1][0] - main_limits[1][0]) / main_ax_height
    detail_ax_width  = (detail_pos[0][1] - detail_pos[0][0]) / main_ax_width
    detail_ax_height = (detail_pos[1][1] - detail_pos[1][0]) / main_ax_height
    # BUT since main_ax has RELATIVE position in regards to the figure, 
    # rescale the position of detail_ax accordingly
    main_ax_pos_rel = main_ax.get_position()
    detail_ax_x0_rel = (detail_ax_x0 * main_ax_pos_rel.width) + main_ax_pos_rel.x0
    detail_ax_y0_rel = (detail_ax_y0 * main_ax_pos_rel.height) + main_ax_pos_rel.y0
    detail_ax_width_rel = detail_ax_width * main_ax_pos_rel.width
    detail_ax_height_rel = detail_ax_height * main_ax_pos_rel.height
    # place the detail_ax within the main_ax
    detail_ax.set_position([detail_ax_x0_rel, detail_ax_y0_rel, detail_ax_width_rel, detail_ax_height_rel], which='both')

    # add rectangle detail
    detail_limit_x0 = detail_limits[0][0]
    detail_limit_y0 = detail_limits[1][0]
    detail_limit_x1 = detail_limits[0][1]
    detail_limit_y1 = detail_limits[1][1]

    rect_bottom = main_ax.plot([detail_limit_x0, detail_limit_x1], [detail_limit_y0,detail_limit_y0], 
                             color=line_setting['color'], 
                             alpha=line_setting['alpha'], 
                             linestyle=line_setting['linestyle'], 
                             linewidth=line_setting['linewidth'])
    lines['rect_bottom'] = rect_bottom
    rect_right  = main_ax.plot([detail_limit_x1, detail_limit_x1], [detail_limit_y0,detail_limit_y1], 
                             color=line_setting['color'], 
                             alpha=line_setting['alpha'], 
                             linestyle=line_setting['linestyle'], 
                             linewidth=line_setting['linewidth'])
    lines['rect_right'] = rect_right
    rect_top    = main_ax.plot([detail_limit_x1, detail_limit_x0], [detail_limit_y1,detail_limit_y1], 
                             color=line_setting['color'], 
                             alpha=line_setting['alpha'], 
                             linestyle=line_setting['linestyle'], 
                             linewidth=line_setting['linewidth'])
    lines['rect_top'] = rect_top
    rect_left   = main_ax.plot([detail_limit_x0, detail_limit_x0], [detail_limit_y1,detail_limit_y0], 
                             color=line_setting['color'], 
                             alpha=line_setting['alpha'], 
                             linestyle=line_setting['linestyle'], 
                             linewidth=line_setting['linewidth'])
    lines['rect_left'] = rect_left
    
    # add connectors
    detail_pos_x0 = detail_pos[0][0]
    detail_pos_y0 = detail_pos[1][0]
    detail_pos_x1 = detail_pos[0][1]
    detail_pos_y1 = detail_pos[1][1]
    
    for idxConnector, connection in enumerate(connections):
        # select corner of the detail
        if('E' in connection['connector_detail']):
            connction_x0 = detail_limit_x0
        else:
            connction_x0 = detail_limit_x1
        if('N' in connection['connector_detail']):
            connction_y0 = detail_limit_y1
        else:
            connction_y0 = detail_limit_y0
        # select corner of the detail_ax
        if('E' in connection['connector_detail_ax']):
            connction_x1 = detail_pos_x0
        else:
            connction_x1 = detail_pos_x1
        if('N' in connection['connector_detail_ax']):
            connction_y1 = detail_pos_y1
        else:
            connction_y1 = detail_pos_y0
        # plot the connector
        connector   = main_ax.plot([connction_x0, connction_x1], [connction_y0, connction_y1], 
                                 clip_on=False,
                                 color=line_setting['color'], 
                                 alpha=line_setting['alpha'], 
                                 linestyle=line_setting['linestyle'], 
                                 linewidth=line_setting['linewidth'])
        lines['connector_'+str(idxConnector)] = connector

    # pretty detail_ax
    detail_ax.set_xlim(detail_limits[0])
    detail_ax.set_ylim(detail_limits[1])
    detail_ax.grid('on')
    
    for spine in ['bottom', 'left', 'top', 'right']:
        detail_ax.spines[spine].set_linestyle(line_setting['linestyle'])
        detail_ax.spines[spine].set_color(line_setting['color'])
        detail_ax.spines[spine].set_linewidth(line_setting['linewidth'])
        detail_ax.spines[spine].set_alpha(line_setting['alpha']) 
    
    return lines
    
#%% figure_size
def set_figure_size(wdth, height, ax=None):
    """
    Set the figure size in centimeters. 

    Parameters
    ----------
    w : <float>
        Width of the figure.
    h : <float>
        Height of the figure.
    ax : <handle axes>, optional
        Handle of the axes belonging to the figure to be resized. The default is None.

    Returns
    -------
    None.

    """
    
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(wdth)/(r-l)
    figh = float(height)/(t-b)
    ax.figure.set_size_inches(figw/2.54, figh/2.54)    

#%% legend
def pretty_legend(axes, label_source = [], position='best', label_order='default', title=''):
    """
    Control the legend content and position. 

    Parameters
    ----------
    axes : <handle axes>
        Handle of the axes.
    position : <string> / <list>/<tuple>/<numpy.ndarray>, optional
    Location of the legend within the axes. \n
        If <string> then following values are available: "best", "upper right", "upper left", "lower left", "lower right", "right", "center left", "center right", "lower center", "upper center", "center".\n
        If <list>/<tuple>/<numpy.ndarray> then relative position of legends origin in form of [x0, y0], where 0.0<x0,y0<1.0, but values <0.0 and >1.0 are allowed as well. The default is 'best'.
    label_order : <string> / <list<list>>/<2D numpy.ndarray>, optional
        Order of the labels within the legend. \n
        If <string> then following values are available: "default" and "reverse". \n
        If <list<list>>/<2D numpy.ndarray> then the labels are ordered as follows: \n
            label_order = [[ 1 , 2 , 3], \n
                           ['e', 0 , 4 ]] \n
        where the <int> are indexed position of labels and "e" is empty entry (e.g. when grouping of the labels into columns is required). \n
        The default is 'default'.
    title : <string>, optional
        The title of the legend.
    
    Raises
    ------
    ValueError
        Parameters "position" and "label_order" have multiple types, wrong type throws error.

    Returns
    -------
    Handle of the legend <handle legend>.

    """
    # get handles and labels from the legend
    if( not label_source):
        handles, labels = axes.get_legend_handles_labels()        
    else:
        handles = []
        labels = []
        for ax in label_source:
            _handles, _labels = ax.get_legend_handles_labels()
            handles.extend(_handles)
            labels.extend(_labels)
    
    if(label_order == 'reverse'):
        handles_ordered = handles.copy()
        labels_ordered  = labels.copy()
        handles_ordered.reverse()
        labels_ordered.reverse()
    elif(label_order == 'default'):
        handles_ordered = handles.copy()
        labels_ordered  = labels.copy()
    elif(type(label_order) == np.ndarray or type(label_order) == list):
        # assure the array is np.array
        label_order_np = np.array(label_order, dtype=object)
        # allocate empty lists
        handles_ordered = []
        labels_ordered = []
        # order the elements according to label_order_np
        for x in np.transpose(label_order_np):
            for y in x:
                if(isinstance(y, int)):
                    handles_ordered.append(handles[y])
                    labels_ordered.append(labels[y])
                else:
                    empty_entry = mpl.lines.Line2D([1, 0], [0, 1], linewidth=None, linestyle=None, color=None, alpha=0.0, marker=None, markersize=None, markeredgewidth=None, markeredgecolor=None, markerfacecolor=None, markerfacecoloralt='none')
                    handles_ordered.append(empty_entry)
                    labels_ordered.append('')
    else:
        raise ValueError('The "label_order" parameter is incorrect. Check help(pretty_legend)')
    
    # show the legend
    # axes.legend(handles, labels, ncol=2, bbox_to_anchor=(1.0, 1.0), loc=label_order_np.shape[1], borderaxespad=0.0)
    
    if(isinstance(position, str)):
        legend = axes.legend(handles_ordered, labels_ordered, ncol=label_order_np.shape[1], loc=position, title=title)
    elif(isinstance(position, list) or isinstance(position, np.ndarray) or isinstance(position, tuple)):
        # legend = axes.legend(handles_ordered, labels_ordered, ncol=label_order_np.shape[1], bbox_to_anchor=position, title=title)
        # assure the current figure is the figure containing axis
        plt.figure( axes.get_figure().number )
        # add legend
        legend = plt.legend(handles_ordered, labels_ordered, ncol=label_order_np.shape[1], loc='center', bbox_to_anchor=(position[0], position[1]), title=title, bbox_transform=plt.gcf().transFigure)
    else:
        raise ValueError('The "position" parameter is incorrect. Only <string> with values: "best", "upper right", "upper left", "lower left", "lower right", "right", "center left", "center right", "lower center", "upper center", "center" \n or relative position <list>/<tuple>/<numpy.ndarray> with [x0, y0]')

    return legend

#%% colorbar_axes
def add_colorbar(axes_colorbar, colormap, min_value, max_value, 
                 style_ticks={'number_of_ticks':11, 'ticks_start': 0.0, 'ticks_end': 1.0, 'labels':[]}, 
                 style_labels={'label_format':'{0:.3f}', 'label_align':'', 'rotation_angle':0.0, 'rotation_origin':'anchor', 'padding_x':0.0, 'padding_y':0.0},
                 style_colorbar={'orientation': 'vertical', 'xlabel':'', 'ylabel':'', 'title':'', 'boundaries':[] } ):

    norm = mpl.colors.Normalize(vmin=min_value,vmax=max_value)
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
    sm.set_array([])
    
    clb = plt.colorbar(sm,
                        ticks = [] if style_ticks['number_of_ticks'] <= 0 else np.linspace( style_ticks['ticks_start'], 
                                                                                              style_ticks['ticks_end'], 
                                                                                              style_ticks['number_of_ticks']),
                        boundaries = None if np.array(style_colorbar['boundaries']).size == 0 else style_colorbar['boundaries'], 
                        ax=axes_colorbar, fraction=1.0, pad=0.0)
    
    # set colorbar style
    clb.set_title  = style_colorbar['title']  
    clb.set_xlabel = style_colorbar['xlabel']
    clb.set_ylabel = style_colorbar['ylabel']
    
    # hide the orignal axis
    axes_colorbar.set_axis_off()
    
    if( style_colorbar['orientation'] == 'vertical' ):
        clb.ax.set_yticklabels(style_ticks['labels'])
    elif( style_colorbar['orientation'] == 'horizontal' ):
        clb.ax.set_xticklabels(style_ticks['labels'])
    else:
        raise ValueError('The only allowed values for "style_colorbar[\'orientation\']" are \'horizontal\' and \'vertical\'.')

    # force to draw
    axes.get_figure().canvas.draw()
    
    # loop through labels
    if( style_colorbar['orientation'] == 'horizontal' ):
        label_list = clb.ax.get_xticklabels(minor=False)
    elif( style_colorbar['orientation'] == 'vertical'):
        label_list = clb.ax.get_yticklabels(minor=False)
        
    for label_idx, label_object in enumerate(label_list):
        # horizontal alignment
        if('W' in style_labels['label_align'] or 'E' in style_labels['label_align']):
            label_object.set_horizontalalignment( 'left' if 'W' in style_labels['label_align'] else 'right' )
        else:
            label_object.set_horizontalalignment( 'center' )
        # vertical alignment
        if('N' in style_labels['label_align'] or 'S' in style_labels['label_align']):
            label_object.set_verticalalignment( 'top' if 'N' in style_labels['label_align'] else 'bottom' )
        else:
            label_object.set_verticalalignment( 'center' )
            
        # set rotation origin
        label_object.set_rotation_mode(style_labels['rotation_origin'])
        # rotate
        label_object.set_rotation(style_labels['rotation_angle'])
        
        # adjust position of labels
        label_object.set_position( (label_object.get_position()[0] + style_labels['padding_x'], label_object.get_position()[1] + style_labels['padding_y']) )

        # print( 'colorbar label['+str(label_idx)+'] = '+  str(label_object.get_text().replace('−','-')  ) ) 

        # set text
        if( style_ticks['labels'] == None ):
            # remove text
            label_object.set_text( '' )
        elif( not style_ticks['labels'] ):
            # apply formatting to the text
            if( any( x in style_labels['label_format'] for x in ['f', 'F', 'e', 'E', 'g', 'G'] ) ):
                # convert text to float
                label_object.set_text( style_labels['label_format'].format( float( label_object.get_text().replace('−','-') ) ) )
            elif( any( x in style_labels['label_format'] for x in ['f'] ) ):
                # convert text to integer
                label_object.set_text( style_labels['label_format'].format( int( label_object.get_text()).replace('−','-') ) )
            else:
                # no conversion
                label_object.set_text( style_labels['label_format'].format( label_object.get_text()) )
        else:
            label_object.set_text( style_labels['label_format'].format( style_ticks['labels'][label_idx] ) )

    # force to draw
    if( style_colorbar['orientation'] == 'horizontal' ):
        clb.ax.set_xticklabels(label_list)
    elif( style_colorbar['orientation'] == 'vertical' ):
        clb.ax.set_yticklabels(label_list)


#%% major_ticks
def set_major_ticks(axes, periodicity, along_axes='x', labels=[], which_axes='SW', 
                    style_labels={'label_format':'{0:.3f}', 'label_align':'', 'rotation_angle':0.0, 'rotation_origin':'anchor', 'padding_x':0.0, 'padding_y':0.0}):
    
    # sanity check
    if( not any( x in along_axes for x in ['x', 'y'] ) ):
        raise ValueError('The only allowed values for "along_axes" are \'x\' and \'y\'.')
    
    # force to draw
    axes.get_figure().canvas.draw()
    
    # get axes limits
    if(along_axes=='x'):
        limits = axes.get_xlim()
    elif(along_axes=='y'):
        limits = axes.get_ylim()
    
    # set position
    if(along_axes=='x'):
        if('N' in which_axes or 'S' in which_axes):
            axes.xaxis.set_ticks_position( 'top' if 'N' in which_axes else 'bottom' )
        else:
            axes.xaxis.set_ticks_position( 'bottom' )
    elif(along_axes=='y'):
        if('W' in which_axes or 'E' in which_axes):
            axes.yaxis.set_ticks_position( 'left' if 'W' in which_axes else 'right' )
        else:
            axes.yaxis.set_ticks_position( 'left' )    
    
    
    # set periodicity of the ticks
    # EXPLANATION: the combination of "MultipleLocator" and "FixedLocator" is used 
    # to prevent an error "FixedFormatter should only be used together with FixedLocator"
    if(along_axes=='x'):
        ticks = MultipleLocator(periodicity)
        axes.xaxis.set_major_locator(FixedLocator( ticks.tick_values(limits[0], limits[1]) ))
    elif(along_axes=='y'):
        ticks = MultipleLocator(periodicity)
        axes.yaxis.set_major_locator(FixedLocator( ticks.tick_values(limits[0], limits[1]) ))
    
    # force to draw
    axes.get_figure().canvas.draw()

    # loop through labels
    if(along_axes=='x'):
        label_list = axes.get_xticklabels(minor=False)
    elif(along_axes=='y'):
        label_list = axes.get_yticklabels(minor=False)
        
    for label_idx, label_object in enumerate(label_list):
        # horizontal alignment
        if('W' in style_labels['label_align'] or 'E' in style_labels['label_align']):
            label_object.set_horizontalalignment( 'left' if 'W' in style_labels['label_align'] else 'right' )
        else:
            label_object.set_horizontalalignment( 'center' )
        # vertical alignment
        if('N' in style_labels['label_align'] or 'S' in style_labels['label_align']):
            label_object.set_verticalalignment( 'top' if 'N' in style_labels['label_align'] else 'bottom' )
        else:
            label_object.set_verticalalignment( 'center' )
            
        # set rotation origin
        label_object.set_rotation_mode(style_labels['rotation_origin'])
        # rotate
        label_object.set_rotation(style_labels['rotation_angle'])
        
        # adjust position of labels
        label_object.set_position( (label_object.get_position()[0] + style_labels['padding_x'], label_object.get_position()[1] + style_labels['padding_y']) )

        # print( 'label['+str(label_idx)+'] = '+  str(label_object.get_text().replace('−','-')  ) ) 

        # set text
        if( labels == None ):
            # remove text
            label_object.set_text( '' )
        elif( not labels ):
            # apply formatting to the text
            if( any( x in style_labels['label_format'] for x in ['f', 'F', 'e', 'E', 'g', 'G'] ) ):
                # convert text to float
                label_object.set_text( style_labels['label_format'].format( float( label_object.get_text().replace('−','-') ) ) )
            elif( any( x in style_labels['label_format'] for x in ['f'] ) ):
                # convert text to integer
                label_object.set_text( style_labels['label_format'].format( int( label_object.get_text()).replace('−','-') ) )
            else:
                # no conversion
                label_object.set_text( style_labels['label_format'].format( label_object.get_text()) )
        else:
            label_object.set_text( style_labels['label_format'].format( labels[label_idx] ) )

    # force to draw
    if(along_axes=='x'):
        axes.set_xticklabels(label_list)
    elif(along_axes=='y'):
        axes.set_yticklabels(label_list)



#%%
# #%% 
# def prettify_minor_ticks(axes, multiple=1.0, width=1.0, length=3.0, color='black', direction='in'):
#     axes.xaxis.set_minor_locator(MultipleLocator(multiple))
#     axes.yaxis.set_minor_locator(MultipleLocator(multiple))
#     axes.tick_params(which='minor', width=width, length=length, color=color, direction=direction)
    
# #%%
# def prettify_major_ticks(axes, multiple=1.0, width=2.0, length=50.0, color='black', direction='out'):
#     axes.xaxis.set_major_locator(MultipleLocator(multiple))
#     axes.yaxis.set_major_locator(MultipleLocator(multiple))
#     # axes.tick_params(which='major', width=width, length=length, color=color, direction=direction)

# #%% latexify
# def _latexify(string, special_chars=['%', '$', '&', '"', "'"]):

#     latex_string = '$'
        
#     # prepend \ to any of the symbols '%', '$', '&'
#     for element in special_chars:
#         latex_string = string.replace(element, '\\'+element)
    
#     latex_string = latex_string + '$'
    
#     return latex_string

#%% ---------------------------------------------------------------------------
#   ----------------------------BACK COMPATIBILITY-----------------------------
#   ---------------------------------------------------------------------------









#%% ---------------------------------------------------------------------------
#   ----------------------------------TESTING----------------------------------
#   ---------------------------------------------------------------------------
if __name__ == "__main__":
    
    # number of data plotted
    data_resolution = 6    
    
    # pick colormap
    colormap= 'viridis'    
    
    # axes limits
    limX = [-0.5, 49.5]
    limY = [-1.1, 1.1]    
    
    # apply specific style
    set_style(style='pretty_style_v1', apply_to=['figure', 'fonts', 'grid', 'ticks', 'legend'])    
    
    ### close any previous figure
    plt.close('all')    
    ### create figure
    figure = plt.figure(1)
    ### add axes
    # main axes 1
    axes = figure.add_axes([0.10,0.54,0.70,0.40])
    axes.set_zorder(1)
    axes.grid('on')
    axes.set_xlim(limX)
    axes.set_ylim(limY)
    # main axes 2
    axes2 = figure.add_axes([0.10,0.07,0.70,0.40])
    axes2.set_zorder(-1)
    axes2.grid('on')
    axes2.set_xlim(limX)
    axes2.set_ylim(limY)
    # colorbar axes
    axes_colorbar = figure.add_axes([0.85,0.10,0.1,0.80])
    # axes for detail
    detail_ax = figure.add_axes([0.40,0.40,0.20,0.20])
    detail_ax.set_zorder(2)
    
    # get colormap function
    cmap = plt.get_cmap(colormap)
    
    # plot data
    for idx in range(0, data_resolution):
        axes.plot( ((idx+0.3)/data_resolution)*np.sin(np.linspace(0, 2 * np.pi)), color=cmap(idx/(data_resolution-1) ), label = 'Line '+str(idx+1))
        detail_ax.plot( ((idx+0.3)/data_resolution)*np.sin(np.linspace(0, 2 * np.pi)), color=cmap(idx/(data_resolution-1) ) )
        axes2.plot( ((idx+0.3)/data_resolution)*np.cos(np.linspace(0, 2 * np.pi)), color=cmap(idx/(data_resolution-1)), label = 'Line '+str(idx+1+data_resolution), linestyle=':')     
    
    # colorbar
    add_colorbar(axes_colorbar, cmap, 0.3, 1.3, 
                 style_ticks={'number_of_ticks':6, 'ticks_start': 0.4, 'ticks_end': 1.2, 'labels':['a', 'b', 'c', 'd', r'$\bf{e}$', r'$\frac{f}{g}$']},
                 style_labels={'label_format':'{0!s}', 'label_align':'W', 'rotation_angle':-45.0, 'rotation_origin':'anchor', 'padding_x':0.3, 'padding_y':0.0},
                 style_colorbar={'orientation': 'vertical', 'xlabel':'X', 'ylabel':'Y', 'title':'Title', 'boundaries':[]} )
    
    # set detail
    pretty_detail_axis(axes,
                       detail_ax,
                       main_limits=[limX, limY],
                       detail_limits=[[21.5, 27.5],[-0.35, 0.35]],
                       detail_pos=[[14, 29],[-2.3, -0.6]],
                       connections=[{'connector_detail':'NW', 'connector_detail_ax':'NW'}, {'connector_detail':'NE', 'connector_detail_ax':'NE'}],
                       line_setting = {'linestyle':'-', 'color':'black', 'linewidth':1.0, 'alpha':1.0} )
    
    set_major_ticks(axes,      5, along_axes='x', labels=[], which_axes='NW', 
                      style_labels={'label_format':'{0:.0f}', 'label_align':'SW', 'rotation_angle': 45.0, 'rotation_origin':'anchor', 'padding_x':0.0, 'padding_y': 0.01})
    set_major_ticks(axes2,     5, along_axes='x', labels=[], which_axes='SW', 
                      style_labels={'label_format':'{0:.0f}', 'label_align':'NW', 'rotation_angle':-45.0, 'rotation_origin':'anchor', 'padding_x':0.0, 'padding_y':-0.01})
    set_major_ticks(detail_ax, 2, along_axes='x', labels=[], which_axes='SW', 
                      style_labels={'label_format':'{0:.0f}', 'label_align':'NW', 'rotation_angle':-45.0, 'rotation_origin':'anchor', 'padding_x':0.0, 'padding_y':-0.01})
    
    set_major_ticks(axes,     0.4, along_axes='y', labels=[], which_axes='SW', 
                      style_labels={'label_format':'{0:.1f}', 'label_align':'NE', 'rotation_angle':-45.0, 'rotation_origin':'anchor', 'padding_x':-0.01, 'padding_y':0.01})
    set_major_ticks(detail_ax, 0.2, along_axes='y', labels=[], which_axes='SW', 
                      style_labels={'label_format':'{0:.1f}', 'label_align':'NE', 'rotation_angle':-45.0, 'rotation_origin':'anchor', 'padding_x':-0.01, 'padding_y':0.01})  
    set_major_ticks(axes2,    0.4, along_axes='y', labels=[], which_axes='SW', 
                      style_labels={'label_format':'{0:.1f}', 'label_align':'NE', 'rotation_angle':-45.0, 'rotation_origin':'anchor', 'padding_x':-0.01, 'padding_y':0.01})

    # add legend
    label_order = [[ 0 ,  2  , 'e' ],
                   [ 6  , 8  , 4 ],
                   [ 1  , 3  ,10 ],
                   [ 7 ,  9  , 'e' ]]
    legend = pretty_legend(axes, label_source=[axes, axes2], position=[0.66, 0.91], label_order=label_order, title='$Legend \; \Omega$')

    # set figure size
    set_figure_size(20,12,axes)

    plt.savefig('../graphics/pretty_style.pdf', bbox_inches='tight', dpi=200)
    plt.savefig('../graphics/pretty_style.png', bbox_inches='tight', dpi=200)