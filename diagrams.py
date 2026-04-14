"""
Dark Fibre Engine - System Architecture Diagrams Generator
Generates Mermaid diagrams for dissertation and presentation use.

Usage:
    python generate_diagrams.py
"""

from pathlib import Path

# Mermaid diagram templates
SYSTEM_ARCHITECTURE = r"""
graph TB
    subgraph "User Interface Layer"
        A[User] --> B[Streamlit Web App]
        B --> C{Select Level}
        C -->|L1 Quick| D[L1: 8-Field Form]
        C -->|L2 Standard| E[L2: 15-Field Form]
        C -->|L3 Dark Fibre| F[L3: 5-Phase Wizard]
    end

    F --> G[Phase 1: Provider Details<br/>4 fields]
    G --> H[Phase 2: Customer Details<br/>4 fields]
    H --> I[Phase 3: Agreement Terms<br/>3 fields]
    I --> J[Phase 4: Wayleave & Access<br/>8 fields]
    J --> K[Phase 5: Commercials<br/>6 fields]
    K --> L[Phase 6: Liability<br/>4 fields]
    L --> M[Phase 7: Termination<br/>3 fields]
    M --> N[Phase 8: Technical SLAs<br/>4 fields]

    subgraph "Core Processing Layer"
        O[DarkFibreAgent<br/>proposal_agent.py]
        P[Session Manager<br/>agent_state.py]
        Q[Phase Config<br/>phases.py]
        R[Level Config<br/>levels.py]
    end

    subgraph "AI/ML Layer"
        S[LLM Engine<br/>llm_engine.py<br/>Google Gemini]
        T[RAG Retriever<br/>rag_retriever.py<br/>ChromaDB]
        U[Prompts<br/>prompts.py]
        V[Risk Analysis<br/>cross_clause_rules.py]
    end

    subgraph "Data Layer"
        W[RAG Ingestion<br/>rag_ingest.py<br/>.doc/.pdf/.docx -> chunks -> embeddings]
        X[Document Storage<br/>rag_data/]
        Y[Proposal Storage<br/>storage.py<br/>JSON files]
        Z[Vector Database<br/>ChromaDB]
    end

    D --> O
    E --> O
    N --> O

    O --> P
    O --> Q
    O --> R

    O --> S
    S --> T
    S --> U
    S --> V

    W --> X
    W --> Z
    T --> Z

    O --> Y

    classDef userInterface fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef processing fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef ai fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef data fill:#fff3e0,stroke:#e65100,stroke-width:2px

    class A,B,C,D,E,F,G,H,I,J,K,L,M,N userInterface
    class O,P,Q,R processing
    class S,T,U,V ai
    class W,X,Y,Z data
"""

USER_JOURNEY = r"""
flowchart TD
    Start([Start]) --> Level{Choose Level}

    Level -->|L1 Quick| L1_Form[L1: Quick Form<br/>8 Fields<br/>Fast Generation]
    Level -->|L2 Standard| L2_Form[L2: Standard Form<br/>15 Fields<br/>Balanced]
    Level -->|L3 Dark Fibre| L3_Start[L3: 8-Phase Wizard<br/>36 Fields<br/>Comprehensive]

    L3_Start --> P1[Phase 1: Provider Details<br/>Company Name, Address, Registration No, Notice Email]
    P1 --> P2[Phase 2: Customer Details<br/>Company Name, Address, Registration No, Notice Email]
    P2 --> P3[Phase 3: Agreement Terms<br/>Effective Date, Governing Law, Dispute Resolution]
    P3 --> P4[Phase 4: Wayleave & Access<br/>Access Rights, Installation, Maintenance, Permissions, Route, Timeline, Costs, Conditions]
    P4 --> P5[Phase 5: Commercials<br/>Pricing, Payment Terms, Indexation, Minimum Term, Renewal, Termination Fees]
    P5 --> P6[Phase 6: Liability<br/>Provider Liability, Customer Liability, Indemnity, Insurance]
    P6 --> P7[Phase 7: Termination<br/>Termination Rights, Notice Periods, Consequences]
    P7 --> P8[Phase 8: Technical SLAs<br/>Service Levels, Performance Metrics, Monitoring, Penalties]

    P8 --> AI_Process[AI Processing<br/>Risk Analysis, RAG Retrieval, LLM Generation, Cross-Clause Validation]
    AI_Process --> Output[Final Output<br/>Framework Agreement, Risk Assessment, Compliance Check]

    L1_Form --> AI_Process_L1[Quick AI Generation]
    L2_Form --> AI_Process_L2[Standard AI Generation]

    AI_Process_L1 --> Output_L1[Quick Proposal]
    AI_Process_L2 --> Output_L2[Standard Proposal]

    Output --> End([Complete])
    Output_L1 --> End
    Output_L2 --> End

    style Start fill:#4CAF50,color:white
    style End fill:#4CAF50,color:white
    style L3_Start fill:#2196F3,color:white
    style AI_Process fill:#FF9800,color:white
"""

