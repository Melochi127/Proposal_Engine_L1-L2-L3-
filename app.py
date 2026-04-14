"""
Telecom Proposal Engine - Streamlit App
=========================================
L1 Quick | L2 Standard | L3 Dark Fibre — All in One
Run: streamlit run app.py
"""
import streamlit as st
from datetime import datetime
from proposal_agent import Agent
from levels import (
    get_level, get_l1l2_fields, get_l3_phase, get_l3_phase_fields,
    get_l3_phase_keys,
)
from rag_retriever import check_kb
from rag_ingest import run_ingestion
from storage import save_proposal, list_proposals, load_proposal, delete_proposal

# ━━━ Page Config ━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title="Telecom Proposal Engine", page_icon="📡", layout="wide")

# ━━━ CSS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
    /* ━━━ Hide Elements ━━━ */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stSidebar"] {display: none !important;}
    
    /* ━━━ Container & General ━━━ */
    .block-container {
        padding: 2rem 2.5rem !important; 
        max-width: 1200px !important;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        min-height: 100vh;
    }
    
    /* ━━━ Typography ━━━ */
    h1 {
        color: #0f172a !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        color: #1e293b !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
    }
    h3 {
        color: #334155 !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }
    
    /* ━━━ Chat Messages ━━━ */
    .ai-msg {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a8c 100%) !important;
        color: #f1f5f9 !important; 
        padding: 16px 20px !important;
        border-radius: 16px 16px 16px 4px !important; 
        margin: 12px 0 !important;
        font-size: 0.95rem !important; 
        line-height: 1.6 !important;
        border-left: 4px solid #0ea5e9 !important;
        box-shadow: 0 4px 12px rgba(30, 58, 95, 0.15) !important;
    }
    .user-msg {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        padding: 14px 18px !important;
        border-radius: 16px 16px 4px 16px !important; 
        margin: 12px 0 !important;
        text-align: right !important; 
        font-size: 0.95rem !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
    }
    .sys-msg {
        background: linear-gradient(135deg, #fef08a 0%, #fde047 100%) !important;
        color: #78350f !important;
        padding: 12px 16px !important; 
        border-radius: 10px !important;
        margin: 8px 0 !important; 
        font-size: 0.88rem !important;
        border-left: 4px solid #eab308 !important;
        box-shadow: 0 2px 8px rgba(234, 179, 8, 0.1) !important;
    }
    
    /* ━━━ Alerts & Warnings ━━━ */
    .risk-warn {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
        border-left: 4px solid #ef4444 !important;
        color: #7f1d1d !important; 
        padding: 14px 16px !important;
        border-radius: 8px !important; 
        margin: 10px 0 !important; 
        font-size: 0.88rem !important;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.1) !important;
    }
    
    /* ━━━ Badges ━━━ */
    .badge {
        display: inline-block; 
        padding: 4px 12px;
        border-radius: 20px; 
        font-size: 0.75rem;
        font-weight: 700; 
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-phase {
        background: linear-gradient(135deg, #fef3c7 0%, #fcd34d 100%);
        color: #92400e;
    }
    .badge-q {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
    }
    .badge-risk {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
    }
    
    /* ━━━ Preview Styles ━━━ */
    .pv-h {
        color: #0f766e !important; 
        font-size: 0.72rem !important; 
        font-weight: 700 !important;
        text-transform: uppercase !important; 
        letter-spacing: 0.08em !important; 
        margin: 12px 0 4px 0 !important;
    }
    .pv-v {
        color: #1e293b !important; 
        font-size: 0.9rem !important; 
        margin-bottom: 10px !important;
        padding: 8px 12px !important;
        background: #ffffff !important;
        border-radius: 6px !important;
        border-left: 3px solid #06b6d4 !important;
    }
    
    /* ━━━ Buttons ━━━ */
    .stButton > button {
        padding: 10px 20px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    /* ━━━ Cards ━━━ */
    .card {
        background: #ffffff !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
        border: 1px solid #e2e8f0 !important;
        transition: all 0.3s ease !important;
    }
    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12) !important;
        border-color: #cbd5e1 !important;
    }
    
    /* ━━━ Progress Bar ━━━ */
    .stProgress > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #0ea5e9 100%) !important;
        height: 8px !important;
    }
    
    /* ━━━ Input Fields ━━━ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* ━━━ Divider ━━━ */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent) !important;
        margin: 1.5rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ━━━ Session State ━━━━━━━━━━━━━━━━━━━━━━━━━
