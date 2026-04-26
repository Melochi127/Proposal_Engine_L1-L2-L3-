"""
Dark Fibre Engine - Configuration & Environment
================================================

Centralizes all configurable settings: paths, API keys, model names,
and RAG hyperparameters. Loads environment variables from .env file.

Key Configuration Areas:
    1. API Integration: Google Gemini API credentials and model selection
    2. RAG Paths: ChromaDB vector store and BM25 index locations
    3. Embedding Model: HuggingFace sentence-transformers model selection
    4. Chunking: Document chunk size and overlap for RAG ingestion
    
Environment Variables (from .env):
    - GOOGLE_API_KEY: Required. Your Google Cloud API key for Gemini
    
File Structure:
    - RAG_DATA_DIR: ./rag_data/ (reference documents)
    - CHROMA_DIR: ./rag_data/chroma_db/ (vector database)
    - BM25_STORE: ./rag_data/bm25_chunks.pkl (keyword index)
    
Usage:
    >>> from config import GOOGLE_API_KEY, EMBEDDING_MODEL, CHUNK_SIZE
    >>> print(f"Using {EMBEDDING_MODEL} with chunk size {CHUNK_SIZE}")
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (must be in project root)
load_dotenv()

# Get base directory for relative path references
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ━━━ RAG Data & Storage Paths ━━━━━━━━━━━━━━━━━━
RAG_DATA_DIR = os.path.join(BASE_DIR, "rag_data")
CHROMA_DIR = os.path.join(RAG_DATA_DIR, "chroma_db")
BM25_STORE = os.path.join(RAG_DATA_DIR, "bm25_chunks.pkl")

# ━━━ LLM Configuration (Google Gemini) ━━━━━━━━━
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
"""
Google Cloud API key for Gemini 2.5 Flash access.
Required to run the proposal engine.
Get from: https://ai.google.dev/
Set in: .env file as GOOGLE_API_KEY=your_key_here
"""

GEMINI_MODEL = "gemini-2.5-flash"
"""
Google Gemini model identifier for LLM tasks.
Fallback: uses gemini-2.5-flash if gem 2.5-flash-preview unavailable.
"""

# ━━━ Embeddings Configuration (HuggingFace) ━━━━
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
"""
HuggingFace sentence-transformers model for dense semantic embeddings.
- Outputs: 384-dimensional vectors
- Speed: Very fast inference (~5ms per chunk)
- Quality: Excellent for technical/legal domain
- Size: ~90MB (downloaded on first use, cached locally)
"""

# ━━━ RAG Chunking Hyperparameters ━━━━━━━━━━━━━
CHUNK_SIZE = 800
"""
Number of characters per document chunk.
Larger = more context per chunk, fewer chunks. Recommended: 500-1000.
"""

CHUNK_OVERLAP = 150
"""
Number of overlapping characters between adjacent chunks.
Prevents clause boundaries from being cut off.
Typically 10-20% of CHUNK_SIZE.
"""
