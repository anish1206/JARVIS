import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Load scraped data
with open("mosdac_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Load model (you can upgrade to BGE-small later)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Get texts to embed
texts = [entry.get("text", "") for entry in data]
embeddings = model.encode(texts, show_progress_bar=True)

# Create FAISS index
dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save index and metadata
faiss.write_index(index, "mosdac_index.faiss")

with open("mosdac_metadata.pkl", "wb") as f:
    pickle.dump(data, f)

print(f"✅ Built FAISS index for {len(data)} entries.")
