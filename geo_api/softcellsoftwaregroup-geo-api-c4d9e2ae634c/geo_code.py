import numpy as np
from geopy import distance
from fuzzywuzzy import fuzz
import re
from router_request import geo_code_request
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('log/geo_code')
logging.basicConfig(level=logging.DEBUG, filemode='a')
log_format = '%(asctime)s - %(lineno)d - %(levelname)s - %(message)s'

logfilename = "log/geo_code.log"
handler = TimedRotatingFileHandler(logfilename, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False

google_api_key = 'AIzaSyDImnlgB6P5m0uXFVmd2XSpQJaUwvhgeCM'
here_app_id = 'A9Ag9pc9EkJXpWTSWWAu'
here_app_code = 'miatgFK7AGtwCyqMPW7FkQ'


def extract_element_from_json(obj, path):
    """
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    """
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr


def extract(obj, path, ind, arr):
    """
        Extracts an element from a nested dictionary
        along a specified path and returns a list.
        obj - dict - input dictionary
        path - list - list of strings that form the JSON path
        ind - int - starting index
        arr - list - output list
    """
    key = path[ind]
    if ind + 1 < len(path):
        if isinstance(obj, dict):
            if key in obj.keys():
                extract(obj.get(key), path, ind + 1, arr)
            else:
                arr.append(None)
        elif isinstance(obj, list):
            if not obj:
                arr.append(None)
            else:
                for item in obj:
                    extract(item, path, ind, arr)
        else:
            arr.append(None)
    if ind + 1 == len(path):
        if isinstance(obj, list):
            if not obj:
                arr.append(None)
            else:
                for item in obj:
                    arr.append(item.get(key, None))
        elif isinstance(obj, dict):
            arr.append(obj.get(key, None))
        else:
            arr.append(None)
    return arr


'''

def call_google_geocoding(Full_Address):
    google_url='https://maps.googleapis.com/maps/api/geocode/json?address='+Full_Address+'&key='+google_api_key
    google_response = requests.post(google_url,verify=False)
    return google_response.json()

def call_google_reverse_geocoding(lat,lng):
    google_reverse_url='https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(lat)+','+str(lng)+'&key='+google_api_key
    google_response = requests.post(google_reverse_url,verify=False)
    return google_response.json()

def call_here_geocoding(Full_Address,city,pincode,state):
    here_url='https://geocoder.api.here.com/6.2/geocode.json?app_id='+here_app_id+'&app_code='+here_app_code+'&city='+city+'&country=IND&gen=9&postalcode='+str(pincode)+'&state='+state
    here_response = requests.get(here_url,verify=False)
    return here_response.json()

def call_here_reverse_geocoding(lat,lng,radius):
    here_reverse_url='https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?app_id='+here_app_id+'&app_code='+here_app_code+'&gen=9&level=postalCode&mode=retrieveAddresses&prox='+str(lat)+','+str(lng)+','+str(radius)
    here_response = requests.get(here_reverse_url,verify=False)
    return here_response.json()
'''

'''
Highest - 1  Highest precision
High -2      medium/high precision
Low - 3      low precision
Lowest -4   cannot use

1 and 2 are granular while 3 and 4 are non granular
'''

'''1 - lat_long_precision Highest
   2 - lat_long_precision High
   3 - lat_long_precision Medium
   4 - lat_long_precision Low
   5 - lat_long_precision Too Low
'''
here_granular_type = {'houseNumber': 1, 'street': 3, 'intersection': 3, 'landmark': 2, 'country': 4, 'state': 4,
                      'county': 4, 'city': 4, 'district': 4, 'postalCode': 4}
google_granular_type = {'floor': 1, 'room': 1, 'establishment': 2, 'premise': 2, 'subpremise': 2, 'neighborhood': 2,
                        'bus_station': 3, 'train_station': 3, 'transit_station': 3, 'parking': 3, 'park': 3,
                        'street_number': 3, 'intersection': 3, 'route': 3, 'street_address': 3, 'political': 4,
                        'country': 4, 'administrative_area_level_1': 4, 'administrative_area_level_2': 4,
                        'administrative_area_level_3': 4, 'administrative_area_level_4': 4,
                        'administrative_area_level_5': 4, 'colloquial_area': 4, 'locality': 4, 'sublocality': 4,
                        'postal_code': 4, 'natural_feature': 4, 'post_box': 4, 'postal_town': 4, 'airport': 4,
                        'sublocality_level_1': 4, 'sublocality_level_2': 4, 'sublocality_level_3': 4,
                        'sublocality_level_4': 4, 'sublocality_level_5': 4}

here_granular_type_list = list(here_granular_type.keys())
google_granular_type_list = list(google_granular_type.keys())


def get_lat_long_google_yes(Pincode, City, State, Full_Address, appl_id, req_id, inst_name, src_sys_name, product):
    """
        Note:
              Address match percentage threshold is set to 85%
        Algorithm Flow:
        1) Ping the address to google geocoding
        2) Extract latitude,longitude and types from the geocoder response
        3) If latitude and longitude are empty, the Precision is 'not_extracted' and Refer='Yes'
        4) If the geoco-ordinates are not empty, check the types for granularity.
              1. If granular='Highest', the precision is 'High'
              2. If granular='High', the precision is 'Medium'
              3. If granular='Low', ping HERE reverse geocoder with google geoco-ordinates
                  * Extract the reverse geocoder address
                  * Compute address match percentage between input address and reverse geocoder addresses whose
                    pincode matches with that of input address
                  * If the match percentage >=80, then Precision is 'Low'
                  * Else Precision is 'Too Low' and Refer='YES'
              4. If granular='Lowest', precision is 'Too Low' and Refer='YES'

    """
    # Check whether pincode,city,state exists in the address. If not present append it.
    # Handle google status code lat long may be empty
    # Region biasing in geocoding functions
    msg_header = 'Applicant Id: ' + str(appl_id) + ' ' + 'Request Id: ' + str(req_id) + ' Message: '
    try:
        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': 'GOOG',
                                 'address': Full_Address, 'pincode': Pincode, 'city': City, 'state': State,
                                 'reverse_geocoding_api': False, 'google_latitude': None,
                                 'google_longitude': None, 'here_latitude': None,
                                 'here_longitude': None
                                 }
        msg = msg_header + 'Google geocoding request json: ' + str(geo_code_request_json)
        logger.debug('%s', msg)
        ssl_response = geo_code_request(geo_code_request_json)
        msg = msg_header + 'ssl response: ' + str(ssl_response)
        logger.debug('%s', msg)

        google_json = ssl_response.get('google_geocoding_json')
        msg = msg_header + 'Google geocoding json: ' + str(google_json)
        logger.debug('%s', msg)
        google_latitude = extract_element_from_json(google_json, ["payload", "geometry", "location", "lat"])
        google_longitude = extract_element_from_json(google_json, ["payload", "geometry", "location", "lng"])
        google_types = extract_element_from_json(google_json, ["payload", "types"])

        if google_latitude[0] is not None and len(google_types[0]) == 0:
            msg = msg_header + 'Google geocoding type not present'
            logger.error('%s', msg)
            return {'latitude': None, 'longitude': None, 'lat_long_precision': None, 'Refer_flag': True,
                    'scenario': 'G_0', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                    'address_match_percent_list': None}
        if google_latitude[0] is None:  # geocordinates are empty
            return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                    'lat_long_precision': 'not_extracted', 'Refer_flag': True, 'scenario': 'GY_1',
                    'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
        elif google_latitude[0] is not None and google_longitude[0] is not None:
            # The line below returns the granular elements present in the types returned by google geocoder
            granular_common_elements = list(set(google_types[0]).intersection(set(google_granular_type_list)))
            msg = msg_header + 'Google granular elements: ' + str(granular_common_elements)
            logger.debug('%s', msg)
            granular_common_elements_order = [google_granular_type.get(i) for i in granular_common_elements]
            msg = msg_header + 'Google granular elements order: ' + str(granular_common_elements_order)
            logger.debug('%s', msg)
            if min(granular_common_elements_order) == 1:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0], 'lat_long_precision': 'High',
                        'Refer_flag': False, 'scenario': 'GY_2', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif min(granular_common_elements_order) == 2:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                        'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'GY_3',
                        'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
            elif min(granular_common_elements_order) == 3:
                geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                         'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                         'address': None, 'pincode': None, 'city': None, 'state': None,
                                         'reverse_geocoding_api': 'HERE', 'google_latitude': google_latitude[0],
                                         'google_longitude': google_longitude[0], 'here_latitude': None,
                                         'here_longitude': None
                                         }
                msg = msg_header + 'HERE reverse geocoding request json: ' + str(geo_code_request_json)
                logger.debug('%s', msg)
                ssl_reponse = geo_code_request(geo_code_request_json)
                msg = msg_header + 'ssl response: ' + str(ssl_response)
                logger.debug('%s', msg)

                here_json = ssl_response.get('here_reverse_geocoding_json')
                msg = msg_header + 'HERE reverse geocoding json: ' + str(here_json)
                logger.debug('%s', msg)
                here_reverse_address = extract_element_from_json(here_json,
                                                                 ["payload", "response", "view", "result", "location",
                                                                  "address", "label"])
                here_postal_code = extract_element_from_json(here_json,
                                                             ["payload", "response", "view", "result", "location",
                                                              "address", "postalCode"])
                here_address_match_list = []
                for i, j in zip(here_reverse_address, here_postal_code):
                    try:
                        if int(j) == Pincode:
                            here_address_match_list.append(fuzz.token_set_ratio(Full_Address, i))
                    except Exception as E:
                        logger.exception("Address match exception: ")
                msg = msg_header + 'HERE reverse geocoding address match percentage list: ' + str(
                    here_address_match_list)
                logger.debug('%s', msg)
                if len(here_address_match_list) > 0:
                    if max(here_address_match_list) >= 80:
                        return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'GY_4',
                                'pincode_match': 'Yes', 'rev_geo_json': here_json,
                                'address_match_percent_list': here_address_match_list}
                    else:
                        return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'GY_5',
                                'pincode_match': 'Yes', 'rev_geo_json': here_json,
                                'address_match_percent_list': here_address_match_list}
                else:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'GY_6',
                            'pincode_match': 'No', 'rev_geo_json': here_json, 'address_match_percent_list': np.nan}
            else:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                        'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'GY_7',
                        'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
    except Exception as e:
        logger.exception("Exception occurred in Google YES")


