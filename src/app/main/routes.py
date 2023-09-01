import flask


from flask import render_template, redirect, url_for, request, current_app, jsonify, flash
from app.main import bp
from app.main.routes_helpers import json_response, request_mirror, app_time, request_log


@bp.route('/', methods=['GET'])
def home():
    data = {"name": current_app.config.get('APP_NAME'), "ver": current_app.config.get('APP_VER')}
    return json_response(payload=data)


@bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    data = {"status": "OK"}
    return json_response(payload=data)


@bp.route('/redirect', methods=['GET'])
def redirect():
    data = {"status": "OK"}
    # Redirects to home location(relative URL)
    # url_for(bp.name + '.home')
    return json_response(status_code=302, payload=data, location=url_for(bp.name + '.home'))


@bp.route('/stamp', methods=['GET'])
def stamp():
    # Add a stamp cookie
    data = {"status": "OK"}
    stamp_cookie_key = current_app.config.get('STAMP_COOKIE_KEY')
    stamp_cookie_value = current_app.config.get('STAMP_COOKIE_VALUE')
    return json_response(payload=data, cookie_list=[{stamp_cookie_key: stamp_cookie_value}])


@bp.route('/mirror', methods=['GET'])
def mirror():
    data = request_mirror(raw_request=request)
    return json_response(payload=data)


@bp.route('/ctime', methods=['GET'])
def ctime():
    data = app_time()
    return json_response(payload=data)


@bp.before_request
def before_request():
    request_log(request)
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
