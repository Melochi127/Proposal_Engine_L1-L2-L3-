"""Dark Fibre Engine V3 - Core Agent"""
from datetime import datetime
from agent_state import Session
from phases import get_phase, get_phase_fields, get_all_phase_keys
from levels import get_l1l2_fields
from cross_clause_rules import check_risks, STANDARD_DEFAULTS
from rag_retriever import retrieve_context
from llm_engine import invoke_llm
from prompts import *

class Agent:
    def __init__(self):
        self.sessions = {}

    def create_session(self, level=None, sub_sector=None):
        sid = f"df_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        s = Session(session_id=sid)
        if level:
            s.level = level
        if sub_sector:
            s.subsector = sub_sector
        self.sessions[sid] = s
        return s

    def greeting(self, session=None):
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
            "**12 quick screens** across 5 phases. Most have smart defaults — "
            "type **'defaults'** to accept standard UK telecom terms.\n\n"
            "1️⃣ Entity & Admin\n2️⃣ Wayleave & Access\n"
            "3️⃣ Commercials\n4️⃣ Liability & Termination\n5️⃣ Technical SLAs\n\n"
            "Let's go — **Phase 1: who are the parties?**"
        )

    def get_field(self, s):
        if s.level in ("L1", "L2"):
            fields = get_l1l2_fields(s.level)
            return fields[s.current_field_index] if s.current_field_index < len(fields) else None
        fields = get_phase_fields(s.current_phase)
        return fields[s.current_field_index] if s.current_field_index < len(fields) else None

    def get_phase_info(self, s): return get_phase(s.current_phase)

    def get_phase_num(self, s):
        keys = get_all_phase_keys()
        return keys.index(s.current_phase) + 1 if s.current_phase in keys else 0

    def get_progress(self, s):
        if s.level in ("L1", "L2"):
            total = len(get_l1l2_fields(s.level))
            return s.current_field_index, total, 1, 1
        keys = get_all_phase_keys()
        total = sum(len(get_phase_fields(k)) for k in keys)
        done = sum(len(get_phase_fields(k)) for k in keys[:keys.index(s.current_phase)]) + s.current_field_index
        return done, total, self.get_phase_num(s), len(keys)

    def process_answer(self, s, inp):
        field = self.get_field(s)
        if not field: return "All done! Ready to generate.", True
        inp = inp.strip()

        # Handle defaults
        if inp.lower() in ("defaults", "default", "standard", "keep", "ok", "fine"):
            defs = field.get("defaults", {})
            for dk, dv in defs.items(): s.set_slot(dk, dv)
            s.set_slot(field["key"], f"Defaults: {defs}" if defs else inp)
            self._advance(s)
            return "✅ Smart defaults applied!", True

        # Handle effective_date
        if field["key"] == "effective_date" and inp.lower() in ("last signature", "a"):
            inp = "Date of last signature"

        s.set_slot(field["key"], inp)
        # Fill missing defaults
        for dk, dv in field.get("defaults", {}).items():
            if dk not in s.slots: s.set_slot(dk, dv)

        # Check cross-clause risks
        warnings = check_risks(s.slots)
        new_warnings = [w for w in warnings if w not in s.risk_warnings]
        s.risk_warnings.extend(new_warnings)

        # AI response
        needs_clarify = False
        try:
            raw = invoke_llm(CHAT_RESPONSE.format(
                level_name=s.level,
                phase=get_phase(s.current_phase).get("title", ""),
                clause=field.get("clause", ""),
                question=field["question"][:200],
                answer=inp,
                risk_logic=field.get("risk_logic", "None"),
                slots=s.slots_summary()), task="chat")
            lines = raw.strip().split("\n")
            signal = lines[-1].strip().upper() if lines else "ADVANCE"
            if signal in ("ADVANCE", "CLARIFY"):
                resp = "\n".join(lines[:-1]).strip()
                needs_clarify = signal == "CLARIFY"
            else:
                resp = raw
        except:
            resp = "Got it — noted."

        # Limit clarification to 1 attempt per field
        field_key = field["key"]
        if needs_clarify:
            if s.clarify_counts.get(field_key, 0) >= 1:
                # Already clarified once — force advance
                needs_clarify = False
                resp = resp.rstrip("?").rstrip() + ". Got it, moving on!"
            else:
                s.clarify_counts[field_key] = s.clarify_counts.get(field_key, 0) + 1
        else:
            s.clarify_counts[field_key] = 0

        # Append risk warnings to response
        if new_warnings:
            resp += "\n\n" + "\n".join(w["msg"] for w in new_warnings)

        if not needs_clarify:
            self._advance(s)
        return resp, not needs_clarify

    def skip(self, s):
        field = self.get_field(s)
        if not field: return "Nothing to skip."
        for dk, dv in field.get("defaults", {}).items(): s.set_slot(dk, dv)
        s.set_slot(field["key"], "[Defaults applied]")
        self._advance(s)
        return "Defaults applied, moving on."

    def go_back(self, s):
        if s.current_field_index > 0:
            s.current_field_index -= 1
        elif s.level == "L3" and s.current_phase != "phase_1":
            keys = get_all_phase_keys()
            s.current_phase = keys[keys.index(s.current_phase) - 1]
            s.current_field_index = len(get_phase_fields(s.current_phase)) - 1
        s.all_complete = False

    def _advance(self, s):
        if s.level in ("L1", "L2"):
            s.current_field_index += 1
            if s.current_field_index >= len(get_l1l2_fields(s.level)):
                s.all_complete = True
            return
        fields = get_phase_fields(s.current_phase)
        s.current_field_index += 1
        if s.current_field_index >= len(fields):
            keys = get_all_phase_keys()
            idx = keys.index(s.current_phase)
            if idx + 1 < len(keys):
                s.current_phase = keys[idx + 1]; s.current_field_index = 0
            else:
                s.all_complete = True

    def explain(self, s):
        field = self.get_field(s)
        if not field: return "No field to explain."
        try:
            return invoke_llm(EXPLAIN_FIELD.format(
                field=field["key"].replace("_", " "),
                clause=field.get("clause", ""),
                level_name=s.level))
        except: return f"This relates to {field.get('clause', '')}."

    def ask_rag(self, s, question):
        try:
            ctx, _ = retrieve_context(question, max_docs=4)
            if not ctx.strip():
                ctx = "No reference material."
            return invoke_llm(RAG_QUESTION.format(
                question=question,
                rag_context=ctx,
                level=s.level,
                subsector=s.subsector
            ), task="chat")
        except Exception as e:
            return f"[RAG Error: {e}]"

    def _required_fields(self, s):
        if s.level in ("L1", "L2"):
            return [f["key"] for f in get_l1l2_fields(s.level) if f.get("required")]
        keys = []
        for phase_key in get_all_phase_keys():
            for f in get_phase_fields(phase_key):
                if f.get("required"):
                    keys.append(f["key"])
        return keys

    def _is_invalid_value(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            clean = value.strip().lower()
            if clean in ("", "[tbc]", "[to be confirmed]", "[to be confirmed]", "[defaults applied]"):
                return True
            if "[tbc]" in clean or "[to be confirmed]" in clean:
                return True
        return False

    def _missing_required_fields(self, s):
        missing = []
        for key in self._required_fields(s):
            v = s.slots.get(key)
            if self._is_invalid_value(v):
                missing.append(key)
        return missing

    def generate(self, s):
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

    def generate_l1l2(self, s):
        ctx, _ = retrieve_context(f"{s.subsector} telecom proposal", max_docs=4)
        ctx = ctx or ""
        try:
            if s.level == "L1":
                out = invoke_llm(L1_GENERATE.format(
                    client_name=s.slots.get("client_name", "[TBC]"),
                    service_description=s.slots.get("service_description", "[TBC]"),
                    prepared_by=s.slots.get("prepared_by", "[TBC]"),
                    total_cost=s.slots.get("total_cost", "[TBC]"),
                    timeline=s.slots.get("timeline", "[TBC]"),
                    subsector=s.subsector,
                    date=datetime.now().strftime("%d %B %Y"),
                    rag_context=ctx), task="agreement", system=SYSTEM_PROMPT)
            else:
                out = invoke_llm(L2_GENERATE.format(
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
                    rag_context=ctx), task="agreement", system=SYSTEM_PROMPT)
            if not out or not out.strip():
                return "[Error: LLM returned an empty response. Check your API key and model name in config.py.]"
            s.full_output = out
            return out
        except Exception as e:
            return f"[Error generating proposal: {e}]"

    def generate_agreement(self, s):
        ctx, _ = retrieve_context("dark fibre framework agreement wayleave liability SLA", max_docs=4)
        ctx = ctx or ""
        applied = "\n".join(f"- {k}: {v}" for k, v in STANDARD_DEFAULTS.items()
                           if k not in s.slots or not s.slots.get(k))
        g = s.slots.get
        try:
            agr = invoke_llm(L3_GENERATE.format(
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
                applied_defaults=applied, rag_context=ctx),
                task="agreement", system=L3_SYSTEM)
            if not agr or not agr.strip():
                return "[Error: LLM returned an empty response. Check your API key and model name in config.py.]"
            s.full_output = agr
            return agr
        except Exception as e: return f"[Error: {e}]"

    def generate_risk(self, s):
        warns = "\n".join(w["msg"] for w in s.risk_warnings) or "No specific risk warnings triggered."
        try:
            r = invoke_llm(L3_RISK_SUMMARY.format(
                all_slots=s.slots_summary(), risk_warnings=warns))
            s.risk_summary = r; return r
        except Exception as e: return f"[Error: {e}]"
   
    