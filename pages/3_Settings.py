import streamlit as st
from config import load_config, save_config

st.set_page_config(page_title="Settings", layout="centered")
st.title("⚙️ Settings")

cfg = load_config()

with st.form("settings_form"):
    app_title = st.text_input("App title", value=cfg.get("app_title", "AI Chatbot"))
    submitted = st.form_submit_button("Save")

if submitted:
    new_cfg = save_config({"app_title": app_title.strip() or "AI Chatbot"})
    st.success("Saved. Title will reflect across the app.")
    st.caption(f"Current title: {new_cfg['app_title']}")
