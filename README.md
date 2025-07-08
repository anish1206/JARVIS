# J.A.R.V.I.S: GeoAssist Chatbot for MOSDAC

A smart AI-powered assistant designed to simplify user interaction with the [MOSDAC Portal](https://www.mosdac.gov.in) by enabling natural language queries about satellites, rainfall, cloud data, geospatial information, and more.

---

## 🚀 Project Overview

**J.A.R.V.I.S (Just A Rather Very Intelligent System)** is a chatbot and data retrieval system that:

* Understands natural language queries
* Retrieves relevant data or document snippets from the MOSDAC portal
* Presents results in a clean, conversational format with optional sources or visuals


---

## 🔍 Features (Completed)

### ✅ 1. Fully Functional Chatbot Interface

* Built with **Flask** and **custom HTML/CSS/JS UI**
* Supports user input + bot responses
* Displays thinking animation during long responses
* 
![Screenshot 2025-07-08 203446](https://github.com/user-attachments/assets/cee67dd8-5c58-4ab1-9bee-0157be8506ba)


### ✅ 2. NLP Engine

* Uses **SentenceTransformers** for vector embedding
* Switchable backends: Ollama's **TinyLLaMA** or other open-source LLMs
* Smart keyword matching, context understanding

### ✅ 3. Static Content Vector Store

* **Scraper** crawls all internal MOSDAC links & PDFs
* **PDF text + webpage text** cleaned and chunked
* Stored in FAISS vector DB with source tagging

### ✅ 4. Query Response Engine

* Embeds user query, runs similarity search
* Fetches best matching chunk from FAISS
* Displays answer + source
* Handles greeting ("Hi", "Hello") gracefully


---

## ⏳ Features (Planned/In Progress)

### 🔹 Smart Live Data Fetching

* Automatically retrieve weather/cloud/rainfall datasets from public APIs or NetCDF/CSV
* Convert numerical data into natural language

### 🔹 Knowledge Graph Integration

* Build relationship graph between satellites, sensors, regions, documents using **NetworkX/Neo4j**
* Visualize with PyVis or D3.js

### 🔹 Geo-Intelligence Support

* Support region-aware queries
* Use **GeoPandas/Shapely** to filter datasets by region
* Add optional **Leaflet.js** maps to responses

### 🔹 Automated Update Pipelines

* **Pipeline 1**: Weekly crawl of documentation, PDFs, FAQ
* **Pipeline 2**: Hourly/daily live dataset polling
* Use `APScheduler` or cron jobs

---

## 🚀 Tech Stack

| Layer                     | Technologies Used                            |
| ------------------------- | -------------------------------------------- |
| Frontend                  | HTML, CSS, JS, Flask Templates               |
| Backend / API             | Flask, Python                                |
| NLP / Chat Engine         | Ollama (TinyLLaMA), SentenceTransformers     |
| Vector DB                 | FAISS                                        |
| Scraping / Extraction     | requests, BeautifulSoup, PyMuPDF, Playwright |
| Geospatial (Planned)      | GeoPandas, Shapely, Leaflet.js               |
| Knowledge Graph (Planned) | NetworkX, Neo4j                              |
| Automation                | cron, APScheduler (planned)                  |

---

## 📅 Current Status

| Module                   | Status    |
| ------------------------ | --------- |
| Chat UI + Response       | ✅ Done    |
| Static Crawler + FAISS   | ✅ Done    |
| PDF Extractor            | ✅ Done    |
| Ollama LLM Integration   | ✅ Done    |
| Smart Greeting/Typing UI | ✅ Done    |
| Live Data Polling        | ⏳ Pending |
| Knowledge Graph          | ⏳ Pending |
| Geo Processing           | ⏳ Pending |
| Feedback Learning        | ⏳ Pending |

---

## 📊 Example Queries

* "Tell me about INSAT-3DR"
* "Where can I get cloud data for July 2022?"
* "What are the payloads of Megha-Tropiques?"
* "Download rainfall info for Gujarat"
![Screenshot 2025-07-08 204236](https://github.com/user-attachments/assets/f89eecca-3575-45e0-9ae5-552357ded709)
---

## 🔧 Setup Instructions

```bash
# 1. Clone the repo
https://github.com/your-username/JARVIS-MOSDAC

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Flask app
python app.py
You'll see an URL (e.g. http://127.0.0.1:5000), run the URL on you local device.
```

Ensure `mosdac_data.json` and FAISS index (`mosdac_index.faiss`) are already built. If not, run the scraper:

```bash
python mosdac_scraper.py
python build_vector_store.py
```

---


## 💪 Team Credits

Made with passion for **ISRO Hackathon 2025** by Team \Stark Agents.
