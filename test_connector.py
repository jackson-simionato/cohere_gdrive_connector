#!/usr/bin/env python3
"""
Test script for the Google Drive connector.
This script tests the connector with a sample query.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connector():
    """Test the Google Drive connector with a sample query."""
    
    # Get API key from environment
    api_key = os.getenv('GDRIVE_CONNECTOR_API_KEY')
    if not api_key:
        print("❌ Error: GDRIVE_CONNECTOR_API_KEY not found in environment variables")
        return
    
    # Connector URL
    url = "http://localhost:8080/search"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test query
    test_query = "test"
    payload = {"query": test_query}
    
    print("🧪 Testing Google Drive Connector...")
    print(f"📡 URL: {url}")
    print(f"🔍 Query: {test_query}")
    print(f"🔑 Using API Key: {api_key[:10]}...")
    print("-" * 50)
    
    try:
        # Make the request
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            print(f"✅ Success! Found {len(results)} results")
            
            if results:
                print("\n📄 Sample Results:")
                for i, result in enumerate(results[:3]):  # Show first 3 results
                    title = result.get('title', 'No title')
                    text_preview = result.get('text', '')[:100] + "..." if len(result.get('text', '')) > 100 else result.get('text', '')
                    url = result.get('url', 'No URL')
                    
                    print(f"\n{i+1}. {title}")
                    print(f"   📝 Text: {text_preview}")
                    print(f"   🔗 URL: {url}")
            else:
                print("ℹ️  No results found. This might be normal if:")
                print("   - No Google Docs/Sheets/Slides contain the search term")
                print("   - The service account doesn't have access to any files")
                print("   - The Google Drive folder is empty")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the connector is running on localhost:8080")
        print("   Run: poetry run python main.py")
        
    except requests.exceptions.Timeout:
        print("❌ Timeout: The request took too long")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_connector()
