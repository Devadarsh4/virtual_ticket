import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from datetime import datetime

# ─── Load API Key ────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# ─── Streamlit Page Config ───────────────────────────────────────────────────
st.set_page_config(page_title="🎤 Virtual Concert Ticket Finder", page_icon="🎫", layout="centered")

# ─── Title and Info ──────────────────────────────────────────────────────────
st.title("🎤 AI Virtual Concert Ticket Finder")
st.markdown("Ask about your favorite artist's upcoming concerts! 🌍")

# ─── Chat Setup ──────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("💬 Ask about an artist or chat casually:")

if st.button("Send") and user_input.strip():
    st.session_state.chat_history.append(("You", user_input))

    current_year = datetime.now().year

    prompt = f"""
    You are a smart and helpful concert assistant.
    The user said: "{user_input}"

    Your job:
    1. Extract the artist's name from the input (if any).
    2. Return a list of 3–5 fictional but realistic **upcoming concerts** for that artist.
    3. Use famous venues and cities from around the world.
    4. All concerts should be between {current_year} and {current_year + 1}.
    5. Format the result like:
       **🎶 Upcoming Concerts for [Artist Name]:**
       - 📍 City, Venue – 📅 Date
    6. If the user greets or chats casually, respond warmly and ask who they want to search concerts for.
    """

    try:
        response = model.generate_content(prompt).text.strip()
        st.session_state.chat_history.append(("Bot", response))
    except Exception as e:
        error_message = f"Error fetching concert data: {e}"
        st.session_state.chat_history.append(("Bot", error_message))

# ─── Chat History Display ─────────────────────────────────────────────────────
st.write("---")
st.subheader("🗨 Chat History")
for sender, message in reversed(st.session_state.chat_history[-8:]):
    st.markdown(f"**{sender}:** {message}")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.write("---")
st.caption("🎫 Powered by Gemini | Created by Rohit and Akshat Sukla 💡")