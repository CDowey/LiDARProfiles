# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:01:21 2019

@author: Colin.Dowey
"""


import rasterio as rio
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt



def eval_raster(x, y, dem_path):
    '''
    Function that returns the value of a single band raster for given x, y coordinates
    '''
    with rio.open(dem_path, 'r') as dem:
        arr = dem.read(1)  # read all raster values from first band into array
        row, col = dem.index(x, y)
        rast_value = arr[row, col]
        
    return rast_value

def eval_raster_list(x, y, dem_path):
    '''
    Function that returns the value of a single band raster for a list of x, y coordinates
    '''
    
    # Check that x and y are the same length
    if len(x) == len(y):
        pass

    else:
        raise Exception('List of X and Y are not the same length')
        return

    rast_values = []

    with rio.open(dem_path, 'r') as dem:
        arr = dem.read(1)  # read all raster values from first band into array

        for x_value, y_value in zip(x, y):
            
            row, col = dem.index(x_value, y_value)
            rast_value = arr[row, col]
            rast_values.append(rast_value)
    
    return rast_values


def frange(start, stop, step):
     '''
     Range that allows floats and always includes final value
     '''
     i = start
     
     while i < stop:
         yield i
         i += step
         
     yield stop


def Profile_to_dataframe(dem, profile, sampling_interval):
    '''
    Profile function that uses rasterio and geopandas to produce a dataframe of raster values for points along a line at a defined interval.
    
    '''
    
    df = pd.DataFrame(columns = ['LineID', 'X', 'Y', 'Distance', 'Z'])
    
    
    profile_lines = gpd.read_file(profile)

     
    for linestring in profile_lines['geometry']:

        length = linestring.length
        
        x = []
        y = []
        dist = []
    
        
        for currentdistance in frange(0, length, sampling_interval):
            point = linestring.interpolate(currentdistance)
            xp, yp = point.x, point.y
            x.append(xp)
            y.append(yp)
            dist.append(currentdistance)
        
        raster_values = eval_raster_list(x, y, dem)
            
        line_df = pd.DataFrame({'LineID': list(profile_lines[profile_lines['geometry'] == linestring].index)[0] , 'X': x, 'Y': y, 'Distance': dist, 'Z': raster_values})
        df = df.append(line_df)
    
    return df




def Plot_Profile(profile_dataframe, line_color, xmin, xmax, ymin, ymax, aspect, shade):
    """
    Function that uses matplotlib to plot a simple graph for a profile
    line_color most easily supplied as HTML color code ie '#D0D0D0'
    
    Parameters
    ----------
    profile_dataframe : pandas DataFrame
        A dataframe that contains distance and elevation information need to plot a profile.
        Field names and format follow the DataFrame returned from the Profile_to_dataframe function.
    line_color : string
        HTML string for line color in plot (ex. '#D0D0D0')
    xmax : int/float
        Maximum value shown on x-axis. For visualization the xmax adds 5 to this value.
    xmin : int/float
        Minimum value shown on x-axis
    ymax : int/float
        Maximum value shown on y-axis
    ymin : int/float
        Minimum value shown on y-axis
    aspect : int/float
        Aspect ratio of plot
    shade : boolean
        True = Area beneath plot is shaded
    """
    fig = plt.figure()
    
    plt.plot(profile_dataframe['Distance'], profile_dataframe['Z'], color = line_color)
    
    plt.xlabel('Distance (m)')
    plt.ylabel('Elevation (m)')
    
    plt.xlim(0, max(profile_dataframe['Distance']) + 5)
    plt.ylim(ymin, ymax)
    plt.tight_layout(pad=0)
    
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    plt.gca().set_aspect(aspect)
    
    # This is key to getting the x limits to work with a set aspect ratio!
    plt.gca().set_adjustable("box")
    
    # If statement for shading beneath profile line
    if shade:
        plt.gca().fill_between(profile_dataframe['Distance'], profile_dataframe['Z'], 0, facecolor= line_color, alpha = 0.1)
    
    return fig

