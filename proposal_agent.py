"""
Dark Fibre Framework Agreement Engine - Core Agent
====================================================

The Agent class is the main orchestrator for the proposal wizard. It manages
the multi-step user interaction flow across 3 proposal levels (L1/L2/L3) and
coordinates all major systems:

- Session State Management: Track user answers across wizard screens
- Multi-Level Generation: Generate different proposal formats by level
- Field Progression: Navigate through questions in correct order
- Cross-Clause Risk Detection: Identify dangerous clause combinations
- RAG Integration: Pull context from knowledge base for answers
- LLM Orchestration: Invoke Gemini with appropriate prompts

Architecture:
    User Input → Agent.process_answer() → LLM Chat → Risk Check → Store Answer → Advance
    
Session Lifecycle:
    1. create_session() → Creates new Session object
    2. greeting() → Display welcome message
    3. get_field() → Retrieve current question
    4. process_answer() → Handle user input + risk check + LLM response
    5. generate() → Produce final proposal document
    6. generate_risk() → Create risk summary

Dependencies:
    - Session: State persistence model (agent_state.py)
    - Field definitions: phases.py, levels.py
    - LLM: invoke_llm() from llm_engine.py
    - RAG: retrieve_context() from rag_retriever.py
    - Risk: check_risks() from cross_clause_rules.py
    - Prompts: All templates from prompts.py
"""

from datetime import datetime
from typing import Dict, Optional, Tuple, List, Any
from agent_state import Session
from phases import get_phase, get_phase_fields, get_all_phase_keys
from levels import get_l1l2_fields
from cross_clause_rules import check_risks, STANDARD_DEFAULTS
from rag_retriever import retrieve_context
from llm_engine import invoke_llm
from prompts import (
    CHAT_RESPONSE, EXPLAIN_FIELD, RAG_QUESTION,
    L1_GENERATE, L2_GENERATE, L3_GENERATE, L3_RISK_SUMMARY,
    SYSTEM_PROMPT, L3_SYSTEM
)


