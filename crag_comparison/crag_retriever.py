"""
CRAG Retriever — Corrective Retrieval-Augmented Generation
Builds on hybrid BM25 + MiniLM with corrective filtering using Gemini.
"""

import os
from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_google_genai import ChatGoogleGenerativeAI
from config import CHROMA_DIR, BM25_STORE, EMBEDDING_MODEL, GOOGLE_API_KEY, GEMINI_MODEL


def check_kb():
    chroma_exists = os.path.exists(CHROMA_DIR)
    bm25_exists = os.path.exists(BM25_STORE)

    count = 0
    if bm25_exists:
        try:
            with open(BM25_STORE, "rb") as f:
                import pickle
                chunks = pickle.load(f)
                count = len(chunks)
        except Exception:
            count = 0

    return {
        "exists": chroma_exists and bm25_exists,
        "count": count
    }


@lru_cache(maxsize=1)
def load_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def _load_bm25_chunks():
    if not os.path.exists(BM25_STORE):
        return []
    with open(BM25_STORE, "rb") as f:
        import pickle
        return pickle.load(f)


@lru_cache(maxsize=1)
def _load_vectordb():
    if not os.path.exists(CHROMA_DIR):
        return None
    embeddings = load_embeddings()
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)


def retrieve_hybrid(query, top_k=5):
    """Hybrid retrieval: BM25 + Vector, fused."""
    bm25_chunks = _load_bm25_chunks()
    if bm25_chunks:
        bm25_texts = [doc.page_content for doc in bm25_chunks]
        bm25_retriever = BM25Retriever.from_texts(bm25_texts)
        bm25_results = bm25_retriever.invoke(query)[:top_k]
    else:
        bm25_results = []

    vectordb = _load_vectordb()
    if vectordb:
        vector_results = vectordb.similarity_search(query, k=top_k)
    else:
        vector_results = []

    # Simple fusion: combine and dedupe
    all_docs = bm25_results + vector_results
    seen = set()
    fused = []
    for doc in all_docs:
        if doc.page_content not in seen:
            fused.append(doc)
            seen.add(doc.page_content)
        if len(fused) >= top_k:
            break
    return fused[:top_k]


def correct_retrieval(query, docs):
    """Corrective step: Use Gemini to filter/re-rank docs for relevance."""
    if not GOOGLE_API_KEY:
        return docs  # Fallback to original

    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, api_key=GOOGLE_API_KEY)

    prompt = f"""
    Query: {query}
    Retrieved documents: {[doc.page_content[:200] for doc in docs]}

    Evaluate each document's relevance to the query on a scale of 1-10.
    Return only the top 3 most relevant documents, with their scores.
    Format: Document index (0-based), Score, Brief reason.
    """

    response = llm.invoke(prompt)
    # Parse response (simplified: assume LLM returns structured text)
    corrected = []
    for line in response.content.split('\n'):
        if 'Document' in line:
            # Extract index and score
            parts = line.split(',')
            if len(parts) >= 2:
                idx = int(parts[0].split()[-1])
                score = float(parts[1].strip())
                if score > 5 and idx < len(docs):  # Threshold
                    corrected.append(docs[idx])
    return corrected[:3]  # Top 3


def retrieve_crag(query, top_k=5):
    """CRAG: Retrieve hybrid, then correct."""
    initial_docs = retrieve_hybrid(query, top_k=top_k)
    # corrected_docs = correct_retrieval(query, initial_docs)
    corrected_docs = initial_docs  # Skip correction for now
    return corrected_docs