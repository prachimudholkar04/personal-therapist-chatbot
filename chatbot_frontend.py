import streamlit as st
import requests
from datetime import datetime
import json
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="MindMate 💬", layout="centered")

# Custom CSS for vibe
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #dbeafe, #f0fdfa);
        }
        .stChatInput {
            font-size: 18px;
        }
        .stApp {
            background-color: #f9fafb;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 MindMate – Your AI Therapist")

# Tone setting
tone = st.selectbox("Choose your therapist's vibe:", [
    "🌿 Gentle & Calm", "💡 Honest & Motivational", "✨ Spiritual & Reflective"
])

tone_map = {
    "🌿 Gentle & Calm": "gentle, soft, and nurturing",
    "💡 Honest & Motivational": "motivational, encouraging, but honest",
    "✨ Spiritual & Reflective": "spiritually aware, deep, and reflective"
}

# Mood slider
mood = st.slider("How are you feeling today?", 0, 10, 5)
mood_emoji = ["😭", "😢", "😞", "😐", "🙂", "😊", "😃", "😄", "🤩", "🥳", "🦋"]
st.markdown(f"**Mood:** {mood_emoji[mood]}")

# Init chat
if "chat" not in st.session_state:
    st.session_state.chat = []

API_URL = "http://127.0.0.1:8000/chat"

# Chat input
user_input = st.chat_input("Write your thoughts...")
if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    prompt_payload = {
        "message": user_input,
        "tone": tone_map.get(tone, "gentle and supportive")
    }

    try:
        response = requests.post(API_URL,
                                 json={"message": user_input, "tone": tone_map.get(tone, "gentle and supportive")})
        response.raise_for_status()
        data = response.json()
        bot_reply = data.get("response", "⚠️ Therapist didn’t reply. Try again?")
    except Exception as e:
        bot_reply = f"⚠️ Error: {e}"

    st.session_state.chat.append({"role": "bot", "content": bot_reply})

    # Save journal entry
    journal_entry = {
        "timestamp": datetime.now().isoformat(),
        "mood": mood_emoji[mood],
        "tone": tone,
        "user": user_input,
        "bot": bot_reply
    }
    with open("journal.json", "a") as f:
        f.write(json.dumps(journal_entry) + "\n")

# Display chat
for msg in st.session_state.chat:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
            reaction = st.radio(
                "How did this reply feel?",
                ["😌", "🙂", "😢", "🤔", "❤️"],
                key=msg["content"],
                horizontal=True
            )

# Export button
try:
    with open("journal.json", "r") as f:
        journal_text = f.read()
    st.download_button("📤 Export Journal", journal_text, file_name="MindMate_Journal.json")
except FileNotFoundError:
    st.info("📓 You haven't saved any journal entries yet.")
