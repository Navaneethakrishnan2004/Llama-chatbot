# 🦙Llama-3.1 Chatbot🤖 Powered by Groq & Streamlit

In this guide, we’ll walk you through building and deploying a personalized AI chatbot using **Streamlit** and the **LLaMA-3.1-8B-Instant** model, powered by **Groq** for ultra-fast inference. Best part? We’ll also show you how to **deploy it for free!**

You’ll learn how each part of the code works and how to easily customize it to suit your needs.

## 🚀 Getting Started

1. **Sign in to** [Groq](https://groq.com/) and click **"Start Building"**.

2. **Create a new API key** and save it safely.

## 📦 Install Required Libraries

Create a `requirements.txt` file with the following content:

```txt
groq==0.9.0
streamlit==1.37.0
python-dotenv
```

Install the packages using:

```bash
pip install -r requirements.txt
```

## 📄 Set Up `main.py`

Start by importing the required libraries:

```python
import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq
```

- `streamlit`: for UI
- `dotenv`: for handling environment variables
- `groq`: to interact with the LLM

## ⚙️ Configure the Streamlit Page

Give your app a polished layout:

```python
st.set_page_config(
    page_title="The Tech Buddy",
    page_icon="",
    layout="centered",
)
```

## 🔐 Store API Keys & Prompts Securely

Create a `.env` file in your project root with the following content:

```env
GROQ_API_KEY='YOUR_GROQ_API_KEY'

INITIAL_RESPONSE="Your bot's first message to the user."
CHAT_CONTEXT="How you want the chatbot to behave."
INITIAL_MSG="Initial assistant message to start the conversation."
```

To load these secrets:

```python
try:
    secrets = dotenv_values(".env")  # local environment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except:
    secrets = st.secrets  # Streamlit cloud deployment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
INITIAL_MSG = secrets["INITIAL_MSG"]
CHAT_CONTEXT = secrets["CHAT_CONTEXT"]
```

## 🧠 Initialize the Chat App

Choose your preferred model from [Groq’s supported models](https://console.groq.com/docs/models).
We're using: `llama-3.1-8b-instant`.

Set up the client and initialize chat history:

```python
client = Groq()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE},
    ]
```

## 💬 Build the Chat Interface

Render chat messages using:

```python
st.title("Hey Buddy!")
st.caption("Let's go back in time...")

for message in st.session_state.chat_history:
    with st.chat_message("role", avatar=''):
        st.markdown(message["content"])
```

## ✍️ User Input Field

Allow users to send messages:

```python
user_prompt = st.chat_input("Let's chat!")
```

---

## ⚡ Generate Responses with Groq

Define a function to parse streamed output:

```python
def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

Handle user input and model responses:

```python
if user_prompt:
    with st.chat_message("user", avatar=""):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": CHAT_CONTEXT},
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        stream=True
    )
    response = st.write_stream(parse_groq_stream(stream))
    st.session_state.chat_history.append({"role": "assistant", "content": response})
```

## 🧪 Complete `main.py`

Here’s the full code for `main.py`:

```python
import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq


def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


st.set_page_config(
    page_title="The 70's Painter",
    page_icon="🎨",
    layout="centered",
)

try:
    secrets = dotenv_values(".env")
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except:
    secrets = st.secrets
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
INITIAL_MSG = secrets["INITIAL_MSG"]
CHAT_CONTEXT = secrets["CHAT_CONTEXT"]

client = Groq()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE}
    ]

st.title("Hey Buddy!")
st.caption("Let's go back in time...")

for message in st.session_state.chat_history:
    with st.chat_message("role", avatar='🤖'):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask me")

if user_prompt:
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    messages = [
        {"role": "system", "content": CHAT_CONTEXT},
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    with st.chat_message("assistant", avatar='🤖'):
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            stream=True
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state.chat_history.append({"role": "assistant", "content": response})
```

To run locally:

```bash
streamlit run main.py
```

## 🌍 Deploy Your App for Free

1. Push your code to a **GitHub** repository.

2. Log in to and go to **My Apps**.

3. Click **Create app**.

4. Select your GitHub repo and the correct branch:

5. Point to your `main.py` file:

6. (Optional) Create a custom URL:

7. Under **Additional Settings**, paste the contents of your `.env` file in **Secrets**:

8. Click **Deploy**!

🎉 **Congrats!** Your personalized AI chatbot is now live and available for anyone to use — all for free!
