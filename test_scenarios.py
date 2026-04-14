"""
End-to-end scenario tests for RAG system.
Tests real-world usage patterns and complex query sequences.
"""

import json
from typing import List, Dict
from rag_retriever import retrieve_hybrid
from evaluation_benchmark import QUERIES, Category, Difficulty


def scenario_1_contract_review():
    """Scenario: Contract review workflow."""
    print("\n" + "=" * 70)
    print("SCENARIO 1: Contract Review Workflow")
    print("=" * 70)
    
    scenario_queries = [
        "What are service level agreements?",
        "What penalties apply for breach?",
        "What are renewal clauses?",
        "What escalation procedures exist?",
    ]
    
    print("Use Case: Legal team reviewing contract terms")
    results = []
    
    for query in scenario_queries:
        docs = retrieve_hybrid(query, top_k=3)
        result = {
            "query": query,
            "retrieved": len(docs),
            "sources": [doc.metadata.get("source", "unknown") for doc in docs[:3]]
        }
        results.append(result)
        print(f"  ✓ {query[:50]}... → {len(docs)} results")
    
    return results


def scenario_2_proposal_generation():
    """Scenario: Proposal generation workflow."""
    print("\n" + "=" * 70)
    print("SCENARIO 2: Proposal Generation Workflow")
    print("=" * 70)
    
    scenario_queries = [
        "How do I generate an L1 proposal?",
        "What document types are supported?",
        "How do you validate commercial terms?",
        "What happens before service activation?",
    ]
    
    print("Use Case: Sales team creating proposals")
    results = []
    
    for query in scenario_queries:
        docs = retrieve_hybrid(query, top_k=3)
        result = {
            "query": query,
            "retrieved": len(docs),
            "sources": [doc.metadata.get("source", "unknown") for doc in docs[:3]]
        }
        results.append(result)
        print(f"  ✓ {query[:50]}... → {len(docs)} results")
    
    return results


def scenario_3_system_architecture():
    """Scenario: System architecture understanding."""
    print("\n" + "=" * 70)
    print("SCENARIO 3: System Architecture Deep Dive")
    print("=" * 70)
    
    scenario_queries = [
        "How is the knowledge base structured?",
        "How is the knowledge base updated?",
        "How are query results ranked and filtered?",
        "What redundancy mechanisms are in place?",
    ]
    
    print("Use Case: Engineering team understanding system")
    results = []
    
    for query in scenario_queries:
        docs = retrieve_hybrid(query, top_k=3)
        result = {
            "query": query,
            "retrieved": len(docs),
            "sources": [doc.metadata.get("source", "unknown") for doc in docs[:3]]
        }
        results.append(result)
        print(f"  ✓ {query[:50]}... → {len(docs)} results")
    
    return results


def scenario_4_risk_mitigation():
    """Scenario: Risk and compliance review."""
    print("\n" + "=" * 70)
    print("SCENARIO 4: Risk & Compliance Review")
    print("=" * 70)
    
    scenario_queries = [
        "What are liability limits?",
        "What maintenance windows are specified?",
        "What are data privacy requirements?",
        "What force majeure protections exist?",
    ]
    
    print("Use Case: Compliance team reviewing risk exposure")
    results = []
    
    for query in scenario_queries:
        docs = retrieve_hybrid(query, top_k=3)
        result = {
            "query": query,
            "retrieved": len(docs),
            "sources": [doc.metadata.get("source", "unknown") for doc in docs[:3]]
        }
        results.append(result)
        print(f"  ✓ {query[:50]}... → {len(docs)} results")
    
    return results


def test_category_retrieval():
    """Test retrieval across all categories."""
    print("\n" + "=" * 70)
    print("CATEGORY RETRIEVAL TEST")
    print("=" * 70)
    
    category_results = {}
    
    for category in [Category.CONTRACT_CLAUSES, Category.RISK_LIABILITY, 
                     Category.WIZARD_FLOW, Category.CROSS_CLAUSE_LOGIC,
                     Category.SYSTEM_ARCHITECTURE, Category.COMMERCIAL_TERMS]:
        queries = [q for q in QUERIES if q.category == category]
        success = 0
        
        for query_obj in queries:
            docs = retrieve_hybrid(query_obj.query, top_k=5)
            if len(docs) > 0:
                success += 1
        
        pass_rate = success / len(queries) if queries else 0
        category_results[category.value] = {
            "total": len(queries),
            "passed": success,
            "pass_rate": pass_rate
        }
        
        print(f"  {category.value}: {success}/{len(queries)} ({pass_rate*100:.1f}%)")
    
    return category_results


def test_difficulty_retrieval():
    """Test retrieval across difficulty levels."""
    print("\n" + "=" * 70)
    print("DIFFICULTY LEVEL TEST")
    print("=" * 70)
    
    difficulty_results = {}
    
    for difficulty in [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]:
        queries = [q for q in QUERIES if q.difficulty == difficulty]
        success = 0
        
        for query_obj in queries:
            docs = retrieve_hybrid(query_obj.query, top_k=5)
            if len(docs) > 0:
                success += 1
        
        pass_rate = success / len(queries) if queries else 0
        difficulty_results[difficulty.value] = {
            "total": len(queries),
            "passed": success,
            "pass_rate": pass_rate
        }
        
        print(f"  {difficulty.value}: {success}/{len(queries)} ({pass_rate*100:.1f}%)")
    
    return difficulty_results


def run_all_scenarios():
    """Run all scenario tests."""
    print("\n" + "=" * 80)
    print("RAG SCENARIO TEST SUITE")
    print("=" * 80)
    
    # Run workflow scenarios
    s1_results = scenario_1_contract_review()
    s2_results = scenario_2_proposal_generation()
    s3_results = scenario_3_system_architecture()
    s4_results = scenario_4_risk_mitigation()
    
    # Run category/difficulty tests
    cat_results = test_category_retrieval()
    diff_results = test_difficulty_retrieval()
    
    # Summary
    print("\n" + "=" * 80)
    print("SCENARIO TEST SUMMARY")
    print("=" * 80)
    print("✓ Scenario 1 (Contract Review): Complete")
    print("✓ Scenario 2 (Proposal Generation): Complete")
    print("✓ Scenario 3 (System Architecture): Complete")
    print("✓ Scenario 4 (Risk & Compliance): Complete")
    
    print("\n" + "=" * 80)
    print("OVERALL STATISTICS")
    print("=" * 80)
    
    # Calculate overall pass rate
    all_queries = [q for q in QUERIES]
    success = 0
    for query_obj in all_queries:
        docs = retrieve_hybrid(query_obj.query, top_k=5)
        if len(docs) > 0:
            success += 1
    
    overall_pass = success / len(all_queries) if all_queries else 0
    print(f"Overall Pass Rate: {overall_pass*100:.1f}% ({success}/{len(all_queries)} queries)")
    
    return {
        "scenarios": {
            "contract_review": len(s1_results),
            "proposal_generation": len(s2_results),
            "system_architecture": len(s3_results),
            "risk_compliance": len(s4_results),
        },
        "by_category": cat_results,
        "by_difficulty": diff_results,
        "overall_pass_rate": overall_pass
    }


if __name__ == "__main__":
    run_all_scenarios()
