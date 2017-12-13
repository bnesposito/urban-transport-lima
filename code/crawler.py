import numpy as np
import config

logger = config.config_logger(__name__,10)


def get_district(geocode):
    """ Extracts the district of a json provided by google maps API
    reverse_geocode function.

    Args:
        geocode (dict): json extracted from google maps API.

    Returns:
        str: district name of the geocode.
        np.nan: if there is no district name.
    """
    if not geocode:
        return np.nan
    main = geocode[0]['address_components']
    for section in main:
        type_main = section['types'][0]
        if type_main == 'locality':
            output = section['long_name']
            return output
    return np.nan
       


