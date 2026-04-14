# 🔌 Dark Fibre Framework Agreement Engine

**AI-Guided Legal-Grade Contract Wizard with RAG/CRAG Evaluation Framework**
RAG + CRAG + LangChain + Google Gemini + ChromaDB + Streamlit

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Interface │    │   Agent Core     │    │   AI Processing │
│                 │    │                  │    │                 │
│ • Streamlit UI  │────│ • DarkFibreAgent │────│ • Gemini 1.5 Pro│
│ • 3 Proposal    │    │ • Session State   │    │ • RAG Retriever │
│   Levels (L1-3) │    │ • Phase Config    │    │ • CRAG System   │
│ • 5-Phase L3    │    │ • Risk Analysis   │    │ • Hybrid Search │
│   Wizard        │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌──────────────────┐
                    │   Data Layer     │
                    │                  │
                    │ • ChromaDB       │
                    │ • BM25 Index     │
                    │ • 320 Chunks     │
                    │ • 10 Reference   │
                    │   Documents      │
                    └──────────────────┘
```

## System Capabilities

### Multi-Level Proposal Generation
- **L1 Quick**: 8-field form for rapid proposals
- **L2 Standard**: 15-field form for comprehensive proposals
- **L3 Dark Fibre**: 5-phase wizard with AI assistance (35+ fields)

### 5-Phase L3 Wizard

| Phase | Focus | Key Clauses | Fields |
|-------|-------|-------------|--------|
| 1 | Entity & Admin | Cover Page, Notices | 8 fields |
| 2 | Wayleave & Access | Rights, Permits, Access | 7 fields |
| 3 | Commercials & Pricing | Pricing, Indexation, Terms | 8 fields |
| 4 | Liability & Termination | Risk, Termination, Force Majeure | 6 fields |
| 5 | Technical SLAs | Performance, Monitoring, Penalties | 6 fields |

### RAG/CRAG Retrieval Systems

#### RAG (Retrieval-Augmented Generation)
- **Hybrid Search**: BM25 (60%) + Dense Vectors (40%)
- **Reciprocal Rank Fusion**: Sophisticated document ranking
- **Optimized Chunking**: 500 chars with 100 char overlap
- **Performance**: 56.7% pass rate, 61.8% keyword coverage

#### CRAG (Corrective RAG)
- **Corrective Filtering**: Gemini-based relevance evaluation
- **Quality Enhancement**: Re-ranking for improved accuracy
- **Current Status**: Correction disabled (baseline comparison)
- **Expected Performance**: 58-65% pass rate when enabled

## Files Structure

```
dark_fibre_engine/
├── 📱 User Interface
│   ├── app.py                 # Streamlit web application
│   └── config.py              # Application settings
│
├── 🤖 Agent Core
│   ├── proposal_agent.py      # Main agent logic
│   ├── agent_state.py         # Session state management
│   ├── phases.py              # L3 phase configurations
│   └── levels.py              # L1/L2 field definitions
│
├── 🧠 AI Processing
│   ├── llm_engine.py          # Gemini 1.5 Pro wrapper
│   ├── prompts.py             # All LLM prompt templates
│   ├── rag_retriever.py       # Hybrid RAG retrieval
│   └── cross_clause_rules.py  # 25 risk analysis rules
│
├── 📊 Evaluation & Benchmarking
│   ├── ragas_evaluator.py     # RAG evaluation (30 queries)
│   ├── evaluation_benchmark.py # Benchmark definitions
│   ├── experiment_charts.py   # Chart generation
│   ├── rag_top3.json         # RAG results (top-k=3)
│   ├── rag_top5.json         # RAG results (top-k=5)
│   ├── rag_top7.json         # RAG results (top-k=7)
│   ├── crag_top3.json        # CRAG results (top-k=3)
│   ├── crag_top5.json        # CRAG results (top-k=5)
│   └── crag_top7.json        # CRAG results (top-k=7)
│
├── 📚 Data & Ingestion
│   ├── rag_ingest.py          # Document ingestion pipeline
│   ├── rag_data/              # 10 reference documents
│   ├── chroma_db/             # Vector database
│   └── bm25_chunks.pkl        # BM25 index
│
├── 📈 Charts & Analysis
│   ├── charts/                # Generated charts directory
│   ├── experiment_data.json   # Chart data
│   └── evaluation_report.json # Latest evaluation results
│
├── 🔧 CRAG Comparison
│   └── crag_comparison/
│       ├── crag_retriever.py  # CRAG implementation
│       ├── crag_evaluator.py  # CRAG evaluation
│       └── crag_ingest.py     # CRAG data ingestion
│
└── 📋 Configuration
    ├── requirements.txt       # Python dependencies
    ├── .env.example          # Environment template
    └── README.md             # This file
