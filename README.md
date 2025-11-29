# MARS — Multi-Agent Research & Summary Assistant

MARS is a multi-agent system that:

- Pulls **live online data** (news, sites, articles)
- Extracts and chunks text
- Stores information in a **vector memory database**
- Performs **semantic search + RAG (Retrieval-Augmented Generation)**
- Fact-checks content
- Produces clean, citation-based summaries

This project is designed for the **Google 5-day Agentic AI Intensive Capstone**.

---

## 🚀 Features

- Multi-agent architecture
- Research agent (live web search + scraping)
- Knowledge agent (chunk + embeddings + vector storage)
- Summary agent (RAG + LLM)
- Fact-checking agent
- Long-term memory with Chroma/FAISS
- Fully compatible with Kaggle Notebook submission

---

## 🧠 Project Structure

mars-capstone/
├── src/
│ ├── agents/ # All agents (research, knowledge, summary, fact-check)
│ ├── db/ # Vector DB adapters (Chroma)
│ ├── utils/ # Embeddings + helpers
│ └── init.py
│
├── notebooks/
│ └── demo_kaggle_live.ipynb # Kaggle submission notebook
│
├── docs/ # Architecture diagrams, screenshots
├── requirements.txt
└── README.md

---

## 🛠️ Installation (Local Development)

python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt

---

## ▶️ Running the Kaggle Demo

- Upload `notebooks/demo_kaggle_live.ipynb` to Kaggle
- Add API keys (SerpAPI, OpenAI/Gemini) via Kaggle “Add Environment Variables”
- Run all cells to demonstrate:
  - Live search → fetch → chunk
  - Embed → upsert → retrieve
  - RAG summary with citations

---

## 🤝 Contributing

- Work only on feature branches
- Open PRs into `dev`
- Require approval before merging
- Never commit directly to `main`

See **CONTRIBUTING.md** for details.

---

## 📄 License

Open for educational and capstone use only.
