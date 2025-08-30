# LinkedIn Post Agent Setup Guide

## 🚀 Getting Started

This agent can now automatically post to your LinkedIn page twice daily or on demand!

### 1. Install Dependencies

First, install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Get Your LinkedIn API Credentials

#### Step 1: Create a LinkedIn App
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Click "Create App"
3. Fill in the required information:
   - App name: "Personal LinkedIn Poster"
   - LinkedIn Page: Your personal LinkedIn page
   - Privacy policy URL: Can use a placeholder for personal use
   - App logo: Upload any image

#### Step 2: Get Your Access Token
1. In your app dashboard, go to "Auth" tab
2. Add these scopes:
   - `r_liteprofile` (to read your profile)
   - `w_member_social` (to post on your behalf)
3. Use the "Request access token" feature or implement OAuth2 flow
4. For personal use, you can generate a token manually

#### Step 3: Get Your LinkedIn Person ID
1. Go to your LinkedIn profile
2. View page source and search for "urn:li:person:" 
3. Or use this API call with your access token:
   ```
   GET https://api.linkedin.com/v2/people/~
   ```

### 3. Configure Environment Variables

Edit the `.env` file with your credentials:

```
GOOGLE_API_KEY=your_google_ai_studio_api_key_here
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token_here
LINKEDIN_PERSON_ID=your_linkedin_person_id_here
```

### 4. Run the Agent

```bash
python agent.py
```

## 🤖 Agent Modes

### Mode 1: Manual Mode
- Generate posts interactively
- Review before posting
- Control what gets posted

### Mode 2: Automatic Mode
- Posts twice daily at 9 AM and 3 PM
- Runs continuously in the background
- Uses your content pillars to generate relevant topics

### Mode 3: Post Once Now
- Generate and post immediately
- Good for testing the setup

## 📝 Customizing Your Content

Edit these variables in `agent.py` to match your brand:

- `YOUR_NICHE`: Your professional focus area
- `YOUR_AUDIENCE`: Who you're targeting
- `YOUR_VOICE`: Your writing style
- `YOUR_CONTENT_PILLARS`: 3-5 core topics
- `YOUR_GOAL`: What you want to achieve

## 🔧 Troubleshooting

### Common Issues:

1. **LinkedIn API errors**: Check your access token and permissions
2. **Rate limiting**: LinkedIn has posting limits, space out your posts
3. **Content rejection**: LinkedIn may flag certain content types

### Rate Limits:
- LinkedIn allows limited posts per day for personal profiles
- Consider spacing posts appropriately

## 🚨 Important Notes

- **Test first**: Always test with manual mode before using automatic mode
- **Content quality**: The AI generates content, but review for accuracy
- **LinkedIn Terms**: Ensure your use complies with LinkedIn's terms of service
- **API limits**: Be aware of LinkedIn's API rate limits

## 📊 Monitoring

The agent will log all activities including:
- Post generation times
- Successful/failed LinkedIn posts
- Error messages for troubleshooting

Happy posting! 🎉
