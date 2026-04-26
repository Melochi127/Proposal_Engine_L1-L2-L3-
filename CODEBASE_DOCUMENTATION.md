# Codebase Documentation - Dark Fibre Framework Agreement Engine

Complete technical documentation of the project architecture, modules, and design patterns.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module Reference](#module-reference)
3. [Data Flow](#data-flow)
4. [Design Patterns](#design-patterns)
5. [Configuration & Environment](#configuration--environment)
6. [Error Handling](#error-handling)
7. [Performance Considerations](#performance-considerations)
8. [Testing & Evaluation](#testing--evaluation)

---

## Architecture Overview

### System Layers

```
┌──────────────────────────────────────────────────┐
│              USER INTERFACE (Streamlit)           │
│              app.py (150 lines)                   │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│         AGENT ORCHESTRATION LAYER                 │
│    proposal_agent.py (400+ lines, main logic)     │
│  - Session management                             │
│  - Field progression                              │
│  - LLM invocation                                 │
│  - Risk detection                                 │
└────────────────────┬─────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──┐ ┌───────▼──┐ ┌──────▼──┐
│  LLM     │ │   RAG    │ │  State  │
│  Engine  │ │ Retrieval│ │ & Risk  │
└─────┬────┘ └─────┬────┘ └────┬────┘
      │            │            │
┌─────▼──────────┐ │   ┌────────▼─────┐
│Gemini 2.5 Flash│ │   │ Business     │
│ (Google API)   │ │   │ Rules (25)   │
└────────────────┘ │   └──────────────┘
                   │
        ┌──────────▼──────────┐
        │  KNOWLEDGE BASE     │
        ├─────────────────────┤
        │ BM25 Retriever      │
        │ + MiniLM Dense      │
        │ + ChromaDB Vector   │
        │ (320 chunks)        │
        └─────────────────────┘
        
        ┌──────────────────────┐
        │  PERSISTENT STORAGE  │
        ├──────────────────────┤
        │ proposals/*.json     │
        │ chroma_db/*          │
        │ bm25_chunks.pkl      │
        └──────────────────────┘
```

### Key Architectural Principles

1. **Separation of Concerns**: Each module has single responsibility
2. **Pydantic Models**: Type-safe data validation (Session, Fields)
3. **Lazy Loading**: Models and embeddings cached with @lru_cache
4. **Error Resilience**: Graceful degradation when external APIs fail
5. **Testability**: Pure functions where possible, clear dependencies

---

## Module Reference

### Core Modules (User-Facing)

#### `app.py` (150 lines)
**Purpose**: Streamlit web UI entry point  
**Responsibility**: UI rendering, state management, button handling

Key Components:
- `st.set_page_config()`: Page setup (title, layout, theme)
- CSS styling: Custom Streamlit component styling
- Session management: `st.session_state` for persistent widgets
- Tabs: "New Proposals", "My Proposals", "Knowledge Base", "Help"

Dependencies:
- streamlit ≥1.32.0
- proposal_agent.Agent
- storage functions
- rag_retriever functions

Key Functions:
- Main UI loop
- Button event handlers (Create, Generate, Download, Delete)
- Chat message rendering
- Progress bar updates

#### `proposal_agent.py` (400+ lines, core business logic)
**Purpose**: Main orchestrator for proposal generation  
**Responsibility**: Session lifecycle, LLM orchestration, validation

Classes:
- `Agent`: Main orchestrator
  - `create_session()`: Initialize new session
  - `process_answer()`: Handle user input + LLM response + risk check
  - `generate()`: Dispatch to level-specific generators
  - `generate_l1l2()`: L1/L2 proposal generation
  - `generate_agreement()`: L3 framework agreement generation
  - `ask_rag()`: Answer free-form questions from knowledge base
  - `explain()`: Explain current field
  - `skip()`: Apply defaults and advance
  - `go_back()`: Navigate to previous field

Key Design Pattern:
1. Fetch current field from phases/levels config
2. User enters answer (or "defaults")
3. Store answer in session.slots
4. Check cross-clause risks
5. Invoke LLM for acknowledgment
6. Parse LLM response for ADVANCE/CLARIFY signal
7. Limit clarifications to 1 per field (prevent loops)
8. Advance to next field if satisfied
9. Repeat until all fields complete
10. Generate final document

Error Handling:
- LLM timeouts: Return "Got it — noted."
- Missing required fields: Return validation error list
- Empty LLM response: Return helpful error message

#### `agent_state.py` (100+ lines)
**Purpose**: Type-safe session state definition  
**Responsibility**: Data model for session persistence

Pydantic Model:
```python
class Session(BaseModel):
    session_id: str
    level: str  # L1, L2, L3
    current_phase: str  # phase_1 through phase_5 (L3 only)
    current_field_index: int
    slots: Dict[str, str]  # User answers
    clarify_counts: Dict[str, int]  # Prevent inf. loops
    chat_history: List[Dict]  # AI/user messages
    risk_warnings: List[Dict]  # Detected risks
    full_output: str  # Generated proposal text
    risk_summary: str  # Risk analysis text
    all_complete: bool  # Wizard complete flag
```

Key Methods:
- `filled_count()`: Count non-empty answers
- `slots_summary()`: Format slots for LLM context
- `add_chat()`: Append message with timestamp
- `set_slot()`: Record user answer

---

### LLM & Generation Modules

#### `llm_engine.py` (60 lines)
**Purpose**: Google Gemini API wrapper  
**Responsibility**: LLM invocation, task-specific tuning

Implementations:
- `get_llm(task)`: Get configured Gemini instance
  - "chat": temp=0.7, tokens=2048 (conversational)
  - "agreement": temp=0.4, tokens=4000 (formal contracts)
  - "extraction": temp=0.4, tokens=4096 (structured data)

Functions:
- `invoke_llm(prompt, task, system)`: With system message
- `invoke_simple(prompt, task)`: Without system message

Both catch exceptions and return "[LLM Error: ...]" messages.

#### `prompts.py` (500+ lines)
**Purpose**: All LLM prompt templates  
**Responsibility**: Prompt engineering for consistent outputs

Prompt Categories:
1. **SYSTEM_PROMPT**: Generic system persona for all tasks
2. **L3_SYSTEM**: Domain-specific system prompt for Dark Fibre contracts
3. **CHAT_RESPONSE**: Acknowledge user answers, detect clarifications
4. **EXPLAIN_FIELD**: Educational explanations of clauses
5. **RAG_QUESTION**: Answer user questions from knowledge base
6. **L1_GENERATE**: Template for L1 quick proposals
7. **L2_GENERATE**: Template for L2 standard proposals
8. **L3_GENERATE**: Template for L3 20-clause framework agreements
9. **L3_RISK_SUMMARY**: Generate executive risk summaries

Key Design:
- All use `.format(**kwargs)` for template substitution
- Variables extracted into named fields for clarity
- Examples provided in prompts for few-shot prompting
- Domain knowledge baked in (wayleaves, IRU, TTTR, etc.)

---

### RAG & Knowledge Base Modules

#### `rag_retriever.py` (200 lines)
**Purpose**: Hybrid document retrieval (BM25 + dense embeddings)  
**Responsibility**: Fetch relevant context from knowledge base

Architecture:
- **BM25**: Keyword-based ranking (60% weight)
- **Dense**: Semantic similarity via MiniLM embeddings (40% weight)
- **Fusion**: Reciprocal rank fusion combines both signals
- **Caching**: LRU cache prevents model reload (<1ms subsequent calls)

Key Functions:
- `check_kb()`: Verify knowledge base exists (returns {exists, count})
- `load_embeddings()`: Get cached HuggingFace MiniLM model
- `_load_bm25_chunks()`: Load pickled BM25 index
- `_load_vectordb()`: Load ChromaDB vector store
- `_reciprocal_rank_fusion()`: Combine two ranked lists
- `retrieve_context(query, max_docs=4)`: Main retrieval (returns context + docs)
- `clear_cache()`: Invalidate caches after ingestion

Retrieval Algorithm:
```
1. Query BM25 for keyword matches (2*max_docs)
2. Query dense embeddings for semantic matches (2*max_docs)
3. Score each doc: bm25_weight*(1/(k+rank_bm25+1)) + dense_weight*(1/(k+rank_dense+1))
4. Sort by combined score
5. Return top max_docs deduplicated results
6. Concatenate document text for LLM context
```

#### `rag_ingest.py` (150+ lines)
**Purpose**: Document processing and knowledge base creation  
**Responsibility**: Extract, chunk, and index documents

Pipeline:
1. **Document Loading**: Read .pdf, .docx, .doc, .txt files
2. **Text Extraction**: Convert formats to text
3. **Chunking**: Split into 500-char overlapping chunks (100-char overlap)
4. **Embedding**: Generate 384-dim vectors via MiniLM
5. **BM25 Indexing**: Create keyword index for fast retrieval
6. **ChromaDB Storage**: Persist embeddings in vector database

Output Artifacts:
- `bm25_chunks.pkl`: ~30KB pickle file with chunks
- `chroma_db/`: ~50-100MB vector database directory

---

### Configuration & State Modules

#### `config.py` (50 lines)
**Purpose**: Centralized configuration  
**Responsibility**: Environment variables, model selection, paths

Settings:
```python
GOOGLE_API_KEY  # Google Gemini API key (from .env)
GEMINI_MODEL  # Model ID: "gemini-2.5-flash"
EMBEDDING_MODEL  # HuggingFace: "all-MiniLM-L6-v2"
CHUNK_SIZE  # 800 characters per chunk
CHUNK_OVERLAP  # 150 characters overlap between chunks
RAG_DATA_DIR  # ./rag_data/
CHROMA_DIR  # ./rag_data/chroma_db/
BM25_STORE  # ./rag_data/bm25_chunks.pkl
```

#### `storage.py` (100 lines)
**Purpose**: Proposal persistence  
**Responsibility**: Save, load, list, delete proposals

Functions:
- `save_proposal(session, output, risk)`: Save to JSON file
- `list_proposals()`: Get all proposals (summaries only)
- `load_proposal(filename)`: Load full proposal by name
- `delete_proposal(filename)`: Delete a proposal file

Storage Location: `./proposals/` directory

File Format:
```json
{
  "id": "df_20260324_114640",
  "saved_at": "2026-03-24 11:46",
  "level": "L3",
  "label": "Dark Fibre",
  "subsector": "Core Network",
  "client": "BT Wholesale",
  "slots": {...},
  "output": "generated proposal text...",
  "risk": "risk summary...",
  "risk_warnings": [...]
}
```

---

### Field & Configuration Modules

#### `levels.py` (100+ lines)
**Purpose**: L1 & L2 proposal field definitions  
**Responsibility**: Question templates for quick and standard proposals

Data Structure:
```python
# Each level has list of field definitions:
[
  {
    "key": "client_name",
    "question": "Who is this proposal for?",
    "clause": "Client Details",
    "required": True,
    "defaults": {"company_name": "[Company]"},
    "risk_logic": "None"
  },
  ...
]
```

Functions:
- `get_level(*args)`: Metadata about proposal level
- `get_l1l2_fields(level)`: List of field definitions for L1 or L2
- `get_l3_phase(*args)`: Metadata about L3 phase
- `get_l3_phase_fields(phase_key)`: List of fields for phase
- `get_l3_phase_keys()`: List of all L3 phase keys

#### `phases.py` (200+ lines)
**Purpose**: L3 Dark Fibre phase and field definitions  
**Responsibility**: Question templates for 5-phase wizard

5 Phases:
1. **phase_1**: Entity & Admin (8 fields)
2. **phase_2**: Wayleave & Access (7 fields)
3. **phase_3**: Commercials & Pricing (8 fields)
4. **phase_4**: Liability & Termination (6 fields)
5. **phase_5**: Technical SLAs (6 fields)

Each phase has:
- Title & description
- 6-8 fields with questions, clauses, defaults
- Risk logic for some fields

---

### Risk Analysis Module

#### `cross_clause_rules.py` (100 lines)
**Purpose**: Business rule risk detection  
**Responsibility**: Identify dangerous clause combinations

Rules Implemented (Sample):
- **R01**: Provider-led wayleaves = high delivery risk
- **R02**: High-risk sites (railway, highway, MDU)
- **R03**: Long-term without indexation (CRITICAL)
- **R08**: Aggressive TTTR (<12 hours)
- **R09**: Over-generous service credits
- **R10**: No early termination fees

Risk Levels:
- 🚨 **Critical**: Must resolve before signature
- ⚠️ **High**: Strongly recommend addressing
- ⚠️ **Medium**: Consider implications

Function:
- `check_risks(slots)`: Analyze user answers, return warning list

Invoked after each answer in L3 wizard.

---

## Data Flow

### Typical User Interaction Flow

```
User Opens App
  ↓
app.py initializes Streamlit session
  ↓
User clicks "Create L3 Proposal"
  ↓
Agent.create_session("L3") → Session object
  ↓
Display greeting message
  ↓
Display Phase 1, Question 1 field
  ↓
User enters answer
  ↓
Agent.process_answer(session, user_input)
  ├─→ Get current field from phases.py
  ├─→ Store answer: session.set_slot(key, value)
  ├─→ Check defaults: fill_missing_defaults()
  ├─→ Risk detection: check_risks(session.slots)
  ├─→ Invoke LLM: invoke_llm(CHAT_RESPONSE.format(...))
  ├─→ Parse response: extract ADVANCE/CLARIFY signal
  ├─→ Limit clarifications to 1 per field
  └─→ Return (response_text, advance_flag)
  ↓
Display AI response + risk warnings
  ↓
Auto-advance to next field if satisfied
  ↓
[Repeat for all 35+ fields]
  ↓
User clicks "Generate Agreement"
  ↓
Agent.generate(session)
  ├─→ Validate all required fields filled
  ├─→ Retrieve RAG context: retrieve_context("dark fibre agreement")
  ├─→ Format all slots into L3_GENERATE template
  ├─→ Invoke LLM: invoke_llm(template, task="agreement")
  └─→ Store output: session.full_output = generated_text
  ↓
Display full 20-clause agreement
  ↓
User clicks "Save Proposal"
  ├─→ storage.save_proposal(session, output, risk)
  └─→ File saved to proposals/df_TIMESTAMP.json
  ↓
User clicks "Download as .docx"
  ├─→ Convert Markdown to DOCX format
  └─→ Browser downloads file
  ↓
END
```

### RAG Context Retrieval Flow

```
Query: "What is wayleave?"
  ↓
retrieve_context(query, max_docs=4)
  ↓
BM25 Retrieval:
  ├─→ Load BM25 chunks from pickle
  ├─→ Search for keyword matches
  └─→ Return top 8 results with scores
  ↓
Dense Semantic Retrieval:
  ├─→ Load embeddings model (MiniLM)
  ├─→ Embed query into 384-dim vector
  ├─→ Search ChromaDB for similarity
  └─→ Return top 8 results with scores
  ↓
Reciprocal Rank Fusion:
  ├─→ Combine BM25 (60%) + Dense (40%) scores
  ├─→ Sort by combined score
  ├─→ Deduplicate identical chunks
  └─→ Return top 4 most relevant documents
  ↓
Format Output:
  ├─→ Concatenate document text
  └─→ Return (context_string, document_list)
  ↓
LLM Uses Context:
  ├─→ Embed context in RAG_QUESTION prompt
  └─→ Answer user question grounded in knowledge base
  ↓
END
```

---

## Design Patterns

### 1. Lazy Evaluation with LRU Cache

```python
@lru_cache(maxsize=1)
def load_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
```

**Benefit**: Model loaded only on first call, reused for ~100ms response time.  
**Cache Invalidation**: `clear_cache()` after data ingestion.

### 2. Graceful Error Handling

```python
def invoke_llm(prompt, task="chat", system=None):
    try:
        # LLM invocation
        return response
    except Exception as e:
        # Return user-friendly error
        return f"[LLM Error: {e}]"
```

**Benefit**: Application continues, LLM errors don't crash UI.

### 3. Session-Based State Management

```python
session = Session(session_id=unique_id)
session.set_slot("field_name", user_answer)
# Later: session.slots_summary() for LLM context
```

**Benefit**: Clean separation of session data from UI logic.

### 4. Reciprocal Rank Fusion for Multi-Source Ranking

```python
def _reciprocal_rank_fusion(bm25_docs, dense_docs, ...):
    # Combine BM25 (keyword) + Dense (semantic) signals
    # Fair weighting: 60/40 split
    # Deduplicates identical passages
```

**Benefit**: Hybrid retrieval balances keyword + semantic matching.

### 5. Template-Based Prompting

```python
CHAT_RESPONSE = """...
Level: {level_name}
Phase: {phase}
Question: {question}
Answer: {answer}
..."""

invoke_llm(CHAT_RESPONSE.format(level_name="L3", ...))
```

**Benefit**: Consistent, reusable prompts. Easy to version and test.

### 6. Configuration Externalization

```python
# config.py
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Used everywhere else without hardcoding
from config import GOOGLE_API_KEY, EMBEDDING_MODEL
```

**Benefit**: Easy environment switching (dev/test/prod).

### 7. Field Progression State Machine

```
Phase 1, Q1 → Answer → Store → Check risks → Advance
    ↓
Phase 1, Q2 → Answer → Store → Check risks → Advance
    ...
Phase 5, Q6 → Answer → Store → Check risks → Complete!
```

**Benefit**: Clear, predictable state transitions.

---

## Configuration & Environment

### Environment Variables (.env)

```env
# Required
GOOGLE_API_KEY=AIzaSy...  # From Google Cloud Console

# Optional (defaults provided)
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=800
CHUNK_OVERLAP=150
```

### File Structure

```
dark_fiber_engine/
├── Python Modules (24 files)
│   ├── Core: app.py, proposal_agent.py, agent_state.py
│   ├── LLM: llm_engine.py, prompts.py
│   ├── RAG: rag_retriever.py, rag_ingest.py
│   ├── Config: config.py, levels.py, phases.py, cross_clause_rules.py
│   ├── Storage: storage.py
│   └── Evaluation: ragas_evaluator.py, evaluate_agent.py, ...
│
├── Documentation
│   ├── README.md (comprehensive overview)
│   ├── INSTALLATION.md (setup instructions)
│   ├── USAGE.md (user guide)
│   └── CODEBASE_DOCUMENTATION.md (this file)
│
├── Data & Storage
│   ├── rag_data/
│   │   ├── 18 reference documents (.pdf, .docx, .txt)
│   │   ├── chroma_db/ (vector database)
│   │   └── bm25_chunks.pkl (keyword index)
│   ├── proposals/ (saved proposal JSON files)
│   └── .env (environment variables)
│
└── Configuration
    ├── requirements.txt (dependencies)
    ├── .env.example (template)
    └── .gitignore
```

---

## Error Handling

### LLM Errors

```python
invoke_llm(prompt) → Returns "[LLM Error: ...]" on failure
                   → UI continues without crashing
                   → User sees friendly error message
```

### Knowledge Base Errors

```python
retrieve_context(query) → Returns ("", []) if KB not found
                        → LLM answers without context
                        → Degrades gracefully
```

### Validation Errors

```python
generate(session) → Returns validation error with field list
                  → User knows which fields to complete
                  → Cannot accidentally generate incomplete agreement
```

### API Key Errors

```python
get_llm() → Raises ValueError if GOOGLE_API_KEY not set
         → User-friendly error message in app
         → Points to configuration instructions
```

---

## Performance Considerations

### Latency Breakdown (typical L3 interaction)

| Operation | Time | Bottleneck |
|-----------|------|-----------|
| Load embeddings (first call) | 2-3s | Model download |
| Load embeddings (cached) | <1ms | Memory access |
| BM25 retrieval | 10-20ms | Keyword search |
| Dense retrieval | 50-100ms | Vector search |
| Reciprocal rank fusion | <1ms | Python computation |
| LLM inference (chat) | 2-5s | API network + model |
| LLM inference (agreement) | 10-15s | API network + large output |
| UI render | 100-500ms | Streamlit refresh |
| **Total per step** | **2-5s** | LLM API latency |
| **Total for 35 questions** | **2-3 minutes** | 35 × 2-5s |

### Optimization Strategies

1. **Caching**
   - Embeddings: LRU cache (first load: 2-3s, subsequent: <1ms)
   - BM25 index: Pickled in file (load: 50ms)
   - ChromaDB: Persisted (load: 100ms)

2. **Asynchronous Loading** (future improvement)
   - Pre-load models during startup
   - Background document ingestion
   - Streaming LLM responses

3. **Batch Processing** (future improvement)
   - Generate multiple proposals in parallel
   - Evaluation runs on multiple queries simultaneously

---

## Testing & Evaluation

### Unit Testing (Currently Manual)

Test by running:

```bash
# Test 1: System validation
python -c "
from llm_engine import get_llm
from rag_retriever import check_kb
print('✓ LLM available:', get_llm('chat').model_name)
print('✓ KB available:', check_kb()['exists'])
"

# Test 2: Quick proposal generation
# Start app, select L1, fill 8 fields, generate

# Test 3: L3 agreement generation
# Start app, select L3, fill all 35+ fields through 5 phases

# Test 4: RAG retrieval
python -c "
from rag_retriever import retrieve_context
ctx, docs = retrieve_context('wayleave liability')
print(f'✓ Retrieved {len(docs)} docs')
print(f'✓ Context length: {len(ctx)} chars')
"
```

### Evaluation Framework

See `ragas_evaluator.py`:
- 30 benchmark queries across 6 categories
- Measures: keyword coverage, source accuracy, pass/fail rate
- Compares: RAG vs CRAG performance

Run:
```bash
python ragas_evaluator.py --top_k 5  # Generates rag_top5.json
python experiment_charts.py --mode measured  # Generates charts
```

### Regression Testing

After code changes:

1. Generate L1, L2, L3 proposals
2. Verify no syntax errors
3. Check RAG retrieval works
4. Confirm risk rules trigger on test cases
5. Review generated agreements for quality

---

## Future Improvements

### Stability & Performance
- [ ] Async LLM calls (streaming responses)
- [ ] Request batching for evaluations
- [ ] Connection pooling for ChromaDB

### Features
- [ ] Multi-language support
- [ ] Template versioning & comparison
- [ ] Proposal analytics dashboard
- [ ] Integration with CRM (Salesforce, Pipedrive)
- [ ] Email sharing & approval workflows

### Data
- [ ] More reference documents (CRAG dataset)
- [ ] Multi-tenant support
- [ ] Audit logging

### Quality
- [ ] Automated unit & integration tests
- [ ] CI/CD pipeline
- [ ] Production monitoring & alerting

---

## References

### Key Libraries & Versions

```
streamlit>=1.32.0            # Web UI framework
langchain==0.2.2              # LLM orchestration
langchain-google-genai>=1.0.0  # Gemini integration
pydantic>=2.0.0               # Data validation
sentence-transformers>=2.2.0  # MiniLM embeddings
chromadb>=0.5.0               # Vector database
```

### External Services

- **Google Gemini API**: LLM inference
- **HuggingFace**: MiniLM embeddings
- **OpenAI (future)**: Alternative LLM provider

### Papers & Resources

- Reciprocal Rank Fusion: https://arxiv.org/abs/1809.04040
- RAG Pattern: https://arxiv.org/abs/2005.11401
- CRAG: Corrective RAG with adaptive retrieval

---

**Last Updated**: March 2026  
**Maintained by**: Melochi127  
**Repository**: https://github.com/Melochi127/Proposal_Engine_L1-L2-L3-
