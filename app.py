from flask import Flask, render_template, request, jsonify
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# === Load Sentence Transformer Model and FAISS Index ===
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("mosdac_index.faiss")

with open("mosdac_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"response": "Please enter a valid question."})

    try:
        # Step 1: Embed query
        query_vec = model.encode([user_input])

        # Step 2: Search top 3 results
        top_k = 3
        distances, indices = index.search(np.array(query_vec), top_k)

        # Step 3: Define junk to skip
        junk_phrases = [
            "Website owned and maintained by",
            "Ver 3.0; Last reviewed",
            "Govt. of INDIA",
            "Served By: Web-Srv-Pri"
        ]

        # Step 4: Pick best non-junk, meaningful response
        best_score = float("inf")
        best_match = None

        for dist, idx in zip(distances[0], indices[0]):
            entry = metadata[idx]
            text = entry.get("text", "")

            if len(text) < 60:
                continue

            if any(junk.lower() in text.lower() for junk in junk_phrases):
                continue

            if dist < best_score:
                best_score = dist
                best_match = entry

        # Step 5: Fallback if nothing good found
        if not best_match:
            best_match = metadata[indices[0][0]]

        response = best_match["text"]

        if "source" in best_match:
            response += f"\n\n📎 Source: {best_match['source']}"

        return jsonify({"response": response})

    except Exception as e:
        print("❌ Internal error:", e)
        return jsonify({"response": "Sorry, an error occurred while processing your request."})

if __name__ == "__main__":
    app.run(debug=True)
