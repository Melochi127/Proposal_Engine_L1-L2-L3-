import json
import os
import shutil
from proposal_agent import Agent
from rag_ingest import run_ingestion
from rag_retriever import retrieve_context, clear_cache

QUESTIONS_FILE = "eval_questions.json"

def keyword_hit(text, keywords):
    t = text.lower()
    return all(k.lower() in t for k in keywords)

def swap_corpus(src_folder, active_folder="rag_data"):
    if os.path.exists(active_folder):
        shutil.rmtree(active_folder)
    shutil.copytree(src_folder, active_folder)

def evaluate_corpus(corpus_folder):
    swap_corpus(corpus_folder)
    run_ingestion()
    clear_cache()

    agent = Agent()
    s = agent.create_session(level="L3", sub_sector="Dark Fibre")

    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)

    results = []

    for row in questions:
        q = row["question"]
        expected_keywords = row.get("expected_keywords", [])
        must_have_fact = row.get("must_have_fact", "")

        ctx, docs = retrieve_context(q, max_docs=4)
        retrieval_pass = 1 if keyword_hit(ctx, expected_keywords) else 0

        answer = agent.ask_rag(s, q)
        ans_lower = answer.lower()

        if must_have_fact and must_have_fact.lower() in ans_lower:
            answer_score = 1
        elif any(k.lower() in ans_lower for k in expected_keywords):
            answer_score = 0.5
        else:
            answer_score = 0

        grounded = 0 if "general telecom knowledge" in ans_lower else 1

        results.append({
            "id": row["id"],
            "question": q,
            "retrieval_pass": retrieval_pass,
            "answer_score": answer_score,
            "grounded": grounded,
            "answer": answer
        })

    return results

def summarise(results):
    n = len(results)
    retrieval = sum(r["retrieval_pass"] for r in results) / n
    answer_acc = sum(r["answer_score"] for r in results) / n
    grounded = sum(r["grounded"] for r in results) / n
    return {
        "questions": n,
        "retrieval_hit_at_4": retrieval,
        "answer_accuracy": answer_acc,
        "groundedness": grounded
    }

if __name__ == "__main__":
    for corpus in ["rag_data_3", "rag_data_10"]:
        results = evaluate_corpus(corpus)
        print(corpus, summarise(results))