def get_lat_long_google_no(Pincode, City, State, Full_Address, appl_id, req_id, inst_name, src_sys_name, product):
    '''
        Note:
        Algorithm Flow:
        1) Ping the address to google geocoding
        2) Extract latitude,longitude and types from the geocoder response
        3) If latitude and longitude are empty, the Precision is 'not_extracted' and Refer='Yes'
        4) If the geoco-ordinates are not empty, check the types for granularity.
              1. If granular='Highest', the precision is 'High'
              2. If granular='High',precision is 'Medium'
              3. If granular='Low',precision is 'Low' and Refer='YES'
              4. If granular='Lowest',precision is 'Too Low' and Refer='YES'

        '''
    msg_header = 'Applicant Id: ' + str(appl_id) + ' ' + 'Request Id: ' + str(req_id) + ' Message: '
    try:
        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': 'GOOG',
                                 'address': Full_Address, 'pincode': Pincode, 'city': City, 'state': State,
                                 'reverse_geocoding_api': False, 'google_latitude': None,
                                 'google_longitude': None, 'here_latitude': None,
                                 'here_longitude': None
                                 }
        msg = msg_header + 'Google geocoding request json: ' + str(geo_code_request_json)
        logger.debug('%s', msg)
        ssl_response = geo_code_request(geo_code_request_json)
        msg = msg_header + 'ssl response: ' + str(ssl_response)
        logger.debug('%s', msg)

        google_json = ssl_response.get('google_geocoding_json')
        msg = msg_header + 'Google geocoding json: ' + str(google_json)
        logger.debug('%s', msg)

        google_latitude = extract_element_from_json(google_json, ["payload", "geometry", "location", "lat"])
        google_longitude = extract_element_from_json(google_json, ["payload", "geometry", "location", "lng"])
        google_types = extract_element_from_json(google_json, ["payload", "types"])

        if google_latitude[0] != None and len(google_types[0]) == 0:
            msg = msg_header + 'Google geocoding type not present'
            logger.error('%s', msg)
            return {'latitude': None, 'longitude': None, 'lat_long_precision': None, 'Refer_flag': True,
                    'scenario': 'GN_0', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                    'address_match_percent_list': None}
        if google_latitude[0] == None:  # geocordinates are empty
            return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                    'lat_long_precision': 'not_extracted', 'Refer_flag': True, 'scenario': 'GN_1',
                    'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
        elif google_latitude[0] != None and google_longitude[0] != None:
            # The line below returns the granular elements present in the types returned by google geocoder
            granular_common_elements = list(set(google_types[0]).intersection(set(google_granular_type_list)))
            msg = msg_header + 'Google granular elements: ' + str(granular_common_elements)
            logger.debug('%s', msg)
            granular_common_elements_order = [google_granular_type.get(i) for i in granular_common_elements]
            msg = msg_header + 'Google granular elements order: ' + str(granular_common_elements_order)
            logger.debug('%s', msg)
            if min(granular_common_elements_order) == 1:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0], 'lat_long_precision': 'High',
                        'Refer_flag': False, 'scenario': 'GN_2', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif min(granular_common_elements_order) == 2:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                        'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'GN_3',
                        'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
            elif min(granular_common_elements_order) == 3:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0], 'lat_long_precision': 'Low',
                        'Refer_flag': True, 'scenario': 'GN_4', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                        'address_match_percent_list': None}
            else:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                        'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'GN_5',
                        'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
    except Exception as e:
        logger.exception("Exception occurred in Google NO")


def get_lat_long_here_yes(Pincode, City, State, Full_Address, appl_id, req_id, inst_name, src_sys_name, product):
    '''
        Note:
        Address Match Percentage threshold is set to 85%
        Algorithm Flow:
        1) ping the address to HERE geocoding api
        2) Extract the geoco-ordinates from the geocoder response
        3) If latitude and longitude are empty, the Precision is 'not_extracted' and Refer='Yes'
        4) If the geoco-ordinates are not empty, check the matchLevel for granularity.
              1. If granular='Highest', the precision is 'High'
              2. If granular='High', the precision is 'Medium'
              3. If granular='Low', ping GOOGLE reverse geocoder with HERE geoco-ordinates
                  * Extract the reverse geocoder address
                  * Compute address match percentage between input address and all reverse geocoder addresses whose
                    pincode matches with that of input address
                  * If the maximum match percentage >=85, then Precision is 'Low'
                  * Else Precision is 'Too Low' and Refer='YES'
             4. If granular='Lowest', the precision is 'Too Low' and Refer='YES'
        '''
    msg_header = 'Applicant Id: ' + str(appl_id) + ' ' + 'Request Id: ' + str(req_id) + ' Message: '
    try:
        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': 'HERE',
                                 'address': Full_Address, 'pincode': Pincode, 'city': City, 'state': State,
                                 'reverse_geocoding_api': False, 'google_latitude': None,
                                 'google_longitude': None, 'here_latitude': None,
                                 'here_longitude': None
                                 }
        msg = msg_header + 'HERE geocoding request json: ' + str(geo_code_request_json)
        logger.debug('%s', msg)
        ssl_response = geo_code_request(geo_code_request_json)
        msg = msg_header + 'ssl response: ' + str(ssl_response)
        logger.debug('%s', msg)

        here_json = ssl_response.get('here_geocoding_json')
        msg = msg_header + 'HERE geocoding json: ' + str(here_json)
        logger.debug('%s', msg)
        here_latitude = extract_element_from_json(here_json, ["payload", "response", "view", "result", "location",
                                                              "displayPosition", "latitude"])
        here_longitude = extract_element_from_json(here_json, ["payload", "response", "view", "result", "location",
                                                               "displayPosition", "longitude"])
        #         here_matchQuality=extract_element_from_json(hg, ["Response", "View","Result","MatchQuality"])
        here_matchLevel = extract_element_from_json(here_json, ["payload", "response", "view", "result", "matchLevel"])

        if here_latitude[0] == None:
            return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'not_extracted',
                    'Refer_flag': True, 'scenario': 'HY_1', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                    'address_match_percent_list': None}
        elif here_latitude[0] != None and here_longitude[0] != None:
            here_matchLevel_order = here_granular_type.get(here_matchLevel[0])
            msg = msg_header + 'HERE matchLevel order: ' + str(here_matchLevel_order)
            logger.debug('%s', msg)
            if here_matchLevel_order == 1:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'High',
                        'Refer_flag': False, 'scenario': 'HY_2', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif here_matchLevel_order == 2:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Medium',
                        'Refer_flag': False, 'scenario': 'HY_3', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif here_matchLevel_order == 3:
                geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                         'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                         'address': None, 'pincode': None, 'city': None, 'state': None,
                                         'reverse_geocoding_api': 'GOOG', 'google_latitude': None,
                                         'google_longitude': None, 'here_latitude': here_latitude[0],
                                         'here_longitude': here_longitude[0]
                                         }
                msg = msg_header + 'Google reverse geocoding request json: ' + str(geo_code_request_json)
                logger.debug('%s', msg)
                ssl_response = geo_code_request(geo_code_request_json)
                msg = msg_header + 'ssl response: ' + str(ssl_response)
                logger.debug('%s', msg)

                google_json = ssl_response.get('google_reverse_geocoding_json')
                msg = msg_header + 'Google reverse geocoding json: ' + str(google_json)
                logger.debug('%s', msg)
                google_reverse_address = extract_element_from_json(google_json, ["payload", "formatted_address"])
                '''
                    call address matching api and do pincode match
                    '''
                address_match_list = []
                for i in google_reverse_address:
                    try:
                        pincode = re.findall(r' (\d{6})', i)
                        if len(pincode) > 0:
                            if int(pincode[0]) == Pincode:
                                address_match = fuzz.token_set_ratio(Full_Address, i)
                                address_match_list.append(address_match)
                    except Exception as E:
                        logger.exception("Address match exception: ")
                msg = msg_header + 'Google reverse geocoding address match percentage list: ' + str(address_match_list)
                logger.debug('%s', msg)
                # google_reverse_address[0] will give the address
                if len(address_match_list) > 0:
                    if max(address_match_list) >= 80:
                        return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'HY_4',
                                'pincode_match': 'Yes', 'rev_geo_json': google_json,
                                'address_match_percent_list': address_match_list}
                    else:
                        return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'HY_5',
                                'pincode_match': 'Yes', 'rev_geo_json': google_json,
                                'address_match_percent_list': address_match_list}
                else:
                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'HY_6',
                            'pincode_match': 'No', 'rev_geo_json': google_json, 'address_match_percent_list': np.nan}
            else:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Too Low',
                        'Refer_flag': True, 'scenario': 'HY_7', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                        'address_match_percent_list': None}
    except Exception as e:
        logger.exception("Exception occurred in HERE YES")


