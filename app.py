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
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1.5rem 2rem !important; max-width: 1100px !important;}

    .ai-msg {
        background: linear-gradient(135deg, #1e3a5f, #1a3050);
        color: #e2e8f0; padding: 16px 20px;
        border-radius: 16px 16px 16px 4px; margin: 10px 0;
        font-size: 0.95rem; line-height: 1.6;
        border-left: 4px solid #3b82f6;
    }
    .user-msg {
        background: #f8fafc; color: #1e293b;
        padding: 14px 18px;
        border-radius: 16px 16px 4px 16px; margin: 10px 0;
        text-align: right; font-size: 0.95rem;
        border: 1px solid #e2e8f0;
    }
    .sys-msg {
        background: #fef9c3; color: #713f12;
        padding: 10px 16px; border-radius: 10px;
        margin: 6px 0; font-size: 0.88rem;
        border-left: 3px solid #eab308;
    }
    .risk-warn {
        background: #fef2f2; border-left: 4px solid #ef4444;
        color: #991b1b; padding: 12px 16px;
        border-radius: 8px; margin: 8px 0; font-size: 0.88rem;
    }
    .badge {
        display: inline-block; padding: 3px 10px;
        border-radius: 12px; font-size: 0.75rem;
        font-weight: 700; margin-bottom: 6px;
    }
    .badge-phase {background: #fef3c7; color: #92400e;}
    .badge-q {background: #dbeafe; color: #1e40af;}
    .badge-risk {background: #fee2e2; color: #991b1b;}
    .pv-h {
        color: #3b82f6; font-size: 0.72rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 2px;
    }
    .pv-v {
        color: #1e293b; font-size: 0.88rem; margin-bottom: 10px;
        padding-bottom: 6px; border-bottom: 1px solid #f1f5f9;
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
    h1, h2 = st.columns([4, 1])
    with h1:
        st.markdown("# 📡 Telecom Proposal Engine")
        st.markdown("**Choose your proposal level to get started**")
    with h2:
        if st.button("📁 My Proposals", use_container_width=True):
            st.session_state.pg = "proposals"
            st.rerun()
    st.markdown("---")

    # RAG status
    kb = check_kb()
    if not (kb["exists"] and kb["count"] > 0):
        if st.button("🔄 Run RAG Ingestion (one-time setup)"):
            with st.spinner("Ingesting documents into ChromaDB..."):
                if run_ingestion():
                    st.success("✅ Done!")
                    st.rerun()
                else:
                    st.error("No documents found in rag_data/")
        st.markdown("---")

    # Three level cards
    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        st.markdown("### ⚡ Level 1 — Quick")
        st.markdown("**5 questions** · 2-3 min")
        st.markdown("Fast, clean proposal export (~800 words)")
        sub1 = st.selectbox(
            "Sub-sector",
            ["Fibre Broadband Installation", "Wireless Networks", "VoIP Solutions"],
            key="sub1",
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

    with c2:
        st.markdown("### 📋 Level 2 — Standard")
        st.markdown("**10 questions** · 5-7 min")
        st.markdown("Full 9-section proposal (1500-2000 words)")
        sub2 = st.selectbox(
            "Sub-sector",
            ["Fibre Broadband Installation", "Wireless Networks", "VoIP Solutions", "Dark Fibre Leasing"],
            key="sub2",
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

    with c3:
        st.markdown("### 🔌 Level 3 — Dark Fibre")
        st.markdown("**12 screens** · under 2 min with defaults")
        st.markdown("Contract-grade 20-clause agreement + Risk Summary")
        st.caption("Dark Fibre only — type 'defaults' to go fast")
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
    rag_label = f"RAG: {kb['count']} chunks" if kb["exists"] and kb["count"] > 0 else "RAG offline"
    st.caption(f"Gemini 2.5 Flash · LangChain · ChromaDB ({rag_label}) · Streamlit")


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
        tb = st.columns([1, 1, 1, 1])
        with tb[0]:
            if st.button("❓ Explain", use_container_width=True, key="bex"):
                add_ai(A.explain(s), "Help")
                st.rerun()
        with tb[1]:
            if st.button("📚 Ask RAG", use_container_width=True, key="brag"):
                st.session_state.show_rag = not st.session_state.show_rag
                st.rerun()
        with tb[2]:
            clauses = pi.get("clauses", [])
            if clauses:
                st.caption(f"Clauses: {', '.join(clauses[:2])}")
        with tb[3]:
            if st.button("🏠 Home", use_container_width=True, key="bhome"):
                st.session_state.pg = "home"
                st.session_state.sess = None
                st.session_state.msgs = []
                st.rerun()

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
                b1, b2, b3, b4 = st.columns([1, 1, 1, 2])
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