import streamlit as st
import base64

# --- Page Config ---
st.set_page_config(
    page_title="הפרויקטים שלי",
    page_icon="🤖",
    layout="wide"
)

# --- Load Image as Base64 (לרקע מלא) ---
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

background_image = get_base64_of_image("whatsApp Image 2025-11-05 at 19.05.53.jpeg")


# --- Custom CSS for Full Background ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{background_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Overlay כהה */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.4);
        z-index: 0;
    }}

    /* כותרת */
    .title-style {{
        font-size: 55px;
        font-weight: bold;
        color: #ffeb3b;
        text-shadow: 4px 4px 12px black;
        text-align: center;
        margin-top: 25px;
        position: relative;
        z-index: 1;
    }}

    /* תיבה */
    .box {{
        background: rgba(255, 255, 255, 0.15);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        backdrop-filter: blur(7px);
        font-size: 22px;
        color: white;
        position: relative;
        z-index: 1;
        margin-bottom: 20px;
    }}

    /* כפתור */
    .stButton>button {{
        background: linear-gradient(90deg, #845ec2, #d65db1);
        border: none;
        padding: 12px 30px;
        border-radius: 12px;
        font-size: 20px;
        font-weight: bold;
        color: white;
        cursor: pointer;
        transition: 0.3s;
        position: relative;
        z-index: 1;
    }}
    .stButton>button:hover {{
        transform: scale(1.08);
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }}
    </style>
""",
    unsafe_allow_html=True
)

# --- Title ---
st.markdown('<div class="title-style">🤖 הפרויקטים שלי</div>', unsafe_allow_html=True)

# --- Content Box ---
st.markdown('<div class="box">ברוך הבא! כאן תוכל לראות את כל הפרויקטים שלך בעיצוב חדש ומהמם ✨</div>', unsafe_allow_html=True)

# --- Button ---
st.button("לחץ כאן")


