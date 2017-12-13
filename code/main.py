import googlemaps
import time
import configparser

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

    logger = config.config_logger(__name__, LOGGER_LEVEL)
    logger.info('Beginning execution: GOOGLE URBAN')
    logger.info('Logger configured - level {0}'.format(LOGGER_LEVEL))
    
    logger.info('Logging in Google Maps API')
    gmaps = googlemaps.Client(key=my_key)
   
    logger.info('Opening Lima map: {0}'.format(LIMA_MAP)) 
    lima_gpd = maps.load_map(LIMA_MAP)

    logger.info('Getting Lima limits')
    lima_limits = maps.boundaries(lima_gpd)
    
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

    #TODO generate queries for trafic each hour
    #TODO automatize the code to send queries each hour.

    config.time_taken_display(t0)

if __name__ == '__main__':
    main()
