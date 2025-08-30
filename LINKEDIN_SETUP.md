# LinkedIn API Setup Guide

## Quick Start for Personal Use

### 1. Create LinkedIn App
- Go to: https://www.linkedin.com/developers/
- Click "Create App"
- Fill required fields (use placeholders for personal use)

### 2. Get Client Credentials
- Copy your Client ID and Client Secret from the app dashboard

### 3. Generate Access Token

#### Method A: Use linkedin_auth_helper.py (Recommended)
```bash
python linkedin_auth_helper.py
```

#### Method B: Manual OAuth Flow
1. Visit this URL (replace YOUR_CLIENT_ID):
```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:3000&scope=r_liteprofile%20w_member_social
```

2. Authorize and copy the code from redirect URL

3. Exchange code for token using curl or Postman:
```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=YOUR_AUTH_CODE&redirect_uri=http://localhost:3000&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET"
```

### 4. Test Your Setup
```bash
python linkedin_helper.py
```

### 5. Add to .env file
```
GOOGLE_API_KEY=your_google_ai_studio_api_key
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_PERSON_ID=your_linkedin_person_id
```

## Important Notes:
- Personal access tokens expire after 60 days
- For production use, implement proper OAuth2 refresh flow
- LinkedIn has rate limits: ~100 posts per day for personal profiles
