"""
CRAG Evaluator — Runs 30 benchmark queries against CRAG retrieval.

Works with CRAG pipeline:
    1. crag_ingest.py  -> builds ChromaDB + BM25
    2. This file  -> queries with CRAG (hybrid + corrective)
    3. Scores keyword coverage + source accuracy per query
    4. Prints report by category, difficulty
    5. Saves crag_evaluation_report.json

Usage:
    python crag_evaluator.py                         # run all 30
    python crag_evaluator.py --category risk_liability
    python crag_evaluator.py --difficulty hard
    python crag_evaluator.py --top_k 5
    python crag_evaluator.py --output my_crag_report.json
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

from crag_retriever import retrieve_crag, check_kb


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
    context_length: int
    keyword_coverage: float
    source_accuracy: float
    keywords_found: List[str]
    keywords_missing: List[str]
    sources_retrieved: List[str]
    target_hit: List[str]
    target_missed: List[str]
    passed: bool


# =============================================
#  SCORING FUNCTIONS
# =============================================

def score_keywords(context: str, expected: List[str]) -> Dict:
    """Check what % of expected keywords appear in retrieved context."""
    lower = context.lower()
    found = [k for k in expected if k.lower() in lower]
    missing = [k for k in expected if k.lower() not in lower]
    cov = len(found) / max(len(expected), 1)
    return {"coverage": round(cov, 4), "found": found, "missing": missing}


def score_sources(retrieved_sources: List[str], target_docs: List[str]) -> Dict:
    """Check if correct source documents were in retrieval results."""
    hit, missed = [], []
    for doc_id in target_docs:
        fname = DOCUMENT_MAP.get(doc_id, doc_id)
        # Match on first 20 chars of filename (handles truncation)
        target_prefix = fname[:20].lower()
        found = any(target_prefix in src.lower() for src in retrieved_sources)
        if found:
            hit.append(doc_id)
        else:
            missed.append(doc_id)
    acc = len(hit) / max(len(target_docs), 1)
    return {"accuracy": round(acc, 4), "hit": hit, "missed": missed}


# =============================================
#  MAIN EVALUATION
# =============================================

def evaluate_query(query: BenchmarkQuery, top_k: int) -> QueryResult:
    """Run CRAG retrieval and score."""
    start_time = time.time()
    docs = retrieve_crag(query.query, top_k=top_k)
    retrieval_time = (time.time() - start_time) * 1000

    # Extract context and sources
    context = "\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get("source", "unknown") for doc in docs]

    # Scores
    kw_score = score_keywords(context, query.expected_keywords)
    src_score = score_sources(sources, query.target_docs)

    # Other metrics
    source_diversity = len(set(sources))
    context_length = len(context)
    avg_score = (kw_score["coverage"] + src_score["accuracy"]) / 2
    passed = avg_score >= 0.5  # Arbitrary threshold

    return QueryResult(
        query_id=query.id,
        query=query.query,
        category=query.category.value,
        difficulty=query.difficulty.value,
        ragas_focus=query.ragas_focus,
        retrieval_time_ms=round(retrieval_time, 2),
        num_results=len(docs),
        avg_score=round(avg_score, 4),
        source_diversity=source_diversity,
        context_length=context_length,
        keyword_coverage=kw_score["coverage"],
        source_accuracy=src_score["accuracy"],
        keywords_found=kw_score["found"],
        keywords_missing=kw_score["missing"],
        sources_retrieved=sources,
        target_hit=src_score["hit"],
        target_missed=src_score["missed"],
        passed=passed,
    )


def main():
    parser = argparse.ArgumentParser(description="CRAG Evaluator")
    parser.add_argument("--category", choices=[c.value for c in Category], help="Filter by category")
    parser.add_argument("--difficulty", choices=[d.value for d in Difficulty], help="Filter by difficulty")
    parser.add_argument("--top_k", type=int, default=5, help="Number of docs to retrieve")
    parser.add_argument("--output", default="crag_evaluation_report.json", help="Output JSON file")
    args = parser.parse_args()

    # Check KB
    kb = check_kb()
    if not kb["exists"]:
        print(f"\n❌ CRAG KB not ready. Run crag_ingest.py first.")
        sys.exit(1)
    print(f"\n✅ CRAG KB ready: {kb['count']} chunks")

    # Filter queries
    queries = QUERIES
    if args.category:
        queries = get_by_category(Category(args.category))
    if args.difficulty:
        queries = get_by_difficulty(Difficulty(args.difficulty))

    print(f"\n🔍 Evaluating {len(queries)} queries with top_k={args.top_k}...")

    results = []
    for q in queries:
        result = evaluate_query(q, args.top_k)
        results.append(result)
        status = "✅" if result.passed else "❌"
        print(f"{status} Q{q.id}: {result.avg_score:.2f} (KW:{result.keyword_coverage:.2f}, SRC:{result.source_accuracy:.2f})")

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    avg_kw = sum(r.keyword_coverage for r in results) / total
    avg_src = sum(r.source_accuracy for r in results) / total
    avg_time = sum(r.retrieval_time_ms for r in results) / total

    summary = {
        "total_queries": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4),
        "avg_keyword_coverage": round(avg_kw, 4),
        "avg_source_accuracy": round(avg_src, 4),
        "avg_retrieval_time_ms": round(avg_time, 2),
        "top_k": args.top_k,
    }

    # By category
    categories = {}
    for cat in Category:
        cat_results = [r for r in results if r.category == cat.value]
        if cat_results:
            categories[cat.value] = {
                "count": len(cat_results),
                "avg_score": round(sum(r.avg_score for r in cat_results) / len(cat_results), 4),
                "pass_rate": round(sum(1 for r in cat_results if r.passed) / len(cat_results), 4),
            }

    # By difficulty
    difficulties = {}
    for diff in Difficulty:
        diff_results = [r for r in results if r.difficulty == diff.value]
        if diff_results:
            difficulties[diff.value] = {
                "count": len(diff_results),
                "avg_score": round(sum(r.avg_score for r in diff_results) / len(diff_results), 4),
                "pass_rate": round(sum(1 for r in diff_results if r.passed) / len(diff_results), 4),
            }

    report = {
        "summary": summary,
        "by_category": categories,
        "by_difficulty": difficulties,
        "results": [asdict(r) for r in results],
    }

    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n📊 CRAG Report saved to {args.output}")
    print(f"Pass Rate: {summary['pass_rate']:.1%} | Avg KW: {summary['avg_keyword_coverage']:.2f} | Avg SRC: {summary['avg_source_accuracy']:.2f}")


if __name__ == "__main__":
    main()