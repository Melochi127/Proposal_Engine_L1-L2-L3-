# System Flowcharts - ASCII Format

All major system flows in text-based ASCII diagrams (no rendering issues!)

---

## 1. USER JOURNEY - Complete Proposal Generation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER OPENS APP                           │
│              (streamlit run app.py)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              SELECT PROPOSAL LEVEL                          │
│         ┌─────────────┬─────────────┬─────────────┐         │
│         │   L1 Quick  │ L2 Standard │ L3 Dark     │         │
│         │  (8 Qs)     │  (15 Qs)    │ Fibre (35+) │         │
│         └─────────────┴─────────────┴─────────────┘         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         CREATE NEW SESSION                                  │
│    session_id = df_YYYYMMDDhhmmss                           │
│    level = L1|L2|L3                                         │
│    subsector = user_input                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         DISPLAY GREETING MESSAGE                            │
│    "Welcome to Dark Fibre Wizard..."                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  LOOP: Get Current Field      │
        │  └─ Fetch from phases.py      │
        │  └─ Display question          │
        └────────────┬─────────────────┘
                     │
         ┌───────────┴────────────┐
         │                        │
         ▼                        ▼
    USER INPUT             SPECIAL COMMANDS
    (client answer)        • "defaults" → Apply defaults
                          • "explain" → Explain clause
                          • "back" → Go to previous
                          • "skip" → Apply defaults + advance
         │                        │
         └────────────┬───────────┘
                      │
                      ▼
        ┌──────────────────────────────┐
        │ PROCESS ANSWER               │
        │ ├─ Store in session.slots    │
        │ ├─ Fill missing defaults     │
        │ ├─ Check cross-clause risks  │
        │ ├─ Invoke LLM for response   │
        │ ├─ Parse ADVANCE/CLARIFY     │
        │ └─ Limit clarifications to 1 │
        └────────────┬─────────────────┘
                     │
                     ▼
        ┌──────────────────────────────┐
        │ DISPLAY AI RESPONSE          │
        │ ├─ Acknowledgment message    │
        │ ├─ Risk warnings (if any)    │
        │ └─ Optional clarification    │
        └────────────┬─────────────────┘
                     │
              ┌──────┴──────┐
              │             │
         ADVANCE       CLARIFY (retry)
              │             │
              ▼             └──────┐
        ┌──────────────────────┐   │
        │ Move to Next Field   │   │
        │ (current_field_idx++)│   │
        └──────────┬───────────┘   │
                   │               │
            ┌──────┴───────┐       │
            │              │       │
       All Done?       Still More? │
            │              │       │
           YES            NO      │
            │              │       │
            ▼              ▼       │
         Complete      LOOP ◄─────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│         USER CLICKS "GENERATE PROPOSAL"                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         VALIDATE ALL REQUIRED FIELDS                        │
│    Check _missing_required_fields()                         │
│    If missing: Return error list                            │
│    Else: Continue to generation                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │ RETRIEVE RAG CONTEXT         │
        │ └─ Query knowledge base      │
        │ └─ Return 4 top docs         │
        └────────────┬─────────────────┘
                     │
                     ▼
        ┌──────────────────────────────┐
        │ INVOKE LLM                   │
        │ ├─ Format prompt with data   │
        │ ├─ Send to Gemini API        │
        │ └─ Get generated proposal    │
        └────────────┬─────────────────┘
                     │
                     ▼
        ┌──────────────────────────────┐
        │ DISPLAY PROPOSAL             │
        │ ├─ Render Markdown           │
        │ └─ Show in UI                │
        └────────────┬─────────────────┘
                     │
              ┌──────┴──────┐
              │             │
          SAVE         DOWNLOAD
              │             │
              ▼             ▼
    ┌──────────────┐  ┌──────────────┐
    │ Save JSON    │  │ Export DOCX  │
    │ proposals/   │  │ Download     │
    │ df_*.json    │  │ to computer  │
    └──────────────┘  └──────────────┘
             │             │
             └─────┬───────┘
                   ▼
            ┌─────────────────┐
            │ ALL DONE ✓      │
            └─────────────────┘
```

---

## 2. RAG RETRIEVAL - Hybrid Search Flow

```
USER ASKS QUESTION
        │
        ▼
