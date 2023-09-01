from config import Config
from apiflask import APIFlask


def create_app(config_class=Config):
    # Create Flask app
    app = APIFlask(__name__)
    # Load config
    app.config.from_object(config_class)
    app.config['OPENAPI_VERSION'] = '3.0.2'

    # Flask blueprints imports
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Extra initialization when debugging or testing
    if app.debug:
        pass
    if app.testing:
        pass

    return app
