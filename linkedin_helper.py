"""
LinkedIn API Helper Script
This script helps you get your LinkedIn Person ID and test your access token.
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_linkedin_connection():
    """Test your LinkedIn API connection and get your person ID."""
    
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    
    if not access_token:
        print("❌ No LinkedIn access token found in .env file")
        access_token = input("Please enter your LinkedIn access token: ").strip()
    
    if not access_token:
        print("❌ Access token is required")
        return
    
    try:
        # Test API connection and get profile info
        url = "https://api.linkedin.com/v2/people/~"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            person_id = data.get('id')
            
            print("✅ LinkedIn API connection successful!")
            print(f"📋 Your LinkedIn Person ID: {person_id}")
            print(f"👤 Name: {data.get('localizedFirstName', '')} {data.get('localizedLastName', '')}")
            print("\n📝 Add this to your .env file:")
            print(f"LINKEDIN_PERSON_ID={person_id}")
            
        else:
            print(f"❌ Failed to connect to LinkedIn API")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing LinkedIn connection: {e}")

def check_posting_permissions():
    """Check if your access token has posting permissions."""
    
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    
    if not access_token:
        print("❌ No LinkedIn access token found in .env file")
        return
    
    try:
        # Check permissions by attempting to get posting scope
        url = "https://api.linkedin.com/v2/people/~/shares"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("✅ You have posting permissions!")
        elif response.status_code == 403:
            print("❌ No posting permissions. Make sure your app has 'w_member_social' scope.")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking permissions: {e}")

if __name__ == "__main__":
    print("🔧 LinkedIn API Helper")
    print("=" * 50)
    
    print("\n1️⃣ Testing LinkedIn API connection...")
    test_linkedin_connection()
    
    print("\n2️⃣ Checking posting permissions...")
    check_posting_permissions()
    
    print("\n✨ Setup complete! You can now run the main agent.")
