import os
from dotenv import load_dotenv
from google import genai
import streamlit as st
import time
from helper import *
# ====== PAGE SETTINGS ======
st.set_page_config(page_title="הצ'אט שלי", page_icon="🤖", layout="wide")



# ====== CSS לעיצוב ======
st.markdown("""
    <style>
    /* רקע התמונה */
    .stApp {
        background-image: url("whatsApp image 2025-11-05 at 19.05.53.jpeg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* מיכל שקוף לצ'אט */
    .chat-box {
        background: rgba(255, 255, 255, 0.72);
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 8px 28px rgba(0,0,0,0.25);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)


# ====== TITLE ======
st.title("🤖 הצ'אט שלי")

#load_dotenv()

#API_KEY = os.getenv("API_KEY")
API_KEY = loadAPIKey()



# ------ FUNCTIONS ------

def saveToHistory(sender, text):
    st.session_state.history.append({
        "sender": sender,
        "text": text
    })


def send(prompt):

    # הוספת הודעת המשתמש להיסטוריה
    saveToHistory("user", prompt)

    # בניית הקונטקסט מהשיחה כולה
    all_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash-lite"]

    context = ""
    for line in st.session_state.history:
        context += f"{line['sender']}: {line['text']} \n"

    # ניסיון לשלוח לכל אחד מהמודלים
    for model in all_models:
        chat = st.session_state.gemini.chats.create(model=model)
        try:
            message = chat.send_message(context)

            saveToHistory("assistant", message.text)

            return message
        except:
            print(f"מודל {model} לא עבד - מנסה את המודל הבא")


# ------ FIRST MESSAGE ------
prompt = "מה שלומך?"

def start():
    st.session_state.gemini = genai.Client(api_key=API_KEY)
    st.session_state.history = []

    # שליחה של הודעת הפתיחה
    send(prompt)


if "gemini" not in st.session_state:
    start()


# -------- CHAT CONTAINER --------
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

# הצגת כל ההיסטוריה
if 'history' in st.session_state:
    for line in st.session_state.history[1:]:  # מדלג על הודעת הפתיחה
        msg = st.chat_message(line["sender"])
        msg.write(line["text"])

# קלט המשתמש
prompt = st.chat_input("Say something")
if prompt:

    # הצגת ההודעה על המסך
    user_msg = st.chat_message("user")
    user_msg.write(prompt)

    with st.spinner("Wait for it..."):
        time.sleep(1)

    # שליחה לג'מיני
    message = send(prompt)

    # הצגת תגובת הבוט
    ai_msg = st.chat_message("assistant")
    ai_msg.write(message.text)

st.markdown('</div>', unsafe_allow_html=True)

