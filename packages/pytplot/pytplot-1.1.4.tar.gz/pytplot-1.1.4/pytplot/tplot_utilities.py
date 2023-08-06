# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import os
import datetime
import pickle
import math
import pandas as pd
import numpy as np
import pytz
from _collections import OrderedDict
from . import data_quants

def compare_versions():
    #import libraries
    import requests

    #access complete list of revision numbers on PyPI 
    pytplot_url = "https://pypi.python.org/pypi/pytplot/json"
    try:
        pt_pypi_vn = sorted(requests.get(pytplot_url).json()['releases'])
    except:
        return
    
    #find PyPI version number
    pt_pypi_vn = pt_pypi_vn[-1]
    pr1 = pt_pypi_vn
    pt_pypi_vn = pt_pypi_vn.split(".")
    #convert to integer array for comparison
    pt_pypi_vn = [int(i) for i in pt_pypi_vn]
    
    #find current directory out of which code is executing
    dir_path = os.path.dirname(os.path.realpath(__file__))
    version_path = dir_path + '/version.txt'
    #open version.txt in current directory and read
    with open(version_path) as f:
        cur_vn = f.readline()
    cur_vn = "".join(cur_vn)
    pr2 = cur_vn
    cur_vn = cur_vn.split(".")
    #convert to integer array for comparison
    cur_vn = [int(i) for i in cur_vn]

    #for each item in version number array [X.Y.Z]
    for i in range(len(cur_vn)):
        #if current item > PyPI item (hypothetical), break, latest version is running
        if cur_vn[i] > pt_pypi_vn[i]:
            old_flag = 0
            break
        #if current item = PyPI item, continue to check next item
        elif cur_vn[i] == pt_pypi_vn[i]:
            old_flag = 0
            continue
        #if current item < PyPI item, indicative of old version, throw flag to initiate warning
        else:
            old_flag = 1
            break

    #if not running latest version, throw warning
    if old_flag == 1:
        print("PyPI PyTplot Version")
        print(pr1)
        print("Your PyTplot Version in " + dir_path)
        print(pr2)
        print("")
        print('****************************** WARNING! ******************************')
        print('*                                                                    *')
        print('*          You are running an outdated version of PyTplot.           *')
        print('*              Sync your module for the latest updates.              *')
        print('*                                                                    *')
        print('****************************** WARNING! ******************************')
    return 
        
def option_usage():
    print("options 'tplot variable name' 'plot option' value[s]")
    return

