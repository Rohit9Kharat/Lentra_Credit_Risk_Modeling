import re
import router_config
from flask import Flask, jsonify, abort, request, make_response
from string import punctuation
from address_quality import address_quality
from geo_code import get_latlong


app = Flask(__name__)


@app.errorhandler(405)
def method_not_allowed(e):
    return make_response(jsonify(error=405, text=str(e)), 405)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify(error=404, text=str(e)), 404)


@app.errorhandler(500)
def internal_server_error(e):
    return make_response(jsonify(error=500, text=str(e)), 500)


@app.errorhandler(400)
def page_not_found(e):
    return make_response(jsonify(error_code=400,
                                 text='The browser (or proxy) sent a request that this server could not understand.',
                                 error=str(e)), 400)


@app.route('/geo-code', methods=['POST'])
def geo_code_response():
    error_check(request.json)
    get_ids(request.json)

    if 'geocode_api' not in request.json:
        abort(400, 'geocode_api_missing')
    if 'addr_qty' not in request.json:
        abort(400, 'addr_qty_missing')
    if 'rev_geocode' not in request.json:
        abort(400, 'rev_geocode_missing')
    if 'auto_query' not in request.json:
        abort(400, 'quto_query_missing')

    geocode_api = request.json.get('geocode_api')
    addr_qty = request.json.get('addr_qty')
    rev_geocode = request.json.get('rev_geocode')
    auto_query = request.json.get('auto_query')

    if not isinstance(geocode_api, str):
        abort(400, 'geocode_api_bad_type')
    if not isinstance(addr_qty, bool):
        abort(400, 'addr_qty_bad_type')
    if not isinstance(rev_geocode, bool):
        abort(400, 'rev_geocode_bad_type')
    if not isinstance(auto_query, bool):
        abort(400, 'auto_query_bad_type')

    if len(geocode_api) == 0 or geocode_api.isspace():
        abort(400, 'geocode_api_blank')

    if geocode_api.upper() not in router_config.geocode_api_list:
        abort(400, 'appl_type_bad_value')

    if addr_qty:
        addr_qty_return = address_quality(request.json)

        addr_sem_scr = addr_qty_return.get('address_semantic_score')
        city_match = addr_qty_return.get('city_matching')
        pincode_match = addr_qty_return.get('pincode_matching')
        pincode_miss = addr_qty_return.get('pincode_missing')
        state_match = addr_qty_return.get('state_matching')

        if (addr_sem_scr == 1) or (pincode_match is False) or (city_match is False) or (state_match is False) or (pincode_miss == 1):
            addr_qty_return['bad_qty_refer'] = True
            addr_qty_return['appl_id'] = request.json.get('appl_id')
            addr_qty_return['res_id'] = request.json.get('req_id')
            return jsonify(addr_qty_return)
        else:
            response = get_latlong(request.json)
            response['bad_qty_refer'] = False
            response['appl_id'] = request.json.get('appl_id')
            response['res_id'] = request.json.get('req_id')
            return jsonify(response)

    response = get_latlong(request.json)
    response['appl_id'] = request.json.get('appl_id')
    response['res_id'] = request.json.get('req_id')
    return jsonify(response)


@app.route('/addr-qual', methods=['POST'])
def addr_qual_response():
    error_check(request.json)
    get_ids(request.json)
    response = address_quality(request.json)
    response['appl_id'] = request.json.get('appl_id')
    response['res_id'] = request.json.get('req_id')
    return jsonify(response)


