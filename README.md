# 🚀 AI Content Assistant

An interactive, beginner-friendly Python application built with **Streamlit** and **Google Gemini AI** (`gemini-2.5-flash`). This tool generates platform-tailored social media content (posts, captions, and hashtags) and supports direct API publishing to platforms like **LinkedIn**.

---

## 🌟 Features

- **Tailored AI Content Generation:** Generate posts customized by platform, topic, target audience, tone, and profile context.
- **Structured Output:** Automatically formats posts, captions, and hashtags in a clean, readable layout.
- **Copy-Paste Ready Area:** Provides a ready-to-use text box for quick manual posting to any platform.
- **Direct LinkedIn API Publishing:** Publish text posts directly to LinkedIn using official OAuth 2.0 OpenID Connect authentication.
- **Beginner-Friendly UI:** Simple two-column interactive web interface built with Streamlit.

---

## 🏗️ Project Structure

```text
ai-content-assistant/
│
├── app.py              # Main Streamlit UI and backend logic
├── requirements.txt    # Python package dependencies
├── .env                # Environment file for secret keys (Do NOT commit to Git)
└── README.md           # Project documentation
```

---

## ⚙️ Requirements & Dependencies

The application relies on the following key Python libraries:

* **`streamlit`** — Interactive web UI framework.
* **`google-genai`** — Official Google SDK for Gemini models.
* **`requests`** — HTTP library for interacting with social media REST APIs.
* **`python-dotenv`** — For loading environment variables securely from a `.env` file.

### `requirements.txt`
```text
streamlit>=1.35.0
google-genai>=0.1.0
requests>=2.31.0
python-dotenv>=1.0.1
```

---

## 🔑 Environment & API Setup

### 1. Get a Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Create an API key for the **Gemini API**.

### 2. Configure Local Environment
Create a `.env` file in the root directory of your project:

```env
GEMINI_API_KEY="your_actual_gemini_api_key_here"
```

> ⚠️ **Security Warning:** Never commit your `.env` file or API keys to public repositories like GitHub!

---

## 🚀 How to Run the App Locally

### Step 1: Install Dependencies
Open your terminal/command prompt and run:
```bash
pip install -r requirements.txt
```

### Step 2: Start Streamlit
Launch the local web application:
```bash
streamlit run app.py
```

Your browser will automatically open at `http://localhost:8501`.

---

## 🔐 Optional: LinkedIn Direct Publishing Setup

Direct API publishing requires user authorization via LinkedIn's OAuth 2.0 protocol.

1. **LinkedIn App Creation:** Go to the [LinkedIn Developer Portal](https://developer.linkedin.com/) and create a new application.
2. **Enable Products:** Under the **Products** tab, request access to:
   - **Share on LinkedIn**
   - **Sign In with LinkedIn using OpenID Connect**
3. **Generate Access Token:** Go to **Tools > Token Generator** and select the following permissions (scopes):
   - `w_member_social`
   - `openid`
   - `profile`
4. **Publishing in App:** Copy the generated access token and paste it into the **OAuth Access Token** field in the Streamlit sidebar.

---

## 🛠️ Tech Stack & Model Summary

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit | Web UI rendering and input forms |
| **AI Generation** | Google Gemini (`gemini-2.5-flash`) | Fast, structured text & prompt generation |
| **SDK** | `google-genai` | Official Python client for Gemini models |
| **API Integration** | LinkedIn REST API v2 | Direct posting via OpenID Connect URNs |

---

## 📝 License

Distributed under the MIT License. Feel free to modify and expand for your personal learning or commercial projects!
