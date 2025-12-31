import streamlit as st
from helper import *

st.set_page_config(
    page_title="בוט לשיעורי בית",
    page_icon=""
)

st.title("בוט לשיעורי בית📗")

api_key = LoadAPIkey()


showmessage("ai", "How can I help you?")

user = st.chat_input("הודעה שלך...")
if user:
    showmessage("user",user)































































































