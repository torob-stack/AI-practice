# 🧠 AI Business Systems Prototypes

This repo contains two small prototype projects I built to explore **practical AI for business systems** in preparation for my interview with Bet365.  
Both focus on **retrieval-augmented generation (RAG)** and **prompt engineering** for structured, business-ready outputs.

---

## 📂 Projects

### 1️⃣ RAG Chatbot (`rag_chatbot.py`)
- Loads a PDF (e.g., job description, company policy, documentation).  
- Splits into chunks → embeds into a vector database (Chroma).  
- Lets you ask **questions about the document**.  
- Returns answers in **structured JSON** (answer, summary, sources).  

**Why it matters:**  
This demonstrates how a chatbot can be grounded in company-specific documents. It shows how AI can provide reliable, source-backed answers rather than hallucinations, and produce structured outputs suitable for business integration.

---

### 2️⃣ Prompt Playground (`prompt_playground.py`)
- Experiments with **prompt engineering patterns**:  
  - **Summarization** → concise bullet points  
  - **Extraction** → strict JSON schema (skills, frameworks, topics)  
  - **Classification** → fixed labels with rationale  
  - **Formatting** → Markdown tables  

**Why it matters:**  
Most business data is unstructured text. This playground shows how to **transform unstructured inputs into predictable, structured outputs** that can be integrated into databases, workflows, or dashboards.

---

## 📖 Learnings
- **RAG**: improves reliability by grounding LLMs in real documents.  
- **Low temperature (0.1)**: produces deterministic, structured outputs rather than creative variance.  
- **Prompt engineering**: enables structured outputs (JSON/tables) that business systems can reliably consume.  
- **Security awareness**: API keys kept local only, would be handled via env vars/secret managers in production.  

---

## 🚀 Future Improvements
- Wrap the RAG bot in a simple web UI (e.g., Streamlit) for non-technical users.  
- Add error handling and logging for robustness.  
- Integrate with enterprise-grade vector databases (Pinecone, Weaviate, etc.).  
- Explore evaluation metrics for RAG accuracy and prompt effectiveness.  

---
