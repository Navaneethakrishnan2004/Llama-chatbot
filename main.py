import os
import requests
import streamlit as st
from dotenv import dotenv_values


st.set_page_config(
    page_title="The Tech Buddy 🧑‍💻",
    page_icon="🤖",
    layout="centered",
)

env_secrets = dotenv_values(".env")

GROQ_API_KEY = env_secrets.get("GROQ_API_KEY")
INITIAL_RESPONSE = env_secrets.get("INITIAL_RESPONSE")
INITIAL_MSG = env_secrets.get("INITIAL_MSG")
CHAT_CONTEXT = env_secrets.get("CHAT_CONTEXT")

if not all([GROQ_API_KEY, INITIAL_RESPONSE, INITIAL_MSG, CHAT_CONTEXT]):
    try:
        GROQ_API_KEY = GROQ_API_KEY or st.secrets["GROQ_API_KEY"]
        INITIAL_RESPONSE = INITIAL_RESPONSE or st.secrets["INITIAL_RESPONSE"]
        INITIAL_MSG = INITIAL_MSG or st.secrets["INITIAL_MSG"]
        CHAT_CONTEXT = CHAT_CONTEXT or st.secrets["CHAT_CONTEXT"]
    except FileNotFoundError:
        st.error("Missing secrets! Please provide either a .env file or .streamlit/secrets.toml.")
        st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE},
    ]

st.title("Welcome Buddy!")
st.caption("Helping You Level Up Your Coding Game")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "🗨️"):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask me")

if user_prompt:
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": CHAT_CONTEXT},
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history,
    ]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": messages,
        "stream": False
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
    else:
        reply = f"Error: {response.status_code} - {response.text}"

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(reply)

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
