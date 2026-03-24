# 🔌 Dark Fibre Framework Agreement Engine

# Telecom Proposal Engine

An AI-assisted Streamlit application for generating telecom proposals and Dark Fibre framework agreements across three levels of complexity.

## Overview

The Telecom Proposal Engine helps users create:

- **Level 1** — Quick telecom proposals
- **Level 2** — Standard business proposals
- **Level 3** — Dark Fibre framework agreements with executive risk summaries

The system combines:

- **Gemini 2.5 Flash** for text generation
- **RAG (Retrieval-Augmented Generation)** for knowledge-grounded answers
- **Hybrid retrieval** using **BM25 + MiniLM embeddings**
- **Streamlit** for the user interface

This project was built as an MVP for proposal automation in the telecom domain, with a focus on improving speed, consistency, and usability for SMEs.

---

## Key Features

- Multi-level proposal workflow:
  - **L1:** Fast proposal generation
  - **L2:** Standard detailed proposal generation
  - **L3:** Dark Fibre contract-style agreement drafting
- Wizard-style intake flow
- Smart defaults for Dark Fibre questions
- Risk-aware clause logic
- Knowledge Base Q&A using RAG
- Executive Risk Summary generation for L3
- Save, view, and manage generated proposals
- Markdown and text export

---

## Levels

### Level 1 — Quick Proposal
Designed for rapid proposal generation with minimal questions.

Typical use:
- Fibre Broadband Installation
- Wireless Networks
- VoIP Solutions

### Level 2 — Standard Proposal
A more detailed proposal flow with fuller business and commercial content.

Typical use:
- Client-facing business proposals
- Formal telecom service proposals

### Level 3 — Dark Fibre
A structured framework agreement workflow for Dark Fibre deals.

Includes:
- 12 intake screens
- 5 phases
- Contract-style agreement generation
- Executive Risk Summary

---

## Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **Google Gemini**
- **ChromaDB**
- **BM25 Retriever**
- **Sentence Transformers** (`all-MiniLM-L6-v2`)

---

## Project Structure

```text
Telecom_Proposal_Engine/
│
├── app.py
├── proposal_agent.py
├── llm_engine.py
├── prompts.py
├── config.py
├── levels.py
├── phases.py
├── cross_clause_rules.py
├── agent_state.py
├── rag_ingest.py
├── rag_retriever.py
├── storage.py
├── rag_data/
├── saved_proposals/
└── README.md
