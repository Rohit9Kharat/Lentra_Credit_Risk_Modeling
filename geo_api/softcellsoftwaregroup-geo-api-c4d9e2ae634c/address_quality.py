import re
import pandas as pd
from collections import OrderedDict


def city_state_count(address_field_city_state, count, loc, c_s):
    first_half_of_address = address_field_city_state[0:loc]
    second_half_of_address = address_field_city_state[loc:]
    new_address = second_half_of_address[(len(c_s) * count) - len(c_s):]
    new_address_field = first_half_of_address + new_address
    return new_address_field


def address_quality(request_json):
    address_field = request_json.get('full_addr')
    pincode = request_json.get('pincode')
    if pincode is not None:
        pincode = str(pincode)
    city = request_json.get('city')
    state = request_json.get('state')
    landmark = request_json.get('lnd_mrk')

    address_field = " ".join(address_field.replace(',', ' ').split(' '))  # remove commas

    pincode_in_address = re.findall(r'\d{6}', address_field)
    if len(pincode_in_address) != 0:  # if pincode present in the address then replace it with ""
        address_field = address_field.replace(pincode_in_address[0], "")

    if pincode is None and not pincode_in_address:
        is_pincode_missing = 1  # field absent full_addr absent
    # checking if pincode is missing in the given address
    elif pincode is None and pincode_in_address:
        is_pincode_missing = 2  # field absent full_addr present
    elif pincode is not None and not pincode_in_address:
        is_pincode_missing = 3  # field present full_addr absent
    elif pincode is not None and pincode_in_address:
        is_pincode_missing = 4  # present in both

    if pincode is None:
        is_pincode_matching = None  # default
    # checking if pincode is matching with the pincode given in address or not
    elif pincode_in_address:
        if pincode_in_address[0] == pincode:
            is_pincode_matching = True  # yes
        else:
            is_pincode_matching = False  # no
    else:
        is_pincode_matching = None  # default

    if city is None:
        is_city_matching = None  # default
    # checking if city is matching with the city given in address.
    elif city in address_field:
        is_city_matching = True  # yes
    else:
        is_city_matching = False  # No

    if state is None:
        is_state_matching = None  # default
    # checking if state is matching with the state given in address.
    elif state in address_field:
        is_state_matching = True  # yes
    else:
        is_state_matching = False  # No


    if city and state is not None:
        # This is done incase city or state are appearing multiple times in the address in the format (e.g : PUNEPUNE )
        city_count = address_field.count(city)
        city_loc = address_field.find(city)
        state_count = address_field.count(state)
        state_loc = address_field.find(state)

        if (city in address_field) or (state in address_field):
            address_field = city_state_count(address_field, city_count, city_loc, city)
            address_field = city_state_count(address_field, state_count, state_loc, state)

        address_field = ' '.join(OrderedDict((w, w) for w in address_field.upper().split()).keys())  # remove duplicates

        # if city or state is not present in given addres then append city or state to the address
        if not bool(re.search(city, address_field, re.IGNORECASE)) and not bool(
                re.search(state, address_field, re.IGNORECASE)):
            address_field = address_field + " " + city + " " + state
        elif not bool(re.search(city, address_field, re.IGNORECASE)) and bool(
                re.search(state, address_field, re.IGNORECASE)):
            address_field = address_field + " " + city
        elif bool(re.search(city, address_field, re.IGNORECASE)) and not bool(
                re.search(state, address_field, re.IGNORECASE)):
            address_field = address_field + " " + state

    # list_of_keywords = ['NAGAR', 'COLONY', 'GALI', 'COMPLEX', 'GALLI', 'AREA', 'ROAD', 'LANE', 'VILLAGE', \
    #                     'MOHALLA', 'MOHALA', 'ZONE', 'PLOT', 'BUILDING', 'SECTOR', 'PHASE', 'CHOWKI', 'CHOKI', \
    #                     'SOCIETY', 'BLOCK', 'DOOR', 'HOUSE', 'FLAT', 'CHOWK', 'LAYOUT', 'STREET', 'ST', 'GULLI', 'PO', \
    #                     'TOWNSHIP', 'WARD', 'BASTI', 'H NO', 'HNO', 'H.NO.', 'FLOOR', 'FLR', 'HALLI', 'ROOM', 'POST']

    list_of_keywords = pd.read_csv('resources/keyword_list.csv')

    # print(list_of_keywords['keyword'].values.tolist())
    # print(len(list_of_keywords.index))
    # print(landmark)
    # print(landmark.split())

    if landmark is None:
        is_landmark_matching = None  # default
    elif any(x in list_of_keywords['keyword'].values.tolist() for x in landmark.upper().split()):
        is_landmark_matching = True  # Yes
    else:
        is_landmark_matching = False  # No

    # if any([x in address_field.upper() for x in list_of_keywords]):
    if any(x in list_of_keywords['keyword'].values.tolist() for x in address_field.upper().split()):
        is_keyword_missing = False  # No
    else:
        is_keyword_missing = True  # Yes

    address_field = re.sub('[^a-zA-Z0-9 \n\.]', "", address_field).replace('.', '').replace(' ',
                                                                                            '')  # remove special characters
    # check if any number is present in the address
    if bool(re.search('\d', address_field)):
        is_number_missing = False  # No
    else:
        is_number_missing = True  # Yes

    # check length of the address
    address_length = 0
    if len(address_field) <= 21:
        address_length = 1  # '<=21'
        length_adr = True
    elif 21 < len(address_field) < 26:
        address_length = 2  # '22-25'
        length_adr = False
    elif 25 < len(address_field) < 31:
        address_length = 3  # '26-30'
        length_adr = False
    elif 30 < len(address_field) < 36:
        address_length = 4  # '31-35'
        length_adr = False
    elif len(address_field) > 35:
        address_length = 5  # '>35'
        length_adr = False

    if is_number_missing and length_adr:
        address_semantic_score = 1  # 'LOW'
    elif not is_number_missing and not length_adr:
        address_semantic_score = 3  # 'HIGH'
    else:
        address_semantic_score = 2  # 'MEDIUM'

    return({
        'pincode_missing': is_pincode_missing, 'pincode_matching': is_pincode_matching,
        'city_matching': is_city_matching, 'state_matching': is_state_matching,
        'address_semantic_score': address_semantic_score
    })
