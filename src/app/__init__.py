"""Flask App factory"""

from flask import Flask
from config import Config
# Flask blueprints imports
from app.main import bp as main_bp
from app.errors import bp as errors_bp




def create_app(config_class=Config):
    """Create Flask app from Config class"""
    # Create Flask app
    app = Flask(__name__)
    # Load config
    app.config.from_object(config_class)


    app.register_blueprint(main_bp)


    app.register_blueprint(errors_bp)

    # Extra initialization when debugging or testing
    if app.debug:
        pass
    if app.testing:
        pass

    return app
