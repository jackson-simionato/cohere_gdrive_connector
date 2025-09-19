#!/usr/bin/env python3
"""
Debug script to check if the Google Drive connector can access any files.
This will help diagnose permission and access issues.
"""

import os
import json
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

def debug_google_drive_access():
    """Debug Google Drive access and list available files."""
    
    print("🔍 Google Drive Access Debug")
    print("=" * 50)
    
    # Check environment variables
    service_account_info = os.getenv('GDRIVE_SERVICE_ACCOUNT_INFO')
    folder_id = os.getenv('GDRIVE_FOLDER_ID')
    
    if not service_account_info:
        print("❌ Error: GDRIVE_SERVICE_ACCOUNT_INFO not found in environment")
        return
    
    try:
        # Parse service account info
        credentials_data = json.loads(service_account_info)
        print(f"✅ Service account email: {credentials_data.get('client_email', 'Unknown')}")
        
        # Create credentials
        credentials = service_account.Credentials.from_service_account_info(
            credentials_data, 
            scopes=[
                "https://www.googleapis.com/auth/drive.metadata.readonly",
                "https://www.googleapis.com/auth/drive.readonly",
            ]
        )
        
        # Refresh credentials if needed
        if credentials.expired or not credentials.valid:
            credentials.refresh(Request())
        
        print("✅ Credentials are valid")
        
        # Build the service
        service = build("drive", "v3", credentials=credentials)
        print("✅ Google Drive API service created")
        
        # Test 1: List files without any search filter
        print("\n📋 Test 1: List all accessible files (no search filter)")
        print("-" * 30)
        
        try:
            # Get all files (limited to 10 for testing)
            results = service.files().list(
                pageSize=10,
                fields="nextPageToken, files(id, name, mimeType, webViewLink, modifiedTime)",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True
            ).execute()
            
            files = results.get('files', [])
            print(f"📊 Found {len(files)} total files")
            
            if files:
                print("\n📄 Available files:")
                for i, file in enumerate(files, 1):
                    name = file.get('name', 'Unknown')
                    mime_type = file.get('mimeType', 'Unknown')
                    file_id = file.get('id', 'Unknown')
                    print(f"   {i}. {name} ({mime_type}) - ID: {file_id}")
            else:
                print("❌ No files found - this indicates a permissions issue")
                
        except HttpError as e:
            print(f"❌ Error accessing files: {e}")
            return
        
        # Test 2: List only Google Docs, Sheets, Slides
        print("\n📋 Test 2: List only Google Docs, Sheets, Slides")
        print("-" * 30)
        
        search_mime_types = [
            "application/vnd.google-apps.document",
            "application/vnd.google-apps.spreadsheet", 
            "application/vnd.google-apps.presentation",
        ]
        
        mime_condition = " or ".join([f"mimeType = '{mime_type}'" for mime_type in search_mime_types])
        
        try:
            results = service.files().list(
                pageSize=10,
                q=mime_condition,
                fields="nextPageToken, files(id, name, mimeType, webViewLink, modifiedTime)",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True
            ).execute()
            
            files = results.get('files', [])
            print(f"📊 Found {len(files)} Google Docs/Sheets/Slides")
            
            if files:
                print("\n📄 Google Workspace files:")
                for i, file in enumerate(files, 1):
                    name = file.get('name', 'Unknown')
                    mime_type = file.get('mimeType', 'Unknown')
                    file_id = file.get('id', 'Unknown')
                    print(f"   {i}. {name} ({mime_type}) - ID: {file_id}")
            else:
                print("❌ No Google Docs/Sheets/Slides found")
                print("💡 This explains why searches return 0 results!")
                
        except HttpError as e:
            print(f"❌ Error accessing Google Workspace files: {e}")
        
        # Test 3: Check specific folder if configured
        if folder_id:
            print(f"\n📋 Test 3: Check specific folder (ID: {folder_id})")
            print("-" * 30)
            
            try:
                results = service.files().list(
                    pageSize=10,
                    q=f"'{folder_id}' in parents",
                    fields="nextPageToken, files(id, name, mimeType, webViewLink, modifiedTime)",
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True
                ).execute()
                
                files = results.get('files', [])
                print(f"📊 Found {len(files)} files in specified folder")
                
                if files:
                    print("\n📄 Files in folder:")
                    for i, file in enumerate(files, 1):
                        name = file.get('name', 'Unknown')
                        mime_type = file.get('mimeType', 'Unknown')
                        print(f"   {i}. {name} ({mime_type})")
                else:
                    print("❌ No files found in specified folder")
                    
            except HttpError as e:
                print(f"❌ Error accessing folder: {e}")
        else:
            print("\n📋 Test 3: No specific folder configured (searching entire drive)")
        
        # Summary and recommendations
        print("\n" + "=" * 50)
        print("💡 Recommendations:")
        print("1. If no files are found: Share folders with the service account email")
        print("2. If files found but no Google Docs/Sheets/Slides: Create some test documents")
        print("3. If folder-specific: Check the GDRIVE_FOLDER_ID is correct")
        print("4. Service account email:", credentials_data.get('client_email', 'Unknown'))
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing service account JSON: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    debug_google_drive_access()
