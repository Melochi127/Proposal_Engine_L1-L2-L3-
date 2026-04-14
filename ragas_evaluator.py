"""
RAG Evaluator — Runs 30 benchmark queries against RAG retrieval.

Works with RAG pipeline:
    1. rag_ingest.py  -> builds ChromaDB + BM25
    2. This file  -> queries with RAG (hybrid retrieval)
    3. Scores keyword coverage + source accuracy per query
    4. Prints report by category, difficulty
    5. Saves evaluation_report.json

Usage:
    python ragas_evaluator.py                         # run all 30
    python ragas_evaluator.py --category risk_liability
    python ragas_evaluator.py --difficulty hard
    python ragas_evaluator.py --top_k 5
    python ragas_evaluator.py --output my_report.json
"""

import json
import time
import argparse
import sys
import os
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

from evaluation_benchmark import (
    QUERIES, DOCUMENT_MAP, BenchmarkQuery,
    Category, Difficulty,
    get_by_category, get_by_difficulty,
)

from rag_retriever import retrieve_hybrid, check_kb


# =============================================
#  RESULT DATA CLASS
# =============================================

@dataclass
class QueryResult:
    query_id: int
    query: str
    category: str
    difficulty: str
    ragas_focus: str
    retrieval_time_ms: float
    num_results: int
    avg_score: float
    source_diversity: int


# =============================================
#  SCORING FUNCTIONS
# =============================================

def score_keywords(context: str, expected_keywords: List[str]) -> float:
    """
    Score keyword coverage in retrieved context.
    Returns float 0-1: fraction of expected keywords found.
    """
    if not expected_keywords:
        return 1.0
    
    context_lower = context.lower()
    found = sum(1 for kw in expected_keywords if kw.lower() in context_lower)
    return found / len(expected_keywords)


def score_sources(retrieved_sources: List[str], expected_sources: List[str]) -> float:
    """
    Score source accuracy: what fraction of expected sources were retrieved?
    Returns float 0-1.
    """
    if not expected_sources:
        return 1.0
    
    found = sum(1 for exp_src in expected_sources if any(
        exp_src in ret_src for ret_src in retrieved_sources
    ))
    return found / len(expected_sources)


def evaluate_query(query: str, benchmark_query: BenchmarkQuery, top_k: int = 5) -> Dict[str, Any]:
    """
    Evaluate a single query against RAG.
    Returns scores on keyword coverage, source accuracy, and pass/fail.
    """
    start = time.time()
    docs = retrieve_hybrid(query, top_k=top_k)
    elapsed = time.time() - start
    
    # Extract context and sources
    context = "\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get("source", "unknown") for doc in docs]
    
    # Score
    kw_score = score_keywords(context, benchmark_query.expected_keywords)
    src_score = score_sources(sources, benchmark_query.expected_sources)
    avg_score = (kw_score + src_score) / 2
    
    # Pass threshold: 0.5 (50% average)
    passed = avg_score >= 0.5
    
    return {
        "query_id": benchmark_query.query_id,
        "query": query,
        "category": benchmark_query.category.value,
        "difficulty": benchmark_query.difficulty.value,
        "ragas_focus": benchmark_query.ragas_focus,
        "retrieval_time_ms": round(elapsed * 1000, 1),
        "num_results": len(docs),
        "keyword_coverage": round(kw_score, 3),
        "source_accuracy": round(src_score, 3),
        "avg_score": round(avg_score, 3),
        "passed": passed,
        "sources": sources[:5],  # Top 5 sources
    }


