# 🌍 Culture Sense – GenAI-Powered Cultural Translator (RAG App)

**Culture Sense** is a fun and intelligent GenAI-powered app that helps you understand how phrases, idioms, jokes, or gestures may be interpreted across cultures. It uses a **Corrective RAG (Retrieval-Augmented Generation)** approach — retrieving responses from a local vector database and falling back to **web search** when local context is insufficient.

> ✅ Built using: Streamlit · LangChain · OpenAI · SerpAPI · FAISS

---

## 🎯 What It Does

- ✍️ **Input**: A phrase, idiom, gesture, or joke
- 🌐 **Select**: A culture of interest (e.g., China, India, USA, etc.)
- 📚 **Retrieval**:
  - Checks a local cultural knowledge base (via vector DB + RAG)
  - If not sufficient, performs real-time **web search** fallback
- 🧠 **Response**: Returns cultural insights with the **source clearly labeled**

---

## 🧪 Example

> **Input**: “Wearing red at a funeral in China”

🧠 Response:
> Wearing red at a funeral in China would be considered inappropriate and disrespectful. It’s important to understand color symbolism in different cultures.

🔎 Source: `📚 Local Knowledge Base`

---

## 🖼️ Demo

  
watch this attached demo video in the repo [Video](assets/cultural_translator.mov)

---

## 🧰 Tech Stack

- [LangChain](https://www.langchain.com/) for RAG pipelines
- [OpenAI API](https://platform.openai.com/) (supports GPT-4, o4-mini, etc.)
- [FAISS](https://github.com/facebookresearch/faiss) for vector store
- [SerpAPI](https://serpapi.com/) for Google web fallback
- [Streamlit](https://streamlit.io/) for interactive UI
- `.env` for secure key management

---

## 📂 Project Structure

```

culture-sense-rag/
│
├── app.py                # Streamlit application
├── data/
│   └── Cultural\_Translator\_Data.docx
├── .env.example          # Sample env file (do not commit secrets)
├── requirements.txt      # Python dependencies
├── README.md             # You're reading this
└── assets/               # Optional: screenshots, videos

````

---

## 🚀 Run Locally

```bash
git clone https://github.com/your-username/culture-sense-rag.git
cd culture-sense-rag
pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI & SerpAPI keys
streamlit run app.py
````

---

## 🔐 .env Format

```
OPENAI_API_KEY=your-openai-key
SERPAPI_API_KEY=your-serpapi-key
```

---