retrieve_context(query)
        │
        ├─────────────────────────┬──────────────────────────┐
        │                         │                          │
        ▼                         ▼                          ▼
   BM25 SEARCH          DENSE SEMANTIC SEARCH      RECIPROCAL RANK FUSION
   (Keyword-based)      (Embedding-based)         (Combine both)
        │                         │                          │
        ├─ Load BM25 index        ├─ Load embeddings model  │
        ├─ Query keywords         ├─ Embed query            │
        ├─ Get keyword matches    ├─ Search ChromaDB        │
        └─ Top 8 results          └─ Top 8 results          │
             (with scores)             (with scores)        │
        │                         │                          │
        └─────────────────────────┼──────────────────────────┤
                                  │                          │
                                  ▼                          ▼
                            COMBINE SCORES
                            ┌──────────────────────────┐
                            │ For each document:       │
                            │ score = 0.6 * bm25_rank  │
                            │       + 0.4 * dense_rank │
                            │                          │
                            │ (60% keyword,            │
                            │  40% semantic)           │
                            └───────────┬──────────────┘
                                        │
                                        ▼
                            ┌──────────────────────────┐
                            │ SORT BY COMBINED SCORE   │
                            │ • Highest score first    │
                            │ • Deduplicate identical  │
                            │ • Return top 4 docs      │
                            └───────────┬──────────────┘
                                        │
                                        ▼
                            ┌──────────────────────────┐
                            │ FORMAT CONTEXT           │
                            │ • Concatenate text       │
                            │ • Return (context, docs) │
                            └───────────┬──────────────┘
                                        │
                                        ▼
                            SEND TO LLM WITH CONTEXT
                            LLM answers question
                            grounded in knowledge base
```

---

## 3. RISK DETECTION - Cross-Clause Analysis

```
USER ENTERS ANSWER
        │
        ▼
store in session.slots
        │
        ▼
check_risks(slots)
        │
        ├─────────────────────────────────────────────┐
        │ RULE CHECKS:                                │
        │                                             │
        ├─ R01: Provider-led wayleaves?               │
        │        └─→ HIGH RISK ⚠️                     │
        │                                             │
        ├─ R02: High-risk sites (railway, MDU)?       │
        │        └─→ HIGH RISK ⚠️                     │
        │                                             │
        ├─ R03: Long-term + no indexation?            │
        │        └─→ CRITICAL 🚨                      │
        │                                             │
        ├─ R08: TTTR < 12 hours?                      │
        │        └─→ MEDIUM ⚠️                        │
        │                                             │
        ├─ R09: 100% service credits at risk?         │
        │        └─→ MEDIUM ⚠️                        │
        │                                             │
        └─ R10: No early termination fee?             │
                 └─→ HIGH RISK ⚠️                     │
        │
        ▼
RETURN WARNINGS LIST
        │
        ├─ warnings = [
        │     {
        │       "id": "R01",
        │       "severity": "High",
        │       "msg": "Provider-led wayleaves..."
        │     },
        │     ...
        │   ]
        │
        ▼
APPEND TO RESPONSE
        │
        └─→ Display to user alongside AI response
            ⚠️ [Severity]: [Message with recommendation]
```

---

## 4. PROPOSAL GENERATION - Multi-Level Logic

```
user.level = L1, L2, or L3
        │
        ├─────────────────┬─────────────────┬─────────────────┐
        │                 │                 │                 │
        ▼                 ▼                 ▼                 ▼
      L1 FLOW           L2 FLOW           L3 FLOW          ERROR
    (8 questions)    (15 questions)   (35+ questions)   (Validation)
        │                 │                 │                 │
        ├─ Client name    ├─ All L1 +       ├─ Phase 1:      │
        ├─ Service desc   ├─ Scope          │  Entity/Admin   │
        ├─ Prepared by    ├─ Timeline       ├─ Phase 2:      │
        ├─ Total cost     ├─ Support        │  Wayleave/Acc   │
        ├─ Timeline       ├─ Contact        ├─ Phase 3:      │
        ├─ Tone           └─ More...        │  Commercial     │
        ├─ Subsector                        ├─ Phase 4:      │
        └─ Notes                            │  Liability      │
                                            ├─ Phase 5:      │
                                            │  SLA/Technical  │
                                            └─ Risk Analysis  │
        │                 │                 │                 │
        └─────────────────┼─────────────────┤ Missing fields?
                          │                 │    │
                          │                 │    YES
                          │                 │    │
                          │                 │    ▼
                          │                 │ Return error:
                          │                 │ "Complete fields:"
                          │                 │ • field1
                          │                 │ • field2
                          │                 │ • ...
                          │                 │    │
                          │                 │    NO
                          │                 │
        ┌─────────────────┼─────────────────┤
        │                 │                 │
        ▼                 ▼                 ▼
   RETRIEVE RAG CONTEXT (same for all)
        │
        ▼
   FORMAT TEMPLATE
        │
        ├─ L1_GENERATE template          ├─ L3_GENERATE template
        ├─ Fill with user data             ├─ Fill with all phase data
        └─ Send to LLM                     └─ Send to LLM
        │                                   │
        ▼                                   ▼
   CALL LLM                              CALL LLM
   task="agreement"                      task="agreement"
   temperature=0.4                       system=L3_SYSTEM
        │                                   │
        ▼                                   ▼
   GET RESPONSE                          GET RESPONSE
   (1-2 pages)                           (15-25 pages)
        │                                   │
        └─────────────────┬─────────────────┘
                          │
                          ▼
                   STORE IN SESSION
                   session.full_output = text
                          │
                          ▼
                   DISPLAY IN UI
                   Return to user