def generate_report(query_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate query results into summary report.
    """
    total = len(query_results)
    passed = sum(1 for q in query_results if q["passed"])
    pass_rate = passed / total if total > 0 else 0
    
    avg_kw = sum(q.get("keyword_coverage", 0) for q in query_results) / total if total > 0 else 0
    avg_src = sum(q.get("source_accuracy", 0) for q in query_results) / total if total > 0 else 0
    avg_time = sum(q.get("retrieval_time_ms", 0) for q in query_results) / total if total > 0 else 0
    avg_results = sum(q.get("num_results", 0) for q in query_results) / total if total > 0 else 0
    
    # By category
    by_category = {}
    for category in Category:
        cat_queries = [q for q in query_results if q["category"] == category.value]
        if cat_queries:
            cat_passed = sum(1 for q in cat_queries if q["passed"])
            by_category[category.value] = {
                "total": len(cat_queries),
                "passed": cat_passed,
                "pass_rate": round(cat_passed / len(cat_queries), 3),
                "avg_kw": round(sum(q.get("keyword_coverage", 0) for q in cat_queries) / len(cat_queries), 3),
                "avg_src": round(sum(q.get("source_accuracy", 0) for q in cat_queries) / len(cat_queries), 3),
            }
    
    # By difficulty
    by_difficulty = {}
    for difficulty in Difficulty:
        diff_queries = [q for q in query_results if q["difficulty"] == difficulty.value]
        if diff_queries:
            diff_passed = sum(1 for q in diff_queries if q["passed"])
            by_difficulty[difficulty.value] = {
                "total": len(diff_queries),
                "passed": diff_passed,
                "pass_rate": round(diff_passed / len(diff_queries), 3),
                "avg_kw": round(sum(q.get("keyword_coverage", 0) for q in diff_queries) / len(diff_queries), 3),
                "avg_src": round(sum(q.get("source_accuracy", 0) for q in diff_queries) / len(diff_queries), 3),
            }
    
    return {
        "metadata": {
            "model": "RAG",
            "total_queries": total,
            "date": time.strftime("%Y-%m-%d"),
        },
        "summary": {
            "total": total,
            "passed": passed,
            "pass_rate": round(pass_rate, 3),
            "avg_keyword_coverage": round(avg_kw, 3),
            "avg_source_accuracy": round(avg_src, 3),
            "avg_retrieval_time_ms": round(avg_time, 1),
            "avg_results": round(avg_results, 1),
        },
        "by_category": by_category,
        "by_difficulty": by_difficulty,
        "queries": query_results,
    }


# =============================================
#  MAIN EVALUATION LOOP
# =============================================

def main():
    parser = argparse.ArgumentParser(description="Evaluate RAG on benchmark queries")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--difficulty", type=str, help="Filter by difficulty (easy/medium/hard)")
    parser.add_argument("--top_k", type=int, default=5, help="Number of results to retrieve")
    parser.add_argument("--output", type=str, default="evaluation_report.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    # Check KB
    print("Checking knowledge base...")
    status = check_kb()
    print(f"KB Status: {status}\n")
    
    # Filter queries
    queries_to_eval = QUERIES
    
    if args.category:
        category_enum = Category[args.category.upper()]
        queries_to_eval = get_by_category(category_enum)
        print(f"Filtering by category: {args.category}")
    
    if args.difficulty:
        difficulty_enum = Difficulty[args.difficulty.upper()]
        queries_to_eval = [q for q in queries_to_eval if q.difficulty == difficulty_enum]
        print(f"Filtering by difficulty: {args.difficulty}")
    
    print(f"Evaluating {len(queries_to_eval)} queries with top_k={args.top_k}\n")
    
    # Evaluate
    results = []
    for i, benchmark_query in enumerate(queries_to_eval, 1):
        result = evaluate_query(benchmark_query.query, benchmark_query, top_k=args.top_k)
        results.append(result)
        
        status = "✅" if result["passed"] else "❌"
        print(f"{status} Q{result['query_id']}: {result['query'][:50]}...")
        print(f"   KW: {result['keyword_coverage']:.2f} | SRC: {result['source_accuracy']:.2f} | Time: {result['retrieval_time_ms']:.1f}ms")
    
    # Generate report
    report = generate_report(results)
    
    # Print summary
    print("\n" + "=" * 70)
    print("RAG EVALUATION REPORT")
    print("=" * 70)
    print(f"Total: {report['summary']['total']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Pass Rate: {report['summary']['pass_rate']*100:.1f}%")
    print(f"Avg Keyword Coverage: {report['summary']['avg_keyword_coverage']:.3f}")
    print(f"Avg Source Accuracy: {report['summary']['avg_source_accuracy']:.3f}")
    print(f"Avg Retrieval Time: {report['summary']['avg_retrieval_time_ms']:.1f}ms")
    
    # Save report
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n✅ Report saved to {args.output}")


if __name__ == "__main__":
    main()
