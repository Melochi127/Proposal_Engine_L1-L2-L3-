# 🔌 Dark Fibre Framework Agreement Engine

**AI-Guided Legal-Grade Contract Wizard**
RAG + LangChain + Google Gemini + ChromaDB + Streamlit

## Architecture

```
User → Streamlit UI (5-Phase Wizard)
         ↓
    DarkFibreAgent (proposal_agent.py)
     ├── Phase Config (phases.py) — 5 phases, 35+ fields
     ├── LLM Engine (llm_engine.py) — Gemini 1.5 Pro
     ├── RAG Retriever (rag_retriever.py) → ChromaDB
     └── Prompts (prompts.py) — system, chat, generation, risk
         ↑
    RAG Ingestion (rag_ingest.py) — .doc/.pdf/.docx → chunks → embeddings
```

## 5-Phase Wizard

| Phase | Focus | Clauses |
|-------|-------|---------|
| 1 | Entity & Admin | Cover Page, Clause 19 (Notices) |
| 2 | Wayleave & Access | Clauses 3-5, Schedule 1 |
| 3 | Commercials & Pricing | Clauses 9-11 |
| 4 | Liability & Termination | Clauses 12-14 |
| 5 | Technical SLAs | Schedule 2 |

## Files

```
dark_fibre_engine/
├── app.py              # Streamlit UI
├── config.py           # Settings
├── phases.py           # 5-phase field definitions
├── prompts.py          # All LLM prompts
├── llm_engine.py       # Gemini wrapper
├── agent_state.py      # Session state (Pydantic)
├── proposal_agent.py   # Core agent logic
├── rag_ingest.py       # Doc ingestion (.doc/.pdf/.docx)
├── rag_retriever.py    # ChromaDB retrieval
├── requirements.txt
├── .env.example
└── rag_data/           # 10 Dark Fibre reference docs
```

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env    # Add your GOOGLE_API_KEY
python rag_ingest.py    # Ingest the 10 reference docs
streamlit run app.py    # Launch the wizard
```

## Key Features

- **Risk-Aware Drafting**: Warns about high-risk concessions (uncapped liability, no indexation)
- **Cross-Clause Logic**: Changes in one clause flag impacts on others
- **RAG Context**: 10 reference docs provide domain knowledge during generation
- **Executive Risk Summary**: Plain English breakdown of commercial position
- **Intelligent Handholding**: Colleague-style Q&A, not form filling

## Reference Documents (in rag_data/)

1. Dark Fibre Framework Agreement Template v0.1
2. Level 3 Intake Questionnaire
3. Product Requirements Document (PRD)
4. System Instruction Block (Rules of the Game)
5. Prompting Flow for Wizard Interface
6. Further Q&A Dialogue
7. Clause Intelligence Map
8. 25 Cross-Clause Logic Rules
9. Telecom Contract Risk Matrix
10. MVP Architecture Note
