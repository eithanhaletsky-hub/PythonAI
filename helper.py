from dotenv import load_dotenv
import os
import streamlit as st
from google import genai

all_models = ["gemini-3.0-flash",
              "gemini-2.5-flash",
              "gemini-2.0-flash",
              "gemini-2.5-flash-lite",
              "gemini-2.0-flash-lite",
              ]

def createclient():
    st.session_state.client = genai.Client(api_key=LoadAPIkey())

def sendMessage(text,history=[]):
    if 'client' not in st.session_state:
        createclient()

    for model in all_models:
        client = st.session_state.client
        try:
            chat = client.chat.create(
                model = model
            )
        except:
            print (f"{model} not working...")

def LoadAPIkey():
    load_dotenv()
    API_KEY = os.getenv("API_KEY") or st.secrets["API_KEY"]
    return API_KEY

def showmessage(sender,text):
    newmessage = st.chat_message(sender)
    newmessage. write(text)