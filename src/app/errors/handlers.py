import logging
from flask import request, jsonify
from werkzeug.http import HTTP_STATUS_CODES
from app.errors import bp


def json_error_response(status_code, message=None):
    """Generates json payload with error code"""
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def json_response_preferred():
    """Whether json response is preferred based on request parameters"""
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


@bp.app_errorhandler(401)
def unauthorized_request_status(error):
    """Generates 401 error json response"""
    error_data = {"url": request.url, "data": error, "code": 401}
    logging.error(error_data)
    return json_error_response(401)


@bp.app_errorhandler(403)
def unauthorized_content_error(error):
    """Generates 403 error json response"""
    error_data = {"url": request.url, "data": error, "code": 403}
    logging.error(error_data)
    return json_error_response(403)


@bp.app_errorhandler(404)
def not_found_error(error):
    """Generates 404 error json response"""
    error_data = {"url": request.url, "data": error, "code": 404}
    logging.error(error_data)
    return json_error_response(404)


@bp.app_errorhandler(500)
def internal_error(error):
    """Generates 500 error json response"""
    error_data = {"url": request.url, "data": error, "code": 500}
    logging.error(error_data)
    return json_error_response(500)