```

---

## 5. LLM INVOKE FLOW - With Error Handling

```
invoke_llm(prompt, task, system)
        │
        ▼
TRY:
  │
  ├─ Create message list:
  │  ├─ SystemMessage(content=system_prompt)
  │  └─ HumanMessage(content=prompt)
  │
  ├─ Get LLM instance:
  │  └─ get_llm(task)
  │     ├─ Find temperature by task:
  │     │  ├─ "chat": 0.7 (varied)
  │     │  ├─ "agreement": 0.4 (consistent)
  │     │  └─ "extraction": 0.4 (consistent)
  │     │
  │     └─ Find tokens by task:
  │        ├─ "chat": 2048
  │        ├─ "agreement": 4000
  │        └─ "extraction": 4096
  │
  ├─ Invoke Gemini API:
  │  └─ llm.invoke([system_msg, human_msg])
  │     └─ Calls Google Gemini 2.5 Flash
  │
  ├─ Extract response:
  │  └─ response.content.strip()
  │
  └─ Return response text
        │
        ▼
   ✓ SUCCESS

EXCEPT Exception as e:
  │
  ├─ Catch error
  │  ├─ Network timeout
  │  ├─ API rate limit
  │  ├─ Invalid API key
  │  ├─ Model not found
  │  └─ Empty response
  │
  └─ Return graceful error:
     "[LLM Error: connection timeout]"
        │
        ▼
   ✓ FAIL GRACEFULLY
   (UI continues, shows error message)
```

---

## 6. SESSION STATE MACHINE - Field Progression

```
session.level = "L3"
session.current_phase = "phase_1"
session.current_field_index = 0
        │
        ▼
LOOP: while not all_complete
        │
        ├─ get_field(session)
        │  └─ Get phase 1, field 0 definition
        │     {
        │       "key": "provider_name",
        │       "question": "Provider company name?",
        │       "required": True
        │     }
        │
        ├─ Display question to user
        │
        ├─ User enters answer
        │
        ├─ process_answer(session, answer)
        │  ├─ Store answer
        │  ├─ Check risks
        │  ├─ Get LLM response
        │  └─ Parse signal
        │
        ├─ Display response + risks
        │
        └─ IF advance:
           │
           ├─ _advance(session)
           │  │
           │  ├─ fields = get_phase_fields("phase_1")
           │  │
           │  ├─ session.current_field_index++
           │  │  (0 → 1 → 2 → ... → 7)
           │  │
           │  ├─ IF current_field_index >= len(fields):
           │  │  │
           │  │  ├─ Move to next phase:
           │  │  │  session.current_phase = "phase_2"
           │  │  │  session.current_field_index = 0
           │  │  │
           │  │  ├─ IF no more phases:
           │  │  │  session.all_complete = True
           │  │  │  BREAK
           │  │
           │  └─ CONTINUE LOOP with next field
           │
           └─ Next iteration: Phase 1, Field 1

END LOOP when all_complete = True
        │
        ▼
All 5 phases complete!
Ready for generation
```

---

## 7. ERROR HANDLING STRATEGY

```
SCENARIO: API FAILURE
        │
        ├─ LLM request times out (>30s)
        │  └─ Caught by try/except
        │     └─ Return "[LLM Error: timeout]"
        │        └─ UI shows error, continues
        │
        ├─ Google API rate limit hit
        │  └─ Caught by try/except
        │     └─ Return "[LLM Error: rate limit]"
        │        └─ Show message "Try again in 1 minute"
        │
        ├─ Invalid API key
        │  └─ Caught by try/except
        │     └─ Return "[LLM Error: invalid key]"
        │        └─ Show config help
        │
        └─ Knowledge base missing
           └─ check_kb() returns {exists: False}
              └─ Display "Please ingest documents first"
                 └─ Provide run_ingestion() link

