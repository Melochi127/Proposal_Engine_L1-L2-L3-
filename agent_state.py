"""
Telecom Proposal Engine - Session State Management
===================================================

This module defines the persistent session state model for tracking proposal generation
progress across all three proposal levels (L1 Quick, L2 Standard, L3 Dark Fibre).

Uses Pydantic for type-safe data validation and serialization.

Module Contents:
    - Session: Pydantic model for proposal session state persistence
    
Dependencies:
    - pydantic: For data validation and BaseModel
    - datetime: For timestamp generation
"""

from datetime import datetime
from typing import Dict, List, Any
from pydantic import BaseModel, Field


class Session(BaseModel):
    """
    Tracks a single proposal/agreement session across all levels (L1/L2/L3).
    
    Maintains state for the wizard flow including current progress, user answers,
    chat history, and identified risks. Uses Pydantic for validation.
    
    Attributes:
        session_id (str): Unique identifier for this session (format: df_YYYYMMDDHHmmss)
        created_at (str): ISO timestamp when session was created
        level (str): Proposal level - "L1" (Quick), "L2" (Standard), or "L3" (Dark Fibre)
        subsector (str): Telecom subsector or use case (e.g., "Core Network", "Access")
        current_phase (str): Current L3 phase being edited (e.g., "phase_1", "phase_5")
        current_field_index (int): Index of current field within phase
        slots (Dict[str, str]): Dictionary of all user answers (key: field_key, value: user_answer)
        clarify_counts (Dict[str, int]): Tracks clarification attempts per field (prevents over-asking)
        chat_history (List[Dict]): Chronological list of AI/user messages with timestamps
        full_output (str): Complete generated proposal text
        risk_summary (str): Aggregated commercial risk summary for display
        all_complete (bool): True when all fields are filled and proposal is ready
        risk_warnings (List[Dict]): Active cross-clause risk warnings flagged during entry
    
    Examples:
        >>> s = Session(level="L3", subsector="Core Network")
        >>> s.set_slot("company_name", "BT Wholesale")
        >>> s.filled_count()
        1
        >>> s.slots_summary()
        '- Company Name: BT Wholesale'
    """
    
    session_id: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    level: str = "L1"                    # L1, L2, or L3
    subsector: str = ""
    current_phase: str = "phase_1"       # L3 only; not used in L1/L2
    current_field_index: int = 0
    slots: Dict[str, str] = Field(default_factory=dict)
    clarify_counts: Dict[str, int] = Field(default_factory=dict)
    chat_history: List[Dict[str, Any]] = Field(default_factory=list)
    full_output: str = ""
    risk_summary: str = ""
    all_complete: bool = False
    risk_warnings: List[Dict[str, Any]] = Field(default_factory=list)

    def filled_count(self) -> int:
        """
        Count the number of non-empty user answers collected so far.
        
        Returns:
            int: Number of slots with non-empty values
        """
        return sum(1 for v in self.slots.values() if v and v.strip())

    def slots_summary(self) -> str:
        """
        Generate a readable summary of all filled slots for LLM context.
        
        Converts snake_case keys to Title Case and formats as bullet list.
        Used to provide LLM with current session context during response generation.
        
        Returns:
            str: Formatted bullet list of non-empty slots, or placeholder if empty
            
        Examples:
            >>> s = Session()
            >>> s.set_slot("company_name", "BT")
            >>> s.set_slot("service_type", "Dark Fibre")
            >>> "Company Name: BT" in s.slots_summary()
            True
        """
        lines = []
        for k, v in self.slots.items():
            if v and v.strip():
                nice = k.replace("_", " ").title()
                lines.append(f"- {nice}: {v}")
        return "\n".join(lines) if lines else "(No data collected yet)"

    def add_chat(self, role: str, content: str) -> None:
        """
        Add a message to the chat history with current timestamp.
        
        Args:
            role (str): Message role - typically "user", "assistant", or "system"
            content (str): The message text
            
        Returns:
            None
        """
        self.chat_history.append({
            "role": role,
            "content": content,
            "time": datetime.now().strftime("%H:%M"),
        })

    def set_slot(self, key: str, value: str) -> None:
        """
        Record a user answer in the session slots dictionary.
        
        Args:
            key (str): Field identifier (e.g., "company_name", "pricing_model")
            value (str): User's answer or default value
            
        Returns:
            None
        """
        self.slots[key] = value