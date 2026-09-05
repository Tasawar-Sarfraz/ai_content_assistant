import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ------------------------------------------------------------------------------
# 1. Configuration & Initial Setup
# ------------------------------------------------------------------------------
# Load environment variables from .env file for local development
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="🚀",
    layout="wide"
)

# Fetch Gemini API Key safely from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ------------------------------------------------------------------------------
# 2. Helper Functions
# ------------------------------------------------------------------------------
def get_gemini_client():
    """Initializes and returns the Google GenAI client securely."""
    if not GEMINI_API_KEY:
        st.error("Missing Gemini API Key! Please set GEMINI_API_KEY in environment variables or .env file.")
        st.stop()
    return genai.Client(api_key=GEMINI_API_KEY)

def generate_social_content(platform, topic, audience, tone, profile):
    """
    Constructs a prompt and calls Gemini 2.5 Flash model to produce structured content.
    """
    client = get_gemini_client()
    
    prompt = f"""
    You are an expert social media manager and content creator.
    
    Create a complete content package tailored for the following target parameters:
    - Platform: {platform}
    - Topic: {topic}
    - Target Audience: {audience}
    - Desired Tone: {tone}
    - User Profile Context: {profile}
    
    Return your response strictly in valid JSON format with the following keys:
    {{
      "post_text": "Main content body tailored for the platform",
      "caption": "Short engaging caption or call to action",
      "hashtags": ["hashtag1", "hashtag2", "hashtag3"],
      "post_type": "text-based"
    }}
    """
    
    try:
        # Requesting generation from gemini-2.5-flash
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        
        # Clean response string to parse JSON reliably
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        return json.loads(raw_text.strip())
    
    except Exception as e:
        st.error(f"Error during content generation: {str(e)}")
        return None

def publish_to_linkedin(content_text, access_token):
    """
    Publishes text content to LinkedIn using OpenID Connect profile fetch and REST API v2.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # 1. Fetch authenticated user's ID via OpenID Connect userinfo endpoint
    user_info_url = "https://api.linkedin.com/v2/userinfo"
    
    try:
        user_res = requests.get(user_info_url, headers=headers)
        if user_res.status_code != 200:
            return False, f"Failed to fetch profile info ({user_res.status_code}): {user_res.text}"
        
        user_data = user_res.json()
        author_sub = user_data.get("sub")
        
        if not author_sub:
            return False, "Could not retrieve user ID from LinkedIn response."
            
        author_urn = f"urn:li:person:{author_sub}"

        # 2. Construct and publish post payload according to LinkedIn REST API v2
        post_url = "https://api.linkedin.com/v2/posts"
        post_payload = {
            "author": author_urn,
            "commentary": content_text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }
        
        response = requests.post(post_url, headers=headers, json=post_payload)
        if response.status_code == 201:
            return True, "Successfully published to LinkedIn!"
        else:
            return False, f"LinkedIn API Error ({response.status_code}): {response.text}"

    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"

# ------------------------------------------------------------------------------
# 3. Streamlit UI Interface
# ------------------------------------------------------------------------------
st.title("🚀 AI Social Media Content Assistant")
st.write("Generate tailored posts, captions, and hashtags using Gemini AI.")

st.sidebar.header("🔑 Authentication Setup")
st.sidebar.info(
    "💡 **Note:** Direct publishing is optional.\n\n"
    "To post directly via API, generate a token with `openid`, `profile`, and `w_member_social` scopes.\n\n"
    "Otherwise, you can always generate content and copy-paste it directly!"
)
user_access_token = st.sidebar.text_input("OAuth Access Token (Optional)", type="password")

# 5 Input Fields Required
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox(
        "1. Select Platform",
        ["LinkedIn", "X (Twitter)", "Instagram", "Facebook"]
    )
    topic = st.text_input("2. Topic / Key Message", placeholder="e.g., Launching my new Python portfolio app")
    audience = st.text_input("3. Target Audience", placeholder="e.g., Tech recruiters, Python beginners")

with col2:
    tone = st.selectbox(
        "4. Tone",
        ["Professional", "Casual & Friendly", "Inspirational", "Humorous", "Educational"]
    )
    profile = st.text_input("5. Your Profile Handle / Context", placeholder="e.g., Python Student, Data Analyst")

st.markdown("---")

# Generation Action
if st.button("✨ Generate Content", type="primary"):
    if not topic or not audience:
        st.warning("Please fill in at least Topic and Target Audience.")
    else:
        with st.spinner("Gemini is creating your content..."):
            result = generate_social_content(platform, topic, audience, tone, profile)
            if result:
                st.session_state['generated_content'] = result

# Display Generated Output
if 'generated_content' in st.session_state:
    data = st.session_state['generated_content']
    
    st.subheader("📝 Generated Post Package")
    
    st.markdown("**Post Content:**")
    st.code(data.get("post_text", ""), language="text")
    
    st.markdown("**Caption:**")
    st.info(data.get("caption", ""))
    
    st.markdown("**Recommended Hashtags:**")
    hashtags_str = " ".join([f"#{h.replace('#', '')}" for h in data.get("hashtags", [])])
    st.write(f"`{hashtags_str}`")
    
    post_type_text = data.get('post_type', 'text-based').upper()
    st.markdown(f"**Post Type:** `{post_type_text}`")

    st.markdown("---")
    st.subheader("📤 Publishing Options")
    
    col_pub1, col_pub2 = st.columns(2)
    
    with col_pub1:
        full_text = f"{data.get('post_text')}\n\n{data.get('caption')}\n\n{hashtags_str}"
        st.text_area("Copy-Paste Ready Version", full_text, height=180)
        
    with col_pub2:
        st.markdown("**Direct API Publishing**")
        if platform == "LinkedIn":
            if st.button("Publish to LinkedIn Now"):
                if not user_access_token:
                    st.error("Please enter a valid LinkedIn OAuth Access Token in the sidebar first.")
                else:
                    with st.spinner("Publishing to LinkedIn via REST API..."):
                        success, message = publish_to_linkedin(full_text, user_access_token)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
        else:
            st.warning(f"Direct publishing for {platform} requires elevated API credentials and OAuth token configuration.")
