import streamlit as st
from helper import * #תביא את כל הפונקציות מהקובץ המשותף
import PIL.Image

st.set_page_config(
    page_title="סוכן קוד",
    page_icon=""
)

st.title("סוכן קוד")

api_key = loadAPIKey() #מביא את הפונקציה מהקובץ

#הודעה ראשונה מהצ'אט
showMessage("AI","היי מה נכין היום?")

#אם לא הגדרנו את הפרויקט - צור אותו בזיכרון
if "CodeAgent" not in st.session_state:
    newPage("CodeAgent")

#פרומפט מיוחד שמגדיר לAI איך לעבוד
system_prompt = """
    אתה מתכנת מומחה, אתה ממש טוב 
    
"""

#לשמור בזיכרון
st.session_state["CodeAgent"]["system_prompt"] = system_prompt

history = st.session_state["CodeAgent"]["history"]
for line in history:
    sender = line["role"]
    if sender == "model": #ג'מיני מצפה לקבל model
        sender = "ai" #streamlit מצפה לקבל AI

    text = line["parts"][0]["text"] #פשוט מוציאים את הטקסט מהמבנה של ג'מיני
    showMessage(sender,text)

#מקום להקליד
user = st.chat_input("ההודעה שלך...")

image_button = st.file_uploader("העלאת תמונה", type=["png","jpg","jpeg"])

if user: #אם יש הודעה

    showMessage("user",user)
    #שולפים את ההיסטוריה

    image = None

    if image_button:
        image = PIL.Image.open(image_button)

    save_to_history("CodeAgent","user",user)
    history = st.session_state["CodeAgent"]["history"]
    answer = sendMessage(user,system_prompt,history, image) #לשלוח לAI את ההודעה

    showMessage("ai",answer) #תראה את התשובה

    save_to_history("CodeAgent","model",answer)


