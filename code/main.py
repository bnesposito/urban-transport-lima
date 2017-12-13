import pandas as pd
import numpy as np
import googlemaps
import time
import configparser
import matplotlib.pyplot as plt


import config
import crawler
import maps

def main():

    t0 = time.time()
    LIMA_MAP = './data/lima_map/limaPolyUTM.geojson'
    cfg_name = './config/_credentials.cfg'
    LOGGER_LEVEL = 10
    N = 2000

    cfg_parser = configparser.ConfigParser()
    cfg_parser.read(cfg_name)
    my_key = str(cfg_parser.get('key', 'key'))
    print(my_key)

    logger = config.config_logger(__name__, LOGGER_LEVEL)
    logger.info('Beginning execution: GOOGLE URBAN')
    logger.info('Logger configured - level {0}'.format(LOGGER_LEVEL))
    
    logger.info('Logging in Google Maps API')
    gmaps = googlemaps.Client(key=my_key)
   
    logger.info('Opening Lima map: {0}'.format(LIMA_MAP)) 
    lima_gpd = maps.load_map(LIMA_MAP)
    print(lima_gpd.head())

    logger.info('Getting Lima limits')
    lima_limits = maps.boundaries(lima_gpd)
    print(lima_limits)
    
    logger.info('Plotting Lima map')
    save_path_lima_map = './data/lima_map/lima.png'
    maps.plot_map(lima_gpd, save_path_lima_map, lima_limits)

    logger.info('Getting {0} random starts'.format(N))
    start_points = maps.get_list_of_random_starts(
                       lima_gpd, lima_limits, n = N)
  
    logger.info('Plotting points in Lima map')
    save_path_lima_point = './data/lima_map/lima_start_points.png'
    maps.plot_map_and_points(lima_gpd, save_path_lima_point, start_points)

    logger.info('Converting UTM points into lat-lon points')
    start_points = maps.UTM_to_latlon(start_points)

    print(start_points[:5])

    hi
    #TODO generate queries for trafic each hour
    #TODO automatize the code to send queries each hour.
    
    
#    target_point = (-12.083618, -77.047986)
#    district = maps.included_in_gpd_latlon(lima_gpd, target_point)
#    print(district)
    
   

    # Look up an address with reverse geocoding
    query = gmaps.reverse_geocode((-12.083618, -77.047986))
    print(crawler.get_district(query))
    query = gmaps.reverse_geocode((-12.000976, -77.466567))
    print(crawler.get_district(query))
    query = gmaps.reverse_geocode((-12.296334, -76.828464))
    print(crawler.get_district(query))
    print(' ')

    hi

    # Request directions via public transit
    now = datetime.now()
    start = (-12.000976, -77.466567)
    #(-12.089682, -77.052299)
    end = (-12.091139, -76.964386)
    directions_result = gmaps.directions(start,
                                         end,
                                         mode="driving",
                                         departure_time = now)
    # Golf los incas: (-12.099166, -77.047133),
    # Casa: (-12.091139, -76.964386),
    # UP: (-12.089682, -77.052299), 

    output = directions_result[0]
    print(len(output))
    print(output.keys())
    for i in output:
        print('{0} -- {1}'.format(i, output[i]))

    print(output['legs'][0].keys())
    print(output['legs'][0]['duration'])
    print(output['legs'][0]['distance'])


    config.time_taken_display(t0)

if __name__ == '__main__':
    main()
