import requests
import router_config
import logging
from logging.handlers import TimedRotatingFileHandler


def geo_code_request(payload_dict):
    logger = logging.getLogger('geo_code')
    logging.basicConfig(level=logging.DEBUG, filemode='a')
    log_format = '%(asctime)s - %(lineno)d - %(levelname)s - %(message)s'

    logfilename = "geo_code.log"
    handler = TimedRotatingFileHandler(logfilename, when="midnight", interval=1)
    handler.suffix = "%Y%m%d"
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    google_geocoding_json = None
    here_geocoding_json = None
    google_reverse_geocoding_json = None
    here_reverse_geocoding_json = None

    try:
        if payload_dict.get('geocoding_api') == 'GOOG' or payload_dict.get('geocoding_api') == 'MULT':
            url = router_config.ssl_google_geocoding_url

            PARAMS = {
                'address': payload_dict.get('address'),
                'components': 'country:IN|postal_code:' + str(payload_dict.get('pincode'))
            }
            HEADERS = {
                'sApplicationId': payload_dict.get('appl_id'),
                'sInstituteName': payload_dict.get('inst_name'),
                'sLoginId': 'HDBFS_SSL_USER',
                'sPassword': '16f4c0d64a212664173e120376b639e7c004d31e',
                'sProduct': payload_dict.get('product'),
                'sSourceSystem': payload_dict.get('src_sys_name')
            }

            response = requests.get(url, params=PARAMS, headers=HEADERS)
            google_geocoding_json=response.json()
            
        if payload_dict.get('geocoding_api') == 'HERE' or payload_dict.get('geocoding_api') == 'MULT':
            url = router_config.ssl_here_geocoding_url

            PARAMS = {
                'searchtext': payload_dict.get('address'),
                'state': payload_dict.get('state'),
                'postalcode': str(payload_dict.get('pincode')),
                'gen': 9,
                'country': 'IND',
                'city': payload_dict.get('pincode')
            }
            HEADERS = {
                'sApplicationId': payload_dict.get('appl_id'),
                'sInstituteName': payload_dict.get('inst_name'),
                'sLoginId': 'HDBFS_SSL_USER',
                'sPassword': '16f4c0d64a212664173e120376b639e7c004d31e',
                'sProduct': payload_dict.get('product'),
                'sSourceSystem': payload_dict.get('src_sys_name')
            }
            response = requests.get(url, params=PARAMS, headers=HEADERS)
            here_geocoding_json = response.json()

        if payload_dict.get('reverse_geocoding_api') == 'GOOG' or payload_dict.get('reverse_geocoding_api') == 'MULT':
            url = router_config.ssl_google_reverse_geocoding_url

            PARAMS = {
                'latlng': str(payload_dict.get('here_latitude')) + ',' + str(payload_dict.get('here_longitude'))
            }
            HEADERS = {
                'sApplicationId': payload_dict.get('appl_id'),
                'sInstituteName': payload_dict.get('inst_name'),
                'sLoginId': 'HDBFS_SSL_USER',
                'sPassword': '16f4c0d64a212664173e120376b639e7c004d31e',
                'sProduct': payload_dict.get('product'),
                'sSourceSystem': payload_dict.get('src_sys_name')
            }

            response = requests.get(url, params=PARAMS, headers=HEADERS)
            google_reverse_geocoding_json = response.json()
            
        if payload_dict.get('reverse_geocoding_api') == 'HERE' or payload_dict.get('reverse_geocoding_api') == 'MULT':
            url = router_config.ssl_here_reverse_geocoding_url
            PARAMS = {
                'mode': 'retrieveAddresses',
                'level': 'postalCode',
                'prox': str(payload_dict.get('google_latitude')) + ',' + str(payload_dict.get('google_longitude')) + ',5',
                'gen': 9
            }
            HEADERS = {
                'sApplicationId': payload_dict.get('appl_id'),
                'sInstituteName': payload_dict.get('inst_name'),
                'sLoginId': 'HDBFS_SSL_USER',
                'sPassword': '16f4c0d64a212664173e120376b639e7c004d31e',
                'sProduct': payload_dict.get('product'),
                'sSourceSystem': payload_dict.get('src_sys_name')
            }
            response = requests.get(url, params=PARAMS, headers=HEADERS)
            here_reverse_geocoding_json = response.json()
            
        return {
            'google_geocoding_json': google_geocoding_json,
            'here_geocoding_json': here_geocoding_json,
            'google_reverse_geocoding_json': google_reverse_geocoding_json,
            'here_reverse_geocoding_json': here_reverse_geocoding_json
        }

    except Exception as e:
        logger.exception('Exception occurred in SSL side')
        return {
            'google_geocoding_json': {'Results': None},
            'here_geocoding_json': {'Results': None},
            'google_reverse_geocoding_json': {'Results': None},
            'here_reverse_geocoding_json': {'Results': None}
        }