def set_options(option, value, old_yaxis_opt, old_zaxis_opt, old_line_opt, old_extras):
    new_yaxis_opt = old_yaxis_opt
    new_zaxis_opt = old_zaxis_opt
    new_line_opt = old_line_opt
    new_extras = old_extras
    
    if option == 'color':
        if isinstance(value, list):
            new_extras['line_color'] = value
        else:
            new_extras['line_color'] = [value]
    
    if option == 'colormap':
        if isinstance(value, list):
            new_extras['colormap'] = value
        else:
            new_extras['colormap'] = [value]
    
    if option == 'spec':
        new_extras['spec'] = value
    
    if option == 'alt':
        new_extras['alt'] = value

    if option == 'map':
        new_extras['map'] = value
    
    elif option == 'ylog':
        if value == 1:
            new_yaxis_opt['y_axis_type'] = 'log'
        if value == 0:
            new_yaxis_opt['y_axis_type'] = 'linear'
    
    elif option == 'legend_names':
        new_yaxis_opt['legend_names'] = value
    
    elif option == 'zlog':
        if value == 1:
            new_zaxis_opt['z_axis_type'] = 'log'
        if value == 0:
            new_zaxis_opt['z_axis_type'] = 'linear'
    
    # elif(option == 'ymajor'):  
    
    elif option == 'nodata':
        new_line_opt['visible'] = value
    
    elif option == 'line_style':
        to_be = []
        if value == 0 or value == 'solid_line':
            to_be = []
        elif value == 1 or value == 'dot':
            to_be = [2, 4]
        elif value == 2 or value == 'dash':
            to_be = [6]
        elif value == 3 or value == 'dash_dot':
            to_be = [6, 4, 2, 4]
        elif value == 4 or value == 'dash_dot_dot_dot':
            to_be = [6, 4, 2, 4, 2, 4, 2, 4]
        elif value == 5 or value == 'long_dash':
            to_be = [10]
            
        new_line_opt['line_dash'] = to_be
        
        if(value == 6 or value == 'none'):
            new_line_opt['visible'] = False
            
    elif option == 'name':
        new_line_opt['name'] = value
    
    elif option == "panel_size":
        if value > 1 or value <= 0:
            print("Invalid value. Should be (0, 1]")
            return
        new_extras['panel_size'] = value
    
    elif option =='basemap':
        new_extras['basemap'] = value
    
    elif option =='alpha':
        if value > 1 or value < 0:
            print("Invalid value. Should be [0, 1]")
            return
        new_extras['alpha'] = value
        
    elif option == 'thick':
        new_line_opt['line_width'] = value
    
    elif option == 'transparency':
        alpha_val = value/100
        new_line_opt['line_alpha'] = alpha_val
    
    elif option == ('yrange' or 'y_range'):
        new_yaxis_opt['y_range'] = [value[0], value[1]]
        
    elif option == ('zrange' or 'z_range'):
        new_zaxis_opt['z_range'] = [value[0], value[1]]
    
    elif option == 'ytitle':
        new_yaxis_opt['axis_label'] = value
    
    elif option == 'ztitle':
        new_zaxis_opt['axis_label'] = value
        
    '''       
    # value: NumberSpec(String, Dict(String, Either(String, Float)), Float)
    if(option == 'alpha'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_alpha = value
            i += 1
    # value: Enum('butt', 'round', 'square')
    elif(option == 'cap'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_cap = value
            i += 1
    # value: color value: string
    elif(option == 'color'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_color = value
            i += 1
    # value: DashPattern
    elif(option == 'dash'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_dash = value
            i += 1
    # value: Int
    elif(option == 'dash_offset'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_dash_offset = value
            i += 1
    # value: Enum('miter', 'round', 'bevel')
    elif(option == 'join'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_join = value
            i += 1
    # value: integer
    elif(option == 'thick'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_width = value
            i += 1
    # value: Bool
    elif(option == 'visible'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].visible = value
            i += 1
    # value: [integer, integer]
    elif(option == 'yrange'):
        fig.y_range = Range1d(value[0], value[1])
    # value: string
    elif(option == 'ytitle'):
        fig.yaxis.axis_label = value
    '''
    
    return (new_yaxis_opt, new_zaxis_opt, new_line_opt, new_extras)

def set_tplot_options(option, value, old_tplot_opt_glob):
    new_tplot_opt_glob = old_tplot_opt_glob
    
    if option == 'title':
        new_tplot_opt_glob['title_text'] = value
    
    elif option == 'title_size':
        str_size = str(value) + 'pt'
        new_tplot_opt_glob['title_size'] = str_size
        
    elif option == 'wsize':
        new_tplot_opt_glob['window_size'] = value
        
    elif option == 'title_align':
        new_tplot_opt_glob['title_align'] = value
        
    elif option == 'var_label':
        new_tplot_opt_glob['var_label'] = value
        
    elif option == 'alt_range':
        new_tplot_opt_glob['alt_range'] = value
    
    return (new_tplot_opt_glob)

def str_to_int(time_str):
    epoch_t = "1970-1-1 00:00:00"
    pattern = "%Y-%m-%d %H:%M:%S"
    epoch_t1 = datetime.datetime.strptime(epoch_t, pattern)
    time_str1 = datetime.datetime.strptime(time_str, pattern)
    time_int = int((time_str1-epoch_t1).total_seconds())
    return time_int

