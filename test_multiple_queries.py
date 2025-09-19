#!/usr/bin/env python3
"""
Test script to try multiple search queries and help debug the Google Drive connector.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_query(query, api_key):
    """Test a single query and return results."""
    url = "http://localhost:8080/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"query": query}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', []), None
        else:
            return [], f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return [], str(e)

def main():
    """Test multiple queries to help debug the connector."""
    
    api_key = os.getenv('GDRIVE_CONNECTOR_API_KEY')
    if not api_key:
        print("❌ Error: GDRIVE_CONNECTOR_API_KEY not found")
        return
    
    # Test queries - try different approaches
    test_queries = [
        "curriculum",           # Simple word
        "Jackson",       # Common word
        "the",            # Very common word
        "google",         # Brand name
        "drive",          # Another brand name
        "sheet",          # Google Sheets
        "presentation",   # Google Slides
        "doc",            # Google Docs
        "",               # Empty query (should return some results)
    ]
    
    print("🔍 Testing Multiple Search Queries")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing query: '{query}'")
        results, error = test_query(query, api_key)
        
        if error:
            print(f"   ❌ Error: {error}")
        else:
            print(f"   📊 Found {len(results)} results")
            
            if results:
                # Show first result details
                first_result = results[0]
                title = first_result.get('title', 'No title')
                text_preview = first_result.get('text', '')[:150] + "..." if len(first_result.get('text', '')) > 150 else first_result.get('text', '')
                print(f"   📄 First result: {title}")
                print(f"   📝 Text preview: {text_preview}")
                break  # Stop testing once we find results
    
    print("\n" + "=" * 50)
    print("💡 Troubleshooting Tips:")
    print("1. Make sure you've shared Google Drive folders with your service account")
    print("2. Check that the folders contain Google Docs, Sheets, or Slides")
    print("3. Verify the service account email in your .env file")
    print("4. Try creating a test Google Doc with the word 'test' in it")

if __name__ == "__main__":
    main()
