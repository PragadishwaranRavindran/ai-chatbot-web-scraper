import os
import dotenv
import streamlit as st
from pinecone import Pinecone
from openai import OpenAI, OpenAIError
 
# ---- Load environment variables ----
dotenv.load_dotenv()
openai_api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
pinecone_api_key = st.secrets.get("PINECONE_API_KEY", os.getenv("PINECONE_API_KEY"))
pinecone_index_name = st.secrets.get("PINECONE_INDEX_NAME", os.getenv("PINECONE_INDEX_NAME"))
 
# ---- Initialize clients ----
openai_client = OpenAI(api_key=openai_api_key)
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)
 
# ---- Functions ----
def embed_query(text):
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding
 
def search_pinecone(query_embedding, top_k=5):
    return index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )['matches']
 
def generate_gpt_reply(chat_history, context, user_input):
    system_prompt = (
        "You are an AI assistant representing the company Rajexim. You must answer user questions strictly based on the information scraped from the Rajexim website."
        "Use the provided website context to answer questions accurately. "
        # "Internally Classify the visitor based on their query into one of the following categories:\n"
        # "- General Audience: Curious about the company, basic services, or EV-related interests\n"
        # "- Potential Customer: Asking about specific services, industry use cases, or geographic capabilities\n"
        # "- Technical Expert: Using domain-specific language, asking about tools, workflows, co-simulation, or validation\n\n"
        # "- Only if the context contains no relevant information for the question, then provide the contact form link. Never include the link when the context already answers the question."
        # "- When giving an answer, scan the provided context for any URLs or references to relevant case studies, service pages, or subdomains from hindujatech.com. If such links are present and directly related to the question, include them naturally in the response. Only include links that come from the provided context — do not invent URLs. If no relevant link exists in the context, do not add any link. \n\n"
        
        # "Never mention the visitor type in your response. \n\n"

        # "Adapt your response style accordingly:\n"
        # "- General Audience: Use simple, friendly, and informative language\n"
        # "- Potential Customer: Be slightly formal, concise, and solution-focused\n"
        # "- Technical Expert: Provide in-depth, precise, and technically articulate responses\n\n"
        "Always speak in the first person as if you are Rajexim. For example: "
        "✔️ Say: 'Yes, we offer this service.' "
        "❌ Do NOT say: 'Rajexim offers this service.' \n\n"
        "Use markdown formatting where appropriate:\n"
        "- **Bold important words**\n"
        "- Bullet points for features or benefits\n"
        "- Give links to the relevant case studies/links/subdomains on the website\n"
        "- Add line breaks between paragraphs for readability\n\n"
        "- Respond only within the context of the provided information."
    )
    # system_prompt = """
    # You are an AI assistant representing the company Rajexim. You must answer user questions strictly based on the information scraped from the Rajexim website.

    # **Instructions:**

    # 1. Always speak in the first person as if you are Rajexim. For example:
    # - ✔️ Say: "Yes, we offer this service."
    # - ❌ Do NOT say: "Rajexim offers this service."

    # 2. If the website clearly mentions the product, service, or information being asked about, respond confidently using the information.

    # 3. If the website does NOT clearly mention the requested product, service, or information:
    # - Respond clearly with a "No, we do not..." or "This is not something we offer..."
    # - Do NOT guess, assume, or use external knowledge.

    # 4. Keep answers clear, concise, and professional.

    # You must strictly follow these rules at all times. Do not provide general knowledge or speculate beyond the content of the website.

    # Website Name: Rajexim
    # """
    messages = [{"role": "system", "content": system_prompt}]
    messages += chat_history
    messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_input}"})
 
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content.strip()
 
 