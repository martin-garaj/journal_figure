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
import matplotlib
import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

#%% ---------------------------------------------------------------------------
#   ---------------------------------FUNCTIONS---------------------------------
#   ---------------------------------------------------------------------------

#%% prettify detail axis within a main axis
def pretty_detail_axis(main_ax, main_limits, detail_ax, detail_limits, detail_pos, 
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
def set_font(text_usetex=False, mathtext_fontset='dejavuserif',font_size=12, font_family='serif'):
    """
    Parameters
    ----------
    text_usetex : bool, optional
        Decide whether the text processor if TEX or LATEX. The default is False, thus LATEX is used by default.
    mathtext_fontset : <string>, optional
        Fontset for mathmode, since most of the labels are in a form $<string>$. The default is 'dejavuserif'.
    font_size : <int>, optional
        The default font sizse. The default is 12.
    font_family : <string>, optional
        The default font family 'sans' or 'serif'. The default is 'serif'.

    Returns
    -------
    None.
    """
    plt.rcParams.update({'text.usetex': False, 'mathtext.fontset': 'dejavuserif'})
    plt.rcParams.update({'font.size': 12})
    plt.rcParams.update({'font.family': 'serif'})
    

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
    
def prettify_major_ticks(axes, multiple=1.0, width=2.0, length=50.0, color='black', direction='out'):
    axes.xaxis.set_major_locator(MultipleLocator(multiple))
    axes.yaxis.set_major_locator(MultipleLocator(multiple))
    # axes.tick_params(which='major', width=width, length=length, color=color, direction=direction)
    
    
#%% latexify
def _latexify(string, special_chars=['%', '$', '&', '"', "'"]):

    latex_string = '$'
        
    # prepend \ to any of the symbols '%', '$', '&'
    for element in special_chars:
        latex_string = string.replace(element, '\\'+element)
    
    latex_string = latex_string + '$'
    
    return latex_string

#%% testing
if __name__ == "__main__":
    
    plt.close('all')
    figure = plt.figure(1)
    axes = figure.add_axes([0.10,0.10,0.80,0.80])
    
    axes.plot( np.sin(np.linspace(0, 2 * np.pi)), 'r')
    
    set_ticks(  figure, 
                axes,   
                latexify=False,
                major_X_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'left', 'va':'top'}, 
                minor_X_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'left', 'va':'top'}, 
                major_Y_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'right', 'va':'center'},
                minor_Y_settings={'rotation': 0, 'rotation_mode':'anchor', 'ha':'right', 'va':'center'}  )
    prettify_minor_ticks(axes)
    prettify_major_ticks(axes)

