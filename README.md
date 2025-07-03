# 🌐 JARVIS: AI-Powered Help Bot for the MOSDAC Portal

## 🚀 Bharatiya Antariksh Hackathon 2025

### 👥 Team Stark Agents

- **Anish Kshirsagar** – NLP & Backend Integration
- **Khush Jain** – Knowledge Graph, Document Search
- **Prathamesh Kamble** – Geospatial Intelligence & Automation



## 📌 Problem Statement

Create an **AI-based Help Bot** that retrieves information from a **Knowledge Graph** generated using static and dynamic content available on the **MOSDAC portal**. JARVIS will assist users in querying and exploring satellite data, documents, and insights easily.



## 💡 Project Overview

JARVIS is a next-gen AI-powered assistant for the MOSDAC portal with:

- **Natural language understanding**
- **Document & data parsing**
- **Geospatial insights**
- **Knowledge graph visualization**
- **Dual interaction interface** (chatbot + visual explorer)



## 🧩 Features

### 🔍 JARVIS Bot
- Understands plain English queries like:
  - “Show me rainfall data for Maharashtra in 2023”
- Retrieves documents, FAQs, datasets, and maps
- Displays responses with:
  - Snippets, charts, maps, document previews

### 🧠 Knowledge Graph
- Built from document links, regions, satellites, and datasets
- Visual explorer using D3.js / PyVis
- Allows users to explore connections between content

### 🗺️ Geo-Intelligent Answers
- Map visualizations using Leaflet.js
- Filters and extracts data using GeoPandas

### 🔄 Dual Data Pipelines
- Static: Weekly crawling of PDFs & FAQs
- Live: Hourly fetch of weather/rainfall data from APIs



## ⚙️ Technologies Used

| Module                 | Tools & Libraries                              |
|------------------------|-----------------------------------------------|
| NLP & Chatbot          | spaCy, LangChain, NLTK, Sentence Transformers |
| Document Parsing       | PyMuPDF, pdfminer.six, python-docx            |
| Vector DB Retrieval    | FAISS, ChromaDB                                |
| Knowledge Graph        | NetworkX, Neo4j, PyVis, D3.js                  |
| Geospatial Processing  | GeoPandas, Leaflet.js, Shapely                |
| Frontend (UI)          | Streamlit                                     |
| Backend / APIs         | Flask, FastAPI                                |
| Crawling / Automation  | BeautifulSoup, Requests, Selenium, Scrapy     |
| Scheduling             | cron, APScheduler                             |
