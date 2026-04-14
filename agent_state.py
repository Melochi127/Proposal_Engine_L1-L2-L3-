"""
Telecom Proposal Engine - Session State
"""
from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel, Field


class Session(BaseModel):
    """Tracks a single proposal/agreement session across all levels."""
    session_id: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    level: str = "L1"           # L1, L2, or L3
    subsector: str = ""
    current_phase: str = "phase_1"  # L3 only
    current_field_index: int = 0
    slots: Dict[str, str] = Field(default_factory=dict)
    clarify_counts: Dict[str, int] = Field(default_factory=dict)
    chat_history: List[Dict] = Field(default_factory=list)
    full_output: str = ""
    risk_summary: str = ""
    all_complete: bool = False
    risk_warnings: List[Dict] = Field(default_factory=list)

    def filled_count(self):
        return sum(1 for v in self.slots.values() if v and v.strip())

    def slots_summary(self):
        lines = []
        for k, v in self.slots.items():
            if v and v.strip():
                nice = k.replace("_", " ").title()
                lines.append(f"- {nice}: {v}")
        return "\n".join(lines) if lines else "(No data collected yet)"

    def add_chat(self, role, content):
        self.chat_history.append({
            "role": role,
            "content": content,
            "time": datetime.now().strftime("%H:%M"),
        })

    def set_slot(self, key, value):
        self.slots[key] = value