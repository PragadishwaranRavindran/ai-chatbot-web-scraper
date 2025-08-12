import streamlit as st
from config import load_config

cfg = load_config()
st.set_page_config(page_title=cfg.get("app_title", "WebScraper Home"), layout="wide")

st.title(f"🕸️ Welcome to {cfg.get('app_title', 'Website Scraper')}")
st.write("Use the sidebar to navigate between pages:")
st.markdown("""
- 🕷️ **Website Scraper**: Crawl and extract website content  
- 💬 **Chat with Data**: Ask questions about the scraped content  
""")