#!/usr/bin/env python3
"""
WSGI entry point for the Google Drive connector.
This file is used by Gunicorn to serve the application.
"""

from provider import create_app

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
