"""
Dark Fibre Engine V3 - 12-Screen Wizard Flow
"""
PHASES = {
    "phase_1": {
        "title": "Entity & Admin",
        "description": "Who are the parties to this agreement?",
        "clauses": ["Cover Page", "Clause 19 (Notices)", "Signatures"],
        "fields": [
            {"key": "provider_details", "required": True, "clause": "Cover Page",
             "question": "Let's confirm **your details** as the Provider.\n\nPlease provide **company name, registered address, and company number** — all in one go.",
             "hint": "e.g. 'PMS Fibre Ltd, 123 Fibre Lane London EC1A 1BB, No. 12345678'"},
            {"key": "customer_details", "required": True, "clause": "Cover Page",
             "question": "Now the **Customer** — full legal name, registered address, and company number.\n\n*Use the exact entity name (Ltd/PLC/LLP), not a trading name.*",
             "hint": "e.g. 'Sky Networks Ltd, 456 Network Road Manchester M1 2AB, No. 87654321'"},
            {"key": "effective_date", "required": True, "clause": "Cover Page",
             "question": "Start date? Most use **'Date of last signature'** for flexibility.",
             "hint": "Type 'last signature' or a specific date", "default": "Date of last signature"},
            {"key": "notice_emails", "required": True, "clause": "Clause 19",
             "question": "Notice emails for both parties? *(Clause 19 — formal legal communications)*",
             "hint": "e.g. 'legal@provider.com / procurement@customer.com'"},
        ],
    },
    "phase_2": {
        "title": "Wayleave & Access",
        "description": "Wayleaves are the #1 cause of project failure in Dark Fibre.",
        "clauses": ["Clauses 3-5", "Schedule 1 (External Events)"],
        "fields": [
            {"key": "wayleave_and_access", "required": True, "clause": "Clauses 3-5",
             "question": "Three decisions about **site access**:\n\n**1. Wayleave responsibility:**\n  A) Customer *(lowest risk for you)*\n  B) Shared\n  C) Provider *(highest risk)*\n\n**2. High-risk sites?** (Railways, highways, MDUs) — or 'none'\n\n**3. Access notice?** Default 5 business days.\n\nType all three or just **'A'** for defaults.",
             "hint": "e.g. 'A, none, 5 days' or just 'A'",
             "risk_logic": "Provider wayleaves → add Long-Stop Date + Programme Relief",
             "defaults": {"wayleave_owner": "Customer", "high_risk_sites": "None identified", "access_notice_days": "5 business days"}},
            {"key": "equipment_setup", "required": True, "clause": "Clause 5",
             "question": "**Equipment:**\n  A) Supplier retains ownership *(standard)*\n  B) Customer owns after payment\n\nNTP free of charge? Removal 60 days?\n\nType **'A, defaults'** to accept standard terms.",
             "hint": "e.g. 'A, defaults'",
             "defaults": {"equipment_ownership": "Supplier retains", "ntp_arrangement": "Free of charge in MMR", "equipment_removal_days": "60"}},
        ],
    },
    "phase_3": {
        "title": "Commercials & Pricing",
        "description": "Protecting margins over a 5-15 year term.",
        "clauses": ["Clauses 9-11 (Charges, Payment, Duration)"],
        "fields": [
            {"key": "pricing_structure", "required": True, "clause": "Clauses 9-11",
             "question": "**Financial terms:**\n\n1. **IRU charge** (upfront): £?\n2. **O&M charge** (annual maintenance): £?/year\n3. **Contract term** (lock-in): months?\n\nAll GBP exclusive of VAT.",
             "hint": "e.g. '£50,000 IRU, £2,400/year O&M, 36 months'"},
            {"key": "commercial_protections", "required": True, "clause": "Clause 9.2 / 10",
             "question": "**Inflation & payment:**\n\n  A) RPI indexation *(standard UK telecoms)*\n  B) CPI\n  C) Fixed 3%\n  D) No increase *(risky 10+ years)*\n\nPayment: 30 days. Third-party cost pass-through: yes.\n\nType **'A, defaults'** for recommended settings.",
             "hint": "e.g. 'A, defaults'",
             "risk_logic": "No indexation on long term → margin erosion warning",
             "defaults": {"indexation_model": "RPI", "payment_terms_days": "30", "late_payment_rate": "Statutory", "third_party_passthrough": "Enabled"}},
        ],
    },
    "phase_4": {
        "title": "Liability & Termination",
        "description": "Setting your maximum legal and financial exposure.",
        "clauses": ["Clauses 12-14 (Termination, Force Majeure, Liability)"],
        "fields": [
            {"key": "liability_caps", "required": True, "clause": "Clause 14",
             "question": "**Liability limits:**\n\n- General cap: £50,000 *(default)*\n- Order-specific: 100% of annual fees *(default)*\n- Property damage: £1M/£5M *(default)*\n- Consequential loss: **always excluded**\n\nType **'defaults'** or specify changes.",
             "hint": "Type 'defaults' or e.g. '£100k general, rest defaults'",
             "risk_logic": "Cap >10x annual revenue → disproportionate risk",
             "defaults": {"general_liability_cap": "50000", "order_liability_model": "100% of annual fees", "property_damage_cap": "£1M/£5M"}},
            {"key": "termination_rules", "required": True, "clause": "Clauses 12-13",
             "question": "**Termination & exit:**\n\n- Early exit fee: 100% of remaining fees *(default)*\n- Breach cure: 30 days *(default)*\n- Force majeure exit: 180 days *(default)*\n\nType **'defaults'** or specify changes.",
             "hint": "Type 'defaults' or specify changes",
             "defaults": {"early_termination_fee": "100% of remaining fees", "breach_cure_days": "30", "force_majeure_termination_days": "180"}},
        ],
    },
    "phase_5": {
        "title": "Technical SLAs",
        "description": "Repair targets for physical fibre restoration.",
        "clauses": ["Schedule 2 (SLAs, Credits, Escalation)"],
        "fields": [
            {"key": "sla_structure", "required": True, "clause": "Schedule 2",
             "question": "**Service & repair:**\n\n  A) Build Only\n  B) Build + Warranty 12-24 months *(most common)*\n  C) Build + Ongoing SLA Maintenance\n\nRepair time: 12 hours standard. SLA exclusions: yes.\n\nType **'B, defaults'** for standard terms.",
             "hint": "e.g. 'B, defaults' or 'C, 8 hours, yes'",
             "risk_logic": "<12hr repair on long routes may be infeasible",
             "defaults": {"service_model": "Build + Warranty", "tttr_standard_hours": "12", "sla_exclusions": "Standard exclusions"}},
            {"key": "sla_penalties", "required": True, "clause": "Schedule 2 Sec 5",
             "question": "**Credits & penalties:**\n\n- Credit cap: 50% of annual O&M *(default)*\n- Chronic outage: 3 failures in 4 weeks *(default)*\n- Customer first-line testing: yes *(protects you)*\n\nType **'defaults'** to accept all.",
             "hint": "Type 'defaults' or specify changes",
             "defaults": {"service_credit_cap": "50", "chronic_outage_threshold": "3 in 4 weeks", "first_line_testing": "Yes", "noc_contact": "[TBC]"}},
        ],
    },
}

def get_phase(k): return PHASES.get(k, {})
def get_all_phase_keys(): return list(PHASES.keys())
def get_phase_fields(k): return PHASES.get(k, {}).get("fields", [])
def get_total_field_count(): return sum(len(p["fields"]) for p in PHASES.values())