SCENARIO: USER INPUT ERROR
        │
        ├─ Blank answer on required field
        │  └─ Still stored (no validation on input)
        │     └─ Fails at generation time
        │        └─ Return validation error list
        │
        └─ Invalid selections
           └─ Show clarification question
              └─ Limit to 1 clarification per field
                 └─ Auto-advance after 1 retry

SCENARIO: DATA CORRUPTION
        │
        └─ Proposal JSON unreadable
           └─ load_proposal() returns None
              └─ Skip in list display
                 └─ User doesn't see corrupted file
```

---

## 8. PERFORMANCE FLOW - Timing Breakdown

```
USER INTERACTION TIMELINE:

0ms     │ User enters answer
        │
5ms     ├─ Store in session.slots
        │
10ms    ├─ Check risks (25 rules)
        │
15ms    ├─ RAG retrieval +200ms
        │  ├─ BM25 search (20ms)
        │  ├─ Dense search (100ms)
        │  └─ Fusion (5ms)
        │
220ms   ├─ Format LLM prompt
        │
225ms   ├─ Send to LLM API
        │
2-5s    │ LLM inference (Google Gemini)
        │
5225ms  ├─ Receive response
        │
5230ms  ├─ Parse ADVANCE/CLARIFY signal
        │
5235ms  ├─ Update UI
        │
5500ms  │ ✓ USER SEES RESPONSE

────────────────────────────────────

PER PHASE (5 questions): ~25-30 seconds
L3 COMPLETE (35 questions): ~3-4 minutes
L1 COMPLETE (8 questions): ~1.5 minutes
L2 COMPLETE (15 questions): ~2 minutes

Bottleneck: LLM API latency (80% of wait time)
After caching: Dense search becomes main bottleneck
```

---

## 9. FIGURE 3.1 — High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   USER INTERACTION LAYER                        │
│                                                                 │
│   Streamlit Web Application  (app.py)                           │
│   • Select proposal level  (L1 / L2 / L3)                      │
│   • Define telecom scenario and sub-sector                      │
│   • Trigger ingestion, generation, and save                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│           DOCUMENT INGESTION AND KNOWLEDGE BASE                 │
│                                                                 │
│   Input documents: PDF and DOCX  (rag_data/)                    │
│   ├── Parse and clean text                                      │
│   ├── Segment into chunks with metadata                         │
│   │     (source, chunk_id, chunk_size, section_heading)         │
│   ├── Vector store  ──────────────────►  ChromaDB               │
│   └── BM25 index   ──────────────────►  bm25_chunks.pkl         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RETRIEVAL LAYER                            │
│                                                                 │
│   ┌─────────────────┐     ┌──────────────────┐                  │
│   │  Dense Retrieval │     │  BM25 Retrieval  │                  │
│   │  ChromaDB +      │     │  Keyword-based   │                  │
│   │  MiniLM-L6-v2   │     │  lexical search  │                  │
│   └────────┬────────┘     └────────┬─────────┘                  │
│            └──────────┬────────────┘                            │
│                       ▼                                         │
│           Hybrid Retrieval — Reciprocal Rank Fusion             │
│                (60% BM25 + 40% Dense)                           │
│                       │                                         │
│                       ▼                                         │
│               Top-K ranked documents                            │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GENERATION LAYER                            │
│                                                                 │
│   Proposal Agent  (proposal_agent.py)                           │
│   ├── Construct prompt from retrieved context + user slots      │
│   ├── Invoke Gemini 2.5 Flash (LLM generation)                  │
│   └── CRAG variant: corrective filtering (experimental)         │
│         evaluated separately in  crag_comparison/              │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│               LOGGING AND EVALUATION LAYER                      │
│                                                                 │
│   Run logs — JSON files per configuration                       │
│   ├── rag_top3/5/7/10.json   — RAG benchmark results           │
│   ├── crag_top3/5/7/10.json  — CRAG benchmark results          │
│   ├── evaluation_report.json — full retrieval evaluation        │
│   └── experiment_data.json   — ablation experiment data         │
│                                                                 │
│   Metrics recorded per run                                      │
│   ├── Keyword coverage                                          │
│   ├── Source accuracy                                           │
│   ├── Pass rate by category and difficulty                      │
│   └── Retrieval time (ms)                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Legend

```
┌─┐         ═══════════        ───────
│ │  Box    Process Block     Data flow
└─┘

▼         ✓           ⚠️         🚨
Down      Success    Warning   Critical
arrow     Check      Yellow    Red
          Green
```

---

**All diagrams are text-based and will display correctly everywhere!**
