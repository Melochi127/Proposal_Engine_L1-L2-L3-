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
    from langchain_community.document_loaders import (
        PyPDFLoader,
        TextLoader,
        Docx2txtLoader,
        UnstructuredWordDocumentLoader,
    )
    from rag_retriever import clear_cache

    print(f"RAG_DATA_DIR = {RAG_DATA_DIR}")

    if not os.path.exists(RAG_DATA_DIR):
        print("❌ rag_data folder does not exist.")
        return False

    docs = []
    files = os.listdir(RAG_DATA_DIR)
    print(f"Found {len(files)} files in rag_data")

    for fname in files:
        fpath = os.path.join(RAG_DATA_DIR, fname)

        if not os.path.isfile(fpath):
            continue

        print(f"Processing: {fname}")

        try:
            if fname.lower().endswith(".pdf"):
                loaded = PyPDFLoader(fpath).load()
                docs.extend(loaded)
                print(f"  Loaded PDF pages: {len(loaded)}")

            elif fname.lower().endswith(".txt"):
                loaded = TextLoader(fpath, encoding="utf-8").load()
                docs.extend(loaded)
                print(f"  Loaded TXT docs: {len(loaded)}")

            elif fname.lower().endswith(".docx"):
                loaded = Docx2txtLoader(fpath).load()
                docs.extend(loaded)
                print(f"  Loaded DOCX docs: {len(loaded)}")

            elif fname.lower().endswith(".doc"):
                loaded = UnstructuredWordDocumentLoader(fpath).load()
                docs.extend(loaded)
                print(f"  Loaded DOC docs: {len(loaded)}")

            else:
                print(f"  Skipped unsupported file: {fname}")

        except Exception as e:
            print(f"⚠️ Skipped {fname}: {e}")

    print(f"Total loaded documents: {len(docs)}")

    if not docs:
        print("❌ No documents were loaded.")
        return False

    result = build_hybrid_store(docs)
    print(f"✅ Built {result['num_chunks']} chunks")
    print(f"✅ Chroma saved to: {result['chroma_dir']}")
    print(f"✅ BM25 saved to: {result['bm25_store']}")

    clear_cache()
    return True

if __name__ == "__main__":
    success = run_ingestion()
    if success:
        print("Ingestion completed successfully.")
    else:
        print("Ingestion failed. Check if rag_data/ exists and contains documents.")