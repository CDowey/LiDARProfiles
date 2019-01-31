# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 08:57:38 2019

@author: Colin.Dowey
"""

# Script to create profiles from DEM using arcpy
# Plot profiles in matplotlib

import arcpy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms

def feature_class_to_pandas_data_frame(feature_class, field_list):
    """
    Load data into a Pandas Data Frame for subsequent analysis.
    :param feature_class: Input ArcGIS Feature Class.
    :param field_list: Fields for input.
    :return: Pandas DataFrame object.
    """
    return pd.DataFrame(
        arcpy.da.FeatureClassToNumPyArray(
            in_table=feature_class,
            field_names=field_list,
            skip_nulls=False,
            null_value=-99999
        )
    )
        

def Create_Profile(Line, DEM):
    """
    Creates a pandas DataFrame of the attribute table that results from the ArcGIS Stack Profile tool.
    Useful for further analyzing or plotting profiles.
    If the line input contains multiple lines these can be filtered by the LINE_ID field
    """
    arcpy.Delete_management('in_memory\profile')
    
    arcpy.StackProfile_3d(Line, DEM, 'in_memory\profile')
    
    field_names = [f.name for f in arcpy.ListFields('in_memory\profile')]
    
    df = feature_class_to_pandas_data_frame('in_memory\profile', field_names)
    
    return df


def Plot_Profile(Dataframe_x_z, line_color, xmax, xmin, ymax, ymin, aspect, shade_boolean):
    """
    Function that uses matplotlib to plot a simple graph for a profile
    line_color most easily supplied as HTML color code ie '#D0D0D0'
    """
    fig = plt.figure()
    
    plt.plot(Dataframe_x_z['FIRST_DIST'], Dataframe_x_z['FIRST_Z'], color = line_color)
    
    plt.xlabel('Distance (m)')
    plt.ylabel('Elevation (m)')
    
#    plt.grid(True, color  = '#D0D0D0', linestyle = '--')
    
    plt.xlim(0, max(Dataframe_x_z['FIRST_DIST']) + 5)
    plt.ylim(ymin, ymax)
    plt.tight_layout(pad=0)
    
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    plt.gca().set_aspect(aspect)
    
    # This is key to getting the x limits to work with a set aspect ratio!
    plt.gca().set_adjustable("box")
    
    # Get rid of upper and right side bounding box
    
    if shade_boolean:
        plt.gca().fill_between(Dataframe_x_z['FIRST_DIST'], Dataframe_x_z['FIRST_Z'], 0, facecolor= line_color, alpha = 0.1)
    
    return fig


