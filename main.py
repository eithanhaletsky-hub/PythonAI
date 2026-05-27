import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="הפרויקטים שלי",
    page_icon="🤖",
    layout="wide"
)

# --- Load Image as Base64 (לרקע מלא) ---



# --- Title ---
st.markdown('<div class="title-style">🤖 הפרויקטים שלי</div>', unsafe_allow_html=True)

# --- Content Box ---
st.markdown('<div class="box">ברוך הבא! כאן תוכל לראות את כל הפרויקטים שלך בעיצוב חדש ומהמם ✨</div>', unsafe_allow_html=True)

# --- Button ---
st.button("לחץ כאן")