def get_lat_long_here_no(Pincode, City, State, Full_Address, appl_id, req_id, inst_name, src_sys_name, product):
    '''
        Note:
        Algorithm Flow:
        1) ping the address to HERE geocoding api
        2) Extract the geoco-ordinates from the geocoder response
        3) If latitude and longitude are empty, the Precision is 'not_extracted' and Refer='Yes'
        4) If the geoco-ordinates are not empty, check the matchLevel for granularity.
              1. If granular='Highest', the precision is 'High'
              2. If granular='High',precision is 'Medium'
              3. If granular='Low', precision is 'Low' and Refer='Yes'
              4. If granular='Lowest', precision is 'Too Low' and Refer='Yes'
        '''
    msg_header = 'Applicant Id: ' + str(appl_id) + ' ' + 'Request Id: ' + str(req_id) + ' Message: '
    try:
        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': 'HERE',
                                 'address': Full_Address, 'pincode': Pincode, 'city': City, 'state': State,
                                 'reverse_geocoding_api': False, 'google_latitude': None,
                                 'google_longitude': None, 'here_latitude': None,
                                 'here_longitude': None
                                 }
        msg = msg_header + 'HERE geocoding request json: ' + str(geo_code_request_json)
        logger.debug('%s', msg)
        ssl_response = geo_code_request(geo_code_request_json)
        msg = msg_header + 'ssl response: ' + str(ssl_response)
        logger.debug('%s', msg)

        here_json = ssl_response.get('here_geocoding_json')
        msg = msg_header + 'HERE geocoding json: ' + str(here_json)
        logger.debug('%s', msg)
        here_latitude = extract_element_from_json(here_json, ["payload", "response", "view", "result", "location",
                                                              "displayPosition", "latitude"])
        here_longitude = extract_element_from_json(here_json, ["payload", "response", "view", "result", "location",
                                                               "displayPosition", "longitude"])
        #         here_matchQuality=extract_element_from_json(hg, ["Response", "View","Result","MatchQuality"])
        here_matchLevel = extract_element_from_json(here_json, ["payload", "response", "view", "result", "matchLevel"])

        if here_latitude[0] == None:
            return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'not_extracted',
                    'Refer_flag': True, 'scenario': 'HN_1', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                    'address_match_percent_list': None}
        elif here_latitude[0] != None and here_longitude[0] != None:
            here_matchLevel_order = here_granular_type.get(here_matchLevel[0])
            msg = msg_header + 'HERE matchLevel order: ' + str(here_matchLevel_order)
            logger.debug('%s', msg)
            if here_matchLevel_order == 1:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'High',
                        'Refer_flag': False, 'scenario': 'HN_2', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif here_matchLevel_order == 2:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Medium',
                        'Refer_flag': False, 'scenario': 'HN_3', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif here_matchLevel_order == 3:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Low',
                        'Refer_flag': True, 'scenario': 'HN_4', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                        'address_match_percent_list': None}
            else:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Too Low',
                        'Refer_flag': True, 'scenario': 'HN_5', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                        'address_match_percent_list': None}
    except Exception as e:
        logger.exception("Exception occurred in HERE NO")


