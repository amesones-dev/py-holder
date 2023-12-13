import unittest
import warnings

# App specific imports
# Flask App
from app import create_app
from config import TestConfig


class MockFSOApp:
    def __init__(self, config_class=TestConfig):
        """Creates a mock app using config class attributes"""
        self.config = config_class().to_dict()


class ModelsTestCase(unittest.TestCase):
    # Use flask_app=True  value to create a flask app with the Flask app factory create_app
    # and with test config defined in high level TestConfig
    # Creating a Flask app is needed when testing Flask related capabilities

    # Use flask_app=False to create a MockApp with config class TestFlaskAppUserConfig
    # In this case only the FlaskAppUser class and its methods are tested

    def setUp(self, flask_app=True):
        """Initial test set up"""
        test_app = create_app(config_class=TestConfig)
        self.app = test_app

        # Flask context
        if flask_app:
            self.app_context = test_app.app_context()
            if self.app_context:
                self.app_context.push()

        # App specific

        # Test logging configuration
        warnings.filterwarnings(action="ignore", category=ResourceWarning)

    def tearDown(self):
        """Test tear down tasks"""
        pass

    def test_0_check(self):
        """Test placeholder"""
        pass




if __name__ == '__main__':
    unittest.main(verbosity=2)
