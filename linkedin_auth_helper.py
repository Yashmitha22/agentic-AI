"""
LinkedIn OAuth2 Helper Script
This script helps you get your LinkedIn access token through OAuth2 flow.
"""

import requests
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

def get_authorization_url():
    """Generate the LinkedIn authorization URL."""
    
    client_id = input("Enter your LinkedIn App Client ID: ").strip()
    
    if not client_id:
        print("❌ Client ID is required")
        return
    
    # OAuth2 parameters
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': 'http://localhost:3000',
        'scope': 'r_liteprofile w_member_social'
    }
    
    # Build authorization URL
    base_url = 'https://www.linkedin.com/oauth/v2/authorization'
    auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    print("\n🔗 LinkedIn Authorization URL:")
    print("=" * 80)
    print(auth_url)
    print("=" * 80)
    print("\n📋 Instructions:")
    print("1. Copy the URL above and paste it in your browser")
    print("2. Sign in to LinkedIn and authorize your app")
    print("3. You'll be redirected to localhost (this will show an error page - that's normal)")
    print("4. Copy the 'code' parameter from the URL in your browser")
    print("5. Come back here and paste the code")
    
    return client_id

def exchange_code_for_token(client_id, client_secret, auth_code):
    """Exchange authorization code for access token."""
    
    try:
        url = "https://www.linkedin.com/oauth/v2/accessToken"
        
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': 'http://localhost:3000',
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(url, data=data, headers=headers)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            
            print("\n✅ Success! Got your access token:")
            print("=" * 50)
            print(f"Access Token: {access_token}")
            print("=" * 50)
            print("\n📝 Add this to your .env file:")
            print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
            
            return access_token
        else:
            print(f"Failed to get access token")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting access token: {e}")
        return None

def main():
    """Main function to guide through LinkedIn OAuth2 flow."""
    
    print("🔑 LinkedIn OAuth2 Token Generator")
    print("=" * 50)
    print("This will help you get your LinkedIn access token.")
    print("\nFirst, make sure you have:")
    print("✓ Created a LinkedIn Developer App")
    print("✓ Added 'Share on LinkedIn' product")
    print("✓ Configured r_liteprofile and w_member_social scopes")
    print("\n" + "=" * 50)
    
    # Step 1: Get authorization URL
    client_id = get_authorization_url()
    if not client_id:
        return
    
    # Step 2: Get the authorization code from user
    print("\n" + "=" * 50)
    auth_code = input("Paste the authorization code here: ").strip()
    
    if not auth_code:
        print("Authorization code is required")
        return
    
    # Step 3: Get client secret
    client_secret = input("Enter your LinkedIn App Client Secret: ").strip()
    
    if not client_secret:
        print("Client Secret is required")
        return
    
    # Step 4: Exchange code for token
    access_token = exchange_code_for_token(client_id, client_secret, auth_code)
    
    if access_token:
        print("\n🎉 Setup complete! You can now use the LinkedIn API.")
        print("Next step: Run 'python linkedin_helper.py' to test your connection.")

if __name__ == "__main__":
    main()
