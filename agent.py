import os
import google.generativeai as genai
import requests
import json
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- 1. CONFIGURE YOUR AGENT'S PERSONA ---
# IMPORTANT: Fill this out to define your personal brand. The more specific you are, the better the posts will be.

YOUR_NICHE = "AI consultant helping small businesses automate their marketing."
YOUR_AUDIENCE = "Non-technical small business owners and marketing managers."
YOUR_VOICE = "Helpful, approachable, and practical. I avoid jargon and focus on real-world benefits."
# Choose 3-5 core topics you want to be known for.
YOUR_CONTENT_PILLARS = [
    "Practical AI tool reviews",
    "AI for lead generation",
    "Demystifying AI concepts for beginners",
    "Future of marketing with AI"
]
YOUR_GOAL = "To start conversations and generate leads for my consulting services."


def configure_api():
    """Configures the Gemini API key."""
    try:
        # Best practice: Load API key from an environment variable
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("----------------------------------------------------------------------")
            print("⚠️  API key not found in environment variables.")
            print("Please paste your Google AI Studio API key here and press Enter:")
            print("----------------------------------------------------------------------")
            api_key = input("API Key: ").strip()

        genai.configure(api_key=api_key)
        print("✅ API configured successfully.")
        return True
    except Exception as e:
        print(f"❌ Error configuring the API: {e}")
        return False

def build_master_prompt(topic: str) -> str:
    """Builds the detailed prompt for the AI model based on the user's topic and persona."""

    # This is the "brain" of your agent. It tells the model HOW to write, not just WHAT to write about.
    prompt = f"""
    Act as my expert LinkedIn content strategist and copywriter. Your tone is knowledgeable, engaging, and tailored for the LinkedIn platform.

    **My Persona Profile:**
    - **My Niche:** {YOUR_NICHE}
    - **My Target Audience:** {YOUR_AUDIENCE}
    - **My Voice and Tone:** {YOUR_VOICE}
    - **My Core Content Pillars:** {', '.join(YOUR_CONTENT_PILLARS)}
    - **My Primary Goal:** {YOUR_GOAL}

    **Your Task:**
    Draft a compelling LinkedIn post based on the following topic. You must adhere strictly to my persona and follow the structure below.

    **Topic for today's post:**
    "{topic}"

    **Required Post Structure:**
    1.  **Engaging Hook (1-2 lines):** Start with a provocative question, a bold statement, or a surprising statistic to grab immediate attention.
    2.  **Insightful Body (3-5 short paragraphs):**
        - Elaborate on the hook.
        - Provide your unique perspective, analysis, or a short story related to the topic.
        - Use bullet points or numbered lists for clarity if it makes sense.
        - Explain the "so what?" – why should my audience care?
    3.  **Clear Call-to-Action (CTA):** End with a question to encourage comments and engagement.
    4.  **Relevant Hashtags:** Include 3-5 relevant, specific hashtags. Avoid overly generic ones.

    Produce only the final, ready-to-publish LinkedIn post. Do not include any extra commentary before or after the post.
    """
    return prompt

def generate_post(topic: str):
    """Generates the LinkedIn post using the Gemini model."""
    if not topic:
        print("❌ Topic cannot be empty.")
        return None

    try:
        print("\n🤖 Agent is thinking... Generating your post...")
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        master_prompt = build_master_prompt(topic)
        response = model.generate_content(master_prompt)
        return response.text
    except Exception as e:
        print(f"❌ An error occurred during generation: {e}")
        print("   Please ensure your API key is valid and has permissions.")
        return None

def configure_linkedin_api():
    """Configures the LinkedIn API credentials."""
    try:
        access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
        person_id = os.environ.get("LINKEDIN_PERSON_ID")
        
        if not access_token or not person_id:
            print("----------------------------------------------------------------------")
            print("⚠️  LinkedIn API credentials not found in environment variables.")
            print("Please follow these steps to get your LinkedIn API credentials:")
            print("1. Go to https://www.linkedin.com/developers/")
            print("2. Create an app and get your access token")
            print("3. Get your LinkedIn person ID")
            print("4. Add them to your .env file")
            print("----------------------------------------------------------------------")
            return None, None
            
        return access_token, person_id
    except Exception as e:
        print(f"❌ Error configuring LinkedIn API: {e}")
        return None, None

