import pandas as pd
import numpy as np
import googlemaps
import logging
import config
import random

logger = config.config_logger(__name__,10)

def get_district(geocode):
    '''
    Extracts the district of a json package provided by google maps API
    reverse_geocode function
    '''
    if not geocode:
        return np.nan
    main = geocode[0]['address_components']
    for section in main:
        type_main = section['types'][0]
        if type_main == 'locality':
            output = section['long_name']
            return output
    return np.nan
       


