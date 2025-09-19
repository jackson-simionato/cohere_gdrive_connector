#!/usr/bin/env python3
"""
Main entry point for the Google Drive connector.
Run this file to start the connector server.
"""

import logging
from provider import create_app

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run the app
    app = create_app()
    
    print("🚀 Starting Google Drive Connector...")
    print("📡 Server will be available at: http://localhost:8080")
    print("🔍 Search endpoint: POST /search")
    print("📋 API documentation: http://localhost:8080/ui/")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    app.run(host='0.0.0.0', port=8080, debug=True)
