# Installation Guide - Dark Fibre Framework Agreement Engine

Complete setup instructions for running the Proposal Engine locally or in production.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start (5 minutes)](#quick-start-5-minutes)
3. [Detailed Setup](#detailed-setup)
4. [Google Gemini API Setup](#google-gemini-api-setup)
5. [Knowledge Base Ingestion](#knowledge-base-ingestion)
6. [Verification & Testing](#verification--testing)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Hardware
- **CPU**: Dual-core processor (2+ GHz)
- **RAM**: 4GB minimum (8GB recommended for smooth operation)
- **Disk**: 2GB free space (includes 100MB for models + database)

### Software
- **Python**: Version 3.9 or higher
- **pip**: Python package manager (comes with Python)
- **Virtual Environment**: `venv` or `conda` (recommended)

### Operating Systems
- ✅ Linux (Ubuntu 20.04+, Debian, etc.)
- ✅ macOS (10.14+)
- ✅ Windows 10/11 (use PowerShell or cmd)

---

## Quick Start (5 minutes)

### 1. Clone or Download the Project

```bash
# If using git
git clone https://github.com/Melochi127/Proposal_Engine_L1-L2-L3-.git
cd Proposal_Engine_L1-L2-L3-

# Or extract the downloaded ZIP file
unzip dark_fiber_engine.zip
cd dark_fiber_engine
```

### 2. Create Python Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate venv (choose based on OS)
# Linux/macOS:
source venv/bin/activate

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Windows (Command Prompt):
venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output: "Successfully installed [23 packages]"

### 4. Configure Google API Key

```bash
# Create .env file in project root
cp .env.example .env

# Edit .env and add your Google API key
# Replace YOUR_API_KEY_HERE with actual key from Google Cloud Console
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

[→ See Google Gemini API Setup for detailed instructions](#google-gemini-api-setup)

### 5. Ingest Reference Documents

```bash
# Download/prepare reference documents (see Knowledge Base section)
python rag_ingest.py

# Expected output:
# Processing documents...
# ✓ Ingested 18 documents → 320 chunks
# ✓ Created ChromaDB index
# ✓ Created BM25 index
```

### 6. Launch the Application

```bash
streamlit run app.py

# Open browser to:
# http://localhost:8501
```

✅ **Done!** Application is running.

---

## Detailed Setup

### Step 1: Install Python

#### Linux/macOS
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv

# macOS (using Homebrew)
brew install python@3.11
```

#### Windows
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **Important**: Check "Add Python to PATH"
4. Click "Install Now"

Verify: `python --version` → Should show Python 3.9+

### Step 2: Create Virtual Environment

```bash
# Create venv directory
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows - PowerShell)
venv\Scripts\Activate.ps1

# Activate (Windows - Command Prompt)
venv\Scripts\activate.bat
```

Verify: Prompt should show `(venv)` prefix

### Step 3: Install Dependencies

```bash
# Upgrade pip first (recommended)
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify key packages
pip list | grep -E "streamlit|langchain|pydantic"
```

Expected result:
```
langchain==0.2.2
langchain-community==0.2.0
langchain-google-genai>=1.0.0
pydantic==2.0.0+
streamlit>=1.32.0
```

### Step 4: Verify Installation

```bash
python -c "import streamlit, langchain, pydantic, sentence_transformers; print('✓ All imports OK')"
```

Expected output: `✓ All imports OK`

---

## Google Gemini API Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a Project" → "NEW PROJECT"
3. Enter project name: `dark-fibre-engine`
4. Click "Create"

### Step 2: Enable Generative AI API

1. In console, search for "Generative AI API"
2. Click "Generative AI API"
3. Click "ENABLE"
4. Wait 1-2 minutes for enablement

### Step 3: Create API Key

1. Go to "Credentials" (left sidebar)
2. Click "CREATE CREDENTIALS" → "API Key"
3. Copy the generated key
4. Click "Restrict Key" (optional but recommended)

### Step 4: Configure in Project

Create or edit `.env` file in project root:

```env
GOOGLE_API_KEY=copy_your_api_key_here
```

**Do NOT commit `.env` to git** (security risk!)

### Step 5: Verify API Key

```bash
# Test API connectivity
python -c "
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY
if GOOGLE_API_KEY:
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', google_api_key=GOOGLE_API_KEY)
    print('✓ API Key valid')
else:
    print('✗ API Key not found')
"
```

---

## Knowledge Base Ingestion

### ⚖️ GDPR Compliance Note

**Reference documents are NOT included in the repository** due to GDPR compliance requirements. The original 18 Dark Fibre framework documents contain:
- Proprietary company agreements
- Confidential internal documentation
- Sensitive business logic and rules

**To run the system locally**: You must supply your own reference documents in the `rag_data/` directory.

---

### Step 1: Prepare Reference Documents

Place your reference documents in `rag_data/` directory:

```
rag_data/
├── your_document1.pdf
├── your_document2.docx
├── your_document3.txt
└── ... more documents
```

**Supported formats**:
- `.pdf` (PDF documents)
- `.docx` (Microsoft Word)
- `.doc` (Microsoft Word 97-2003)
- `.txt` (Plain text)

**Recommended**: At least 3-5 reference documents covering:
- Agreement templates
- Standard clauses
- Example contracts
- Guidelines or best practices

### Step 2: Run Ingestion Pipeline

```bash
python rag_ingest.py
```

**Process**:
1. Reads all documents from `rag_data/`
2. Extracts text and chunks (500 chars, 100 overlap)
3. Creates BM25 keyword index (→ `bm25_chunks.pkl`)
4. Creates ChromaDB vector store (→ `chroma_db/`)

**Output**:
```
Processing documents...
✓ Loaded 5 documents
✓ Created 120 chunks
✓ Indexed for BM25 (8.3 KB)
✓ Indexed for ChromaDB (vector store created)
✓ Knowledge base ingestion complete
```

**File sizes**:
- `bm25_chunks.pkl`: ~20-50 KB
- `chroma_db/`: ~50-100 MB (depends on embedding model)

### Step 3: Verify Ingestion

```bash
# Check knowledge base status
python -c "
from rag_retriever import check_kb
kb = check_kb()
print(f'KB exists: {kb[\"exists\"]}')
print(f'Chunks indexed: {kb[\"count\"]}')
"
```

Expected output:
```
KB exists: True
Chunks indexed: 320
```

### Step 4: Update After New Documents

If you add documents to `rag_data/`:

```bash
# Re-run ingestion
python rag_ingest.py

# Clear caches in app (automatic on load, or restart Streamlit)
# Ctrl+C to stop, then: streamlit run app.py
```

---

## Verification & Testing

### Test 1: Full System Check

```bash
python -c "
import sys
from config import GOOGLE_API_KEY, EMBEDDING_MODEL
from llm_engine import get_llm
from rag_retriever import check_kb

print('System Verification')
print('=' * 50)

# Check API Key
print(f'✓ Google API Key: {\"SET\" if GOOGLE_API_KEY else \"NOT SET\"}')

# Check Embedding Model
print(f'✓ Embedding Model: {EMBEDDING_MODEL}')

# Check Knowledge Base
kb = check_kb()
print(f'✓ Knowledge Base: {kb[\"exists\"]} ({kb[\"count\"]} chunks)')

# Check LLM
try:
    llm = get_llm('chat')
    print(f'✓ LLM Model: {llm.model_name}')
except Exception as e:
    print(f'✗ LLM Error: {e}')

print('=' * 50)
print('All systems ready!')
"
```

Expected output:
```
System Verification
==================================================
✓ Google API Key: SET
✓ Embedding Model: sentence-transformers/all-MiniLM-L6-v2
✓ Knowledge Base: True (320 chunks)
✓ LLM Model: gemini-2.5-flash
==================================================
All systems ready!
```

### Test 2: Launch Application

```bash
streamlit run app.py
```

Open http://localhost:8501 and verify:
- ✓ UI loads without errors
- ✓ Can create new proposal
- ✓ Can select proposal level (L1/L2/L3)
- ✓ Can answer first question
- ✓ AI response appears

### Test 3: Quick Proposal Generation

1. Select **L1 (Quick)**
2. Answer all 8 questions
3. Click "Generate Proposal"
4. Verify proposal text appears

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'streamlit'"

**Solution**: Install requirements again
```bash
pip install -r requirements.txt
```

### Problem: "GOOGLE_API_KEY not set in environment"

**Solution**: Create `.env` file with API key
```bash
echo "GOOGLE_API_KEY=your_key_here" > .env
```

### Problem: "Knowledge base does not exist"

**Solution**: Run ingestion
```bash
python rag_ingest.py
```

### Problem: "Permission denied" on macOS/Linux

**Solution**: Add execute permission
```bash
chmod +x venv/bin/activate
```

### Problem: Port 8501 already in use

**Solution**: Use different port
```bash
streamlit run app.py --server.port=8502
```

### Problem: Slow response from LLM

**Cause**: First-time downloads (embeddings model, etc.)
**Solution**: Wait 2-3 minutes for initial setup. Subsequent requests will be fast.

### Problem: "Connection timeout" from Google API

**Solution**:
1. Check internet connection
2. Verify API key is valid (not revoked)
3. Check Google Cloud Console for API quota

### Problem: Chunks not retrieving relevant content

**Solution**: Re-ingest with better documents
```bash
# Remove old indexes
rm -rf rag_data/chroma_db
rm rag_data/bm25_chunks.pkl

# Add better reference documents to rag_data/
# Then re-ingest:
python rag_ingest.py
```

---

## Environment Variables

Complete list of supported environment variables (in `.env`):

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key

# Optional (defaults shown)
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=800
CHUNK_OVERLAP=150
```

---

## Production Deployment

For running on a server:

### Option 1: Docker Containerization (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Deploy:
```bash
docker build -t dark-fibre-engine .
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key dark-fibre-engine
```

### Option 2: Systemd Service (Linux)

Create `/etc/systemd/system/dark-fibre.service`:

```ini
[Unit]
Description=Dark Fibre Proposal Engine
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/dark-fibre-engine
Environment="PATH=/opt/dark-fibre-engine/venv/bin"
Environment="GOOGLE_API_KEY=your_key"
ExecStart=/opt/dark-fibre-engine/venv/bin/streamlit run app.py

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable dark-fibre
sudo systemctl start dark-fibre
```

---

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section above
2. Review [README.md](README.md)
3. Open an issue on [GitHub](https://github.com/Melochi127/Proposal_Engine_L1-L2-L3-)

---

**Last Updated**: March 2026  
**Maintained by**: Melochi127