def get_lat_long_multiple_yes(Pincode, City, State, Full_Address, appl_id, req_id, inst_name, src_sys_name, product):
    '''
        Note:
        Address match percentage threshold is set at 85%
        Algorithm Flow:
        1) Ping the address to both Google geocoding API and HERE geocoding API
        2) Extract GOOGLE geoco-ordinates and HERE geoco-ordinates
        3) If both co-ordinates are empty, precision is 'both_not_extracted' and Refer='Yes'
        4) Else if only Google co-ordinates are empty, check whether matchLevel of HERE co-ordinates is granular
             * If granular='Highest',precision is 'High'
             * If granular='High', precision is 'Medium'
             * If granular='Low', ping GOOGLE reverse geocoder with HERE co-ordinates and compute address match
               percentage with all the reverse addresses whose pincode matches with that of input address
                 1. If address match percentage is >=85, then precision is 'Low'
                 2. Else precision is 'Too Low' and Refer='Yes'
             * If granular='Lowest', precision is 'Too Low' and Refer='Yes'
        5) Else if only HERE co-ordinates are empty, check whether types of GOOGLE co-ordinates is granular
             * If granular='Highest',precision is 'High'
             * If granular='High', precision is 'Medium'
             * If granular='Low', ping HERE reverse geocoder with google co-ordinates and compute address match
               with reverse addresses whose pincode matches with that of input address
                 1. If address match percentage is >=85, then precision is 'Low'
                 2. Else precision is 'Too Low' and Refer='Yes'
             * If granular='Lowest', precision is 'Too Low' and Refer = 'Yes'
        6) Else if both co-ordinates are present, then compute the distance between the two co-ordinates
             1. If granularity of both co-ordinates is either 'Highest' or 'High':
                 * If any one is 'Highest' and distance is less than threshold, then pick it. In case of a tie,
                   pick Google. Precision is 'Highest'
                 * If both granularity = 'High' and distance is less than threshold, pick Google and precision is
                   'High'
                 * If distance is greater than threshold, ping HERE reverse geocoding with GOOGLE co-ordinates and compute address match
                   with the reverse addresses whose pincode matches with that of input address
                     * If the address_match_percent is >=85, then precision is 'Medium'
                     * Else, ping GOOGLE reverse geocoding with HERE co-ordinates and compute address match
                       percentage with the reverse addresses whose pincode matches with that of input address
                         1. If the address match percentage is >=85, then precision is 'Medium'
                         2. Else, precision is 'Low'

             2. If granularity of both co-ordinates is either 'Low' or 'Lowest':
                 * If any one is 'Lowest',precision is 'Too Low' and Refer='Yes'
                 * If both are 'Low'
                     * If distance is greater than threshold, precision is 'Too Low' and Refer='Yes'
                     * Else, ping HERE reverse geocoding with GOOGLE co-ordinates and compute address match
                       with the reverse addresses whose pincode matches with that of input address
                         * If the address_match_percent is >=85, then precision is 'Low'
                         * Else, ping GOOGLE reverse geocoding with HERE co-ordinates and compute address match
                           percentage with the reverse addresses whose pincode matches with that of input address
                             1. If the address match percentage is >=85, then precision is 'Low'
                             2. Else, precision is 'Too Low' and Refer='YES'
            3. If only HERE granularity is either 'Highest' or 'High':
                * If distance is less than threshold, precision is 'High'
                * Else ping GOOGLE reverse geocoding with HERE co-ordinates and compute address match
                  with the reverse addresses whose pincode matches with that of input address
                     * If the address_match_percent is >=85, then precision is 'Medium'
                     * Else, precision is 'Low'
            4. If only GOOGLE granularity is either 'Highest' or 'High':
                * If distance is less than threshold, precision is 'High'
                * Else ping HERE reverse geocoding with GOOGLE co-ordinates and compute address match
                  with the reverse addresses whose pincode matches with that of input address
                     * If the address_match_percent is >=85, then precision is 'Medium'
                     * Else, precision is 'Low'

        '''
    msg_header = 'Applicant Id: ' + str(appl_id) + ' ' + 'Request Id: ' + str(req_id) + ' Message: '
    try:
        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': 'MULT',
                                 'address': Full_Address, 'pincode': Pincode, 'city': City, 'state': State,
                                 'reverse_geocoding_api': False, 'google_latitude': None,
                                 'google_longitude': None, 'here_latitude': None,
                                 'here_longitude': None
                                 }
        msg = msg_header + 'Multiple geocoding request json: ' + str(geo_code_request_json)
        logger.debug('%s', msg)
        ssl_response = geo_code_request(geo_code_request_json)
        msg = msg_header + 'ssl response: ' + str(ssl_response)
        logger.debug('%s', msg)

        google_json = ssl_response.get('google_geocoding_json')
        msg = msg_header + 'Google geocoding json: ' + str(google_json)
        logger.debug('%s', msg)

        here_json = ssl_response.get('here_geocoding_json')
        msg = msg_header + 'HERE geocoding json: ' + str(here_json)
        logger.debug('%s', msg)

        google_latitude = extract_element_from_json(google_json, ["payload", "geometry", "location", "lat"])
        google_longitude = extract_element_from_json(google_json, ["payload", "geometry", "location", "lng"])
        google_types = extract_element_from_json(google_json, ["payload", "types"])

        if google_latitude[0] != None and len(google_types[0]) == 0:
            msg = msg_header + 'Google geocoding type not present'
            logger.error('%s', msg)
            return {'latitude': None, 'longitude': None, 'lat_long_precision': None, 'Refer_flag': True,
                    'scenario': 'MY_0', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                    'address_match_percent_list': None}

        here_latitude = extract_element_from_json(here_json, ["payload", "response", "view", "result", "location",
                                                              "displayPosition", "latitude"])
        here_longitude = extract_element_from_json(here_json, ["payload", "response", "view", "result", "location",
                                                               "displayPosition", "longitude"])
        #         here_matchQuality=extract_element_from_json(hg, ["Response", "View","Result","MatchQuality"])
        here_matchLevel = extract_element_from_json(here_json, ["payload", "response", "view", "result", "matchLevel"])

        if here_latitude[0] == None and google_latitude[0] == None:
            return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                    'lat_long_precision': 'both_not_extracted', 'Refer_flag': True, 'scenario': 'MY_1',
                    'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
        elif google_latitude[0] == None:
            here_matchLevel_order = here_granular_type.get(here_matchLevel[0])
            msg = msg_header + 'HERE matchLevel order: ' + str(here_matchLevel_order)
            logger.debug('%s', msg)
            if here_matchLevel_order == 1:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'High',
                        'Refer_flag': False, 'scenario': 'MY_2', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif here_matchLevel_order == 2:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Medium',
                        'Refer_flag': False, 'scenario': 'MY_3', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif here_matchLevel_order == 3:
                geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                         'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                         'address': None, 'pincode': None, 'city': None, 'state': None,
                                         'reverse_geocoding_api': 'GOOG', 'google_latitude': None,
                                         'google_longitude': None, 'here_latitude': here_latitude[0],
                                         'here_longitude': here_longitude[0]
                                         }
                msg = msg_header + 'Google reverse geocoding request json: ' + str(geo_code_request_json)
                logger.debug('%s', msg)
                ssl_response = geo_code_request(geo_code_request_json)
                msg = msg_header + 'ssl response: ' + str(ssl_response)
                logger.debug('%s', msg)

                google_json = ssl_response.get('google_reverse_geocoding_json')
                msg = msg_header + 'Google reverse geocoding json: ' + str(google_json)
                logger.debug('%s', msg)
                google_reverse_address = extract_element_from_json(google_json, ["payload", "formatted_address"])
                '''
                    call address matching api and do pincode match
                    '''
                address_match_list = []
                for i in google_reverse_address:
                    try:
                        pincode = re.findall(r' (\d{6})', i)
                        if len(pincode) > 0:
                            if int(pincode[0]) == Pincode:
                                address_match = fuzz.token_set_ratio(Full_Address, i)
                                address_match_list.append(address_match)
                    except Exception as E:
                        logger.exception("Address match exception: ")
                msg = msg_header + 'Google reverse geocoding address match percentage list: ' + str(address_match_list)
                logger.debug('%s', msg)
                # google_reverse_address[0] will give the address
                if len(address_match_list) > 0:
                    if max(address_match_list) >= 80:
                        return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_4',
                                'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                'pincode_match': 'Yes'}
                    else:
                        return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_5',
                                'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                'pincode_match': 'Yes'}
                else:
                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_6',
                            'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                            'pincode_match': 'No'}
            else:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Too Low',
                        'Refer_flag': True, 'scenario': 'MY_7', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                        'address_match_percent_list': None}
        elif here_latitude[0] == None:
            granular_common_elements = list(set(google_types[0]).intersection(set(google_granular_type_list)))
            msg = msg_header + 'Google granular elements: ' + str(granular_common_elements)
            logger.debug('%s', msg)
            granular_common_elements_order = [google_granular_type.get(i) for i in granular_common_elements]
            msg = msg_header + 'Google granular elements order: ' + str(granular_common_elements_order)
            logger.debug('%s', msg)
            if min(granular_common_elements_order) == 1:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0], 'lat_long_precision': 'High',
                        'Refer_flag': False, 'scenario': 'MY_8', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif min(granular_common_elements_order) == 2:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                        'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_9',
                        'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
            elif min(granular_common_elements_order) == 3:
                geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                         'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                         'address': None, 'pincode': None, 'city': None, 'state': None,
                                         'reverse_geocoding_api': 'HERE', 'google_latitude': google_latitude[0],
                                         'google_longitude': google_longitude[0], 'here_latitude': None,
                                         'here_longitude': None
                                         }
                msg = msg_header + 'HERE reverse geocoding request json: ' + str(geo_code_request_json)
                logger.debug('%s', msg)
                ssl_response = geo_code_request(geo_code_request_json)
                msg = msg_header + 'ssl response: ' + str(ssl_response)
                logger.debug('%s', msg)

                here_json = ssl_response.get('here_reverse_geocoding_json')
                msg = msg_header + 'HERE reverse geocoding json: ' + str(here_json)
                logger.debug('%s', msg)
                here_reverse_address = extract_element_from_json(here_json,
                                                                 ["payload", "response", "view", "result", "location",
                                                                  "address", "label"])
                here_postal_code = extract_element_from_json(here_json,
                                                             ["payload", "response", "view", "result", "location",
                                                              "address", "postalCode"])
                here_address_match_list = []
                for i, j in zip(here_reverse_address, here_postal_code):
                    try:
                        if int(j) == Pincode:
                            here_address_match_list.append(fuzz.token_set_ratio(Full_Address, i))
                    except Exception as E:
                        logger.exception("Address match exception: ")
                msg = msg_header + 'HERE reverse geocoding address match percentage list: ' + str(
                    here_address_match_list)
                logger.debug('%s', msg)
                if len(here_address_match_list) > 0:
                    if max(here_address_match_list) >= 80:
                        return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_10',
                                'rev_geo_json': here_json, 'address_match_percent_list': here_address_match_list,
                                'pincode_match': 'Yes'}
                    else:
                        return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_11',
                                'rev_geo_json': here_json, 'address_match_percent_list': here_address_match_list,
                                'pincode_match': 'Yes'}
                else:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_12',
                            'rev_geo_json': here_json, 'address_match_percent_list': here_address_match_list,
                            'pincode_match': 'No'}
            else:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                        'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_13',
                        'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
        else:
            here_matchLevel_order = here_granular_type.get(here_matchLevel[0])
            msg = msg_header + 'HERE matchLevel order: ' + str(here_matchLevel_order)
            logger.debug('%s', msg)
            granular_common_elements = list(set(google_types[0]).intersection(set(google_granular_type_list)))
            msg = msg_header + 'Google granular elements: ' + str(granular_common_elements)
            logger.debug('%s', msg)
            granular_common_elements_order = [google_granular_type.get(i) for i in granular_common_elements]
            msg = msg_header + 'Google granular elements order: ' + str(granular_common_elements_order)
            logger.debug('%s', msg)

            here = list([here_latitude[0], here_longitude[0]])  # give here column name
            goog = list([google_latitude[0], google_longitude[0]])  # give google column name
            distance_between_coordinates = distance.distance(here, goog).m
            msg = msg_header + 'Distance between coordinates: ' + str(distance_between_coordinates)
            logger.debug('%s', msg)

            if here_matchLevel_order <= 2 and min(granular_common_elements_order) <= 2:

                # both are granular
                if min(granular_common_elements_order) == 1 and distance_between_coordinates <= 500:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'Highest', 'Refer_flag': False, 'scenario': 'MY_14',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                elif here_matchLevel_order == 1 and distance_between_coordinates <= 500:
                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                            'lat_long_precision': 'Highest', 'Refer_flag': False, 'scenario': 'MY_15',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                elif min(
                        granular_common_elements_order) == 2 and here_matchLevel_order == 2 and distance_between_coordinates <= 500:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MY_16',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                elif distance_between_coordinates > 500:
                    if min(granular_common_elements_order) == 1 and here_matchLevel_order == 2:
                        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name,
                                                 'product': product,
                                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                                 'address': None, 'pincode': None, 'city': None, 'state': None,
                                                 'reverse_geocoding_api': 'HERE', 'google_latitude': google_latitude[0],
                                                 'google_longitude': google_longitude[0], 'here_latitude': None,
                                                 'here_longitude': None
                                                 }
                        msg = msg_header + 'HERE reverse geocoding request json: ' + str(geo_code_request_json)
                        logger.debug('%s', msg)
                        ssl_response = geo_code_request(geo_code_request_json)
                        msg = msg_header + 'ssl response: ' + str(ssl_response)
                        logger.debug('%s', msg)

                        here_json = ssl_response.get('here_reverse_geocoding_json')
                        msg = msg_header + 'HERE reverse geocoding json: ' + str(here_json)
                        logger.debug('%s', msg)
                        here_reverse_address = extract_element_from_json(here_json,
                                                                         ["payload", "response", "view", "result",
                                                                          "location", "address", "label"])
                        here_postal_code = extract_element_from_json(here_json,
                                                                     ["payload", "response", "view", "result",
                                                                      "location", "address", "postalCode"])
                        here_address_match_list = []
                        for i, j in zip(here_reverse_address, here_postal_code):
                            try:
                                if int(j) == Pincode:
                                    here_address_match_list.append(fuzz.token_set_ratio(Full_Address, i))
                            except Exception as E:
                                logger.exception("Address match exception: ")
                        msg = msg_header + 'HERE reverse geocoding address match percentage list: ' + str(
                            here_address_match_list)
                        logger.debug('%s', msg)
                        if len(here_address_match_list) > 0:
                            if max(here_address_match_list) >= 85:
                                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                        'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MY_17',
                                        'rev_geo_json': here_json,
                                        'address_match_percent_list': here_address_match_list, 'pincode_match': 'Yes'}
                            elif max(here_address_match_list) >= 67 and max(here_address_match_list) <= 84:
                                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                        'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_18',
                                        'rev_geo_json': here_json,
                                        'address_match_percent_list': here_address_match_list, 'pincode_match': 'Yes'}
                        if len(here_address_match_list) == 0 or max(here_address_match_list) < 67:
                            geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name,
                                                     'product': product,
                                                     'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                                     'address': None, 'pincode': None, 'city': None, 'state': None,
                                                     'reverse_geocoding_api': 'GOOG', 'google_latitude': None,
                                                     'google_longitude': None, 'here_latitude': here_latitude[0],
                                                     'here_longitude': here_longitude[0]
                                                     }
                            msg = msg_header + 'Google reverse geocoding request json: ' + str(geo_code_request_json)
                            logger.debug('%s', msg)
                            ssl_response = geo_code_request(geo_code_request_json)
                            msg = msg_header + 'ssl response: ' + str(ssl_response)
                            logger.debug('%s', msg)

                            google_json = ssl_response.get('google_reverse_geocoding_json')
                            msg = msg_header + 'Google reverse geocoding json: ' + str(google_json)
                            logger.debug('%s', msg)
                            google_reverse_address = extract_element_from_json(google_json,
                                                                               ["payload", "formatted_address"])
                            '''
                                    call address matching api and do pincode match
                                    '''
                            address_match_list = []
                            for i in google_reverse_address:
                                try:
                                    pincode = re.findall(r' (\d{6})', i)
                                    if len(pincode) > 0:
                                        if int(pincode[0]) == Pincode:
                                            address_match = fuzz.token_set_ratio(Full_Address, i)
                                            address_match_list.append(address_match)
                                except Exception as E:
                                    logger.exception("Address match exception: ")
                            msg = msg_header + 'Google reverse geocoding address match percentage list: ' + str(
                                address_match_list)
                            logger.debug('%s', msg)
                            if len(address_match_list) > 0:
                                if max(address_match_list) >= 85:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_19',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                                elif max(address_match_list) >= 67 and max(address_match_list) <= 84:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_20',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                                elif max(address_match_list) < 67 and len(here_address_match_list) > 0:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_21',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                                elif max(address_match_list) < 67 and len(here_address_match_list) == 0:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_22',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                            else:
                                if len(here_address_match_list) > 0:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_23',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                                else:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_24',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'No'}
                    elif here_matchLevel_order == 1 and min(granular_common_elements_order) == 2:
                        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name,
                                                 'product': product,
                                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                                 'address': None, 'pincode': None, 'city': None, 'state': None,
                                                 'reverse_geocoding_api': 'GOOG', 'google_latitude': None,
                                                 'google_longitude': None, 'here_latitude': here_latitude[0],
                                                 'here_longitude': here_longitude[0]
                                                 }
                        msg = msg_header + 'Google reverse geocoding request json: ' + str(geo_code_request_json)
                        logger.debug('%s', msg)
                        ssl_response = geo_code_request(geo_code_request_json)
                        msg = msg_header + 'ssl response: ' + str(ssl_response)
                        logger.debug('%s', msg)

                        google_json = ssl_response.get('google_reverse_geocoding_json')
                        msg = msg_header + 'Google reverse geocoding json: ' + str(google_json)
                        logger.debug('%s', msg)
                        google_reverse_address = extract_element_from_json(google_json,
                                                                           ["payload", "formatted_address"])
                        '''
                            call address matching api and do pincode match
                            '''
                        address_match_list = []
                        for i in google_reverse_address:
                            try:
                                pincode = re.findall(r' (\d{6})', i)
                                if len(pincode) > 0:
                                    if int(pincode[0]) == Pincode:
                                        address_match = fuzz.token_set_ratio(Full_Address, i)
                                        address_match_list.append(address_match)
                            except Exception as E:
                                logger.exception("Address match exception: ")
                        msg = msg_header + 'Google reverse geocoding address match percentage list: ' + str(
                            address_match_list)
                        logger.debug('%s', msg)

                        if len(address_match_list) > 0:
                            if max(address_match_list) >= 85:
                                return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                        'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MY_25',
                                        'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                        'pincode_match': 'Yes'}
                            elif max(address_match_list) >= 67 and max(address_match_list) <= 84:
                                return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                        'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_26',
                                        'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                        'pincode_match': 'Yes'}
                        if len(address_match_list) == 0 or max(address_match_list) < 67:
                            geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name,
                                                     'product': product,
                                                     'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                                     'address': None, 'pincode': None, 'city': None, 'state': None,
                                                     'reverse_geocoding_api': 'HERE',
                                                     'google_latitude': google_latitude[0],
                                                     'google_longitude': google_longitude[0], 'here_latitude': None,
                                                     'here_longitude': None
                                                     }
                            msg = msg_header + 'HERE reverse geocoding request json: ' + str(geo_code_request_json)
                            logger.debug('%s', msg)
                            ssl_response = geo_code_request(geo_code_request_json)
                            msg = msg_header + 'ssl response: ' + str(ssl_response)
                            logger.debug('%s', msg)

                            here_json = ssl_response.get('here_reverse_geocoding_json')
                            msg = msg_header + 'HERE reverse geocoding json: ' + str(here_json)
                            logger.debug('%s', msg)
                            here_reverse_address = extract_element_from_json(here_json,
                                                                             ["payload", "response", "view", "result",
                                                                              "location", "address", "label"])
                            here_postal_code = extract_element_from_json(here_json,
                                                                         ["payload", "response", "view", "result",
                                                                          "location", "address", "postalCode"])
                            here_address_match_list = []
                            for i, j in zip(here_reverse_address, here_postal_code):
                                try:
                                    if int(j) == Pincode:
                                        here_address_match_list.append(fuzz.token_set_ratio(Full_Address, i))
                                except Exception as E:
                                    logger.exception("Address match exception: ")
                            msg = msg_header + 'HERE reverse geocoding address match percentage list: ' + str(
                                here_address_match_list)
                            logger.debug('%s', msg)
                            if len(here_address_match_list) > 0:
                                if max(here_address_match_list) >= 85:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_27',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                                elif max(here_address_match_list) >= 67 and max(here_address_match_list) <= 84:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_28',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                                elif max(here_address_match_list) < 67 and len(address_match_list) > 0:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_29',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                                elif max(here_address_match_list) < 67 and len(address_match_list) == 0:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_30',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                            else:
                                if len(address_match_list) > 0:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_31',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                                else:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_32',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'No'}
                    elif here_matchLevel_order == 2 and min(granular_common_elements_order) == 2:
                        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name,
                                                 'product': product,
                                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                                 'address': None, 'pincode': None, 'city': None, 'state': None,
                                                 'reverse_geocoding_api': 'HERE', 'google_latitude': google_latitude[0],
                                                 'google_longitude': google_longitude[0], 'here_latitude': None,
                                                 'here_longitude': None
                                                 }
                        msg = msg_header + 'HERE reverse geocoding request json: ' + str(geo_code_request_json)
                        logger.debug('%s', msg)
                        ssl_response = geo_code_request(geo_code_request_json)
                        msg = msg_header + 'ssl response: ' + str(ssl_response)
                        logger.debug('%s', msg)

                        here_json = ssl_response.get('here_reverse_geocoding_json')
                        msg = msg_header + 'HERE reverse geocoding json: ' + str(here_json)
                        logger.debug('%s', msg)
                        here_reverse_address = extract_element_from_json(here_json,
                                                                         ["payload", "response", "view", "result",
                                                                          "location", "address", "label"])
                        here_postal_code = extract_element_from_json(here_json,
                                                                     ["payload", "response", "view", "result",
                                                                      "location", "address", "postalCode"])
                        here_address_match_list = []
                        for i, j in zip(here_reverse_address, here_postal_code):
                            try:
                                if int(j) == Pincode:
                                    here_address_match_list.append(fuzz.token_set_ratio(Full_Address, i))
                            except Exception as E:
                                logger.exception("Address match exception: ")
                        msg = msg_header + 'HERE reverse geocoding address match percentage list: ' + str(
                            here_address_match_list)
                        logger.debug('%s', msg)

                        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name,
                                                 'product': product,
                                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                                 'address': None, 'pincode': None, 'city': None, 'state': None,
                                                 'reverse_geocoding_api': 'GOOG', 'google_latitude': None,
                                                 'google_longitude': None, 'here_latitude': here_latitude[0],
                                                 'here_longitude': here_longitude[0]
                                                 }
                        msg = msg_header + 'Google reverse geocoding request json: ' + str(geo_code_request_json)
                        logger.debug('%s', msg)
                        ssl_response = geo_code_request(geo_code_request_json)
                        msg = msg_header + 'ssl response: ' + str(ssl_response)
                        logger.debug('%s', msg)

                        google_json = ssl_response.get('google_reverse_geocoding_json')
                        msg = msg_header + 'Google reverse geocoding json: ' + str(google_json)
                        logger.debug('%s', msg)
                        google_reverse_address = extract_element_from_json(google_json,
                                                                           ["payload", "formatted_address"])
                        '''
                            call address matching api and do pincode match
                            '''
                        address_match_list = []
                        for i in google_reverse_address:
                            try:
                                pincode = re.findall(r' (\d{6})', i)
                                if len(pincode) > 0:
                                    if int(pincode[0]) == Pincode:
                                        address_match = fuzz.token_set_ratio(Full_Address, i)
                                        address_match_list.append(address_match)
                            except Exception as E:
                                logger.exception("Address match exception: ")
                        msg = msg_header + 'Google reverse geocoding address match percentage list: ' + str(
                            address_match_list)
                        logger.debug('%s', msg)

                        if len(address_match_list) > 0 and len(here_address_match_list) > 0:
                            if max(address_match_list) > max(here_address_match_list):
                                if max(address_match_list) >= 85:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_33',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                                elif max(address_match_list) >= 67 and max(address_match_list) <= 84:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_34',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                                else:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_35',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                            else:
                                if max(here_address_match_list) >= 85:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_36',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                                elif max(here_address_match_list) >= 67 and max(here_address_match_list) <= 84:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_37',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                                else:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_38',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                        elif len(address_match_list) > 0 and len(here_address_match_list) == 0:
                            if max(address_match_list) >= 85:
                                return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                        'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_39',
                                        'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                        'pincode_match': 'Yes'}
                            elif max(address_match_list) >= 67 and max(address_match_list) <= 84:
                                return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                        'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_40',
                                        'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                        'pincode_match': 'Yes'}
                            else:
                                return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                        'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_41',
                                        'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                        'pincode_match': 'Yes'}
                        elif len(address_match_list) == 0 and len(here_address_match_list) > 0:
                            if max(here_address_match_list) >= 85:
                                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                        'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_42',
                                        'rev_geo_json': here_json,
                                        'address_match_percent_list': here_address_match_list, 'pincode_match': 'Yes'}
                            elif max(here_address_match_list) >= 67 and max(here_address_match_list) <= 84:
                                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                        'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_43',
                                        'rev_geo_json': here_json,
                                        'address_match_percent_list': here_address_match_list, 'pincode_match': 'Yes'}
                            else:
                                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                        'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_44',
                                        'rev_geo_json': here_json,
                                        'address_match_percent_list': here_address_match_list, 'pincode_match': 'Yes'}
                        elif len(address_match_list) == 0 and len(here_address_match_list) == 0:
                            return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                    'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_45',
                                    'rev_geo_json': here_json, 'address_match_percent_list': here_address_match_list,
                                    'pincode_match': 'No'}
                    elif here_matchLevel_order == 1 and min(granular_common_elements_order) == 1:
                        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name,
                                                 'product': product,
                                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                                 'address': None, 'pincode': None, 'city': None, 'state': None,
                                                 'reverse_geocoding_api': 'HERE', 'google_latitude': google_latitude[0],
                                                 'google_longitude': google_longitude[0], 'here_latitude': None,
                                                 'here_longitude': None
                                                 }
                        msg = msg_header + 'HERE reverse geocoding request json: ' + str(geo_code_request_json)
                        logger.debug('%s', msg)
                        ssl_response = geo_code_request(geo_code_request_json)
                        msg = msg_header + 'ssl response: ' + str(ssl_response)
                        logger.debug('%s', msg)

                        here_json = ssl_response.get('here_reverse_geocoding_json')
                        msg = msg_header + 'HERE reverse geocoding json: ' + str(here_json)
                        logger.debug('%s', msg)
                        here_reverse_address = extract_element_from_json(here_json,
                                                                         ["payload", "response", "view", "result",
                                                                          "location", "address", "label"])
                        here_postal_code = extract_element_from_json(here_json,
                                                                     ["payload", "response", "view", "result",
                                                                      "location", "address", "postalCode"])
                        here_address_match_list = []
                        for i, j in zip(here_reverse_address, here_postal_code):
                            try:
                                if int(j) == Pincode:
                                    here_address_match_list.append(fuzz.token_set_ratio(Full_Address, i))
                            except Exception as E:
                                logger.exception("Address match exception: ")
                        msg = msg_header + 'HERE reverse geocoding address match percentage list: ' + str(
                            here_address_match_list)
                        logger.debug('%s', msg)

                        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name,
                                                 'product': product,
                                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                                 'address': None, 'pincode': None, 'city': None, 'state': None,
                                                 'reverse_geocoding_api': 'GOOG', 'google_latitude': None,
                                                 'google_longitude': None, 'here_latitude': here_latitude[0],
                                                 'here_longitude': here_longitude[0]
                                                 }
                        msg = msg_header + 'Google reverse geocoding request json: ' + str(geo_code_request_json)
                        logger.debug('%s', msg)
                        ssl_response = geo_code_request(geo_code_request_json)
                        msg = msg_header + 'ssl response: ' + str(ssl_response)
                        logger.debug('%s', msg)

                        google_json = ssl_response.get('google_reverse_geocoding_json')
                        msg = msg_header + 'Google reverse geocoding json: ' + str(google_json)
                        logger.debug('%s', msg)
                        google_reverse_address = extract_element_from_json(google_json,
                                                                           ["payload", "formatted_address"])
                        '''
                            call address matching api and do pincode match
                            '''
                        address_match_list = []
                        for i in google_reverse_address:
                            try:
                                pincode = re.findall(r' (\d{6})', i)
                                if len(pincode) > 0:
                                    if int(pincode[0]) == Pincode:
                                        address_match = fuzz.token_set_ratio(Full_Address, i)
                                        address_match_list.append(address_match)
                            except Exception as E:
                                logger.exception("Address match exception: ")
                        msg = msg_header + 'Google reverse geocoding address match percentage list: ' + str(
                            address_match_list)
                        logger.debug('%s', msg)

                        if len(address_match_list) > 0 and len(here_address_match_list) > 0:
                            if max(address_match_list) > max(here_address_match_list):
                                if max(address_match_list) >= 85:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MY_46',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                                elif max(address_match_list) >= 67 and max(address_match_list) <= 84:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_47',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                                else:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_48',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                            else:
                                if max(here_address_match_list) >= 85:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MY_49',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                                elif max(here_address_match_list) >= 67 and max(here_address_match_list) <= 84:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_50',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                                else:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_51',
                                            'rev_geo_json': here_json,
                                            'address_match_percent_list': here_address_match_list,
                                            'pincode_match': 'Yes'}
                        elif len(address_match_list) > 0 and len(here_address_match_list) == 0:
                            if max(address_match_list) >= 85:
                                return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                        'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MY_52',
                                        'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                        'pincode_match': 'Yes'}
                            elif max(address_match_list) >= 67 and max(address_match_list) <= 84:
                                return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                        'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_53',
                                        'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                        'pincode_match': 'Yes'}
                            else:
                                return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                        'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_54',
                                        'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                        'pincode_match': 'Yes'}
                        elif len(address_match_list) == 0 and len(here_address_match_list) > 0:
                            if max(here_address_match_list) >= 85:
                                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                        'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MY_55',
                                        'rev_geo_json': here_json,
                                        'address_match_percent_list': here_address_match_list, 'pincode_match': 'Yes'}
                            elif max(here_address_match_list) >= 67 and max(here_address_match_list) <= 84:
                                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                        'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_56',
                                        'rev_geo_json': here_json,
                                        'address_match_percent_list': here_address_match_list, 'pincode_match': 'Yes'}
                            else:
                                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                        'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_57',
                                        'rev_geo_json': here_json,
                                        'address_match_percent_list': here_address_match_list, 'pincode_match': 'Yes'}
                        elif len(address_match_list) == 0 and len(here_address_match_list) == 0:
                            return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                    'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_58',
                                    'rev_geo_json': here_json, 'address_match_percent_list': here_address_match_list,
                                    'pincode_match': 'No'}

            elif here_matchLevel_order > 2 and min(granular_common_elements_order) > 2:
                # both are non granular
                if here_matchLevel_order == 4 and min(granular_common_elements_order) == 4:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_59',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                elif min(granular_common_elements_order) == 4:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_60',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                elif here_matchLevel_order == 4:
                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_61',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                else:
                    if distance_between_coordinates > 500:
                        return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_62',
                                'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                                'address_match_percent_list': None}
                    else:
                        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name,
                                                 'product': product,
                                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                                 'address': None, 'pincode': None, 'city': None, 'state': None,
                                                 'reverse_geocoding_api': 'HERE', 'google_latitude': google_latitude[0],
                                                 'google_longitude': google_longitude[0], 'here_latitude': None,
                                                 'here_longitude': None
                                                 }
                        msg = msg_header + 'HERE reverse geocoding request json: ' + str(geo_code_request_json)
                        logger.debug('%s', msg)
                        ssl_response = geo_code_request(geo_code_request_json)
                        msg = msg_header + 'ssl response: ' + str(ssl_response)
                        logger.debug('%s', msg)

                        here_json = ssl_response.get('here_reverse_geocoding_json')
                        msg = msg_header + 'HERE reverse geocoding json: ' + str(here_json)
                        logger.debug('%s', msg)
                        here_reverse_address = extract_element_from_json(here_json,
                                                                         ["payload", "response", "view", "result",
                                                                          "location", "address", "label"])
                        here_postal_code = extract_element_from_json(here_json,
                                                                     ["payload", "response", "view", "result",
                                                                      "location", "address", "postalCode"])
                        here_address_match_list = []
                        for i, j in zip(here_reverse_address, here_postal_code):
                            try:
                                if int(j) == Pincode:
                                    here_address_match_list.append(fuzz.token_set_ratio(Full_Address, i))
                            except Exception as E:
                                logger.exception("Address match exception: ")
                        msg = msg_header + 'HERE reverse geocoding address match percentage list: ' + str(
                            here_address_match_list)
                        logger.debug('%s', msg)
                        if len(here_address_match_list) > 0 and max(here_address_match_list) >= 75:
                            return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                    'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_63',
                                    'rev_geo_json': here_json, 'address_match_percent_list': here_address_match_list,
                                    'pincode_match': 'Yes'}
                        else:
                            geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name,
                                                     'product': product,
                                                     'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                                     'address': None, 'pincode': None, 'city': None, 'state': None,
                                                     'reverse_geocoding_api': 'GOOG', 'google_latitude': None,
                                                     'google_longitude': None, 'here_latitude': here_latitude[0],
                                                     'here_longitude': here_longitude[0]
                                                     }
                            msg = msg_header + 'Google reverse geocoding request json: ' + str(geo_code_request_json)
                            logger.debug('%s', msg)
                            ssl_response = geo_code_request(geo_code_request_json)
                            msg = msg_header + 'ssl response: ' + str(ssl_response)
                            logger.debug('%s', msg)

                            google_json = ssl_response.get('google_reverse_geocoding_json')
                            msg = msg_header + 'Google reverse geocoding json: ' + str(google_json)
                            logger.debug('%s', msg)
                            google_reverse_address = extract_element_from_json(google_json,
                                                                               ["payload", "formatted_address"])
                            '''
                                call address matching api and do pincode match
                                '''
                            address_match_list = []
                            for i in google_reverse_address:
                                try:
                                    pincode = re.findall(r' (\d{6})', i)
                                    if len(pincode) > 0:
                                        if int(pincode[0]) == Pincode:
                                            address_match = fuzz.token_set_ratio(Full_Address, i)
                                            address_match_list.append(address_match)
                                except Exception as E:
                                    logger.exception("Address match exception: ")
                            msg = msg_header + 'Google reverse geocoding address match percentage list: ' + str(
                                address_match_list)
                            logger.debug('%s', msg)
                            # google_reverse_address[0] will give the address
                            if len(address_match_list) > 0:
                                if max(address_match_list) >= 75:
                                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_64',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                                else:
                                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_65',
                                            'rev_geo_json': google_json,
                                            'address_match_percent_list': address_match_list, 'pincode_match': 'Yes'}
                            else:
                                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                        'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_66',
                                        'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                        'pincode_match': 'No'}
            elif here_matchLevel_order <= 2:
                # only here is granular
                if distance_between_coordinates <= 500:
                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'High',
                            'Refer_flag': False, 'scenario': 'MY_67', 'pincode_match': 'Not Applicable',
                            'rev_geo_json': None, 'address_match_percent_list': None}
                else:
                    geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                             'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                             'address': None, 'pincode': None, 'city': None, 'state': None,
                                             'reverse_geocoding_api': 'GOOG', 'google_latitude': None,
                                             'google_longitude': None, 'here_latitude': here_latitude[0],
                                             'here_longitude': here_longitude[0]
                                             }
                    msg = msg_header + 'Google reverse geocoding request json: ' + str(geo_code_request_json)
                    logger.debug('%s', msg)
                    ssl_response = geo_code_request(geo_code_request_json)
                    msg = msg_header + 'ssl response: ' + str(ssl_response)
                    logger.debug('%s', msg)

                    google_json = ssl_response.get('google_reverse_geocoding_json')
                    msg = msg_header + 'Google reverse geocoding json: ' + str(google_json)
                    logger.debug('%s', msg)
                    google_reverse_address = extract_element_from_json(google_json, ["payload", "formatted_address"])
                    '''
                        call address matching api and do pincode match
                        '''
                    address_match_list = []
                    for i in google_reverse_address:
                        try:
                            pincode = re.findall(r' (\d{6})', i)
                            if len(pincode) > 0:
                                if int(pincode[0]) == Pincode:
                                    address_match = fuzz.token_set_ratio(Full_Address, i)
                                    address_match_list.append(address_match)
                        except Exception as E:
                            logger.exception("Address match exception: ")
                    msg = msg_header + 'Google reverse geocoding address match percentage list: ' + str(
                        address_match_list)
                    logger.debug('%s', msg)
                    # google_reverse_address[0] will give the address
                    if len(address_match_list) > 0:
                        if max(address_match_list) >= 85:
                            return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                    'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MY_68',
                                    'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                    'pincode_match': 'Yes'}
                        elif max(address_match_list) >= 67 and max(address_match_list) <= 84:
                            return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                    'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_69',
                                    'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                    'pincode_match': 'Yes'}
                        else:
                            return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                    'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_70',
                                    'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                    'pincode_match': 'Yes'}
                    else:
                        return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_71',
                                'rev_geo_json': google_json, 'address_match_percent_list': address_match_list,
                                'pincode_match': 'No'}
            elif min(granular_common_elements_order) <= 2:
                # only google is granular
                if distance_between_coordinates <= 500:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MY_72',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                else:
                    geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                             'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': False,
                                             'address': None, 'pincode': None, 'city': None, 'state': None,
                                             'reverse_geocoding_api': 'HERE', 'google_latitude': google_latitude[0],
                                             'google_longitude': google_longitude[0], 'here_latitude': None,
                                             'here_longitude': None
                                             }
                    msg = msg_header + 'HERE reverse geocoding request json: ' + str(geo_code_request_json)
                    logger.debug('%s', msg)
                    ssl_response = geo_code_request(geo_code_request_json)
                    msg = msg_header + 'ssl response: ' + str(ssl_response)
                    logger.debug('%s', msg)

                    here_json = ssl_response.get('here_reverse_geocoding_json')
                    msg = msg_header + 'HERE reverse geocoding json: ' + str(here_json)
                    logger.debug('%s', msg)
                    here_reverse_address = extract_element_from_json(here_json,
                                                                     ["payload", "response", "view", "result",
                                                                      "location", "address", "label"])
                    here_postal_code = extract_element_from_json(here_json,
                                                                 ["payload", "response", "view", "result", "location",
                                                                  "address", "postalCode"])
                    here_address_match_list = []
                    for i, j in zip(here_reverse_address, here_postal_code):
                        try:
                            if int(j) == Pincode:
                                here_address_match_list.append(fuzz.token_set_ratio(Full_Address, i))
                        except Exception as E:
                            logger.exception("Address match exception: ")
                    msg = msg_header + 'HERE reverse geocoding address match percentage list: ' + str(
                        here_address_match_list)
                    logger.debug('%s', msg)
                    if len(here_address_match_list) > 0:
                        if max(here_address_match_list) >= 85:
                            return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                    'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MY_73',
                                    'rev_geo_json': here_json, 'address_match_percent_list': here_address_match_list,
                                    'pincode_match': 'Yes'}
                        elif max(here_address_match_list) >= 67 and max(here_address_match_list) <= 84:
                            return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                    'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MY_74',
                                    'rev_geo_json': here_json, 'address_match_percent_list': here_address_match_list,
                                    'pincode_match': 'Yes'}
                        else:
                            return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                    'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MY_75',
                                    'rev_geo_json': here_json, 'address_match_percent_list': here_address_match_list,
                                    'pincode_match': 'Yes'}
                    else:
                        return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MY_76',
                                'rev_geo_json': here_json, 'address_match_percent_list': here_address_match_list,
                                'pincode_match': 'No'}
    except Exception as e:
        logger.exception("Exception occurred in MULITPLE YES")


