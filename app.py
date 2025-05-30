import os
import json
import faiss
import gradio as gr
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google.generativeai import GenerativeModel, configure

# Load environment
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise EnvironmentError("GOOGLE_API_KEY not found in .env")
configure(api_key=api_key)

# Constants
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "index/my_index.faiss"
LOOKUP_PATH = "index/chunk_lookup.json"

# Load index and data
model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(INDEX_PATH)
with open(LOOKUP_PATH, "r") as f:
    chunk_lookup = json.load(f)

# Gemini model
llm = GenerativeModel(model_name="gemini-1.5-flash")

def rewrite_query(original_query):
    prompt = f"""Rewrite the following user question to improve document retrieval while using Catan vocabulary. Answer only with the improved Query, no options and no explanations
Original: "{original_query}"
Rewritten:"""
    response = llm.generate_content(prompt)
    return response.text.strip().strip('"')

def search_faiss(query, k):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)
    retrieved = [(idx, chunk_lookup[idx]) for idx in indices[0]]
    return retrieved

def build_prompt(original_query, retrieved_chunks):
    prompt = f"""
You are an expert on the rules of Catan (with expansions). 

Do not answer questions, that are off topic. If the Question or Prompt is out of context, simply explain that you are only answering questions related to settlers of Catan.
Do not make up answers. If the Information is not included in the context chunks, simply explain that you dont have the knowledge. Additionally dont provide information that the user did not specifically ask for, even if you dont know the answer.

This is the context information:

---
{chr(10).join(chunk for i, (_, chunk) in enumerate(retrieved_chunks))}
---

Answer this question in natural and polite language: "{original_query}"
"""
    return prompt

def rag_pipeline(original_query, k):
    rewritten_query = rewrite_query(original_query)
    retrieved = search_faiss(rewritten_query, k)
    retrieved_texts = [f"[{i+1}] {chunk}" for i, (_, chunk) in enumerate(retrieved)]
    prompt = build_prompt(original_query, retrieved)
    response = llm.generate_content(prompt)
    return rewritten_query, retrieved_texts, response.text


def ui_func(query, k):
    rewritten_query, chunks, response = rag_pipeline(query, k)
    return rewritten_query, "\n\n".join(chunks), response

# UI
with gr.Blocks(title="RAG for Catan Rules") as demo:
    gr.Markdown("## RAG for Catan Rules (with expansions)")
    gr.Markdown("Ask anything about the Catan rules. Especially useful when your friends are being rules lawyers.")

    with gr.Row():
        query = gr.Textbox(label="Your Question", placeholder="Can I build a road through another player's settlement?")
        k_slider = gr.Slider(1, 10, value=3, step=1, label="Top K Results")

    submit_btn = gr.Button("Get Answer")
    
    with gr.Row():
        rewritten_query = gr.Textbox(label="Rewritten Query", lines=4, interactive=False)
        retrieved = gr.Textbox(label="Retrieved Chunks", lines=16, interactive=False)
        answer = gr.Textbox(label="Answer", lines=10, interactive=False)

    example_queries = [
        "Can I move the robber back to the same tile?",
        "How do knight cards work in Cities and Knights?",
        "What's the rule for building a settlement on a port?",
    ]
    gr.Examples(
        examples=example_queries,
        inputs=[query],
    )

    submit_btn.click(fn=ui_func, inputs=[query, k_slider], outputs=[rewritten_query, retrieved, answer])

demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
