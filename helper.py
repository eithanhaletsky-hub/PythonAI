from time import ctime

from dotenv import load_dotenv
import os
import streamlit as st
from google import genai
from google.genai import types
import time

def current_time() -> str:
    """
    פונקציה שמחזירה מה התאירך והשעה
    """
    return time.ctime()



all_models = ["gemini-2.5-flash",
              "gemini-2.0-flash",
              "gemini-2.5-flash-lite",
              "gemini-2.0-flash-lite",
              ]

def createclient():
    st.session_state.client = genai.Client(api_key=LoadAPIkey())

def sendMessage(text,system_prompt,history=[]):
    if 'client' not in st.session_state:
        createclient()

    for model in all_models:
        client = st.session_state.client
        try:
            chat = client.chats.create(
                model = model,
                history = history,
                config = types.GenerateContentConfig(
                    system_instruction = system_prompt
                )
            )
            ai = chat.send_message(text)
            print(ai.text)
            return ai.text
        except Exception as e:
            error = str(e)
            print(e)
            if "429" in error:
                st.info("שלחת יותר מדי הודעות נסה מחר פעם נוספת")
                return
            if "503" in error:
                st.info(f"המודל עמוס נסה  מודל אחר")
            else:
              st.info("error" + error)
              return
            print (f"{model} not working...")

def LoadAPIkey():
    load_dotenv()
    API_KEY = os.getenv("API_KEY") or st.secrets["API_KEY"]
    return API_KEY

def showmessage(sender,text):
    newmessage = st.chat_message(sender)
    newmessage. write(text)

def save_to_history(project,sender,text):
    if project not in st.session_state:
        st.session_state[project] = {
            "history": []
        }
    st.session_state[project]["history"].append(
        {
            "role": sender,
            "parts": [{"text": text}]
        }
    )

def newpage(project):
        st.session_state[project] = {
            "history": []
        }