def get_lat_long_multiple_no(Pincode, City, State, Full_Address, appl_id, req_id, inst_name, src_sys_name, product):
    '''
        Note:
        Algorithm Flow:
        1) Ping the address to both Google geocoding API and HERE geocoding API
        2) Extract GOOGLE geoco-ordinates and HERE geoco-ordinates
        3) If both co-ordinates are empty, precision is 'both_not_extracted' and Refer='Yes'
        4) Else if only Google co-ordinates are empty, check whether matchLevel of HERE co-ordinates is granular
             * If granular='Highest',precision is 'High'
             * If granular='High', precision is 'Medium'
             * If granular='Low',then precision is 'Low' and Refer='Yes'
             * If granular='Lowest', precision is 'Too Low' and Refer='Yes'
        5) Else if only HERE co-ordinates are empty, check whether types of GOOGLE co-ordinates is granular
             * If granular='Highest',precision is 'High'
             * If granular='High', precision is 'Medium'
             * If granular='Low', then precision is 'Low' and Refer='Yes'
             * If granular='Lowest', precision is 'Too Low' and Refer = 'Yes'
        6) Else if both co-ordinates are present, then compute the distance between the two co-ordinates
             1. If granularity of both co-ordinates is either 'Highest' or 'High':
                 * If any one is 'Highest' and distance is less than threshold, then pick it. In case of a tie,
                   pick Google. Precision is 'Highest'
                 * If both granularity = 'High' and distance is less than threshold, pick Google and precision is
                   'High'
                 * If distance is greater than threshold, pick the one most granular. Precision is 'Low'
             2. If granularity of both co-ordinates is either 'Low' or 'Lowest':
                 * If any one is 'Lowest',precision is 'Too Low' and Refer='Yes'
                 * If both are 'Low'
                     * If distance is greater than threshold, precision is 'Too Low' and Refer='Yes'
                     * Else, precision is 'Low'
             3. If only HERE granularity is either 'Highest' or 'High':
                * If distance is less than threshold, precision is 'High'
                * Else precision is 'Low'
             4. If only GOOGLE granularity is either 'Highest' or 'High':
                * If distance is less than threshold, precision is 'High'
                * Else precision is 'Low'

        '''
    msg_header = 'Applicant Id: ' + str(appl_id) + ' ' + 'Request Id: ' + str(req_id) + ' Message: '
    try:
        geo_code_request_json = {'inst_name': inst_name, 'src_sys_name': src_sys_name, 'product': product,
                                 'appl_id': appl_id, 'req_id': req_id, 'geocoding_api': 'MULT',
                                 'address': Full_Address, 'pincode': Pincode, 'city': City, 'state': State,
                                 'reverse_geocoding_api': False, 'google_latitude': None,
                                 'google_longitude': None, 'here_latitude': None,
                                 'here_longitude': None
                                 }
        msg = msg_header + 'Multiple geocoding request json: ' + str(geo_code_request_json)
        logger.debug('%s', msg)
        ssl_response = geo_code_request(geo_code_request_json)
        msg = msg_header + 'ssl response: ' + str(ssl_response)
        logger.debug('%s', msg)

        google_json = ssl_response.get('google_geocoding_json')
        msg = msg_header + 'Google geocoding json: ' + str(google_json)
        logger.debug('%s', msg)

        here_json = ssl_response.get('here_geocoding_json')
        msg = msg_header + 'HERE geocoding json: ' + str(here_json)
        logger.debug('%s', msg)

        google_latitude = extract_element_from_json(google_json, ["payload", "geometry", "location", "lat"])
        google_longitude = extract_element_from_json(google_json, ["payload", "geometry", "location", "lng"])
        google_types = extract_element_from_json(google_json, ["payload", "types"])

        if google_latitude[0] != None and len(google_types[0]) == 0:
            msg = msg_header + 'Google geocoding type not present'
            logger.error('%s', msg)
            return {'latitude': None, 'longitude': None, 'lat_long_precision': None, 'Refer_flag': True,
                    'scenario': 'MN_0', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                    'address_match_percent_list': None}

        here_latitude = extract_element_from_json(here_json, ["payload", "response", "view", "result", "location",
                                                              "displayPosition", "latitude"])
        here_longitude = extract_element_from_json(here_json, ["payload", "response", "view", "result", "location",
                                                               "displayPosition", "longitude"])
        #         here_matchQuality=extract_element_from_json(hg, ["Response", "View","Result","MatchQuality"])
        here_matchLevel = extract_element_from_json(here_json, ["payload", "response", "view", "result", "matchLevel"])

        if here_latitude[0] == None and google_latitude[0] == None:
            return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                    'lat_long_precision': 'both_not_extracted', 'Refer_flag': True, 'scenario': 'MN_1',
                    'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
        elif google_latitude[0] == None:
            here_matchLevel_order = here_granular_type.get(here_matchLevel[0])
            msg = msg_header + 'HERE matchLevel order: ' + str(here_matchLevel_order)
            logger.debug('%s', msg)
            if here_matchLevel_order == 1:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'High',
                        'Refer_flag': False, 'scenario': 'MN_2', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif here_matchLevel_order == 2:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Medium',
                        'Refer_flag': False, 'scenario': 'MN_3', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif here_matchLevel_order == 3:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Low',
                        'Refer_flag': True, 'scenario': 'MN_4', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                        'address_match_percent_list': None}
            else:
                return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Too Low',
                        'Refer_flag': True, 'scenario': 'MN_5', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                        'address_match_percent_list': None}
        elif here_latitude[0] == None:
            granular_common_elements = list(set(google_types[0]).intersection(set(google_granular_type_list)))
            msg = msg_header + 'Google granular elements: ' + str(granular_common_elements)
            logger.debug('%s', msg)
            granular_common_elements_order = [google_granular_type.get(i) for i in granular_common_elements]
            msg = msg_header + 'Google granular elements order: ' + str(granular_common_elements_order)
            logger.debug('%s', msg)
            if min(granular_common_elements_order) == 1:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0], 'lat_long_precision': 'High',
                        'Refer_flag': False, 'scenario': 'MN_6', 'pincode_match': 'Not Applicable',
                        'rev_geo_json': None, 'address_match_percent_list': None}
            elif min(granular_common_elements_order) == 2:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                        'lat_long_precision': 'Medium', 'Refer_flag': False, 'scenario': 'MN_7',
                        'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
            elif min(granular_common_elements_order) == 3:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0], 'lat_long_precision': 'Low',
                        'Refer_flag': True, 'scenario': 'MN_8', 'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                        'address_match_percent_list': None}
            else:
                return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                        'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MN_9',
                        'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
        else:
            here_matchLevel_order = here_granular_type.get(here_matchLevel[0])
            msg = msg_header + 'HERE matchLevel order: ' + str(here_matchLevel_order)
            logger.debug('%s', msg)
            granular_common_elements = list(set(google_types[0]).intersection(set(google_granular_type_list)))
            msg = msg_header + 'Google granular elements: ' + str(granular_common_elements)
            logger.debug('%s', msg)
            granular_common_elements_order = [google_granular_type.get(i) for i in granular_common_elements]
            msg = msg_header + 'Google granular elements order: ' + str(granular_common_elements_order)
            logger.debug('%s', msg)

            here = list([here_latitude[0], here_longitude[0]])  # give here column name
            goog = list([google_latitude[0], google_longitude[0]])  # give google column name
            distance_between_coordinates = distance.distance(here, goog).m
            msg = msg_header + 'Distance between coordinates: ' + str(distance_between_coordinates)
            logger.debug('%s', msg)

            if here_matchLevel_order <= 2 and min(granular_common_elements_order) <= 2:
                # both are granular
                if min(granular_common_elements_order) == 1 and distance_between_coordinates <= 500:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'Highest', 'Refer_flag': False, 'scenario': 'MN_10',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                elif here_matchLevel_order == 1 and distance_between_coordinates <= 500:
                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                            'lat_long_precision': 'Highest', 'Refer_flag': False, 'scenario': 'MN_11',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                elif min(
                        granular_common_elements_order) == 2 and here_matchLevel_order == 2 and distance_between_coordinates <= 500:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MN_12',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                elif distance_between_coordinates > 500:
                    if min(granular_common_elements_order) == 1:
                        return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MN_13',
                                'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                                'address_match_percent_list': None}
                    elif here_matchLevel_order == 1:
                        return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                                'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MN_14',
                                'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                                'address_match_percent_list': None}
                    else:
                        return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MN_15',
                                'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                                'address_match_percent_list': None}
            elif here_matchLevel_order > 2 and min(granular_common_elements_order) > 2:
                # both are non granular
                if here_matchLevel_order == 4 and min(granular_common_elements_order) == 4:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MN_16',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                elif min(granular_common_elements_order) == 4:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MN_17',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                elif here_matchLevel_order == 4:
                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0],
                            'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MN_18',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                else:
                    if distance_between_coordinates > 500:
                        return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                'lat_long_precision': 'Too Low', 'Refer_flag': True, 'scenario': 'MN_19',
                                'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                                'address_match_percent_list': None}
                    else:
                        return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                                'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MN_20',
                                'pincode_match': 'Not Applicable', 'rev_geo_json': None,
                                'address_match_percent_list': None}
            elif here_matchLevel_order <= 2:
                # only here is granular
                if distance_between_coordinates <= 500:
                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'High',
                            'Refer_flag': False, 'scenario': 'MN_21', 'pincode_match': 'Not Applicable',
                            'rev_geo_json': None, 'address_match_percent_list': None}
                else:
                    return {'latitude': here_latitude[0], 'longitude': here_longitude[0], 'lat_long_precision': 'Low',
                            'Refer_flag': False, 'scenario': 'MN_22', 'pincode_match': 'Not Applicable',
                            'rev_geo_json': None, 'address_match_percent_list': None}
            elif min(granular_common_elements_order) <= 2:
                # only google is granular
                if distance_between_coordinates <= 500:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'High', 'Refer_flag': False, 'scenario': 'MN_23',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
                else:
                    return {'latitude': google_latitude[0], 'longitude': google_longitude[0],
                            'lat_long_precision': 'Low', 'Refer_flag': False, 'scenario': 'MN_24',
                            'pincode_match': 'Not Applicable', 'rev_geo_json': None, 'address_match_percent_list': None}
    except Exception as e:
        logger.exception("Exception occurred in MULITPLE NO")


