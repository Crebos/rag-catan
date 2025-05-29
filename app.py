import os
import json
import faiss
import gradio as gr
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google.generativeai import GenerativeModel, configure

# Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in .env")
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
llm = GenerativeModel("gemini-pro")

def search_faiss(query, k):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)
    retrieved = [(idx, chunk_lookup[str(idx)]) for idx in indices[0]]
    return retrieved

def build_prompt(query, retrieved_chunks):
    prompt = f"""You are an expert on the rules of Catan (with expansions). Answer the user query using the following retrieved context chunks:

---
{chr(10).join(f'[{i+1}] {chunk}' for i, (_, chunk) in enumerate(retrieved_chunks))}
---

Now, answer the question: "{query}"
"""
    return prompt

def rag_pipeline(query, k):
    retrieved = search_faiss(query, k)
    retrieved_texts = [f"[{i+1}] {chunk}" for i, (_, chunk) in enumerate(retrieved)]
    prompt = build_prompt(query, retrieved)
    response = llm.generate_content(prompt)
    return retrieved_texts, response.text

def ui_func(query, k):
    chunks, response = rag_pipeline(query, k)
    return chunks, response

# UI
with gr.Blocks(title="RAG for Catan Rules") as demo:
    gr.Markdown("## RAG for Catan Rules (with expansions)")
    gr.Markdown("Ask anything about the Catan rules. Especially useful when your friends are being rules lawyers.")

    with gr.Row():
        query = gr.Textbox(label="Your Question", placeholder="Can I build a road through another player's settlement?")
        k_slider = gr.Slider(1, 10, value=3, step=1, label="Top K Results")

    submit_btn = gr.Button("Get Answer")
    
    with gr.Row():
        retrieved = gr.HighlightedText(label="Retrieved Chunks", combine_adjacent=True)
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

    submit_btn.click(fn=ui_func, inputs=[query, k_slider], outputs=[retrieved, answer])

demo.launch()
