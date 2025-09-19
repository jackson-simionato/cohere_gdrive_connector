import logging
import os
import nltk

import connexion
from dotenv import load_dotenv

load_dotenv()

# download nltk data
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("punkt_tab")

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
    
    # Also load environment variables directly (for Render compatibility)
    import os
    flask_app.config["SERVICE_ACCOUNT_INFO"] = os.getenv("GDRIVE_SERVICE_ACCOUNT_INFO")
    flask_app.config["CONNECTOR_API_KEY"] = os.getenv("GDRIVE_CONNECTOR_API_KEY")
    flask_app.config["SEARCH_LIMIT"] = os.getenv("GDRIVE_SEARCH_LIMIT", "10")
    flask_app.config["FOLDER_ID"] = os.getenv("GDRIVE_FOLDER_ID")
    
    # Debug: Log environment variable status
    logger = logging.getLogger(__name__)
    service_account_info = flask_app.config.get("SERVICE_ACCOUNT_INFO")
    if service_account_info:
        logger.info(f"Service account info loaded: {type(service_account_info)} - {str(service_account_info)[:50]}...")
    else:
        logger.warning("No SERVICE_ACCOUNT_INFO found in environment")
        logger.info(f"Available env vars: GDRIVE_SERVICE_ACCOUNT_INFO={bool(os.getenv('GDRIVE_SERVICE_ACCOUNT_INFO'))}")

    # Add health check endpoint
    from .app import health_check
    flask_app.add_url_rule('/health', 'health_check', health_check, methods=['GET'])

    return flask_app
