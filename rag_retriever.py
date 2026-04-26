"""
Telecom Proposal Engine - Hybrid RAG Retriever
===============================================

Implements hybrid document retrieval combining BM25 (keyword-based) and
semantic (dense embedding) search with weighted reciprocal rank fusion.

This module provides the backbone for the Retrieval-Augmented Generation
system that pulls relevant telecom contract clauses and guidelines to inform
the LLM responses.

Architecture:
    BM25 Retriever (60% weight)  ─────┐
                                       ├─→ Reciprocal Rank Fusion ─→ Top-K Results
    MiniLM Dense Embeddings (40%)  ───┘
    via ChromaDB vector store

Module Functions:
    - check_kb(): Verify knowledge base is initialized
    - load_embeddings(): Get cached HuggingFace embeddings
    - retrieve_context(): Main retrieval function (returns context + docs)
    - clear_cache(): Invalidate caches after data ingestion
    
Key Components:
    - BM25Retriever: Keyword-based ranking (good for technical terms)
    - Chroma: Vector database (good for semantic meaning)
    - Reciprocal Rank Fusion: Combines both, re-ranks, deduplicates
    
Dependencies:
    - langchain_huggingface: HuggingFace embeddings
    - langchain_community: BM25 retriever and Chroma vector store
    - config: Directory and model configuration
"""

import os
import pickle
from functools import lru_cache
from typing import List, Tuple, Optional, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from config import CHROMA_DIR, BM25_STORE, EMBEDDING_MODEL


def check_kb() -> Dict[str, Any]:
    """
    Check if knowledge base (ChromaDB + BM25 index) is initialized.
    
    Verifies both the vector database and BM25 keyword index exist.
    Used by the UI to prompt for data ingestion if not ready.
    
    Returns:
        Dict with keys:
            - exists (bool): True if both DB and BM25 index present
            - count (int): Number of chunks in BM25 index (0 if missing)
            
    Examples:
        >>> kb = check_kb()
        >>> kb["exists"]
        True
        >>> kb["count"]
        320
        
    Error Handling:
        Gracefully handles corrupted pickle files, returns count=0 if unreadable.
    """
    chroma_exists = os.path.exists(CHROMA_DIR)
    bm25_exists = os.path.exists(BM25_STORE)

    count = 0
    if bm25_exists:
        try:
            with open(BM25_STORE, "rb") as f:
                chunks = pickle.load(f)
                count = len(chunks)
        except (pickle.PickleError, EOFError, IOError):
            # Corrupted pickle file - treat as non-existent
            count = 0

    return {
        "exists": chroma_exists and bm25_exists,
        "count": count
    }


@lru_cache(maxsize=1)
def load_embeddings() -> HuggingFaceEmbeddings:
    """
    Load and cache HuggingFace MiniLM-L6-v2 embedding model.
    
    Uses LRU cache to avoid reloading the ~100MB model on every request.
    Cache is invalidated by clear_cache() after data ingestion.
    
    Returns:
        HuggingFaceEmbeddings: Initialized embeddings model (sentence-transformers)
        
    Examples:
        >>> embeddings = load_embeddings()
        >>> vec = embeddings.embed_query("What is Dark Fibre?")
        >>> len(vec)
        384  # MiniLM outputs 384-dimensional vectors
        
    Performance:
        First call: ~5s (model download/load)
        Subsequent calls: <1ms (cached)
    """
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def _load_bm25_chunks() -> List[Document]:
    """
    Load and cache BM25 index (pickled document chunks).
    
    BM25 uses pre-chunked documents stored in pickle format for fast
    keyword-based retrieval without needing a separate index engine.
    
    Returns:
        List[Document]: All chunks loaded from BM25 pickle file
        
    Internal Use:
        Called by retrieve_context() to initialize BM25Retriever
        
    Cache Management:
        Cached by LRU cache. Clear with clear_cache() after ingestion.
    """
    if not os.path.exists(BM25_STORE):
        return []
    try:
        with open(BM25_STORE, "rb") as f:
            return pickle.load(f)
    except (pickle.PickleError, EOFError, IOError):
        return []


@lru_cache(maxsize=1)
def _load_vectordb() -> Optional[Chroma]:
    """
    Load and cache Chroma vector database.
    
    Connects to persisted ChromaDB vector store containing embedded chunks.
    Uses same embeddings model as dense retrieval component.
    
    Returns:
        Optional[Chroma]: Vector database instance, or None if not found
        
    Internal Use:
        Called by retrieve_context() for semantic similarity search
        
    Cache Management:
        Cached by LRU cache. Clear with clear_cache() after ingestion.
    """
    if not os.path.exists(CHROMA_DIR):
        return None
    try:
        return Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=load_embeddings()
        )
    except Exception:
        return None


