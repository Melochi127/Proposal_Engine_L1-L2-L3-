"""
Quick retrieval tests for RAG system.
Tests basic functionality: BM25, vector search, hybrid retrieval.
"""

import sys
import json
from typing import Dict, List

from rag_retriever import (
    retrieve_bm25,
    retrieve_vector,
    retrieve_hybrid,
    check_kb
)
from evaluation_benchmark import QUERIES


def test_kb_status() -> bool:
    """Test knowledge base initialization."""
    print("=" * 60)
    print("TEST 1: KB Status Check")
    print("=" * 60)
    
    status = check_kb()
    print(f"✅ KB Status: {status}")
    return True


def test_bm25_retrieval() -> bool:
    """Test BM25 keyword retrieval."""
    print("\n" + "=" * 60)
    print("TEST 2: BM25 Retrieval (Keyword Search)")
    print("=" * 60)
    
    query = "What are service level agreements?"
    results = retrieve_bm25(query, top_k=5)
    
    print(f"Query: {query}")
    print(f"Retrieved {len(results)} results:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.metadata.get('source', 'unknown')} - {doc.page_content[:80]}...")
    
    return len(results) > 0


def test_vector_retrieval() -> bool:
    """Test vector semantic retrieval."""
    print("\n" + "=" * 60)
    print("TEST 3: Vector Semantic Retrieval")
    print("=" * 60)
    
    query = "proposal generation steps"
    results = retrieve_vector(query, top_k=5)
    
    print(f"Query: {query}")
    print(f"Retrieved {len(results)} results:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.metadata.get('source', 'unknown')} - {doc.page_content[:80]}...")
    
    return len(results) > 0


def test_hybrid_retrieval() -> bool:
    """Test hybrid retrieval combining BM25 + vectors."""
    print("\n" + "=" * 60)
    print("TEST 4: Hybrid Retrieval (BM25 + Vector)")
    print("=" * 60)
    
    query = "contract penalties"
    results = retrieve_hybrid(query, top_k=5)
    
    print(f"Query: {query}")
    print(f"Retrieved {len(results)} results:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.metadata.get('source', 'unknown')} - {doc.page_content[:80]}...")
    
    return len(results) > 0


def test_benchmark_queries(num_queries: int = 5) -> Dict[str, float]:
    """Test retrieval on benchmark queries."""
    print("\n" + "=" * 60)
    print(f"TEST 5: Benchmark Queries (First {num_queries})")
    print("=" * 60)
    
    success = 0
    total = min(num_queries, len(QUERIES))
    
    for query_obj in QUERIES[:total]:
        results = retrieve_hybrid(query_obj.query, top_k=5)
        success += 1 if len(results) > 0 else 0
        
        status = "✅" if len(results) > 0 else "❌"
        print(f"{status} Q{query_obj.query_id}: {query_obj.query[:50]}... ({len(results)} results)")
    
    pass_rate = success / total if total > 0 else 0
    print(f"\nPass Rate: {pass_rate * 100:.1f}% ({success}/{total})")
    
    return {"pass_rate": pass_rate, "total": total, "passed": success}


def run_all_tests():
    """Run all retrieval tests."""
    print("\n" + "=" * 80)
    print("RAG RETRIEVAL TEST SUITE")
    print("=" * 80)
    
    tests = [
        ("KB Status", test_kb_status),
        ("BM25 Retrieval", test_bm25_retrieval),
        ("Vector Retrieval", test_vector_retrieval),
        ("Hybrid Retrieval", test_hybrid_retrieval),
        ("Benchmark Queries", lambda: test_benchmark_queries(5)),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = "PASS" if result else "FAIL"
        except Exception as e:
            results[test_name] = f"ERROR: {str(e)}"
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    for test_name, status in results.items():
        print(f"{test_name}: {status}")
    
    return results


if __name__ == "__main__":
    run_all_tests()