def error_check(request_json):
    utc = re.compile(r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}Z$')

    if 'inst_name' not in request_json:
        abort(400, 'inst_name_missing')
    if 'appl_id' not in request_json:
        abort(400, 'appl_id_missing')
    if 'appl_type' not in request_json:
        abort(400, 'appl_type_missing')
    if 'co_appl_no' not in request_json:
        abort(400, 'co_appl_no_missing')
    if 'addr_type' not in request_json:
        abort(400, 'addr_type_missing')
    if 'src_sys_name' not in request_json:
        abort(400, 'src_sys_name_missing')
    if 'addr_src' not in request_json:
        abort(400, 'addr_src_missing')
    if 'pincode' not in request_json:
        abort(400, 'pincode_missing')
    if 'city' not in request_json:
        abort(400, 'city_missing')
    if 'state' not in request_json:
        abort(400, 'state_missing')
    if 'lnd_mrk' not in request_json:
        abort(400, 'lnd_mrk_missing')
    if 'full_addr' not in request_json:
        abort(400, 'full_addr_missing')
    if 'req_dttm' not in request_json:
        abort(400, 'req_dttm_missing')
    if 'req_id' not in request_json:
        abort(400, 'req_id_missing')
    if 'addr_id' not in request_json:
        abort(400, 'addr_id_missing')
    if 'product' not in request_json:
        abort(400, 'product_missing')

    inst_name = request_json.get('inst_name')
    appl_id = request_json.get('appl_id')
    appl_type = request_json.get('appl_type')
    co_appl_no = request_json.get('co_appl_no')
    addr_type = request_json.get('addr_type')
    src_sys_name = request_json.get('src_sys_name')
    addr_src = request_json.get('addr_src')
    pincode = request_json.get('pincode')
    city = request_json.get('city')
    state = request_json.get('state')
    lnd_mrk = request_json.get('lnd_mrk')
    full_addr = request_json.get('full_addr')
    req_dttm = request_json.get('req_dttm')
    req_id = request_json.get('req_id')
    addr_id = request_json.get('addr_id')
    product = request_json.get('product')

    if not isinstance(inst_name, str):
        abort(400, 'inst_name_bad_type')
    if not isinstance(appl_id, str):
        abort(400, 'appl_id_bad_type')
    if not isinstance(appl_type, str):
        abort(400, 'appl_type_bad_type')
    if not isinstance(co_appl_no, int):
        abort(400, 'co_appl_no_bad_type')
    if not isinstance(addr_type, str):
        abort(400, 'addr_type_bad_type')
    if not isinstance(src_sys_name, str):
        abort(400, 'src_sys_name_bad_type')
    if not isinstance(addr_src, str):
        abort(400, 'addr_src_bad_type')
    if pincode is not None and not isinstance(pincode, int):
        abort(400, 'pincode_bad_type')
    if city is not None and not isinstance(city, str):
        abort(400, 'city_bad_type')
    if state is not None and not isinstance(state, str):
        abort(400, 'state_bad_type')
    if lnd_mrk is not None and not isinstance(lnd_mrk, str):
        abort(400, 'lnd_mrk_bad_type')
    if not isinstance(full_addr, str):
        abort(400, 'full_addr_bad_type')
    if not isinstance(req_dttm, str):
        abort(400, 'req_dttm_bad_type')
    if not isinstance(req_id, str):
        abort(400, 'req_id_bad_type')
    if addr_id is not None and not isinstance(addr_id, int):
        abort(400, 'addr_id_bad_type')
    if not isinstance(product, str):
        abort(400, 'product_bad_type')

    if len(inst_name) == 0 or inst_name.isspace():
        abort(400, 'inst_name_blank')
    if len(appl_id) == 0 or appl_id.isspace():
        abort(400, 'appl_id_blank')
    if len(appl_type) == 0 or appl_type.isspace():
        abort(400, 'appl_type_blank')
    if len(addr_type) == 0 or addr_type.isspace():
        abort(400, 'addr_type_blank')
    if len(src_sys_name) == 0 or src_sys_name.isspace():
        abort(400, 'src_sys_name_blank')
    if len(addr_src) == 0 or addr_src.isspace():
        abort(400, 'addr_src_blank')
    if city is not None and (len(city) == 0 or city.isspace()):
        abort(400, 'city_blank')
    if state is not None and (len(state) == 0 or state.isspace()):
        abort(400, 'state_blank')
    if lnd_mrk is not None and (len(lnd_mrk) == 0 or lnd_mrk.isspace()):
        abort(400, 'lnd_mrk_blank')
    if len(full_addr) == 0 or full_addr.isspace():
        abort(400, 'full_addr_blank')
    if len(req_dttm) == 0 or req_dttm.isspace():
        abort(400, 'req_dttm_blank')
    if len(req_id) == 0 or req_id.isspace():
        abort(400, 'req_id_blank')
    if len(product) == 0 or product.isspace():
        abort(400, 'product_blank')

    if inst_name.upper() not in router_config.inst_id_map:
        abort(400, 'inst_name_bad_value')
    if len(set(punctuation).intersection(set(appl_id))) != 0:
        abort(400, 'appl_id_bad_value')
    if appl_type.upper() not in router_config.appl_type_list:
        abort(400, 'appl_type_bad_value')
    if (appl_type.upper() == 'PRI' and co_appl_no != 0) or (appl_type.upper() == 'SEC' and co_appl_no <= 0):
        abort(400, 'co_appl_no_bad_value')
    if addr_type.upper() not in router_config.addr_type_list:
        abort(400, 'addr_type_bad_value')
    if src_sys_name.upper() not in router_config.src_sys_id_map:
        abort(400, 'src_sys_name_bad_value')
    if addr_src.upper() not in router_config.addr_src_list:
        abort(400, 'addr_src_bad_value')
    if pincode is not None and len(str(pincode)) != 6:
        abort(400, 'pincode_bad_value')
    if city is not None and (not re.search('[a-zA-Z]', city) or len(set(punctuation).intersection(set(city))) != 0):
        abort(400, 'city_bad_value')
    if state is not None and (not re.search('[a-zA-Z]', state) or len(set(punctuation).intersection(set(state))) != 0):
        abort(400, 'state_bad_value')
    if lnd_mrk is not None and (not re.search('[a-zA-Z]', lnd_mrk)):
        abort(400, 'lnd_mrk_bad_value')
    if not re.search('[a-zA-Z]', full_addr):
        abort(400, 'full_addr_bad_value')
    if not bool(utc.search(req_dttm)):
        abort(400, 'req_dttm_bad_value')
    if not len(req_id) <= 26 or len(set(punctuation).intersection(set(req_id))) != 0:
        abort(400, 'req_id_bad_value')
    if not re.search('[a-zA-Z]', product) or len(set(punctuation).intersection(set(product))) != 0:
        abort(400, 'product_bad_value')


def get_ids(request_json):
    inst_name = request_json.get('inst_name')
    src_sys_name = request_json.get('src_sys_name')

    inst_id = router_config.inst_id_map.get(inst_name)
    src_sys_id = router_config.src_sys_id_map.get(src_sys_name)

    request_json['inst_id'] = inst_id
    request_json['src_sys_id'] = src_sys_id
    return request_json
