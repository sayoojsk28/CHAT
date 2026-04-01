import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.0-flash")

# UI
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("💬 Chatbot with Gemini")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user msg
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Convert history to Gemini format
    chat = model.start_chat(history=[
        {"role": "user", "parts": [m["content"]]} if m["role"] == "user"
        else {"role": "model", "parts": [m["content"]]}
        for m in st.session_state.messages[:-1]
    ])

    # Get response
    response = chat.send_message(user_input)

    bot_reply = response.text

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)