"""
Benchmark suite for RAG/CRAG evaluation.

Defines 30 benchmark queries across 6 categories and 3 difficulty levels.
Provides scoring metrics: keyword coverage, source accuracy, pass/fail.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class Category(Enum):
    CONTRACT_CLAUSES = "contract_clauses"
    RISK_LIABILITY = "risk_liability"
    WIZARD_FLOW = "wizard_flow"
    CROSS_CLAUSE_LOGIC = "cross_clause_logic"
    SYSTEM_ARCHITECTURE = "system_architecture"
    COMMERCIAL_TERMS = "commercial_terms"


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class BenchmarkQuery:
    query_id: int
    query: str
    category: Category
    difficulty: Difficulty
    expected_keywords: List[str]
    expected_sources: List[str]
    ragas_focus: str


# Document mapping for source accuracy
DOCUMENT_MAP = {
    "contract_overview.md": "Contract Overview",
    "sla_terms.md": "Service Level Agreements",
    "proposal_wizard.md": "Proposal Generation Wizard",
    "l1_generation.md": "L1 Quick Proposal",
    "l2_generation.md": "L2 Standard Proposal",
    "l3_dark_fiber.md": "L3 Dark Fibre Proposal",
    "system_overview.md": "System Architecture Overview",
    "system_config.md": "System Configuration",
    "activation_checklist.md": "Service Activation Checklist",
    "cross_clause_rules.md": "Cross-Clause Validation Rules",
    "prompt_engineering.md": "LLM Prompt Templates",
    "config_management.md": "Configuration Management",
    "liability_clauses.md": "Liability Limitation Clauses",
    "risk_management.md": "Risk Management Strategy",
    "penalty_clauses.md": "Contract Penalties",
    "pricing_structure.md": "Pricing & Commercial Terms",
    "commercial_terms.md": "Commercial Terms Reference",
    "maintenance_policy.md": "Maintenance & Support",
    "kb_structure.md": "Knowledge Base Structure",
    "chroma_integration.md": "ChromaDB Integration",
    "validation_rules.md": "Term Validation Rules",
    "privacy_policy.md": "Data Privacy Requirements",
    "data_protection.md": "Data Protection Standards",
    "proposal_versioning.md": "Proposal Versioning",
    "escalation_procedures.md": "Escalation Procedures",
    "dispute_resolution.md": "Dispute Resolution",
    "l3_config.md": "L3 Advanced Configuration",
    "advanced_config.md": "Advanced Configuration",
    "maintenance_windows.md": "Maintenance Windows",
    "kb_update_process.md": "Knowledge Base Updates",
    "payment_terms.md": "Payment Terms",
    "negotiation_guidelines.md": "Negotiation Guidelines",
    "renewal_clauses.md": "Contract Renewal",
    "proposal_agent.md": "Proposal Agent Logic",
    "decision_logic.md": "Decision Making Logic",
    "force_majeure.md": "Force Majeure Clauses",
    "supported_types.md": "Supported Document Types",
    "encryption_config.md": "Encryption Configuration",
    "validation_engine.md": "Validation Engine",
    "ip_rights.md": "Intellectual Property Rights",
    "indemnification.md": "Indemnification Clauses",
}


QUERIES = [
    BenchmarkQuery(
        query_id=1,
        query="What are the service level agreements in the contract?",
        category=Category.CONTRACT_CLAUSES,
        difficulty=Difficulty.EASY,
        expected_keywords=["service level", "SLA", "agreement", "uptime"],
        expected_sources=["sla_terms.md", "contract_overview.md"],
        ragas_focus="faithfulness"
    ),
    BenchmarkQuery(
        query_id=2,
        query="How are liabilities limited in dark fiber agreements?",
        category=Category.RISK_LIABILITY,
        difficulty=Difficulty.HARD,
        expected_keywords=["liability", "limited", "dark fiber", "maximum"],
        expected_sources=["liability_clauses.md", "risk_management.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=3,
        query="Explain the L1 proposal generation flow",
        category=Category.WIZARD_FLOW,
        difficulty=Difficulty.EASY,
        expected_keywords=["L1", "proposal", "generation", "quick"],
        expected_sources=["proposal_wizard.md", "l1_generation.md"],
        ragas_focus="faithfulness"
    ),
    BenchmarkQuery(
        query_id=4,
        query="What must be checked before service activation?",
        category=Category.CROSS_CLAUSE_LOGIC,
        difficulty=Difficulty.MEDIUM,
        expected_keywords=["activation", "checklist", "validation", "check"],
        expected_sources=["activation_checklist.md", "system_config.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=5,
        query="How do BM25 and vector embeddings interact in retrieval?",
        category=Category.SYSTEM_ARCHITECTURE,
        difficulty=Difficulty.HARD,
        expected_keywords=["BM25", "embeddings", "retrieval", "hybrid"],
        expected_sources=["system_overview.md", "kb_structure.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=6,
        query="What are the pricing terms for dark fiber?",
        category=Category.COMMERCIAL_TERMS,
        difficulty=Difficulty.EASY,
        expected_keywords=["pricing", "terms", "dark fiber", "cost"],
        expected_sources=["pricing_structure.md", "commercial_terms.md"],
        ragas_focus="faithfulness"
    ),
    BenchmarkQuery(
        query_id=7,
        query="What penalties apply for contract breaches?",
        category=Category.CONTRACT_CLAUSES,
        difficulty=Difficulty.MEDIUM,
        expected_keywords=["penalty", "breach", "contract", "fine"],
        expected_sources=["penalty_clauses.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=8,
        query="How do I generate an L2 proposal?",
        category=Category.WIZARD_FLOW,
        difficulty=Difficulty.EASY,
        expected_keywords=["L2", "proposal", "generation", "standard"],
        expected_sources=["proposal_wizard.md", "l2_generation.md"],
        ragas_focus="faithfulness"
    ),
    BenchmarkQuery(
        query_id=9,
        query="What are cross-clause validation rules?",
        category=Category.CROSS_CLAUSE_LOGIC,
        difficulty=Difficulty.HARD,
        expected_keywords=["cross-clause", "validation", "rules", "constraint"],
        expected_sources=["cross_clause_rules.md", "validation_engine.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=10,
        query="What document types are supported?",
        category=Category.SYSTEM_ARCHITECTURE,
        difficulty=Difficulty.EASY,
        expected_keywords=["document", "types", "supported", "format"],
        expected_sources=["system_overview.md", "supported_types.md"],
        ragas_focus="faithfulness"
    ),
    BenchmarkQuery(
        query_id=11,
        query="What maintenance windows are specified?",
        category=Category.RISK_LIABILITY,
        difficulty=Difficulty.MEDIUM,
        expected_keywords=["maintenance", "window", "schedule", "downtime"],
        expected_sources=["maintenance_policy.md", "sla_terms.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=12,
        query="How is the knowledge base structured?",
        category=Category.SYSTEM_ARCHITECTURE,
        difficulty=Difficulty.MEDIUM,
        expected_keywords=["knowledge base", "structure", "architecture", "organization"],
        expected_sources=["kb_structure.md", "chroma_integration.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=13,
        query="What escalation procedures are defined?",
        category=Category.CONTRACT_CLAUSES,
        difficulty=Difficulty.HARD,
        expected_keywords=["escalation", "procedure", "steps", "contact"],
        expected_sources=["escalation_procedures.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=14,
        query="How do you validate commercial terms?",
        category=Category.COMMERCIAL_TERMS,
        difficulty=Difficulty.EASY,
        expected_keywords=["validate", "validation", "commercial", "terms"],
        expected_sources=["validation_rules.md", "commercial_terms.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=15,
        query="What are the data privacy requirements?",
        category=Category.RISK_LIABILITY,
        difficulty=Difficulty.HARD,
        expected_keywords=["privacy", "data", "requirements", "protection"],
        expected_sources=["privacy_policy.md", "data_protection.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=16,
        query="How do you handle proposal versioning?",
        category=Category.WIZARD_FLOW,
        difficulty=Difficulty.MEDIUM,
        expected_keywords=["versioning", "version", "proposal", "tracking"],
        expected_sources=["proposal_versioning.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=17,
        query="What redundancy mechanisms are in place?",
        category=Category.SYSTEM_ARCHITECTURE,
        difficulty=Difficulty.HARD,
        expected_keywords=["redundancy", "backup", "failover", "recovery"],
        expected_sources=["system_overview.md", "disaster_recovery.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=18,
        query="What dispute resolution mechanisms exist?",
        category=Category.CONTRACT_CLAUSES,
        difficulty=Difficulty.MEDIUM,
        expected_keywords=["dispute", "resolution", "arbitration", "mediation"],
        expected_sources=["dispute_resolution.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=19,
        query="How do you configure the L3 proposal?",
        category=Category.WIZARD_FLOW,
        difficulty=Difficulty.HARD,
        expected_keywords=["L3", "dark fiber", "configuration", "advanced"],
        expected_sources=["l3_dark_fiber.md", "advanced_config.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=20,
        query="What are the uptime guarantees?",
        category=Category.COMMERCIAL_TERMS,
        difficulty=Difficulty.EASY,
        expected_keywords=["uptime", "guarantee", "availability", "SLA"],
        expected_sources=["sla_terms.md", "uptime_guarantees.md"],
        ragas_focus="faithfulness"
    ),
    BenchmarkQuery(
        query_id=21,
        query="How are query results ranked and filtered?",
        category=Category.SYSTEM_ARCHITECTURE,
        difficulty=Difficulty.HARD,
        expected_keywords=["ranking", "filtering", "score", "relevance"],
        expected_sources=["kb_structure.md", "retrieval_ranking.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=22,
        query="What are the indemnification clauses?",
        category=Category.RISK_LIABILITY,
        difficulty=Difficulty.HARD,
        expected_keywords=["indemnification", "indemnify", "clause", "protection"],
        expected_sources=["indemnification.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=23,
        query="How is the knowledge base updated?",
        category=Category.SYSTEM_ARCHITECTURE,
        difficulty=Difficulty.MEDIUM,
        expected_keywords=["update", "knowledge base", "ingestion", "refresh"],
        expected_sources=["kb_update_process.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=24,
        query="What payment terms are negotiable?",
        category=Category.COMMERCIAL_TERMS,
        difficulty=Difficulty.HARD,
        expected_keywords=["payment", "negotiable", "flexible", "terms"],
        expected_sources=["payment_terms.md", "negotiation_guidelines.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=25,
        query="What are renewal clauses?",
        category=Category.CONTRACT_CLAUSES,
        difficulty=Difficulty.EASY,
        expected_keywords=["renewal", "clause", "contract", "extension"],
        expected_sources=["renewal_clauses.md"],
        ragas_focus="faithfulness"
    ),
    BenchmarkQuery(
        query_id=26,
        query="How does the proposal agent make decisions?",
        category=Category.CROSS_CLAUSE_LOGIC,
        difficulty=Difficulty.HARD,
        expected_keywords=["proposal agent", "decision", "logic", "algorithm"],
        expected_sources=["proposal_agent.md", "decision_logic.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=27,
        query="What force majeure protections exist?",
        category=Category.RISK_LIABILITY,
        difficulty=Difficulty.MEDIUM,
        expected_keywords=["force majeure", "protection", "unforeseeable", "clause"],
        expected_sources=["force_majeure.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=28,
        query="How do you validate cross-clause constraints?",
        category=Category.CROSS_CLAUSE_LOGIC,
        difficulty=Difficulty.MEDIUM,
        expected_keywords=["validate", "constraint", "cross-clause", "check"],
        expected_sources=["cross_clause_rules.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=29,
        query="What are the intellectual property rights?",
        category=Category.CONTRACT_CLAUSES,
        difficulty=Difficulty.HARD,
        expected_keywords=["intellectual property", "IP", "rights", "ownership"],
        expected_sources=["ip_rights.md"],
        ragas_focus="relevant"
    ),
    BenchmarkQuery(
        query_id=30,
        query="How is encryption configured in the system?",
        category=Category.SYSTEM_ARCHITECTURE,
        difficulty=Difficulty.MEDIUM,
        expected_keywords=["encryption", "configured", "security", "cipher"],
        expected_sources=["encryption_config.md"],
        ragas_focus="relevant"
    ),
]


def get_by_category(category: Category) -> List[BenchmarkQuery]:
    """Get all queries for a specific category."""
    return [q for q in QUERIES if q.category == category]


def get_by_difficulty(difficulty: Difficulty) -> List[BenchmarkQuery]:
    """Get all queries for a specific difficulty level."""
    return [q for q in QUERIES if q.difficulty == difficulty]


def get_by_ragas_focus(focus: str) -> List[BenchmarkQuery]:
    """Get all queries for a specific RAGAS focus area."""
    return [q for q in QUERIES if q.ragas_focus == focus]