defaults = {"agent": Agent(), "sess": None, "msgs": [], "pg": "home", "out": "", "risk": "", "show_rag": False, "saved": False, "viewing": {}}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

A = st.session_state.agent


# ━━━ Chat Helpers ━━━━━━━━━━━━━━━━━━━━━━━━━━
def add_ai(c, tag=None):
    st.session_state.msgs.append({"r": "ai", "c": c, "tag": tag})

def add_user(c):
    st.session_state.msgs.append({"r": "usr", "c": c})

def add_sys(c):
    st.session_state.msgs.append({"r": "sys", "c": c})

def render_chat():
    for m in st.session_state.msgs:
        if m["r"] == "ai":
            badge = ""
            if m.get("tag"):
                badge = f'<span class="badge badge-phase">{m["tag"]}</span><br>'
            st.markdown(f'<div class="ai-msg">{badge}{m["c"]}</div>', unsafe_allow_html=True)
        elif m["r"] == "usr":
            st.markdown(f'<div class="user-msg">{m["c"]}</div>', unsafe_allow_html=True)
        elif m["r"] == "sys":
            st.markdown(f'<div class="sys-msg">ℹ️ {m["c"]}</div>', unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HOME — Level Selection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if st.session_state.pg == "home":
    # Header
    h1, h2 = st.columns([4, 1])
    with h1:
        st.markdown("# 📡 Telecom Proposal Engine")
        st.markdown("**Create professional telecom proposals in minutes with AI + RAG**")
    with h2:
        if st.button("📁 My Proposals", use_container_width=True):
            st.session_state.pg = "proposals"
            st.rerun()
    st.markdown("---")

    # RAG Status Card
    kb = check_kb()
    if not (kb["exists"] and kb["count"] > 0):
        st.info("🔄 **Knowledge Base Setup Required**")
        if st.button("📖 Initialize RAG (Ingest Documents)", use_container_width=True, type="primary"):
            with st.spinner("🔍 Scanning documents and building vector store..."):
                if run_ingestion():
                    st.success("✅ Knowledge base ready! 148+ chunks indexed.")
                    st.rerun()
                else:
                    st.error("❌ No documents found in rag_data/")
        st.markdown("---")
    
    # Level Cards Container
    st.markdown("### 🚀 Choose Your Proposal Type")
    
    c1, c2, c3 = st.columns(3, gap="large")

    # ─── LEVEL 1 ───
    with c1:
        st.markdown("""
        <div class="card">
            <h3 style="margin-top: 0; color: #0f172a;">⚡ Level 1 — Quick</h3>
            <p style="color: #64748b; margin-bottom: 16px;"><strong>5 questions</strong> • 2-3 minutes</p>
            <p style="color: #475569; margin-bottom: 16px;">Fast, clean proposal export (~800 words). Perfect for quick quotes and initial outreach.</p>
        </div>
        """, unsafe_allow_html=True)
        
        sub1 = st.selectbox(
            "Sub-sector",
            ["Fibre Broadband Installation", "Wireless Networks", "VoIP Solutions"],
            key="sub1",
            label_visibility="collapsed"
        )
        if st.button("Start L1 →", use_container_width=True, key="bl1", type="primary"):
            s = A.create_session("L1", sub1)
            st.session_state.sess = s
            st.session_state.pg = "wizard"
            st.session_state.msgs = []
            st.session_state.out = ""
            st.session_state.saved = False
            add_ai(A.greeting(s), "L1 Quick")
            st.rerun()

    # ─── LEVEL 2 ───
    with c2:
        st.markdown("""
        <div class="card">
            <h3 style="margin-top: 0; color: #0f172a;">📋 Level 2 — Standard</h3>
            <p style="color: #64748b; margin-bottom: 16px;"><strong>10 questions</strong> • 5-7 minutes</p>
            <p style="color: #475569; margin-bottom: 16px;">Full 9-section proposal (1500-2000 words). Ideal for detailed technical and commercial proposals.</p>
        </div>
        """, unsafe_allow_html=True)
        
        sub2 = st.selectbox(
            "Sub-sector",
            ["Fibre Broadband Installation", "Wireless Networks", "VoIP Solutions", "Dark Fibre Leasing"],
            key="sub2",
            label_visibility="collapsed"
        )
        if st.button("Start L2 →", use_container_width=True, key="bl2", type="primary"):
            s = A.create_session("L2", sub2)
            st.session_state.sess = s
            st.session_state.pg = "wizard"
            st.session_state.msgs = []
            st.session_state.out = ""
            st.session_state.saved = False
            add_ai(A.greeting(s), "L2 Standard")
            st.rerun()

    # ─── LEVEL 3 ───
    with c3:
        st.markdown("""
        <div class="card">
            <h3 style="margin-top: 0; color: #0f172a;">🔌 Level 3 — Dark Fibre</h3>
            <p style="color: #64748b; margin-bottom: 16px;"><strong>12 screens</strong> • under 2 min (with defaults)</p>
            <p style="color: #475569; margin-bottom: 16px;">Contract-grade 20-clause agreement + Risk Summary. Enterprise-level infrastructure contracts.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("💡 Type 'defaults' during wizard to skip optional fields")
        if st.button("Start L3 →", use_container_width=True, key="bl3", type="primary"):
            s = A.create_session("L3", "Dark Fibre")
            st.session_state.sess = s
            st.session_state.pg = "wizard"
            st.session_state.msgs = []
            st.session_state.out = ""
            st.session_state.saved = False
            add_ai(A.greeting(s), "L3 Dark Fibre")
            st.rerun()

    st.markdown("---")
    st.markdown("---")
    
    # Footer with tech stack
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📊 **Knowledge Base:** {kb['count']} chunks" if kb["exists"] else "📊 **Knowledge Base:** Offline")
    with col2:
        st.caption("🤖 **Model:** Gemini 2.5 Flash")
    with col3:
        st.caption("🔍 **Vector DB:** ChromaDB + BM25")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# WIZARD — All Levels
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif st.session_state.pg in ("wizard", "review"):
    s = st.session_state.sess
    lv = get_level(s.level)
    done, total, pnum, ptotal = A.get_progress(s)
    pct = (done / total * 100) if total else 0
    pi = A.get_phase_info(s)

    # Header
    if s.level == "L3":
        st.markdown(f"### {lv['icon']} Phase {pnum}/{ptotal}: {pi.get('title', '')}")
        if pi.get("description"):
            st.caption(pi["description"])
    else:
        st.markdown(f"### {lv['icon']} {lv['name']} — {s.subsector}")

    label = "screens" if s.level == "L3" else "questions"
    tip = " · type **'defaults'** to go fast" if s.level == "L3" else ""
    st.progress(pct / 100, text=f"{done}/{total} {label} ({pct:.0f}%){tip}")
    st.markdown("---")

    # Layout: Chat | Preview (widen right panel when output is ready)
    col_ratio = [1.2, 2] if st.session_state.out else [3, 1.2]
    chat_col, prev_col = st.columns(col_ratio, gap="large")

    # ── CHAT COLUMN ──
    with chat_col:
        # Toolbar
        tb = st.columns([1, 1, 1])
        with tb[0]:
            if st.button("❓ Explain", use_container_width=True, key="bex"):
                add_ai(A.explain(s), "Help")
                st.rerun()
        with tb[1]:
            if st.button("🏠 Home", use_container_width=True, key="bhome"):
                st.session_state.pg = "home"
                st.session_state.sess = None
                st.session_state.msgs = []
                st.rerun()
        with tb[2]:
            st.write("")  # spacer

        st.markdown("---")

        # Chat history
        render_chat()

        # RAG panel
        if st.session_state.show_rag:
            st.markdown("---")
            st.markdown("**📚 Ask the Knowledge Base**")
            rq = st.text_input(
                "Question:",
                placeholder="e.g. What is standard wayleave practice in UK telecoms?",
                key="rag_q",
            )
            if st.button("Ask", key="brqa") and rq:
                add_user(f"📚 {rq}")
                with st.spinner("Searching knowledge base..."):
                    ans = A.ask_rag(s, rq)
                add_ai(ans, "Knowledge Base")
                st.session_state.show_rag = False
                st.rerun()

        st.markdown("---")

        # ── Current Question or Review ──
        if not s.all_complete:
            field = A.get_field(s)
            if field is None:
                # Field index is past the end but all_complete wasn't set — fix and rerun
                s.all_complete = True
                st.rerun()
            if field:
                # Phase transition (L3)
                if s.level == "L3" and s.current_field_index == 0 and s.current_phase != "phase_1":
                    st.info(f"🔄 **Phase {pnum}: {pi['title']}** — {pi.get('description', '')}")

                # Question bubble
                risk_badge = ""
                if field.get("risk_logic"):
                    risk_badge = ' <span class="badge badge-risk">⚠️ Risk-aware</span>'

                if s.level == "L3":
                    q_label = f"Phase {pnum}"
                    badge_class = "badge-phase"
                else:
                    q_label = f"Q{done + 1}/{total}"
                    badge_class = "badge-q"

                st.markdown(
                    f'<div class="ai-msg">'
                    f'<span class="badge {badge_class}">{q_label}</span>{risk_badge}<br>'
                    f'🤖 {field["question"]}</div>',
                    unsafe_allow_html=True,
                )

                # Input field
                if len(field.get("question", "")) > 200:
                    user_input = st.text_area(
                        "Your answer:",
                        placeholder=field.get("hint", ""),
                        key=f"in_{s.current_phase}_{s.current_field_index}",
                        height=80,
                        label_visibility="collapsed",
                    )
                else:
                    user_input = st.text_input(
                        "Your answer:",
                        placeholder=field.get("hint", ""),
                        key=f"in_{s.current_phase}_{s.current_field_index}",
                        label_visibility="collapsed",
                    )

                # Action buttons
                b1, b2, b3, b4, b5 = st.columns([1, 1, 1, 1, 1.5])
                with b1:
                    if st.button("⬅️ Back", key="bb"):
                        A.go_back(s)
                        st.rerun()
                with b2:
                    if st.button("⏭️ Skip", key="bs"):
                        add_sys(A.skip(s))
                        st.rerun()
                with b3:
                    if st.button("❓ Help", key="bh"):
                        add_ai(A.explain(s), "Help")
                        st.rerun()
                with b4:
                    if st.button("📚 RAG", key="brag"):
                        st.session_state.show_rag = not st.session_state.show_rag
                        st.rerun()
                with b5:
                    if st.button("✅ Submit", key="bsub", type="primary"):
                        if user_input and user_input.strip():
                            add_user(user_input)
                            s.add_chat("user", user_input)
                            with st.spinner("Processing..."):
                                resp, _ = A.process_answer(s, user_input)
                            add_ai(resp, pi.get("title", ""))
                            s.add_chat("ai", resp)
                            st.rerun()
                        else:
                            st.warning("Please type an answer or click Skip.")
        else:
            # ── ALL COMPLETE — REVIEW ──
            st.session_state.pg = "review"
            st.success(f"🎉 All done! Review your data, then generate your {lv['name']}.")

            st.markdown("### 📋 Data Summary")

            if s.level == "L3":
                for pk in get_l3_phase_keys():
                    phase = get_l3_phase(pk)
                    st.markdown(f"**{phase['title']}**")
                    for ff in get_l3_phase_fields(pk):
                        v = s.slots.get(ff["key"], "")
                        if v and "[" not in v and "Defaults" not in v:
                            st.markdown(f"- {ff['key'].replace('_', ' ').title()}: {v[:200]}")
                    st.markdown("")

                if s.risk_warnings:
                    st.markdown("### ⚠️ Risk Warnings Triggered")
                    for w in s.risk_warnings:
                        st.markdown(f'<div class="risk-warn">{w["msg"]}</div>', unsafe_allow_html=True)
            else:
                for ff in get_l1l2_fields(s.level):
                    v = s.slots.get(ff["key"], "")
                    if v and v != "[To be confirmed]":
                        st.markdown(f"- **{ff['key'].replace('_', ' ').title()}:** {v[:200]}")

            st.markdown("---")

            gc1, gc2 = st.columns(2)
            with gc1:
                if st.button("✏️ Go Back & Edit", use_container_width=True, key="bed"):
                    s.all_complete = False
                    s.current_field_index = 0
                    if s.level == "L3":
                        s.current_phase = "phase_1"
                    st.session_state.pg = "wizard"
                    st.rerun()
            with gc2:
                btn_text = f"✨ Generate {lv['name']}"
                if st.button(btn_text, use_container_width=True, type="primary", key="bgen"):
                    missing = A._missing_required_fields(s)
                    if missing:
                        st.error(
                            "Cannot generate: required fields are missing or placeholders remain. "
                            f"Fill these fields first: {', '.join(missing)}"
                        )
                    else:
                        with st.spinner(f"🔄 Generating {lv['name']} with AI + RAG..."):
                            output = A.generate(s)
                        st.session_state.out = output
                        s.full_output = output

                        if s.level == "L3":
                            with st.spinner("📊 Generating Risk Summary..."):
                                st.session_state.risk = A.generate_risk(s)

                        st.balloons()
                        st.rerun()

    # ── PREVIEW COLUMN ──
    with prev_col:
        if st.session_state.out:
            # ── Generated output ──
            st.markdown(f"### {lv['icon']} {lv['name']}")
            st.markdown("---")

            e1, e2, e3 = st.columns(3)
            fname = f"{s.level}_{s.subsector.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
            with e1:
                st.download_button("📥 .md", st.session_state.out,
                    file_name=f"{fname}.md", mime="text/markdown", use_container_width=True)
            with e2:
                st.download_button("📥 .txt", st.session_state.out,
                    file_name=f"{fname}.txt", mime="text/plain", use_container_width=True)
            with e3:
                if st.session_state.saved:
                    st.success("Saved!")
                elif st.button("💾 Save", use_container_width=True, key="bsave"):
                    save_proposal(s, st.session_state.out, st.session_state.risk)
                    st.session_state.saved = True
                    st.rerun()

            if st.session_state.risk:
                tab1, tab2 = st.tabs(["📄 Agreement", "⚠️ Risk Summary"])
                with tab1:
                    st.markdown(st.session_state.out)
                with tab2:
                    st.markdown(st.session_state.risk)
            else:
                st.markdown(st.session_state.out)

        else:
            # ── Field preview while answering ──
            st.markdown("### 📄 Preview")
            st.markdown("---")

            if s and s.slots:
                if s.level == "L3":
                    for pk in get_l3_phase_keys():
                        phase = get_l3_phase(pk)
                        has_data = False
                        for ff in get_l3_phase_fields(pk):
                            v = s.slots.get(ff["key"])
                            if v and v.strip() and "[" not in v and "Defaults" not in v:
                                if not has_data:
                                    st.markdown(f'<div class="pv-h">{phase["title"]}</div>', unsafe_allow_html=True)
                                    has_data = True
                                name = ff["key"].replace("_", " ").title()
                                dv = v[:100] + "..." if len(v) > 100 else v
                                st.markdown(f'<div class="pv-v"><small>{name}:</small> {dv}</div>', unsafe_allow_html=True)
                else:
                    for ff in get_l1l2_fields(s.level):
                        v = s.slots.get(ff["key"])
                        if v and v.strip() and v != "[To be confirmed]":
                            name = ff["key"].replace("_", " ").title()
                            dv = v[:100] + "..." if len(v) > 100 else v
                            st.markdown(f'<div class="pv-h">{name}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="pv-v">{dv}</div>', unsafe_allow_html=True)

                st.markdown("---")
                st.markdown(f"**{pct:.0f}% complete**")
            else:
                st.info("Answers appear here as you go.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# OUTPUT — Generated Document
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif st.session_state.pg == "done":
    s = st.session_state.sess
    lv = get_level(s.level)
    output = st.session_state.out

    # Tabs for L3 (Agreement + Risk), single tab for L1/L2
    if s.level == "L3":
        tab1, tab2 = st.tabs(["📄 Framework Agreement", "⚠️ Risk Summary"])
    else:
        tab1 = st.tabs([f"📄 {lv['name']}"])[0]

    with tab1:
        if s.level == "L3":
            provider = s.slots.get("provider_details", "Provider")
            customer = s.slots.get("customer_details", "Customer")
            st.markdown(f"### 🔌 Dark Fibre Framework Agreement")
            st.markdown(f"*{provider} ↔ {customer}*")
        else:
            client = s.slots.get("client_name", "Client")
            prepared = s.slots.get("prepared_by", "Company")
            st.markdown(f"### {lv['icon']} {lv['name']}")
            st.markdown(f"*For: {client} | By: {prepared} | {s.subsector}*")

        st.markdown("---")

        # Export buttons
        e1, e2, e3, e4 = st.columns([1, 1, 1, 2])
        with e1:
            st.download_button(
                "📥 Download .md",
                output,
                file_name=f"{s.level}_{s.subsector.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with e2:
            st.download_button(
                "📥 Download .txt",
                output,
                file_name=f"{s.level}_{s.subsector.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with e3:
            if st.button("✏️ Edit & Regen", use_container_width=True, key="bre"):
                s.all_complete = False
                s.current_field_index = 0
                if s.level == "L3":
                    s.current_phase = "phase_1"
                st.session_state.pg = "wizard"
                st.rerun()
        with e4:
            if st.button("🏠 Home — New Proposal", use_container_width=True, key="bnew"):
                st.session_state.pg = "home"
                st.session_state.sess = None
                st.session_state.msgs = []
                st.session_state.out = ""
                st.session_state.risk = ""
                st.rerun()

        st.markdown("---")
        st.markdown(output)

    # Risk Summary tab (L3 only)
    if s.level == "L3":
        with tab2:
            st.markdown("### ⚠️ Executive Risk Summary")
            st.markdown(f"*Generated: {datetime.now().strftime('%d %B %Y')}*")
            st.markdown("---")
            st.markdown(st.session_state.risk)
            st.download_button(
                "📥 Download Risk Summary",
                st.session_state.risk,
                file_name=f"risk_summary_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

    st.markdown("---")
    st.caption(f"Telecom Proposal Engine — {lv['name']} | RAG + Gemini + LangChain + ChromaDB")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MY PROPOSALS — Saved Proposals Library
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif st.session_state.pg == "proposals":
    st.markdown("# 📁 My Proposals")
    if st.button("← Back to Home", key="bph"):
        st.session_state.pg = "home"
        st.rerun()
    st.markdown("---")

    proposals = list_proposals()
    if not proposals:
        st.info("No saved proposals yet. Generate one and click 💾 Save.")
    else:
        for p in proposals:
            level_icons = {"L1": "⚡", "L2": "📋", "L3": "🔌"}
            icon = level_icons.get(p["level"], "📄")
            with st.expander(f"{icon} {p['client']} — {p['label']} ({p['subsector']})  ·  {p['saved_at']}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.caption(f"ID: {p['id']}")
                with col2:
                    if st.button("📖 View", key=f"view_{p['filename']}", use_container_width=True):
                        rec = load_proposal(p["filename"])
                        if rec:
                            st.session_state.pg = "view_proposal"
                            st.session_state.viewing = rec
                            st.rerun()
                with col3:
                    if st.button("🗑️ Delete", key=f"del_{p['filename']}", use_container_width=True):
                        delete_proposal(p["filename"])
                        st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VIEW PROPOSAL — Single saved proposal
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif st.session_state.pg == "view_proposal":
    rec = st.session_state.get("viewing", {})
    if not rec:
        st.session_state.pg = "proposals"
        st.rerun()

    level_icons = {"L1": "⚡", "L2": "📋", "L3": "🔌"}
    icon = level_icons.get(rec.get("level", ""), "📄")

    st.markdown(f"# {icon} {rec.get('label', 'Proposal')} — {rec.get('client', '')}")
    st.caption(f"Saved: {rec.get('saved_at', '')}  ·  {rec.get('subsector', '')}")

    if st.button("← Back to My Proposals", key="bvp"):
        st.session_state.pg = "proposals"
        st.rerun()
    st.markdown("---")

    fname = f"{rec.get('level', 'proposal')}_{rec.get('subsector', '').replace(' ', '_')}_{rec.get('saved_at', '').replace(':', '').replace(' ', '_')}"
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button("📥 .md", rec.get("output", ""),
            file_name=f"{fname}.md", mime="text/markdown", use_container_width=True)
    with dl2:
        st.download_button("📥 .txt", rec.get("output", ""),
            file_name=f"{fname}.txt", mime="text/plain", use_container_width=True)

    st.markdown("---")
    if rec.get("risk"):
        tab1, tab2 = st.tabs(["📄 Proposal", "⚠️ Risk Summary"])
        with tab1:
            st.markdown(rec.get("output", ""))
        with tab2:
            st.markdown(rec.get("risk", ""))
    else:
        st.markdown(rec.get("output", ""))