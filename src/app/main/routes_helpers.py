"""Helper functions for Flask module routes: main"""

import datetime
import logging


from flask import request, current_app, jsonify


def filler(num):
    """Fill with num *"""
    return '*' * num


def json_response_preferred():
    """Fill with num *"""
    return current_app.config.get('JSON_PREFERRED') or \
           request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


# Generates a json response
# HTTP 200 by default
# Certain json payload by default
# If cookies provided (list of dicts with one key and one value),
# all valid cookies are included in the response
def json_response(status_code=200, payload=None, location=None, cookie_list=None):
    """Whether json response is preferred based on request parameters"""
    if payload is None:
        payload = {"status": "OK"}
    response = jsonify(payload)
    response.status_code = status_code
    if location:
        response.location = location

    # cookie_list must be a list of dicts,  with one key and valid value each
    # isinstance also returns False if first element is None
    if isinstance(cookie_list, list):
        for include_cookie in cookie_list:
            # include_cookie must be a dict with one key and valid value
            if isinstance(include_cookie, dict):
                if include_cookie.keys().__len__() == 1:
                    cookie_key = set(include_cookie.keys()).pop()
                    cookie_value = include_cookie.get(cookie_key)
                    if cookie_value:
                        response.set_cookie(key=cookie_key, value=cookie_value)
    return response


def non_empty_kv(sparse_dict):
    """Extract only keys with a value"""
    if isinstance(sparse_dict, dict):
        h = {}
        for key in sparse_dict.keys():
            if sparse_dict.get(key) is not None:
                h[key] = sparse_dict.get(key)
        return h


def print_dict(input_dict):
    """Extract only keys with a value and returns a json string representation """
    if isinstance(input_dict, dict):
        h = non_empty_kv(input_dict)
        r = ""
        for key in h.keys():
            r = r + f'<{key}:  {h[key]}>\n'
        return r


# Default log level: INFO
def response_log(raw_response, raw_request, log_level=logging.INFO):
    """Logs response to standard logging"""

    response_simple_log_str = \
        f'Outgoing RESPONSE to ' \
        f'{raw_request.__hash__()}{filler(30)}\nStatus: {raw_response.status_code}'+\
                              f'\nHeaders:' \
                              f'\n{print_dict(raw_response.headers)}\nData\n:{raw_response.data}' + \
                              f'\nLocation: ' \
                              f'{raw_response.location}\nContent Type: {raw_response.content_type}'
    logging.log(level=log_level, msg=response_simple_log_str)


# Default log level: INFO
def request_log(raw_request, log_level=logging.INFO):
    """Logs request to standard logging"""
    request_simple_log_str = f'Incoming REQUEST {raw_request.__hash__()} {filler(30)}' + \
                             f'\nPath: {raw_request.path}\nServer: {request.server}' + \
                             f'\nMethod: {raw_request.method}\nOrigin: {request.origin}' + \
                             f'\nQuery: {raw_request.query_string}' + \
                             f'\nHeaders:\n{print_dict(raw_request.headers)}'
    logging.log(level=log_level, msg=request_simple_log_str)


def headers_to_dict(raw_request):
    """Request headers to dictionary representation"""
    headers = raw_request.headers.to_wsgi_list()
    h = {}
    for header in headers:
        h.update({header[0]: header[1]})
    return h


def request_mirror(raw_request):
    """Return request info formatted as a dictionary"""
    request_image = {}
    request_image.update({'0_id': f'{raw_request.__hash__()}'})
    request_image.update({'1_server': raw_request.server})
    request_image.update({'2_path': raw_request.path})
    request_image.update({'3_method': raw_request.method})
    request_image.update({'5_headers': headers_to_dict(raw_request=raw_request)})
    request_image.update({'6_cookies': request.cookies.to_dict()})

    return request_image


def app_time():
    """Return app time info formatted as a dictionary"""
    data = {"status": "OK"}
    data.update({"now_utc_iso": datetime.datetime.utcnow().isoformat()})
    data.update({"now_utc_timestamp": datetime.datetime.utcnow().timestamp().__str__()})
    return data
