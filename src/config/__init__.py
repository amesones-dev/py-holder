import os


class Config(object):
    # App name for HTML views, it appears on titles, links, etc.
    VIEW_APP_NAME = os.environ.get('VIEW_APP_NAME') or 'py-holder-demo'
    API_NAME = os.environ.get('API_NAME') or 'py-holder-API-demo'
    API_VER = os.environ.get('API_VER') or '1.0'

    # Content constraints
    JSON_PREFERRED = os.environ.get('JSON_API') or True

    # Flask config
    # Recommended generating key before running server
    # export  FLASK_SECRET_KEY =$(openssl rand -base64 128 | tee /secrets_storage_path/flask_secret_key.log)
    # It generates a strong key and record its value to variable and file both

    # The Config object key for the Flask app must be called SECRET_KEY, regardless of the OS environment variable name

    # Flask Config keys and values
    # Cannot use random SECRET_KEYS with multiple gunicorn workers
    # since every worker will generate a different random key

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT') or True
    SESSION_TYPE = os.environ.get('SESSION_TYPE') or "filesystem"


class TestConfig(object):
    # App name for HTML views, it appears on titles, links, etc.
    VIEW_APP_NAME = os.environ.get('VIEW_APP_NAME') or 'py-holder-demo-test'
    API_NAME = os.environ.get('API_NAME') or 'py-holder-API-demo-test'
    API_VER = os.environ.get('API_VER') or '1.0'

    # Content constraints
    JSON_PREFERRED = os.environ.get('JSON_API') or True

    # Flask config
    # Recommended generating key before running server
    # export  FLASK_SECRET_KEY =$(openssl rand -base64 128 | tee /secrets_storage_path/flask_secret_key.log)
    # It generates a strong key and record its value to variable and file both

    # The Config object key for the Flask app must be called SECRET_KEY, regardless of the OS environment variable name

    # Flask Config keys and values
    # Cannot use random SECRET_KEYS with multiple gunicorn workers
    # since every worker will generate a different random key

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT') or True
    SESSION_TYPE = os.environ.get('SESSION_TYPE') or "filesystem"
