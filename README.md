# 🩺 Medical Context Retriever (Hackathon Prototype)

This project is a **prototype module** from a larger **medical chatbot** built for the **IIIT Gwalior Hacksagon Hackathon**.  
The full chatbot included:
- **Intent classification**
- **Sentiment analysis**
- **Context-aware multi-turn conversation**
- A polished **frontend UI**

This repo focuses on the **semantic context retriever** module, which finds trusted WHO health information matching a user’s question using **PubMedBERT embeddings**, **FAISS vector similarity search**, and **SQLite**.

---

## 🔍 Dual Context Retrieval System

This prototype uses a **dual-retrieval system**:
- **Short, crisp context:** Extracted keywords and summaries — symptoms, causes, treatments — for quick, factual responses.
- **Full descriptive context:** Detailed paragraphs from WHO factsheets — deeper explanations, patterns, diagnosis, and self-care.

Both datasets were **scraped and cleaned** from WHO public health sources and stored in a local SQLite database.

---

## 🚀 Features

✅ Semantic similarity search with **transformer-based embeddings**  
✅ Vector indexing with **FAISS**  
✅ Dual source context: **briefs + factsheets**  
✅ Local **SQLite** for trusted storage  
✅ Minimal **Streamlit UI** for interactive queries

---

## ⚙️ How it works

1️⃣ **`setup_sqlite.py`** — creates the SQLite database with both context tables (briefs & factsheets).  
2️⃣ **`create_faiss_index.py`** — embeds all text chunks and builds the vector index + ID mapping.  
3️⃣ **`retriever.py`** — handles query embedding, FAISS search, and pulls matching context from the correct source.  
4️⃣ **`app.py`** — simple **Streamlit** interface to test questions and view retrieved context.

---

## ▶️ Quick Start

**1. Clone this repo**

```bash
git clone https://github.com/YOUR_USERNAME/medical-context-retriever.git
cd chat.e-context_retriever