```

## Quick Start

### Basic Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env    # Add your GOOGLE_API_KEY

# Ingest reference documents
python rag_ingest.py    # Creates 320 chunks from 10 docs

# Launch the proposal wizard
streamlit run app.py    # Access at http://localhost:8501
```

### Evaluation & Benchmarking
```bash
# Run RAG evaluation with different top-k values
python ragas_evaluator.py --top_k 3    # Results saved to rag_top3.json
python ragas_evaluator.py --top_k 5    # Results saved to rag_top5.json
python ragas_evaluator.py --top_k 7    # Results saved to rag_top7.json

# Run CRAG evaluation (requires fixes for full functionality)
python crag_comparison/crag_evaluator.py --top_k 5

# Generate comparison charts
python experiment_charts.py --mode measured
```

## Key Features

### 🤖 Intelligent Proposal Generation
- **Multi-Level Support**: L1 (quick), L2 (standard), L3 (comprehensive) proposals
- **Smart Defaults**: Pre-configured UK telecom industry standards
- **Cross-Clause Logic**: 25 rules detecting inter-clause impacts and risks
- **Risk-Aware Drafting**: Real-time warnings for high-risk concessions

### 🔍 Advanced RAG System
- **Hybrid Retrieval**: BM25 keyword search + MiniLM semantic search
- **Optimized Chunking**: 500-character chunks with 100-character overlap
- **Reciprocal Rank Fusion**: Weighted combination (BM25 60%, Dense 40%)
- **Metadata Enrichment**: Source tracking, section detection, chunk sizing

### 📊 Comprehensive Evaluation Framework
- **30 Benchmark Queries**: Across 6 categories and 3 difficulty levels
- **Multi-Metric Scoring**: Keyword coverage, source accuracy, pass/fail rates
- **RAG vs CRAG Comparison**: Performance analysis across retrieval strategies
- **Chart Generation**: Publication-ready matplotlib visualizations

### 🎯 Risk Intelligence
- **Executive Summaries**: Plain English commercial risk breakdowns
- **Real-Time Warnings**: Immediate alerts for problematic clauses
- **Clause Interdependencies**: Automatic detection of related clause impacts
- **Industry Standards**: UK telecom contract best practices built-in

## Reference Documents (rag_data/)

1. **Dark Fibre Framework Agreement Template v0.1** - Base contract structure
2. **Level 3 Intake Questionnaire** - Comprehensive requirement gathering
3. **Product Requirements Document (PRD)** - System specifications
4. **System Instruction Block (Rules of the Game)** - Operational guidelines
5. **Prompting Flow for Wizard Interface** - UI interaction patterns
6. **Further Q&A Dialogue** - Example conversations
7. **Clause Intelligence Map** - Contract clause relationships
8. **25 Cross-Clause Logic Rules** - Risk analysis engine
9. **Telecom Contract Risk Matrix** - Risk assessment framework
10. **MVP Architecture Note** - System design documentation

## Performance Metrics

### Current RAG Performance (Top-K=5)
- **Pass Rate**: 56.7% (17/30 queries)
- **Keyword Coverage**: 61.8%
- **Source Accuracy**: 50.5%
- **Retrieval Time**: 182.4ms average
- **Context Length**: 2,500 characters

### CRAG Baseline (Correction Disabled)
- **Pass Rate**: 40.0% (12/30 queries)
- **Keyword Coverage**: 56.0%
- **Source Accuracy**: 35.0%
- **Issue**: Correction step disabled, using inferior fusion algorithm

## Architecture Details

### Data Pipeline
```
Documents → Text Extraction → Chunking (500 chars) → Embedding (MiniLM) → ChromaDB
    ↓                                                        ↓
BM25 Indexing → Hybrid Retrieval → Reciprocal Rank Fusion → LLM Generation
```

### Evaluation Pipeline
```
Benchmark Queries → RAG/CRAG Retrieval → Response Generation → Multi-Metric Scoring → Charts
```

## Development Status

- ✅ **Core Functionality**: L1/L2/L3 proposal generation
- ✅ **RAG System**: Hybrid retrieval with optimized chunking
- ✅ **Risk Analysis**: 25 cross-clause rules implemented
- ✅ **Evaluation Framework**: 30 benchmark queries with metrics
- ⚠️ **CRAG System**: Implemented but correction disabled (needs activation)
- 📊 **Chart Generation**: Automated visualization system
- 🔬 **Research Ready**: Comprehensive benchmarking for dissertation

## Citation

For academic use, please cite:
```
Melochi127. (2026). Dark Fibre Framework Agreement Engine:
AI-Guided Legal-Grade Contract Wizard with RAG/CRAG Evaluation Framework.
GitHub Repository. https://github.com/Melochi127/Proposal_Engine_L1-L2-L3-
```
