"""
Dark Fibre Engine — 32-Question Wizard Flow
One question per field. 8 phases covering the full dark fibre framework agreement.
"""

PHASES = {

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PHASE 1 — PROVIDER DETAILS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "phase_1": {
        "title": "Provider Details",
        "description": "Your company information as the Provider.",
        "clauses": ["Cover Page", "Clause 19"],
        "fields": [
            {
                "key": "provider_name",
                "question": "What is your **full legal company name** as the Provider?",
                "hint": "e.g. 'PMS Fibre Ltd'",
                "required": True,
                "clause": "Cover Page",
            },
            {
                "key": "provider_address",
                "question": "What is the Provider's **registered address**?",
                "hint": "e.g. '123 Fibre Lane, London EC1A 1BB'",
                "required": True,
                "clause": "Cover Page",
            },
            {
                "key": "provider_company_no",
                "question": "What is the Provider's **company registration number**?",
                "hint": "e.g. '12345678'",
                "required": True,
                "clause": "Cover Page",
            },
            {
                "key": "provider_notice_email",
                "question": "What email address should the Customer send **formal legal notices** to you? *(Clause 19)*",
                "hint": "e.g. 'legal@pmsfibre.co.uk'",
                "required": True,
                "clause": "Clause 19",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PHASE 2 — CUSTOMER DETAILS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "phase_2": {
        "title": "Customer Details",
        "description": "The Customer's legal entity information.",
        "clauses": ["Cover Page", "Clause 19"],
        "fields": [
            {
                "key": "customer_name",
                "question": "What is the Customer's **full legal company name**? Include entity type (Ltd / PLC / LLP).",
                "hint": "e.g. 'Sky Networks Ltd'",
                "required": True,
                "clause": "Cover Page",
            },
            {
                "key": "customer_address",
                "question": "What is the Customer's **registered address**?",
                "hint": "e.g. '456 Network Road, Manchester M1 2AB'",
                "required": True,
                "clause": "Cover Page",
            },
            {
                "key": "customer_company_no",
                "question": "What is the Customer's **company registration number**?",
                "hint": "e.g. '87654321'",
                "required": True,
                "clause": "Cover Page",
            },
            {
                "key": "customer_notice_email",
                "question": "What email address should you send **formal legal notices** to the Customer? *(Clause 19)*",
                "hint": "e.g. 'procurement@skynetworks.co.uk'",
                "required": True,
                "clause": "Clause 19",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PHASE 3 — AGREEMENT TERMS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "phase_3": {
        "title": "Agreement Terms",
        "description": "Effective date, law, and dispute resolution.",
        "clauses": ["Cover Page", "Clause 20"],
        "fields": [
            {
                "key": "effective_date",
                "question": "What is the **effective date** of this Agreement?\n\nMost use **'Date of last signature'** for flexibility.",
                "hint": "Type 'last signature' or a specific date e.g. '01 April 2026'",
                "required": True,
                "clause": "Cover Page",
                "default": "Date of last signature",
            },
            {
                "key": "governing_law",
                "question": "Which **governing law** applies to this Agreement?\n\nStandard for UK dark fibre is **English Law**.",
                "hint": "e.g. 'English Law' or 'Scots Law'",
                "required": True,
                "clause": "Clause 20",
                "defaults": {"governing_law": "English Law, Courts of England and Wales"},
            },
            {
                "key": "dispute_resolution",
                "question": "How should **disputes** be resolved?\n\nStandard: Expert Determination first, then Courts of England and Wales.",
                "hint": "Type 'defaults' or specify e.g. 'Mediation then arbitration'",
                "required": True,
                "clause": "Clause 20",
                "defaults": {"dispute_resolution": "Expert Determination, then Courts of England and Wales"},
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PHASE 4 — SERVICES & ROUTE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "phase_4": {
        "title": "Services & Route",
        "description": "What fibre is being provided and where.",
        "clauses": ["Clause 2", "Schedule 1 (Route)"],
        "fields": [
            {
                "key": "fibre_route",
                "question": "Describe the **dark fibre route** — from where to where?\n\nInclude the A-end and B-end locations.",
                "hint": "e.g. 'From Telehouse North, London E14 to 123 Business Park, Manchester M1'",
                "required": True,
                "clause": "Clause 2",
            },
            {
                "key": "fibre_specification",
                "question": "What is the **fibre specification**? Include type and number of cores.",
                "hint": "e.g. 'G.652D single-mode, 24 cores'",
                "required": True,
                "clause": "Clause 2",
                "defaults": {"fibre_specification": "G.652D single-mode dark fibre"},
            },
            {
                "key": "rfs_date",
                "question": "What is the target **Ready for Service (RFS)** date — when should the fibre be live?",
                "hint": "e.g. '30 June 2026' or '90 days from Order date'",
                "required": True,
                "clause": "Clause 4",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PHASE 5 — WAYLEAVE & ACCESS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "phase_5": {
        "title": "Wayleave & Access",
        "description": "The #1 cause of dark fibre project failure.",
        "clauses": ["Clauses 3-5", "Schedule 1 (External Events)"],
        "fields": [
            {
                "key": "wayleave_responsibility",
                "question": "Who is responsible for **obtaining wayleaves** (landowner permissions for the fibre route)?\n\n  A) Customer — lowest risk for you\n  B) Shared — you assist, customer signs\n  C) Provider — highest risk, you carry delays",
                "hint": "Type A, B, or C",
                "required": True,
                "clause": "Clause 3",
                "risk_logic": "If Provider (C), add Long-Stop Date + Programme Relief to protect against delays.",
                "defaults": {"wayleave_owner": "Customer"},
            },
            {
                "key": "high_risk_sites",
                "question": "Are there any **high-risk wayleave sites** on this route?\n\nThese include: railways, highways, MDUs (multi-tenant buildings), or listed structures.",
                "hint": "e.g. 'Railway crossing at Manchester Piccadilly' or 'None'",
                "required": True,
                "clause": "Clause 3",
                "risk_logic": "High-risk sites cause 6-9 month permit delays. Programme Relief should be reinforced.",
                "defaults": {"high_risk_sites": "None identified"},
            },
            {
                "key": "access_notice_days",
                "question": "How many **business days' notice** is required before accessing a site?",
                "hint": "e.g. '5 business days' (standard)",
                "required": True,
                "clause": "Clause 3",
                "defaults": {"access_notice_days": "5 business days"},
            },
            {
                "key": "equipment_ownership",
                "question": "Who **owns the fibre equipment** (cabinets, NTPs, termination equipment) after installation?\n\n  A) Supplier retains ownership — standard for leased dark fibre\n  B) Customer owns after full payment",
                "hint": "Type A or B",
                "required": True,
                "clause": "Clause 5",
                "defaults": {
                    "equipment_ownership": "Supplier retains ownership",
                    "ntp_arrangement": "Free of charge in Meet-Me-Room",
                    "equipment_removal_days": "60",
                },
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PHASE 6 — COMMERCIALS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "phase_6": {
        "title": "Commercials & Pricing",
        "description": "Protecting your margins over a 5-15 year term.",
        "clauses": ["Clauses 9-11 (Charges, Payment, Duration)"],
        "fields": [
            {
                "key": "iru_charge",
                "question": "What is the **upfront IRU charge** (Indefeasible Right of Use — the one-time capital payment)?\n\nAll charges GBP exclusive of VAT.",
                "hint": "e.g. '£50,000'",
                "required": True,
                "clause": "Clause 9",
            },
            {
                "key": "om_charge",
                "question": "What is the **annual O&M charge** (Operations & Maintenance — recurring yearly fee)?",
                "hint": "e.g. '£2,400 per year'",
                "required": True,
                "clause": "Clause 9",
            },
            {
                "key": "contract_term_months",
                "question": "What is the **minimum contract term** (lock-in period) in months?",
                "hint": "e.g. '36' (3 years) or '60' (5 years)",
                "required": True,
                "clause": "Clause 11",
                "risk_logic": "Terms over 60 months with no indexation = margin erosion risk.",
            },
            {
                "key": "indexation_model",
                "question": "Which **annual price indexation** model applies to the O&M charge?\n\n  A) RPI — standard UK telecoms\n  B) CPI — public sector preferred\n  C) Fixed 3% increase\n  D) No increase — risky on long terms",
                "hint": "Type A, B, C, or D",
                "required": True,
                "clause": "Clause 9.2",
                "risk_logic": "No indexation (D) on long contracts causes margin erosion. Strongly recommend A or B.",
                "defaults": {
                    "indexation_model": "RPI (annual increase)",
                    "late_payment_rate": "Statutory interest (8% over base)",
                    "third_party_passthrough": "Enabled — pass-through to customer",
                },
            },
            {
                "key": "payment_terms_days",
                "question": "What are the **payment terms** — how many days does the Customer have to pay an invoice?",
                "hint": "e.g. '30 days' (standard)",
                "required": True,
                "clause": "Clause 10",
                "defaults": {"payment_terms_days": "30"},
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PHASE 7 — LIABILITY & TERMINATION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "phase_7": {
        "title": "Liability & Termination",
        "description": "Your maximum legal and financial exposure.",
        "clauses": ["Clauses 12-14 (Termination, Force Majeure, Liability)"],
        "fields": [
            {
                "key": "general_liability_cap",
                "question": "What is the **general liability cap** (for claims not related to a specific Order)?\n\nNote: consequential loss (lost profit/revenue/data) is always excluded.",
                "hint": "e.g. '£50,000' (standard)",
                "required": True,
                "clause": "Clause 14",
                "risk_logic": "Cap >10x annual revenue = disproportionate risk for your business.",
                "defaults": {
                    "general_liability_cap": "£50,000",
                    "property_damage_cap": "£1,000,000 per claim / £5,000,000 aggregate",
                },
            },
            {
                "key": "order_liability_cap",
                "question": "What is the **order-specific liability cap** — maximum liability for claims arising from a single Order?",
                "hint": "e.g. '100% of annual fees for that route' (standard)",
                "required": True,
                "clause": "Clause 14",
                "defaults": {"order_liability_model": "100% of annual fees for that Order"},
            },
            {
                "key": "early_termination_fee",
                "question": "If the Customer exits **early**, what fee do they pay?\n\nThis protects your build cost recovery.",
                "hint": "e.g. '100% of remaining minimum period fees' (standard)",
                "required": True,
                "clause": "Clause 12",
                "defaults": {"early_termination_fee": "100% of remaining minimum period fees"},
            },
            {
                "key": "breach_cure_days",
                "question": "How many days does a party have to **cure a breach** before the other can terminate?",
                "hint": "e.g. '30 days' (standard)",
                "required": True,
                "clause": "Clause 12",
                "defaults": {"breach_cure_days": "30"},
            },
            {
                "key": "force_majeure_days",
                "question": "After how many days of **force majeure** can either party terminate the Agreement?",
                "hint": "e.g. '180 days' (standard)",
                "required": True,
                "clause": "Clause 13",
                "defaults": {"force_majeure_termination_days": "180"},
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PHASE 8 — TECHNICAL SLAs
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "phase_8": {
        "title": "Technical SLAs",
        "description": "Repair targets, credits, and escalation.",
        "clauses": ["Schedule 2 (SLAs, Credits, Escalation)"],
        "fields": [
            {
                "key": "service_model",
                "question": "Which **service model** applies after the fibre is live?\n\n  A) Build Only — you install, customer maintains\n  B) Build + Warranty 12-24 months — most common\n  C) Build + Ongoing SLA Maintenance — full managed service",
                "hint": "Type A, B, or C",
                "required": True,
                "clause": "Schedule 2",
                "defaults": {"service_model": "Build + 12-month Warranty"},
            },
            {
                "key": "tttr_hours",
                "question": "What is the **Target Time to Repair (TTTR)** for physical fibre faults?\n\nThis is physical restoration time — not software uptime.",
                "hint": "e.g. '12 hours' (standard)",
                "required": True,
                "clause": "Schedule 2",
                "risk_logic": "TTTR under 12 hours on long routes may be physically impossible. Add permit extension clause if <12hr.",
                "defaults": {
                    "tttr_standard_hours": "12",
                    "sla_exclusions": "Standard: third-party strikes, power failures, extreme weather, landowner access refusal",
                },
            },
            {
                "key": "service_credit_cap",
                "question": "What is the **maximum service credit** a Customer can claim in a year?\n\nThis caps your credit exposure.",
                "hint": "e.g. '50% of annual O&M' (standard)",
                "required": True,
                "clause": "Schedule 2 Sec 5",
                "defaults": {
                    "service_credit_cap": "50% of annual O&M",
                    "chronic_outage_threshold": "3 failures in 4 weeks",
                    "first_line_testing": "Yes — customer must test before raising ticket",
                },
            },
            {
                "key": "noc_contact",
                "question": "What is the **NOC (Network Operations Centre)** contact for fault reporting — email and/or phone?",
                "hint": "e.g. 'noc@pmsfibre.co.uk / 0800 123 456'",
                "required": True,
                "clause": "Schedule 2",
                "defaults": {"noc_contact": "[To be confirmed]"},
            },
        ],
    },
}


def get_phase(k): return PHASES.get(k, {})
def get_all_phase_keys(): return list(PHASES.keys())
def get_phase_fields(k): return PHASES.get(k, {}).get("fields", [])
def get_total_field_count(): return sum(len(p["fields"]) for p in PHASES.values())
