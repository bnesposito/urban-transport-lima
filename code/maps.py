import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import utm
import random
from shapely import geometry

import config

logger = config.config_logger(__name__,10)
random.seed(1234)

def load_map(path):
    """ Load a geojson file.
    Args:
        path (str): path to the geojson file.

    Returns:
        object: geopandas object
    """
    temp = gpd.read_file(path)
    return temp

def plot_map(gpd_df, path, limits):
    """ Plot polygons in gpd_df. Plot a line in each limit of the figure.
        Save fig in path.

    Args:
        gpd_df (object): geopandas object that will be graphed.
        path (str): save path.
        limits (tuple): limits of the polygons plotted.

    Returns:
        nothing.
    """
    plt.figure()
    gpd_df.plot(cmap='Set2', figsize=(10, 10))
    plt.axhline(limits[1], color='black')
    plt.axhline(limits[3], color='black')
    plt.axvline(limits[0], color='black')
    plt.axvline(limits[2], color='black')
    plt.savefig(path)
    plt.close
    return


def plot_map_and_points(gpd_df, path, points):
    """ Plot polygons in gpd_df. Plot points on top of gpd_df.
        Save fig in path.

    Args:
        gpd_df (object): geopandas object that will be graphed.
        path (str): save path.
        points (list): collection of point objects

    Returns:
        nothing.
    """
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
    """ Extract the overall limits of multiple polygons in gpd_df (UTM).

    Args:
        gpd_df (object): geopandas object - collection of polygons.

    Returns:
        tuple: maximum over x, maximum over y, minimum over x, minimum over y.
    """
    limits = gpd_df.geometry.bounds
    max_x = np.max(limits['maxx'])
    max_y = np.max(limits['maxy'])
    min_x = np.min(limits['minx'])
    min_y = np.min(limits['miny'])
    return (max_x, max_y, min_x, min_y)

def included_in_gpd_latlon(gpd_df, lat_lon):
    """ Find the name of the polygon that contains lat_lon.

    Args:
        gpd_df (object): geopandas object - collection of polygons.
        lat_lon (tuple): latitude and longitude of a point.

    Returns:
        str: name of the polygon that containg lat_lon.
    """
    target = utm.from_latlon(lat_lon[0], lat_lon[1])
    print(target)
    target = geometry.Point(target)
    for i, district in enumerate(gpd_df['geometry']):
        if district.contains(target):
            return gpd_df['name'][i]
    return np.nan 

def included_in_gpd_point(gpd_df, point):
    """ Check if point is included in any polygon of gdp_df.

    Args:
        gpd_df (object): geopandas object - collection of polygons.
        point (object): geopandas object - point.

    Returns:
        bool: True if point is included in gpd_df
    """
    for i, district in enumerate(gpd_df['geometry']):
        if district.contains(point):
            return gpd_df['name'][i]
    return False 

def random_start(gpd_df, limits):
    """ Generate a random valid point inside gpd_df.

    Args:
        gpd_df (object): geopandas object - collection of polygons.
        limits (tuple): range in x,y for the random point generation.

    Returns:
        object: geopandas object - point randomly generated inside gpd_df.
    """
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
    """ Generate a list of random points inside gpd_df.

    Args:
        gpd_df (object): geopandas object - collection of polygons.
        limits (tuple): range in x,y for the random point generation.
        n (int): number of points generated.

    Returns:
        list: collection of random points inside gpd_df.
    """
    output = []
    for i in range(n):
        output.append(random_start(gpd_df, limits))
    return output
 
def UTM_to_latlon(list_UTM):
    """ Converts a list of UTM points into latitude - longitude points.

    Args:
        list_UTM (list): collection of geopandas points in UTM.

    Returns:
        list: collection of geopandas points in lat-lon.
    """
    output = []
    for point in list_UTM:
        output.append(utm.to_latlon(point.x, point.y, 18, 'L'))
    return output