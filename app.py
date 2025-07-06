from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import requests
import os

# Optional: Suppress TF logs if present
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask(__name__)

# === Load Data & FAISS Index ===
with open("mosdac_metadata.json", "r", encoding="utf-8") as f:
    meta = json.load(f)
texts = meta["texts"]
sources = meta["sources"]

model = SentenceTransformer("BAAI/bge-base-en-v1.5")
index = faiss.read_index("mosdac_index.faiss")

# === Greeting keywords ===
greetings = {"hi", "hello", "hey", "namaste", "good morning", "good evening"}

# === Use Ollama to generate smart RAG answers ===
def generate_rag_response(user_input, top_chunks):
    context = "\n\n".join(top_chunks)

    prompt = f"""
You are a helpful assistant for the MOSDAC satellite data platform by ISRO. Use the following context to answer the user's question clearly and completely.

Context:
{context}

User Question:
{user_input}

Answer:
""".strip()

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "tinyllama",  # or mistral, phi, etc.
        "prompt": prompt,
        "stream": False
    })

    result = response.json()
    return result.get("response", "Sorry, I couldn’t generate a response.")

# === Flask Routes ===
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.get_json().get("message", "").strip().lower()

    # Greet directly
    if user_input in greetings:
        return jsonify({"response": "👋 Hello! I’m your MOSDAC Assistant. Ask me anything about satellites, rainfall, products, or data access."})

    # Encode query
    query = model.encode([f"query: {user_input}"], normalize_embeddings=True)
    distances, indices = index.search(np.array(query, dtype="float32"), k=3)

    # Fetch top 3 chunks
    top_chunks = [texts[i] for i in indices[0] if i < len(texts)]

    # Generate answer using RAG
    if top_chunks:
        answer = generate_rag_response(user_input, top_chunks)
        return jsonify({"response": answer})
    else:
        return jsonify({"response": "❌ Sorry, I couldn't find relevant information for that."})

# === Run Server ===
if __name__ == "__main__":
    app.run(debug=True)
