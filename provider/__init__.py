import logging
import os
import nltk

import connexion
from dotenv import load_dotenv

load_dotenv()

# download nltk data
nltk.download("stopwords")
nltk.download("punkt")

API_VERSION = "api.yaml"


class UpstreamProviderError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def create_app():
    # Use absolute path to find the API spec
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    api_spec_path = os.path.join(parent_dir, "api.yaml")
    
    # If api.yaml exists in parent directory, use it; otherwise use relative path
    if os.path.exists(api_spec_path):
        app = connexion.FlaskApp(__name__, specification_dir=parent_dir)
    else:
        app = connexion.FlaskApp(__name__, specification_dir="../../.openapi")
    
    app.add_api(
        API_VERSION, resolver=connexion.resolver.RelativeResolver("provider.app")
    )
    logging.basicConfig(level=logging.INFO)
    flask_app = app.app
    config_prefix = os.path.split(os.getcwd())[1].upper()
    flask_app.config.from_prefixed_env(config_prefix)
    flask_app.config["APP_ID"] = config_prefix

    return flask_app