RAG_DATA_FLOW = r"""
flowchart LR
    subgraph "Document Ingestion"
        A1[Raw Documents<br/>.doc, .pdf, .docx] --> B1[Text Extraction<br/>rag_ingest.py]
        B1 --> C1[Chunking<br/>512-token chunks]
        C1 --> D1[Embedding Generation<br/>Dense Embeddings]
        D1 --> E1[Vector Storage<br/>ChromaDB]
    end

    subgraph "Query Processing"
        F1[User Query<br/>Contract Field Input] --> G1[Retriever<br/>rag_retriever.py]
        G1 --> H1[Similarity Matching<br/>Hybrid or Dense Search]
        H1 --> I1[Context Retrieval<br/>Top-K Relevant Chunks]
    end

    subgraph "AI Generation"
        J1[LLM Engine<br/>llm_engine.py] --> K1[Prompt Engineering<br/>prompts.py]
        K1 --> L1[Risk Analysis<br/>cross_clause_rules.py]
        L1 --> M1[Contract Generation<br/>Gemini]
    end

    E1 --> G1
    I1 --> K1
    M1 --> N1[Final Contract<br/>With Risk Assessment]

    style A1 fill:#e3f2fd
    style F1 fill:#f3e5f5
    style J1 fill:#e8f5e8
    style N1 fill:#fff3e0,stroke:#f57c00,stroke-width:3px
"""

def save_diagram(output_dir: Path, name: str, content: str) -> None:
    filename = output_dir / f"{name}.mmd"
    filename.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Saved {filename}")

def generate_html_viewer(output_dir: Path) -> None:
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dark Fibre Engine - System Diagrams</title>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .diagram-container {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4 {{
            color: #2c3e50;
        }}
        .nav {{
            background: #34495e;
            color: white;
            padding: 14px 18px;
            border-radius: 6px;
            margin-bottom: 20px;
        }}
        a {{
            color: #1565c0;
        }}
    </style>
</head>
<body>
    <div class="nav">
        <h1>Dark Fibre Engine - System Architecture Diagrams</h1>
        <p>Generated for dissertation and presentation use</p>
    </div>

    <div class="diagram-container">
        <h2>1. System Architecture Overview</h2>
        <div class="mermaid">
{SYSTEM_ARCHITECTURE}
        </div>
    </div>

    <div class="diagram-container">
        <h2>2. User Journey Flow</h2>
        <div class="mermaid">
{USER_JOURNEY}
        </div>
    </div>

    <div class="diagram-container">
        <h2>3. RAG Data Flow</h2>
        <div class="mermaid">
{RAG_DATA_FLOW}
        </div>
    </div>
</body>
</html>
"""
    viewer_path = output_dir / "diagrams_viewer.html"
    viewer_path.write_text(html_content, encoding="utf-8")
    print(f"Saved {viewer_path}")

def main() -> None:
    output_dir = Path.cwd()
    print("Generating Dark Fibre Engine system diagrams...")

    save_diagram(output_dir, "system_architecture", SYSTEM_ARCHITECTURE)
    save_diagram(output_dir, "user_journey", USER_JOURNEY)
    save_diagram(output_dir, "rag_data_flow", RAG_DATA_FLOW)
    generate_html_viewer(output_dir)

    print("\nFiles generated:")
    print(" - system_architecture.mmd")
    print(" - user_journey.mmd")
    print(" - rag_data_flow.mmd")
    print(" - diagrams_viewer.html")
    print("\nOpen diagrams_viewer.html in your browser.")

if __name__ == "__main__":
    main()