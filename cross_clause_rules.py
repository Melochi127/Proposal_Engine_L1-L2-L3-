"""
Telecom Proposal Engine - Cross-Clause Risk Logic
===================================================
Intelligence from 10 Dark Fibre reference documents, baked into code.
Checked after each L3 user answer to flag risks and dependencies.
"""

STANDARD_DEFAULTS = {
    "wayleave_owner": "Customer",
    "high_risk_sites": "None identified",
    "access_notice_days": "5 business days",
    "equipment_ownership": "Supplier retains ownership",
    "ntp_arrangement": "Free of charge in Meet-Me-Room",
    "equipment_removal_days": "60",
    "currency_vat": "GBP exclusive of VAT",
    "indexation_model": "RPI (annual increase)",
    "payment_terms_days": "30",
    "late_payment_rate": "Statutory interest (8% over base)",
    "third_party_passthrough": "Enabled — pass-through to customer",
    "general_liability_cap": "£50,000",
    "order_liability_model": "100% of annual fees for that route",
    "property_damage_cap": "£1M per claim / £5M aggregate",
    "early_termination_fee": "100% of remaining fees for minimum period",
    "breach_cure_days": "30",
    "force_majeure_termination_days": "180",
    "service_model": "Build + 12-month Warranty",
    "tttr_standard_hours": "12",
    "chronic_outage_threshold": "3 failures in 4 weeks",
    "service_credit_cap": "50% of annual O&M",
    "first_line_testing": "Yes — customer tests before raising ticket",
    "sla_exclusions": "Standard: third-party strikes, power failures, extreme weather, landowner access",
    "noc_contact": "[To be confirmed]",
}


def check_risks(slots: dict) -> list:
    """Check user answers against cross-clause rules. Return list of warnings."""
    warnings = []

    wayleave = slots.get("wayleave_and_access", "").lower()
    if wayleave.strip() in ("c", "c)", "provider") or "provider fully" in wayleave:
        warnings.append({
            "id": "R01",
            "severity": "High",
            "msg": "⚠️ Provider-led wayleaves = highest delivery risk. External Event relief and Long-Stop Date will be added automatically.",
        })

    if any(kw in wayleave for kw in ["railway", "highway", "mdu", "multi-tenant"]):
        warnings.append({
            "id": "R02",
            "severity": "High",
            "msg": "⚠️ High-risk sites detected (railway/highway/MDU). Programme Relief reinforced. Expect 6-9 month permit delays.",
        })

    protections = slots.get("commercial_protections", "").lower()
    pricing = slots.get("pricing_structure", "").lower()
    if ("no increase" in protections or protections.strip() == "d") and any(
        t in pricing for t in ["60", "84", "96", "120", "180"]
    ):
        warnings.append({
            "id": "R03",
            "severity": "Critical",
            "msg": "🚨 CRITICAL: No indexation on a long-term contract. Your O&M costs will double while revenue stays flat. Strongly recommend RPI/CPI.",
        })

    penalties = slots.get("sla_penalties", "").lower()
    if "100%" in penalties and "credit" in penalties:
        warnings.append({
            "id": "R09",
            "severity": "Medium",
            "msg": "⚠️ 100% service credits at risk means customer pays nothing if service is poor. Standard protection is 50%.",
        })

    liability = slots.get("liability_caps", "").lower()
    if "no fee" in liability or "zero" in liability:
        warnings.append({
            "id": "R10",
            "severity": "High",
            "msg": "⚠️ No early termination fee means customer can exit without covering your build costs.",
        })

    sla = slots.get("sla_structure", "").lower()
    if ("8" in sla or "6" in sla) and "hour" in sla:
        warnings.append({
            "id": "R08",
            "severity": "Medium",
            "msg": "⚠️ Aggressive repair target (<12 hours). Mobilising dig-teams for long routes may take 12+ hours. Consider adding a permit extension clause.",
        })

    return warnings