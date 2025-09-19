#!/usr/bin/env python3
"""
Script to help set up Google Drive connector environment variables.
Run this script and follow the prompts.
"""

import json
import os
import secrets
import string


def generate_api_key(length: int = 32) -> str:
    """Generate a secure random API key."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def main():
    print("Google Drive Connector Environment Setup")
    print("=" * 50)
    
    # Get service account JSON
    print("\n1. Service Account Credentials")
    print("Paste your service account JSON credentials below.")
    print("Press Enter twice when done:")
    
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    
    # Remove the last empty line
    if lines and lines[-1] == "":
        lines.pop()
    
    json_str = '\n'.join(lines)
    
    try:
        # Validate JSON
        json.loads(json_str)
        print("✅ Valid JSON credentials!")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return
    
    # Generate API key
    api_key = generate_api_key()
    print(f"\n2. Generated API Key: {api_key}")
    
    # Create .env file content
    env_content = f"""# Google Drive Connector Environment Variables
# Generated on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Service Account Credentials
GDRIVE_SERVICE_ACCOUNT_INFO={json_str}

# Connector API Key
GDRIVE_CONNECTOR_API_KEY={api_key}

# Optional: Search limit (default is 10)
GDRIVE_SEARCH_LIMIT=10

# Optional: Specific folder ID to search (leave empty to search entire drive)
# GDRIVE_FOLDER_ID=your-folder-id-here
"""
    
    # Write .env file
    env_file_path = ".env"
    with open(env_file_path, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Environment variables saved to {env_file_path}")
    print("\nNext steps:")
    print("1. Share your Google Drive folders with the service account email")
    print("2. Run: poetry install")
    print("3. Run: poetry run python -m provider")
    print("4. Test with: curl -X POST 'http://localhost:8080/search' -H 'Authorization: Bearer YOUR_API_KEY' -H 'Content-Type: application/json' -d '{\"query\": \"test\"}'")


if __name__ == "__main__":
    main()
