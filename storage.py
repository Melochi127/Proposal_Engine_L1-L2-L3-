"""
Telecom Proposal Engine - Proposal Storage
==========================================
Saves, loads, lists, and deletes proposals as JSON files in the proposals/ directory.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

PROPOSALS_DIR = os.path.join(os.path.dirname(__file__), "proposals")


def _ensure_dir():
    os.makedirs(PROPOSALS_DIR, exist_ok=True)


def save_proposal(session, output: str, risk: str = "") -> str:
    """Save a completed proposal. Returns the saved file path."""
    _ensure_dir()

    # Build a human-readable title from slots
    client = (
        session.slots.get("client_name")
        or session.slots.get("provider_details", "")[:30]
        or "Unknown"
    )
    level_labels = {"L1": "Quick", "L2": "Standard", "L3": "Dark Fibre"}
    label = level_labels.get(session.level, session.level)

    record = {
        "id": session.session_id,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "level": session.level,
        "label": label,
        "subsector": session.subsector,
        "client": client,
        "slots": session.slots,
        "output": output,
        "risk": risk,
        "risk_warnings": session.risk_warnings,
    }

    filename = f"{session.session_id}.json"
    path = os.path.join(PROPOSALS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    return path


def list_proposals() -> List[Dict]:
    """Return all saved proposals sorted by newest first (summary only)."""
    _ensure_dir()
    results = []
    for fname in os.listdir(PROPOSALS_DIR):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(PROPOSALS_DIR, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                rec = json.load(f)
            results.append({
                "id": rec.get("id", fname),
                "saved_at": rec.get("saved_at", ""),
                "level": rec.get("level", ""),
                "label": rec.get("label", ""),
                "subsector": rec.get("subsector", ""),
                "client": rec.get("client", ""),
                "filename": fname,
            })
        except Exception:
            continue
    return sorted(results, key=lambda x: x["saved_at"], reverse=True)


def load_proposal(filename: str) -> Optional[Dict]:
    """Load a full proposal record by filename."""
    path = os.path.join(PROPOSALS_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_proposal(filename: str) -> bool:
    """Delete a proposal file. Returns True if deleted."""
    path = os.path.join(PROPOSALS_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
