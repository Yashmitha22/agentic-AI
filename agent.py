import os
import google.generativeai as genai

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

def main():
    """Main function to run the agent."""
    print("--- LinkedIn Post Agent Initializing ---")
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

        except KeyboardInterrupt:
            print("\n\n👍 Agent session ended by user. Goodbye!")
            break

if __name__ == "__main__":
    main()
