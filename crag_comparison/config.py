"""
Dark Fibre Engine V3 - Config
"""
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

#BASE_DIR = Path(__file__).parent
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

RAG_DATA_DIR = os.path.join(PROJECT_ROOT, "rag_data")
CHROMA_DIR = os.path.join(RAG_DATA_DIR, "chroma_db")
BM25_STORE = os.path.join(RAG_DATA_DIR, "bm25_chunks.pkl")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"  # fallback if gemini-2.5-flash-preview is unavailable
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