def _reciprocal_rank_fusion(
    bm25_docs: List[Document],
    dense_docs: List[Document],
    k: int = 60,
    bm25_weight: float = 0.6,
    dense_weight: float = 0.4
) -> List[Document]:
    """
    Merge two ranked document lists using weighted reciprocal rank fusion.
    
    Combines BM25 (keyword relevance) and dense (semantic relevance) ranking
    into a single unified rankingthat balances both signals.
    
    Algorithm:
        score(doc) = bm25_weight * (1/(k+rank_bm25+1)) + dense_weight * (1/(k+rank_dense+1))
        
        Reciprocal rank formula (a) dampens high-rank documents (b) combines
        multiple signals fairly (c) deduplicates identical documents
        
    Args:
        bm25_docs (List[Document]): Documents ranked by BM25 keyword search
        dense_docs (List[Document]): Documents ranked by semantic similarity
        k (int): Damping factor (default 60). Higher k = lower weight for high ranks
        bm25_weight (float): Weight for BM25 scores (default 0.6 = 60%)
        dense_weight (float): Weight for dense scores (default 0.4 = 40%)
        
    Returns:
        List[Document]: Merged list ranked by combined score, descending
        
    Examples:
        >>> from langchain_schema import Document
        >>> bm25 = [Document(page_content="A"), Document(page_content="B")]
        >>> dense = [Document(page_content="B"), Document(page_content="C")]
        >>> merged = _reciprocal_rank_fusion(bm25, dense)
        >>> len(merged) <= 4  # At most 4, could deduplicate
        True
        
    Deduplication:
        Documents are deduplicated by first 100 characters of content.
        Helps avoid multiple retrievals of same passage.
    """
    scores: Dict[str, float] = {}
    doc_map: Dict[str, Document] = {}

    # Score BM25 results
    for rank, doc in enumerate(bm25_docs):
        # Use first 100 chars as unique key (deduplication)
        key = doc.page_content[:100]
        scores[key] = scores.get(key, 0) + bm25_weight * (1 / (k + rank + 1))
        doc_map[key] = doc

    # Score dense results and accumulate with BM25 scores
    for rank, doc in enumerate(dense_docs):
        key = doc.page_content[:100]
        scores[key] = scores.get(key, 0) + dense_weight * (1 / (k + rank + 1))
        doc_map[key] = doc

    # Sort by combined scores, return documents in order
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_map[key] for key, _ in ranked]


def retrieve_context(query: str, max_docs: int = 4) -> Tuple[str, List[Document]]:
    """
    Retrieve relevant context for a user query using hybrid retrieval.
    
    Main function for RAG context retrieval. Queries both BM25 and dense
    indexes, fuses results, and returns top-K documents as formatted text.
    
    Retrieval Strategy:
        1. BM25 retrieval (keyword + frequency based)
        2. Dense semantic similarity search
        3. Reciprocal rank fusion with (60% BM25, 40% dense)
        4. Return top K documents + concatenated context string
        
    Args:
        query (str): User question or search term
        max_docs (int): Maximum number of documents to return (default 4)
        
    Returns:
        Tuple[str, List[Document]]:
            - str: Concatenated document contents for LLM context
            - List[Document]: Individual documents (with metadata)
            
    Examples:
        >>> context, docs = retrieve_context("What is wayleave?")
        >>> len(docs) <= 4
        True
        >>> "wayleave" in context.lower() or len(context) > 0
        True
        
    Fallback Behavior:
        - If both BM25 and dense fail: return ("", [])
        - If only BM25 works: use BM25 results only
        - If only dense works: use dense results only
        
    Error Handling:
        Catches and logs retrieval errors, returns empty context gracefully
        so the LLM continues without context rather than crashing.
    """
    try:
        bm25_docs: List[Document] = []
        dense_docs: List[Document] = []

        # Attempt BM25 keyword retrieval
        chunks = _load_bm25_chunks()
        if chunks:
            bm25 = BM25Retriever.from_documents(chunks)
            bm25.k = max_docs * 2  # Over-retrieve, will trim after fusion
            bm25_docs = bm25.invoke(query)

        # Attempt dense semantic retrieval
        vectordb = _load_vectordb()
        if vectordb:
            dense_docs = vectordb.similarity_search(query, k=max_docs * 2)

        # Combine results via reciprocal rank fusion
        if bm25_docs and dense_docs:
            docs = _reciprocal_rank_fusion(bm25_docs, dense_docs)
        elif bm25_docs:
            docs = bm25_docs
        elif dense_docs:
            docs = dense_docs
        else:
            # No retrieval possible - return empty context
            return "", []

        # Trim to requested max_docs
        docs = docs[:max_docs]
        
        # Format context as concatenated document text
        context = "\n\n".join(doc.page_content for doc in docs)
        return context, docs

    except Exception as e:
        # Log error but don't fail - LLM continues without context
        print(f"⚠️ Retrieval error: {e}")
        return "", []


def clear_cache() -> None:
    """
    Clear all LRU caches to force reload of knowledge base.
    
    Call this function after running rag_ingest.py to pickup newly
    ingested documents. Otherwise, old cached index will be used.
    
    Usage:
        >>> from rag_ingest import run_ingestion
        >>> run_ingestion()  # Ingest documents
        >>> clear_cache()    # Force reload of new index
        >>> context, docs = retrieve_context("test query")
        
    Performance Impact:
        Slight performance cost on next retrieve_context() call as indexes
        must be reloaded from disk (~2-5s for models and indexes).
    """
    load_embeddings.cache_clear()
    _load_bm25_chunks.cache_clear()
    _load_vectordb.cache_clear()
