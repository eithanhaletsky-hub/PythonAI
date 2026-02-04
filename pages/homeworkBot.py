from multiprocessing.connection import answer_challenge

import streamlit as st
from helper import *

st.set_page_config(
    page_title="בוט לשיעורי בית",
    page_icon=""
)

st.title("בוט לשיעורי בית📗")

api_key = LoadAPIkey()


showmessage("ai", "How can I help you?")

if "homework" not in st.session_state:
    newpage("homework")

system_prompt = """
    # תפקיד
    אתה בוט שמסייע בשיעורי בית.
    
    # מטרה
    לעזור לי להבין את החומר ולפתור תרגילים.
    הסברים צריכים להיות ברורים, מסודרים ובגובה העיניים.
    כוון אותי לחשיבה הנכונה ולפתרון, ולא רק לתשובה הסופית.
    
    # סגנון
    ענה בצורה אנושית, רגועה וישירה.
    אם מתאים – תן דוגמאות קצרות.
    
    # מגבלות
    אם אינך יודע את התשובה – אמור זאת במפורש.
    אל תנחש ואל תמציא מידע.
"""

st.session_state["homework"]["system_prompt"] = system_prompt

history = st.session_state["homework"]["history"]
for line in history:
    sender = line["role"]
    if sender == "model":
        sender = "ai"

    text = line["parts"][0]["text"]
    showmessage(sender,text)

user = st.chat_input("הודעה שלך...")
if user:
    showmessage("user",user)
    save_to_history("homework","user",user)
    history = st.session_state["homework"]["history"]
    answer = sendMessage(user,system_prompt,history)
    showmessage("ai", answer)
    save_to_history("homework", "model", answer)





























































































