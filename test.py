import asyncio
import json
import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import streamlit as st
import pineconeDataLoad as pinecone_util


def call_pinecone(fileName):
    st.write("📤 Uploading to Pinecone:", fileName)
    pinecone_util.uploadFileOnPonecone(fileName)
    st.success("✅ Upload completed!")


async def scrape_to_json(base_url: str, output_file: str = "scraped_data.json", max_pages: int = 100):
    visited = set()
    to_visit = {base_url}
    results = {}

    parsed_base = urlparse(base_url)
    base_domain = parsed_base.netloc

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            java_script_enabled=True
        )

        page = await context.new_page()

        await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.navigator.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        """)

        await page.set_extra_http_headers({
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        })

        while to_visit and len(visited) < max_pages:
            url = to_visit.pop()
            if url in visited:
                continue
            visited.add(url)

            try:
                st.write(f"🔍 Scraping: {url}")
                await page.goto(url, wait_until='domcontentloaded', timeout=60000)
                await asyncio.sleep(3)

                try:
                    close_popup = await page.query_selector("button[class*='popup-close'], .close, .close-popup, .login-close")
                    if close_popup:
                        await close_popup.click()
                        await asyncio.sleep(1)
                        st.write("🔒 Popup closed")
                except Exception as e:
                    st.warning(f"Popup close failed: {e}")

                await asyncio.sleep(3)

                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text(separator="\n", strip=True)
                results[url] = text

                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    full_url = urljoin(url, href)
                    parsed = urlparse(full_url)
                    if parsed.netloc.endswith(base_domain) and parsed.scheme in ["http", "https"]:
                        if full_url not in visited:
                            to_visit.add(full_url)

            except Exception as e:
                st.error(f"❌ Failed to scrape {url}: {e}")
                results[url] = f"Failed to scrape: {str(e)}"

        await browser.close()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    st.success(f"✅ Saved {len(results)} pages to {output_file}")


# 🚀 Streamlit UI logic
def main():
    st.title("🌐 Website Scraper & Pinecone Uploader")

    url_input = st.text_input("Enter URL to scrape:", value="https://example.com")

    if st.button("🕸️ Scrape Website"):
        if not url_input:
            st.error("Please enter a valid URL!")
        else:
            st.info("🔄 Scraping started...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(scrape_to_json(url_input))
            st.success("✅ Scraping completed.")

    if st.button("📤 Upload Cleaned JSON to Pinecone"):
        if os.path.exists("scraped_data.json"):
            call_pinecone("scraped_data.json")
        else:
            st.error("❌ scraped_data.json not found. Please run scraping first.")


if __name__ == "__main__":
    main()






import os
import json
import time
from tqdm import tqdm
import dotenv
from pinecone import Pinecone
from openai import OpenAI, OpenAIError, RateLimitError
 
# ---- Load environment variables ----
dotenv.load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
 
# ---- Initialize OpenAI client ----
openai_client = OpenAI(api_key=openai_api_key)
 
# ---- Initialize Pinecone ----
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)
 
# ---- Load the chunked JSON ----
with open("pepperfry_chunks.json", "r", encoding="utf-8") as f:
    chunked_docs = json.load(f)
 
print(f"📦 Loaded {len(chunked_docs)} chunks for embedding.")
 
# ---- Function: Get OpenAI Embedding ----
def get_embedding(text, model="text-embedding-ada-002", max_retries=5):
    """Fetch embedding for a given text using OpenAI API."""
    for attempt in range(max_retries):
        try:
            response = openai_client.embeddings.create(
                input=text,
                model=model
            )
            return response.data[0].embedding
        except RateLimitError:
            print("⚠️ OpenAI rate limit hit. Retrying in 5 seconds...")
            time.sleep(5)
        except OpenAIError as e:
            print(f"❌ OpenAI error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    raise RuntimeError("Failed to get embedding after retries.")
 
# ---- Prepare vectors for Pinecone ----
vectors = []
print("🔄 Generating embeddings...")
for doc in tqdm(chunked_docs, desc="Embedding chunks"):
    vector_id = doc["id"]  # Unique ID like url#chunk-0
    embedding = get_embedding(doc["text"])  # 1536-dim vector
    metadata = {
        "url": doc["url"],  # Store original URL
        "text": doc["text"][:500]  # Store partial text (limit size in metadata)
    }
    vectors.append((vector_id, embedding, metadata))
 
# ---- Upsert in Batches ----
batch_size = 100  # Recommended batch size
print("⬆️ Upserting vectors to Pinecone...")
for i in tqdm(range(0, len(vectors), batch_size), desc="Upserting batches"):
    batch = vectors[i:i + batch_size]
    index.upsert(vectors=batch)
 
print("✅ All embeddings successfully upserted to Pinecone.")