def get_latlong(request_json):
    input_json = request_json
    Pincode = input_json.get('pincode')
    City = input_json.get('city')
    State = input_json.get('state')
    Full_Address = input_json.get('full_addr')
    geocode_api = input_json.get('geocode_api')
    rev_geocode = input_json.get('rev_geocode')
    appl_id = input_json.get('appl_id')
    req_id = input_json.get('req_id')
    inst_name = input_json.get('inst_name')
    src_sys_name = input_json.get('src_sys_name')
    product = input_json.get('product')
    '''
    Field names in the json
    inst_id
    appl_id
    appl_type
    co_appl_no
    geocode_api
    addr_type
    src_sys_id
    addr_src
    pincode
    city
    state
    full_addr
    req_dttm
    addr_qty
    rev_geocode
    req_id
    auto_query
    addr_id
    lnd_mrk
    '''
    msg_header = 'Applicant Id: ' + str(appl_id) + ' ' + 'Request Id: ' + str(req_id) + ' Message: '
    if geocode_api.upper() == 'GOOG' and rev_geocode == True:
        msg = msg_header + 'Google Yes initiated'
        logger.debug('%s', msg)
        response_json = get_lat_long_google_yes(Pincode, City, State, Full_Address, appl_id, req_id, inst_name,
                                                src_sys_name, product)
        msg = msg_header + 'Google Yes completed'
        logger.debug('%s', msg)
    elif geocode_api.upper() == 'GOOG' and rev_geocode == False:
        msg = msg_header + 'Google No initiated'
        logger.debug('%s', msg)
        response_json = get_lat_long_google_no(Pincode, City, State, Full_Address, appl_id, req_id, inst_name,
                                               src_sys_name, product)
        msg = msg_header + 'Google No completed'
        logger.debug('%s', msg)
    elif geocode_api.upper() == 'HERE' and rev_geocode == True:
        msg = msg_header + 'HERE Yes initiated'
        logger.debug('%s', msg)
        response_json = get_lat_long_here_yes(Pincode, City, State, Full_Address, appl_id, req_id, inst_name,
                                              src_sys_name, product)
        msg = msg_header + 'HERE Yes completed'
        logger.debug('%s', msg)
    elif geocode_api.upper() == 'HERE' and rev_geocode == False:
        msg = msg_header + 'HERE No initiated'
        logger.debug('%s', msg)
        response_json = get_lat_long_here_no(Pincode, City, State, Full_Address, appl_id, req_id, inst_name,
                                             src_sys_name, product)
        msg = msg_header + 'HERE No completed'
        logger.debug('%s', msg)
    elif geocode_api.upper() == 'MULT' and rev_geocode == True:
        msg = msg_header + 'Multiple Yes initiated'
        logger.debug('%s', msg)
        response_json = get_lat_long_multiple_yes(Pincode, City, State, Full_Address, appl_id, req_id, inst_name,
                                                  src_sys_name, product)
        msg = msg_header + 'Multiple Yes completed'
        logger.debug('%s', msg)
    elif geocode_api.upper() == 'MULT' and rev_geocode == False:
        msg = msg_header + 'Multiple No initiated'
        logger.debug('%s', msg)
        response_json = get_lat_long_multiple_no(Pincode, City, State, Full_Address, appl_id, req_id, inst_name,
                                                 src_sys_name, product)
        msg = msg_header + 'Multiple No completed'
        logger.debug('%s', msg)
    msg = msg_header + 'Response to be returned: ' + str(response_json)
    logger.debug('%s', msg)
    if response_json != None:
        keys = ['latitude', 'longitude', 'lat_long_precision', 'Refer_flag', 'pincode_match']
        response_to_return = {key: response_json[key] for key in keys}
        return response_to_return
    else:
        return response_json
    # return response_json