def post_to_linkedin(content: str, access_token: str, person_id: str):
    """Posts content to LinkedIn using the LinkedIn API."""
    try:
        url = "https://api.linkedin.com/v2/ugcPosts"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # LinkedIn API payload
        payload = {
            "author": f"urn:li:person:{person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            print("✅ Successfully posted to LinkedIn!")
            return True
        else:
            print(f"❌ Failed to post to LinkedIn. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error posting to LinkedIn: {e}")
        return False

def generate_and_post_automatically():
    """Generates content and posts automatically to LinkedIn."""
    print(f"\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting automatic post generation...")
    
    # Configure APIs
    if not configure_api():
        print("❌ Cannot generate post without Google AI API configuration.")
        return
    
    access_token, person_id = configure_linkedin_api()
    if not access_token or not person_id:
        print("❌ Cannot post to LinkedIn without API credentials.")
        return
    
    # Generate topics based on your content pillars
    topics = [
        "Latest AI tool that's changing how small businesses handle customer service",
        "Common AI misconceptions that are holding small businesses back",
        "How AI can automate your email marketing in 2025",
        "Simple AI automation that saves 5 hours per week",
        "The future of AI in small business marketing"
    ]
    
    # Pick a random topic or cycle through them
    import random
    topic = random.choice(topics)
    
    # Generate the post
    post_content = generate_post(topic)
    
    if post_content:
        print(f"\n📝 Generated post about: {topic}")
        print("="*60)
        print(post_content)
        print("="*60)
        
        # Post to LinkedIn
        success = post_to_linkedin(post_content, access_token, person_id)
        if success:
            print("🎉 Post successfully shared on LinkedIn!")
        else:
            print("❌ Failed to post to LinkedIn. Please check your credentials.")
    else:
        print("❌ Failed to generate post content.")

def schedule_posts():
    """Schedules automatic posts twice a day."""
    # Schedule posts at 9 AM and 3 PM every day
    schedule.every().day.at("09:00").do(generate_and_post_automatically)
    schedule.every().day.at("15:00").do(generate_and_post_automatically)
    
    print("📅 Scheduled automatic posts at 9:00 AM and 3:00 PM daily.")
    print("🔄 Agent is now running in automatic mode...")
    print("Press Ctrl+C to stop the agent.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def main():
    """Main function to run the agent."""
    print("--- LinkedIn Post Agent Initializing ---")
    
    print("\n🤖 Choose your mode:")
    print("1. Manual mode - Generate posts interactively")
    print("2. Automatic mode - Schedule posts twice daily")
    print("3. Post once now - Generate and post immediately")
    
    while True:
        try:
            choice = input("\nEnter your choice (1/2/3): ").strip()
            
            if choice == "1":
                # Original manual mode
                if not configure_api():
                    print("Agent cannot start without a valid API configuration. Exiting.")
                    return

                print("\n👋 Welcome! I'm your LinkedIn Post Agent.")
                print("Provide me with a topic, an idea, or even a link, and I'll draft a post for you.")
                print("Type 'exit' or 'quit' to end the session.")

                while True:
                    try:
                        topic_input = input("\nEnter your post topic > ")
                        if topic_input.lower() in ['exit', 'quit']:
                            print("\n👍 Agent session ended. Goodbye!")
                            break

                        post = generate_post(topic_input)

                        if post:
                            print("\n✨ Here is your draft post. Ready to copy and paste! ✨")
                            print("="*60)
                            print(post)
                            print("="*60)
                            
                            # Ask if user wants to post to LinkedIn
                            post_now = input("\nDo you want to post this to LinkedIn now? (y/n): ").lower()
                            if post_now == 'y':
                                access_token, person_id = configure_linkedin_api()
                                if access_token and person_id:
                                    success = post_to_linkedin(post, access_token, person_id)
                                    if success:
                                        print("🎉 Posted to LinkedIn successfully!")

                    except KeyboardInterrupt:
                        print("\n\n👍 Agent session ended by user. Goodbye!")
                        break
                break
                
            elif choice == "2":
                # Automatic scheduling mode
                schedule_posts()
                break
                
            elif choice == "3":
                # Post once immediately
                generate_and_post_automatically()
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\n👍 Agent session ended by user. Goodbye!")
            break

if __name__ == "__main__":
    main()
