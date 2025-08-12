# Website Scrape – Streamlit App

## Run Locally

1. Create a virtualenv and install deps:

```
pip install -r requirements.txt
python -m playwright install chromium
```

2. Create a `.env` file with:

```
OPENAI_API_KEY=...
PINECONE_API_KEY=...
PINECONE_INDEX_NAME=...
```

3. Start the app:

```
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. In Streamlit Cloud, create a new app pointing to `app.py`.
3. In “Secrets”, add:

```
OPENAI_API_KEY="..."
PINECONE_API_KEY="..."
PINECONE_INDEX_NAME="..."
```

4. Add this to `packages.txt` (root) if scraping is enabled:

```
libnss3
libatk1.0-0
libatk-bridge2.0-0
libdrm2
libxkbcommon0
libxcomposite1
libxdamage1
libxfixes3
libgbm1
libpango-1.0-0
libasound2
libatspi2.0-0
libxrandr2
libgtk-3-0
```

The app entry is `app.py`; pages are auto-discovered from `pages/`.