'''
import pandas as pd
data=pd.read_csv('../DPL_vijay_data_with_algo_results_complete_to_share_final.csv')
print(data.shape)

print(data.columns)

data.reset_index(drop=True,inplace=True)

data_to_store=pd.DataFrame()
for i in range(0,10):
    list1=[]
    full_addr=str(data.iloc[i,:]['Address'])
    pincode=data.iloc[i,:]['Residence Pin Code']
    city=str(data.iloc[i,:]['Residence City'])
    state=' '
    req_id='123456'
    appl_id=str(data.iloc[i,:]['Application ID'])
    geocode_api='MULT'
    rev_geocode=True
    request_json={'full_addr':full_addr,'pincode':pincode,'city':city,'state':state,'req_id':req_id,'appl_id':appl_id,
     'geocode_api':geocode_api,'rev_geocode':rev_geocode}
    
    response=get_latlong(request_json)
    if response!=None:
        list1.append(data.iloc[i,:]['Application ID'])
        list1.append(response.get('latitude'))
        list1.append(response.get('longitude'))
        list1.append(response.get('lat_long_precision'))
        list1.append(response.get('Refer_flag'))
        list1.append(response.get('scenario'))
        list1.append(response.get('pincode_match'))
        list1.append(response.get('rev_geo_json'))
        list1.append(response.get('address_match_percent_list'))
        inter=pd.DataFrame(np.array(list1).reshape(1,-1))
        data_to_store=pd.concat([data_to_store,inter])
    print(i,' completed')
data_to_store.columns=['Application ID','latitude','longitude',\
                       'lat_long_precision','Refer_flag','scenario',\
                           'pincode_match','rev_geo_json','address_match_percent_list']
'''