class Agent:
    """
    Core orchestrator for multi-level proposal generation wizard.
    
    Manages proposal generation across 3 levels:
    - L1 Quick: 8 questions, 2 minutes
    - L2 Standard: 15 questions, 5 minutes
    - L3 Dark Fibre: 35+ questions across 5 phases, 15+ minutes
    
    Attributes:
        sessions (Dict[str, Session]): Active sessions keyed by session ID
    """
    
    def __init__(self):
        """Initialize empty sessions dictionary."""
        self.sessions: Dict[str, Session] = {}

    def create_session(self, level: Optional[str] = None, sub_sector: Optional[str] = None) -> Session:
        """
        Create a new proposal session with unique ID.
        
        Args:
            level (str, optional): Proposal level ("L1", "L2", or "L3"). Defaults to "L1" if not set.
            sub_sector (str, optional): Telecom subsector or use case. Defaults to empty string.
            
        Returns:
            Session: New session object
            
        Session ID Format:
            df_YYYYMMDDhhmmss (e.g., "df_20260324_114640")
            Sortable by creation timestamp
            
        Examples:
            >>> agent = Agent()
            >>> session = agent.create_session("L3", "Core Network")
            >>> session.level
            'L3'
            >>> session.subsector
            'Core Network'
        """
        sid = f"df_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        s = Session(session_id=sid)
        if level:
            s.level = level
        if sub_sector:
            s.subsector = sub_sector
        self.sessions[sid] = s
        return s

    def greeting(self, session: Optional[Session] = None) -> str:
        """
        Generate personalized greeting message for session start.
        
        Greeting varies by proposal level (L1/L2 = quick, L3 = detailed wizard intro).
        Informs user about what to expect and sets expectations.
        
        Args:
            session (Session, optional): Current session. Auto-detects level from session.level.
        
        Returns:
            str: Greeting message with markdown formatting for Streamlit display
            
        Examples:
            >>> agent = Agent()
            >>> s = agent.create_session("L1")
            >>> greeting = agent.greeting(s)
            >>> "Quick Proposal" in greeting
            True
        """
        if session and session.level in ("L1", "L2"):
            level_names = {"L1": "Quick Proposal", "L2": "Standard Proposal"}
            name = level_names.get(session.level, "Proposal")
            return (
                f"Welcome to the **{name} Wizard**.\n\n"
                "I'll ask you a few quick questions and generate a professional proposal.\n\n"
                "Let's get started — **Question 1: who is this proposal for?**"
            )
        return (
            "Welcome to the **Dark Fibre Framework Agreement Wizard**.\n\n"
            "**8 phases · 32 questions.** Most have smart defaults — "
            "type **'defaults'** to accept standard UK telecom terms.\n\n"
            "1️⃣ Provider Details\n2️⃣ Customer Details\n"
            "3️⃣ Agreement Terms\n4️⃣ Services & Route\n"
            "5️⃣ Wayleave & Access\n6️⃣ Commercials & Pricing\n"
            "7️⃣ Liability & Termination\n8️⃣ Technical SLAs\n\n"
            "Let's go — **Phase 1: Provider details.**"
        )

    def get_field(self, s: Session) -> Optional[Dict[str, Any]]:
        """
        Get current field/question definition for this session.
        
        Returns appropriate field from levels (L1/L2) or phases (L3) based on
        session progress (current_field_index and current_phase).
        
        Args:
            s (Session): Session to fetch field for
            
        Returns:
            Optional[Dict]: Field definition with keys: key, question, clause, required, defaults, etc.
                           Returns None if past last field (session complete).
                           
        Examples:
            >>> s = agent.create_session("L1")
            >>> field = agent.get_field(s)
            >>> field["key"]
            'client_name'  # First L1 field
        """
        if s.level in ("L1", "L2"):
            fields = get_l1l2_fields(s.level)
            return fields[s.current_field_index] if s.current_field_index < len(fields) else None
        fields = get_phase_fields(s.current_phase)
        return fields[s.current_field_index] if s.current_field_index < len(fields) else None

    def get_phase_info(self, s: Session) -> Dict[str, Any]:
        """
        Get metadata about current L3 phase (title, description, clause count).
        
        Internal helper for UI display. Only relevant for L3 proposals.
        """
        return get_phase(s.current_phase)

    def get_phase_num(self, s: Session) -> int:
        """
        Get 1-indexed current phase number for L3 proposals.
        
        Returns phase number (1-5) or 0 if not in L3 or invalid phase.
        """
        keys = get_all_phase_keys()
        return keys.index(s.current_phase) + 1 if s.current_phase in keys else 0

    def get_progress(self, s: Session) -> Tuple[int, int, int, int]:
        """
        Calculate progress metrics for UI progress bar.
        
        Returns:
            Tuple[int, int, int, int]:
                - current_question: Current field index (0-indexed)
                - total_questions: Total fields in this level/wizard
                - current_phase: Phase number (1-indexed) or 1 for L1/L2
                - total_phases: 5 for L3, 1 for L1/L2
                
        Examples:
            >>> s = agent.create_session("L1")
            >>> done, total, phase, phases = agent.get_progress(s)
            >>> total
            8  # L1 has 8 fields
        """
        if s.level in ("L1", "L2"):
            total = len(get_l1l2_fields(s.level))
            return s.current_field_index, total, 1, 1
        
        keys = get_all_phase_keys()
        total = sum(len(get_phase_fields(k)) for k in keys)
        done = sum(len(get_phase_fields(k)) for k in keys[:keys.index(s.current_phase)]) + s.current_field_index
        return done, total, self.get_phase_num(s), len(keys)

    def process_answer(self, s: Session, inp: str) -> Tuple[str, bool]:
        """
        Process user's answer to current question.
        
        Main wizard interaction handler. Orchestrates:
        1. Validate and store user input
        2. Fill missing defaults
        3. Check cross-clause risks
        4. Invoke LLM for acknowledgment + optional clarification
        5. Limit clarifications to prevent infinite loops
        6. Advance to next field if satisfied
        
        Args:
            s (Session): Current session
            inp (str): User's answer to current question
            
        Returns:
            Tuple[str, bool]:
                - str: AI response (acknowledgment ± risk warnings ± clarification question)
                - bool: Whether to advance to next field (True) or retry current (False)
                
        Special Inputs:
            - "defaults", "default", "standard", "keep", "ok", "fine": Apply field defaults
            - "last signature" or "a" for effective_date: Convert to standard date
            
        Error Handling:
            LLM errors caught gracefully, returns "[LLM Error: ...]" but continues.
            Always attempts field advancement even if LLM fails.
            
        Examples:
            >>> s = agent.create_session("L1")
            >>> resp, advance = agent.process_answer(s, "Acme Corp")
            >>> advance
            True  # Moved to next field
            >>> resp.startswith("✅") or resp.startswith("Got it")
            True
        """
        field = self.get_field(s)
        if not field:
            return "All done! Ready to generate.", True
        
        inp = inp.strip()

        # ─ Special: Handle smart defaults ─
        if inp.lower() in ("defaults", "default", "standard", "keep", "ok", "fine"):
            defs = field.get("defaults", {})
            for dk, dv in defs.items():
                s.set_slot(dk, dv)
            s.set_slot(field["key"], f"Defaults: {defs}" if defs else inp)
            self._advance(s)
            return "✅ Smart defaults applied!", True

        # ─ Special: Handle date field shorthand ─
        if field["key"] == "effective_date" and inp.lower() in ("last signature", "a"):
            inp = "Date of last signature"

        # Store answer
        s.set_slot(field["key"], inp)
        
        # Fill missing dependent defaults (if any)
        for dk, dv in field.get("defaults", {}).items():
            if dk not in s.slots:
                s.set_slot(dk, dv)

        # ─ Check cross-clause risks ─
        warnings = check_risks(s.slots)
        new_warnings = [w for w in warnings if w not in s.risk_warnings]
        s.risk_warnings.extend(new_warnings)

        # ─ Get LLM response ─
        needs_clarify = False
        try:
            raw = invoke_llm(
                CHAT_RESPONSE.format(
                    level_name=s.level,
                    phase=get_phase(s.current_phase).get("title", ""),
                    clause=field.get("clause", ""),
                    question=field["question"][:200],
                    answer=inp,
                    risk_logic=field.get("risk_logic", "None"),
                    slots=s.slots_summary()
                ),
                task="chat"
            )
            lines = raw.strip().split("\n")
            signal = lines[-1].strip().upper() if lines else "ADVANCE"
            
            if signal in ("ADVANCE", "CLARIFY"):
                resp = "\n".join(lines[:-1]).strip()
                needs_clarify = signal == "CLARIFY"
            else:
                resp = raw
        except Exception:
            resp = "Got it — noted."

        # ─ Limit clarifications to 1 per field ─
        field_key = field["key"]
        if needs_clarify:
            if s.clarify_counts.get(field_key, 0) >= 1:
                # Already clarified once — force advance to prevent infinite loops
                needs_clarify = False
                resp = resp.rstrip("?").rstrip() + ". Got it, moving on!"
            else:
                s.clarify_counts[field_key] = s.clarify_counts.get(field_key, 0) + 1
        else:
            s.clarify_counts[field_key] = 0

        # ─ Append risk warnings to response ─
        if new_warnings:
            resp += "\n\n" + "\n".join(w["msg"] for w in new_warnings)

        # ─ Advance if satisfied ─
        if not needs_clarify:
            self._advance(s)
            
        return resp, not needs_clarify

    def skip(self, s: Session) -> str:
        """
        Skip current field and apply defaults.
        
        Args:
            s (Session): Current session
            
        Returns:
            str: Status message
        """
        field = self.get_field(s)
        if not field:
            return "Nothing to skip."
        
        for dk, dv in field.get("defaults", {}).items():
            s.set_slot(dk, dv)
        s.set_slot(field["key"], "[Defaults applied]")
        self._advance(s)
        return "Defaults applied, moving on."

    def go_back(self, s: Session) -> None:
        """
        Navigate to previous field.
        
        For L1/L2: Decrement field index within level.
        For L3: Decrement field within phase, or go to last field of previous phase.
        
        Args:
            s (Session): Current session
            
        Returns:
            None (modifies session in-place)
        """
        if s.current_field_index > 0:
            s.current_field_index -= 1
        elif s.level == "L3" and s.current_phase != "phase_1":
            keys = get_all_phase_keys()
            s.current_phase = keys[keys.index(s.current_phase) - 1]
            s.current_field_index = len(get_phase_fields(s.current_phase)) - 1
        s.all_complete = False

    def _advance(self, s: Session) -> None:
        """
        Internal: Advance session to next field or mark complete.
        
        For L1/L2: Increment field index, mark complete when past last field.
        For L3: Increment field in current phase; if phase complete, move to next phase.
        """
        if s.level in ("L1", "L2"):
            s.current_field_index += 1
            if s.current_field_index >= len(get_l1l2_fields(s.level)):
                s.all_complete = True
            return
        
        # L3 logic
        fields = get_phase_fields(s.current_phase)
        s.current_field_index += 1
        if s.current_field_index >= len(fields):
            # Move to next phase
            keys = get_all_phase_keys()
            idx = keys.index(s.current_phase)
            if idx + 1 < len(keys):
                s.current_phase = keys[idx + 1]
                s.current_field_index = 0
            else:
                s.all_complete = True

    def explain(self, s: Session) -> str:
        """
        Provide user-friendly explanation of current field/clause.
        
        Invokes LLM to explain the "why" and "so what" of the current question.
        Helps users understand the business implications before answering.
        
        Args:
            s (Session): Current session
            
        Returns:
            str: Explanation text (3-5 sentences)
        """
        field = self.get_field(s)
        if not field:
            return "No field to explain."
        try:
            return invoke_llm(
                EXPLAIN_FIELD.format(
                    field=field["key"].replace("_", " "),
                    clause=field.get("clause", ""),
                    level_name=s.level
                )
            )
        except Exception:
            return f"This relates to {field.get('clause', '')}."

    def ask_rag(self, s: Session, question: str) -> str:
        """
        Answer user's off-topic question using knowledge base context.
        
        Retrieves 4 most relevant documents from RAG system and has LLM
        answer user's question with that context. Enables exploration while
        staying grounded in reference materials.
        
        Args:
            s (Session): Current session
            question (str): User's free-form question
            
        Returns:
            str: Answer grounded in reference materials
            
        Examples:
            >>> s = agent.create_session("L3")
            >>> answer = agent.ask_rag(s, "What is TTTR in Dark Fibre?")
            >>> len(answer) > 0
            True
        """
        try:
            ctx, _ = retrieve_context(question, max_docs=4)
            if not ctx.strip():
                ctx = "No reference material."
            field = self.get_field(s)
            current_q = field["question"] if field else "No active question."
            return invoke_llm(
                RAG_QUESTION.format(
                    question=question,
                    rag_context=ctx,
                    level=s.level,
                    subsector=s.subsector,
                    current_question=current_q
                ),
                task="chat"
            )
        except Exception as e:
            return f"[RAG Error: {str(e)[:100]}]"

    def _required_fields(self, s: Session) -> List[str]:
        """Internal: Get list of required field keys for this session's level."""
        if s.level in ("L1", "L2"):
            return [f["key"] for f in get_l1l2_fields(s.level) if f.get("required")]
        keys = []
        for phase_key in get_all_phase_keys():
            for f in get_phase_fields(phase_key):
                if f.get("required"):
                    keys.append(f["key"])
        return keys

    def _is_invalid_value(self, value: Any) -> bool:
        """Internal: Check if a value is a placeholder or invalid."""
        if value is None:
            return True
        if isinstance(value, str):
            clean = value.strip().lower()
            invalid_values = ("", "[tbc]", "[to be confirmed]", "[defaults applied]")
            if clean in invalid_values:
                return True
            if "[tbc]" in clean or "[to be confirmed]" in clean:
                return True
        return False

    def _missing_required_fields(self, s: Session) -> List[str]:
        """Internal: Get list of required fields that are still unfilled."""
        missing = []
        for key in self._required_fields(s):
            v = s.slots.get(key)
            if self._is_invalid_value(v):
                missing.append(key)
        return missing

    def generate(self, s: Session) -> str:
        """
        Generate final proposal document from session state.
        
        Validates all required fields are filled, then dispatches to level-specific
        generator (generate_l1l2 or generate_agreement).
        
        Args:
            s (Session): Completed or nearly-completed session
            
        Returns:
            str: Full proposal document (Markdown formatted) or error message
            
        Validation:
            Returns error message (with field list) if required fields missing.
            Supports partial completion with "[To be confirmed]" placeholders.
            
        Examples:
            >>> s = agent.create_session("L1")
            >>> s.set_slot("client_name", "Acme")
            >>> proposal = agent.generate(s)  # Will error - needs more fields
            >>> "[Validation Error]" in proposal
            True
        """
        missing = self._missing_required_fields(s)
        if missing:
            field_list = ", ".join(missing)
            return (
                "[Validation Error] Cannot generate agreement. "
                f"The following required fields are missing or placeholders: {field_list}. "
                "Please complete all required fields before generation."
            )
        
        if s.level == "L3":
            return self.generate_agreement(s)
        return self.generate_l1l2(s)

    def generate_l1l2(self, s: Session) -> str:
        """
        Generate L1 or L2 proposal (quick or standard).
        
        Retrieves RAG context, invokes LLM with level-specific prompt,
        stores output in session, and returns formatted proposal.
        
        Args:
            s (Session): L1 or L2 session with fields filled
            
        Returns:
            str: Generated proposal Markdown
            
        Error Handling:
            Returns error message if LLM fails or returns empty response.
        """
        ctx, _ = retrieve_context(f"{s.subsector} telecom proposal", max_docs=4)
        ctx = ctx or ""
        try:
            if s.level == "L1":
                out = invoke_llm(
                    L1_GENERATE.format(
                        client_name=s.slots.get("client_name", "[TBC]"),
                        service_description=s.slots.get("service_description", "[TBC]"),
                        prepared_by=s.slots.get("prepared_by", "[TBC]"),
                        total_cost=s.slots.get("total_cost", "[TBC]"),
                        timeline=s.slots.get("timeline", "[TBC]"),
                        subsector=s.subsector,
                        date=datetime.now().strftime("%d %B %Y"),
                        rag_context=ctx
                    ),
                    task="agreement",
                    system=SYSTEM_PROMPT
                )
            else:  # L2
                out = invoke_llm(
                    L2_GENERATE.format(
                        proposal_title=s.slots.get("proposal_title", "[TBC]"),
                        client_name=s.slots.get("client_name", "[TBC]"),
                        service_description=s.slots.get("service_description", "[TBC]"),
                        prepared_by=s.slots.get("prepared_by", "[TBC]"),
                        validity_period=s.slots.get("validity_period", "[TBC]"),
                        subsector=s.subsector,
                        date=datetime.now().strftime("%d %B %Y"),
                        exec_summary_tone=s.slots.get("exec_summary_tone", "professional"),
                        scope_of_work=s.slots.get("scope_of_work", "[TBC]"),
                        total_cost=s.slots.get("total_cost", "[TBC]"),
                        timeline=s.slots.get("timeline", "[TBC]"),
                        contact_details=s.slots.get("contact_details", "[TBC]"),
                        rag_context=ctx
                    ),
                    task="agreement",
                    system=SYSTEM_PROMPT
                )
            
            if not out or not out.strip():
                return "[Error: LLM returned an empty response. Check your API key and model name in config.py.]"
            
            s.full_output = out
            return out
        except Exception as e:
            return f"[Error generating proposal: {str(e)[:200]}]"

    def generate_agreement(self, s: Session) -> str:
        """
        Generate L3 Dark Fibre framework agreement (legal-grade contract).
        
        Retrieves RAG context for telecom-specific clause guidance, merges all
        user answers with defaults, and invokes LLM with L3-specific prompt
        (domain knowledge about wayleave, liability, SLAs, etc.).
        
        Args:
            s (Session): L3 session with all 5 phases completed
            
        Returns:
            str: Generated agreement as numbered clauses + schedules
            
        Error Handling:
            Returns error message if LLM fails. Still saves partial output if available.
        """
        ctx, _ = retrieve_context(
            "dark fibre framework agreement wayleave liability SLA",
            max_docs=4
        )
        ctx = ctx or ""
        
        # Build list of defaults that weren't overridden by user
        applied = "\n".join(
            f"- {k}: {v}" for k, v in STANDARD_DEFAULTS.items()
            if k not in s.slots or not s.slots.get(k)
        )
        
        g = s.slots.get
        try:
            agr = invoke_llm(
                L3_GENERATE.format(
                    provider_name=g("provider_name", "[TBC]"),
                    provider_address=g("provider_address", "[TBC]"),
                    provider_company_no=g("provider_company_no", "[TBC]"),
                    provider_notice_email=g("provider_notice_email", "[TBC]"),
                    customer_name=g("customer_name", "[TBC]"),
                    customer_address=g("customer_address", "[TBC]"),
                    customer_company_no=g("customer_company_no", "[TBC]"),
                    customer_notice_email=g("customer_notice_email", "[TBC]"),
                    effective_date=g("effective_date", "Date of last signature"),
                    governing_law=g("governing_law", "English Law, Courts of England and Wales"),
                    dispute_resolution=g("dispute_resolution", "Expert Determination, then Courts of England and Wales"),
                    fibre_route=g("fibre_route", "[TBC]"),
                    fibre_specification=g("fibre_specification", "G.652D single-mode dark fibre"),
                    rfs_date=g("rfs_date", "[TBC]"),
                    wayleave_responsibility=g("wayleave_responsibility", "Customer"),
                    high_risk_sites=g("high_risk_sites", "None identified"),
                    access_notice_days=g("access_notice_days", "5 business days"),
                    equipment_ownership=g("equipment_ownership", "Supplier retains ownership"),
                    iru_charge=g("iru_charge", "[TBC]"),
                    om_charge=g("om_charge", "[TBC]"),
                    contract_term_months=g("contract_term_months", "[TBC]"),
                    indexation_model=g("indexation_model", "RPI (annual increase)"),
                    payment_terms_days=g("payment_terms_days", "30"),
                    general_liability_cap=g("general_liability_cap", "£50,000"),
                    order_liability_cap=g("order_liability_cap", "100% of annual fees for that Order"),
                    early_termination_fee=g("early_termination_fee", "100% of remaining minimum period fees"),
                    breach_cure_days=g("breach_cure_days", "30"),
                    force_majeure_days=g("force_majeure_days", "180"),
                    service_model=g("service_model", "Build + 12-month Warranty"),
                    tttr_hours=g("tttr_hours", "12 hours"),
                    service_credit_cap=g("service_credit_cap", "50% of annual O&M"),
                    noc_contact=g("noc_contact", "[TBC]"),
                    applied_defaults=applied,
                    rag_context=ctx
                ),
                task="agreement",
                system=L3_SYSTEM
            )
            
            if not agr or not agr.strip():
                return "[Error: LLM returned an empty response. Check your API key and model name in config.py.]"
            
            s.full_output = agr
            return agr
        except Exception as e:
            return f"[Error: {str(e)[:200]}]"

    def generate_risk(self, s: Session) -> str:
        """
        Generate commercial risk summary from cross-clause warnings.
        
        Aggregates all risk warnings triggered during wizard and creates
        executive summary explaining implications and recommendations.
        
        Args:
            s (Session): Session with risk_warnings populated
            
        Returns:
            str: Risk summary (1-2 pages, executive level)
            
        Error Handling:
            Returns error message if LLM fails.
        """
        warns = "\n".join(w["msg"] for w in s.risk_warnings) or "No specific risk warnings triggered."
        try:
            r = invoke_llm(
                L3_RISK_SUMMARY.format(
                    all_slots=s.slots_summary(),
                    risk_warnings=warns
                )
            )
            s.risk_summary = r
            return r
        except Exception as e:
            return f"[Error: {str(e)[:200]}]"
    