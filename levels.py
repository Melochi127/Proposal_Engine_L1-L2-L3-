"""
Telecom Proposal Engine - Level Definitions
=============================================
L1 (Quick)    — 5 fields, 2-3 min, concise proposal
L2 (Standard) — 10 fields, 5-7 min, full 9-section proposal
L3 (Dark Fibre) — 12 grouped screens across 5 phases, contract-grade framework agreement
"""

LEVELS = {

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # LEVEL 1 — QUICK PROPOSAL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "L1": {
        "name": "Quick Proposal",
        "icon": "⚡",
        "time": "2-3 minutes",
        "description": "Fast proposal with minimal input. AI drafts and formats.",
        "output_type": "Concise professional proposal (~800 words)",
        "subsectors": [
            "Fibre Broadband Installation",
            "Wireless Networks",
            "VoIP Solutions",
        ],
        "fields": [
            {
                "key": "client_name",
                "question": "Who is this proposal for?",
                "hint": "e.g. 'Sky Networks Ltd'",
                "required": True,
            },
            {
                "key": "service_description",
                "question": "What service are we proposing?",
                "hint": "e.g. 'Fibre Broadband Installation – 1Gbps business grade'",
                "required": True,
            },
            {
                "key": "prepared_by",
                "question": "Who is preparing this proposal?",
                "hint": "e.g. 'Freedom Fibre Ltd'",
                "required": True,
            },
            {
                "key": "total_cost",
                "question": "What's the total cost?",
                "hint": "e.g. '£6,750 excluding VAT'",
                "required": True,
            },
            {
                "key": "timeline",
                "question": "Delivery timeframe?",
                "hint": "e.g. '15 September to 30 September 2025'",
                "required": True,
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # LEVEL 2 — STANDARD PROPOSAL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "L2": {
        "name": "Standard Proposal",
        "icon": "📋",
        "time": "5-7 minutes",
        "description": "Full proposal with all sections. AI guides you step-by-step.",
        "output_type": "Detailed 9-section proposal (1500-2000 words)",
        "subsectors": [
            "Fibre Broadband Installation",
            "Wireless Networks",
            "VoIP Solutions",
            "Dark Fibre Leasing",
        ],
        "fields": [
            {
                "key": "proposal_title",
                "question": "Do you have a title for this proposal, or should I suggest one?",
                "hint": "e.g. '1Gbps Business-grade Fibre Broadband Service Proposal'",
                "required": True,
            },
            {
                "key": "client_name",
                "question": "Who is the proposal for?",
                "hint": "e.g. 'Sky Networks Ltd'",
                "required": True,
            },
            {
                "key": "service_description",
                "question": "What service are we proposing?",
                "hint": "e.g. 'Fibre Broadband Installation – 1Gbps business grade'",
                "required": True,
            },
            {
                "key": "prepared_by",
                "question": "Who should we list as the proposal preparer?",
                "hint": "e.g. 'Freedom Fibre Ltd'",
                "required": True,
            },
            {
                "key": "validity_period",
                "question": "How long should the proposal be valid?",
                "hint": "e.g. 'Until 30 November 2025' or '30 days'",
                "required": True,
            },
            {
                "key": "exec_summary_tone",
                "question": "Let's draft the executive summary. Would you like it **persuasive**, **warm**, **factual**, or **urgent**?",
                "hint": "Pick a tone or write your own summary",
                "required": True,
            },
            {
                "key": "scope_of_work",
                "question": "Here's a default scope:\n• Pre-installation survey\n• Fibre trenching and cabling\n• Equipment installation\n• Testing and commissioning\n• 3-month post-deployment support\n\nAnything to add or remove? Type **'keep'** for defaults.",
                "hint": "Type 'keep' for defaults or describe changes",
                "required": True,
            },
            {
                "key": "total_cost",
                "question": "What's the total cost?",
                "hint": "e.g. '£6,750 excluding VAT'",
                "required": True,
            },
            {
                "key": "timeline",
                "question": "Start date and completion date?",
                "hint": "e.g. '15 September to 30 September 2025'",
                "required": True,
            },
            {
                "key": "contact_details",
                "question": "Add your contact details? (Name, phone, email) — or type **'skip'**.",
                "hint": "e.g. 'John Smith, +44 20 7123 4567, john@freedomfibre.co.uk'",
                "required": False,
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # LEVEL 3 — DARK FIBRE FRAMEWORK AGREEMENT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "L3": {
        "name": "Dark Fibre Framework Agreement",
        "icon": "🔌",
        "time": "Under 2 minutes with defaults",
        "description": "Contract-grade 20-clause framework agreement with cross-clause risk logic.",
        "output_type": "Legal-grade Framework Agreement (3000-4000 words) + Executive Risk Summary",
        "subsectors": ["Dark Fibre"],
        "phases": {
            "phase_1": {
                "title": "Entity & Admin",
                "description": "Who are the parties to this agreement?",
                "clauses": ["Cover Page", "Clause 19 (Notices)", "Signatures"],
                "fields": [
                    {
                        "key": "provider_details",
                        "question": "**Your details** as Provider — company name, registered address, and company number (all in one go).",
                        "hint": "e.g. 'PMS Fibre Ltd, 123 Fibre Lane London EC1A 1BB, No. 12345678'",
                        "required": True,
                        "clause": "Cover Page",
                    },
                    {
                        "key": "customer_details",
                        "question": "Now the **Customer** — full legal name, registered address, and company number.\n\n*Use the exact entity name (Ltd/PLC/LLP), not a trading name.*",
                        "hint": "e.g. 'Sky Networks Ltd, 456 Network Road Manchester M1 2AB, No. 87654321'",
                        "required": True,
                        "clause": "Cover Page",
                    },
                    {
                        "key": "effective_date",
                        "question": "Start date for this Framework Agreement?\n\nMost people use **'Date of last signature'** for flexibility.",
                        "hint": "Type 'last signature' or a specific date",
                        "required": True,
                        "clause": "Cover Page",
                        "default": "Date of last signature",
                    },
                    {
                        "key": "notice_emails",
                        "question": "Notice emails for both parties? *(For formal legal communications under Clause 19)*",
                        "hint": "e.g. 'legal@provider.com / procurement@customer.com'",
                        "required": True,
                        "clause": "Clause 19",
                    },
                ],
            },
            "phase_2": {
                "title": "Wayleave & Access",
                "description": "Wayleaves are the #1 cause of project failure in Dark Fibre.",
                "clauses": ["Clauses 3-5", "Schedule 1 (External Events)"],
                "fields": [
                    {
                        "key": "wayleave_and_access",
                        "question": "Three decisions about **site access**:\n\n**1. Wayleave responsibility:**\n  A) Customer responsible *(lowest risk for you)*\n  B) Shared — you assist, customer signs\n  C) Provider fully responsible *(highest risk)*\n\n**2. High-risk sites?** (Railways, highways, MDUs) — or 'none'\n\n**3. Access notice period?** Default 5 business days.\n\nType all three, or just **'A'** for all defaults.",
                        "hint": "e.g. 'A, none, 5 days' or just 'A'",
                        "required": True,
                        "clause": "Clauses 3-5",
                        "risk_logic": "If Provider responsible, add Long-Stop Date + Programme Relief.",
                        "defaults": {
                            "wayleave_owner": "Customer",
                            "high_risk_sites": "None identified",
                            "access_notice_days": "5 business days",
                        },
                    },
                    {
                        "key": "equipment_setup",
                        "question": "**Equipment & termination:**\n\n  A) Supplier retains ownership *(standard for leased dark fibre)*\n  B) Customer owns after payment\n\nNTP free of charge? Equipment removal 60 days?\n\nType **'A, defaults'** to accept standard terms.",
                        "hint": "e.g. 'A, defaults'",
                        "required": True,
                        "clause": "Clause 5",
                        "defaults": {
                            "equipment_ownership": "Supplier retains",
                            "ntp_arrangement": "Free of charge in MMR",
                            "equipment_removal_days": "60",
                        },
                    },
                ],
            },
            "phase_3": {
                "title": "Commercials & Pricing",
                "description": "Protecting your margins over a 5-15 year term.",
                "clauses": ["Clauses 9-11 (Charges, Payment, Duration)"],
                "fields": [
                    {
                        "key": "pricing_structure",
                        "question": "**Financial terms:**\n\n1. **IRU charge** (upfront): £?\n2. **O&M charge** (annual maintenance): £?/year\n3. **Contract term** (lock-in): months?\n\nAll charges GBP exclusive of VAT.",
                        "hint": "e.g. '£50,000 IRU, £2,400/year O&M, 36 months'",
                        "required": True,
                        "clause": "Clauses 9-11",
                    },
                    {
                        "key": "commercial_protections",
                        "question": "**Inflation & payment protections:**\n\n  A) RPI indexation *(standard UK telecoms)*\n  B) CPI *(public sector)*\n  C) Fixed 3% increase\n  D) No increase *(risky for 10+ year terms)*\n\nPayment: 30 days. Third-party cost pass-through: yes.\n\nType **'A, defaults'** for recommended settings.",
                        "hint": "e.g. 'A, defaults'",
                        "required": True,
                        "clause": "Clause 9.2 / 10",
                        "risk_logic": "No indexation on long term = margin erosion warning.",
                        "defaults": {
                            "indexation_model": "RPI (annual increase)",
                            "payment_terms_days": "30",
                            "late_payment_rate": "Statutory (8% over base)",
                            "third_party_passthrough": "Enabled",
                        },
                    },
                ],
            },
            "phase_4": {
                "title": "Liability & Termination",
                "description": "Setting your maximum legal and financial exposure.",
                "clauses": ["Clauses 12-14 (Termination, Force Majeure, Liability)"],
                "fields": [
                    {
                        "key": "liability_caps",
                        "question": "**Liability limits:**\n\n- General (non-order) cap: **£50,000** (default)\n- Order-specific: **100% of annual fees** (default)\n- Property damage: **£1M per claim / £5M aggregate** (default)\n- Consequential loss: **always excluded**\n\nType **'defaults'** or specify changes.",
                        "hint": "Type 'defaults' or e.g. '£100k general, rest defaults'",
                        "required": True,
                        "clause": "Clause 14",
                        "risk_logic": "If cap >10x annual revenue, flag disproportionate risk.",
                        "defaults": {
                            "general_liability_cap": "£50,000",
                            "order_liability_model": "100% of annual fees",
                            "property_damage_cap": "£1M/£5M",
                        },
                    },
                    {
                        "key": "termination_rules",
                        "question": "**Termination & exit:**\n\n- Early termination fee: **100% of remaining fees** (default)\n- Breach cure period: **30 days** (default)\n- Force majeure termination: **180 days** (default)\n\nType **'defaults'** or specify changes.",
                        "hint": "Type 'defaults' or specify changes",
                        "required": True,
                        "clause": "Clauses 12-13",
                        "defaults": {
                            "early_termination_fee": "100% of remaining fees",
                            "breach_cure_days": "30",
                            "force_majeure_termination_days": "180",
                        },
                    },
                ],
            },
            "phase_5": {
                "title": "Technical SLAs",
                "description": "Repair targets for physical fibre restoration.",
                "clauses": ["Schedule 2 (SLAs, Credits, Escalation)"],
                "fields": [
                    {
                        "key": "sla_structure",
                        "question": "**Service & repair model:**\n\n  A) Build Only — you install, customer maintains\n  B) Build + Warranty 12-24 months *(most common)*\n  C) Build + Ongoing SLA Maintenance\n\nRepair time: **12 hours** standard. SLA exclusions: **yes**.\n\nType **'B, defaults'** for standard terms.",
                        "hint": "e.g. 'B, defaults' or 'C, 8 hours, yes'",
                        "required": True,
                        "clause": "Schedule 2",
                        "risk_logic": "<12hr repair on long routes may be infeasible.",
                        "defaults": {
                            "service_model": "Build + 12-month Warranty",
                            "tttr_standard_hours": "12",
                            "sla_exclusions": "Standard (third-party strikes, power failures, extreme weather)",
                        },
                    },
                    {
                        "key": "sla_penalties",
                        "question": "**Credits & penalties:**\n\n- Service credit cap: **50% of annual O&M** (default)\n- Chronic outage trigger: **3 failures in 4 weeks** (default)\n- Customer first-line testing: **yes** (protects you from false call-outs)\n\nType **'defaults'** to accept all standard terms.",
                        "hint": "Type 'defaults' or specify changes",
                        "required": True,
                        "clause": "Schedule 2 Sec 5",
                        "defaults": {
                            "service_credit_cap": "50% of annual O&M",
                            "chronic_outage_threshold": "3 failures in 4 weeks",
                            "first_line_testing": "Yes",
                            "noc_contact": "[To be confirmed]",
                        },
                    },
                ],
            },
        },
    },
}


# ── Helper Functions ──────────────────────────
def get_level(key):
    return LEVELS.get(key, {})

def get_level_names():
    return {k: v["name"] for k, v in LEVELS.items()}

def get_l1l2_fields(level_key):
    return LEVELS.get(level_key, {}).get("fields", [])

def get_l3_phases():
    return LEVELS["L3"]["phases"]

def get_l3_phase(phase_key):
    return LEVELS["L3"]["phases"].get(phase_key, {})

def get_l3_phase_fields(phase_key):
    return LEVELS["L3"]["phases"].get(phase_key, {}).get("fields", [])

def get_l3_phase_keys():
    return list(LEVELS["L3"]["phases"].keys())

def get_total_l3_fields():
    return sum(len(p["fields"]) for p in LEVELS["L3"]["phases"].values())
