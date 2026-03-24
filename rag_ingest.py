"""
Telecom Proposal Engine - Hybrid RAG Ingestion
Builds:
1. Chroma vector DB (MiniLM embeddings)
2. BM25 chunk store
"""

import os
import pickle
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import CHROMA_DIR, BM25_STORE, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, RAG_DATA_DIR


def build_hybrid_store(documents: list[Document], reset_db: bool = True):
    """
    documents: list of LangChain Document objects
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)

    os.makedirs(os.path.dirname(BM25_STORE), exist_ok=True)

    # Save chunks for BM25
    with open(BM25_STORE, "wb") as f:
        pickle.dump(chunks, f)

    # Rebuild Chroma if requested
    if reset_db and os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    return {
        "num_chunks": len(chunks),
        "chroma_dir": CHROMA_DIR,
        "bm25_store": BM25_STORE
    }


def run_ingestion() -> bool:
    """Scan rag_data/ for documents, build hybrid BM25+Chroma stores. Returns True on success."""
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from rag_retriever import clear_cache

    if not os.path.exists(RAG_DATA_DIR):
        return False

    docs = []
    for fname in os.listdir(RAG_DATA_DIR):
        fpath = os.path.join(RAG_DATA_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        try:
            if fname.lower().endswith(".pdf"):
                docs.extend(PyPDFLoader(fpath).load())
            elif fname.lower().endswith(".txt"):
                docs.extend(TextLoader(fpath, encoding="utf-8").load())
        except Exception as e:
            print(f"⚠️ Skipped {fname}: {e}")

    if not docs:
        return False

    build_hybrid_store(docs)
    clear_cache()
    return True