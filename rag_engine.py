"""
Telecom Proposal Engine - Hybrid Retrieval
BM25 + MiniLM (Chroma)
"""

import os
import pickle
from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from config import CHROMA_DIR, BM25_STORE, EMBEDDING_MODEL


@lru_cache(maxsize=1)
def load_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def load_bm25_retriever():
    if not os.path.exists(BM25_STORE):
        raise FileNotFoundError(f"BM25 store not found: {BM25_STORE}")

    with open(BM25_STORE, "rb") as f:
        chunks = pickle.load(f)

    retriever = BM25Retriever.from_documents(chunks)
    retriever.k = 4
    return retriever


@lru_cache(maxsize=1)
def load_dense_retriever():
    if not os.path.exists(CHROMA_DIR):
        raise FileNotFoundError(f"Chroma DB not found: {CHROMA_DIR}")

    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=load_embeddings()
    )

    return vectordb.as_retriever(search_kwargs={"k": 4})


def load_hybrid_retriever():
    bm25 = load_bm25_retriever()
    dense = load_dense_retriever()

    return EnsembleRetriever(
        retrievers=[bm25, dense],
        weights=[0.6, 0.4]
    )


def retrieve_context(query, max_docs=4):
    retriever = load_hybrid_retriever()
    docs = retriever.invoke(query)
    docs = docs[:max_docs]

    context = "\n\n".join(doc.page_content for doc in docs)
    return context, docs