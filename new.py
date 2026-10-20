import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
# ---------------------------------
# 1. ENTER YOUR GEMINI API KEY HERE
# ---------------------------------
API_KEY = os.getenv("API_KEY")

# ---------------------------------
# 2. PAGE CONFIGURATION
# ---------------------------------
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Gemini AI Chatbot")
st.caption("Powered by Google Gemini")
st.write("Hello! Ask me anything.")

# Validate that a key has been entered
if not API_KEY.strip() or API_KEY == "PASTE_YOUR_GEMINI_API_KEY_HERE":
    st.warning("Please add your Gemini API key in the code.")
    st.stop()

# Initialize Gemini client
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Could not initialize Gemini: {e}")
    st.stop()

# ---------------------------------
# 3. CHAT HISTORY
# ---------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------
# 4. USER INPUT AND AI RESPONSE
# ---------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Ask Gemini
    with st.chat_message("assistant"):
        try:
            with st.spinner("Gemini is thinking..."):

                # Convert conversation history to Gemini format
                history = []

                for message in st.session_state.messages[:-1]:
                    history.append(
                        types.Content(
                            role=(
                                "user" if message["role"] == "user"
                                else "model"
                            ),
                            parts=[types.Part.from_text(
                                text=message["content"]
                            )]
                        )
                    )

                chat = client.chats.create(
                    model="gemini-3.8-flash",
                    history=history,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "You are a friendly and helpful AI assistant. "
                            "Answer questions clearly and accurately."
                        )
                    )
                )

                response = chat.send_message(user_input)
                answer = response.text or "I couldn't generate a response."

                st.markdown(answer)

            # Save AI response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"Gemini API error: {e}")

# ---------------------------------
# 5. SIDEBAR AND CLEAR CHAT
# ---------------------------------
st.sidebar.title("Chat Settings")
st.sidebar.write("Model: Gemini 2.5 Flash")

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()