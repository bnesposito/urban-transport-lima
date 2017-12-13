import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import utm
import random
from shapely import geometry

import config

logger = config.config_logger(__name__,10)

def load_map(gpd_df):
    '''
    Load a geojson file
    '''
    temp = gpd.read_file(gpd_df)
    return temp

def plot_map(gpd_df, path, limits):
    '''
    Plot polygons in gpd_df. 
    Limits is a 4-len tuple containing the limits of the polygons plotted. 
    Plot a line in each limit.
    Save fig in path.
    '''
    plt.figure()
    gpd_df.plot(cmap='Set2', figsize=(10, 10))
    plt.axhline(limits[1], color='black')
    plt.axhline(limits[3], color='black')
    plt.axvline(limits[0], color='black')
    plt.axvline(limits[2], color='black')
    plt.savefig(path)
    plt.close
    return

def plot_map_and_single_point(gpd_df, path, point):
    '''
    Plot polygons in gpd_df. 
    Limits is a 4-len tuple containing the limits of the polygons plotted. 
    Plot a line in each limit.
    Save fig in path.
    '''
    plt.figure()
    fig = plt.figure(1, figsize=(10, 10))
    gpd_df.plot(cmap='Set2', figsize=(10, 10))
    plt.plot(point.x, point.y, marker='+', color='black', 
             markersize=20, mew=2)
    plt.savefig(path)
    plt.close
    return

def plot_map_and_points(gpd_df, path, points):
    '''
    Plot polygons in gpd_df. 
    Limits is a 4-len tuple containing the limits of the polygons plotted. 
    Plot a line in each limit.
    Save fig in path.
    '''
    plt.figure()
    fig = plt.figure(1, figsize=(10, 10))
    gpd_df.plot(cmap='Set2', figsize=(10, 10))
    for point in points:
        plt.plot(point.x, point.y, marker='.', color='black', 
                 markersize=5, mew=1)
    plt.savefig(path)
    plt.close
    return

def boundaries(gpd_df):
    '''
    Extract the overall limits of multiple polygons in gpd_df. In UTM. 
    '''
    limits = gpd_df.geometry.bounds
    max_x = np.max(limits['maxx'])
    max_y = np.max(limits['maxy'])
    min_x = np.min(limits['minx'])
    min_y = np.min(limits['miny'])
    return (max_x, max_y, min_x, min_y)

def included_in_gpd_latlon(gpd_df, lat_lon):
    '''
    Checks if lat_lon point is included in any polygon inside gdp_df.
    Returns the name of the polygon.
    '''
    target = utm.from_latlon(lat_lon[0], lat_lon[1])
    print(target)
    target = geometry.Point(target)
    for i, district in enumerate(gpd_df['geometry']):
        if district.contains(target):
            return gpd_df['name'][i]
    return np.nan 

def included_in_gpd_point(gpd_df, point):
    '''
    Checks if geometry point is included in any polygon inside gdp_df.
    Returns boolean if found
    '''
    for i, district in enumerate(gpd_df['geometry']):
        if district.contains(point):
            return gpd_df['name'][i]
    return False 

def random_start(gpd_df, limits):
    '''
    Extract a random valid point in Lima Metropolitana
    '''
    (max_x, max_y, min_x, min_y) = limits
    n_max = 200
    n = 1
    while n < n_max:
        target = geometry.Point(random.uniform(min_x, max_x), 
                                random.uniform(min_y, max_y))    
        district = included_in_gpd_point(gpd_df, target)
        if district:
            #logger.debug('Point chosen: {0} - {2} after {1} iterations'
            #             .format(target, n, district))
            return target
        n += 1
    return np.nan 

def get_list_of_random_starts(gpd_df, limits, n):
    '''
    Get a list of n random starts.
    '''
    output = []
    for i in range(n):
        output.append(random_start(gpd_df, limits))
    return output
 
def UTM_to_latlon(list_UTM):
    '''
    Converts a list of UTM points into a list of 2-len tuples with lat-lon
    coordinates.
    '''
    output = []
    for point in list_UTM:
        output.append(utm.to_latlon(point.x, point.y, 18, 'L'))
    return output
 
