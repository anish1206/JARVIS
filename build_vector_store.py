from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

# Load data
with open("mosdac_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["text"] for item in data]
sources = [item["source"] for item in data]

# Load improved embedding model
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Required for bge
queries = [f"query: {text}" for text in texts]
embeddings = model.encode(queries, convert_to_numpy=True, normalize_embeddings=True).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "mosdac_index.faiss")

# Save metadata
with open("mosdac_metadata.json", "w", encoding="utf-8") as f:
    json.dump({"texts": texts, "sources": sources}, f, ensure_ascii=False, indent=2)

print(f"✅ Saved {len(texts)} vectors and metadata.")