def int_to_str(time_int):
    if math.isnan(time_int):
        return "NaN"
    else:
        return datetime.datetime.fromtimestamp(int(round(time_int)), tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")

def return_bokeh_colormap(name):
    import matplotlib as mpl
    #mpl.use('tkagg')
    from matplotlib import cm
    
    if name=='yellow':
        map = [rgb_to_hex(tuple((np.array([1,1,0,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    elif name=='red':
        map = [rgb_to_hex(tuple((np.array([1,0,0,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    elif name=='blue':
        map = [rgb_to_hex(tuple((np.array([0,0,1,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    elif name=='green':
        map = [rgb_to_hex(tuple((np.array([0,1,0,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    elif name=='purple':
        map = [rgb_to_hex(tuple((np.array([1,0,1,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    elif name=='teal':
        map = [rgb_to_hex(tuple((np.array([0,1,1,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    else:
        cm = mpl.cm.get_cmap(name)
        map = [rgb_to_hex(tuple((np.array(cm(x))*255).astype(np.int))) for x in range(0,cm.N)]
        return map

def rgb_to_hex(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    return '#%02x%02x%02x' % (red, green, blue)

def get_heatmap_color(color_map, min_val, max_val, values, zscale = 'log'):
    colors = []
    if not isinstance(values, list):
        values = [values]
    for value in values:
        if np.isfinite(value):
            if value > max_val:
                value = max_val
            if value < min_val:
                colors.append("#%02x%02x%02x" % (255, 255, 255))
                continue
            if zscale=='log':
                log_min=np.log10(min_val)
                log_max=np.log10(max_val)
                log_val=np.log10(value)
                if np.isfinite(np.log10(value)):
                    cm_index = int((((log_val-log_min) / (log_max-log_min)) * (len(color_map)-1)))
                    colors.append(color_map[cm_index])
                else:
                    colors.append(("#%02x%02x%02x" % (255, 255, 255)))
            else:
                cm_index = int((((value-min_val) / (max_val-min_val)) * (len(color_map)-1)))
                colors.append(color_map[cm_index])
        else:
            colors.append("#%02x%02x%02x" % (255, 255, 255))
    return colors
    
def timebar_delete(t, varname=None, dim='height'):
    if varname is None:
        for name in tplot_common.data_quants:
            list_timebars = tplot_common.data_quants[name].time_bar
            elem_to_delete = []
            for elem in list_timebars:
                for num in t:
                    if (elem.location == num) and (elem.dimension == dim):
                        elem_to_delete.append(elem)
            for i in elem_to_delete:
                list_timebars.remove(i)
            tplot_common.data_quants[name].time_bar = list_timebars
    else:
        if not isinstance(varname, list):
            varname = [varname]
        for i in varname:
            if i not in tplot_common.data_quants.keys():
                print(str(i) + " is currently not in pytplot.")
                return
            list_timebars = tplot_common.data_quants[i].time_bar
            elem_to_delete = []
            for elem in list_timebars:
                for num in t:
                    if (elem.location == num) and (elem.dimension == dim):
                        elem_to_delete.append(elem)
            for j in elem_to_delete:
                list_timebars.remove(j)
            tplot_common.data_quants[i].time_bar = list_timebars
    return    

def return_lut(name):
    import matplotlib as mpl
    mpl.use('tkagg')
    from matplotlib import cm
    
    if name=='yellow':
        map = [(np.array([1,1,0,1])*255).astype(np.int) for x in range(0,256)]
        return map
    elif name=='red':
        map = [(np.array([1,0,0,1])*255).astype(np.int) for x in range(0,256)]
        return map
    elif name=='blue':
        map = [(np.array([0,0,1,1])*255).astype(np.int) for x in range(0,256)]
        return map
    elif name=='green':
        map = [(np.array([0,1,0,1])*255).astype(np.int) for x in range(0,256)]
        return map
    elif name=='purple':
        map = [(np.array([1,0,1,1])*255).astype(np.int) for x in range(0,256)]
        return map
    elif name=='teal':
        map = [(np.array([0,1,1,1])*255).astype(np.int) for x in range(0,256)]
        return map
    else:
        cm = mpl.cm.get_cmap(name)
        map = [(np.array(cm(x))*255).astype(np.int) for x in range(0,cm.N)]
        return map
