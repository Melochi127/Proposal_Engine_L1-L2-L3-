"""
Telecom Proposal Engine - Proposal JSON Storage Management
============================================================

Handles persistence of completed proposals to the file system as JSON files.
Provides CRUD operations: save, load, list, and delete proposals.

Each proposal is stored as a timestamped JSON file containing:
    - Session metadata (ID, level, client, subsector)
    - All user answers (slots) from the wizard
    - Generated proposal text output
    - Risk summary and cross-clause warnings
    - Save timestamp for sorting

Default storage location: ./proposals/ directory

Module Functions:
    - save_proposal(): Persist completed session to JSON file
    - list_proposals(): Get summary of all saved proposals
    - load_proposal(): Load full proposal record by filename
    - delete_proposal(): Remove a proposal file
    
Dependencies:
    - json: For JSON serialization/deserialization
    - os: File system operations
    - datetime: For timestamp generation
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


PROPOSALS_DIR = os.path.join(os.path.dirname(__file__), "proposals")


def _ensure_dir() -> None:
    """Ensure proposals directory exists, creating if necessary."""
    os.makedirs(PROPOSALS_DIR, exist_ok=True)


def save_proposal(session, output: str, risk: str = "") -> str:
    """
    Save a completed proposal session to a JSON file.
    
    Combines session state, generated output, and risk analysis into a single
    JSON record file with human-readable naming based on client info.
    
    Args:
        session: Session object containing all proposal data
        output (str): Complete generated proposal text
        risk (str, optional): Risk summary or analysis text. Default: ""
        
    Returns:
        str: Absolute file path to the saved proposal JSON file
        
    File Naming:
        Uses session_id format (e.g., "df_20260324_114640.json")
        allowing chronological sorting and preventing duplicates
        
    File Contents:
        {
            "id": "df_YYYYMMDDhhmmss",
            "saved_at": "YYYY-MM-DD HH:MM",
            "level": "L1|L2|L3",
            "label": "Quick|Standard|Dark Fibre",
            "subsector": "use case",
            "client": "extracted client name",
            "slots": {all user answers},
            "output": generated proposal text,
            "risk": risk analysis,
            "risk_warnings": [list of cross-clause warnings]
        }
        
    Examples:
        >>> from agent_state import Session
        >>> s = Session(level="L1", session_id="df_20260324_114640")
        >>> path = save_proposal(s, "Proposal text here", "No risks")
        >>> os.path.exists(path)
        True
        
    Error Handling:
        Creates proposals directory if missing. Silently handles encoding
        via UTF-8 with ensure_ascii=False for international characters.
    """
    _ensure_dir()

    # Extract human-readable client name from slots
    client = (
        session.slots.get("client_name")
        or session.slots.get("provider_details", "")[:30]
        or "Unknown"
    )
    
    # Map level codes to readable labels
    level_labels = {"L1": "Quick", "L2": "Standard", "L3": "Dark Fibre"}
    label = level_labels.get(session.level, session.level)

    # Build complete proposal record
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

    # Save to file using session ID as filename
    filename = f"{session.session_id}.json"
    path = os.path.join(PROPOSALS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    return path


def list_proposals() -> List[Dict]:
    """
    Retrieve summary metadata for all saved proposals, sorted by newest first.
    
    For performance, only returns summary fields (not full proposal text).
    Use load_proposal() to get complete proposal details.
    
    Returns:
        List[Dict]: List of proposal summaries sorted by save date (newest first)
        
    Summary Fields per Proposal:
        - id: Session ID
        - saved_at: Save timestamp
        - level: L1/L2/L3
        - label: "Quick"|"Standard"|"Dark Fibre"
        - subsector: Use case or subsector
        - client: Client name extracted from slots
        - filename: JSON filename
        
    Examples:
        >>> proposals = list_proposals()
        >>> len(proposals) >= 0
        True
        >>> if proposals:
        ...     proposals[0]["label"] in ["Quick", "Standard", "Dark Fibre"]
        ...     True
        
    Error Handling:
        Silently skips corrupted or unparseable JSON files. Returns empty list
        if proposals directory doesn't exist or is empty.
    """
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
        except (json.JSONDecodeError, IOError):
            # Skip corrupted files silently
            continue
            
    return sorted(results, key=lambda x: x["saved_at"], reverse=True)


def load_proposal(filename: str) -> Optional[Dict]:
    """
    Load a complete proposal record by filename.
    
    Args:
        filename (str): JSON filename (e.g., "df_20260324_114640.json")
        
    Returns:
        Optional[Dict]: Complete proposal record including output text,
                        or None if file doesn't exist or cannot be parsed
                        
    Examples:
        >>> proposal = load_proposal("df_20260324_114640.json")
        >>> if proposal:
        ...     print(proposal["output"][:50])
        
    Error Handling:
        Returns None if file not found or JSON parsing fails.
    """
    path = os.path.join(PROPOSALS_DIR, filename)
    if not os.path.exists(path):
        return None
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def delete_proposal(filename: str) -> bool:
    """
    Delete a proposal file from storage.
    
    Args:
        filename (str): JSON filename to delete (e.g., "df_20260324_114640.json")
        
    Returns:
        bool: True if file was deleted, False if file didn't exist
        
    Examples:
        >>> deleted = delete_proposal("df_20260324_114640.json")
        >>> deleted
        True  # or False if didn't exist
        
    Error Handling:
        Returns False silently if file doesn't exist or deletion fails.
    """
    path = os.path.join(PROPOSALS_DIR, filename)
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
    except (OSError, IOError):
        pass
    return False
