import os
import base64


class Config:

    # App name for HTML views, it appears on titles, links, etc.
    APP_NAME = os.environ.get('APP_NAME') or 'py-holder-demo'
    APP_VER = os.environ.get('APP_VER') or '1.0'
    STAMP_COOKIE_KEY = os.environ.get('STAMP_COOKIE_KEY') or 'x-stamp'
    STAMP_COOKIE_VALUE = os.environ.get('STAMP_COOKIE_VALUE') \
                         or base64.urlsafe_b64encode(APP_NAME.encode())

    # Flask config
    # Recommended generating key before running server
    # export FLASK_KEY_LOG=/secrets_storage_path/flask_secret_key.log
    # export  FLASK_SECRET_KEY=$(openssl rand -base64 128 | tee ${FLASK_KEY_LOG})
    # It generates a strong key and record its value to variable and file both

    # The Config object key for the Flask app must be called SECRET_KEY, regardless
    # of the OS environment variable name

    # Flask Config keys and values
    # Cannot use random SECRET_KEYS with multiple gunicorn workers
    # since every worker will generate a different random key

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT') or True
    SESSION_TYPE = os.environ.get('SESSION_TYPE') or "filesystem"


class TestConfig:
    # App name for HTML views, it appears on titles, links, etc.
    VIEW_APP_NAME = os.environ.get('VIEW_APP_NAME') or 'py-holder-demo-test'
    APP_NAME = os.environ.get('APP_NAME') or 'py-holder-demo-test'
    APP_VER = os.environ.get('APP_VER') or '1.0'

    # Flask config
    # Recommended generating key before running server
    # export FLASK_KEY_LOG=/secrets_storage_path/flask_secret_key.log
    # export  FLASK_SECRET_KEY=$(openssl rand -base64 128 | tee ${FLASK_KEY_LOG})
    # It generates a strong key and record its value to variable and file both
    # The Config object key for the Flask app must be called SECRET_KEY, regardless
    # of the OS environment variable name

    # Flask Config keys and values
    # Cannot use random SECRET_KEYS with multiple gunicorn workers
    # since every worker will generate a different random key

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT') or True
    SESSION_TYPE = os.environ.get('SESSION_TYPE') or "filesystem"
