import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI  # Use o4-mini
from langchain.prompts import PromptTemplate

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Init LLM factory (using o4-mini)
def get_llm(tone_temp):
    return ChatOpenAI(
        model="gpt-4o",  # o4-mini maps to gpt-4o for now
        temperature=tone_temp,
        api_key=OPENAI_API_KEY,
        max_tokens=512,
        streaming=False
    )

# Embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Streamlit UI
st.set_page_config(page_title="Cultural Translator – RAG", layout="wide")
st.title("🌍 Cultural Translator – Corrective RAG")
st.write("Input a phrase, joke, or gesture to understand how it may be interpreted across cultures.")

# Tone slider
tone = st.slider("🎚️ Tone (Casual ↔ Formal)", 0.0, 1.0, 0.3, 0.1)

# Culture dropdown
culture = st.selectbox(
    "🌏 Optional: Select a culture of interest",
    ["All", "China", "India", "Japan", "USA", "France", "Germany", "Brazil", "Saudi Arabia", "South Africa"]
)

# Text input
query = st.text_input("🗣️ Enter a phrase, idiom, joke, or gesture:")

# Load vector DB (cached)
@st.cache_resource
def load_vectorstore():
    loader = Docx2txtLoader("data/Cultural_Translator_Data.docx")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    return FAISS.from_documents(chunks, embeddings)

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# QA chain with fallback prompt
qa_chain = RetrievalQA.from_chain_type(
    llm=get_llm(tone),
    retriever=retriever,
    return_source_documents=False
)

# Web search fallback tool
search_tool = Tool(
    name="WebSearch",
    func=SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY).run,
    description="Search the web for cultural meanings."
)

agent = initialize_agent(
    tools=[search_tool],
    llm=get_llm(tone),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# Process input
if query:
    search_query = f"{query} in {culture}" if culture != "All" else query
    st.write("🔍 Retrieving cultural interpretations...")

    # Try local RAG
    rag_response = qa_chain.run(search_query)

    # Fallback check
    fallback_reason = ""
    if not rag_response:
        fallback_reason = "❌ Local DB returned nothing."
    elif "i don't know" in rag_response.lower():
        fallback_reason = "🤷 LLM responded with 'I don't know'."
    elif len(rag_response.strip()) < 50:
        fallback_reason = f"🪶 Local answer too short: {len(rag_response.strip())} characters."

    # If fallback needed
    if fallback_reason:
        st.warning("Not enough local data. Using web search fallback...")
        st.info(f"🧾 Fallback Reason: {fallback_reason}")
        response = agent.run(f"How is this interpreted in {culture}: {query}")
        source = "🌐 Web Search (SerpAPI)"
    else:
        response = rag_response
        source = "📚 Local Knowledge Base"

    # Output
    st.markdown("### 🧠 Cultural Insight")
    st.write(response)
    st.markdown(f"**🔎 Source:** {source}")
