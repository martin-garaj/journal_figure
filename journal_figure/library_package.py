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
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

import os.path

#%% ---------------------------------------------------------------------------
#   ---------------------------------FUNCTIONS---------------------------------
#   ---------------------------------------------------------------------------

# copied from: https://stackoverflow.com/questions/4187300/how-do-i-use-a-relative-path-in-a-python-module-when-the-cwd-has-changed
def package_path(*paths, package_directory=os.path.dirname(os.path.abspath(__file__))):
    return os.path.join(package_directory, *paths)

#%% prettify detail axis within a main axis
def pretty_detail_axis(main_ax, detail_ax, main_limits, detail_limits, detail_pos, 
                       connections=[{'connector_detail':'NE', 'connector_detail_ax':'NE'}, {'connector_detail':'SW', 'connector_detail_ax':'SW'}], 
                       line_setting = {'linestyle':'-', 'color':'black', 'linewidth':0.5, 'alpha':1.0}):
    """Set the position of the detail axis "detail_ax" within the main axis "main_ax",
    create the focussed area and draw the connecting lines among edges.

    Parameters
    ----------
    main_ax: <axis handle>
        Handle of the main axis.
    main_limits: [[x_min, x_max], [y_min, y_max]]
        Limits of the main axis, such as required by xlim() abd ylim() functions.
    detail_ax: <axis handle>
        Handle of the detail axis.
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
            path = package_path(apply_to, style+'.mplstyle')
            if( os.path.isfile(path) ):
                plt.style.use(path)
            else:
                raise RuntimeError(_fuctionName+': the file at the end of the path : '+path+', doesn''t exist.')
    else:
        raise ValueError(_fuctionName+': the "apply_to" parameter needs to be a <list> of <strings>.')

#%% set ticks 
def set_ticks(figure, axes, minor_ticks=True, minor_labels=False, major_ticks=True, major_labels=True, latexify=True, 
              minor_X_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'center', 'va':'top'}, 
              minor_Y_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'center', 'va':'center'}, 
              major_X_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'center', 'va':'top'}, 
              major_Y_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'center', 'va':'center'}):
    """
    Parameters
    ----------
    axes : <handle axes>
        Handle of the axes.
    minor_ticks : bool, optional
        Add minor ticks. The default is True.
    minor_labels : bool, optional
        Add minor labels. The default is False.
    major_ticks : bool, optional
        Add major ticks. The default is True.
    major_labels : bool, optional
        Add major labels. The default is True.
    minor_X_settings : <dict>, optional
        'rotation' : rotation of the ticks in degrees. The default is 0.
        'rotation_mode' : 'default' or 'anchor'. The default is 'anchor'.
        'ha' : Horizontal alignment of ticks: 'left', 'center', 'right'. The default is 'center'.
        'va': Vertical alignment of ticks: 'bottom', 'baseline', 'center', 'top'. The default is 'top'.
        https://matplotlib.org/stable/gallery/text_labels_and_annotations/demo_text_rotation_mode.html
    minor_Y_settings : <dict>, optional
        'rotation' : rotation of the ticks in degrees. The default is 0.
        'rotation_mode' : 'default' or 'anchor'. The default is 'anchor'.
        'ha' : Horizontal alignment of ticks: 'left', 'center', 'right'. The default is 'center'.
        'va': Vertical alignment of ticks: 'bottom', 'baseline', 'center', 'top'. The default is 'right'.
        https://matplotlib.org/stable/gallery/text_labels_and_annotations/demo_text_rotation_mode.html
    major_X_settings : <dict>, optional
        'rotation' : rotation of the ticks in degrees. The default is 0.
        'rotation_mode' : 'default' or 'anchor'. The default is 'anchor'.
        'ha' : Horizontal alignment of ticks: 'left', 'center', 'right'. The default is 'center'.
        'va': Vertical alignment of ticks: 'bottom', 'baseline', 'center', 'top'. The default is 'top'.
        https://matplotlib.org/stable/gallery/text_labels_and_annotations/demo_text_rotation_mode.html
    major_Y_settings : <dict>, optional
        'rotation' : rotation of the ticks in degrees. The default is 0.
        'rotation_mode' : 'default' or 'anchor'. The default is 'anchor'.
        'ha' : Horizontal alignment of ticks: 'left', 'center', 'right'. The default is 'center'.
        'va': Vertical alignment of ticks: 'bottom', 'baseline', 'center', 'top'. The default is 'right'.
        https://matplotlib.org/stable/gallery/text_labels_and_annotations/demo_text_rotation_mode.html

    Returns
    -------
    None.

    """
    # assure all elements in figure are available
    figure.canvas.draw()
    
    # major x labels
    x_labels_latex = []
    if(major_labels):
        x_labels = axes.get_xticklabels(minor=False)
        for x_label in x_labels:
            x_label.set_rotation(major_X_settings['rotation'])
            x_label.set_horizontalalignment(major_X_settings['ha'])
            x_label.set_verticalalignment(major_X_settings['va'])
            x_label.set_rotation_mode(major_X_settings['rotation_mode'])
            if(latexify):
                x_labels_latex.append( _latexify(x_label.get_text()) )
            else:
                x_labels_latex.append( x_label.get_text() ) 
        # set positions
        x_positions = []
        x_labels = axes.get_xticklabels(minor=False)
        for x_label in x_labels:
            x_positions.append( x_label.get_position()[0] )
        axes.set_xticks( x_positions )
        # set labels
        axes.set_xticklabels(x_labels_latex, minor=False)
    # minor x labels
    x_labels_latex = []
    if(minor_labels):
        x_labels = axes.get_xticklabels(minor=True)
        for x_label in x_labels:
            x_label.set_rotation(minor_X_settings['rotation'])
            x_label.set_horizontalalignment(minor_X_settings['ha'])
            x_label.set_verticalalignment(minor_X_settings['va'])
            x_label.set_rotation_mode(minor_X_settings['rotation_mode'])
            if(latexify):
                x_labels_latex.append( _latexify(x_label.get_text()) )
            else:
                x_labels_latex.append( x_label.get_text() )
        # set positions
        x_positions = []
        x_labels = axes.get_xticklabels(minor=True)
        for x_label in x_labels:
            x_positions.append( x_label.get_position()[0] )
        axes.set_xticks( x_positions )
        # set labels
        axes.set_xticklabels(x_labels_latex, minor=True)
    # major y labels
    y_labels_latex = []
    if(major_labels):
        y_labels = axes.get_yticklabels(minor=False)
        for y_label in y_labels:
            y_label.set_rotation(major_Y_settings['rotation'])
            y_label.set_horizontalalignment(major_Y_settings['ha'])
            y_label.set_verticalalignment(major_Y_settings['va'])
            y_label.set_rotation_mode(major_Y_settings['rotation_mode'])
            if(latexify):
                y_labels_latex.append( _latexify(y_label.get_text()) )
            else:
                y_labels_latex.append( y_label.get_text() )
        # set positions
        y_positions = []
        y_labels = axes.get_yticklabels(minor=False)
        for y_label in y_labels:
            y_positions.append( y_label.get_position()[1] )
        axes.set_yticks( y_positions )
        # set labels
        axes.set_yticklabels(y_labels_latex, minor=False)
    # minor y labels
    y_labels_latex = []
    if(minor_labels):
        y_labels = axes.get_yticklabels(minor=True)
        for y_label in y_labels:
            y_label.set_rotation(minor_Y_settings['rotation'])
            y_label.set_horizontalalignment(minor_Y_settings['ha'])
            y_label.set_verticalalignment(minor_Y_settings['va'])
            y_label.set_rotation_mode(minor_Y_settings['rotation_mode'])
            if(latexify):
                y_labels_latex.append( _latexify(y_label.get_text()) )
            else:
                y_labels_latex.append( y_label.get_text() )
        # set positions
        y_positions = []
        y_labels = axes.get_yticklabels(minor=True)
        for y_label in y_labels:
            y_positions.append( y_label.get_position()[1] )
        axes.set_yticks( y_positions )
        # set labels
        axes.set_yticklabels(y_labels_latex, minor=True)
        
    # if(not latexify):
    #     ax.xaxis.set_major_formatter('{x:.0f}')          
    # # set looks of ticks
    # if(minor_ticks):
        
    # # set the ticks
    # axes.set_xticklabels(x_labels_latex)
    # axes.set_yticklabels(y_labels_latex)
    
#%% 
def prettify_minor_ticks(axes, multiple=1.0, width=1.0, length=3.0, color='black', direction='in'):
    axes.xaxis.set_minor_locator(MultipleLocator(multiple))
    axes.yaxis.set_minor_locator(MultipleLocator(multiple))
    axes.tick_params(which='minor', width=width, length=length, color=color, direction=direction)
    
#%%
def prettify_major_ticks(axes, multiple=1.0, width=2.0, length=50.0, color='black', direction='out'):
    axes.xaxis.set_major_locator(MultipleLocator(multiple))
    axes.yaxis.set_major_locator(MultipleLocator(multiple))
    # axes.tick_params(which='major', width=width, length=length, color=color, direction=direction)
    
#%% 
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
    
    
#%% latexify
def _latexify(string, special_chars=['%', '$', '&', '"', "'"]):

    latex_string = '$'
        
    # prepend \ to any of the symbols '%', '$', '&'
    for element in special_chars:
        latex_string = string.replace(element, '\\'+element)
    
    latex_string = latex_string + '$'
    
    return latex_string

#%% pretty_legend
def pretty_legend(axes, position='best', label_order='default', title=''):
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
    handles, labels = axes.get_legend_handles_labels()
    
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
        legend = axes.legend(handles_ordered, labels_ordered, ncol=label_order_np.shape[1], bbox_to_anchor=position, title=title)
    else:
        raise ValueError('The "position" parameter is incorrect. Only <string> with values: "best", "upper right", "upper left", "lower left", "lower right", "right", "center left", "center right", "lower center", "upper center", "center" \n or relative position <list>/<tuple>/<numpy.ndarray> with [x0, y0]')

    return legend
#%% ---------------------------------------------------------------------------
#   ----------------------------------TESTING----------------------------------
#   ---------------------------------------------------------------------------
if __name__ == "__main__":
    # close any previous figure
    plt.close('all')
    
    # create figure
    figure = plt.figure(1)
    # add main axes
    axes = figure.add_axes([0.10,0.10,0.80,0.80])
    # add axis for detail
    detail_ax = figure.add_axes([0.40,0.40,0.20,0.20])
    ## axes limits
    limX = [-0.5, 49.5]
    limY = [-1.1, 1.1]
    # pick colormap
    colormap= 'viridis'
    # number of data plotted
    resolution = 5
    
    # apply specific style
    set_style(style='pretty_style_v1', apply_to=['figure', 'fonts', 'grid', 'ticks', 'legend'])
    
    # get colormap function
    cmap = plt.get_cmap(colormap,resolution)
    
    # plot data
    for idx in range(0, resolution):
        axes.plot( ((idx+0.3)/resolution)*np.sin(np.linspace(0, 2 * np.pi)), color=cmap(idx), label = 'Line '+str(idx+1))
        detail_ax.plot( ((idx+0.3)/resolution)*np.sin(np.linspace(0, 2 * np.pi)), color=cmap(idx))
    
    # set ticks
    # set_ticks(  figure, 
    #             axes,   
    #             latexify=False,
    #             major_X_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'left', 'va':'top'}, 
    #             minor_X_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'left', 'va':'top'}, 
    #             major_Y_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'right', 'va':'center'},
    #             minor_Y_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'right', 'va':'center'}  )
    # prettify_minor_ticks(axes)
    # prettify_major_ticks(axes)

    # set ticks position
    axes.xaxis.set_major_locator(MultipleLocator(10))
    axes.yaxis.set_major_locator(MultipleLocator(0.5))
    axes.xaxis.set_minor_locator(MultipleLocator(1))
    axes.yaxis.set_minor_locator(MultipleLocator(0.05))
    axes.xaxis.set_ticks_position('both')
    axes.yaxis.set_ticks_position('both')
    
    detail_ax.xaxis.set_major_locator(MultipleLocator(1))
    detail_ax.yaxis.set_major_locator(MultipleLocator(0.1))
    detail_ax.xaxis.set_minor_locator(MultipleLocator(1))
    detail_ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    detail_ax.xaxis.set_ticks_position('both')
    detail_ax.yaxis.set_ticks_position('both')
    
    # set ticks format
    axes.xaxis.set_major_formatter('${x:.0f}$')
    axes.yaxis.set_major_formatter('${x:.1f}$')

    # set detail
    pretty_detail_axis(axes,
                       detail_ax,
                       main_limits=[limX, limY],
                       detail_limits=[[21.5, 27.5],[-0.35, 0.35]],
                       detail_pos=[[5, 20],[-0.9, -0.1]],
                       connections=[{'connector_detail':'NE', 'connector_detail_ax':'NE'}, {'connector_detail':'SW', 'connector_detail_ax':'SW'}],
                       line_setting = {'linestyle':'-', 'color':'black', 'linewidth':1.0, 'alpha':1.0} )
    
    # enable grid
    axes.grid('on')
    
    # set figure size
    set_figure_size(20,12,axes)

    # add legend
    label_order = [[ 1 , 2 , 3],
                    ['e', 0 , 4 ]]
    pretty_legend(axes, position=[1.03, 1.05], label_order=label_order, title='$Legend \; \Omega$')
