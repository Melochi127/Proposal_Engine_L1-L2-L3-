"""
Telecom Proposal Engine - Hybrid RAG Retriever
BM25 + MiniLM + Chroma  (manual reciprocal rank fusion, no EnsembleRetriever)
"""

import os
import pickle
from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from config import CHROMA_DIR, BM25_STORE, EMBEDDING_MODEL


def check_kb():
    chroma_exists = os.path.exists(CHROMA_DIR)
    bm25_exists = os.path.exists(BM25_STORE)

    count = 0
    if bm25_exists:
        try:
            with open(BM25_STORE, "rb") as f:
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
        return pickle.load(f)


@lru_cache(maxsize=1)
def _load_vectordb():
    if not os.path.exists(CHROMA_DIR):
        return None
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=load_embeddings()
    )


def _reciprocal_rank_fusion(bm25_docs, dense_docs, k=60, bm25_weight=0.6, dense_weight=0.4):
    """Merge two ranked lists using weighted reciprocal rank fusion."""
    scores = {}
    doc_map = {}

    for rank, doc in enumerate(bm25_docs):
        key = doc.page_content[:100]
        scores[key] = scores.get(key, 0) + bm25_weight * (1 / (k + rank + 1))
        doc_map[key] = doc

    for rank, doc in enumerate(dense_docs):
        key = doc.page_content[:100]
        scores[key] = scores.get(key, 0) + dense_weight * (1 / (k + rank + 1))
        doc_map[key] = doc

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_map[key] for key, _ in ranked]


def retrieve_context(query, max_docs=4):
    try:
        bm25_docs = []
        dense_docs = []

        chunks = _load_bm25_chunks()
        if chunks:
            bm25 = BM25Retriever.from_documents(chunks)
            bm25.k = max_docs * 2
            bm25_docs = bm25.invoke(query)

        vectordb = _load_vectordb()
        if vectordb:
            dense_docs = vectordb.similarity_search(query, k=max_docs * 2)

        if bm25_docs and dense_docs:
            docs = _reciprocal_rank_fusion(bm25_docs, dense_docs)
        elif bm25_docs:
            docs = bm25_docs
        elif dense_docs:
            docs = dense_docs
        else:
            return "", []

        docs = docs[:max_docs]
        context = "\n\n".join(doc.page_content for doc in docs)
        return context, docs

    except Exception as e:
        print(f"⚠️ Retrieval error: {e}")
        return "", []


def clear_cache():
    """Call after re-ingestion so new data is picked up."""
    load_embeddings.cache_clear()
    _load_bm25_chunks.cache_clear()
    _load_vectordb.cache_clear()
